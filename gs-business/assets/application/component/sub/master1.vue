<template>
    <container class="container-fluid">
        <container-header>
            <top-menu></top-menu>
        </container-header>
        <container-body>
            <b-card header="Project" class="gs-container">
                <container>
                    <container-header>
                        <b-input-group style="margin-bottom: 5px">
                            <b-input placeholder="[search]" v-model="keyword" />

                           <b-form-checkbox-group
        v-model="selected"
        :options="types_for_tables_opt"
        @change="keywordChange()"
        buttons
      ></b-form-checkbox-group>
   </b-input-group>


                        </b-form>
                    </container-header>
                    <container-body>
           <v-infinite-scroll :loading="loading" @bottom="nextPage" :offset='20' style="max-height: 80vh; overflow-y: scroll;">

                        <b-table stacked="sm" hover  :items="items_search" :fields="fields"  @row-clicked="inItemClick"  class="tableProject" small busy.sync="isBusy">
                            
                        
                               <template slot="project_number" slot-scope="data">
                                  {{rpeNumber(data.item.id)}}-{{data.item.project_number_year}}
                                </template>
                                <template slot="status_set" slot-scope="data">
                                   <b-form inline v-on:click.stop.prevent class="status">
                                      <b-form-select  v-model="data.item.status_set" @change="updateWork($event, data.item.id)">
                                           <option v-for="opt in options" >{{opt.text}}</option>
                                       </b-form-select>
                                   </b-form>
                                </template>
                                <template slot="other" slot-scope="data">
                                   {{firstRos(data.item.other)}}
                             <!--    <vue-editor class="modEdit"
                                     :value="firstRos(data.item.other)" 
                                     >
                                  </vue-editor> -->
                              </template>
                                <template slot="invoice" slot-scope="data">
                      
                                    <b-button size="sm" @click.stop="getOffer(data.item.id)" v-b-modal.invoice variant="outline-secondary" class="mr-1 fas fa-dollar-sign" />
                                </template>

                        <!--         <template slot="offer" slot-scope="data">
                                    <b-button size="sm" @click.stop="data.toggleDetails" variant="outline-secondary"  class="mr-1 fas fa-info" />
                                </template> -->


                            <template slot="row-details" slot-scope="data">
                                <b-row>
                                    <b-col v-html="data.item.other" class="pWOutMargin"></b-col>
                                </b-row>
                            </template>

     </b-table>
       </v-infinite-scroll>
                    </container-body>
                </container>
                <b-card-footer>
                  <b-button @click="addProject">Add Project</b-button>
                  <!-- <b-button @click="addProject">Add Project</b-button> -->
                </b-card-footer>
            </b-card>
        </container-body>
  <b-modal id="invoice" size="lg" title="List" ok-only  centered>
    <div v-for="name in types_for_tables">
                                   {{name.type}}   
                                    <b-table class="tableProject" striped hover :items="getItems(name.type)" :fields="fieldsTable">
                                        <template slot="number" slot-scope="it">
                                             <b-link @click.stop="findRow(it.item.number, name.type)"
                                             v-if="it.item.number.split(' ')[1]">{{ it.item.number.split(' ')[0] }}</b-link>
                                             <div v-else>{{ it.item.number.split(' ')[0] }}</div>
                                        </template>

                                        <template slot="delete" slot-scope="it">
                                            <b-col align-self="center">
                                                <b-link @click="offerDel(it.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>

                                      <template slot="status_set" slot-scope="it" >
                                          <line-chart :datas="dataCharts(it.item)" v-if="name.type=='Invoices'"
                                          :width="150"  :height="20" style="margin-left: -15px;">
                                          </line-chart>
                                          <b-form inline v-else>
                                                <b-form-select v-model="it.item.status_set" @change="updateItem($event, name.type, it.item.id)"
                                                class="w-100" :style="computeStyleOfferM(it.item.status_set)">
                                                  <option v-for="opt in options" :style="computeStyleOfferM(opt.text)">
                                                  {{opt.text}}
                                                  </option>
                                                </b-form-select>
                                            </b-form>
                                      </template>
                                    </b-table>
                                  </div>
          </b-modal>

  <b-modal id="addProjectWithDate" ref="addProjectWithDate"  size="md" title="Data Of Project" centered>
    
                                      
                                                <b-form-group horizontal :label-cols="4" label="Zip code:" >
                                                    <b-form-input  :state="null" type="text" v-model="zip" @input="searchZip($event)" placeholder="Enter zip code"   />
                                                </b-form-group>
                                           
                                                <br>
                                          
                                                <b-form-group horizontal :label-cols="4" label="City:" >
                                                    <b-form-input  :state="null" type="text"  :value="city" placeholder="Enter city"   />
                                                </b-form-group>
                                             <br>

                                                   <b-form-group horizontal :label-cols="4"  label="Street:">
                                                    <b-input-group>
                                                        <b-form-input :state="null" v-model="street" type="text" placeholder="Enter street" />
                                                        <b-button v-b-modal.map >
                                                            G
                                                        </b-button>
                                                    </b-input-group>
                                                   
                                                </b-form-group>
                                            
<template slot="modal-footer">
                    <b-button type="submit" variant="primary" @click="createProject">
                        OK
                    </b-button>
                </template>
          </b-modal>
           <b-modal size="lg" centered ok-only id="map" title="Track">
            <b-embed type="iframe" aspect="16by9" :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+street">
            </b-embed>
                    <template slot="modal-footer">
                    <b-button type="submit" variant="primary" v-b-modal.addProjectWithDate>
                        OK
                    </b-button>
                </template>
        </b-modal>
    </container>
</template>
<script>
import {VueEditor, Quill} from 'vue2-editor';
import axios from 'axios';
export default {
    components: {
        VueEditor
    },
    data() {
        return {
           selected: [], // Must be an array reference!
        options: [
          { text: 'Orange', value: 'orange' },
          { text: 'Apple', value: 'apple' },
          { text: 'Pineapple', value: 'pineapple' },
          { text: 'Grape', value: 'grape' }
        ],
            keyword: '',
            page: 1,
            // // items: [],
            loading: false,
            additem:[],
            types_for_tables:[],
            types_for_tables_opt:[],
            items_table:[],
            fields: {
                project_number: {
                label: 'Project Number',
                sortable: true,
                variant:''
                // class: 'number'
                },
                date: {
                label: 'Start',
                sortable: true,
                variant:''
                // class: 'number'
                },
                street: {
                label: 'Street',
                sortable: true,
                variant:''
                // class: 'number'
                },
                zip: {
                label: 'ZIP',
                sortable: true,
                variant:''
                // class: 'number'
                },
                city: {
                label: 'City',
                sortable: true,
                variant:''
                // class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                variant:''
                // class: 'other'
                },
                // offer: {
                // label: 'Offer',
                // variant:''
                // // class: 'number'
                // },
                invoice: {
                label: 'List',
                // class: 'number',
                variant:''
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'number',
                variant:''
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
            ddd: 0,
            idSpan: 0,
            offers: null,
            invoices: null,
            city: null,
            street: null,
            zip: null,

            fieldsTable: {
                number: {
                    label: 'Number',
                    sortable: true
                },
                date: {
                    label: 'Date',
                    sortable: true
                },
                place: {
                    label: 'Place',
                    sortable: true
                },
                insurance_number: {
                    label: 'Insurance Number',
                    sortable: true
                },

                other: {
                    label: 'Other',
                    sortable: true
                },
               

                netto: {
                    label: 'Netto',
                    sortable: true
                },

                brutto: {
                    label: 'Brutto',
                    sortable: true
                },

                 status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },

                delete: {
                    label: "&#128465;",
                    class: 'text-center'
                }
            }
        }


    },
computed:{
items_search() {
      this.fields.project_number.variant =
            this.fields.date.variant =
            this.fields.street.variant =
            this.fields.zip.variant =
            this.fields.other.variant =
            this.fields.status_set.variant =
            this.fields.invoice.variant =
            this.fields.city.variant = ''
      if (this.keyword){

         return this.items.filter(item =>{

          if ((this.rpeNumber(item.id)+'-'+item.project_number_year).includes(this.keyword)) {
            this.fields.project_number.variant = 'info'
            return true
          }
          if (item.date.includes(this.keyword)){
            this.fields.date.variant = 'info'
            return true
          }
          if (item.street.includes(this.keyword)){
            this.fields.street.variant = 'info'
            return true
          }
          if (item.city.includes(this.keyword)){
            this.fields.city.variant = 'info'
            return true
          }
          if (item.zip.includes(this.keyword)){
            this.fields.zip.variant = 'info'
            return true
          } 
          if (item.other?item.other.includes(this.keyword):''){
            this.fields.other.variant = 'info'
            return true
          }
          if (item.status_set?item.status_set.includes(this.keyword):''){
            this.fields.status_set.variant = 'info'
            return true
          } 
            this.getOfferRet(item.id, item)

            if(this.additem.length>0){
              var retid = this.additem.filter((v)=>{
                if (item.id==v) return true
              })
              if(retid.length>0){
              this.fields.invoice.variant = 'info'
                this.additem = []
                return true
              }
            }


          })
        }else{
            return this.items
        }
}
    
    },

    methods: {

      searchZip(val){
             axios.get('https://maps.google.com/maps/api/geocode/json', {
                    params: {
                        components: "country:DE|postal_code:"+val,
                        sensor: "false",
                        language: "en",
                        key: "AIzaSyDKWZ-Jrk9KMoHYakuQfD6xQ4qUZ2XkGpo"
                    }
                }).then(response => {
                      if (JSON.parse(response.request.response).results[0]!=undefined){
                      var city = JSON.parse(response.request.response).results[0].formatted_address.split(' ')[1].split(',')[0]
                      this.city = city

                  }
                })
  
        },

    keywordChange(){
      this.keyword = this.keyword+' '
      this.keyword = this.keyword.slice(0,-1)
    },
 getOfferRet(project_id, item){
axios.get('/sub_detail_new', {
  params: {
    id: project_id
  }
}).then(response => {
  var newresp = response.data.filter((v)=>{
    var result = 0
    this.selected.forEach((s)=>{
      if (s == v.type){
        result=result+1
      }
    })
    if (result>0){
      return v
    }
    
  })


     if(JSON.stringify(newresp).includes(this.keyword)){
          if (this.additem.indexOf(item.id)==-1){
            this.additem.push(item.id)
          }
          
      }
})




        },

prevPage () {
       if (this.page == 1) return
       --this.page
       this.api()
     },
     nextPage () {
       ++this.page
       this.api()
     },
     api () {
       this.loading = true
       axios.get('/sub', {
            params: {
              page: this.page
            }
  }).then((response) => {
         this.items = response.data
         this.loading = false
       })
     },


updateWork(val, id){
        axios.get('/updateSub', {params: {
                id: id,
                date: val,
                fild: 'status_set'
        }})
},
findRow(id, name){
var intId=parseInt(id.split(' ')[1])
var rows = this.getItems('Contracts').filter((v)=>{
    if(v.id==intId){
     return v
    }
})

   this.inItemGetData(rows[0], 0)

},
getItems(type){
  return this.items_table.filter((v)=>{
    if (v.type == type){
      return v
    }
  })
}, 
dataCharts(val){

    var pay = this.summFromRow(val, val.brutto)*100/val.brutto
    var withOut =100-(this.summFromRow(val, val.brutto)*100/val.brutto)
    // var days = ((-this.difdate(val.date)*34/14)<=0)?0:-this.difdate(val.date)*34/14


    // if (pay >= withOut){
    // pay = pay + (34 - days)
    // } else{
    // withOut = withOut + (34 - days)
    // }
    
    // pay = pay.toFixed(0)
    // withOut = withOut.toFixed(0)
    // days = days.toFixed(0)

    // console.log(pay, withOut, days, pay+withOut+days)
    return [pay, withOut]
    },
    updateItem(val, type, id){
      axios.get('/update_item_from_sub', {
            params: {
                 val: val,
                 id: id
               }
      })
    },
            computeStyleOfferM(value) {
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
    summFromRow(row, brutto){
    // console.log(brutto)
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
    },
        offerDel(del_id) {

            if (confirm("Are you sure?")) {
                axios.get('/del_item_sub', {
                    params: {
                        id: del_id
                    }
                }).then(response => {
                    this.offers = response.data
                })
            };
},
        firstRos(val){
            if (val!=null){
                if (val.split('</p>').length>0){
                    var firstRow = val.split('</p>')
                    var firsrtRow1 = firstRow[0].split('<p>')
                    return firsrtRow1[1]
                }
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
                path: `/sub/detail/${item.id}`
            })
        },
        inOfferClick(item, index, event) {
            this.$router.push({
                path: `/sub/detail/${item.id}/offer/${offer.id}`
            })
        },
    getOffer(project_id){


axios.get('/get_types_for_tables', {
}).then(response => {
  this.types_for_tables = response.data;
})
axios.get('/sub_detail_new', {
  params: {
    id: project_id
  }
}).then(response => {
  this.items_table = response.data;
})




        },


    getInvoice(project_id){
        axios.get('/invoice_sub', {params: {id: project_id}}).then(response => {
               this.invoices = response.data
         })
        },
    addProject(){
      this.$refs.addProjectWithDate.show()

     this.city = ""
     this.street = ""
     this.zip = ""
        },
      createProject(){
      this.$refs.addProjectWithDate.hide()

        axios.get('/add_sub', {
            params: {
               city: this.city,
               street: this.street,
               zip: this.zip
            }
        }).then(response => {
               this.items = response.data
             this.$router.push({
                 path: '/sub/detail/'+this.items[this.items.length-1].id
             })
         })
      },
       getSub(){
        axios.get('/sub', {
            params: {
              page: 1
            }
  }).then(response => {
                 this.items = response.data
                this.loading = false
          });
  axios.get('/get_types_for_tables', {
}).then(response => {
  this.types_for_tables_opt = []
  response.data.forEach((v)=>{
    this.types_for_tables_opt.push(v.type)
    this.selected.push(v.type)
  })
});

        },
        computeStyle(value) {
             switch (value) {
                    case 'Open':
                    return {
                        'background-color': '#FFFFFF'
                    };
                case 'Done':
                    return {
                        'background-color': '#00f25A'
                    };
                case 'Invoice':
                    return {
                        'background-color': 'yellow'
                    };
                case 'Desiccation':
                    return {
                        'background-color': 'grey'
                    };
                case 'Leakage Detection':
                    return {
                        'background-color': 'red'
                    };
                case 'Restoration':
                    return {
                        'background-color': 'blue'
                    };
                }
        },
        computeStyleOffer(value) {
            switch (value) {
                case 'Not Finished': return {'color': 'grey'};
                case 'Sent': return {'color': 'orange'};
                case 'Denied': return {'color':'red'};
                case 'Agreement': return {'color':'green'};
            }
        },
        computeStyleInvoice(value) {
            switch (value) {
                case 'Paid': return {'color': 'green'};
                case 'Not Paid': return {'color': 'gray'};
                case 'Overdue': return {'color':'red'};
                case 'Partially Paid': return {'color':'orange'};
            }
        }
},
      mounted(){
        setTimeout(() => {
            this.$socket.send('getSub')
            this.$options.sockets.onmessage = (data) => (data.data=='getSub') ? this.getSub(): ''
        },1000);
        }
    }
</script>
<style type="text/css">
    .pWOutMargin p{
        margin-bottom:0px; 
    }
</style>