<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-card class="gs-container" header-class="mx-0 px-0">
        <template #header>
          <b-row fluid align-v="end">
            <b-col col xl="2" lg="2" md="2" sm="2" cols="3">
              <b-button @click="addProject" variant="primary" class="text-nowrap">{{$t('projects.addProject')}}</b-button>
            </b-col>
            <b-col col  xl="3" lg="3" md="8" sm="8" cols="6">

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
                    <b-form-checkbox v-for="fild in filterFilds(fields)" :key="fild.key" :value="fild.key">
                      {{fild.label}}
                    </b-form-checkbox>
                    </b-form-checkbox-group>
                  </b-dropdown>
            </b-col>
            <b-col col  xl="6" lg="6" md="12" sm="12" cols="8">
              <b-form-checkbox-group
              class="text-lg-nowrap text-xl-nowrap  text-sm-left text-md-left p-1 text-lg-right"
              switches
              v-model="selected"
              :options="types_for_tables_opt"
              @change="keywordChange($event)"
              />
            </b-col>
          </b-row>
        </template>
        <container>
          <container-body>
            <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
              <!-- :busy="((items.length==0) && (selected.length!=0))" -->

            <b-table hover :items="items" :fields="getFields()" @row-clicked="inItemClick" 
              :filter="filter"
              :filter-included-fields="filterOn"
              @filtered="onFiltered"
              no-border-collapse
              stacked="lg"
              show-empty
              :busy="isBusy"
             >
              <template #cell(status_set)="data" >


                    <b-icon v-for="plan in getPlans(data.item.subPlan)" v-if="(data.item.subPlan!=undefined)"
                    :icon="(plan.autosend==1)?'arrow-repeat':'gear'" aria-hidden="true" scale="2" :key="plan.id"
                    :variant="detectColorPlan(plan.lastsend)" style="margin:9px;" />

                    <b-icon icon="card-text" aria-hidden="true" v-if="(data.item.subPlan==undefined)||(data.item.subPlan.length==0)"
                     scale="1.5" />


              </template>
              <template #cell(other)="data">
                <div class="text-container">
                  <span  class="text-content" v-html="firstRos(data.item.other, '', '', 'h')"
                  :title="firstRos(data.item.other, data.item.user?'['+data.item.user+' ':'', data.item.datacomment?data.item.datacomment+']':'', 't')" />
                </div>
              </template>
              <template #cell(invoice)="data">
                <b-button size="sm" @click.stop="getOffer(data.item.id)" v-b-modal.invoice variant="primary">
                  <b-icon icon="inbox-fill" aria-hidden="true"></b-icon>
                </b-button>
              </template>
              <template #cell(number)="data">
                <b-row>
                  <b-col>
                    {{data.item.number}}
                  </b-col>
                </b-row>
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
    <b-modal :title="$t('projects.list')" ok-only size="xl" id="invoice">
        <div v-for="name in types_for_tables">
          <span v-if="getItems(name.type).length!=0">{{name.type}}</span>
          <b-table :items="getItems(name.type)" :fields="fieldsTable" v-if="getItems(name.type).length!=0" hover stacked="lg">
            <template #cell(brutto)="it">
              <div class="text-container">
                <span  class="text-content" style="white-space: nowrap;">{{it.item.brutto|thousandSeparator}}  &nbsp;</span>
              </div>
            </template>
            <template #cell(netto)="it">
              <div class="text-container">
                <span  class="text-content"  style="white-space: nowrap;">{{it.item.netto|thousandSeparator}}  &nbsp;</span>
              </div>
            </template>
            <template #cell(number)="it">
              <div style="white-space: nowrap;">{{ it.item.number.split(' ')[0] }}  &nbsp;</div>
            </template>
            <template #cell(delete)="it">
              <b-col align-self="center">
                <b-link @click="offerDel(it.item.id)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-link>
              </b-col>
            </template>
            <template #cell(other)="it">
              <span  class="text-content" style="white-space: nowrap;">{{it.item.other}}  &nbsp;</span>
            </template>
            <template #cell(date)="it">
              <span  class="text-content" style="white-space: nowrap;">{{it.item.date}}  &nbsp;</span>
            </template>
            <template #cell(place)="it">
              <span  class="text-content" style="white-space: nowrap;">{{it.item.place}}  &nbsp;</span>
            </template>
            <template #cell(insurance_number)="it">
              <span  class="text-content" style="white-space: nowrap;">{{it.item.insurance_number}}  &nbsp;</span>
            </template>
            <template #cell(status_set)="it">
              <line-chart :datas="dataCharts(it.item)" v-if="name.type==('Invoices')"
              :width="150"  :height="20" style="margin-left: -15px;">
              </line-chart>
              <line-chart :datas="dataCharts(it.item)" v-if="name.type==('Sub Invoices')"
              :width="150"  :height="20" style="margin-left: -15px;">
              </line-chart>
              <b-form-select v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)" v-if="name.type=='Orders'"
                size="sm" :style="computeStyleOfferM(it.item.status_set)"> 
                  <option v-for="opt in order_options" :style="computeStyleOfferM(opt.text)">
                    {{opt.text}}
                  </option>
              </b-form-select>
              <b-form-select v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)"
              size="sm" :style="computeStyleOfferM(it.item.status_set)" v-if="name.type=='SUB'"> 
                  <option v-for="opt in order_options" :style="computeStyleOfferM(opt.text)">
                    {{opt.text}}
                  </option>
              </b-form-select>
              <b-form-select v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)"  v-if="name.type=='Offers'"
               :style="computeStyleOfferM(it.item.status_set)" size="sm">
                  <option v-for="opt in order_options" :style="computeStyleOfferM(opt.text)">
                    {{opt.text}}
                  </option>
              </b-form-select>
            </template>
          </b-table>
        </div>
    </b-modal>
    <b-modal id="addProjectWithDate" ref="addProjectWithDate" :title="$t('projects.addProjectWithDate')"  size="md">
      <b-form-group :label="$t('projects.country')+':'" label-cols="4">
        <b-select selected="Germany" value-field="code" text-field="name" v-model="selectedCornty"  :options="countries" :name="nohash" />
      </b-form-group>
      <b-form-group :label="$t('projects.zip')+':'" label-cols="4">
        <b-form-input type="text" v-model="zip" @input="searchZip($event)" :placeholder="$t('projects.ezip')" :name="nohash" />
      </b-form-group>
      <b-form-group :label="$t('projects.area')+':'" label-cols="4" >
        <b-form-input type="text" v-model="area" :placeholder="$t('projects.earea')" :name="nohash" />
      </b-form-group>
      <b-form-group :label="$t('projects.city')+':'" label-cols="4" >
        <b-form-input type="text"  v-model="city" :placeholder="$t('projects.ecity')" :name="nohash" />
      </b-form-group>
      <b-form-group :label="$t('projects.street')+':'" label-cols="4">
        <b-input-group>
          <b-form-input v-model="street" type="text" :placeholder="$t('projects.estreet')" :name="nohash" />
            <b-button v-b-modal.map variant="primary">
              <b-icon icon="pin-map-fill" aria-hidden="true"></b-icon>
            </b-button>
        </b-input-group>
      </b-form-group>
      <template slot="modal-footer">
        <b-button @click="createProject">
          OK
        </b-button>
      </template>
    </b-modal>
    <b-modal ok-only id="map" title="Track" size="lg">
      <b-embed type="iframe" aspect="16by9"
      :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
      'origin='+addressfild+'&'+
      'destination='+(street+', '+zip+' '+city).replace('undefined', '')">
      </b-embed>
    </b-modal>

    <b-modal ok-only ref="sentInvoices" :title="$t('projects.sentInvoices')" size="lg" no-close-on-esc no-close-on-backdrop hide-header-close>
      <b-row v-for="rowMail in sentEmails" :key="rowMail.id">
        <b-col>
          {{rowMail.sent}}
          {{$t('projects.wasSent')}}
          {{rowMail.to.split(',').join(', ')}} {{$t('projects.wasSentDe')}}
          
        </b-col>
      </b-row>
      <template slot="modal-footer">
        <b-button @click="closeMessage">
          OK
        </b-button>
      </template>
    </b-modal>

  </container>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
      isBusy: true,
      hideNumberOfYear:null,
      addressfild:null,
      wassentids:[],
      sentEmails:[],
      project:{contetn:'Projcet'},
      old_done: '011',
      area: null,
      selectedCornty: 'DE',
      countries:[],
      keywordOld: null,
      keyword: '',
      page: 1,
      additem:[],
      types_for_tables:[],
      items_table:[],
      order_options: [{
        value: 'Open',
        text: 'Open'
      },
      {
        value: 'Done',
        text: 'Done'
      }],
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
      area: null,
      zip: null,
      fieldsTable: [{
        key: 'number',
        label: 'Number',
        sortable: true
      },
      {
        key: 'date',
        label: 'Date',
        sortable: true
      },
      {
        key: 'place',
        label: 'Place',
        sortable: true
      },
      {
        key: 'insurance_number',
        label: 'Insurance',
        sortable: true
      },
      {
        key: 'other',
        label: 'Other',
        sortable: true
      },
      {
        key: 'netto',
        label: 'Netto',
        sortable: true
      },
      {
        key: 'brutto',
        label: 'Brutto',
        sortable: true
      },
      {
        key: 'status_set',
        label: 'Status',
        sortable: true
      }],

        totalRows: 1,
        filter: null,
        filterOn: []
    }
  },
  computed: {
    nohash(){
      return Math.random().toString(36).slice(2)
    },
    types_for_tables_opt(){
      return [
        this.$t('states.done'),
        this.$t('states.notdone'),
        this.$t('states.auto')
      ]
    },
    selected(){
      return [this.$t('states.notdone'), this.$t('states.auto')]
    },
    fields() {
      return [{
        key: 'number',
        label: 'Project',
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
        key: 'zip1',
        label: this.$t('fields.zip'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'city1',
        label: this.$t('fields.city'),
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
        key: 'date',
        label: this.$t('fields.start'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'edate',
        label: this.$t('fields.end'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'other',
        label: this.$t('fields.other'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'invoice',
        label: this.$t('fields.list')
      },
      {
        key: 'status_set',
        label: this.$t('fields.status'),
        sortable: true,
        variant: 'default'
      }]
    }
  },
  methods: {
    closeMessage(){
      axios.get('/closeWasSent', {params: {
        wassentids: this.wassentids.join()
      }})
      this.$refs.sentInvoices.hide()
    },
    detectColorPlan(val){
      if (val == 'missed'){
        return 'danger'
      }
      if (val == 'not missed'){
        return 'dark'
      }
      if (val == 'not set'){
        return 'warning'
      }
    },
    getPlans(val){
      // var autosend = 0
      // var notautosend = 0
      
      // console.log(val)
      // return val.filter((v)=>{
      //   var lastsend = 0
      //   if (v.autosend == 1){
      //     if (autosend == 0){
      //       autosend = 1
      //       v.lastsend = 'not'
      //       return v
      //     }
      //   }
      //   if (v.autosend == 0){
      //     if (v.lastsend == 'missed'){
      //       lastsend = 'missed'
      //     }
      //     if (notautosend == 0){
      //       notautosend = 1
      //       v.lastsend = lastsend
      //       return v
      //     }
      //   }
      // });
      // console.log(val)
      return val
    },
    getFields(){
      return this.fields.filter((v)=>{
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
        if ((v.key != 'invoice')&(v.key != 'status_set')) {
          return v;
        }
      })
    },
    onFiltered(filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
    },
    searchZip(val){
      axios.get('https://maps.google.com/maps/api/geocode/json', {
        params: {
          components: "country:"+this.selectedCornty+"|postal_code:"+val,
          sensor: "false",
          language: "en",
          key: "AIzaSyDKWZ-Jrk9KMoHYakuQfD6xQ4qUZ2XkGpo"
        }
      }).then(response => {
        if (JSON.parse(response.request.response).results[0]!=undefined){
          var results = JSON.parse(response.request.response).results[0]
          for (var i=0; i<results.address_components.length; i++)
          {
            if (results.address_components[i].types[0] == "locality") {
              //this is the object you are looking for City
              var  city = results.address_components[i];
            }
            if (results.address_components[i].types[0]=="postal_town"){
              //this is the object you are looking for City for GB
              var  city = results.address_components[i];
            }
            if (results.address_components[i].types[0] == "administrative_area_level_1") {
              //this is the object you are looking for State
              var  region = results.address_components[i];
            }
          }
          this.city = city?city.long_name:''
          this.area = region?region.long_name:''
        }
      })
    },
    keywordChange(e){
      var done = '0'
      var notdone = '0'
      var auto = '0'

      e.forEach((v)=>{
        if(v==this.$t('states.done')){
          done='1'
        }
        if(v==this.$t('states.notdone')){
          notdone='1'
        }
        if(v==this.$t('states.auto')){
          auto='1'
        }

      })
      if ((done+notdone+auto)!=this.old_done){
        this.getProjects(done+notdone+auto)
        this.old_done = done+notdone+auto
      }
    },
    getOfferRet(project_id, item){
      if (this.keywordOld!=this.keyword){ 
        axios.get('/project_detail_new', {
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
          this.keywordOld=this.keyword 
        })
      }
    },
    // updateWork(val, id){
    //   axios.get('/updateProject', {params: {
    //     id: id,
    //     date: val,
    //     fild: 'status_set'
    //   }})
    // },
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
      return [pay, withOut]
    },
    updateItem(val, type, id){
      axios.get('/update_item_from_project', {
        params: {
          val: val,
          type: type,
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
      if (confirm(this.$t('alert.sure'))) {
        axios.get('/del_item', {
          params: {
            id: del_id
          }
        }).then(response => {
          this.offers = response.data
        })
      };
    },
    firstRos(val, user, datacomment, t){
      if (val!=null){
        if (t=='h'){
          val = val.split('</p>').join(" &crarr; ")
          val = val.split('<br>').join(" &crarr; ")
          val = val.split('<p>').join('')
        }     
        if (t=='t'){
          val = val.split('</p>').join('\n')
          val = val.split('<br>').join('\n')
          val = val.replace(/(<([^>]+)>)/ig, "")
        }       
        val = val + '\n' +user+datacomment
        return val
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
        path: `/project/detail/${item.id}`
      })
    },
    getOffer(project_id){
      axios.get('/get_types_for_tables', {
      }).then(response => {
        this.types_for_tables = response.data;
      })
      axios.get('/project_detail_new', {
        params: {
          id: project_id
        }
      }).then(response => {
        this.items_table = response.data;
      })
    },
    addProject(){
      this.$refs.addProjectWithDate.show()
      this.area = ""
      this.city = ""
      this.street = ""
      this.zip = ""
    },
    createProject(){
      this.$refs.addProjectWithDate.hide()
      axios.get('/add_project', {
          params: {
            city: this.city,
            street: this.street,
            zip: this.zip,
            area: this.area,
            contry: this.selectedCornty,
            user: this.$security.account.id
          }
      }).then(response => {
        this.items = response.data
        this.$router.push({
          path: '/project/detail/'+this.items[this.items.length-1].id
        })
      })
    },
    getProjects(done){
      axios.get('/projects', {
        params: {
        done: done
        }
      }).then(response => {
        var sentEmails = []
        var datasent
        var lastSendShown
        this.items = response.data.filter((v)=>{
          v.number =  this.rpeNumber(v.project_number) + ((this.hideNumberOfYear!=1)?('-' + v.project_number_year):'')
          v.date = this.$options.filters.dateInverse(v.date)
          v.edate = this.$options.filters.dateInverse(v.edate)
          if (v.subPlan){
            if(v.subPlan.autosend="1"){
              v.subPlan.forEach((subPlan)=>{
                if(subPlan.datasent){
                  v.subPlan.forEach((plan)=>{
                    this.sentEmails.push({'sent':plan.lastSendShown, 'to':plan.to})
                    this.wassentids.push(plan.id)
                  })
                }
              })
            }
          }
         if(this.sentEmails.length>0){
            this.$refs.sentInvoices.show()
         }
         return v
        });
        this.isBusy = false;
      });

      // this.$refs.sentInvoices.show();
      // setInterval(this.changeColor, 2000);
    },
    // changeColor(){
    //   this.items.forEach(v=>{
    //     if (v.subPlan!=undefined) {
    //       // console.log(v)
    //       if((v.subPlan.lastsend == 'missed')&(v.subPlan.autosend == '0')){
    //         v._rowVariant=(v._rowVariant=='warning')?'danger':'warning'
    //       }
    //     }
    //   })
    // },
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
    this.totalRows = this.items.length
    axios.get('/variables').then(response => {
        this.project=response.data[0]
        this.fields[0].label=this.project.content
        this.addressfild=response.data[1].content.split(' ').join('+')
        this.hideNumberOfYear = response.data[4].content
      })
      axios.get('/countries').then(response => {
        this.countries=response.data
      })
    setTimeout(() => {
       this.$socket.send('getProjects')
      this.$options.sockets.onmessage = (data) => (data.data=='getProjects') ? this.getProjects('011'): ''
    },1000);
  }
}
</script>
<style type="text/css">
.text-container {
    position: relative;
    display: block;
    max-width: 300px;
    height: calc(2em + -5px);
    overflow: hidden;
    white-space: normal;
}

.text-content {
  word-break: break-all;
  position: relative;
  display: block;
  max-height: 3em;
}
 



/*.block-1 {
height: calc(87vh - 7rem);overflow-y: auto;
}
.block-2 {
height: calc(87vh - 7rem);overflow-x: hidden;
}*/
/*@media only screen and (min-width : 768px) {
.b-table-sticky-header {
  overflow-y: auto;
  max-height: 100%
}

  .b-table-sticky-header > .table.b-table > thead > tr > th {
    position: sticky !important;
    background-color: #fff;
  }
}
@media only screen and (max-width : 767px) { 
.b-table-sticky-header {
  max-height: unset;
}
.sticky-header-lg{
  overflow-x:hidden;
}
}*/
</style>