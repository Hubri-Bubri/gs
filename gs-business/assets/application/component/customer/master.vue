<template>

    <container class="container-fluid">
    
        <container-header>
            <top-menu>

<b-input-group style="margin-bottom: 5px">
                            <b-input placeholder="search" v-model="keyword" />

                           <b-form-checkbox-group
        v-model="selected"
        :options="types_for_tables_opt"
        @change="keywordChange()"
        buttons
      ></b-form-checkbox-group>
   </b-input-group>

            </top-menu>
        </container-header>
        <container-body>
            <b-card header="Customers" class="gs-container">
                <container>

                    <container-body>
                        <b-table stacked="lg" hover :items="items_search" :fields="fields" @row-clicked="inItemClick"  class="tableProject" small busy.sync="isBusy">
                             <template slot="in" slot-scope="data">
                               {{ data.index + 1 }}
                            </template>
                            <template slot="old" slot-scope="data">
                               <b-form inline  class="ccbox" v-on:click.stop.pervent>
                                 <b-form-checkbox @change="changeOld(data.item.id, $event);(data.item.old=data.item.old?0:1);(show=='Show')?itemsFilter(1):'';"  plain :checked="data.item.old=(data.item.old==0)?false:true"  style="margin: 0px;" class="withoutPad">
                                 </b-form-checkbox>
                                </b-form>
                            </template>
                            <template slot="data" slot-scope="data">
                                {{data.item.data | dateInverse}}
                            </template>
                         <!--   <template slot="invoice" slot-scope="data">
                                    <b-button size="sm" @click.stop="getInvoice(data.item.id)" v-b-modal.invoice variant="outline-secondary" class="mr-1 fas fa-dollar-sign" />
                            </template>
                            <template slot="offer" slot-scope="data">
                                <b-button size="sm" @click.stop="getOffer(data.item.id)" v-b-modal.offer  variant="outline-secondary" class="mr-1 fas fa-hand-holding-usd" />
                            </template> -->
                        </b-table>
                        <div v-show="items_search.length==0">
 <Spinner size="large" ></Spinner>
</div>
                    </container-body>
                </container>
                <b-card-footer>
                    <b-button @click="itemsFilter((show!='Show')?1:0); show=(show!='Show')?'Show':'Hide'">{{show}}</b-button>
                    <b-button @click="addCustomer">Add Customer</b-button>
                </b-card-footer>
            </b-card>
        </container-body>
          <b-modal id="offer"  size="lg" title="Offer List" ok-only  centered>

          <!--   <b-table hover stacked="sm" :items="offers" :fields="fieldsOffer" @row-clicked="inOfferClick"  class="tableProject" small >
                    <template slot="status_set" slot-scope="offer">
                        <b-row>
                            <b-col cols="6">  {{ offer.item.status_set }}  </b-col>   <b-col cols="1"><i class="fas fa-circle fa-w-16 fa-2x " :style="computeStyleOffer(offer.item.status_set)"></i></b-col>
                   </b-row>
                    </template>
            </b-table> -->
           </b-modal>
         <b-modal id="invoice" size="lg" title="Invoice List" ok-only  centered>
         <!--   <b-table hover  stacked="sm" :items="invoices" :fields="fieldsInvoice" @row-clicked="inItemClick"  class="tableProject" small >
                    <template slot="status_set" slot-scope="invoice">
                        <b-row>
                            <b-col cols="6">  {{ invoice.item.status_set }}  </b-col>   <b-col cols="1"><i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleInvoice(invoice.item.status_set)"></i></b-col>
                   </b-row>
                    </template>
            </b-table> -->
          </b-modal>
    </container>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            additem:[],
            keyword: '',
            selected: ['web', 'bic', 'iban', 'tax'],
            types_for_tables_opt:['web', 'bic', 'iban', 'tax'],
            countNamePerson:[''],
            countMailPerson:[''],
            countPhonePerson:[''],
            countFaxPerson:[''],
            countOtherPerson:null,
            addFirm:null,
            addAppeal:null,
            addDep:null,
            addPos:null,
            show:"Show",
            fields: {
                in: {
                label: 'Number',
                sortable: true,
                class: 'n'
                },
                name: {
                label: 'Name',
                sortable: true,
                class: 'number',
                variant: ''
                },
                data: {
                label: 'Registred',
                sortable: true,
                class: 'number',
                variant: ''
                },
                zip: {
                label: 'ZIP',
                sortable: true,
                class: 'number',
                variant: ''
                },
                city: {
                label: 'City',
                sortable: true,
                class: 'number',
                variant: ''
                },
                 street: {
                label: 'Street',
                sortable: true,
                class: 'number',
                variant: ''
                },
                old: {
                label: 'Old',
                sortable: true,
                class: 'number',
                variant: ''
                }
                
                },




            fieldsOffer: {
                offer_number: {
                label: 'Offer Number',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                class: 'other'
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status'
                }
                },
            fieldsInvoice: {
                invoice_number: {
                label: 'Invoice Number',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                class: 'other'
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status'
                }
                },
               options: [
                         { value: 'Open', text: 'Open' },
                         { value: 'Done', text: 'Done'},
                         { value: 'Invoice', text:'Invoice' },
                         { value: 'Desiccation', text:'Desiccation' },
                         { value: 'Leakage_Detection', text:'Leakage Detection' },
                         { value: 'Restoration', text:'Restoration'}
               ],
            items: [],
            items1:[],
            ddd: 0,
            idSpan: 0,
            offers: null,
            invoices: null
        }
    },
    computed:{
items_search() {
            this.fields.name.variant =
            this.fields.data.variant =
            this.fields.zip.variant =
            this.fields.city.variant =
            this.fields.street.variant = ''
      if (this.keyword){

         return this.items.filter(item =>{

         if (item.name!=null){
          if (item.name.includes(this.keyword)){
            this.fields.name.variant = 'info'
            return true
          }}
          if (item.data!=null){
          if (item.data.includes(this.keyword)){
            this.fields.data.variant = 'info'
            return true
          }}
          if (item.zip!=null){
          if (item.zip.includes(this.keyword)){
            this.fields.zip.variant = 'info'
            return true
          }}
          if (item.city!=null){
          if (item.city.includes(this.keyword)){
            this.fields.city.variant = 'info'
            return true
          }}
          if (item.street!=null){
          if (item.street.includes(this.keyword)){
            this.fields.street.variant = 'info'
            return true
          }}

            if(this.selected.indexOf('iban') > -1) {
                if (item.iban) {
                    if (item.iban.includes(this.keyword)){
                        this.fields.name.variant = 'info'
                        return true
            }}} 
            if(this.selected.indexOf('bic') > -1) {
                if (item.bic) {
                    if (item.bic.includes(this.keyword)){
                        this.fields.name.variant = 'info'
                        return true
            }}} 
            if(this.selected.indexOf('tax') > -1) {
                if (item.tax) {
                    if (item.tax.includes(this.keyword)){
                        this.fields.name.variant = 'info'
                        return true
            }}}
            if(this.selected.indexOf('web') > -1) {
                if (item.web) {
                    if (item.web.includes(this.keyword)){
                        this.fields.name.variant = 'info'
                        return true
            }}}  

          })
        }else{
            return this.items
        }
}
    
    },

    methods: {

    keywordChange(){
      this.keyword = this.keyword+' '
      this.keyword = this.keyword.slice(0,-1)
    },
        itemsFilter(val){
        if(val==1){
            var arr = this.items.filter(function(val){
            if (val.old==false){
                return val
            }
        })
        this.items=arr
        }else{
            this.items=this.items1
        }
        },
        rpeNumber(num){
            var nuls=3-num.toString().length
            for (var i = 0; i <= nuls; i++) {
                num='0'+num
            }

            return num
            
        },
        inItemClick(item, index, event) {
            this.$router.push({
                path: `/customer/detail/${item.id}`
            })
        },
    addCustomer(){
        axios.get('/add_customer_list').then(response => {
               this.items = response.data;
             this.$router.push({
                 path: '/customer/detail/'+this.items[this.items.length-1].id
             })
         })
        },
       getCustomers(){
        axios.get('/customer').then(response => {
               this.items= response.data
               this.items1= response.data
               this.itemsFilter((this.show!='Show')?0:1)
         })
        },
        changeOld(id, eve){
        
        axios.get('/customer_old', {
            params: {
                id: id,
                event: eve?1:0
            }
        })

        },
},
      mounted(){

  


     setTimeout(() => {
        
        this.$socket.send('getCustomers')
        this.$options.sockets.onmessage = (data) => (data.data=='getCustomers') ? this.getCustomers(): ''
        },1000);


        }

    }
</script>
