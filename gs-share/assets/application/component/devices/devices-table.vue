<template>
  <b-container fluid>
    <slot name="tableHead" :tableId="tableId" ></slot>
     <b-collapse visible :id="'dev'+tableId">
      <table class="tableProject table b-table">
        <tr>
          <th class="text-center">#</th>
          <th class="text-center" style="width:110px;" >Location</th>
          <th class="text-center"  style="white-space:nowrap;">Device type</th>
          <th class="text-center"  style="white-space:nowrap;">Device no.</th>
          <th class="text-right" style="white-space:nowrap;width:100px;">Use in hour [KW]</th>
          <th class="text-right" style="white-space:nowrap;width:100px;" colspan="2">Time Used</th>
          <th class="text-right" style="white-space:nowrap;">Target [h]&nbsp;</th>
          <th class="text-right" style="white-space:nowrap;">Actual [h]&nbsp;</th>
          <th class="text-right" style="white-space:nowrap;">Target [KW]&nbsp;</th>
          <th class="text-right" style="white-space:nowrap;">Actual [KW]&nbsp;</th>
          <th class="text-right" style="white-space:nowrap;">i&nbsp;</th>
          <th class="text-right" style="white-space:nowrap;">Delete</th>
        </tr>
        <template v-for="(content, subIndex) in value.parts.devices_content">
         <tr>
            <td style="background:#e9ecef;white-space:nowrap;">{{(subIndex+1)}}&nbsp;</td>
            <td><b-input :value="content.location" class="cForm-input"  @change="updateDeviceList($event, 'location', content.id)"></b-input></td>
            <td style="background:#e9ecef;white-space:nowrap;">&nbsp;{{content.designation}}</td>
            <td style="background:#e9ecef;white-space:nowrap;">{{content.serial}}</td>
            <td style="background:#e9ecef;white-space:nowrap;" class="text-right">{{(content.kilowatt.replace(',','.')/1000).toFixed(2).replace('.',',')}}</td>
            <td class="text-right" style="white-space:nowra" colspan="2">{{content.fdate?toTime(difTime(content.sdate, content.fdate, 'seconds')):'Not Set'}}</td>
            <td class="text-right">{{content.fdate?difTime(content.sdate, content.fdate, 'hours'):'Not Set'}}</td>
            <td class="text-right">{{content.fmReading?(content.fmReading-content.smReading).toFixed(2).replace('.',','):'Not Set'}}</td>
            <td class="text-right">{{content.fdate?(difTime(content.sdate, content.fdate, 'hours') * (content.kilowatt.replace(',','.')/1000)).toFixed(2).replace('.',','):'Not Set'}}</td>
            <td class="text-right">{{content.fmReading?((content.fmReading-content.smReading)*(content.kilowatt.replace(',','.')/1000)).toFixed(2).replace('.',','):'Not Set'}}</td>
            <td class="text-right">
              <b-link style="text-decoration: none;font-weight: normal;" @click="showRowFunc(content.id)?showRows.splice(showRows.indexOf(content.id), 1):showRows.push(content.id)">
                &nbsp;&nbsp;&nbsp;{{showRowFunc(content.id)?'-':'+'}}
              </b-link>
            </td>
            <td class="text-right" style=""><b-link  @click="subPartDel(content.id, subIndex);" class="fas fa-trash fa-w-16" />&nbsp;&nbsp;&nbsp;</td>
          </tr>
          <tr v-show="showRowFunc(content.id)">
                <th colspan="1" class="text-center"></th>
                <th colspan="2" class="text-center" style="padding-top: 5px;">Measurement</th>
                <th colspan="2" class="text-center">Date</th>
                <th colspan="4" class="text-center">Worker</th>
                <th colspan="2" class="text-center" style="white-space:nowrap;">Meter reading</th>
<!--                 <th colspan="1" class="text-center" style="white-space:nowrap;">W-dielectric</th>
                <th colspan="1" class="text-center" style="white-space:nowrap;">W-resistance</th>
                <th colspan="1" class="text-center" style="white-space:nowrap;">B-dielectric</th>
                <th colspan="1" class="text-center" style="white-space:nowrap;">B-resistance</th> -->
                <th colspan="2"></th>
          </tr>

            <tr v-show="showRowFunc(content.id)">
                <td colspan="1" class="text-center">1</td>
                <td colspan="2" class="text-center" style="padding-top: 5px;">Installation</td>
                <td colspan="2" class="text-center">
                  <VueCtkDateTimePicker class="cForm-input" style="padding:0px;" format="YYYY-MM-DD H:mm" no-label noClearButton  minute-interval="10"
                  v-model="content.sdate"  @input="updateDeviceList($event, 'sdate', content.id)"/>
                </td>
                <td colspan="4" class="text-center"><b-form-select class="customButton"  :value="content.sworker" :options="workers"  @change="updateDeviceList($event, 'sworker', content.id)"/></td>
                <td colspan="2" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.smReading.replace('.',',')"  @change="updateDeviceList($event.replace(',','.'), 'smReading', content.id)"/></td>
<!--                 <td colspan="1" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.swDielectric.replace('.',',').replace('.',',')"  @change="updateDeviceList($event.replace(',','.'), 'swDielectric', content.id)"/></td>
                <td colspan="1" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.swResistance.replace('.',',')"  @change="updateDeviceList($event.replace(',','.'), 'swResistance', content.id)"/></td>
                <td colspan="1" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.sbDielectric.replace('.',',')"  @change="updateDeviceList($event.replace(',','.'), 'sbDielectric', content.id)"/></td>
                <td colspan="1" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.sbResistance.replace('.',',')"  @change="updateDeviceList($event.replace(',','.'), 'sbResistance', content.id)"/></td> -->
                <td colspan="2"></td>
            </tr>

         <tr v-for="(row, index) in content.subEquel"  v-show="showRowFunc(content.id)">
                <td colspan="1" class="text-center">{{(index+2)}}</td>
                <td colspan="2" class="text-center" style="padding-top: 5px;">Intermediate</td>
                <td colspan="2" class="text-center">
                  <VueCtkDateTimePicker class="cForm-input"  style="padding:0px" format="YYYY-MM-DD H:mm" no-label noClearButton minute-interval="10"
                  :min-date="(content.subEquel[index-1]!=undefined)?content.subEquel[index-1].date:content.sdate"
                  v-model="row.date" @input="updateDeviceIntern($event, 'date', row.id)"/>
                </td>
                <td colspan="4" class="text-center"><b-form-select class="customButton" :value="row.worker" :options="workers" @change="updateDeviceIntern($event, 'worker', row.id)"/></td>
                <td colspan="2" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" :value="row.mReading.replace('.',',')"  @change="updateDeviceIntern($event.replace(',','.'), 'mReading', row.id)" style="text-align: center"/></td>
                <td colspan="2" class="text-right"><b-link @click="delmeasrow(row.id)" class="fas fa-trash fa-w-16" />&nbsp;&nbsp;&nbsp;</td>
            </tr>
            <tr v-show="showRowFunc(content.id)">
                <td colspan="1" class="text-center">{{content.subEquel.length+2}}</td>
                <td colspan="2" class="text-center" style="padding-top: 5px;">Dismounting</td>
                <td colspan="2" class="text-center">
                  <VueCtkDateTimePicker class="cForm-input" style="padding:0px" format="YYYY-MM-DD H:mm" no-label noClearButton  minute-interval="10"
                  :min-date="(content.subEquel[content.subEquel.length-1]!=undefined)?content.subEquel[content.subEquel.length-1].date:content.sdate"
                  v-model="content.fdate" @input="updateDeviceList($event, 'fdate', content.id)"/>
                </td>
                <td colspan="4" class="text-center"><b-form-select class="customButton" :value="content.fworker" :options="workers" @change="updateDeviceList($event, 'fworker', content.id)"/></td>
                <td colspan="2" class="text-center" style="white-space:nowrap;"><b-input class="cForm-input" style="text-align: center" :value="content.fmReading.replace('.',',')" @change="updateDeviceList($event.replace(',','.'), 'fmReading', content.id)"/></td>
                <td colspan="2"></td>
            </tr>

          <tr v-show="showRowFunc(content.id)">
            <td class="text-center" style="border:0px;"><b-link @click="addmeasrow(content.id)" style="text-decoration: none !important;">+</b-link><br><br></td>
            <td colspan="12"></td>
          </tr>
        </template>
         <tr>
            <td colspan="6" class="text-center"><b>Period {{fromTo(value.parts.devices_content)}}</b></td>
            <td class="text-right"><b>General</b></td>
            <td class="text-right"><b>{{sumTH(value.parts.devices_content)}}</b></td>
            <td class="text-right"><b>{{sumAH(value.parts.devices_content)}}</b></td>
            <td class="text-right"><b>{{sumTKW(value.parts.devices_content)}}</b></td>
            <td class="text-right"><b>{{sumAKW(value.parts.devices_content)}}</b></td>
            <td colspan="2"></td>
          </tr>
      </table>
    </b-collapse>
  </b-container>
</template>

<script type="text/javascript">
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import moment from 'moment';
import axios from 'axios';
export default {
  components: { VueCtkDateTimePicker },
  props: ['value', 'tableId', 'workers'],
    data() {
      return {
        showRows:[],
      }
    },
  methods: {
fromTo(val){
  function formatDate(date) {
  let dd = date.getDate();
  dd < 10 ? dd = '0' + dd : '';

  let mm = date.getMonth() + 1;
  mm < 10 ? mm = '0' + mm : '';

  let yy = date.getFullYear();
  return  dd+'.'+mm+'.'+yy;
  }
  
  var from = [];
  var to =[];
  val.forEach((v)=>{
    from.push(new Date(v.sdate));
    to.push(new Date(v.fdate));
  });
  var fromSorted = from.sort((a, b) => a-b)
  var toSorted = to.sort((a, b) => b-a)
  return ('from '+formatDate(fromSorted[0])+' to '+formatDate(toSorted[0]));
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
  // toHours(v){
  //   var partOfDays= v/24
  //   var partOfHours = partOfDays.toString().split('.')[0]
  //   var minusHaurs = partOfHours*24
  //   return (v-minusHaurs)

  // },
  difTime(start, end, t){
    var fend=end?end:moment().format("YYYY-MM-DD HH:mm:ss")
    var diffrent = moment(fend,"YYYY-MM-DD HH:mm").diff(moment(start,"YYYY-MM-DD HH:mm"), t)
    return diffrent
  },
  updateDeviceIntern(newData, fild, id){
    axios.get('/updateDeviceIntern', {params: {
      newData: newData,
      fild: fild,
      id: id
    }})
  },
  updateDeviceList(newData, fild, id){
    axios.get('/updateDeviceList', {params: {
      newData: newData,
      fild: fild,
      id: id
    }})
  },
  delmeasrow(id){
      if (confirm("Are you sure?")) {
        axios.get('/delmeasrow', {
          params: {
            id: id
          }
        })
      }
    },
    addmeasrow(id){
      axios.get('/addmeasrow', {
        params: {
          id: id
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
            id: subDel_id
          }
        })
      }
    },
    sendDataTable(id, fild, data){
      this.value.parts.devices_content.forEach((v)=>{
        if(v.id==id){
          axios.get('/update_table_data', {
                        params: {
                          id: id,
                          fild: fild,
                          data: data
                        }
          })         
        }
      })
    },
  },
}
</script>
<style type="text/css">
  .cForm-input input{
    height: 19px !important;
    font-size: 12px !important;
    min-height:19px !important; 
  }
  .cForm-input .custom-button.round{
    height: 10px !important;
  }
  .cForm-input .custom-button.round .custom-button-effect{
    height: 10px !important;
  }
  .date-time-picker .field-input{
    width: 170px !important;
  }
</style>