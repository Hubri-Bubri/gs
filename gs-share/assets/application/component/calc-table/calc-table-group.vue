<template>
   <div>
    <b-modal size="lg" centered id="reports" ref="reports" title="Reports" body-class="workerHeight">
      <b-table class="tableProject" striped hover :fields="fieldsTableD" :items="raports" @row-clicked="inItemGetData" />        
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="addInvoice('Damage Description')">Add</button>
           </template>
        </b-modal>

<!--     <b-modal size="sm" centered id="worker" ref="worker" title="Select Workers" body-class="workerHeight">
        <b-form-input type="text" v-model="searchWorker"  style="margin-bottom: 4px !important;"/>
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="workers_list"/>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="selectedWorkers=[]">Clear</button>
           </template>
        </b-modal>  -->

    <b-modal size="sm" centered id="ids" ref="ids" title="Number of Invoice" body-class="workerHeight" >
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" :checked="[selectedId]"  @change="selectedId=$event"
            text-field="lastNumber" value-field="lastNumber" stacked :options="id_list" v-if="detectNewRound(id_list)" />

            <div v-else class="text-center">
             There will be a new account range.

            <b-form-checkbox-group buttons  style="width:100%" checked="[1]" @change="selectedId=$event"
             stacked :options="[1]" />
            </div>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="okInvoice(!detectNewRound(id_list))">OK</button>
           </template>
         
           
        </b-modal>

    <b-modal size="sm" centered id="ids_sub" ref="ids_sub" title="Number Of SUB Invoice" body-class="workerHeight"  >

            <b-input @change="selectedId=$event" />
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="okInvoiceSub">OK</button>
           </template>
        </b-modal>
      <!-- <b-form @submit.prevent="nameOfPart(nameofpart)"> -->
         <b-modal size="md" centered id="addPart" ref="shpart" title="Add Part">
            <b-form-group horizontal :label-cols="4" label="Name of part:"
               label-for="nameofpart" style="padding: 5px;">
               <b-form-input v-model="nameofpart" required class="cForm-input" id="nameofpart"
                  :state="null" type="text" placeholder="Enter name of part" />
            </b-form-group>
            <template slot="modal-footer">
               <b-button type="submit" variant="primary" data-toggle="addPart" @click="nameOfPart(nameofpart)">OK</b-button>
            </template>
         </b-modal>
      <!-- </b-form> -->
      <b-modal size="md" centered id="addSub" ref="addSub" title="SUB">
        <b-form-group horizontal :label-cols="4" label="SUB:" style="padding: 5px;">
          <!-- <b-form-input class="cForm-input" v-model="numberforsub"
              type="text" placeholder="Enter name for SUB:" />
          </b-form-group> -->
          <b-select label="name" v-model="numberforsub"  value-field="name" text-field="name" :options="customer_sub" />
           </b-form-group> 
          <template slot="modal-footer">
            <b-button type="submit" variant="primary"  @click="okcontractsub">OK</b-button>
          </template>
      </b-modal>
      <b-modal size="sm" centered id="move" ref="move" title="Move">
         <b-form-select multiple class="" id="move" @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" :select-size="4">
            <option v-for="part in value">{{part.parts.part_name}}</option>
         </b-form-select>
         <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['Move', 'Copy']" />
         <template slot="modal-footer">
            <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button>
         </template>
      </b-modal>


      <print v-if="tmp.typeOfHead != 'Devices' & tmp.typeOfHead != 'Damage'"
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
          <b-button   v-b-modal.addPart size="sm" >
              Add Part
          </b-button>
          <b-button  size="sm"  @click="getSubCustomers()"  v-if="type=='Orders'">
              Add SUB
          </b-button>
<!--           <b-button  class="customButton col-12 col-lg-1" @click="addInvoice('Damage Description')"  style="min-width:55px;" v-if="(type=='Orders')"> 
              To Damage
          </b-button> -->
          <b-button  size="sm"  @click="reports" >
              Reports
          </b-button>
          <b-button  size="sm" @click="worker" >
            Workers
          </b-button>

          <b-button  size="sm"  @click="addInvoice('SInvoices')"  v-if="(type=='SUB')">
              SUB Invoice
          </b-button>

          <b-button @click="addInvoice('Invoices')"  size="sm"  v-if="(type=='Orders')">
              To Invoice
          </b-button>


    



    





            <b-form inline align-h="between" slot="Type">
              <label>Type:&nbsp;&nbsp;</label>
                <b-select  :value="type" @change="offerChangeType(id, $event)" :options="getOpt()"  size="sm" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
            <label>Work:&nbsp;&nbsp;</label>
                <b-select :value="tmp.work" :options="works" @change="updateItem($event, 'work', tmp.id)"  size="sm"/>
             
            </b-form>





</print>


  <div class="text-center text-info" v-show="value.length==0">
    <b-spinner class="align-middle" ></b-spinner>
    <strong>Loading...</strong>
  </div>


      <draggable :value="value" @input="onItems" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="checkMove($event)">
         <div v-for="(part, index) in value" :key="part.id">




          <calc-table :nowTableId="value" :value="sort(value[index])" :addtaxColapse="addtaxColapse" :tableId="index" :butDiscPerc="butDiscPerc" :unitType="unitType" :looks="looks"
            :color="color" :selectedWorkers="selectedWorkers" :toggle="value[index].parts.toggle" :type="type" :funcStop="funcStop"  v-on:changeSum="discOfPercent()"  >

               <b-checkbox plain name="partx" slot-scope="table" class="withoutbox"
                    :class="{ 'table-dark' : value[index].parts.toggle,' handleTitle':type!='Invoices'}"
                    v-model="value[index].parts.toggle" 
                    slot="tableHead"> 

                    <b-link v-b-toggle="'partx' + table.tableId" class="butMore" style="width:100%">
                     + {{total(value[index].parts.part_content) | thousandSeparator }} €
                    </b-link>

                    <i class="fas fa-dot-circle" style="font-size:12px"></i> 
                    <span :contenteditable="type!='Invoices'" @blur="toModel($event, value[index].parts.id, value[index].parts.part_name)" @click.prevent.self>
                        {{value[index].parts.part_name}}
                    </span>
                       <span v-for="file in responseFiles" v-if="file.id==value[index].parts.id">
                         
                        <span v-viewer :class="'im'+value[index].parts.id" style="display:none">
                        <template v-for="image in file.gallery">
                              <img :src="image" class="image" :key="image" height="200px">
                        </template>
                        </span> 
                        <b-link class="butMore" style="padding-left:0px;" @click="showImages('im'+value[index].parts.id)">Images</b-link> 
                      </span>
                      

                    <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(value[index].parts.id)"/>
                </b-checkbox>
            </calc-table>

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
    props: ['value', 'tmp', 'addtaxColapse', 'workers', 'toggle', 'responseFiles', 'type', 'id', 'funcStop', 'opt', 'butDiscPerc', 'looks',
    'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList','selectedCornty', 'project',  'account', 'pid', 'person', 'customer', 'selectCustomer', 'selectPerson', 'windowPrint',
    'disc', 'discP', 'tax', 'taxDub', 'taxP', 'taxPDub', 'netto', 'brutto', 'comments', 'loadDamages', 'works', 'selectedWorkers'],
    data() {
        return {
            customer_sub:[],
            raports:[],
            counter: -1,
            moveToCopyRadio: 'Move',
            moveToCopy: [],
            tmpArr: [],
            color: [],
            oldColor: [],
            nameofpart: null,
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
    workers_list() {
      return this.workers.filter(post => {
        return post.toLowerCase().includes(this.searchWorker.toLowerCase())
      })
    },
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
    this.unitType = response.data;
    })
  },1000);
},
methods: {
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
        axios.get('/update_item_from_project', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
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
          if (v.type!='Damage Description')if(v.type!='Invoices')if(v.type!='SUB')if(v.type!='Sub Invoices'){opts.push(v.type)}
        })
       return opts
      },
        addInvoice(val){
        if(val=="Invoices" || val=="SInvoices"){
        if(val=='SInvoices'){

          this.$refs.ids_sub.show();
        }else{

          axios.get('/detect_invoice').then(response => {
            console.log(response.data)
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
                number:this.color.join()

            }
            })

        }

 
        },
        okInvoice(newRange){
        this.$refs.ids.hide(),

        axios.get('/add_invoice', {
            params: {
                id: this.id,
                type: 'Invoices',
                number: this.selectedId,
                newRange: newRange
            }
            })
        },
        okInvoiceSub(){
        this.$refs.ids_sub.hide(),
        axios.get('/add_invoice_sub', {
            params: {
                id: this.id,
                type: 'Sub Invoices',
                number: this.selectedId.split(' ').join('_'),
                newRange: false
            }
            })
        },
        okcontractsub(){
        this.$refs.addSub.hide(),
       axios.get('/add_invoice', {
            params: {
                id: this.id,
                type: 'SUB',
                number: this.numberforsub.split(' ').join('_'),
                newRange: false
            }
            })
        },
        offerChangeType(id, type){
     if (confirm("Are you sure?")){
         axios.get((document.URL.split('/')[4]=='sub')?'/change_type_sub':'/change_type', {
            params: {
                id: id,
                type: type
            }
            })
        // this.type = type
    }
        },
        showImages(classId){
          const viewer = this.$el.querySelector('.'+classId).$viewer
          viewer.show()
        },
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
        nameOfPart(nameofpart) {
            var tmpArrValue = []
            this.shpart = true,
            this.$refs.shpart.hide(),
            tmpArrValue.push({
                     parts: {
                         checkbox_list: {
                             flavours: {},
                             selected: {},
                             allSelected: {},
                             indeterminate: {}
                         },
                         part_content: []
                     }
                 })


             axios.get((document.URL.split('/')[4]=='sub')?'/add_part_sub':'/add_part', {
                          params: {
                              part_name: nameofpart,
                              item_id: this.id
                           }
                      })
            this.$emit('input', tmpArrValue.concat(this.value))
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
            if (confirm("Are you sure?")){
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