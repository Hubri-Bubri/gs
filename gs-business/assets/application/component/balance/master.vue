<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-card class="gs-container" footer-class="cardFooterBorder">
        <template #header>
          <b-row align-v="end">
            <b-col col  xl="2" lg="2" md="12"  sm="12" xs="12">
              <b-form-input
              class="w-100"
              v-model="filter"
              type="search"
              placeholder="Search">
              </b-form-input>
            </b-col>
            <b-col col xl="6" lg="6" md="8"  sm="8" xs="8"> 
              <b-form-checkbox-group
              class="text-lg-center text-xl-center text-sm-left text-md-left"
              switches
              v-model="filterOn">
                <b-form-checkbox v-for="fild in filterFilds(fieldsTable)" :key="fild.key" :value="fild.key">
                  {{fild.label}}
                </b-form-checkbox>
              </b-form-checkbox-group>
            </b-col>
            <b-col col xl="4" lg="4" md="4"  sm="4" xs="4">
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
            <b-table @row-clicked="dataToFoot($event)" :items="items" :fields="getFields()" hover :filter="filter" :filter-included-fields="filterOn"
              show-empty @filtered="onFiltered" sticky-header no-border-collapse style="max-height:100%" :busy="((items.length==0) && (selected.length!=0))">
              <template #cell(status_set)="it">
                  <line-chart :datas="dataCharts(it.item)" :height="50" style="max-width:200px;" />
              </template>
              <template #cell(cnumber)="it">
                <b-link :to="'/project/detail/'+it.item.project_id" variant="primary">
                  {{it.item.cnumber}}
                </b-link>
              </template>
              <template #table-busy>
                <div class="text-center text-info">
                  <b-spinner class="align-middle"></b-spinner>
                  <strong>Loading...</strong>
                </div>
              </template>
            </b-table>
          </container-body>
          </container>
          <template #footer>
            <b-table-simple v-show="(rowId!=null)&addPaymentState">
              <b-tbody>
                    <b-tr>
                      <b-td class="text-center">
                        Amounts
                      </b-td>
                      <b-td>
                        <b-row>
                          <b-col col>
                            Payments:
                          </b-col>
                          <b-col col>
                            {{Math.abs(summ())|thousandSeparator}} €
                          </b-col>
                          <b-col col >
                            = 
                          </b-col>
                          <b-col col>
                            {{Math.abs((summ())*100/Math.abs(amount)).toFixed(2)|thousandSeparator}} %
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
                            Invoice Amount:
                          </b-col>
                          <b-col col>
                            {{amount|thousandSeparator}} €
                          </b-col>
                        </b-row>
                      </b-td>
                      <b-td>
                        <b-row>
                          <b-col col>
                            Outstanding balance:
                          </b-col>
                          <b-col col>
                            {{(Math.abs(summ())-Math.abs(amount))|thousandSeparator}} €
                          </b-col>
                          <b-col col>
                            =
                          </b-col>
                          <b-col col>
                            {{((Math.abs(summ())-Math.abs(amount))*100/Math.abs(amount)).toFixed(2)|thousandSeparator}} %
                          </b-col>
                        </b-row>
                      </b-td>
                      <b-td>
                        
                      </b-td>
                    </b-tr>
                    <b-tr>
                      <b-td>
                        <b-textarea :rows="textLength()" @change.native="updateComment(comment)" placeholder="Description" v-model="comment" />
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
                            <b-form-input type="text"  @change="updateBalance($event, operation, 'value')" 
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
                Add payment
              </b-button>
              <b-button @click="op=[];items=[];getBalance(old_done)" variant="warning" v-show="(addPaymentState)&(cancelPay()!=0)">
                Сancel all new payments
              </b-button>
              <b-button  variant="success" v-show="(addPaymentState)&(cancelPay()!=0)" @click="saveAll">
                Save all new payments
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
      valueType:'',
      addPaymentState: false,
      old_done: '100',
      result:[],
      keyword: '',
      bank:null,
      tabxmodal:false,
      items:[],
      selected: ['Unpaid Invoices'],
      rowId:null,
      amount:null,
      op:[],
      comment:null,
      typesForTablesOpt:['Unpaid Invoices', 'Paid Invoices', 'Sub Invoices'],
      fieldsTable: [
      {
        key:'number',
        label: 'Number',
        sortable: true
      },
      {
        key:'cnumber',
        label: 'Contract',
        sortable: true
      },
      {
        key:'date',
        label: 'Date',
        sortable: true
      },
      {
        key:'street1',
        label: 'Street',
        sortable: true
      },
      {
        key:'names',
        label: 'Customer',
        sortable: true
      },
      {
        key:'netto',
        label: 'Netto',
        sortable: true
      },
      {
        key:'brutto',
        label: 'Brutto',
        sortable: true
      },
      {
        key:'status_set',
        label: 'Status',
        sortable: true,
        class: 'status'
      },
      {
        key:'days',
        label: 'Days',
        sortable: true
      }
      ],
      options: [
      {
        value: 'Open',
        text: 'Open'
      },
      {
        value: 'Done',
        text: 'Done'
      },
      {
        value: 'Invoice',
        text: 'Invoice'
      },
      {
        value: 'Desiccation',
        text: 'Desiccation'
      },
      {
        value: 'Leakage_Detection',
        text: 'Leakage Detection'
      },
      {
        value: 'Restoration',
        text: 'Restoration'
      }
      ],
      totalRows: 1,
      filter: null,
      filterOn: []
    }
  },
  methods: {
    cancelPay(){
      var newTrue = 0
      this.items.filter((v)=>{
        v.op.filter((v1)=>{
          if (v1.new) newTrue = newTrue + 1
        });
      });
      return newTrue
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
        if ((v.key != 'days')&(v.key != 'status_set')) {
          return v;
        }
      })
    },
    dataCharts(val){
      var valBruto = this.$options.filters.reThousandSeparator(val.brutto)
      var pay=this.summFromRow(val, valBruto)*100/valBruto
      var withOut=100-(this.summFromRow(val, valBruto)*100/valBruto)
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
        var countSelect = 0
        this.items = response.data.filter((v)=>{
          v.date = this.$options.filters.dateInverse(v.date)
          v.days = this.difdate(v.date)
          v.status_set = (this.summFromRow(v, v.brutto)*66/v.brutto)+((34-(-this.difdate(v.date))*34/14)/2)
            if (v.number.split(' ').length==3){
              v.cnumber = this.countDigitals(v.number.split(' ')[0])
              v.number = this.countDigitals(v.number.split(' ')[1])+'-'+v.number.split(' ')[0].split('-')[1]
            }
            if (v.number.split(' ').length==5){
              v.cnumber = v.number.split(' ')[2]
              v.number = v.number.split(' ')[3]+' - '+v.number.split(' ')[0]
            }
          if (v.type==3){
            v.type = 'DEBET'
            if((v.number.split(' ').length==1)|(v.number.split(' ').length==3)|(v.number.split(' ').length==5)){
              v.netto = this.$options.filters.thousandSeparator(v.netto)
              v.brutto = this.$options.filters.thousandSeparator(v.brutto)
            }
          }
          if (v.type==6){
            v.type = 'CREDIT'
            v.netto = -v.netto
            v.brutto = -v.brutto
            v.netto = this.$options.filters.thousandSeparator(v.netto)
            v.brutto = this.$options.filters.thousandSeparator(v.brutto)
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
          return v
        })
        if(countSelect==0){
          this.addPaymentState = false
          this.op=[]
        }
      })
    },
    summFromRow(row, brutto){
      var result = 0
      row.op.forEach((v)=>{
        result = result + parseFloat(v.value)
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
    keywordChange(e){
      var unpaid = '0'
      var paid = '0'
      var subinvoice = '0'
        e.forEach((v)=>{
          if(v=='Unpaid Invoices'){
            unpaid='1'
          }
          if(v=='Paid Invoices'){
            paid='1'
          }
          if(v=='Sub Invoices'){
            subinvoice='1'
          }
        })
      if ((unpaid+paid+subinvoice)!=this.old_done){
        this.op=[]
        this.items=[]
        this.getBalance(unpaid+paid+subinvoice)
        this.old_done = unpaid+paid+subinvoice
      }
    },
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
      this.amount=this.$options.filters.reThousandSeparator(item.brutto)
      this.op = item.op
      this.rowId = item.id
      this.valueType = item.type
      this.comment = item.comment
      this.addPaymentState = true
    },
    addPayment(){
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
      if (confirm("Are you sure?")) {
        axios.get('/remove_payment', {
          params: {
            id: id
          }
        })
      }
    },
    summ(){
      var brutto = 0
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
      var netto = parseFloat(0.00)
      this.items.filter((v)=>{
        brutto = brutto + this.$options.filters.reThousandSeparator(v.brutto)
        netto = netto + this.$options.filters.reThousandSeparator(v.netto)
        // console.log(brutto, netto)
      })
      if (
        (this.$security.account['id']==1) ||
        (this.$security.account['id']==3)
      ){
        return 'Netto '+this.$options.filters.thousandSeparator(netto)+' €  Brutto '+this.$options.filters.thousandSeparator(brutto)+' €'
      }
    }
  },
  mounted(){
    this.totalRows = this.items.length
    setTimeout(() => {
      this.$socket.send('getBalance')
      this.$options.sockets.onmessage = (data) => (data.data=='getBalance') ? this.getBalance('100'): ''
      this.$options.sockets.onmessage = (data) => (data.data=='getBalanceAfterPay') ? this.getBalance(this.old_done): ''
    },1000);
  }
}
</script>
<style type="text/css">
  .cardFooterBorder{
    border-top: 1px solid #000!important;
  }
</style>