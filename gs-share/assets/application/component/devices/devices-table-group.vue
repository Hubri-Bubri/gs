<template>
  <b-container>
    <b-row align-h="end">
    <print v-if="tmp.typeOfHead == 'Devices'"
    :windowPrint="windowPrint"
    :selectedCornty="selectedCornty"
    :project="project" :tmp="tmp"
    :account="account" :id="pid"

    :partx="[]" :head="tmp.typeOfHead"
    :addtaxColapsel="false"
    :workers="workers" :comments="comments"
    :customer="customer"
    :person="person"
    :selectCustomer="selectCustomer"
    :selectPerson="selectPerson"
    :selectedDocsList="selectedDocsList"
    :addPdfs="addPdfs"
    :makemodalpdf="makemodalpdf"
    :typeDocsList="typeDocsList"
    @selectedDocs="selectedDocs"
    @addPdf="addPdf"
    @addPdfSep="addPdfSep"
    @printPdf="printPdf"
    @preview="preview"
    @printOffer="printOffer"
    @hideWindowPrint="hideWindowPrint"
    ref="print" 
    >
    </print>
  </b-row>
    <div v-for="table in tables" :key="table.id">
      <devices-table
      :table="table"
      :workers="workers"
      :ref="'deviceTable'+table.id">
      </devices-table>
      <devices-measurement
      :table="table"
      :ref="'measurement'+table.id">
      </devices-measurement>
      <br>
    </div>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: [
    'workers',
    'selectedDocsList',
    'addPdfs',
    'makemodalpdf',
    'typeDocsList',
    'windowPrint',
    'pid',
    'selectedCornty',
    'project',
    'tmp',
    'comments',
    'account',
    'head',
    'id',
    'customer',
    'person',
    'selectCustomer',
    'selectPerson'
    ],
    data() {
      return {
        tables:[]
      }
    },
  methods: {

    selectedDocs(event){
      this.$emit('selectedDocs', event)
    },
    addPdf(){
      this.$emit('addPdf')
    },
    addPdfSep(){
      this.$emit('addPdfSep')
    },
    printPdf(){
      this.$emit('printPdf')
    },
    preview(){
      this.$emit('preview')
    },
    printOffer(){
      this.$emit('printOffer')
    },
    hideWindowPrint(){
      this.$emit('hideWindowPrint')
    },
    openWindowPrint(){
      this.$emit('openWindowPrint')
    },
    updateNameDevice(newVal, id, partName) {
      if(newVal.target.innerText != partName){
        axios.get('/updateNameDevice', {
          params: {
            nameDevice: newVal.target.innerText.replace(/[\s]{2,}/, ''),
            id: id
          }
        })
      }
    }, 
    // showTable(){
    //   return this.value.filter((v)=>{
    //     if(this.tmp.device.length>0){
    //       return v
    //     }
    //   })
    // },

getTablesInDevices(id) {
  axios.get('/get_tables_in_devices', {
    params: {
      id: id
    }
    }).then(response => {
      this.tables = response.data;
      if(response.data.length==0){
        this.$emit('switchDevices', false)
      } 
    })
}
},
mounted(){

    this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')

      if (delimetr[0] == 'update_part_device') {
        this.tables.filter((v)=>{
          if (v.id == delimetr[1]) {
            this.getTablesInDevices(this.tmp.id)
          };
        })
      }
      if ((delimetr[0] == 'send_device') || (delimetr[0] == 'del_row_device') || (delimetr[0] == 'add_rows_for_devices') || (delimetr[0] == 'del_rows_for_devices')) {
        delimetr[1].split(',').forEach((tableForReload)=>{
          this.$refs['deviceTable'+tableForReload][0].getRowsInDevice(tableForReload)
          this.selectedTables=[]
        })
      }
      if (delimetr[0] == 'updateFildDevice') {
        var updateFild = (JSON.parse(data.data.split('updateFildDevice:')[1]))
        this.$refs['deviceTable'+updateFild.table_id][0].getFild(updateFild)
      }
      if (delimetr[0] == 'updateFildMeasurement') {
        var updateFild = (JSON.parse(data.data.split('updateFildMeasurement:')[1]))
        this.$refs['deviceTable'+updateFild.table_id][0].getFildMeasurement(updateFild)
      }
      if ((delimetr[0] == 'add_rows_MeasureProtocol') || (delimetr[0] == 'del_rows_MeasureProtocol')) {
        delimetr[1].split(',').forEach((tableForReload)=>{
          this.$refs['measurement'+tableForReload][0].getRowsInMeasureProtocol(tableForReload)
          this.selectedTables=[]
        })
      }
      if (delimetr[0] == 'updateFildMeasureProtocol') {
        var updateFild = (JSON.parse(data.data.split('updateFildMeasureProtocol:')[1]))
        this.$refs['measurement'+updateFild.table_id][0].getFild(updateFild)
      }
   }
  }
}
</script>