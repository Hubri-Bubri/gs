<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-card class="gs-container" footer-class="cardFooterBorder">
        <template #header>
          <b-row align-v="end" align-h="between">
             <b-col col xl="9" lg="8" md="8" sm="12" cols="12">
            <b-input-group>
              <template #prepend>
              <b-dropdown  variant="primary" dropright>
                <template #button-content>
                  {{$t('states.mode')}}
                  <!-- <b-icon icon="list-check" aria-hidden="true"></b-icon>  -->
                </template>

 <b-form-checkbox class="ml-2" style="width:200px;" switch @change="modeInvoice($event)">
      {{(me_sub=='0')?$t('alert.Invoices'):$t('states.subInvoices')}}
    </b-form-checkbox>
    <b-form-checkbox class="ml-2" style="width:200px;" switch @change="paid($event)">
      {{(unpaid_all=='0')?$t('states.unpaidInvoices'):$t('states.paidInvoices')}}
    </b-form-checkbox>
                
              </b-dropdown>
              </template>


              <b-form-input

              v-model="filter"
              type="search"
              :placeholder="$t('projects.search')">
              </b-form-input>


              <template #append>
              <b-dropdown  variant="primary" dropright>
                <template #button-content>
                  {{$t('states.options')}}
                  <!-- <b-icon icon="list-check" aria-hidden="true"></b-icon>  -->
                </template>



<!-- 
            <b-form-checkbox-group 
              class="m-2"
              style="width:200px;"
              switches
              :value="selmode"
              :options="typesForTablesOpt"
              @change="keywordChange($event)">
                
              </b-form-checkbox-group> -->

   
<b-form-checkbox-group
                class="m-2"
                switches
                v-model="filterOn">
                  <b-form-checkbox v-for="fild in filterFilds(fieldsTable)" :key="fild.key" :value="fild.key">
                    {{fild.label}}
                  </b-form-checkbox>
                </b-form-checkbox-group>
              </b-dropdown>
            </template>
            </b-input-group>
            </b-col>
            <b-col col xl="3" lg="4" md="4" sm="12" cols="12" align-self="end">

              <b-form-row style="width:260px;float: right;">
              <b-form-datepicker style="max-width:125px;"
              :date-format-options="{ year: 'numeric', month: 'numeric', day: 'numeric' }"
              :locale="$i18n.locale"
              :value="fromData"
              :max="detectMax()"
              @input="changeDate('min', $event)"
              >
              </b-form-datepicker>
              
             
              <b-form-datepicker style="max-width:125px;"
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


          </b-row>
        </template>
        <container>
          <container-body>
            <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
            <b-table @row-clicked="dataToFoot($event)" :items="items" :fields="getFields()" hover :filter="filter" :filter-included-fields="filterOn" stacked="lg"
            show-empty :busy="isBusy" @filtered="onFiltered"  no-border-collapse >
              <template #cell(status_set)="it">
                  <line-chart :datas="dataCharts(it.item)" :height="50" style="max-width:200px;" />
              </template>
              <template #cell(cnumber)="it">
                <b-link :to="'/project/detail/'+it.item.project_id" variant="primary">
                  {{it.item.cnumber}}
                </b-link>
              </template>
              <template #cell(sorting_data)="it">
                  {{it.item.date}}
              </template>
              <template #cell(brutto)="it">
                  {{it.item.brutto | thousandSeparator}}
              </template>
              <template #cell(gen_summa)="it">
                  {{it.item.gen_summa | thousandSeparator}}
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
          <template #footer>
            <b-table-simple v-show="(rowId!=null)&addPaymentState" >
              <b-tbody>
                    <b-tr>
                      <b-td class="text-center">
                        {{$t('balance.amounts')}}
                      </b-td>
                      <b-td>
                        <b-row>
                          <b-col col>
                            {{$t('balance.payments')}}:
                          </b-col>
                          <b-col col>
                            {{Math.abs(summ())|thousandSeparator}} €
                          </b-col>
                          <b-col col >
                            = 
                          </b-col>
                          <b-col col>
                            {{Math.abs((summ())*100/Math.abs(amount)).toFixed(0)}} %
                          </b-col>
                        </b-row>
                      </b-td>
                      <b-td class="text-right">
                        <b-button @click="op=[];addPaymentState=false;" variant="primary" size="sm">
                          <b-icon icon="x" aria-hidden="true"></b-icon>
                        </b-button>
                      </b-td>
                    </b-tr>
                    <b-tr>
                      <b-td>
                        <b-row>
                          <b-col col>
                            {{$t('balance.invoiceAmount')}}:
                          </b-col>
                          <b-col col>
                            {{amount|thousandSeparator}} €
                          </b-col>
                        </b-row>
                      </b-td>
                      <b-td>
                        <b-row>
                          <b-col col>
                            {{$t('balance.outstandingBalance')}}:
                          </b-col>
                          <b-col col>
                            {{(Math.abs(summ())-Math.abs(amount))|thousandSeparator}} €
                          </b-col>
                          <b-col col>
                            =
                          </b-col>
                          <b-col col>
                            {{((Math.abs(summ())-Math.abs(amount))*100/Math.abs(amount)).toFixed(0)}} %
                          </b-col>
                        </b-row>
                      </b-td>
                      <b-td>
                        
                      </b-td>
                    </b-tr>
                    <b-tr>
                      <b-td>
                        <b-textarea :rows="textLength()" @change.native="updateComment(comment)" :placeholder="$t('balance.description')" v-model="comment" />
                      </b-td>
                      <b-td colspan="2">
                        <b-row v-for="(operation, index) in op" :key="op.id" align-v="center" :class="(operation.new)?'bg-primary text-light':'bg-default'">
                          <b-col col cols="1" class="text-center">
                            {{(index+1)}}
                          </b-col>
                          <b-col col cols="2" class="text-center">
                            <b-badge pill style="font-size:0.8125rem;font-weight:400;" variant="dark">
                              {{valueType}}
                            </b-badge>
                          </b-col>
                          <b-col col cols="2">
                            <b-form-input type="text"  @change="updateBalance($event.replace(',','.'), operation, 'value')" 
                            :value="operation.value|thousandSeparator" />
                          </b-col>
                          <b-col col cols="1">
                            €
                          </b-col>
                          <b-col col cols="2">
                            <b-form-input type="date" @change="(operation.new)?'':updateBalance($event, operation, 'date')"
                             :value="operation.date" />
                          </b-col>
                          
                          <b-col col cols="4" class="text-right">
                            <b-button @click="(operation.new)?removeNewPay(index):removePay(operation.id)" variant="danger" size="sm">
                              <b-icon icon="trash" aria-hidden="true"></b-icon>
                            </b-button>
                          </b-col>
                        </b-row>
                      </b-td>
                    </b-tr>
                  </b-tbody>
                </b-table-simple>
              <b-row align-v="end">
                <b-col col cols="6">
              <b-button @click="addPayment"  v-show="addPaymentState" variant="primary" :disabled="(Math.abs(summ())>=Math.abs(amount))">
                {{$t('balance.addPayment')}}
              </b-button>
              <b-button @click="op=[];items=[];getBalance(old_done+'|'+fd+'|'+td)" variant="warning" v-show="(addPaymentState)&(cancelPay()!=0)">
                {{$t('balance.cancelAllNewPayments')}}
              </b-button>
              <b-button  variant="success" v-show="(addPaymentState)&(cancelPay()!=0)" @click="saveAll">
                {{$t('balance.saveAllNewPayments')}}
              </b-button>
            </b-col>
            <b-col col cols="6" class="text-right">
              <b-badge pill variant="primary" style="font-size:0.8125rem;font-weight:400;">
                {{allbalance()}}
              </b-badge>
            </b-col>
            </b-row>
          </template>
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
      selmode:[],
      fd:'0000-00-00',
      td:'0000-00-00',
      me_sub: '0',
      unpaid_all: '0',
      max:null,
      min:null,
      valueType:'',
      addPaymentState: false,
      old_done: '00',
      result:[],
      keyword: '',
      bank:null,
      tabxmodal:false,
      items:[],
      rowId:null,
      amount:null,
      op:[],
      comment:null,
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
    // typesForTablesOpt(){
    //   return [
    //   (this.old_done[1]==0)?this.$t('alert.Invoices'):this.$t('states.subInvoices'),
    //   (this.old_done[0]==0)?this.$t('states.unpaidInvoices'):this.$t('states.paidInvoices')
    //   ]
    // },

    // selected(){
    //   return []
    // },
    fieldsTable() {
      return [{
        key: 'number',
        label: this.$t('fields.number'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'cnumber',
        label: this.$t('fields.contract'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'sorting_data',
        label: this.$t('customerDetail.date'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'street1',
        label: this.$t('fields.street'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'names',
        label: this.$t('customerDetail.customer'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'gen_summa',
        label: this.$t('edit.netto'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'brutto',
        label: this.$t('edit.brutto'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'status_set',
        label: this.$t('fields.status'),
        // sortable: true,
        variant: 'default'
      },
      {
        key: 'days',
        label: this.$t('fields.days'),
        sortable: true,
        variant: 'default'
      }]
    }
  },
  methods: {
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
      this.getBalance(this.old_done+'|'+this.fd+'|'+this.td)
    },
    cancelPay(){
      // var newTrue = 0
      // this.items.filter((v)=>{
      //   v.op.filter((v1)=>{
      //     if (v1.new) newTrue = newTrue + 1
      //   });
      // });
      // return newTrue
    },
    textLength(){
     if(this.rowId!=null){
        return this.op.length*2
      }
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
        if ((v.key != 'days')&(v.key != 'status_set')&(v.key != 'sorting_data')) {
          return v;
        }
      })
    },
    dataCharts(val){
      // var valBruto = this.$options.filters.reThousandSeparator(val.brutto)
      var valBruto = parseFloat(val.brutto)
      var pay=this.summFromRow(val)*100/valBruto
      var withOut=100-(this.summFromRow(val)*100/valBruto)
      // console.log(valBruto, pay, withOut)
      var t = 'i'

      if (val.type=='CREDIT'){
        t = 's'
        pay = Math.abs(pay)
      }
      if (val.type=='DEBET'){
        t = 'i'
      }
      return [pay, withOut, t]
    },
    countDigitals(val){
      var nuls=3-val.toString().length
      for (var i = 0; i <= nuls; i++) {
        val='0'+val
      }
      return val
    },
    getBalance(mode){
      // console.log(mode)
      axios.get('/balance', {
        params: {
          mode: mode
        }
      }).then(response => {
        // console.log(response.data)
        var countSelect = 0
        this.items = response.data.filter((v)=>{

          // console.log('2')
          v.date = this.$options.filters.dateInverse(v.date)
          v.days = this.difdate(v.date)
          v.status_set = (this.summFromRow(v)*66/v.brutto)+((34-(-this.difdate(v.date))*34/14)/2)
            if (v.number.split(' ').length==3){
              v.cnumber = this.countDigitals(v.number.split(' ')[0])
              v.number = this.countDigitals(v.number.split(' ')[1])+'-'+v.number.split(' ')[0].split('-')[1]
            }
            if (v.number.split(' ').length==5){
              v.cnumber = v.number.split(' ')[2]
              v.number = v.number.split(' ')[3]+' - '+v.number.split(' ')[0]
            }
          if (v.type==30){
            v.type = 'DEBET'
            if((v.number.split(' ').length==1)|(v.number.split(' ').length==3)|(v.number.split(' ').length==5)){
              // v.netto = this.$options.filters.thousandSeparator(v.netto)
              // v.brutto = this.$options.filters.thousandSeparator(v.brutto)
            }
          }
          if (v.type==60){
            // console.log('3')
            v.type = 'CREDIT' 
            // v.netto = -v.netto
            // console.log(v.brutto)
            // v.brutto = -v.brutto
            // console.log(v.brutto)
            // v.netto = '-'+this.$options.filters.thousandSeparator(v.netto)
            // v.brutto = '-'+this.$options.filters.thousandSeparator(v.brutto)
          }
          if (this.rowId!=null){
            this.items = this.items.filter((selected)=>{
              if (v.id == this.rowId){
                countSelect = countSelect +1
                v._rowVariant ='success'
                this.op=[]
                this.op = v.op
              } 
              return selected
            })
            
          }
          // console.log(v.other=='TEC / 1 / 35.362 / 2022')
          // if (v.id==552){
          //   console.log(v)
          // }
          return v
        });
        this.isBusy = false;
        if(countSelect==0){
          this.addPaymentState = false
          this.op=[]
        }
      })
    },
    summFromRow(row){
      // console.log(row)
      var result = 0.0
      row.op.forEach((v)=>{
        result = parseFloat(result) + parseFloat(v.value)
        // console.log(result)
      })
      return result
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

    modeInvoice(e){
      if(e==false){
        this.me_sub='0'
      }
      if(e==true){
        this.me_sub='1'
      }
      if ((this.unpaid_all+this.me_sub+'|'+this.fd+'|'+this.td)!=this.old_done+'|'+this.fd+'|'+this.td){
        this.op=[]
        this.items=[]
        this.getBalance(this.unpaid_all+this.me_sub+'|'+this.fd+'|'+this.td)
        this.old_done = this.unpaid_all+this.me_sub
        // this.selmode=selected
      }
    },
    paid(e){
      if(e==false){
        this.unpaid_all='0'
      }
      if(e==true){
        this.unpaid_all='1'
      }
      if ((this.unpaid_all+this.me_sub+'|'+this.fd+'|'+this.td)!=this.old_done+'|'+this.fd+'|'+this.td){
        this.op=[]
        this.items=[]
        this.getBalance(this.unpaid_all+this.me_sub+'|'+this.fd+'|'+this.td)
        this.old_done = this.unpaid_all+this.me_sub
        // this.selmode=selected
      }
    },


    // keywordChange(e){
    //   // console.log(e)
    //   var unpaid_all = '0'
    //   var me_sub = '0'
    //   var selected = []
    //   var same = false
    //   // var subinvoice = '0'

    //   console.log(this.selmode)
    //     e.forEach((v)=>{


          
    //       if(v==this.$t('states.unpaidInvoices')){
    //           same = false
    //           this.selmode.forEach((oldval)=>{
    //             console.log(v, oldval, this.selmode)
    //             if (v == oldval) {
    //               same = true
    //             }
    //           })
    //           if (same == false){
    //             console.log('!')
    //             unpaid_all='1'
    //             selected.push(this.$t('states.paidInvoices'))
    //           }
    //         }

    //         if(v==this.$t('states.paidInvoices')){
    //           same = false
    //           this.selmode.forEach((oldval)=>{
    //             if (v == oldval) {
    //               same = true
    //             }
    //           })
    //           if (same == false){
    //             unpaid_all='0'
    //             selected.push(this.$t('states.unpaidInvoices'))
    //           }
    //         }

    //         if(v==this.$t('states.subInvoices')){
    //           same = false
    //           this.selmode.forEach((oldval)=>{
    //             if (v == oldval) {
    //               same = true
    //             }
    //           })
    //         if (same == false){
    //             me_sub='0'
    //             selected.push(this.$t('alert.Invoices'))
    //           }
    //         }

    //         if(v==this.$t('alert.Invoices')){
    //           same = false
    //           this.selmode.forEach((oldval)=>{
    //             if (v == oldval) {
    //               same = true
    //             }
    //         })
    //         if (same == false){
    //             me_sub='1'
    //             selected.push(this.$t('states.subInvoices'))
    //           }
    //         }
    //     })

      
    //   if ((unpaid_all+me_sub+'|'+this.fd+'|'+this.td)!=this.old_done+'|'+this.fd+'|'+this.td){
    //     this.op=[]
    //     this.items=[]
    //     this.getBalance(unpaid_all+me_sub+'|'+this.fd+'|'+this.td)
    //     this.old_done = unpaid_all+me_sub
    //     this.selmode=selected
    //   }
    // },
    updateBalance(val, operation, type) {
      if (operation.new){
        this.$set(operation, type, val)
      } else{
        // this.items =[]
        axios.get('/update_payment', {
          params: {
            id: operation.id,
            value: val,
            fild: type
          }
        })
      }
    },
    updateComment(val) {
      axios.get('/update_comment', {
        params: {
          id: this.rowId,
          value: val
        }
      })
    },
    dataToFoot(item){
      this.items.forEach((v)=>{
        if (v._rowVariant!='primary'){
          v._rowVariant=''
        }
      })
      if (item._rowVariant!='primary'){
        item._rowVariant ='success'
      }
      this.amount=parseFloat(item.brutto)
      this.op = item.op
      this.rowId = item.id
      this.valueType = item.type
      this.comment = item.comment
      this.addPaymentState = true
    },
    addPayment(){
      // console.log(Math.abs(this.amount),  Math.abs(this.summ()))
      var brutto = Math.abs(this.amount) - Math.abs(this.summ())
      var date = new Date();
      var getYear = date.toLocaleString("default", { year: "numeric" })
      var getMonth = date.toLocaleString("default", { month: "2-digit" })
      var getDay = date.toLocaleString("default", { day: "2-digit" })
      var dateFormat = getYear + "-" + getMonth + "-" + getDay
      var index = null
      var value = null
      this.items.filter((v, i)=>{
        if(v.id == this.rowId){
          v._rowVariant ='primary'
          v.op.push({type:(v.type), date:dateFormat, value:brutto, new:true})
          index = i
          value = v
        }
      })
      if (index!=null){
        this.items.splice(index, 1, value)
      }
    },
    saveAll(){
      var savearr=[]
      this.items.filter((v)=>{
        v.op.filter((v1)=>{
          if (v1.new==true){
            savearr.push({'id':v.id,'type':v1.type,value:v1.value,'date':v1.date})
          }
        })
      })

      axios.get('/add_payment', {
        params: {
          savearr: savearr.map(u => Object.values(u).join(',')).join('|')
        }
      })
    },
    removeNewPay(index){
      this.op.splice(index, 1)
      var newTrue = 0 
      this.op.forEach((v)=>{
        if (v.new) newTrue = newTrue + 1
      })
      if (newTrue == 0) {
        this.items.forEach((v)=>{
          if(v.id == this.rowId){
            v._rowVariant ='success'
          }
        })
      }
    },
    removePay(id){
      if (confirm(this.$t('alert.sure'))) {
        axios.get('/remove_payment', {
          params: {
            id: id
          }
        })
      }
    },
    summ(){
      var brutto = 0.0
      this.items.filter((v)=>{
        if (v.id == this.rowId){
          v.op.filter((v1)=>{
            var value=parseFloat(v1.value)
            brutto=brutto+value
          })
        }
      })
      return brutto
    },
    allbalance(){
      // console.log(this.filter)
      var brutto = parseFloat(0.00)
      var gen_summa = parseFloat(0.00)

      this.items.filter((v)=>{
        // v.brutto = v.brutto.replace('--', '-')
        // v.netto = v.netto.replace('--', '-')
        brutto = brutto + parseFloat(v.brutto)
        gen_summa = gen_summa + parseFloat(v.gen_summa)
        // console.log(brutto, gen_summa)
      })
     
      // if (
      //   (this.$security.account['id']==1) ||
      //   (this.$security.account['id']==3)
      // )
      // {
        return 'Netto '+this.$options.filters.thousandSeparator(gen_summa)+' €  Brutto '+this.$options.filters.thousandSeparator(brutto)+' €'
      // }
    }
  },
  mounted(){
    this.totalRows = this.items.length
    setTimeout(() => {
      this.$socket.send('getBalance')
      this.$options.sockets.onmessage = (data) => (data.data=='getBalance') ? this.getBalance('00|0000-00-00|0000-00-00'): ''
      this.$options.sockets.onmessage = (data) => (data.data=='getBalanceAfterPay') ? this.getBalance(this.old_done+'|'+this.fd+'|'+this.td): ''
    },1000);
  }
}
</script>
<style type="text/css">
  .cardFooterBorder{
    border-top: 1px solid #000!important;
  }
</style>
