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
            <b-col col xl="5" lg="8" md="8" sm="12" cols="12">
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
            show-empty :busy="isBusy" @filtered="onFiltered" no-border-collapse  >
              <template #cell(number)="it">
                <b-link :to="'/project/detail/'+it.item.project_id" variant="primary">
                  {{it.item.number}}
                </b-link>
              </template>
              <template #cell(insurance_number)="it">
                <b-form-input  type="text"  placeholder="Enter insurance name"
                  @change="updateItem($event, 'insurance_number', it.item.id, it.item.insurance_number)"
                  :value="it.item.insurance_number"
                   size="sm"
                   :id="'ofinsurance2'+it.item.id"  />
              </template>
              <template #cell(date)="it">
                <b-form-input  
                  type="date" @change="updateItem($event, 'date',  it.item.id, -1)"
                  :value="it.item.date" placeholder="Enter date"                    
                   :id="'ofdate'+ it.item.id" size="sm"/>
              </template>
              <template #cell(other)="it">
                <b-form-input  type="text"
                  @change="updateItem($event, 'other', it.item.id, it.item.other)"
                  :value="it.item.other" placeholder="Enter number" size="sm"
                   :id="'ofother'+it.item.id" />
              </template>
              <template #cell(place)="it">
                <b-form-input  type="text"  
                  @change="updateItem($event, 'place', it.item.id, it.item.place)"
                  :value="it.item.place" placeholder="Enter place" 
                  :id="'ofplace'+it.item.id" size="sm"/>
              </template>
              <template #cell(work)="it">
                <b-form-select size="sm" :value="detectOfWork(it.item.work)" :options="works"  @change="updateItem($event, 'work', it.item.id, detectOfWork(it.item.work))" />
              </template>
              <template #cell(status_set)="it">
                <b-form-select size="sm" :value="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id, it.item.status_set);it.item.status_set=$event"
                :style="computeStyleOffer(it.item.status_set)">
                  <option v-for="opt in options" :style="computeStyleOffer(opt.text)">
                    {{opt.text}}
                  </option>
                </b-form-select>
              </template>
              <template #empty>
                <div class="text-center">{{$t('projects.empty')}}</div>
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
      isBusy: true,
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
      {
        key: 'number',
        label: this.$t('fields.contract'),
        sortable: true,
        variant: 'default'
      },

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
      ]
    }
  },
  methods: {
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


		updateItem(val, type, id, old) {
      if (old != val) {
        axios.get('/update_item_from_project', {
          params: {
            val: val,
            type: type,
            id: id
          }
        })
      }
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
      this.getContracts(this.old_done+'|'+this.fd+'|'+this.td)
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
    getContracts(mode){
      axios.get('/suggest', {
        params: {
          type: '20',
          mode: mode
        }
      }).then(response => {
        this.items = response.data;
        this.isBusy = false;
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
        this.getContracts(done+'|'+this.fd+'|'+this.td)
        this.old_done = done
      }
    },
  },
  mounted(){
    this.totalRows = this.items.length
    this.get_type_works()
    this.getContracts('1|0000-00-00|0000-00-00')
    this.$options.sockets.onmessage = (data) => (data.data=='getContracts') ? this.getContracts('1|0000-00-00|0000-00-00'): ''
  }
}
</script>