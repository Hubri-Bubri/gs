<template>
  <b-container>
      <b-row align-v="center">
      <b-link style="text-decoration: none" @click="toog(table.id)">
        <div
          :id="'dp'+table.id"
          style="display: none; vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-down" font-scale="1" />
        </div>
        <div :id="'dm'+table.id" style="vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-up" font-scale="1" />
        </div>
      </b-link>
  
      <div :id="'s'+table.id" style="display: none;">
        <span v-show="table.summa!='0,00'" align-self="end" class="text-right">{{$t('projectDetail.total')}} {{table.summa}} €</span>
        <span v-show="table.alt_summa!='0,00'" align-self="end" class="text-right" > {{$t('projectDetail.totalAlternative')}} {{table.alt_summa}} €</span>
        &nbsp;|&nbsp;
      </div>
      <div
        contenteditable
        class="diveditable"
        @click.prevent.self
        @blur="tableRename($event.target.innerText, table.id, table.device)"
        v-html="table.device"></div>
    </b-row>
     <div visible :id="'dev'+table.id">
        <b-table-simple>
        <b-tr>
          <b-th class="text-center">#</b-th>
          <b-th class="text-center" style="">{{$t('measurement.location')}}</b-th>
          <b-th class="text-center" style="white-space:nowrap;">{{$t('measurement.type')}}</b-th>
          <b-th class="text-center" style="white-space:nowrap;">{{$t('measurement.number')}}</b-th>
          <b-th class="text-right" style="white-space:nowrap;">{{$t('measurement.useInHour')}} [KW]</b-th>
          <b-th class="text-right" style="white-space:nowrap;" colspan="2">{{$t('measurement.timeUsed')}}</b-th>
          <b-th class="text-right" style="white-space:nowrap;">{{$t('measurement.target')}} [h]</b-th>
          <b-th class="text-right" style="white-space:nowrap;">{{$t('measurement.actual')}} [h]</b-th>
          <b-th class="text-right" style="white-space:nowrap;">{{$t('measurement.target')}} [KW]</b-th>
          <b-th class="text-right" style="white-space:nowrap;">{{$t('measurement.actual')}} [KW]</b-th>
          <b-th class="text-right" style="white-space:nowrap;">i</b-th>
          <b-th class="text-right" style="white-space:nowrap;">X</b-th>
        </b-tr>
        <template v-for="(content, subIndex) in device_list">
         <b-tr>
            <b-td style="background:#e9ecef;white-space:nowrap;">{{(subIndex+1)}}</b-td>
            <b-td><b-input :value="content.location" class="cForm-input"  @change="updateDeviceList(subIndex, $event, 'location', content.id, content.location)"></b-input></b-td>
            <b-td style="background:#e9ecef;white-space:nowrap;">{{content.designation}}</b-td>
            <b-td style="background:#e9ecef;white-space:nowrap;">{{content.serial}}</b-td>
            <b-td style="background:#e9ecef;white-space:nowrap;" class="text-right">{{(content.kilowatt.replace(',','.')/1000).toFixed(2).replace('.',',')}}</b-td>
            <b-td class="text-right" style="white-space:nowra" colspan="2">{{content.fdate?toTime(difTime(content.sdate, content.fdate, 'seconds')):'Not Set'}}</b-td>
            <b-td class="text-right">{{content.fdate?difTime(content.sdate, content.fdate, 'hours'):'Not Set'}}</b-td>
            <b-td class="text-right">{{content.fmReading?(content.fmReading-content.smReading).toFixed(2).replace('.',','):'Not Set'}}</b-td>
            <b-td class="text-right">{{content.fdate?(difTime(content.sdate, content.fdate, 'hours') * (content.kilowatt.replace(',','.')/1000)).toFixed(2).replace('.',','):'Not Set'}}</b-td>
            <b-td class="text-right">{{content.fmReading?((content.fmReading-content.smReading)*(content.kilowatt.replace(',','.')/1000)).toFixed(2).replace('.',','):'Not Set'}}</b-td>
            <b-td class="text-right">
              <b-link style="text-decoration: none;font-weight: normal;" @click="showRowFunc(content.id)?showRows.splice(showRows.indexOf(content.id), 1):showRows.push(content.id)">
               {{showRowFunc(content.id)?'-':'+'}}
              </b-link>
            </b-td>
            <b-td class="text-right">
              <b-icon icon="trash" aria-hidden="true" style="cursor: pointer;" @click="subPartDel(content.id, subIndex);"></b-icon>
            </b-td>
          </b-tr>
          <b-tr v-show="showRowFunc(content.id)" >
            <b-th colspan="1" class="text-center"></b-th>
            <b-th colspan="2" class="text-center" style="padding-top: 5px;">{{$t('measurement.measurement')}}</b-th>
            <b-th colspan="2" class="text-center">{{$t('customerDetail.date')}}</b-th>
            <b-th colspan="4" class="text-center">{{$t('calcTableGroup.workers')}}</b-th>
            <b-th colspan="2" class="text-center" style="white-space:nowrap;">{{$t('measurement.meterReading')}}</b-th>
            <b-th colspan="2"></b-th>
          </b-tr>
            <b-tr v-show="showRowFunc(content.id)" >
                <b-td colspan="1" class="text-center">1</b-td>
                <b-td colspan="2" class="text-center" style="padding-top: 5px;">{{$t('measurement.installation')}}</b-td>
                <b-td colspan="2" class="text-center">
                  <VueCtkDateTimePicker format="YYYY-MM-DD H:mm" no-label noClearButton  minute-interval="10"
                  v-model="content.sdate" @input="updateDeviceList(subIndex, $event, 'sdate', content.id, -1)"/>
                </b-td>
                <b-td colspan="4" class="text-center">
              <b-dropdown
                size="sm"
                :text="((content.sworker=='')||(content.sworker==null))?'---':content.sworker"
                variant="link"
                no-caret
                class="maxHeight outUnderline">
                <b-dropdown-item-button
                  @click="updateDeviceList(subIndex, '---', 'sworker', content.id, content.sworker);"
                  >---</b-dropdown-item-button>
                <b-dropdown-item-button
                  :key="worker"
                  v-for="worker in workers"
                  @click="updateDeviceList(subIndex, worker, 'sworker', content.id, content.sworker);">
                  {{worker}}
                </b-dropdown-item-button>
              </b-dropdown>
                </b-td>
                <b-td colspan="2" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.smReading.replace('.',',')"
                  @change="updateDeviceList(subIndex, $event.replace(',','.'), 'smReading', content.id, content.smReading.replace('.',','))"/></b-td>
                <b-td colspan="2"></b-td>
            </b-tr>
         <b-tr v-for="(row, index) in content.subEquel"  v-show="showRowFunc(content.id)" :key="row.id">
                <b-td colspan="1" class="text-center">{{(index+2)}}</b-td>
                <b-td colspan="2" class="text-center" style="padding-top: 5px;">{{$t('measurement.intermediate')}}</b-td>
                <b-td colspan="2" class="text-center">
                  <VueCtkDateTimePicker format="YYYY-MM-DD H:mm" no-label noClearButton minute-interval="10"
                  :min-date="(content.subEquel[index-1]!=undefined)?content.subEquel[index-1].date:content.sdate"
                  v-model="row.date" @input="updateDeviceIntern(subIndex, index, $event, 'date', row.id, -1)"/>
                </b-td>
                <b-td colspan="4" class="text-center">
              <b-dropdown
                size="sm"
                :text="((row.worker=='')||(row.worker==null))?'---':row.worker"
                variant="link"
                no-caret
                class="maxHeight outUnderline">
                <b-dropdown-item-button
                  @click="updateDeviceIntern(subIndex, index, '---', 'worker', row.id, row.worker);"
                  >---</b-dropdown-item-button>
                <b-dropdown-item-button
                  :key="worker"
                  v-for="worker in workers"
                  @click="updateDeviceIntern(subIndex, index, worker, 'worker', row.id, row.worker);">
                  {{worker}}
                </b-dropdown-item-button>
              </b-dropdown>
                </b-td>
                <b-td colspan="2" class="text-center" style="white-space:nowrap;"><b-input :value="row.mReading.replace('.',',')"
                  @change="updateDeviceIntern(subIndex, index, $event.replace(',','.'), 'mReading', row.id ,row.mReading.replace('.',','))" style="text-align: center"/></b-td>
                <b-td colspan="2" class="text-right">
                  <b-icon icon="trash" aria-hidden="true" style="cursor: pointer;" @click="delmeasrow(row.id)"></b-icon>
                </b-td>
            </b-tr>
            <b-tr v-show="showRowFunc(content.id)">
                <b-td colspan="1" class="text-center">{{content.subEquel.length+2}}</b-td>
                <b-td colspan="2" class="text-center" style="padding-top: 5px;">{{$t('measurement.dismounting')}}</b-td>
                <b-td colspan="2" class="text-center">
                  <VueCtkDateTimePicker format="YYYY-MM-DD H:mm" no-label noClearButton  minute-interval="10"
                  :min-date="(content.subEquel[content.subEquel.length-1]!=undefined)?content.subEquel[content.subEquel.length-1].date:content.sdate"
                  v-model="content.fdate" @input="updateDeviceList(subIndex, $event, 'fdate', content.id, -1)"/>
                </b-td>
                <b-td colspan="4" class="text-center">
              <b-dropdown
                size="sm"
                :text="((content.fworker=='')||(content.fworker==null))?'---':content.fworker"
                variant="link"
                no-caret
                class="maxHeight outUnderline">
                <b-dropdown-item-button
                  @click="updateDeviceIntern(subIndex, '---', 'fworker', content.id, content.fworker);"
                  >---</b-dropdown-item-button>
                <b-dropdown-item-button
                  :key="worker"
                  v-for="worker in workers"
                  @click="updateDeviceList(subIndex, worker, 'fworker', content.id, content.fworker);">
                  {{worker}}
                </b-dropdown-item-button>
              </b-dropdown>
                </b-td>
                <b-td colspan="2" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.fmReading.replace('.',',')" @change="updateDeviceList(subIndex, $event.replace(',','.'), 'fmReading', content.id, content.fmReading.replace('.',','))"/></b-td>
                <b-td colspan="2"></b-td>
            </b-tr>
          <b-tr v-show="showRowFunc(content.id)">
            <b-td class="text-center" style="border:0px;"><b-link @click="addmeasrow(content.id)" style="text-decoration: none !important;">+</b-link><br><br></b-td>
            <b-td colspan="12"></b-td>
          </b-tr>
        </template>
         <b-tr>
            <b-td colspan="6" class="text-center"><b>{{$t('measurement.period')}} {{fromTo(device_list)}}</b></b-td>
            <b-td class="text-right"><b>{{$t('topMenu.general')}}</b></b-td>
            <b-td class="text-right"><b>{{sumTH(device_list)}}</b></b-td>
            <b-td class="text-right"><b>{{sumAH(device_list)}}</b></b-td>
            <b-td class="text-right"><b>{{sumTKW(device_list)}}</b></b-td>
            <b-td class="text-right"><b>{{sumAKW(device_list)}}</b></b-td>
            <b-td colspan="2"></b-td>
          </b-tr>
      </b-table-simple>
    </div>
  </b-container>
</template>
<script type="text/javascript">
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import moment from 'moment';
import axios from 'axios';
export default {
  components: { VueCtkDateTimePicker },
  props: ['table', 'workers'],
    data() {
      return {
        showRows:[],
        device_list:[]
      }
    },
  methods: {
    toog(val){
      document.getElementById('dm'+val).style.display = document.getElementById('dev'+val).style.display = (document.getElementById('dev'+val).style.display=='none') ? '' : 'none'
      document.getElementById('dp'+val).style.display = (document.getElementById('dm'+val).style.display=='none') ? '' : 'none'
    },

fromTo(val){
  function formatDate(date) {
  if (date!=undefined){
  let dd = date.getDate();
  dd < 10 ? dd = '0' + dd : '';
  let mm = date.getMonth() + 1;
  mm < 10 ? mm = '0' + mm : '';
  let yy = date.getFullYear();
  return  dd+'.'+mm+'.'+yy;
  }}
  var from = [];
  var to =[];
  val.forEach((v)=>{
    from.push(new Date(v.sdate));
    to.push(new Date(v.fdate));
  });
  var fromSorted = from.sort((a, b) => a-b)
  var toSorted = to.sort((a, b) => b-a)
  return (this.$t('measurement.from')+' '+formatDate(fromSorted[0])+' '+this.$t('measurement.to')+' '+formatDate(toSorted[0]));
},
sumTH(val){
 var start = 0;
  val.forEach((v)=>{
    var hours = v.fdate?this.difTime(v.sdate, v.fdate, 'hours'):0
    start = start + hours
  });
  return start;
},
sumAH(val){
 var start = 0;
  val.forEach((v)=>{
    var hours = v.fmReading?(v.fmReading-v.smReading):0
    start = start + hours
  });
  return start.toFixed(2).replace('.',',');
},
sumTKW(val){
 var start = 0;
  val.forEach((v)=>{
    var kw = v.fdate?(this.difTime(v.sdate, v.fdate, 'hours')*(v.kilowatt.replace(',','.')/1000)):0
    start = start + kw
  });
  return start.toFixed(2).replace('.',',');
},
sumAKW(val){
 var start = 0;
  val.forEach((v)=>{
    var kw = v.fmReading?((v.fmReading-v.smReading)*(v.kilowatt.replace(',','.')/1000)):0
    start = start + kw
  });
  return start.toFixed(2).replace('.',',');
},
toTime(seconds){
var seconds = Number(seconds)
var d = Math.floor(seconds / (3600*24))
var h = Math.floor(seconds % (3600*24) / 3600)
var m = Math.floor(seconds % 3600 / 60)
var s = Math.floor(seconds % 60)
var dDisplay = d > 0 ? d + (d == 1 ? " day " : " days ") : ""
var hDisplay = h +':'
var mDisplay = m +'h'
var result = dDisplay + hDisplay + mDisplay
return result
  },
  difTime(start, end, t){
    var fend=end?end:moment().format("YYYY-MM-DD HH:mm:ss")
    var diffrent = moment(fend,"YYYY-MM-DD HH:mm").diff(moment(start,"YYYY-MM-DD HH:mm"), t)
    return diffrent
  },
  updateDeviceIntern(subIndex, index, newData, fild, id, old){
    if (old!=newData){
      axios.get('/updateDeviceIntern', {params: {
        subIndex:subIndex,
        index:index,
        tableId: this.table.id,
        newData: newData,
        fild: fild,
        id: id
      }})
    }
  },
  updateDeviceList(index, newData, fild, id, old){
     if (old!=newData){
      axios.get('/updateDeviceList', {
        params: {
          tableId: this.table.id,
          index:index,
          newData: newData,
          fild: fild,
          id: id
      }
    })
   }
  },
  delmeasrow(id){
      if (confirm("Are you sure?")) {
        axios.get('/delmeasrow', {
          params: {
            id: id,
            tableId: this.table.id
          }
        })
      }
    },
    addmeasrow(id){
      axios.get('/addMeasrow', {
        params: {
          id: id,
          tableId: this.table.id
        }
      })
    },
    showRowFunc(val){
      var ret = false
      this.showRows.filter((v)=>{
        if (val == v){
          ret = true
        }
      })
      return ret
    },
    subPartDel(subDel_id, subIndex) {
      if (confirm("Are you sure?")) {
        axios.get('/del_row_from_devices', {
          params: {
            id: subDel_id,
            tableId: this.table.id
          }
        })
      }
    },
    tableRename(newVal, id, partName) {
            if(newVal!= partName){
                axios.get('/update_part_device', {
                  params: {
                    part_name: newVal,
                    id: id
                  }
                })
            }
        },
    getRowsInDevice(id) {
         axios.get('/get_device_list', {
            params: {
               id: id
            }
         }).then(response => {
            this.device_list = response.data;
         })
      },
      getFild(updateFild) {
        this.device_list[updateFild.index][updateFild.fild] = updateFild.value;
      },
      getFildMeasurement(updateFild) {
        this.device_list[updateFild.subIndex].subEquel[updateFild.index][updateFild.fild] = updateFild.value;
      },
  },
  mounted() {
    this.getRowsInDevice(this.table.id);
   }
}
</script>