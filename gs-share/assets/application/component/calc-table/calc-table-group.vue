<template>
   <div>
    <b-modal size="sm" centered id="ids" ref="ids" :title="$t('calcTableGroup.numberOfInvoice')" body-class="workerHeight" >
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" :checked="[selectedId]"  @change.native="selectedId=$event;"
            text-field="lastNumber" value-field="lastNumber" stacked :options="id_list" v-if="detectNewRound(id_list)" />

            <div v-else class="text-center">
            {{$t('calcTableGroup.newRange')}}

            <b-form-checkbox-group buttons  style="width:100%" :checked="[1]"
            @change.native="selectedId=$event"
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
                <b-col cols="1"><b-button size="sm" variant="outline-primary" @click="nameofparts.push({'nameofpart':null, 'folderInDocumentsCheck':false, 'folderInDocuments':null, 'folderInImagesCheck':false, 'folderInImages':null})">+</b-button></b-col>
              </b-row>
            </b-col>
          </b-container>

            <template slot="modal-footer">
               <b-button type="submit" variant="primary" data-toggle="addPart" @click="nameOfPart(nameofparts)">OK</b-button>
            </template>
         </b-modal>

      <b-modal size="md" centered id="addSub" ref="addSub" :title="$t('calcTableGroup.sub')">
        <b-form-group horizontal :label-cols="4" :label="$t('calcTableGroup.sub')+':'" style="padding: 5px;">

          <b-select label="name" v-model="numberforsub"  value-field="name" text-field="name" :options="customer_sub" />
           </b-form-group> 
          <template slot="modal-footer">
            <b-button type="submit" variant="primary"  @click="okcontractsub">OK</b-button>
          </template>
      </b-modal>
<hr>
<b-row align-h="between">
<b-col>
          <b-button size="sm" @click="(nameofparts=[{nameofpart:null, folderInDocumentsCheck:false, folderInDocuments:null, folderInImagesCheck:false, folderInImages:null}]);($refs['shpart'].show());">
              {{$t('calcTableGroup.addPart')}}
          </b-button>

          <b-dropdown  size="sm" :text="$t('projectDetail.plusRow')"  class="text-center maxHeight" v-show="selectedTables.length > 0">
            <b-dropdown-item-button :key="count_row" v-for="count_row in 10"
            @click="addRow(count_row)" >
            {{count_row}} {{$t('projectDetail.plusRow')}}
            </b-dropdown-item-button>
          </b-dropdown>

          <b-button  size="sm"  @click="getSubCustomers()"  v-if="(tmp.type=='Orders')">
              {{$t('calcTableGroup.addSub')}}
          </b-button>

          <b-button  size="sm" @click="worker" v-if="(tmp.type!='StandingOrder')">
            {{$t('calcTableGroup.workers')}}
          </b-button>

          <b-button  size="sm" @click="$emit('sendMail', availableMails)"
          v-if="(tmp.type=='StandingOrder')">
            {{$t('calcTableGroup.timetableInvoice')}}
          </b-button>

          <b-button size="sm" @click="exec(plan.id)" :variant="lastButton?'':detectExec(plan)"
          v-if="((plan!=null) && (plan.autosend==0))">
            {{$t('calcTableGroup.timetableExec')}}
          </b-button>

          <b-button size="sm"  @click="addInvoice('SInvoices')" v-if="(tmp.type=='SUB')" :disabled="addSInvoiceLoad">
            {{addSInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.subInvoice')}}
            <b-iconstack font-scale="1" v-if="addSInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>

          <b-button @click="addInvoice('Invoices')"  size="sm"  v-if="((tmp.type=='Orders') || (tmp.type=='StandingOrder'))" :disabled="addInvoiceLoad">
            {{addInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.toInovice')}}
            <b-iconstack font-scale="1" v-if="addInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>

          <b-button @click="addInvoice('removeInvoices')"  size="sm"  v-if="(tmp.type=='Invoices')&&(tmp.number.substr(0, 1)=='0')" :disabled="addInvoiceLoad" variant="danger">
            {{addInvoiceLoad?$t('calcTableGroup.toInoviceInProgress'):$t('calcTableGroup.removeInovice')}}
            <b-iconstack font-scale="1" v-if="addInvoiceLoad">
              <b-icon stacked icon="circle-fill" animation="throb" variant="primary"></b-icon>
            </b-iconstack>
          </b-button>
        </b-col>
        <b-col class="text-right">
        <b-dropdown  size="sm" :text="$t('oneCountAlret.'+tmp.type)"  class="text-center maxHeight" v-if="(tmp.type!='SUB'&&tmp.type!='Invoices')">
          <b-dropdown-item-button :key="opt" v-for="opt in getOpt()"
          @click="offerChangeType(tmp.id, opt)" >
            {{opt}} {{($t('oneCountAlret.'+tmp.type) == opt)?'('+$t('company.copy')+')':''}}
          </b-dropdown-item-button>
        </b-dropdown>

        <b-dropdown  size="sm" :text="detectOfWork()"  class="text-center maxHeight">
          <b-dropdown-item-button :key="index" v-for="(opt, index) in works"
          @click="updateItem(opt.value, 'work', tmp.id, tmp.work)" >
            {{opt.text}}
          </b-dropdown-item-button>
        </b-dropdown>

        <b-button size="sm" @click="$emit('openWindowPrint', tmp.type)">
          <b-icon icon="printer" aria-hidden="true"></b-icon>
        </b-button>

</b-col>
    </b-row><br />
<!-- value.length==0 -->


  <div class="text-center" v-show="rowsBusy">
    <strong v-if="rowsLoading" class="text-info">
        <b-spinner class="align-middle" ></b-spinner>
        {{$t('projects.loading')}}...
      </strong>
      <div v-else class="text-center">{{$t('projects.empty')}}</div>
    </div>


  <!-- <draggable :value="tables" @input="onItems" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="checkMove($event)"> -->
      
         <div v-for="table in tables" :key="table.id">
          
          <!-- <calc-table :nowTableId="tables" :value="table" :addtaxColapse="addtaxColapse" :tableId="table.id" :butDiscPerc="butDiscPerc" :unitType="unitType" :looks="looks"
            :color="color" :selectedWorkers="selectedWorkers"  :type="type" v-on:changeSum="discOfPercent()"  :discP="discP"> -->

            <calc-table
            :ref="'table'+table.id"
            :table="table"
            :unitPercent="((table.obj!='')&&(table.obj!=null))?table.obj.split(','):[]"
            :selectedWorkers="selectedWorkers"
            :butDiscPerc="tmp.butDiscPerc"
            :discP="tmp.discP"
            :addtaxColapse="tmp.addtaxColapse=='true'"
            :unitType="unitType"
            :item_id="tmp.id"
            @chengeCountPresents="chengeCountPresents"
            @seltable="seltable"
            @tableDelete="tableDelete">
            </calc-table>
            <hr style="padding:0;margin:5px;display:none;" :id="'hr'+table.id"/>
        </div>
      <!-- </draggable> -->

   </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
import axios from 'axios';
export default {
    components: {
        draggable,
    },
    props: ['tmp', 'workers', 'availableMails', 'plan', 'works', 'selectedWorkers', 'opt', 'pid'],
    data() {
        return {

            // head:null,
            // id:null,
            // type:null,
            // disc:null,
            // discP:null,
            // tax:null,
            // taxDub:null,
            // taxP:null,
            // taxPDub:null,
            // netto:null,
            // brutto:null,
            // butDiscPerc:null,
            // addtaxColapse:null,


            selectedTables:[],
            checked:false,
            tables:null,
            rowsBusy:true,
            rowsLoading:true,
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
    axios.get('/get_units').then(response => {
    this.unitType = response.data.sort();
    });
    this.getTablesInItem(this.tmp.id);
    this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')
      if (delimetr[0] == 'add_part') {
        if (delimetr[1] == this.tmp.id) this.getTablesInItem(this.tmp.id);
      }
      if ((delimetr[0] == 'update_part') || (delimetr[0] == 'table_delete' || delimetr[0] == 'checnge_count_percent')) {
        this.tables.filter((v)=>{
          if (v.id == delimetr[1]) {
            this.getTablesInItem(this.tmp.id)
          };
        })
      }
      if ((delimetr[0] == 'send_price') || (delimetr[0] == 'del_row')) {
        delimetr[1].split(',').forEach((tableForReload)=>{
          this.$refs['table'+tableForReload][0].getRowsInTable(tableForReload)
          this.selectedTables=[]
        })
      }
      if (delimetr[0] == 'updateFild') {
        var updateFild = (JSON.parse(data.data.split('updateFild:')[1]))
        this.$refs['table'+updateFild.table_id][0].getFild(updateFild)
      }

      if (delimetr[0] == 'update_part_parametrs') {
        var update_part_parametrs = (JSON.parse(data.data.split('update_part_parametrs:')[1]))
        this.$refs['table'+update_part_parametrs.table_id][0].update_part_parametrs(update_part_parametrs)
      }

    }




},
methods: {
  getTablesInItem(id) {
			axios.get('/get_tables_in_edit', {
				params: {
					id: id
				}
			}).then(response => {
        // console.log(response.data)
				this.tables = response.data;
        this.rowsLoading = false;
        this.rowsBusy = (response.data.length > 0) ? false : true;
			})
		},


	seltable(id, e) {
    // console.log(this.selectedTables)
      if (e){
        this.selectedTables.push(id)
      } else{
        this.selectedTables = this.selectedTables.filter( el => el !== id)
      }
      // console.log(this.selectedTables)
      this.$emit('seltable', this.selectedTables)
  },
  addRow(count_row){
    for (var i = 0; i <= (count_row-1); i++) {
      axios.get('/send_price', {
				params: {
					ids: [].join(),
					names: this.selectedTables.join()
				}
			})
		}
    this.selectedTables = []
    this.$emit('seltable', this.selectedTables)
  },
  chengeCountPresents(unitPercent, dir, row_id, table_id){
    axios.get('/checnge_count_percent', {
      params: {
        dir: dir,
        unitPercent:unitPercent.join(),
        row_id: row_id,
        table_id: table_id
        }
    })
    // console.log(id, dir, index)
  },

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
        //   selectedDocs(event){
        //   this.$emit('selectedDocs', event)
        // },
        // addPdf() {
        //   this.$emit('addPdf')
        // },
        // printPdf() {
        //   this.$emit('printPdf')
        // },
        // preview() {
        //   this.$emit('preview')
        // },
        // printOffer() {
        //   this.$emit('printOffer')
        // },
// hideWindowPrint(){
//   this.$emit('hideWindowPrint')
// },
// openWindowPrint(){
//   this.$emit('openWindowPrint')
// },
getSubCustomers(){
axios.get('/customer_sub').then(response => {
               this.customer_sub=response.data;
                this.$refs.addSub.show();
  })


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
                id: this.tmp.id,
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
                id: this.tmp.id,
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
                id: this.tmp.id,
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
                id: this.tmp.id,
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
          }
        },
        onItems($event){
          { this.$emit('input', $event) }
        },
        nameOfPart(nameofparts) {
            var tmpArrValue = []
            this.shpart = true,
            this.$refs.shpart.hide(),
            axios.get('/add_part', {
                          params: {
                              parts_names:  JSON.stringify(nameofparts), 
                              item_id: this.tmp.id,
                              pid:this.pid
                           }
                      })
        },
        tableDelete(id, item_id) {
            if (confirm(this.$t('alert.sure'))){
            axios.get('/table_delete', {
                params: {
                  id: id,
                  item_id
                }
            })
            }
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