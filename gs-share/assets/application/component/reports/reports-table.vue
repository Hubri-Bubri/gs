<template>
  <div>
    <b-row align-v="center">
      <b-link style="text-decoration: none" @click="toog(table.id)">
        <div
          :id="'rp'+table.id"
          style="display: none; vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-down" font-scale="1" />
        </div>
        <div :id="'rm'+table.id" style="vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-up" font-scale="1" />
        </div>
      </b-link>
        <div
        contenteditable
        class="diveditable"
        @click.prevent.self
        @blur="tableRename($event.target.innerText, table.id, table.report)"
        v-html="table.report"></div>
    </b-row>
        <div :id="'report'+table.id">
            <b-table hover :items="reports_list" :fields="fields" small stacked="lg"
        show-empty no-border-collapse >
          <template #cell(#)="data">
            <div @click.prevent.stop="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(date)="row">
            <b-form-input size="sm"
            type="date"
            @change="sendDataTable(row.item.id, 'date', $event, row.index, row.item.date)"
            :value="row.item.date"
            placeholder="Enter date"
            :id="'date'+row.item.id" />
          </template>
          <template #cell(service)="row">
          <div contenteditable="plaintext-only"
          style="width:100%;padding-left:4px;"
          @click.prevent.self
          @blur="sendDataTable(row.item.id, 'service',
          $event.target.innerText, row.index, row.item.service)"
          :id="'service'+row.item.id"
          v-html="row.item.service" />
          </template>
          <template #cell(time)="row">
            <div
            contenteditable="plaintext-only"
            class="diveditable text-right"
            @click.prevent.stop="selectAll('time'+row.item.id)"
            @blur="toDigital($event.target.innerText, 'time', row.item.id, row.index, valueDigital(row.item.time))"
            :id="'time'+row.item.id" v-html="valueDigital(row.item.time)" />
           X {{(row.item.workers!=null)?(row.item.workers.split(',').length):1}}
          </template>
          <template #cell(workers)="row">
            <div v-if="(row.item.workers != 'Null')&row.item.workers != null">
              <div v-for="worker in row.item.workers.split(',')">
                <span>{{worker}}</span><br>
              </div>
            </div>
            <b-link size="sm"
            @click="sendDataTable(row.item.id, 'workers', ((selectedWorkers!=null)||(selectedWorkers!=''))?selectedWorkers.join():'Null', row.index, -1)">
            {{$t('reports.workers')}}
          </b-link>
          </template>
          <template #cell(delete)="row">
            <b-icon icon="trash" aria-hidden="true" @click.prevent.stop="delRow(row.item.id)"></b-icon>
          </template>
        </b-table>
        <b-row class="ttotalsumm">
               <b-col align-self="end" class="text-right" style="margin-right:22.6%">
               {{$t('projectDetail.total')}} {{ total(reports_list)  }}
              </b-col>
            </b-row>
        </div>
  </div>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
    props: ['table', 'workers', 'selectedWorkers'],
    data() {
        return {
          reports_list:[],
	  stopTimmer:false,
          oldarray: [],
          stopDis: false
        } //return
    }, //data
    computed: {
      fields(){
      return[
      {
        key: '#',
        label: '#',
        sortable: true,
        class:"cindex"
      },
      {
        key: 'date',
        label: this.$t('customerDetail.date'), 
        sortable: true,
        class:"cdate"
      },
      {
        key: 'service',
        label: this.$t('reports.service'), 
        sortable: true,
        class:"cservice"
      },
      {
        key: 'time',
        label: this.$t('reports.time'), 
        sortable: true,
        class:"ctime"
      },
      {
        key: 'workers',
        label: this.$t('reports.workers'), 
        sortable: true,
        class:"cworkers"
      },
      {
        key: 'delete',
        label: 'X',
        class:"cdel"
      }
    ]
  },
    total: function() {
      return function(value) {
        var summa = 0
        value.forEach(function(val) {
            summa += (val.time * ((val.workers!=null)?(val.workers.split(',').length):1))
        }) 
        return summa; //количество разрядов
      };
    },
    },
    methods: {
      tableRename(newVal, id, partName) {
            if(newVal!= partName){
                axios.get('/update_part_report', {
                  params: {
                    part_name: newVal,
                    id: id
                  }
                })
            }
        },
      toog(val){
      document.getElementById('rm'+val).style.display = document.getElementById('report'+val).style.display = (document.getElementById('report'+val).style.display=='none') ? '' : 'none'
      document.getElementById('rp'+val).style.display = (document.getElementById('rm'+val).style.display=='none') ? '' : 'none'
    },
      updateNameReport(newVal, id, partName) {
      if(newVal.target.innerText != partName){
        axios.get('/updateNameReport', {
          params: {
            nameReport: newVal.target.innerText.replace(/[\s]{2,}/, ''),
            id: id
          }
        })
      }
    }, 
      selectAll(id){
    function selectElementContents(el) {
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }

    var el = document.getElementById(id);
    selectElementContents(el);
    },
      valueDigital(model){
      var value = model
      
      if (value == null){
        value = '0.0'
      }
      var value = parseFloat(value)
      value = value.toString()
      value = value.replace('.',',')
      value = (value=='NaN')?0:value
      if (value.length < 3){
        value = '&nbsp;&nbsp;'+value
      }
      return value
    },
    toDigital(event, fild, id, index, old){
      var value = event.toString().replace(',','.');
      value = parseFloat(value);
      value = (value.toString()=='NaN')?0:value;
      this.sendDataTable(id, fild, value.toString(), index, old);
    },
      sendDataTable(id, fild, data, index, old){
        if (old!=data){
          data = (data=='')?'Null':data
                    axios.get('/updateReportsList', {
                        params: {
                          id: id,
                          fild: fild,
                          newData: data,
                          index: index,
                          tableId:this.table.id
                        }
                    })
      }
      },
      delRow(id) {
            if (confirm("Are you sure?")) {
                axios.get('/del_row_from_report', {
                      params: {
                        id: id,
                        tableId:this.table.id
                      }
                  })
                }
              },
  getRowsInReports(id) {
         axios.get('/get_reports_list', {
            params: {
               id: id
            }
         }).then(response => {
            this.reports_list = response.data;
         })
      },
      getFild(updateFild) {
        this.reports_list[updateFild.index][updateFild.fild] = updateFild.value;
      },
  },
  mounted() {
    this.getRowsInReports(this.table.id);
   }
}
</script>