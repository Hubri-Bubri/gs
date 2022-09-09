<template>
    <container>
        <b-modal class="mail" v-model="tabxmodal" centered no-close-on-esc no-close-on-backdrop hide-header-close title="Balance">
<b-container fluid>
                                <b-input-group style="margin-bottom: 5px">
                                 <b-input placeholder="[search]" v-model="keyword" busy.sync="isBusy"/>
                                
                                <template #append>
                                  <b-dropdown text="options" variant="outline-secondary">
                                    <b-form-checkbox-group style="width:100%"
                                      button-variant="outline-secondary"
                                      stacked
                                      :checked="selected"
                                      :options="typesForTablesOpt"
                                      @change="keywordChange($event)"
                                      buttons />
                                  </b-dropdown>
                                </template>
                              </b-input-group>


                            <balance
                            :selected="selected"
                            :rowId="rowId"
                            :brutto="brutto"
                            :op="op"
                            :comment="comment"
                            :typesForTablesOpt="typesForTablesOpt"
                            :fieldsTable="fieldsTable"
                            :options="options"
                            :result="result"
                            :items="items"
                            :keyword="keyword"

          
                            @dataToFoot="dataToFoot"

                            >
                           
                            </balance>
</b-container>
            <template slot="modal-footer">

<b-container fluid>
<b-row v-show="op" style="border-top: 1px solid black;padding-top:7px;">
      <b-col sm="5" class="cuestomRow">
        <b-row>
          <b-col class="text-center">
            Amounts
          </b-col>
        </b-row>
        <b-form-group horizontal :label-cols="5"  class="cForm" label="Invoice Amount:">
          <b-row>
            <b-col cols="7">
              <b-form-input  type="text" :value="brutto|thousandSeparator" disabled class="cForm-input  text-right" />
            </b-col>
            <b-col cols="2">
              €
            </b-col>
          </b-row>
        </b-form-group>
      </b-col>
      <b-col sm="7" class="cuestomRow">
        <b-row>
          <b-col cols="4" class="cForm">    
            Payments:
          </b-col>
          <b-col cols="3">    
            <b-form-input :value="summ()|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm">    
            €
          </b-col>
          <b-col cols="1" class="cForm">    
            =
          </b-col>
          <b-col cols="2">
            <b-form-input :value="(summ()*100/brutto)|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm text-left">
            %
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="4" class="cForm">    
            Outstanding balance:
          </b-col>
          <b-col cols="3">    
            <b-form-input :value="balance()|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm">    
            €
          </b-col>
          <b-col cols="1" class="cForm">    
            =
          </b-col>
          <b-col cols="2">
            <b-form-input value="0" :value="(balance()*100/brutto)|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm text-left">
            %
          </b-col>
        </b-row>
        <br>
      </b-col>
    </b-row>
    <b-row  v-show="op">
      <b-col cols="5" >
        <b-textarea  @change.native="updateComment(comment)" placeholder="Description" v-model="comment" class="cForm-input"></b-textarea>
        <br>
      </b-col>
      <b-col cols="7">
        <b-input-group v-for="(operation, index) in op" :key="op.id">
          <div style="background-color:#e9ecef;width:20px;"
            class="text-center border cForm-input">
            {{(index+1)}}
          </div>
          <b-input type="date" class="cForm-input" @change="updateBalance($event, operation.id, 'date')" :value="operation.date"/>
            <b-select @change="updateBalance($event, operation.id, 'type')" :value="operation.type" style="height:19px" :options="['DEBET','CREDET']" class="customButton">
            </b-select>
            <b-form-input type="text" class="text-right cForm-input" @change="updateBalance($event.replace(',', '.'), operation.id, 'value');balance();" :value="operation.value|thousandSeparator"/>
              <b-col cols="1"  style="background-color:#e9ecef" class="text-right border cForm-input">

                <b-link class="fas fa-trash fa-w-16 text-center" @click="removePay(operation.id)"/>
              </b-col>
        </b-input-group>   
      </b-col>
    </b-row>
    <b-input-group>
    <b-button type="button" variant="outline-secondary"  @click="tabxmodal=false">Close</b-button>
      <b-button @click="addPayment"  v-show="op" variant="outline-secondary">
        Add Payment
      </b-button>
      <b-form-input id="netto" :state="null" type="text" disabled class=" text-right" :value="allbalance()" />
    </b-input-group>
</b-container>
            </template>
        </b-modal>
        <container-header class="container-fluid">
            <top-menu>
            </top-menu>
        </container-header>
        <container-body class="container-fluid">
            <b-card-group deck>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab>

                            <template #title>
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="tabxmodal=true">
                                    <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                                </svg>
                                Balance
                            </template>
                            <container>
                            <container-header class="container-fluid">
                                <b-input-group style="margin-bottom: 5px">
                                 <b-input placeholder="[search]" v-model="keyword" busy.sync="isBusy"/>
                                
                                <template #append>
                                  <b-dropdown text="options" variant="outline-secondary">
                                    <b-form-checkbox-group style="width:100%"
                                      button-variant="outline-secondary"
                                      stacked
                                      :checked="selected"
                                      :options="typesForTablesOpt"
                                      @change="keywordChange($event)"
                                      buttons />
                                  </b-dropdown>
                                </template>
                              </b-input-group>
                            </container-header>
                            <container-body class="container-fluid">
<br>
                            <balance
                            :selected="selected"
                            :rowId="rowId"
                            :brutto="brutto"
                            :op="op"
                            :comment="comment"
                            :typesForTablesOpt="typesForTablesOpt"
                            :fieldsTable="fieldsTable"
                            :options="options"
                            :result="result"
                            :items="items"
                            :keyword="keyword"

          
                            @dataToFoot="dataToFoot"

                            >
                           
                            </balance>
                            </container-body>

<container-footer>
<b-row v-show="op" style="border-top: 1px solid black;padding-top:7px;">
      <b-col sm="5" class="cuestomRow">
        <b-row>
          <b-col class="text-center">
            Amounts
          </b-col>
        </b-row>
        <b-form-group horizontal :label-cols="5"  class="cForm" label="Invoice Amount:">
          <b-row>
            <b-col cols="7">
              <b-form-input  type="text" :value="brutto|thousandSeparator" disabled class="cForm-input  text-right" />
            </b-col>
            <b-col cols="2">
              €
            </b-col>
          </b-row>
        </b-form-group>
      </b-col>
      <b-col sm="7" class="cuestomRow">
        <b-row>
          <b-col cols="4" class="cForm">    
            Payments:
          </b-col>
          <b-col cols="3">    
            <b-form-input :value="summ()|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm">    
            €
          </b-col>
          <b-col cols="1" class="cForm">    
            =
          </b-col>
          <b-col cols="2">
            <b-form-input :value="(summ()*100/brutto)|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm text-left">
            %
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="4" class="cForm">    
            Outstanding balance:
          </b-col>
          <b-col cols="3">    
            <b-form-input :value="balance()|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm">    
            €
          </b-col>
          <b-col cols="1" class="cForm">    
            =
          </b-col>
          <b-col cols="2">
            <b-form-input value="0" :value="(balance()*100/brutto)|thousandSeparator" type="text" disabled class="cForm-input text-right" />
          </b-col>
          <b-col cols="1" class="cForm text-left">
            %
          </b-col>
        </b-row>
        <br>
      </b-col>
    </b-row>
    <b-row  v-show="op">
      <b-col cols="5" >
        <b-textarea  @change.native="updateComment(comment)" placeholder="Description" v-model="comment" class="cForm-input"></b-textarea>
        <br>
      </b-col>
      <b-col cols="7">
        <b-input-group v-for="(operation, index) in op" :key="op.id">
          <div style="background-color:#e9ecef;width:20px;"
            class="text-center border cForm-input">
            {{(index+1)}}
          </div>
          <b-input type="date" class="cForm-input" @change="updateBalance($event, operation.id, 'date')" :value="operation.date"/>
            <b-select @change="updateBalance($event, operation.id, 'type')" :value="operation.type" style="height:19px" :options="['DEBET','CREDET']" class="customButton">
            </b-select>
            <b-form-input type="text" class="text-right cForm-input" @change="updateBalance($event.replace(',', '.'), operation.id, 'value');balance();" :value="operation.value|thousandSeparator"/>
              <b-col cols="1"  style="background-color:#e9ecef" class="text-right border cForm-input">

                <b-link class="fas fa-trash fa-w-16 text-center" @click="removePay(operation.id)"/>
              </b-col>
        </b-input-group>   
      </b-col>
    </b-row>
    <b-input-group>
      <b-button @click="addPayment"  v-show="op" variant="outline-secondary">
        Add Payment
      </b-button>
      <b-form-input id="netto" :state="null" type="text" disabled class=" text-right" :value="allbalance()" />
    </b-input-group>
</container-footer>
</container>
                        </b-tab>
                    </b-tabs>
                </b-card>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Bank">
                            <container>
                                <container-body>
                                    <iframe
                                        :src="bank"
                                        frameborder="0"
                                        style="height: 100vh;width:100%"
                                        name="myFrame" >
                                    </iframe>
                                </container-body>
                                <container-footer>
                                    <b-container>
                                        <b-button @click="bank='https://www.sparkasse-darmstadt.de'" variant="outline-secondary">
                                            Sparkasse-Darmstadt
                                        </b-button>
                                        <b-button @click="bank='https://www.volksbanking.de'" variant="outline-secondary">
                                            Volksbanking
                                        </b-button>
                                        <b-button @click="bank='https://www.paypal.com'" variant="outline-secondary">
                                            PayPal
                                        </b-button>
                                    </b-container>
                                </container-footer>
                            </container>
                        </b-tab>
                    </b-tabs>
                </b-card>
            </b-card-group>
        </container-body>
    </container>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            result:[],
            keyword: '',
            bank:null,
            tabxmodal:false,
            items:[],
            selected: ['Unpaid Invoices'],
            rowId:null,
            brutto:null,
            op:null,
            comment:null,
            typesForTablesOpt:['Unpaid Invoices', 'Paid Invoices', 'Sub Invoices'],
             fieldsTable: {
                number: {
                    label: 'Number',
                    sortable: true,
                    variant:''
                },
                cnumber: {
                    label: 'Contract',
                    sortable: true,
                    variant:''
                },
                date: {
                    label: 'Date',
                    sortable: true,
                    variant:''
                },
                street1: {
                    label: 'Street',
                    sortable: true,
                    variant:''
                },
                name: {
                    label: 'Customer',
                    sortable: true,
                    variant:''
                },
                netto: {
                    label: 'Netto',
                    sortable: true,
                    variant:'',
                    class: 'text-lg-right'
                },
                brutto: {
                    label: 'Brutto',
                    sortable: true,
                    variant:'',
                    class: 'text-lg-right'
                },
                status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },
                days:{
                    label: 'Days',
                    sortable: true,
                    variant:'',
                    class: 'text-lg-right'
                }
            },
            options: [{
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
        }
    },


    methods: {





    countDigitals(val){
        var nuls=3-val.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        val='0'+val
                    }
        return val
    },
        getBalance(){
                this.items = []
                axios.get('/balance').then(response => {
                response.data.reverse().forEach((v)=>{
                    v.status_set = (this.summFromRow(v, v.brutto)*66/v.brutto)+((34-(-this.difdate(v.date))*34/14)/2)
                    v.days = v.date
                    var withOut=100-(this.summFromRow(v, v.brutto)*100/v.brutto)
                    this.selected.forEach((vx)=>{
                        if(vx=='Unpaid Invoices'){
                            if (v.type=='Invoices'){
                                if (withOut >= 99){
                                    this.items.push(v)
                                }
                           }
                        }
                        if(vx=='Paid Invoices'){
                            if (v.type=='Invoices'){
                                if (withOut <= 99){
                                    this.items.push(v)
                                }
                           }
                        }
                        if (v.type==vx){
                            if (v.type=='Sub Invoices'){
                                v.brutto= -v.brutto
                                v.netto= -v.netto
                                this.items.push(v)
                            } 
                        }
                    })
                    if (this.rowId!=null){
                            if (v.id==this.rowId){
                                this.brutto = v.brutto,
                                    this.op = v.op
                            }                
                    }            
                })
            })
        },
        summFromRow(row, brutto){
            var result = 0
            row.op.forEach((v)=>{
                 result = parseFloat(result) + parseFloat(v.value)
            })
            if (result>brutto){
                result = brutto
            }
            if (result<(-brutto)){
                result = -brutto
            }
            return result
        },

   difdate(val){
        var date1 = new Date(val)
        var date2 = new Date()
        var daysLag = Math.ceil(Math.abs(date2.getTime() - date1.getTime()) / (1000 * 3600 * 24))
        return (-14+(daysLag-1))
    },
    keywordChange(val){
      this.selected = val
      this.keyword = this.keyword+' '
      this.keyword = this.keyword.slice(0,-1)
      this.getBalance()
    },
        updateBalance(val, id, fild) {
        if ((id!=undefined)&&(val!=undefined)){
             axios.get('/update_payment', {
                params: {
                    id: id,
                    value: val,
                    fild: fild
                }
            })
         }
    },
    updateComment(val) {
        axios.get((this.rowId[0]=='s')?'/update_comment_sub':'/update_comment', {
            params: {
                id: this.rowId,
                value: val
            }
        })
    },
    dataToFoot(item){
        this.items.forEach((v)=>{
            v._rowVariant=''
        })
        item._rowVariant ='secondary',
        this.brutto=parseFloat(item.brutto),
        this.op = item.op,
        this.rowId = item.id,
        this.comment = item.comment
    },
  addPayment(){
        var brutto=(this.brutto < 0) ? -this.brutto : this.brutto
        axios.get('/add_payment', {
            params: {
                id: this.rowId,
                value: brutto,
                type: (this.brutto < 0) ? 'CREDET' : 'DEBET'
            }
        })
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


getRandomInt () {
        return Math.floor(Math.random() * (50 - 5 + 1)) + 5
      },
summ(){
    if(this.op){
    var result = 0
    this.op.forEach((v)=>{
        result = parseFloat(result) + (v.type == 'CREDET') ? -parseFloat(v.value): parseFloat(v.value)
    })
    return result}
},
    allbalance(){
    var brutto = 0;
    var netto = 0;
    this.items.forEach((v)=>{
        brutto = brutto + parseFloat(v.brutto),
        netto = netto + parseFloat(v.netto)
    })
    if (
        (this.$security.account['id']==1) ||
        (this.$security.account['id']==3)
        ) {
    return 'Netto '+this.$options.filters.thousandSeparator(netto)+' €  Brutto '+this.$options.filters.thousandSeparator(brutto)+' €'
    }
    },

balance(){
    if(this.op){
    var result = parseFloat(-this.brutto)
    this.op.forEach((v)=>{
        result = parseFloat(result) + (v.type == 'CREDET') ? -parseFloat(v.value): parseFloat(v.value)
    })
    return parseFloat(result)}
}
    },
      mounted(){
    setTimeout(() => {
        this.$socket.send('getBalance')
        this.$options.sockets.onmessage = (data) => (data.data=='getBalance') ? this.getBalance(): ''
  },1000);
        }
}
</script>