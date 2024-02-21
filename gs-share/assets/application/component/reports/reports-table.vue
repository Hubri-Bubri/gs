<template>
  <div>
    <slot name="tableHead" :tableId="tableId" @click.prevent.self></slot>
    <input ref="unfocus" style="width: 0px; height: 0px; position: absolute; top: 0; left: 0; margin:0; padding:0; border: 0"></input>
        <div>
            <b-table hover :items="value.parts.reports_content" :fields="fields" small stacked="lg"
        show-empty no-border-collapse :id="'partx'+value.parts.id">
          <template #cell(#)="data">
            <div @click.prevent.stop="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(date)="row">
            <b-form-input size="sm"
            type="date"
            @change="sendDataTable(row.item.id, 'date', $event)"
            :value="row.item.date"
            placeholder="Enter date"
            :disabled="disablefild('date', row.item.id)"
            @focus.native="changeDisable('f', 'date', row.item.id)"
            @blur.native="changeDisable('b', 'date', row.item.id)"
            :id="'date'+row.item.id" />
          </template>
          <template #cell(service)="row">




<div contenteditable="plaintext-only"
style="width:100%;padding-left:4px;"
  @click.prevent.self
  @blur="sendDataTable(row.item.id, 'service', $event.target.innerText);changeDisable('b', 'service', row.item.id);"
  @focus="changeDisable('f', 'service', row.item.id)"
  :id="'service'+row.item.id" v-html="row.item.service" />


          </template>
          <template #cell(time)="row">
            <!-- <div
            :contenteditable="!disablefild('time', row.item.id)"
            class="diveditable"
            @click.prevent.self 
            @blur="toDigital($event.target.innerText, 'time', row.item.id);changeDisable('b', 'time', row.item.id);"
            @focus="changeDisable('f', 'time', row.item.id)"
            :id="'time'+row.item.id"  v-html="valueDigital(row.item.time)" /> -->



            <div
            :contenteditable="!disablefild('time', row.item.id)"
            class="diveditable text-right"
            @click.prevent.stop="selectAll('time'+row.item.id)"
            @blur="toDigital($event.target.innerText, 'time', row.item.id)"
            @focus="changeDisable('f', 'time', row.item.id)"
            :id="'time'+row.item.id" v-html="valueDigital(row.item.time)" />


           X {{(row.item.workers!=null)?(row.item.workers.split(',').length):1}}




          </template>
          <template #cell(workers)="row">
            <!-- <b-form-select class="text-center" :value="row.item.workers" :options="workers"
            @change="sendDataTable(row.item.id, 'workers', $event)" /> -->
            <div v-if="(row.item.workers != 'Null')&row.item.workers != null">
              <div v-for="worker in row.item.workers.split(',')">
                <span>{{worker}}</span><br>
              </div>
            </div>
            <b-link size="sm"
            @click="sendDataTable(row.item.id, 'workers', selectedWorkers?selectedWorkers.join():'Null')">
            {{$t('reports.workers')}}
          </b-link>
           


          </template>
          <template #cell(delete)="row">
            <b-icon icon="trash" aria-hidden="true" @click.prevent.stop="delRow(row.item.id)"></b-icon>
          </template>
        </b-table>
        <b-row class="ttotalsumm">
               <b-col align-self="end" class="text-right" style="margin-right:22.6%">
               {{$t('projectDetail.total')}} {{ total(value.parts.reports_content)  }}</b-col>
            </b-row>
        </div>
  </div>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
    props: ['value', 'tableId', 'workers',  'looks', 'selectedWorkers'],
    
    data() {
        return {

	  stopTimmer:false,
          oldarray: [],
          stopDis: false,
          // window: {
       
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
      var vm = this;
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
      // console.log(value)
      // value = value.replace(',','.')
      // console.log(1, value)
      var value = parseFloat(value)
      // console.log(2, value)
      value = value.toString()
      value = value.replace('.',',')
      value = (value=='NaN')?0:value
      if (value.length < 3){
        value = '&nbsp;&nbsp;'+value
        // console.log(4, value)
      }
      return value
    },
    toDigital(event, fild, id){
      var value = event.toString().replace(',','.');
      value = parseFloat(value);
      value = (value.toString()=='NaN')?0:value;
      // console.log(value);
      this.sendDataTable(id, fild, value.toString());
      this.changeDisable('b', fild, id);
    },
      disablefild(fild, id){
        var result = false
              this.looks.forEach((val)=>{
                    if (val.rows_id == id) {
                      if (val.fild == fild) {
                        result = true
                      }
                    }
                })
        if (this.stopDis==true) result = false
        return result
      },
      changeDisable(type_operation, fild, id){
        this.stopDis=(type_operation=='f')
        axios.get('/changeDisableTable', {
          params: {
            type_operation: type_operation,
            fild: fild,
            id: id,
            'user': this.$security.account['first_name']+'_'+this.$security.account['second_name']
          }
        })
        if ((type_operation == 'f') & (this.stopTimmer==false)){
          setTimeout(()=>{


          }, 15000);
        }
      if (type_operation == 'b'){
        this.stopTimmer=true
      }

      },
      sendDataTable(id, fild, data){
        
        data = (data=='')?'Null':data
        this.value.parts.reports_content.forEach((v)=>{
             if(v.id==id){
                  axios.get('/updateReportsList', {
                      params: {
                        id: id,
                        fild: fild,
                        newData: data
                      }
                  })
             }
        })
      },
      delRow(id) {
            if (confirm("Are you sure?")) {
                axios.get('/del_row_from_report', {
                      params: {
                        id: id
                      }
                  })
                }
        }

  }
}
</script>