<template>
  <b-container>
    <b-row>
      <b-col cols="11">
      <b-button  size="sm" @click="worker" >
            {{$t('calcTableGroup.workers')}}
          </b-button>
        </b-col>
      <b-col cols="1" class="text-right">
        <b-button size="sm" @click="$emit('openWindowPrint', 'Reports')">
          <b-icon icon="printer" aria-hidden="true"></b-icon>
        </b-button>
    </b-col>
  </b-row>
    <div v-for="(table, index) in tables" :key="table.id">
      <reports-table
      :table="table"
      :workers="workers"
      :selectedWorkers="selectedWorkers" 
      :ref="'report'+table.id"
      >
      </reports-table>
      <br>
    </div>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: [
    'selectedWorkers',
    'workers',
    'tmp',
    'id',
    'project'
    ],
    data() {
      return {
        tables:[]
      }
    },
  methods: {
    toogMeas(val){
      document.getElementById('measurementProtocolOpen'+val).style.display = document.getElementById('mestable'+val).style.display = (document.getElementById('mestable'+val).style.display=='none') ? '' : 'none'
      document.getElementById('measurementProtocolClose'+val).style.display = (document.getElementById('measurementProtocolOpen'+val).style.display=='none') ? '' : 'none'
    },

        worker() {
          this.$emit('worker')
        },
        getTablesInReports(id) {
        axios.get('/get_tables_in_reports', {
          params: {
            id: id
          }
        }).then(response => {
          this.tables = response.data;
          if(response.data.length==0){
        this.$emit('switchReports', false)
      } 
        })
      },
},
    mounted(){
      this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')
      if (delimetr[0] == 'update_part_report') {
        this.tables.filter((v)=>{
          if (v.id == delimetr[1]) {
            this.getTablesInReports(this.tmp.id)
          };
        })
      }
      if ((delimetr[0] == 'del_rows_for_report')) {
        delimetr[1].split(',').forEach((tableForReload)=>{
          this.$refs['report'+tableForReload][0].getRowsInReports(tableForReload)
          this.selectedTables=[]
        })
      }
      if (delimetr[0] == 'updateFildReport') {
        var updateFild = (JSON.parse(data.data.split('updateFildReport:')[1]))
        this.$refs['report'+updateFild.table_id][0].getFild(updateFild)
      }
   }
  }
}
</script>