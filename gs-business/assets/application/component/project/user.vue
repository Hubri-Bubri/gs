<template>
    <container>
        <container-header class="container-fluid">
        </container-header>
        <container-body class="container-fluid">
            <b-card-group deck>
                <b-card no-body class="gs-container">
                    <b-tabs card>

                        <b-tab title="Upload">
                            <container>
                                <b-button v-if="coonect?false:true" @click="coonect=true" >Show Images</b-button>
                                        <container-body  style="overflow-x: hidden;" v-if="coonect">
                              <b-row >
                                <b-col cols="12" md="6">
                                    Images group by:
                                </b-col>
                                    <b-col cols="12" md="6">
                                          <b-select  v-model="selectedDamageImages" :options="labelForFieldsImages()" @change="resetFilds()"  />
                                    </b-col>
                                  
                                  </b-row>
                                    <br/>

                                     <b-table v-viewer  :items="domage_images" :fields="fieldsImages" stacked="lg" hover
                                      class="tableProject outgroup" small v-if="selectedDamageImages=='Image'">
                                      <template slot="id" slot-scope="row">
                                        <b-col cols="12" class="text-center">
                                          <img :src="row.item.id" class="image" style="max-height:70px;max-width:70px" @click.stop="showx('outgroup')">
                                        </b-col>
                                      </template>
                                      <template slot="file_name" slot-scope="row">
                                            {{row.item.file_name}}
                                      </template>

                                      <template slot="group" slot-scope="row">
                                          {{opt_images[opt_images.findIndex(x => x.id == row.item.group)]?opt_images[opt_images.findIndex(x => x.id == row.item.group)].value:''}}
                                         
                                      </template>
                                        <template slot="date" slot-scope="data">
                                           {{data.item.date | dateInverse}}
                                        </template>
                                    </b-table>
                                    <div v-else  v-for="(item, i) in groupByFild(selectedDamageImages)">
                                    <b-link v-b-toggle="item.id+'-'+i" class="butMore">
                                      <span class="when-opened">- {{item.name}}</span>
                                      <span class="when-closed">+ {{item.name}}</span>
                                    </b-link> 
                                    <b-collapse :id="item.id+'-'+i">
                                      <b-table  v-viewer :items="item.table" :fields="fieldsImages" stacked="lg" hover  
                                      :class="'tableProject '+'im'+item.id+'-'+i" small >
                                        <template slot="id" slot-scope="row">
                                        <b-col cols="12" class="text-center">
                                          <img :src="row.item.id" class="image" style="max-height:100px;max-width:100px" @click.stop="showx('im'+item.id+'-'+i)">
                                        </b-col>
                                        </template>
                                      <template slot="file_name" slot-scope="row">
                                           {{row.item.file_name}}
                                      </template>
                                      <template slot="group" slot-scope="row">
                                         {{opt_images[opt_images.findIndex(x => x.id == row.item.group)]?opt_images[opt_images.findIndex(x => x.id == row.item.group)].value:''}}
                                      </template>
                                     
                                        <template slot="date" slot-scope="data">
                                           {{data.item.date | dateInverse}}
                                        </template>
                                      </b-table>
                                    </b-collapse>
                                    </div>
                            </container-body>
                            
                             
                            <b-row>
                               <b-col cols="12" md="6"> <b-select :options="workers" :value="user" disabled ></b-select> </b-col>
                               <b-col cols="12" md="6"> <b-select :options="opt_images" text-field="value" value-field="id" v-model="selected_table"></b-select> </b-col>
                            </b-row>
                                        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd">
                                        </vue-dropzone>
                        
                         
                            </container>
                        </b-tab>



                    </b-tabs>
                </b-card>
              
            </b-card-group>
        </container-body>
    </container>
</template>
<script type="text/javascript">
import io from 'socket.io-client';
import draggable from 'vuedraggable';
import axios from 'axios';
import moment from 'moment';
import { Multipane, MultipaneResizer } from 'vue-multipane';

import {
    VueEditor,
    Quill
} from 'vue2-editor';
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';

const items = [{
        isActive: true,
        age: 40,
        first_name: 'Dickerson',
        last_name: 'Macdonald'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    },
    {
        isActive: true,
        age: 38,
        first_name: 'Jami',
        last_name: 'Carney'
    }
];
const worksinside = [{
    checkbox: null,
    count: null,
    description_head: null,
    description_from_price: null,
    description_work: null,
    discount: null,
    position_number: null,
    price: null,
    status: null,
    summa: null,
    unit: null,
    without: null
}];


export default {
    components: {
        VueEditor,
        vueDropzone: vue2Dropzone,
        draggable,
        VueCtkDateTimePicker,
        Multipane,
        MultipaneResizer,
    },
    props: {
        id: String,
        user: String
    },
    data() {
        return {
          coonect:false,
          selected_table:0,
          opt_images:[],
          selectedDamageImages:'Image',
          domage_images:[],
          selectedLenght: 0,
          dateForInvoice:null,
          tmpForOffer: {
            name:{connect:null},
            first:{connect:null},
            second:{connect:null}
          },
          tmpForDamageDescription: {
            name:{connect:null},
            first:{connect:null},
            second:{connect:null}
          },
          tmpForOfferSharing: {
            name:{connect:null},
            first:{connect:null},
            second:{connect:null}
          },
          tmpForOfferAward: {
            name:{connect:null},
            first:{connect:null},
            second:{connect:null}
          },
          tempForModal:[],
          google: false,
          q:'baer-gs',
          generalCommentContet:null,
          generalComments:true,
          searchWorker:[],
          selectedWorkers:[],
          startTask:null,
          endTask:null,
          tasktime:'',
          taskName:null,
          task_table_id:null,
          newList:[],
          addhead:null,
          types_for_tables:[],
          items_table:[],
            funcStop:0,
            invoices: [],
            partx: [],
            customerTax:null,
            customerWeb:null,
            customerBic:null,
            customerIban:null,
            countMailCustomer:[''],
            countPhoneCustomer:[''],
            countFaxCustomer:[''],
            countOtherCustomer:null,
            answer:null,
            customerZip:null,
            customerCity:null,
            customerStreet:null,
            customerName:null,
            countNamePerson:[''],
            countMailPerson:[''],
            countPhonePerson:[''],
            countFaxPerson:[''],
            countOtherPerson:null,
            addFirm:null,
            addAppeal:null,
            addDep:null,
            addPos:null,

            updatePojectFunc:0,
            modalMail:[],
            modalFiles:[],
            ws:null,
            // tax: 0,
            // taxDub: 0,
            // taxP: 19,
            // taxPDub: 10,
            // disc: 0,
            // discP: 20,
            tax: 0,
            taxDub: 0,
            taxP: 0,
            taxPDub: 0,
            disc: 0,
            discP: 0,
            unit_type: ['Psch.', '%', 'Stück.', 'Sack.'],
            calc: ['yes', 'no', 'etc', 'alternative'],
            butDiscPerc: '%',
            netto: 0,
            brutto: 0,
            persentCounter: 0,
            damages:[],
            loadDamages:[],

            fieldsImages: [
                {   
                    key: 'id',
                    label: 'Image',
                    sortable: true,
                    thClass:''
                },
                {
                    key: 'file_name',
                    label: 'Name',
                    sortable: true,
                    thClass:''
                },
                {
                    key: 'date',
                    label: 'Date / Time',
                    sortable: true,
                    thClass:''
                },
                {
                    key: 'user',
                    label: 'User',
                    sortable: true,
                    thClass:''
                },
                {
                    key: 'group',
                    label: 'Table',
                    sortable: true,
                    thClass:''
                }
            ],



            dropzoneOptions: {
                url: '/loadFiles',
                thumbnailWidth: 50,
                parallelUploads: 10
            },

            sendToGroupForDamages: {
                url: '/load_img_in_group',
                thumbnailWidth: 50,
                parallelUploads: 10
            },

            docs: [],
            files: [],
            responseFiles: [],
            addPdfs: false,
            secondText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            firstText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            threText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            fourText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            fiveText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            sixText: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. \r\n Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            resp: null,
            viewPrint: true,
            today: (new Date().getFullYear() + '-' +
                    (((new Date().getFullYear() + '-' + (new Date().getMonth() + 1)).length == 6) ? '0' + (new Date().getMonth() + 1) : (new Date().getMonth() + 1))) +
                '-' +
                (((new Date().getFullYear() + '-' + (new Date().getDate())).length == 6) ? '0' + (new Date().getDate()) : (new Date().getDate())),
            customerContract: [],
            prices: true,
            comments: true,
            addtaxColapse: null,
            workers: [],

            items: items,
            worksinside: worksinside,

            fieldsInvoice: {

                inoice_number: {
                    label: 'Invoice',
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
                status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },
                show_details: {
                    key: 'show_details',
                    label: 'Contract'
                }
            },
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

                // other: {
                //     label: 'Other',
                //     sortable: true
                // },
               

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

                // delete: {
                //     // label: "&#128465;",
                //     // class: 'text-center'
                // }
            },

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

                // delete: {
                //     label: "&#128465;",
                //     class: 'text-center'
                // }
            },

            fieldsOffer: {
                offer_number: {
                    label: 'Offer Number',
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
                status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },
                // delete: {
                //     label: 'Delete',
                // }
            },

            fieldsDamages:{
                damage_number: {
                    label: 'Offer Number',
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
                }
                // status_set: {
                //     label: 'Status',
                //     sortable: true,
                //     class: 'status'
                // },
                // delete: {
                //     label: 'Delete',
                // }
            },
            options: [{
                    value: 'Open',
                    text: 'Open'
                },
                {
                    value: 'Done',
                    text: 'Done'
                }
            ],

            offers: [],

            project: {
                number: null,
                editor: null,
                date: null,
                street: null,
                city: null,
                zip: null,
                other:null
            },
            customer: null,
            person: null,
            personMail: null,
            personPhone: null,
            personFax: null,
            selectedNode: null,
            treeFilter: '',
            treeOptions: {
                multiple: false,
                filter: {
                    plainList: true
                }
            },
            show: false,
            tabs: [],
            tabCounter: 0,
            fieldsPrice: {
                position_number: {
                    label: 'Position Number',
                    sortable: true,
                },
                description_head: {
                    label: 'Description Head',
                    sortable: true
                },
                action: {
                    label: '<i class="fas fa-info" style="font-size:10px"></i>',
                    class: 'text-center'
                },
                count: {
                    label: '=',
                    sortable: true
                },
                unit: {
                    label: 'Unit',
                    sortable: true,
                },
                other: {
                    label: '&euro;',
                    sortable: true,
                    class: 'text-center'
                },
                summa: {
                    label: '&sum;',
                    sortable: true,
                },
                without: {
                    label: 'Without',
                    sortable: true,
                },
                // discount: {
                // label: 'Discount',
                // sortable: true,
                // },
                status: {
                    label: 'Status',
                    sortable: true,
                },
                checkbox: {
                    label: '%',
                    sortable: true,
                    class: 'text-center'
                }
            },
            add_offer: {
                work: null,
                insurance_number: null,
                place: null,
                comment: null
            },
            count_offer_number: 0,
            works: [{
                    value: 'painting',
                    text: 'Painting Works'
                },
                {
                    value: 'tiling',
                    text: 'Tiling Work'
                }
            ],


            tmp: {
                number: null,
                date: null,
                place: null,
                insurance: null,
                work: null,
                other: null,
                parts: null,
                typeOfHead:'Offer',
                dateEvent:null,
                dateInspect:null,
                worker:null
            },
            commentOfTable: '"At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."',
                        area: [],
        } //return
    }, //data

    sockets:{
    connect: function(){
      console.log('socket connected')
    },
    customEmit: function(val){
      console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
    }
  },

    methods: {
    showx(classId){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.show()
    },
 resetFilds(){
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].tdClass=''

    },
     groupByFild(fild){
        var tables = []
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == fild)].thClass='d-none'
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == fild)].tdClass='d-none'

        this.domage_images.forEach((v)=>{
            var date = v.date
            var user = v.user
            var file_name = v.file_name
            var id = v.id
            var group = v.group


          if (fild == 'date'){
            var nameOfDate = v.date.split(' ')[0]
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'group':group, 'file_name':file_name, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'file_name'){
            var nameOfDate = v.file_name
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'group':group, 'date':date, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'user'){
            var nameOfDate = v.user
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'group':group, 'file_name':file_name, 'date':date, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'group'){
            var nameOfDate = v.group
            if (this.opt_images[this.opt_images.findIndex(y => y.id == group)]){
              if (tables.findIndex(x => x.name == this.opt_images[this.opt_images.findIndex(y => y.id == group)].value) == -1){
                tables.push({'name':this.opt_images[this.opt_images.findIndex(y => y.id == group)].value, 'table':[{'id':id, 'user':user, 'file_name':file_name, 'date':date, '_rowVariant':''}]})
              }else{
                tables[tables.findIndex(x => x.name == this.opt_images[this.opt_images.findIndex(y => y.id == group)].value)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
              }
            }
          }




        })
        return tables
      },
      labelForFieldsImages(){
        var labelsArr = [];
        this.fieldsImages.forEach((v)=>{
          if(v.key=='id'){
            labelsArr.push('Image')
          }else{
            if(v.key!='delete'){
              labelsArr.push(v.key)
            }
          }

        })
        return labelsArr
      },
      getdomageImages(){
       axios.get('/domage_images', {
          params: {
            id: this.id,
            project: this.project.number
          }
        }).then(response => {

        this.domage_images = response.data.filter(function (v){
          if((v.file_name.split('.')[v.file_name.split('.').length-1]) != 'pdf'){ return v}
        })

        })
      },
      countWorker(val){
        if (val != null) {
          return '* '+val.split(',').length
        }
      },
      countDigitals(val){
        var nuls=3-val.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        val='0'+val
                    }
        return val
      },
      changeTmp(val, type){
        this.tempForModal.forEach((v)=>{
   
          if (type=='Offer'){
           if (v.name.content==val) {this.tmpForOffer = v}
          }
          if (type=='Sharing'){
            if (v.name.content==val) {this.tmpForOfferSharing = v}
          }
          if (type=='Award'){
            if (v.name.content==val) {this.tmpForOfferAward = v}
          }
          if (type=='DamageDescription'){
            if (v.name.content==val) {this.tmpForDamageDescription = v}
          }
        })
      },

    workersToTask(id, event){
      axios.get('/workers_task', {
        params: {
          workers: event?this.selectedWorkers.join():'Null',
          id: id
        }
      })
    },
    updateItem(val, type, id){
      if (this.updatePojectFunc==0){
        axios.get('/update_item_from_project', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        }).then(response => {
          this.updatePojectFunc=1
        })
      }
    },
    showCommetnts(){
      this.tmp.number= null,
      this.generalComments=true
      //
    },
    dataCharts(val){
    var brutto=val.brutto.replace('.', '')
    brutto=parseFloat(brutto.replace(',', '.'))

    var pay = this.summFromRow(val, brutto)*100/brutto
    var withOut =100-(this.summFromRow(val, brutto)*100/brutto)

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
    displaytime() {
    var self = this
    // var start = moment("21:00:17.000", "HH:mm:ss.SSS");
    this.tasktime = moment().format("YYYY-MM-DD HH:mm:ss");
    setTimeout(self.displaytime, 1000)
    },
    difTime(val, t){
    var start = moment(val, "YYYY-MM-DD HH:mm:ss.SSS");
  
    var diffrent = moment(this.tasktime,"YYYY-MM-DD HH:mm:ss")
    .diff(moment(start,"YYYY-MM-DD HH:mm:ss"), "seconds")

    var sec = diffrent;
    var h = sec/3600 ^ 0;
    var m = (sec-h*3600)/60 ^ 0;
    var s = sec-h*3600-m*60;

    if((t=='s') | (t=='l')){
    return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+((t=='l')?":"+(s<10?"0"+s:s):''))
    }
    if((t=='x')){
    return diffrent
    }
    },
    difTimeFinish(start, end, t){

    var diffrent = moment(end,"YYYY-MM-DD HH:mm:ss")
    .diff(moment(start,"YYYY-MM-DD HH:mm:ss"), "seconds")

    var sec = diffrent;
    var h = sec/3600 ^ 0;
    var m = (sec-h*3600)/60 ^ 0;
    var s = sec-h*3600-m*60;

    if((t=='s') | (t=='l')){
    return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+((t=='l')?":"+(s<10?"0"+s:s):''))
    }
    if((t=='x')){
    return diffrent
    }

    },
    summHour(tasks, t){
    var totallHours=0
    var totallHoursS=0
      tasks.forEach((v)=>{
        if(v.data_time_start!=null & v.data_time_end!=null){
          totallHours = totallHours + parseInt(this.difTimeFinish(v.data_time_start, v.data_time_end, 'x'))
          var temp = parseInt(this.difTimeFinish(v.data_time_start, v.data_time_end, 'x'))

          temp = temp*((v.workers==null)?1:v.workers.split.length)
          totallHoursS = totallHoursS + temp

        } else{
          totallHours = totallHours + parseInt(this.difTime(v.data_time_start, 'x'))
          var temp = parseInt(this.difTime(v.data_time_start, 'x'))

          temp = temp*((v.workers==null)?1:v.workers.split.length)
          totallHoursS = totallHoursS + temp
        }
      })
// console.log(totallHours, totallHoursS)
    var sec = (t=='(s)')?totallHoursS:totallHours;
    var h = sec/3600 ^ 0;
    var m = (sec-h*3600)/60 ^ 0;
    var s = sec-h*3600-m*60;

    if(t=='s'){
    return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    }
    if(t=='(s)'){
    return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    }
    if(t=='x'){
    return totallHours
    }
    if(t=='xs'){
    return totallHoursS
    }
   
    },
    allhours(val){
    var hours = 0
      this.loadDamages.forEach((v)=>{
        if (val == 'n'){
        var result = this.summHour(v.tasks, 'x')

        }
        if (val == '(s)'){
        var result = this.summHour(v.tasks, 'xs')

        }

        hours = hours + parseInt(result)
      
      })
    var sec = hours;
    var h = sec / 3600 ^ 0;
    var m = (sec - h * 3600) / 60 ^ 0;
    var s = sec - h * 3600 - m * 60;

    return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    },
    taskStop(id){
      axios.get('/task_time_damage', {
            params: {
                 id: id
               }
      })
    },
      // addImage(treeDamage){

      //   treeDamage.forEach((v)=>{
      //     v.images.forEach((i)=>{
      //       axios.get('/image_damage', {
      //         params: {
      //           id: i.id
      //         },
      //         responseType: 'arraybuffer'
      //       }).then(response => {
      //          i.imgData = Buffer.from(response.data, 'binary').toString('base64')
      //       })
      //     })
      //   })
      //   return treeDamage
      // },
      ShowContract(idContract){
        var contract = this.offers.filter((val)=>{
         // console.log(val.id, idContract)
          if(val.id==idContract) {
          return val
          }
        });
      return contract[0].offer_number;
      },
      getContracts(offers){

           return offers.filter((val)=>{ if(val.type!='offer') {
              var equalId=0
              this.invoices.forEach((v) =>{
                equalId=(v.offer_id==val.id)?equalId+1:equalId+0
              })
              if (equalId==0){

                return val
              }
          }  })
            
      },
      
      addSameModal(type){
        this.addhead=type,
        this.add_offer.comment=null,
        this.add_offer.place=null,
        this.add_offer.insurance_number=null,
        this.add_offer.work=null,
        this.$refs.addSame.show()
      },
      insertCustomer(val, type, person){
    
if (this.updatePojectFunc==0){
            if (val!=null && this.person[(type=='phone')?'tel':type].findIndex(x => x[type] == val)==-1 ){
            if (type!='customer' && type!='person'){
             
                  if (confirm("Are you sure want to add "+type+": "+val+" for "+this.person.label +" ?")) {
                           
                     axios.get('/add_contact', {
                         params: {
                             type: type,
                             val: val,
                             person: person,
                             sel: (this.person[(type=='phone')?'tel':type].length),
                             project: this.id
                          }
                     }).then(response => {
this.updatePojectFunc=1
        })
                  }
            }
}
}
        },
        newFirm(val){
            this.customerName=val,
            this.customerZip='',
            this.customerCity='',
            this.customerTax='',
            this.customerWeb='',
            this.customerBic='',
            this.customerIban='',
            this.countOtherCustomer='',
            this.countMailCustomer=[''],
            this.countPhoneCustomer=[''],
            this.countFaxCustomer=[''],
            this.$refs.customer.show()
        },
        newPerson(val){
            // this.updatePojectFunc=1
            this.countNamePerson=val.split(' '),
             this.countMailPerson=[''],
             this.countPhonePerson=[''],
             this.countFaxPerson=[''],
             this.countOtherPerson='',
             this.addFirm=this.customer,
             this.addAppeal=null,
             this.addDep=null,
             this.addPos=null,

            this.$refs.personModal.show()
        },
        newPersonSave(){
        this.updatePojectFunc=0
            if (this.addFirm!=null && this.countNamePerson[0].length>=1 && this.countNamePerson[1].length>=1){
             this.addAppeal=this.addAppeal?this.addAppeal:'',
             this.addDep=this.addDep?this.addDep:'',
             this.addPos=this.addPos?this.addPos:'',

            this.$refs.personModal.hide()
            axios.get('/add_person', {
                params: {
                    name: this.countNamePerson.join(),
                    mail: this.countMailPerson.join(),
                    phone: this.countPhonePerson.join(),
                    fax: this.countFaxPerson.join(),
                    other: this.countOtherPerson,
                    firm: this.addFirm.id,
                    appeal: this.addAppeal,
                    dep: this.addDep,
                    pos: this.addPos
                }
            })
            }
        },
        addTaskModal(id){
            this.taskName = null
            this.startTask = null
            this.endTask = null
            this.$refs.addTask.show()
            this.task_table_id = id          
        },
        newTaskSave(){
            axios.get('/add_task', {
                params: {
                    name: this.taskName?this.taskName:'New Task',
                    id: this.task_table_id,
                    start: this.startTask?this.startTask:'null',
                    end: this.endTask?this.endTask:'null'
                }
            })
          this.$refs.addTask.hide()
        },
        update_task(data, fild, id){
          axios.get('/update_task', {
                params: {
                    data: (data==null)?'null':data,
                    fild: fild,
                    id: id
                }
            })
        },
        newCustomerSave(){
        this.updatePojectFunc=0
            
    if (this.customerName!=''){
            this.$refs.customer.hide()
            axios.get('/add_customer', {

                params: {
                    name: this.customerName?this.customerName:'',
                    zip: this.customerZip?this.customerZip:'',
                    city: this.customerCity?this.customerCity:'',
                    street: this.customerStreet?this.customerStreet:'',
                    tax: this.customerTax?this.customerTax:'',
                    web: this.customerWeb?this.customerWeb:'',
                    bic: this.customerBic?this.customerBic:'',
                    iban: this.customerIban?this.customerIban:'',
                    other: this.countOtherCustomer?this.countOtherCustomer:'',
                    mail: this.countMailCustomer.join(),
                    phone: this.countPhoneCustomer.join(),
                    fax: this.countFaxCustomer.join()
                }
            }).then(response=>{
                this.newPerson('')

                this.addFirm={name: this.customerName, id: response.data.id}
            })
  }          
        },
        objToArrFPerson(val, type){
            if (val!=undefined){
                var arrForPerson=[]
                val.forEach((v)=>{
                    arrForPerson.push(v[type])
                })
                return arrForPerson
            }
        },
        sendMail(val){
            this.modalMail=[]
            val.forEach((val)=>{
            this.modalMail.push(val.mail)    
            })
            this.responseFiles.forEach((val)=>{
            this.modalFiles.push(val.name)    
            })
            
            
            this.$refs.mails.show()
        },
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
                      this.project.city = city,
                      this.updateProject('city', city)
                  }
                })
      this.updateProject('zip', val)
        },
    searchZipCustomer(val){
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
                      this.customerCity = city
                  }
                })
        },
             searchZipName(val){
             axios.get('https://maps.google.com/maps/api/geocode/json', {
                    params: {
                        components: "country:DE",
                        address: val,
                        sensor: "false",
                        language: "en",
                        key: "AIzaSyDKWZ-Jrk9KMoHYakuQfD6xQ4qUZ2XkGpo"
                    }
                }).then(response => {
                      if (JSON.parse(response.request.response).results[0]!=undefined){
                      var street = JSON.parse(response.request.response).results[0].formatted_address.split(',')[0] 
                      var city = JSON.parse(response.request.response).results[0].formatted_address.split(',')[1].split(' ')[2]
                      var zip = JSON.parse(response.request.response).results[0].formatted_address.split(',')[1].split(' ')[1]
                      this.customerZip = zip,
                      this.customerCity = city,
                      this.customerStreet = street
                      
                  }
                })
        },
        updateProjectAfter(){
            this.$options.sockets.onmessage = (data) => (data.data=='getProjectDetail') ? this.getProjectDetail(1): ''
        },
        updateProject(fild, newData){
        delete this.$options.sockets.onmessage;

        axios.get('/updateProject', {params: {
                id: this.id,
                date: newData,
                fild: fild
        }}).then(response => {

            this.updatePojectFunc=0

        })
        },
        updateProjectTaxs(){
          if (this.tmp.id!=null){
            axios.get('/updateProjectTaxs', {params: {
                            id: this.tmp.id,
                            butDiscPerc: this.butDiscPerc, 
                            tax: this.tax?this.tax:'0',
                            taxDub: this.taxDub?this.taxDub:'0',
                            taxP: this.taxP?this.taxP:'0',
                            taxPDub: this.taxPDub?this.taxPDub:'0',
                            disc: this.disc?this.disc:'0',
                            discP: this.discP?this.discP:'0',
                            addtaxColapse: (this.addtaxColapse==true)?'true':'false'
                    }})
          }
        },
        discOfPercent() {
           // console.log('1')
          this.tax=(this.tax=='NaN,00')?0:this.tax,
          this.taxDub=(this.taxDub=='NaN,00')?0:this.taxDub
          this.butDiscPerc=(this.butDiscPerc==undefined)?'%':this.butDiscPerc


            var tmpDisc, tmpNetto, tmpTax, tmpTax2
            var summa = 0
                this.partx.forEach(function(val) {
                    val.parts.part_content.forEach(function(val1) {
                        if (val1.status == 'yes') {
                            summa += val1.count * val1.price
                        }
                    })
                })
            if (this.butDiscPerc == '%') {
                var add = 0
                this.partx.forEach((val) => {
                    val.parts.part_content.forEach((sval) => {
                        if (sval.without == true) {
                            add = add + ((sval.count * sval.price / 100) * this.discP)
                        }
                    })
                })
                this.disc = this.$options.filters.thousandSeparator((summa / 100) * this.discP - add)
                tmpDisc = (summa / 100) * this.discP - add
            } else {
                this.disc = this.$options.filters.thousandSeparator(this.discP)
                tmpDisc = this.discP
            }

            this.netto = this.$options.filters.thousandSeparator(summa - tmpDisc)
            tmpNetto = summa - tmpDisc
            var addt = 0
            var addt2 = 0
            this.partx.forEach((val) => {
                val.parts.part_content.forEach((sval, index) => {
                    if (sval.status == 'yes') {
                        if (sval.alttax != true) {
                            addt = addt + (sval.count * sval.price)
                        } else {
                            addt2 = addt2 + (sval.count * sval.price)
                        }
                    }
                })
            })
            if (this.butDiscPerc == '%') {
              addt=addt-(addt/100)*(this.discP)
              addt2=addt2-(addt2/100)*(this.discP)
            }
            if (this.butDiscPerc == 'P') {
              addt=addt-(addt/100)*(this.discP*100/summa)
              addt2=addt2-(addt2/100)*(this.discP*100/summa)
            }
            this.tax = this.$options.filters.thousandSeparator(addt * (this.taxP / 100))
            tmpTax = (addt * (this.taxP / 100))
            this.taxDub = this.$options.filters.thousandSeparator(addt2 * (this.taxPDub / 100))
            tmpTax2=  (addt2*(this.taxPDub/100))
            //tmpTax2 = 0
            this.brutto = this.$options.filters.thousandSeparator(tmpNetto + tmpTax + tmpTax2)
        },
      docs2files() {
            var retArr = []
            var retArrs = []
            var withOutGroup = []
            var addgroup = []
            var files1
            var files = []
            var retArr = []
            var uniqueArray 
            var gallery 
                axios.get('/docs', {
                    params: {
                        id: this.id
                    }
                }).then(response => {
                    this.docs = (this.docs != response.data)?response.data:this.docs
                    axios.get('/files', {
                    params: {
                        id: this.project.number
                    }
                }).then(response => {
var rows1 = this.getItems('Offers').filter((v)=>{
    v.type = 'Offers'
    return v
})

var rows2 = this.getItems('Orders').filter((v)=>{
    v.type = 'Orders'
    return v
})

var rows3 = this.getItems('Invoices').filter((v)=>{
    v.type = 'Invoices'
    return v
})

// var rows4 = this.getItems('SUB').filter((v)=>{
//     v.type = 'SUB'
//     return v
// })
// var mergedArr = rows1.concat(rows2.concat(rows3.concat(rows4)))
var mergedArr = rows1.concat(rows2.concat(rows3))
this.files = (this.files != response.data)?response.data:this.files
var addFiles = []
mergedArr.forEach((item)=>{
axios.get('/get_tables', {
            params: {
              id: item.id
            }
        }).then(response => {
          var filesarr = response.data
          this.$delete(filesarr, filesarr.length-1)
                  files = this.files.filter(function(val) {
                  var ret
                  filesarr.forEach((v)=>{
                  ret = 1
                   if (val.name.split('.')[val.name.split('.').length-1] == 'pdf') {
                    if(v.parts!=undefined){
                      if (val.group.split(',').length>1){
                        ret = 0
                        var subval = []
                        val.group.split(',').forEach((valGroup)=>{
                          subval = JSON.parse(JSON.stringify(val))
                          subval.group = valGroup
                          if(subval.group==v.parts.id){
                            subval.group = v.parts.part_name + ' from ' + item.type
                            addFiles.push(subval)
                          }
                        })
                      } 
                      if(ret == 1) {
                        if(val.group==v.parts.id){
                          val.group = v.parts.part_name + ' from ' + item.type
                        }  
                      }
                      
                    }
                  }
                  })
                 if (ret == 1) {return val.name.split('.')[val.name.split('.').length-1] == 'pdf'}
                  })
                  addgroup = []
                  if(addFiles.length!=0) files = files.concat(addFiles)
                  files1 = files.filter((file, i) => {
                  
                  if (file.name.split('.')[file.name.split('.').length-1] != 'pdf') {
                    if (file.group) {
                        file.group.split(',').forEach((g) => {
                            addgroup.push(this.partx[g].parts.part_name)
                        })
                    }
                    if (addgroup.join(', ')) {
                        file.name = file.name + ': ' + addgroup.join(', ')
                    }
                  return file
                  }
                  })
          // filesarr.forEach((v, topIndex) => {
          // retArr = []

                // this.files.forEach(function(file) {

                //     if (file.name.split('.')[1] != 'pdf' && file.group != '') {
                //         file.group.split(',').forEach(function(ind, index) {
                //             if (v.parts.id == ind) {

                //                 retArr.push('/image?id=' + file.id)
                //             }


                //         })
                //     }
                //     if (file.name.split('.')[1] != 'pdf' && file.group == '') {
                //          // console.log('WG-'+file)  
                //         withOutGroup.push('/image?id=' + file.id)
                //     }
                // })



            //     if (retArr.length != 0) {retArrs.push({
            //         name: 'Images',
            //         id: v.parts.id, 
            //         group: v.parts.part_name +' from ' + item.type,
            //         gallery: retArr
            //     })
            //   }
            // })
            // uniqueArray = withOutGroup.filter(function(item, pos) {
            //     return withOutGroup.indexOf(item) == pos;
            // })
            // gallery = [{
            //     name: 'Images',
            //     group: 'General',
            //     gallery: uniqueArray
            // }]
            this.responseFiles = this.docs.concat(files)
                 })
        })
        })
              })
        },
        fsadd() {
                this.$refs.myVueDropzone.removeAllFiles()
        },
        sendingEvent(file, xhr, formData) {
            xhr.setRequestHeader('X-Number', this.project.number);
            xhr.setRequestHeader('X-Group', this.selected_table);
            xhr.setRequestHeader('X-User', this.workers[this.workers.findIndex(x => x.value == this.user)].text.replace(' ', '_').replace('ä', 'ae'));
        },
        sendingImageInGroupForDamages(file, xhr, formData) {
          var groups=[]
          this.loadDamages.forEach((v)=>{
            if(v.up==true){
              groups.push(v.id)
            }
          })
            xhr.setRequestHeader('group_id', groups.join());
        },
        addPdf() {
            this.addPdfs = true
            this.$refs.printOffer.hide()
            setTimeout(() => {
                this.$refs.preForm.submit()
                   

            }, 10);
        },
        updatePrew() {
            this.prices = true
            setTimeout(() => {
                if (this.viewPrint == false) {
                    this.$refs.preForm.submit()
                }
            }, 10);
        },
        htmlToPdf() {
            if (this.$refs.printPages != undefined) return this.$refs.printPages.innerHTML
        },
        preview() {
            this.viewPrint = this.viewPrint ? false : true,
                this.$refs.preForm.submit()
        },
        getDateFormat(val) {
          if (val!=null){
            var t = val.split('-')
            var y = t[0]
            var m = t[1]
            var d = t[2]
            return d + '.' + m + '.' + y
          }
        },
        getCustomer() {
            if (this.customer) return this.customer.name
        },
        getCustomerAdress() {

            if (this.customer) return this.customer.adress
        },
        getCustomerAdress1() {
            if (this.customer) return this.customer.adress1
        },
        getPerson() {
            if (this.person) return this.person.label
        },
        price() {
            this.prices = this.prices ? false : true,
                this.customerContract = []

            setTimeout(() => {
                if (this.viewPrint == false) {
                    this.$refs.preForm.submit()
                }
            }, 10);
        },
        // comment(){
        //     this.comments = this.comments ? false : true
        // },
        printOffer() {
            this.viewPrint = true
            this.$refs.printOffer.show()


    
            axios.get('/personals', {
                params: {
                    id: 119,
                    type: 'factory'
                }
            }).then(response => {
            

             var name
             var type
             var first
             var second
             this.tempForModal = []
                response.data[0].content.forEach((v, i)=>{
                  var index = ((i+1)%4==0)?4:(i+1)%4
                    if (index == 1){
                       name = v
                    }
                    if (index == 2){
                       type = v
                    }
                    if (index == 3){
                       first = v
                    }
                    if (index == 4){
                       second = v
                      this.tempForModal.push({name:name, type:type, first:first, second:second})
                    }
                 
                })
                    
              
                     }
                )

        },
        loadDocToFrame(index) {
            setTimeout(() => {
                if (this.$refs['ifrForm' + index].submit() != undefined) this.$refs['ifrDocForm' + index].submit()
            }, 10);
        },

        allSumms() {
            var allSumms = 'General: ' + this.$options.filters.thousandSeparator(this.alltotal(this.partx)) + ' ' +
                'I' +
                ' Alternative: ' + this.$options.filters.thousandSeparator(this.altalltotal(this.partx));
            return allSumms;
        },

        alltotal: function() {
            var summa = 0
            this.partx.forEach(function(val) {
                val.parts.part_content.forEach(function(val1) {
                    if (val1.status == 'yes') {
                        summa += val1.count * val1.price
                    }
                })
            })
            return summa;
        },
        altalltotal: function() {
            var summa = 0
            this.partx.forEach(function(val) {
                val.parts.part_content.forEach(function(val1) {
                    if (val1.status != 'yes') {
                        summa += val1.count * val1.price
                    }
                })
            })
            return summa;
        },
inItemClickCotract(val){

 var item = this.offers.filter(function(v){
    if(v.id==val){
      return v
    }
 })

this.inItemClick(item[0], 0)
}, 
        inItemClick(item, index) {

        this.tmp.typeOfHead = 'Offer',
        this.tmp.number = item.offer_number,
        this.tmp.date = item.date,
        this.tmp.place = item.place,
        this.tmp.insurance = item.insurance_number,
        this.tmp.work = item.work,
        this.tmp.other = item.other,
        this.tmp.type=item.type,
        this.tmp.id=item.id,
        axios.get('/table_data', {
            params: {
              id: item.id
            }
        }).then(response => {
            this.partx=[],
            response.data.forEach((val)=>{
            var addofnew=0
            this.partx.forEach((px)=>{
              if(px.parts.part_name==val.part_name){
                addofnew=1
              }
            })
            if(addofnew==0){
            this.partx.push(
                {
                        parts: {
                            part_name: val.part_name,
                            toggle: false,
                            checkbox_list: {
                                flavours: {},
                                selected: {},
                                allSelected:  {},
                                indeterminate: {}
                            },

                            part_content: [{
                                    upHere: false,
                                    сheckbox: 'true',
                                    count: val.count,
                                    description_head: val.description_head,
                                    description_work: val.description_work,
                                    description_from_price: val.description_from_price,
                                    discount: val.discount,
                                    position_number: val.position_number,
                                    price: val.price,
                                    status: val.status,
                                    alttax: val.alttax,
                                    summa: val.summa,
                                    unit: val.unit,
                                    without: val.without,
                                    done: val.done,
                                    id_row: val.id,
                                    item_id: val.item_id,
                                    part_name: val.part_name
                                }

                            ]
                        }
                  }
              
            )
          } else{
            var indexOfPart=(this.partx.findIndex(x => x.parts.part_name == val.part_name))
this.partx[indexOfPart].parts.part_content.push(
                             {
                                     upHere: false,
                                     сheckbox: 'true',
                                     count: val.count,
                                     description_head: val.description_head,
                                     description_work: val.description_work,
                                     description_from_price: val.description_from_price,
                                     discount: val.discount,
                                     position_number: val.position_number,
                                     price: val.price,
                                     status: val.status,
                                     alttax: val.alttax,
                                     summa: val.summa,
                                     unit: val.unit,
                                     without: val.without,
                                     done: val.done,
                                     id_row: val.id,
                                     item_id: val.item_id,
                                     part_name: val.part_name
                                 }

                             )
                         
                  }
              
            
          
        })
})
        // this.$socket.send('getFiles')
        // this.$options.sockets.onmessage = (data) => (data.data=='getFiles') ? this.docs2files(): ''
        },


        inItemClickInvoice(item, index) {
        this.tmp.typeOfHead = 'Invoice',
         //console.log(item),
        //this.tmp = item.parts,
        this.tmp.number = item.inoice_number,
        this.tmp.date = item.date,
        this.tmp.place = item.place,
        this.tmp.insurance = item.insurance_number,
        this.tmp.work = item.work,
        this.tmp.other = item.other,
        this.tmp.type='invoice',
        this.tmp.id=item.id

        axios.get('/invoice_data_table', {
            params: {
              id: item.id
            }
        }).then(response => {
             this.partx=[]
            response.data.forEach((val)=>{
            var addofnew=0
            this.partx.forEach((px)=>{
              if(px.parts.part_name==val.part_name){
                addofnew=1
              }
            })
            if(addofnew==0){
            this.partx.push({
                            parts: {
                            part_name: val.part_name,
                            toggle: false,
                            checkbox_list: {
                                flavours: {},
                                selected: {},
                                allSelected: {},
                                indeterminate: {}
                            },

                            part_content: [{
                                    upHere: false,
                                    сheckbox: 'true',
                                    count: val.count,
                                    description_head: val.description_head,
                                    description_work: val.description_work,
                                    description_from_price: val.description_from_price,
                                    discount: val.discount,
                                    position_number: val.position_number,
                                    price: val.price,
                                    status: val.status,
                                    alttax: val.alttax,
                                    summa: val.summa,
                                    unit: val.unit,
                                    without: val.without,
                                    done: val.done,
                                    id_row: val.id,
                                    item_id: val.item_id,
                                    part_name: val.part_name
                                }

                            ]
                        }
                }
            )
          } else{
            var indexOfPart=(this.partx.findIndex(x => x.parts.part_name == val.part_name))
this.partx[indexOfPart].parts.part_content.push(
                             {      
                                    upHere: false,
                                    сheckbox: 'true',
                                    count: val.count,
                                    description_head: val.description_head,
                                    description_work: val.description_work,
                                    description_from_price: val.description_from_price,
                                    discount: val.discount,
                                    position_number: val.position_number,
                                    price: val.price,
                                    status: val.status,
                                    alttax: val.alttax,
                                    summa: val.summa,
                                    unit: val.unit,
                                    without: val.without,
                                    done: val.done,
                                    id_row: val.id,
                                    item_id: val.item_id,
                                    part_name: val.part_name
                                 }

                             )
                         
                  }
        })
            // this.partx = get_data
            // get_data.filter(function(val){
            //     val.parts.part_content.forEach(function(v){
            //      // console.log(v.item_id)
            //     })
            // })
})
        
        // this.$socket.send('getFiles')
        // this.$options.sockets.onmessage = (data) => (data.data=='getFiles') ? this.docs2files(): ''
        },
        inItemClickPrice(item, index) {

            this.partx.forEach((valuePart, index)=> {
                if (valuePart.parts.toggle) {

                    for (var property in valuePart.parts.checkbox_list.flavours) {
                        valuePart.parts.checkbox_list.flavours[property].push('temp' + valuePart.parts.checkbox_list.flavours[property].length)
                    }
                    valuePart.parts.part_content.push({ //сheckbox:item.checkbox,
                        position_number: item.position_number,
                        description_head: item.description_head,
                        description_work: item.description_work,
                        description_from_price: item.description_from_price,
                        count: item.count,
                        discount: item.discount,
                        price: item.price,
                        status: item.status,
                        alttax: false,
                        summa: item.summa,
                        unit: item.unit,
                        without: item.without,
                        upHere: false,
                        toggle: false,
                        сheckbox: item.сheckbox
                    });

                      this.funcStop=1
                      axios.get('/add_part_form_price', {
                          params: {
                              part_name: valuePart.parts.part_name,
                              type: (this.tmp.type==undefined)?'invoice':this.tmp.type,
                              item_id: this.tmp.id,
                              position_number: item.position_number,
                              description_head: item.description_head,
                              description_work: item.description_work,
                              description_from_price: item.description_from_price,
                              count: item.count,
                              discount: item.discount,
                              price: item.price,
                              status: item.status,
                              alttax: false,
                              summa: item.summa,
                              unit: item.unit,
                              without: item.without
                           }
                      }).then(response =>{
                        this.funcStop=0
                      })
                }
            });


        },
inItemClickDamage(item, index) {

  this.tmp.typeOfHead = 'Damage',
  this.tmp.number = item.damage_number,
  // this.tmp.date = item.date,
  this.tmp.place = item.place,
  this.tmp.insurance = item.insurance_number,
  this.tmp.work = item.work,
  this.tmp.other = item.other,
  this.tmp.type='damage',
  // this.tmp.id=item.id,
  this.partx=[]
},

addGropuDamage(){
    axios.get('/add_group_damage', {
        params: {
          item_id: this.tmp.id
        }
    })
},
worker() {
          this.$refs.worker.show()
        },
damageToBase(fild, event, id){
       axios.get('/damage_update', {
        params: {
          fild: fild,
          event: event,
          id: id
        }
    })
},

        keyupMethod(event) {

            if (event.keyCode === 113) {
                this.tmouseOver()
            }
            if (event.keyCode === 27) {
                this.mouseOut()
            }
        },



        tmouseOver: function() {
            this.show = true;
        },
        mouseOut: function() {
            this.show = false;
        },
        newTab() {
            this.tabs.push(this.tabCounter++)
        },
        addOk() {
               axios.get('/add_same', {
                    params: {
                        add_number: this.project.number,
                        add_insurance_number: this.add_offer.insurance_number,
                        add_place: this.add_offer.place,
                        add_work: this.add_offer.work,
                        add_comment: this.add_offer.comment,
                        add_project_id: this.id,
                        type: this.addhead
                    }
                }).then(response => {
                    axios.get('/project_detail_new', {
                      params: {
                        id: this.id
                      }
                    }).then(response => {
                        this.items_table = response.data;
                    })
                }),
                this.$refs.addSame.hide()
        },

        offerDel(del_id) {

            if (confirm("Are you sure?")) {
                axios.get('/del_item', {
                    params: {
                        id: del_id
                    }
                }).then(response => {
                    this.offers = response.data
                })
            };

        },
        docDel(id, number) {
            if (confirm("Are you sure?")) {
                axios.get('/del_doc', {
                    params: {
                        id: id,
                        number: number
                    }
                }).then(response => {
                    this.docs = response.data
                })
            }
        },
        fileDel(id, number) {
            if (confirm("Are you sure?")) {
                axios.get('/del_file', {
                    params: {
                        id: id,
                        number: number
                    }
                }).then(response => {
                    //шаблон не реагирует на изминение files
                    this.files = response.data
                })
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
findRow(id, name){
var intId=parseInt(id.split(' ')[2])

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

inItemGetData(item, index) {
  if (item!=undefined) {
  this.generalComments=false,
  this.tmp.typeOfHead = item.type,
  this.tmp.number = item.number,
  this.tmp.date = item.date,
  this.tmp.place = item.place,
  this.tmp.insurance = item.insurance_number,
  this.tmp.work = item.work,
  this.tmp.other = item.other,
  this.tmp.type=item.type,
  this.tmp.id=item.id,
  this.tmp.dateEvent = item.dateEvent,
  this.tmp.dateInspect = item.dateInspect,
  this.tmp.worker = item.ExamWorker
  }
  

if(this.tmp.type!='Damage Description'){
axios.get('/get_tables', {
  params: {
    id: item.id
  }
}).then(response => {
  var tables = response.data.filter((v, i)=>{

    if (i<(response.data.length-1)){
      return v
    }
  });

     this.tax = response.data[(response.data.length-1)].taxs.tax;
     this.taxDub = response.data[(response.data.length-1)].taxs.taxDub;
     this.taxP = response.data[(response.data.length-1)].taxs.taxP;
     this.taxPDub = response.data[(response.data.length-1)].taxs.taxPDub;
     this.disc = response.data[(response.data.length-1)].taxs.disc;
     this.discP = response.data[(response.data.length-1)].taxs.discP;
     this.butDiscPerc = response.data[(response.data.length-1)].taxs.butDiscPerc;
     this.addtaxColapse = (response.data[(response.data.length-1)].taxs.addtaxColapse=='false')?false:true;
     this.partx=[];
     // console.log(tables)
     this.partx = tables;

  //this.partx[0].parts.content.alttax=false;
})
}

if(this.tmp.type=='Damage Description'){

axios.get('/get_damage', {
  params: {
    id: this.tmp.id
  }
}).then(response => {
this.loadDamages = response.data;
})
}

        // this.$socket.send('getFiles')
        // this.$options.sockets.onmessage = (data) => (data.data=='getFiles') ? this.docs2files(): ''
        // this.funcStop=1
},


getProjectDetail(old){

  var opt_images = [{id:0, value:'Undefined'}]


axios.get('/get_types_for_tables', {
}).then(response => {
  this.types_for_tables = response.data;
});

axios.get('/project_detail_new', {
  params: {
    id: this.id
  }
}).then(response => {
  response.data.filter((v)=>{
    axios.get('/get_tables', {
      params: {
        id: v.id
      }
    }).then(response => {
      if ((v.type!='Invoices') && (v.type!='Sub Invoices')) {
        for (let i = 0; i < (response.data.length-1); i++) {
            opt_images.push({id:response.data[i].parts.id, value:response.data[i].parts.part_name})
        }
      }
      if(opt_images!=this.opt_images){
        this.opt_images = opt_images
      }
    })

      // var cOffer=0
      // var cCounract=0
      // response.data.forEach((v, index)=>{
      //   console.log(v)

      //   if (v.type == 'Offers') {
      //   cOffer=cOffer+1
      //   if(cOffer.toString().length<2){
      //       cOffer = '0'+cOffer
      //       v.number = v.number + '-' + cOffer
      //   // console.log(index, cOffer)

      //   } 
      //   }

      //   if (v.type == 'Contracts') {
      //   cCounract=cCounract+1
      //   if(cCounract.toString().length<2){
      //       cCounract = '0'+cCounract
      //       v.number = v.number + '-' + cCounract
      //   } 
      //   }
      // })


      // response.data.brutto = this.$options.filters.thousandSeparator(response.data.brutto);
      // response.data.netto = this.$options.filters.thousandSeparator(response.data.netto);
      
        v.netto = this.$options.filters.thousandSeparator(parseFloat(v.netto));
        v.brutto = this.$options.filters.thousandSeparator(parseFloat(v.brutto));
        if (v.type == 'Damage Description'){
          // console.log(v.number)
        }
        return v;
      })

  this.items_table = response.data;

})
axios.get('/get_workers', {
}).then(response => {
  this.workers = [],
  response.data.forEach((v)=>{
    // console.log(v)
    this.workers.push({'value':v.id, 'text':((v.short_name!=null)?v.short_name:v.name)})
  })
})




  
 
if(this.updatePojectFunc==0){
    this.updatePojectFunc=1
     if(this.tmp.number!=null){
     var cliked = this.items_table.filter((val)=>{
     if (val.id==this.tmp.id){
       return val
     }
   })
   this.inItemGetData(cliked[0], 0)

} 
    this.area=[]
     axios.get('/project_detail', {
                params: {
                    id: this.id
                }
            }).then(response => {
                    var num = response.data.id
                    var nuls=3-num.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        num='0'+num
                    }

                    this.project.work = response.data.work,
                    this.project.number=num+'-'+response.data.project_number_year,
                    this.project.date = response.data.date,
                    this.project.street = response.data.street,
                    this.project.city = response.data.city,
                    this.project.zip = response.data.zip,
                    this.project.other = response.data.other,
                    this.project.editor = response.data.first_name + ' ' + response.data.second_name

                    var customer_id=response.data.customer_id
                    var person_id=response.data.person_id
                    var personMail=response.data.mail
                    var personPhone=response.data.phone
                    var personFax=response.data.fax
this.docs2files()
this.getdomageImages()

                    var countValPers=0
                    axios.get('/person_date', {
                params: {
                    old: old
                }
            }).then(response => {
              this.area = response.data;

                     response.data.forEach((val)=>{
//                 axios.get('/mails', {
//                                 params: {
//                                     id: val.person
//                                 }
//                             }).then(response => {
//                                 var mail = response.data;

//                 axios.get('/phons', {
//                                 params: {
//                                     id: val.person
//                                 }
//                             }).then(response => {
//                             var phone = response.data;
//                 axios.get('/faxs', {
//                                 params: {
//                                     id: val.person
//                                 }
//                             }).then(response => {
//                             var fax = response.data;
 
 // if(this.area.findIndex(x => x.name == val.name)!=-1){
 // this.area[this.area.findIndex(x => x.name == val.name)].persons.push(
 // {'label': val.names, 'adress':val.street, 'adress1':val.zip+' '+val.city, 'mail': mail, 'tel' : phone, 'fax': fax, 'id' : val.person})}
 // else{
 // this.area.splice(0, 0,
 // {'id':val.id, 'name':val.name,  'adress':val.street, 'adress1':val.zip+' '+val.city, 'persons':[{'label': val.names, 'mail': mail, 'tel' : phone, 'fax': fax, 'id' : val.person}]});
 // }



 if(val.id==customer_id){
     this.area.forEach((valArea)=>{
         if(valArea.name==val.name){
     
             if(this.customer!=valArea){this.customer=valArea}
         }
          val.persons.forEach((per)=>{
          if(per.id == person_id){
             countValPers++
             var newPerson=per

             if(this.person!=newPerson){
               this.person=newPerson
              }
             if(this.person.mail[personMail]!=undefined){if(this.personMail!=this.person.mail[personMail].mail){this.personMail=this.person.mail[personMail].mail}}else{this.personMail=null}
             if(this.person.tel[personPhone]!=undefined){if(this.personPhone!=this.person.tel[personPhone].phone){this.personPhone=this.person.tel[personPhone].phone}}else{this.personPhone=null}
             if(this.person.fax[personFax]!=undefined){if(this.personFax!=this.person.fax[personFax].fax){this.personFax=this.person.fax[personFax].fax}}else{this.personFax=null}

          }
         })

             if(countValPers==0){
              this.person=null
             }
    
     }) 
 }

         setTimeout(()=>{
          
                        this.updatePojectFunc=0;
                  }, 1000);
    
                             })
                         // })
                     // })
                    
                 // })
                
                     // this.customer.adress='response.data.street;';
                     // this.customer.adress1='response.data.zip++response.data.city;';
                     // this.customer.adress=response.data.street;
                     // this.customer.adress1=response.data.zip+' '+response.data.city;
             

            })
            })
            // axios.get('/offers', {
            //     params: {
            //         id: this.id
            //     }
            // }).then(response => {
            //     this.offers = response.data.filter((val)=>{
            //                     //console.log(val.type)
            //     if (val.type!='offer'){
            //          var separator = val.offer_number.split('-')
            //          val.offer_number=separator[0]+'-'+val.type.split('-')[1]+'-'+separator[1]+'-'+separator[2]
            //     } 
            //     return val
            //     })
                
            // })
            // axios.get('/invoices', {
            //     // params: {
            //     //     id: this.id
            //     // }
            // })
            // .then(response => {
            //   // this.invoices = []
            //   //   response.data.forEach((val)=>{

            //   //     var countNull = (4-val.id.toString().length)
            //   //     var nulls = ''
            //   //     for (var i = 0; i < countNull; i++){
            //   //         nulls = nulls + '0'
            //   //     }
                 
            //   //     val.inoice_number=nulls+val.id+'-'+val.year
            //   //     this.invoices.push(val) 
            //   //   })
                
            // })
}



        // this.$socket.send('getFiles')
        // this.$options.sockets.onmessage = (data) => (data.data=='getFiles') ? this.docs2files(): ''
}

    },

    watch: {
    customer : function (val, oldval) {

    if (this.updatePojectFunc==0){
        this.updatePojectFunc=1
        //console.log(val, oldval)
        if(val!=null)
            { 
              if(oldval==null){
                oldval={ name:null }
              }
                if (val.name!=oldval.name){
                    if (oldval.name!=null){
                      this.person = null
                    }
                    if(this.area.indexOf(val)!=-1){

                        this.updateProject('customer_id', val.id)
                        setTimeout(()=>{
                             this.updateProjectAfter()
                        }, 1000);
                    }
                    // else{
                    //     this.insertCustomer(val.hasOwnProperty('name')?val.name:val, 'customer')
                    // }

                    // this.updateProject('person_id', '-1')
                    // this.updateProject('mail', '-1')
                    // this.updateProject('phone', '-1')
                    // this.updateProject('fax', '-1')

                     //this.person=null
                     //this.personMail=null
                     //this.personPhone=null
                     //this.personFax=null
                    


                }
        }
    }
    },
     person : function (val, oldval) {
if (this.updatePojectFunc==0){

   this.updatePojectFunc=1
      //  if(this.area.findIndex(x => x.name == val)!=-1){
                 
if(oldval==null){
 oldval={id:-1}
}
if(val==null){
 val={id:-1}
}
        if(val.hasOwnProperty('id')){
            if (val.id!=oldval.id){

             this.updateProject('person_id', val.id)
             setTimeout(()=>{
                  this.updateProjectAfter()
             }, 1000);
         }}
          // }else{
          //       this.insertCustomer(val.hasOwnProperty('label')?val.label:val, 'person')
          // }
                  
if(this.person!=undefined){
                      this.updateProject('mail', '0')
                      this.updateProject('phone', '0')
                      this.updateProject('fax', '0')
                      
                      this.personMail=(this.person.mail[0]!=undefined)?this.person.mail[0].mail:null
                      this.personPhone=(this.person.tel[0]!=undefined)?this.person.tel[0].phone:null
                      this.personFax=(this.person.fax[0]!=undefined)?this.person.fax[0].fax:null
                      }
//}
}
     },
      personMail : function (val, oldval) {
         if (this.updatePojectFunc==0){
             this.updatePojectFunc=1
  if (this.person!=null){
  if(oldval==null){
   oldval={mail:-1}
  }

  if(val==null){
   val={mail:-1}
  }


              if(this.person.mail.findIndex(x => x.mail == this.personMail)!=-1){
                  this.updateProject('mail', this.person.mail.findIndex(x => x.mail == this.personMail))
                  setTimeout(()=>{
                       this.updateProjectAfter()
                  }, 1000);
              }

              // else{
              //     this.insertCustomer(val, 'mail', this.person.id, this.person.mail.length)
              // }
 }
 this.updatePojectFunc=0
}
      },


      personPhone : function (val, oldval) {
         if (this.updatePojectFunc==0){
  if (this.person!=null){
  if(oldval==null){
   oldval={tel:-1}
  }

  if(val==null){
   val={tel:-1}
  }
              if(this.person.tel!=undefined && this.person.tel.findIndex(x => x.phone == this.personPhone)!=-1){
                  this.updateProject('phone', this.person.tel.findIndex(x => x.phone == this.personPhone))
                  setTimeout(()=>{
                       this.updateProjectAfter()
                  }, 1000);
                  }
              //     else{
              //     this.insertCustomer(val, 'phone', this.person.id, this.person.tel.length)
              // }
          }
      }
      },
      personFax : function (val, oldval) {
        //console.log(this.updatePojectFunc)
        if (this.updatePojectFunc==0){
             this.updatePojectFunc=1
  if (this.person!=null){
  if(oldval==null){
   oldval={fax:-1}
  }

  if(val==null){
   val={fax:-1}
  }


              if(this.person.fax.findIndex(x => x.fax == this.personFax)!=-1){
                  this.updateProject('fax', this.person.fax.findIndex(x => x.fax == this.personFax))
                  setTimeout(()=>{
                       this.updateProjectAfter()
                  }, 1000);
              }

              // else{
              //     this.insertCustomer(val, 'mail', this.person.id, this.person.mail.length)
              // }
 }
 this.updatePojectFunc=0
}
      },
          partx: {
            handler: function(newValue, oldValue) {
              var arr2 = 0
              newValue.forEach((v)=>{
                for (var obj in v.parts.checkbox_list.selected) {
                 arr2 = arr2 + v.parts.checkbox_list.selected[obj].length
                }
              })
              
              if(this.selectedLenght!=arr2){
                this.discOfPercent()
              }
              this.selectedLenght = 0
              oldValue.forEach((v)=>{
                for (var obj in v.parts.checkbox_list.selected) {
                  this.selectedLenght = this.selectedLenght + v.parts.checkbox_list.selected[obj].length
                }
              })
                        
                    },
                    deep: true,
                },

        commentOfTable: function(value) {

            var result
            var sval
            var separator
            var indexReplace, indexRuslt
            var safeEval = require('safe-eval')

            separator = this.$refs.refCommentOfTable.quill.getText()
            separator = separator.replace(/\n/g, ' ')
            separator = separator.substring(0, separator.length - 1);
            separator = separator.split(' ')
            separator.splice(-1, 1)
            separator.forEach((val) => {
                if (val.search(/[a-zA-z=]/gim) == -1) {
                    if (val.search(/[-+*)(/]/gim) > -1) {
                        if (val.search(/[0-9]/gim) > -1) {
                            if (/[\d)]/.test(val[val.length - 1])) {
                                try {
                                    result = this.$options.filters.thousandSeparator(safeEval(val))
                                } catch (e) {
                                    result = '(not valid formula)'
                                }
                                sval = val.replace(/([-+*)(/])/gim, '$1&shy;') + '=' + result + ' '
                                indexRuslt = result.length ? result.length : 4
                                indexReplace = this.commentOfTable.indexOf(val) + indexRuslt + 6
                                this.$refs.refCommentOfTable.quill.clipboard.dangerouslyPasteHTML(
                                    this.commentOfTable.replace(val, sval))
                                this.$refs.refCommentOfTable.quill.setSelection(indexReplace, 0)
                            }
                        }
                    }
                }
            })

        }
    },

      mounted(){
     setTimeout(() => {
        this.$socket.send('getProjectDetail')
        this.$options.sockets.onmessage = (data) => (data.data=='getProjectDetail') ? (this.getProjectDetail(1)): ''
        // this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? (console.log('!!!!')): ''
        this.displaytime()
        },1000);



        },
    created: function() {
        document.addEventListener('keyup', this.keyupMethod)
    }
}
</script>
<style>
.warpTree {
    position: relative;
    height: 100%;
}

.navTree {
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    overflow: auto;
    overflow-x: hidden;
    background-color: #f7f7f7;
    z-index: 9999;
}

.tree-anchor {
    text-decoration: none !important;
    font-size: 12px;
    padding: 0px;
    margin: 0px;
}

.tree-arrow {
    height: 12px;
}

.tree-arrow.has-child:after {
    height: 7px;
    width: 7px;
    top: 40%;
}

.filter-input {
    padding: 2px;
    margin: 0px;
    width: 70%;
    min-width: 125px;
    height: 20px;
    font-size: 12px;
}

.slide-leave-active,
.slide-enter-active {
    transition: 1s;
}

.slide-enter {
    transform: translate(-100%, 0);
}

.slide-leave-to {
    transform: translate(-100%, 0);
}

.butMore {
    text-decoration: none !important;
    font-size: 15px;
    padding-left: 10px;
    padding-top: 0px;
}

.cForm {
    font-size: 12px;
    height: 20px;

}

.cForm-input {
    font-size: 12px;
    height: 19px;

}

.cForm-inputG {
    height: 19px;
    width: 20px;
    font-size: 10px;
    padding: 0px;
    margin-left: 2px;
}

.cForm-text {
    font-size: 12px;
    margin-top: 20px;
}

.cForm-inputBeforG {
    font-size: 12px;
    height: 19px;
}

.v-select {
    height: 12px;
}
.cFormVsel{
    font-size: 12px;
    height: 20px;
}
 .v-select .selected-tag {margin: -29px 2px 0;}
/*@media screen and (-webkit-min-device-pixel-ratio:0) {
  .v-select .selected-tag {margin: 0 0 0;}
}*/
.v-select.open .dropdown-toggle {
    height: 12px;
}

.dropdown-toggle .clearfix {
    height: 12px;
}

.v-select .dropdown-toggle .clear {
    bottom: -7px;
    font-size: 18px;
}

.v-select .open-indicator::before {
    margin-top: 4px;
    width: 7px;
    height: 7px;
}

.v-select.searchable .dropdown-toggle {
    height: 20px !important;
}

.v-select .selected-tag {
    line-height: 4px;

}

.v-select .dropdown-menu {
    font-size: 10px !important;
    /*or some other pixel value < 160*/
}

.dropdown-toggle::after {
    display: none !important;
}

.col-form-label {
    padding: 0px;
    margin: 0px;
}

.b-form-group {
    padding: 0px;
    height: 4px;
}

.customButton {
    padding: 1px;
    font-size: 10px;
    height: 19px !important;
}

.select {
    font-size: 12px;
    height: 20px !important;
    padding: 0px;
    padding-left: 12px;
    margin: 0px;
}

input[type='number'] {
    -moz-appearance: textfield;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
}

.withoutbox input[type=checkbox] {
    display: none;
}

.withoutmargin {
    margin-bottom: 0px !important;
}

.withoutborder {
    border-top: 0px !important;
}

.collapsed>.when-opened,
:not(.collapsed)>.when-closed {
    display: none;
}


.withoutborder th,
.withoutborder td {
    border-top: 0px !important;
}

.howerRow {
    background: #e9ecef;
}

.upHereColumn {
    background-color: #007bff !important;
}

.upHereColumn input {
    background-color: #007bff !important;
}


/*////////////////////*/

.tposition input,
.tdeschead input,
.tcount input,
.tunit input,
.tprice input,
.twithout input,
.tcalc input {
    /* background-color: rgba(0,0,0,0.8);*/
}

.totalTable {
    font-size: 12px;
    font-weight: bold;
}

input {
    padding: 2px !important;
}

.ainput {
    text-align: center !important;
}

.rinput {
    text-align: right !important;
}

.cinput {
    text-align: center !important;
}

.greenrow .form-row {
    background-color: #c8e6c9;
}


/* checked icon */

.calttax {
    text-decoration: underline;
}

.quillWrapper .ql-snow.ql-toolbar {
    padding-top: 0px !important;
    height: 30px !important;
}

.ql-snow.ql-toolbar button svg {
    height: 13px !important;
}
.lablelInInput{
        height: 19px;
        font-size: 14px;
}
.prokrutka {
height: 624px; /* высота нашего блока */
overflow-y: scroll; /* прокрутка по вертикали */
overflow-x: auto; /* прокрутка по вертикали */
}
.selBtn .dropdown-toggle{
    height: 31px !important;
   /* width: 160px;*/
}
.selBtn .dropdown-toggle .vs__selected-options .selected-tag{
    line-height: 27px !important;
}
.tablePadding td{
    padding-left: 5px;
   border: 1px solid #bbb8b8;
}
.docs .footer{
    display: none !important;
}

.iframeclass iframe {
    html {
        body {
            background-color: #ffffff !important;
        }
        #zoom-toolbar {
            display: none !important;
        }
        #zoom-buttons {
            display: none !important;
        }
    }
}
.selrequired .dropdown-toggle {
border-color: red !important;
}

.iframe-container {
  overflow: hidden;
  /*padding-top: 56.25%;*/
  position: relative;
}

.iframe-container iframe {
   border: 0;
   height: 100%;
   left: 0;
   position: absolute;
   top: 0;
   width: 100%;
}
.horizontal-panes {
  width: 100%;
  height: 100vh;
  border: 1px solid #ccc;
}

.horizontal-panes > .pane {
  text-align: left;
  /*padding: 15px;*/
  overflow: hidden;
  background: #eee;
}

.horizontal-panes > .pane ~ .pane {
  border-top: 1px solid #ccc;
}
</style>