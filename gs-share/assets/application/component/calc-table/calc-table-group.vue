<template>
   <div>
    <!-- <b-modal size="lg" centered id="reports" ref="reports" :title="$t('calcTableGroup.reports')" body-class="workerHeight">
      <b-table class="tableProject" striped hover :fields="fieldsTableD" :items="raports" @row-clicked="inItemGetData" />        
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="addInvoice('Damage Description')">{{$t('projectDetail.add')}}</button>
           </template>
        </b-modal> -->

<!--     <b-modal size="sm" centered id="worker" ref="worker" title="Select Workers" body-class="workerHeight">
        <b-form-input type="text" v-model="searchWorker"  style="margin-bottom: 4px !important;"/>
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="workers_list"/>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="selectedWorkers=[]">Clear</button>
           </template>
        </b-modal>  -->

    <b-modal size="sm" centered id="ids" ref="ids" :title="$t('calcTableGroup.numberOfInvoice')" body-class="workerHeight" >
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" :checked="[selectedId]"  @change.native="selectedId=$event;"
            text-field="lastNumber" value-field="lastNumber" stacked :options="id_list" v-if="detectNewRound(id_list)" />

            <div v-else class="text-center">
            {{$t('calcTableGroup.newRange')}}

            <b-form-checkbox-group buttons  style="width:100%" checked="[1]" @change.native="selectedId=$event"
             stacked :options="[1]" />
            </div>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="addInvoiceLoad=true;okInvoice(!detectNewRound(id_list))">OK</button>
           </template>
         
           
        </b-modal>

    <b-modal size="sm" centered id="ids_sub" ref="ids_sub" :title="$t('calcTableGroup.numberOfSUBInvoice')" body-class="workerHeight"  >

            <b-input @change.native="selectedId=$event" />
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="addSInvoiceLoad=true;okInvoiceSub();">OK</button>
           </template>
        </b-modal>
      <!-- <b-form @submit.prevent="nameOfPart(nameofpart)"> -->
         <b-modal size="md" centered ref="shpart" :title="$t('calcTableGroup.addPart')">
          <b-container>
            <b-col cols="12" v-for="(nameofpart, index) in nameofparts"  :key="nameofpart.id">
            <b-row align-v="center">
              <b-col cols="1" align-self="center">
                <b-checkbox plain checked="true" disabled></b-checkbox>
              </b-col>
              <b-col cols="4" align-self="center">
                {{$t('calcTableGroup.nameOfPart')}}
              </b-col>
              <b-col cols="7" align-self="center">
                <b-form-input :value="nameofpart.nameofpart" @input="nameofpart.folderInImages=nameofpart.folderInDocuments=nameofpart.nameofpart=$event" required :state="null" type="text" placeholder="Enter name of table" />
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col cols="1" align-self="center">
                <b-checkbox plain v-model="nameofpart.folderInDocumentsCheck" :id="'folderInDocuments-'+index"></b-checkbox>
              </b-col>
              <b-col cols="4" align-self="center">
                <label :for="'folderInDocuments-'+index">{{$t('calcTableGroup.folderInDocuments')}}</label>
              </b-col>
              <b-col cols="7" align-self="center">
                <b-form-input :disabled="!nameofpart.folderInDocumentsCheck" :value="nameofpart.folderInDocumentsCheck?nameofpart.folderInDocuments:''" @change="nameofpart.folderInDocuments=$event" required :state="null" type="text" placeholder="Enter name of folder in documents" />
              </b-col>
            </b-row>
            <b-row align-v="center">
              <b-col cols="1" align-self="center">
                <b-checkbox plain v-model="nameofpart.folderInImagesCheck" :id="'folderInImages-'+index"></b-checkbox>
              </b-col>
              <b-col cols="4" align-self="center">
                <label :for="'folderInImages-'+index">{{$t('calcTableGroup.folderInImages')}}</label>
              </b-col>
              <b-col cols="7" align-self="center">
                <b-form-input :disabled="!nameofpart.folderInImagesCheck" :value="nameofpart.folderInImagesCheck?nameofpart.folderInImages:''" @change="nameofpart.folderInImages=$event" required :state="null" type="text" placeholder="Enter name of folder in images" />
              </b-col>
            </b-row>
            <b-row align-h="between" class="pt-2">
              <b-col cols="1"><b-button size="sm" :disabled="(nameofparts.length==1)" variant="danger" @click="nameofparts.splice((index), 1)">-</b-button></b-col>
              <b-col cols="1"><b-button size="sm" variant="outline-primary" @click="nameofparts.push({'nameofpart':null, 'folderInDocumentsCheck':true, 'folderInDocuments':null, 'folderInImagesCheck':true, 'folderInImages':null})">+</b-button></b-col>
            </b-row>
            </b-col>

          </b-container>

            <template slot="modal-footer">
               <b-button type="submit" variant="primary" data-toggle="addPart" @click="nameOfPart(nameofparts)">OK</b-button>
            </template>
         </b-modal>
      <!-- </b-form> -->
      <b-modal size="md" centered id="addSub" ref="addSub" :title="$t('calcTableGroup.sub')">
        <b-form-group horizontal :label-cols="4" :label="$t('calcTableGroup.sub')+':'" style="padding: 5px;">
          <!-- <b-form-input class="cForm-input" v-model="numberforsub"
              type="text" placeholder="Enter name for SUB:" />
          </b-form-group> -->
          <b-select label="name" v-model="numberforsub"  value-field="name" text-field="name" :options="customer_sub" />
           </b-form-group> 
          <template slot="modal-footer">
            <b-button type="submit" variant="primary"  @click="okcontractsub">OK</b-button>
          </template>
      </b-modal>

      <print v-if="tmp.typeOfHead != 'Devices' & tmp.typeOfHead != 'Damage' & tmp.typeOfHead != 'Reports'" 
      :windowPrint="windowPrint"
      :selectedCornty="selectedCornty"
      :project="project" :tmp="tmp"

      :account="account" :id="pid"
      :disc='disc' :discP='discP'
      :tax='tax' :taxDub='taxDub'
      :taxP='taxP' :taxPDub='taxPDub'
      :netto='netto' :brutto='brutto'
      :butDiscPerc='butDiscPerc'
      :partx='value' :head="tmp.typeOfHead"
      :addtaxColapsel="addtaxColapse"
      :workers="workers" :comments="comments"
      :customer="customer"
      :person="person"
      :selectCustomer="selectCustomer"
      :selectPerson="selectPerson"
  
      :selectedDocsList="selectedDocsList"
      :addPdfs="addPdfs"
      :makemodalpdf="makemodalpdf"
      :typeDocsList="typeDocsList"

      @selectedDocs="selectedDocs"
      @addPdf="addPdf"
      @printPdf="printPdf"
      @preview="preview"
      @printOffer="printOffer"
      @hideWindowPrint="hideWindowPrint"
      ref="print"
      >

        <!--             <b-button class="customButton" @click="move">
                       Move
                    </b-button> -->
          <b-col>
          <b-button size="sm" @click="(nameofparts=[{nameofpart:null, folderInDocumentsCheck:true, folderInDocuments:null, folderInImagesCheck:true, folderInImages:null}]);($refs['shpart'].show());">
              {{$t('calcTableGroup.addPart')}}
          </b-button>
          <b-button  size="sm"  @click="getSubCustomers()"  v-if="(type=='Orders')">
              {{$t('calcTableGroup.addSub')}}
          </b-button>
<!--           <b-button  class="customButton col-12 col-lg-1" @click="addInvoice('Damage Description')"  style="min-width:55px;" v-if="(type=='Orders')"> 
              To Damage
          </b-button> -->
<!--           <b-button  size="sm"  @click="reports" >
              {{$t('calcTableGroup.reports')}}
          </b-button> -->
          <b-button  size="sm" @click="worker" v-if="(type!='StandingOrder')">
            {{$t('calcTableGroup.workers')}}
          </b-button>

          <b-button  size="sm" @click="$emit('sendMail', availableMails)"
          v-if="(type=='StandingOrder')">
            {{$t('calcTableGroup.timetableInvoice')}}
          </b-button>

          <b-button size="sm" @click="exec(plan.id)" :variant="lastButton?'':detectExec(plan)"
          v-if="((plan!=null) && (plan.autosend==0))">
            {{$t('calcTableGroup.timetableExec')}}
          </b-button>


          <b-button size="sm"  @click="addInvoice('SInvoices')" v-if="(type=='SUB')" :disabled="addSInvoiceLoad">
            {{addSInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.subInvoice')}}
            <b-iconstack font-scale="1" v-if="addSInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>

          <b-button @click="addInvoice('Invoices')"  size="sm"  v-if="((type=='Orders') || (type=='StandingOrder'))" :disabled="addInvoiceLoad">
            {{addInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.toInovice')}}
            <b-iconstack font-scale="1" v-if="addInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>
          <b-button @click="addInvoice('removeInvoices')"  size="sm"  v-if="(type=='Invoices')" :disabled="addInvoiceLoad" variant="danger">
            {{addInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.removeInovice')}}
            <b-iconstack font-scale="1" v-if="addInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>
          </b-col>
<!--           <label v-if="(type!='SUB'&&type!='Invoices')">{{$t('calcTableGroup.type')}}:&nbsp;&nbsp;</label>
          <b-select v-if="(type!='SUB'&&type!='Invoices')" :value="$t('oneCountAlret.'+type)" @change="offerChangeType(id, $event)"
          :options="getOpt()"  size="sm" />&nbsp;&nbsp;&nbsp; -->
          
          <!-- <label>{{$t('calcTableGroup.work')}}:&nbsp;&nbsp;</label> -->
          <!-- <b-select :value="tmp.work" :options="works" @change="updateItem($event, 'work', tmp.id)"  size="sm"/> -->
        <b-col cols="12" lg="2">
        <b-select v-if="(type!='SUB'&&type!='Invoices')" :value="$t('oneCountAlret.'+type)" size="sm"
        @change="offerChangeType(id, $event)" :options="getOpt()" />
      </b-col>
      <b-col cols="12" lg="2">
        <b-select :value="detectOfWork()"
        :options="works" size="sm" @change="updateItem($event, 'work', tmp.id)" />
      </b-col>

<!-- this.$t('calcTableGroup.work') -->
</print>
<!-- value.length==0 -->


  <div class="text-center" v-show="rowsBusy">
    <strong v-if="rowsLoading" class="text-info">
        <b-spinner class="align-middle" ></b-spinner>
        {{$t('projects.loading')}}...
      </strong>
      <div v-else class="text-center">{{$t('projects.empty')}}</div>
    </div>


  <draggable :value="value" @input="onItems" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="checkMove($event)">
         <div v-for="(part, index) in value" :key="part.id">
          <calc-table :nowTableId="value" :value="sort(value[index])" :addtaxColapse="addtaxColapse" :tableId="index" :butDiscPerc="butDiscPerc" :unitType="unitType" :looks="looks"
            :color="color" :selectedWorkers="selectedWorkers" :toggle="value[index].parts.toggle" :type="type" :funcStop="funcStop"  v-on:changeSum="discOfPercent()"  :discP="discP">
            <!-- :class="{ 'table-dark' : value[index].parts.toggle,' handleTitle':type!='Invoices'}"    -->
            <b-checkbox plain name="partx" slot-scope="table" class="withoutbox"
                :class="{' handleTitle':type!='Invoices'}"
                v-model="value[index].parts.toggle" slot="tableHead" @change="$emit('seltable')"> 

                    <b-link style="width:100%" @click="toog(value[index].parts.id)">
                     <span :id="'p'+value[index].parts.id" style="display:none;vertical-align: middle;padding-right: 3px;" >

                      <b-icon icon="arrow-down" font-scale="1"></b-icon>

 {{total(value[index].parts.part_content) | thousandSeparator }} € </span>
                     <span :id="'m'+value[index].parts.id" style="vertical-align: middle;">

                      <b-icon icon="arrow-up" font-scale="1"></b-icon>
                    
                    </span>
                    </b-link>
                    <span class="forFinger">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>

                    <!-- <b-icon icon="circle-fill" aria-hidden="true"></b-icon> -->
                    <b-icon :icon="(value[index].parts.toggle)?'chat-square-text-fill':'chat-square-text'" font-scale="1.5" aria-hidden="true" :variant="(value[index].parts.toggle)?'success':''"></b-icon>
                    
                    <span class="forFinger">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span>
                    <!-- <i class="fas fa-dot-circle" style="font-size:12px"></i>  -->
                    <span :contenteditable="type!='Invoices'" class="diveditable" @blur="toModel($event, value[index].parts.id, value[index].parts.part_name)" @click.prevent.self>
                        {{value[index].parts.part_name}}
                    </span>
                       <!-- <span v-for="file in responseFiles" v-if="file.id==value[index].parts.id"> -->
                         
                        <!-- <span v-viewer :class="'im'+value[index].parts.id" style="display:none">
                        <template v-for="image in file.gallery">
                              <img :src="image" class="image" :key="image" height="200px">
                        </template>
                        </span>  -->
                        <!-- <b-link class="butMore" style="padding-left:0px;" @click="showImages('im'+value[index].parts.id)">Images</b-link>  -->
                      <!-- </span> -->
                      
                      <b-icon icon="trash" aria-hidden="true"  @click="partDel(value[index].parts.id)"></b-icon>
                     
                    <!-- <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(value[index].parts.id)"/> -->
                </b-checkbox>
            </calc-table>
            <hr style="padding:0;margin:5px;display:none;" :id="'hr'+value[index].parts.id"/>
        </div>
      </draggable>

   </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
import axios from 'axios';
export default {
    components: {
        draggable,
    },
    props: ['value', 'tmp', 'addtaxColapse', 'workers', 'toggle', 'responseFiles', 'type', 'id', 'funcStop', 'opt', 'butDiscPerc', 'looks', 'availableMails', 'plan',
    'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList','selectedCornty', 'project',  'account', 'pid', 'person', 'customer', 'selectCustomer', 'selectPerson', 'windowPrint',
    'disc', 'discP', 'tax', 'taxDub', 'taxP', 'taxPDub', 'netto', 'brutto', 'comments', 'loadDamages', 'works', 'selectedWorkers', 'rowsBusy', 'rowsLoading', 'wwidth'],
    data() {
        return {
            lastButton: false,
            addInvoiceLoad:false,
            addSInvoiceLoad:false,
            customer_sub:[],
            raports:[],
            counter: -1,
            moveToCopyRadio: 'Move',
            moveToCopy: [],
            tmpArr: [],
            color: [],
            oldColor: [],
            nameofparts:null,
            // nameofpart: null,
            // folderInDocuments:null,
            // folderInImages:null,
            shpart: null,
            oldPartx: [],
            // selectedWorkers: [],
            searchWorker:'',
            selectedId: null,
            id_list:[],
            unitType: [],
            numberforsub: null,
            fieldsTableD: {
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

                // other: {
                //     label: 'Other',
                //     sortable: true
                // },
               
               

                 status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },

              
            },
        }
    },
computed: {

    total: function() {
        var vm = this;
            return function(value) {
                var summa = 0
                value.forEach(function(val) {
                    if (val.status == 'yes') {
                        summa += val.count * val.price
                    }
                })
                return summa; //количество разрядов
            };
        },

  },
mounted(){
this.head = this.tmp.typeOfHead
this.id = this.tmp.id
this.type = this.tmp.type
  setTimeout(() => {
    axios.get('/get_units').then(response => {
    this.unitType = response.data.sort();
    });
  },1000);



},
methods: {
exec(id){
  if (confirm(this.$t('alert.sure'))){
    axios.get('/plan_exec', {
      params: {
        id: id
      }
    });
    this.lastButton = true;
  }
},
detectExec(val){
  var now = new Date()
  var endOfMonth = false
  if (val.period=='mstart'){
    val.period = 1
  }
  if (val.period=='mmidle'){
    val.period = Math.floor((new Date(now.getFullYear(), (now.getMonth()+1), 0).getDate()) / 2)
  }
  if (val.period=='mend'){
    endOfMonth = true
    val.period = new Date(now.getFullYear(), (now.getMonth()+1), 0).getDate()
  }
  var period = new Date(now.getFullYear()+'-'+(now.getMonth()+1)+'-'+val.period)
  if(val.pushToWorkDays==1){
    var weekDay = [7, 1, 2, 3, 4, 5, 6][period.getDay()]
    if (weekDay>5){
      if(endOfMonth){
        val.period = val.period-(weekDay-5)
      }
      else {
        val.period = val.period+(8-weekDay)
      }
    }
  }

  var lastsend = this.$options.filters.dateInverse(val.lastsend).split(' ')[0].split('.')
  var last = new Date(lastsend[2]+'-'+lastsend[1]+'-'+lastsend[0])

  if (period < now){
    if(last < period){
      return ('danger')
    }
  }         
},
detectOfWork(){
  if(this.tmp.work=='{"isTrusted":true}'){
    return this.$t('calcTableGroup.work');
  } else{
    return this.tmp.work;
  }
},
toog(val){
  document.getElementById('m'+val).style.display = document.getElementById('partx'+val).style.display = (document.getElementById('partx'+val).style.display=='none') ? '' : 'none'
  document.getElementById('p'+val).style.display = (document.getElementById('m'+val).style.display=='none') ? '' : 'none'
  document.getElementById('hr'+val).style.display = (document.getElementById('m'+val).style.display=='none') ? '' : 'none'

},

detectNewRound(id_list){
var year = 2020
var nowYear = (new Date().getFullYear())
if (id_list[id_list.length-1]){
  var lastItemOfList = id_list[id_list.length-1]

  if (lastItemOfList.lastDate != null) {
    year = (lastItemOfList.lastDate.date.split('-')[0])
  }
}
return (year == nowYear)
},
          selectedDocs(event){
          this.$emit('selectedDocs', event)
        },
        addPdf() {
          this.$emit('addPdf')
        },
        printPdf() {
          this.$emit('printPdf')
        },
        preview() {
          this.$emit('preview')
        },
        printOffer() {
          this.$emit('printOffer')
        },
hideWindowPrint(){
  this.$emit('hideWindowPrint')
},
openWindowPrint(){
  this.$emit('openWindowPrint')
},
getSubCustomers(){
axios.get('/customer_sub').then(response => {
               this.customer_sub=response.data;
                this.$refs.addSub.show();


                 
               // this.items1= response.data
               // this.itemsFilter((this.show!='Show')?0:1)
  })


},

    updateItem(val, type, id){
      // alert()
      // if (this.updatePojectFunc==0){
        axios.post('/update_item_from_project', {
              
                   val: val,
                   type: type,
                   id: id
                 
        }).then(response => {
          // this.updatePojectFunc=1
        })
      // }
    },

      sort(val){
        return val
      },
    discOfPercent(){
      this.$emit('changeSum'); 
    },
    checkMove(event){
      axios.get('/update_id_table', {
                      params: {
                        newIndex: event.newIndex,
                        oldIndex: event.oldIndex,
                        id: this.tmp.id
                      }
                  })
    },

inItemGetData(item, index) {
  this.tmp.typeOfHead = 'Damage Description',
  this.tmp.number = item.number,
  this.tmp.date = item.date,
  this.tmp.place = item.place,
  this.tmp.insurance = item.insurance_number,
  this.tmp.work = item.work,
  this.tmp.other = item.other,
  this.tmp.type='Damage Description',
  this.tmp.id=item.id,
  this.tmp.dateEvent = item.dateEvent,
  this.tmp.dateInspect = item.dateInspect,
  this.tmp.worker = item.ExamWorker,
  this.partx=[],
 
 this.$socket.send('getProjectDetail')
},



      reports(){
      axios.get('/get_reports', {
        params: {
          id: this.id
        }
      }).then(response => {
        this.raports = response.data
      })
        this.$refs.reports.show()
      },
      getOpt(){
       var opts = []
       this.opt.forEach((v)=>{
          if (v.type!='Damage Description')if(v.type!='Invoices')if(v.type!='SUB')if(v.type!='Sub Invoices'){opts.push(this.$t('oneCountAlret.'+v.type))}
        })
       return opts
      },
        addInvoice(val){
        if(val=="Invoices" || val=="SInvoices"  || val=="removeInvoices"){
        if(val=='SInvoices'){
          this.$refs.ids_sub.show();
        }else{
          axios.get('/detect_invoice').then(response => {
            // console.log(response.data)
            this.id_list = response.data,
            this.selectedId = response.data[(response.data.length-1)].lastNumber,
            this.$refs.ids.show()
          });
        }}

        if(val=="Damage Description"){
        // console.log(this.color)
        axios.get('/add_invoice', {
            params: {
                id: this.id,
                type: val,
                number:this.color.join(),
                labelForDelete:''

            }
            })

        }

 
        },
        okInvoice(newRange){
        this.$refs.ids.hide(),
        axios.get('/add_invoice', {
            params: {
                id: this.id,
                type: (this.tmp.type!="Invoices")?'Invoices':'removeInvoices',
                number: ((typeof(this.selectedId)=='object')?this.selectedId.target.value:this.selectedId),
                newRange: newRange,
                labelForDelete:this.$t('oneCountAlret.labelForDelete')
            }
            }).then(response => {
              this.addInvoiceLoad = false
            })

        
        },
        okInvoiceSub(){
        this.$refs.ids_sub.hide(),
        axios.get('/add_invoice_sub', {
            params: {
                id: this.id,
                type: 'Sub Invoices',
                number: ((typeof(this.selectedId)=='object')?this.selectedId.target.value:this.selectedId).split(' ').join('_'),
                newRange: false,
                labelForDelete:''
            }
            }).then(response => {
              this.addSInvoiceLoad = false
            })
        },
        okcontractsub(){
        this.$refs.addSub.hide(),
       axios.get('/add_invoice', {
            params: {
                id: this.id,
                type: 'SUB',
                number: this.numberforsub.split(' ').join('_'),
                newRange: false,
                labelForDelete:''
            }
            })
        },
        offerChangeType(id, type){
          if (confirm(this.$t('alert.sure'))){
            if (type==this.$t('oneCountAlret.Offers')) {type = 'Offers'}
            if (type==this.$t('oneCountAlret.Orders')) {type = 'Orders'}
            if (type==this.$t('oneCountAlret.StandingOrder')) {type = 'StandingOrder'}
              axios.get('/change_type', {
                params: {
                    id: id,
                    type: type
                }
            })
          // this.type = type
          }
        },
        // showImages(classId){
        //   const viewer = this.$el.querySelector('.'+classId).$viewer
        //   viewer.show()
        // },
        toModel(newVal, id, partName) {
            // partName = newVal.target.innerText
            if(newVal.target.innerText != partName){
                axios.get('/update_part', {
                  params: {
                    part_name: newVal.target.innerText.replace(/[\s]{2,}/, ''),
                    id: id
                  }
                })
            }
        }, 
        onItems($event){
          { this.$emit('input', $event) }
        },
        nameOfPart(nameofparts) {
            var tmpArrValue = []
            this.shpart = true,
            this.$refs.shpart.hide(),
            // tmpArrValue.push({
            //          parts: {
            //              checkbox_list: {
            //                  flavours: {},
            //                  selected: {},
            //                  allSelected: {},
            //                  indeterminate: {}
            //              },
            //              part_content: []
            //          }
            //      })

             axios.get('/add_part', {
                          params: {
                              parts_names:  JSON.stringify(nameofparts), 
                              item_id: this.id,
                              pid:this.pid
                           }
                      })
            // this.$emit('input', tmpArrValue.concat(this.value))
        },
        okMoveToCopy() {
            this.$refs.move.hide()
        },
        move() {
            if (this.color.length != 0) {
                this.counter = -1
                this.moveToCopy = []
                this.oldPartx = []
                this.$refs.move.show()
            } else {
                alert('no selected rows')
            }
        },
        moveToCopySelect(event, radio) {
            var nowPartx = JSON.parse(JSON.stringify(this.value))
            var tmpArr = this.tmpArr = []
            this.oldColor.push(JSON.parse(JSON.stringify(this.color)))
            this.oldPartx.push(JSON.parse(JSON.stringify(this.value)))
            var tmpArrCp = JSON.parse(JSON.stringify(this.value))
            var newColor = []
            this.color.forEach((clolorRow) => {
                var partIndex = clolorRow.split('-')
                nowPartx.forEach(function(part, index) {
                    var temRow = ''
                    var other = ''
                    if (part.parts.part_name == partIndex[0]) {
                        temRow = part.parts.part_content[partIndex[1]]
                        other = tmpArrCp[index].parts.part_content[partIndex[1]]
                        tmpArr.splice(0, 0, other)
                        if (radio == 'Move') {
                            part.parts.part_content.splice(temRow, 1)
                        }
                    }
                })
            })

            event.forEach((eve)=> {
                nowPartx.forEach((part)=>{
                    if (part.parts.part_name == eve) {
                        this.tmpArr.forEach(function(val, index) {
                            newColor.push(part.parts.part_name + '-' + index)
                            part.parts.part_content.unshift(val)
                        })
                    }
                })
            })
            this.color = []
            this.color = newColor.slice()
            this.counter = this.counter + 1
            this.$emit('input', nowPartx)
        },
        partDel(part) {
            // console.log(del_id);
            if (confirm(this.$t('alert.sure'))){
            // var deltable=this.value.filter(function(val){return (val!=part)})
            // this.$emit('input', deltable)

            axios.get('/del_part', {
                params: {
                  id: part
                }
            })

            }

        },
        cancelPartx(indexButton) {
            var tmpArrValue = []
            this.color = []
            this.moveToCopy = []
            this.oldPartx[indexButton].forEach((val)=> {
                tmpArrValue.push(val)
            })
            this.$emit('input', tmpArrValue)
            this.color = JSON.parse(JSON.stringify(this.oldColor[indexButton]))
            this.counter = this.counter - 1
        },
        okMoveToCopy() {
            this.$refs.move.hide()
        },
        worker() {
          this.$emit('worker')
        },
        okWorker() {
            this.$refs.worker.hide()
        }

    }
}
</script>
<style type="text/css">
 
  .withoutbox input[type=checkbox] {
    display: none;
}
</style>