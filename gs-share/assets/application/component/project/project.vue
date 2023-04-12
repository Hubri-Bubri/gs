<template>
  <b-container style="padding: 0px;" fluid>
    <b-row>
       <b-col cols="12"><br></b-col>
      <b-col lg="6" sm="12">
        <b-form-group :label="projectfild.content+':'" label-cols="3" label-size="sm">
          {{project.number}}
        </b-form-group>
        <b-form-group label="Start date:" label-cols="3" label-size="sm">
          <b-form-input size="sm" type="date"
          @change="updateProject('date', $event)" :value="project.date" placeholder="Enter date" 
          :disabled="disablefild('project-start-date', id)"
          @focus.native="changeDisable('f', 'project-start-date', id)"
          @blur.native="changeDisable('b', 'project-start-date', id)" :id="'project-start-date'+id"/>
        </b-form-group>
        <b-tooltip triggers="none" :show="disablefild('pdata', id)" :target="'pdata'+id">
          {{disablefildUser('pdata', id)}}
        </b-tooltip>





      </b-col>
      <b-col lg="6" sm="12">

        <b-form-group label="Editor:" label-cols="3" label-size="sm">
          {{project.editor}}
        </b-form-group>
        <b-form-group label="End date:" label-cols="3" label-size="sm">
          <b-form-input size="sm"
          :min="project.date"
          type="date"
          @change="updateProject('edate', $event)"
          :value="project.edate"
          placeholder="Enter date"
          :disabled="disablefild('project-end-date', id)"
          @focus.native="changeDisable('f', 'project-end-date', id)"
          @blur.native="changeDisable('b', 'project-end-date', id)"
          :id="'project-end-date'+id" />
        </b-form-group>



      </b-col>
    </b-row>
    <hr />
    <b-row>

      <b-col lg="6" sm="12" >


        <b-form-group label="Customer:" label-cols="3" label-size="sm">
          <b-form-select
          label="name"
          text-field="name"
          value-field="id"
          :value="selectCustomer.id"
          size="sm"
          @change="get_person($event, true);updateProject('customer_id', $event);"
          :options="area"
          :disabled="area==[]" />
        </b-form-group>
        <b-form-group label="Contact:" label-cols="3" label-size="sm">
          <b-form-select text-field="name" value-field="id" size="sm"
          :value="selectPerson.id" :options="availablePersons"
          @change="get_contact($event);updateProject('person_id', $event);" />
        </b-form-group>
        <b-form-group label="Phone:" label-cols="3" label-size="sm">
          <b-form-select text-field="phone" value-field="phone" 
          :value="selectPhone" :options="availablePhons" size="sm" />
        </b-form-group>
        <b-form-group label="E-mail:" label-cols="3" label-size="sm">
          <b-input-group>
            <b-form-select size="sm" text-field="mail" value-field="mail"  :value="selectMail" :options="availableMails" />
              <template #prepend><b-icon icon="inboxes" aria-hidden="true" @click="$emit('sendMail', availableMails)" class="m-1" /></template>
          </b-input-group>
        </b-form-group>

      </b-col>
      <b-col lg="6" sm="12">
        <b-form-group label="ZIP:" label-cols="3" label-size="sm">
          <b-input-group>
            <b-form-input type="text" @change="searchZip($event)" :value="project.zip1" placeholder="Enter zip code" size="sm"
              :disabled="disablefild('pzip1', id)" @focus.native="changeDisable('f', 'pzip1', id)" @blur.native="changeDisable('b', 'pzip1', id)" :id="'pzip1'+id"  />
             
                <b-form-select value-field="code" text-field="name" size="sm"
              :value="selectedCornty.code" :options="countries" @change="updateProject('country', $event)"/>
       
          </b-input-group>
        </b-form-group>
        <b-tooltip triggers="none" :show="disablefild('pcountry', id)" :target="'pcountry'+id">
          {{disablefildUser('pcountry', id)}}
        </b-tooltip>
        <b-tooltip triggers="none" :show="disablefild('pzip', id)" :target="'pzip'+id">
          {{disablefildUser('pzip', id)}}
        </b-tooltip>
        <b-form-group label="Area:" label-cols="3" label-size="sm">
          <b-form-input type="text" @change="updateProject('area', $event)" :value="project.area" placeholder="Enter area" size="sm"
          :disabled="disablefild('parea', id)" @focus.native="changeDisable('f', 'parea', id)" @blur.native="changeDisable('b', 'parea', id)" :id="'parea'+id"  />
        </b-form-group>
        <b-tooltip triggers="none" :show="disablefild('parea', id)" :target="'parea'+id">
          {{disablefildUser('parea', id)}}
        </b-tooltip>
        <b-form-group label="City:" label-cols="3" label-size="sm">
          <b-form-input  type="text" @change="updateProject('city1', $event)" :value="project.city1" size="sm"
          placeholder="Enter city" :disabled="disablefild('pcity1', id)" @focus.native="changeDisable('f', 'pcity', id)"
          @blur.native="changeDisable('b', 'pcity1', id)" :id="'pcity1'+id"  />
        </b-form-group>
        <b-tooltip triggers="none" :show="disablefild('pcity', id)" :target="'pcity'+id">
          {{disablefildUser('pcity', id)}}
        </b-tooltip>
        <b-form-group label="Street:" label-cols="3" label-size="sm">
          <b-input-group>
            <b-form-input type="text" @change="updateProject('street1', $event)" :value="project.street1"
            placeholder="Enter street" :disabled="disablefild('pstreet1', id)" size="sm"
            @focus.native="changeDisable('f', 'pstreet1', id)" @blur.native="changeDisable('b', 'pstreet1', id)" :id="'pstreet1'+id" />
              <template #append><b-icon icon="pin-map" aria-hidden="true" @click="$emit('openmap')" class="m-1" /></template>
          </b-input-group>
        </b-form-group>
        <b-tooltip triggers="none" :show="disablefild('pstreet', id)" :target="'pstreet'+id">
          {{disablefildUser('pstreet', id)}}
        </b-tooltip>
      </b-col>
    </b-row>
    <hr />
    <b-row>
      <b-col>
        <b-button class="customButton" @click="addSameModal()" size="sm">
          Add Offer
        </b-button>
        <b-button class="customButton" @click="showCommetnts" :disabled="!tmp.id"  size="sm">
          Show comments
        </b-button>
        <b-dropdown  text="Link For Workers" class="customDrop"  size="sm">
          <b-dropdown-item  v-for="item in workersForSend" :key="item.id" v-clipboard="'https://'+detecthost()+'/#/project/user/'+id+'/'+item.value" >
            {{item.text}}
          </b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
    <br/>
    <!-- start tables -->
    <div v-show="typesForTables.length==0">
      <Spinner size="large" ></Spinner>
    </div>
    <div v-for="name in typesForTables" v-if="getItems(name.type)!=''">
        {{name.type}}
      <b-table :items="getItems(name.type)" hover  small 
      :fields="fieldsTable" @row-clicked="inItemGetData">
        <template #cell(number)="it">
          <div v-if="name.type=='Invoices'" class="text-container">
            <span v-if="it.item.number.split(' ').length==5"  class="text-content">
              <b-link @click.stop="findRow(' | '+it.item.number.split(' ')[4], name.type)" class="fa fa-clone fa-w-16"  />
              {{it.item.number.split(' ')[0]}} - {{it.item.number.split(' ')[3]}}
            </span>
            <span v-else  class="text-content">
              <b-link @click.stop="findRow(it.item.number, name.type)" class="fa fa-clone fa-w-16"  />
                {{
                  countDigitals(it.item.number.split(' ')[1])
                  +'-'+
                  it.item.number.split(' ')[0].split('-')[1]
                }}
            </span>
          </div>
          <div v-if="((name.type=='Orders') && (it.item.number.split(' ').length==1))"  class="text-container">
            <b-link v-if="(it.item.id==((getItems('Orders')[it.index+1])?getItems('Orders')[it.index+1].number.split(' ')[1]:''))"
            class="hidenotlg" style="text-decoration:none;font-size:14px;vertical-align:top;" @click="showsub(it.item.id, (showsubarr.indexOf(it.item.id)==-1)?'+':'-')">
              {{(showsubarr.indexOf(it.item.id)==-1)?'+':'-'}} 
            </b-link>
            {{it.item.number.split(' ')[0]+'' }} 
          </div>
          <div v-if="((name.type=='Orders') && (it.item.number.split(' ').length==3))"  class="text-container">
            <span class="text-content"> &nbsp;  &nbsp;  &nbsp; {{it.item.number.split(' ')[0]}}</span>
          </div>
          <div v-if="name.type=='Damage Description'"  class="text-container">
            <span  class="text-content">{{ it.item.number.split(' ')[0] }}</span>
          </div>
          <div v-if="name.type=='Offers'" class="text-container">
            <span  class="text-content">{{ it.item.number.split(' ')[0] }}</span>
          </div>
        </template>
        <template #cell(delete)="it">
            <b-link @click.stop="offerDel(it.item.id)">
              <b-icon icon="trash" aria-hidden="true"></b-icon>
            </b-link>
        </template>
        <template #cell(status_set)="it">

            <line-chart :datas="dataCharts(it.item)" :height="50" style="max-width:200px;" v-if="name.type=='Invoices'"/>
            <b-form-select v-else  size="sm" v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)"
            :style="computeStyleOffer(it.item.status_set)">
              <option v-for="opt in options" :style="computeStyleOffer(opt.text)">
                {{opt.text}}
              </option>
            </b-form-select>
    
        </template>
        <template #cell(brutto)="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.brutto}}</span>
          </div>
        </template>
        <template #cell(netto)="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.netto}}</span>
          </div>
        </template>
        <template #cell(date)="data">
          <div class="text-container"><span class="text-content">{{data.item.date | dateInverse}}</span></div>
        </template>
        <template #cell(insurance_number)="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.insurance_number}}</span>
          </div>
        </template>
        <template #cell(other)="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.other}}</span>
          </div>
        </template>
      </b-table>
    </div>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
import moment from 'moment';
import {VueEditor} from 'vue2-editor';
export default {
  components: {
    VueEditor,
  },
  props: ['projectfild', 'project',
  'id', 'tmp', 'itemsTable', 'showsubarr',
   'availablePersons', 'responseFiles', 'selrow',
  'area', 'typesForTables', 'availablePhons', 
  'availableMails', 'countries', 'selectedCornty', 
  'looks', 'workersForSend', 'selectCustomer', 
  'selectPerson', 'selectMail', 'selectPhone'],
  data(){
    return{
      fieldsTable: [
        {
          key: 'number',
          label: 'Number',
          sortable: true
          // class: 'pn'
        },
        {
          key: 'date',
          label: 'Date',
          sortable: true
          // class: 'st'
        },
        {
          key: 'insurance_number',
          label: 'Insurance',
          sortable: true
        },
        {
          key: 'other',
          label: "Order",
          sortable: true
        },
        {
          key: 'netto',
          label: 'Netto',
          sortable: true
          // class: 'text-lg-right'
        },
        {
          key: 'brutto',
          label: 'Brutto',
          sortable: true
          // class: 'text-lg-right'
        },
        {
          key: 'status_set',
          label: 'Status',
          sortable: true
          // class: 'status text-left'
        },
        {
          key: 'delete',
          label: 'Delete'
          // class: 'delete'
          // class: 'text-center'
        }
      ],
      options: [{
        value: 'Open',
        text: 'Open'
        },
        {
          value: 'Done',
          text: 'Done'
        }
      ],
    }
  },
  methods: {
    detecthost(){
      return window.location.host
    },
    get_contact(id){
      this.$emit('getcontact', id)
    },
    get_person(id, mnew){
      this.$emit('getperson', id, mnew)
    },
    offerDel(del_id) {
      this.$emit('offerDel', del_id)
    },
    addSameModal(){
      this.$emit('addSameModal')
    },
    updateItem(val, type, id){
      axios.get('/update_item_from_project', {
        params: {
          val: val,
          type: type,
          id: id
        }
      }).then(response => {})
    },
    searchZip(val){
      axios.get('https://maps.google.com/maps/api/geocode/json', {
        params: {
          components: "country:"+this.selectedCornty.code+"|postal_code:"+val,
          sensor: "false",
          language: "en",
          key: "AIzaSyDKWZ-Jrk9KMoHYakuQfD6xQ4qUZ2XkGpo"
        }
      }).then(response => {
        if (JSON.parse(response.request.response).results[0]!=undefined){
          var results = JSON.parse(response.request.response).results[0]
          for (var i=0; i<results.address_components.length; i++) {
            if (results.address_components[i].types[0] == "locality") {
              var  city = results.address_components[i];
            }
            if (results.address_components[i].types[0] == "administrative_area_level_1") {
              var  region = results.address_components[i];
            }
          }
          // this.project.city = city.long_name
          // this.project.area = region.long_name
          this.updateProject('city1', city.long_name)
          this.updateProject('area', region.long_name)
        }
      })
      this.updateProject('zip1', val)
    },
    updateProject(fild, newData){
      axios.get('/updateProject', {params: {
        id: this.id,
        date: newData,
        fild: fild
      }}).then(response => {
        if (fild == 'other'){
          axios.get('/updateProject', {
            params: {
              id: this.id,
              date:  this.$security.table.account.first_name+'_'+this.$security.table.account.second_name,
              fild: 'user'
          }});
          axios.get('/updateProject', {
            params: {
              id: this.id,
              date: moment().format("DD.MM HH:mm"),
              fild: 'datacomment'
          }});
        }
      })
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
      if (type_operation == 'f'){
        setTimeout(()=>{
        }, 15000);
      }
    },
    showCommetnts(){
      this.$emit('showCommetnts')
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
      if (this.type=='Invoices') result = true
      return result
    },
    disablefildUser(fild, id){
      var result = (this.type=='Invoices') ? '' : 'you'
      this.looks.forEach((val)=>{
        if (val.rows_id == id) {
          if (val.fild == fild) {
            result = val.user
          }
        }
      })
      return result
    },
    getItems(type){
      if (type != 'Orders'){
        if (type != 'SUB'){
          if (type != 'Sub Invoices'){
            if (type != 'Invoices'){
              return this.itemsTable.filter((v)=>{
                if (v.type == type){
                  v._rowVariant = (v.id==this.selrow)?'secondary':''
                    return v 
                }
              })
            }
          }
        }
      }
      if (type == 'Orders')  {
        var orderandsub = []
        var onlisub = []
        this.itemsTable.forEach((v)=>{
          if (v.type == 'Orders'){
            v._rowVariant = (v.id==this.selrow)?'secondary':''
            var xid = v.id
            onlisub = []
            this.itemsTable.forEach((vx)=>{
              if (vx.type == 'SUB'){
                var intId=parseInt(vx.number.split(' ')[1])
                if (xid == intId) {
                  vx._rowVariant = "primaryHide"
                  this.showsubarr.forEach((ss)=>{
                    if (intId == ss) {
                      vx._rowVariant = (vx.id==this.selrow)?'secondary':''
                    }
                  })
                  onlisub.push(vx)
                }
              }
            })
            var mer=[]
            mer.push(v)
            var segmer =  mer.concat(onlisub)
            orderandsub = JSON.parse(JSON.stringify(orderandsub.concat(segmer)));
          }
        })
        return orderandsub
      }
      if (type == 'Invoices'){
        var invoices =[]
        this.itemsTable.forEach((v)=>{
          if(v.type == 'Invoices'){
            v._rowVariant = (v.id==this.selrow)?'secondary':'',
            invoices.push(v)
          }
          if(v.type == 'Sub Invoices'){
            v._rowVariant = (v.id==this.selrow)?'secondary':'',
            invoices.push(v)
          }
        })
        return invoices
      }
    },
    inItemGetData(item, index) {
      this.partx=[]
      this.$emit('inItemGetData', item, index)
    },
    computeStyleOffer(value) {
      switch (value) {
        case 'Open':
          return {
            'background-color': '#FFFFFF'
          };
        case 'Done':
          return {
            'background-color': '#00f25A'
          };
      }
    },
    findRow(id, name){
      var intId=parseInt(id.split(' ')[2])
      var rows = this.getItems('Orders').filter((v)=>{
        if(v.id==intId){
          return v
        }
      })
      this.inItemGetData(rows[0], 0)
    },
    showsub(id, d){
      if (d=='+'){
        this.showsubarr.push(id)
      }
      if (d=='-'){
        this.showsubarr.splice(this.showsubarr.indexOf(id), 1);
      }
    },
    countDigitals(val){
      var nuls=3-val.toString().length
      for (var i = 0; i <= nuls; i++) {
        val='0'+val
      }
      return val
    },
    dataCharts(val){
      if(val.brutto.substr(0, 1)=='-'){
        var brutto=val.brutto.slice(1)
        brutto=brutto.replace('.', '')
        brutto=parseFloat(brutto.replace(',', '.'))
        var pay = this.summFromRow(val, brutto)*100/brutto
        var withOut =100-(this.summFromRow(val, brutto)*100/brutto)
        var t='s'
      } else {
        var brutto=val.brutto.replace('.', '')
        brutto=parseFloat(brutto.replace(',', '.'))
        var pay = this.summFromRow(val, brutto)*100/brutto
        var withOut =100-(this.summFromRow(val, brutto)*100/brutto)
        var t='i'
      }
      return [pay, withOut, t]
    },
    summFromRow(row, brutto){ 
      var result = 0
      row.op.forEach((v)=>{
        result = parseInt(result) + parseInt(v.value)
      })
      if (result>brutto){
        result = brutto
      }
      if (result<(-brutto)){
        result = -brutto
      }
      return result
    }
  }
}
</script>