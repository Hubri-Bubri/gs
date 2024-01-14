<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-card class="gs-container" footer-class="cardFooterBorder">
        <template #header>
          <b-row align-v="end">
            <b-col col  xl="3" lg="11" md="10" sm="10" cols="9">
              <b-form-input
              class="w-100"
              v-model="filter"
              type="search"
              :placeholder="$t('projects.search')">
              </b-form-input>
            </b-col>
            <b-col col  xl="1" lg="1" md="2" sm="2" cols="3"> 
              <b-dropdown  variant="primary" dropright>
                <template #button-content>
                  <b-icon icon="list-check" aria-hidden="true"></b-icon> 
                </template>
                <b-form-checkbox-group
                class="m-2"
                switches
                v-model="filterOn">
                  <b-form-checkbox v-for="fild in filterFilds(fieldsTable)" :key="fild.key" :value="fild.key">
                    {{fild.label}}
                  </b-form-checkbox>
                </b-form-checkbox-group>
              </b-dropdown>
            </b-col>

             <b-col col xl="3" lg="4" md="4" sm="12" cols="12">

                <b-form-row>
                  <b-form-datepicker size="sm" style="max-width:100px;"
                  :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                  :locale="$i18n.locale"
                  :value="fromData"
                  :max="detectMax()"
                  @input="changeDate('min', $event)"
                  >
                  </b-form-datepicker>
                
                   -
                  
                    <b-form-datepicker size="sm" style="max-width:100px;"
                    :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
                    :locale="$i18n.locale"
                    :value="toData"
                    :min="min"
                    :max="toData"
                    @input="changeDate('max', $event)"
                    >
                    </b-form-datepicker>
                 </b-form-row>
 
              </b-col>


            <b-col col  xl="5" lg="8" md="8" sm="12" cols="12">
              <b-form-checkbox-group
              class="text-sm-left text-md-left text-lg-right "
              switches
              v-model="selected"
              :options="typesForTablesOpt"
              @change="keywordChange($event)"/>
            </b-col>
          </b-row>
        </template>
        <container>
          <container-body>
            <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
            <b-table :items="items" :fields="getFields()" hover :filter="filter" :filter-included-fields="filterOn" stacked="lg"
              show-empty @filtered="onFiltered" show-empty  no-border-collapse >
              <!-- :busy="((items.length==0) && (selected.length!=0))" -->
              <template #cell(number)="it">
                <b-link :to="'/project/detail/'+it.item.project_id" variant="primary">
                  {{it.item.number}}
                </b-link>
              </template>
              <template #cell(insurance_number)="it">
                <b-form-input disabled :state="null" type="text"  placeholder="Enter insurance name"
                  @change="updateItem($event, 'insurance_number', it.item.id)"
                  :disabled="disablefild('ofinsurance2', it.item.id)" :value="it.item.insurance_number"
                  @focus.native="changeDisable('f', 'ofinsurance2', it.item.id)" size="sm"
                  @blur.native="changeDisable('b', 'ofinsurance2', it.item.id)" :id="'ofinsurance2'+it.item.id"  />
              </template>
              <template #cell(date)="it">
                <b-form-input disabled :disabled="disablefild('ofdate',  it.item.id)"
                  type="date" @change="updateItem($event, 'date',  it.item.id)"
                  :value="it.item.date" placeholder="Enter date"  
                  @focus.native="changeDisable('f', 'ofdate',  it.item.id)"
                  @blur.native="changeDisable('b', 'ofdate',  it.item.id)" :id="'ofdate'+ it.item.id" size="sm"/>
              </template>
              <template #cell(other)="it">
                <b-form-input disabled :disabled="disablefild('ofother', it.item.id)" :state="null" type="text"
                  @change="updateItem($event, 'other', it.item.id)"
                  :value="it.item.other" placeholder="Enter number" size="sm"
                  @focus.native="changeDisable('f', 'ofother', it.item.id)"
                  @blur.native="changeDisable('b', 'ofother', it.item.id)" :id="'ofother'+it.item.id" />
              </template>
              <template #cell(place)="it">
                <b-form-input disabled type="text"  :disabled="disablefild('ofplace', it.item.id)" 
                  @change="updateItem($event, 'place', it.item.id)"
                  :value="it.item.place" placeholder="Enter place" 
                  @focus.native="changeDisable('f', 'ofplace', it.item.id)"
                  @blur.native="changeDisable('b', 'ofplace', it.item.id)" :id="'ofplace'+it.item.id" size="sm"/>
              </template>
              <template #cell(work)="it">
                <b-form-select size="sm" :value="detectOfWork(it.item.work)" :options="works"  @change="updateItem($event, 'work', it.item.id)" />
              </template>
              <template #cell(status_set)="it">
                <b-form-select size="sm" v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)"
                :style="computeStyleOffer(it.item.status_set)">
                  <option v-for="opt in options" :style="computeStyleOffer(opt.text)">
                    {{opt.text}}
                  </option>
                </b-form-select>
              </template>
              <template #table-busy>
                <div class="text-center text-info">
                  <b-spinner class="align-middle"></b-spinner>
                  <strong>{{$t('projects.loading')}}...</strong>
                </div>
              </template>
            </b-table>
          </div>
          </container-body>
          </container>
      </b-card>
    </container-body>
  </container>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
      fd:'0000-00-00',
      td:'0000-00-00',
      max:null,
      min:null,
      valueType:'',
      addPaymentState: false,
      old_done: '100',
      result:[],
      keyword: '',
      bank:null,
      tabxmodal:false,
      items:[],
      rowId:null,
      amount:null,
      looks: [],

      // options: [
      // {
      //   value: 'Open',
      //   text: 'Open'
      // },
      // {
      //   value: 'Done',
      //   text: 'Done'
      // },
      // {
      //   value: 'Invoice',
      //   text: 'Invoice'
      // },
      // {
      //   value: 'Desiccation',
      //   text: 'Desiccation'
      // },
      // {
      //   value: 'Leakage_Detection',
      //   text: 'Leakage Detection'
      // },
      // {
      //   value: 'Restoration',
      //   text: 'Restoration'
      // }
      // ],
      totalRows: 1,
      filter: null,
      filterOn: []
    }
  },
  computed: {
    options(){ 
        return [{
        value: 'Open',
        text: 'Open'
        },
        {
          value: 'Done',
          text: 'Done'
        }
      ]
    },
    fromData(){
      var date = new Date();
      var day = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear() - 1;
      var currentDate = `${year}-${month}-${day}`;
      return currentDate
    },
    toData(){
      var date = new Date();
      var day = date.getDate();
      var month = date.getMonth() + 1;
      var year = date.getFullYear();
      var currentDate = `${year}-${month}-${day}`;
      return currentDate
    },
    // calendar(){
    //   return {'de':{
    //                       labelPrevDecade: this.$t('calendar.labelPrevDecade'),
    //                       labelPrevYear: this.$t('calendar.labelPrevYear'),
    //                       labelPrevMonth: this.$t('calendar.labelPrevMonth'),
    //                       labelCurrentMonth: this.$t('calendar.labelCurrentMonth'),
    //                       labelNextMonth: this.$t('calendar.labelNextMonth'),
    //                       labelNextYear: this.$t('calendar.labelNextYear'),
    //                       labelNextDecade: this.$t('calendar.labelNextDecade'),
    //                       labelToday: this.$t('calendar.labelToday'),
    //                       labelSelected: this.$t('calendar.labelSelected'),
    //                       labelNoDateSelected: this.$t('calendar.labelNoDateSelected'),
    //                       labelCalendar: this.$t('calendar.labelCalendar'),
    //                       labelNav: this.$t('calendar.labelNav'),
    //                       labelHelp: this.$t('calendar.labelHelp')}}
            
    // },
    typesForTablesOpt(){
      return [
        this.$t('states.done')
      ]
    },
    selected(){
      return [this.$t('states.done')]
    },
    fieldsTable() {
      return [
      // {
      //   key: 'id',
      //   label: this.$t('fields.id'),
      //   sortable: true,
      //   variant: 'default'
      // },
      {
        key: 'number',
        label: this.$t('fields.contract'),
        sortable: true,
        variant: 'default'
      },
      // {
      //   key: 'number',
      //   label: this.$t('fields.number'),
      //   sortable: true,
      //   variant: 'default'
      // },
      {
        key: 'insurance_number',
        label: this.$t('edit.insurance'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'date',
        label: this.$t('customerDetail.date'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'other',
        label: this.$t('lists.order'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'place',
        label: this.$t('fields.place'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'work',
        label: this.$t('calcTableGroup.work'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'status_set',
        label: this.$t('fields.status'),
        sortable: true,
        variant: 'default'
      }
      // {
      //   key: 'type',
      //   label: this.$t('fields.type'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'tax',
      //   label: this.$t('fields.tax'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'taxDub',
      //   label: this.$t('fields.taxDub'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'taxP',
      //   label: this.$t('fields.taxP'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'taxPDub',
      //   label: this.$t('fields.taxPDub'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'disc',
      //   label: this.$t('fields.disc'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'discP',
      //   label: this.$t('fields.discP'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'butDiscPerc',
      //   label: this.$t('fields.butDiscPerc'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'addtaxColapse',
      //   label: this.$t('fields.addtaxColapse'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'dateEvent',
      //   label: this.$t('fields.dateEvent'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'dateInspect',
      //   label: this.$t('fields.dateInspect'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'ExamWorker',
      //   label: this.$t('fields.ExamWorker'),
      //   sortable: true,
      //   variant: 'default'
      // },
      // {
      //   key: 'insurname',
      //   label: this.$t('fields.insurname'),
      //   sortable: true,
      //   variant: 'default'
      // }
      ]
    }
  },
  methods: {
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
    getLoocks(){
       axios.get('/getLoocks').then(response => {
          this.looks=[]
          this.looks = response.data
      })
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
      // if (this.type=='Invoices') result = true
      return result
    },
    get_type_works(){
      axios.get('/get_type_works', {
      }).then(response => {
        this.works = response.data;
        this.works.unshift(this.$t('calcTableGroup.work'))
      })
    },
    detectOfWork(val){
      if(val=='{"isTrusted":true}'){
        return this.$t('calcTableGroup.work');
      } else{
        return val;
      }
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
    updateItem(val, type, id){
      axios.post('/update_item_from_project', 
        {
          val: val,
          type: type,
          id: id
        }
      ).then(response => {})
    },
    countDigitals(val){
      var nuls=3-val.toString().length
      for (var i = 0; i <= nuls; i++) {
        val='0'+val
      }
      return val
    },
    detectMax(){
      if (this.max == null){
        var toData = this.toData.split('-')
        return toData[0]+'-'+toData[1]+'-'+(toData[2]-1)
      } else {
        return this.max
      }

    },
    changeDate(type, value){
      if (type == 'max'){
        this.max = value;
        this.td = value;
      }
      if (type == 'min'){
        this.min = value;
        this.fd = value;
      }
      this.getOffer(this.old_done+'|'+this.fd+'|'+this.td)
    },
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
    },
    getFields(){
      return this.fieldsTable.filter((v)=>{
        v.variant = "default"
        this.filterOn.forEach((v1)=>{
          if(v.key==v1){
              v.variant="info"
          }
        });
        return v
      });
    },
    filterFilds(val){
      return  val.filter((v)=>{
        if (v.key != 'status_set') {
          return v;
        }
      })
    },
    getOffer(mode){
      axios.get('/suggest', {
        params: {
          type: '10',
          mode: mode
        }
      }).then(response => {
        this.items = response.data
      })
    },
    difdate(val){
      var dateuninverse = val.split('.')
        if (dateuninverse.length == 3) {
          val = dateuninverse[2]+'-'+dateuninverse[1]+'-'+dateuninverse[0]
        }
      var date1 = new Date(val)
      var date2 = new Date()
      var daysLag = Math.ceil(Math.abs(date2.getTime() - date1.getTime()) / (1000 * 3600 * 24))
      return (-14+(daysLag-1))
    },
    keywordChange(e){
      var done = '0'
        e.forEach((v)=>{
          if(v==this.$t('states.done')){
            done='1'
          }
        })

      if ((done+'|'+this.fd+'|'+this.td)!=this.old_done+'|'+this.fd+'|'+this.td){
        this.op=[]
        this.items=[]
        this.getOffer(done+'|'+this.fd+'|'+this.td)
        this.old_done = done
      }
    },
  },
  mounted(){
    this.totalRows = this.items.length
    setTimeout(() => {
      this.get_type_works()
      this.$socket.send('getOffer')
      this.$options.sockets.onmessage = (data) => (data.data=='getOffer') ? this.getOffer('1|0000-00-00|0000-00-00'): ''
      this.$options.sockets.onmessage = (data) => (data.data=='getLoocks') ? (this.getLoocks()): ''
    },1000);
  }
}
</script>
<style type="text/css">
/*  .cardFooterBorder{
    border-top: 1px solid #000!important;
  }*/
</style>
