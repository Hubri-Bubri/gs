<template>
    <container>


     <b-modal size="lg" centered id="attr" ref="attr" title="Select Type">
        <b-row>
        <b-col cols="6">
 
         <b-form-select :select-size="optionsForFactory.length">
            <option v-for="item in optionsForFactory" @click="(selectedOptFactory=item.id)">{{item.name}}</option>
         </b-form-select>
        </b-col>
        <b-col>
            <div v-if="selectedOptFactory">
                <div  :key="item.id" v-for="(item, index) in optionsForFactory[optionsForFactory.findIndex(x => x.id == selectedOptFactory)].filds">
                    <b-form-group horizontal :label-cols="1" class="cForm" :label="''+(index+1)">
                        <b-row>
                            <b-col>
                                <b-form-input :value="(index!=0)?item.name:'Name'" :disabled="(index==0)" :state="null" @input="updateRowInTemplate(item.id, $event, 'name')" type="text" class="cForm-input" />
                            </b-col>
                            <b-col>
                                <b-form-select class="select" :disabled="(index==0)"
                                :value="(index!=0)?item.type:'text'" @change="updateRowInTemplate(item.id, $event, 'type')" :options="['text', 'color', 'date', 'datetime', 'datetime-local', 'email', 'number', 'range', 'search', 'tel', 'time', 'url', 'month', 'week']"></b-form-select>
                            </b-col>
                            <b-col cols="1">
                               <b-link class="butMore" style="padding-left:0px;" @click="removeRowInTemplate(item.id)">-</b-link>
                            </b-col>
                        </b-row>
                    </b-form-group>
                </div>
                <b-link class="butMore" style="padding-left:0px;" @click="addRowInTemplate(selectedOptFactory)">+</b-link>
            </div>

        </b-col>
        </b-row>


        <template slot="modal-footer" v-if="(selectedOptFactory)">
            <b-input-group-append>
                <button type="button" class="btn btn-secondary"  @click="addItemInTemplate">
                    Add item         
                </button>
                <button type="button" class="btn btn-secondary"  @click="removeItemInTemplate(selectedOptFactory)">
                    Remove item         
                </button>
            </b-input-group-append>
            <b-form-input :value="optionsForFactory[optionsForFactory.findIndex(x => x.id == selectedOptFactory)].name" @input="updateItemInTemplate(selectedOptFactory, $event)">
            </b-form-input>
            <b-input-group-append>
                <button type="button" class="btn btn-primary" @click="addRowForFactory(optionsForFactory[optionsForFactory.findIndex(x => x.id == selectedOptFactory)].name, selectedOptFactory)">OK</button> 
            </b-input-group-append>
        </template>
      </b-modal>

     <b-modal size="md" centered id="move" ref="move" title="Move">
        <!-- @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" -->
         <b-form-select class="" id="move" v-model="selectedItems" :select-size="detectRowSise(items_menu)">
            <option v-for="item in detectItem(items_menu)" :disabled="addFactoryButton?item.type=='factory':item.type=='part'" @click="selectedModal(item)">{{item.name}}</option>
         </b-form-select>

         <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['move', 'copy']" />
         <template slot="modal-footer">
<!--             <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>-->
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button> 
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
                        <b-tab title="Company Data">
                            <container>
                                <container-body>
                                    <b-container>
                            <b-row>
                                <b-col cols="4" > 
                                    <vue-drag-tree :data='items_menu'
                                    :allowDrag='allowDrag'
                                    :allowDrop='allowDrop' disableDBClick
                                    @drag="dragHandler" @drag-enter="dragEnterHandler"
                                    @current-node-clicked="curNodeClicked"
                                    @drag-leave="dragLeaveHandler" @drag-over="dragOverHandler"
                                    @drag-end="dragEndHandler" @drop="dropHandler" :thrId="idNode" :parId="parId">
                                    </vue-drag-tree>                              
                                </b-col> 
                                <b-col cols="8">
                                    <b-table stacked="lg" borderless small hover :items="items" :fields="this.addFactoryButton?fields_workers:fields_factory"
                                        class="tableProject"
                                        @row-clicked="inItemGetData"
                                        @row-dblclicked="rowSelected" >
                                             <template slot="index" slot-scope="data">
                                                {{ data.index + 1 }}
                                              </template>
<!--                                             <template slot="name" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.name" @input="updateDate($event, 'name', row.item.id)"></b-input>
                                            </template>
                                            <template slot="short_name" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.short_name" @input="updateDate($event, 'short_name', row.item.id)"></b-input>
                                            </template>
                                            <template slot="start_work" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.start_work" @input="updateDate($event, 'start_work', row.item.id)"></b-input>
                                            </template>
                                            <template slot="end_work" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.end_work" @input="updateDate($event, 'end_work', row.item.id)"></b-input>
                                            </template>
                                            <template slot="position" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.position" @input="updateDate($event, 'position', row.item.id)"></b-input>
                                            </template>
                                            <template slot="salary" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" v-model="row.item.salary" @input="updateDate($event, 'salary', row.item.id)"></b-input>
                                            </template>
                                            <template slot="desc" slot-scope="row">
                                                <div contenteditable="true" @input="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
                                            </template>--> 
                                            <template slot="delete" slot-scope="row">
                                                   <b-link @click="delRow(row.item.id)" class="fas fa-trash fa-w-16 text-center" />
                                            </template>
                                    </b-table>
                                    <div hidden>{{ selected }}</div>
                                </b-col>
                            </b-row>
                        </b-container>
                    </container-body>
                </container>
                <b-card-footer>


                        <b-input-group>
                            <b-input-group-append>
                                <b-button :disabled="addFactoryButton" @click="add('factory')">Add Factory</b-button>
                                <b-button :disabled="idNode==129" @click="add('part')">Add Part</b-button>
                                <b-button :disabled="idNode==129" @click="remove">Remove</b-button>
                            </b-input-group-append>
                            <b-form-input v-model="nameNode" @input="toModel"></b-form-input>
                            <b-input-group-append>
                                <b-button @click="addRow">Add Row</b-button>
                                <b-button @click="mv_cp">Move/Copy</b-button>
                            </b-input-group-append>
                        </b-input-group>
           

            </b-card-footer>
 </b-container>
                      </b-tab>

                  </b-tabs>
              </b-card>
              <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Details">
                            <container>
                                <container-body>

 <b-container v-if="(addFactoryButton) && (details.id!=null)">

<b-row>
<b-col sm="6" class="cuestomRow">
<b-form-group horizontal :label-cols="4" class="cForm" label="ID:">
<b-form-input :state="null" disabled type="text" :value="details.id" class="cForm-input" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" label="Start Date:">
<b-form-input :state="null" type="date"  :value="details.start_work" placeholder="Enter date" class="cForm-input" @change="updateDate($event, 'start_work', details.id)" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" label="End Date:">
<b-form-input :state="null" type="date"  :value="details.end_work" placeholder="Enter date" class="cForm-input" @change="updateDate($event, 'end_work', details.id)" />
</b-form-group>
</b-col>

<b-col sm="6" class="cuestomRow">
<b-form-group horizontal :label-cols="4" class="cForm" label="Name:">
<b-form-input :state="null" type="text" :value="details.name" placeholder="Enter name" class="cForm-input" @change="updateDate($event, 'name', details.id)" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" label="Short Name:">
<b-form-input :state="null" type="text" :value="details.short_name" placeholder="Enter Short Name" class="cForm-input" @change="updateDate($event, 'short_name', details.id)"  />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" label="Position:">
<b-form-input :state="null" type="text" :value="details.position" placeholder="Enter position" class="cForm-input"  @change="updateDate($event, 'position', details.id)" />
</b-form-group>
</b-col>
</b-row>





                               <b-row >
                                      

                            
                                            <b-col sm="12">
                                             <br>
                                            </b-col> 
                                          <b-col sm="4" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" :label="'Mail: '+(index+1)" v-for="(m, index) in details.mail" :key="m.id">
                                                    <b-input-group>
                  <b-form-input :value="m.mail"  @change="m.mail=$event;editContactInPerson('mail', details.mail)"
                                                     type="text" placeholder="Enter mail" class="cForm-input" />
                                                         <b-input-group-append>
                                          

                    <b-link style="margin-left:10px"
                    @click="(index==0)?addContactInPerson('mail', '+', index):addContactInPerson('mail', '-', index)">
                        {{(index==0)?'+':'-'}}
                    </b-link> 
                                                            </b-input-group-append>
                                                              </b-input-group>
                                                </b-form-group>
                                            </b-col>
                                          <b-col sm="4" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" :label="'Phone: '+(index+1)" v-for="(p, index) in details.phone" :key="p.id">
                                                    <b-input-group>
<b-form-input :value="p.phone"  @change="p.phone=$event;editContactInPerson('phone', details.phone)"
                                                    type="text" placeholder="Enter phone" class="cForm-input" />
                                                       <b-input-group-append>
                                                    
                    <b-link style="margin-left:10px"
                    @click="(index==0)?addContactInPerson('phone', '+', index):addContactInPerson('phone', '-', index)">
                        {{(index==0)?'+':'-'}}
                    </b-link> 
                                                    </b-input-group-append>
                                                    </b-input-group>
                                                </b-form-group>
                                            </b-col>
                                          <b-col sm="4" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" :label="'fax: '+(index+1)" v-for="(f, index) in details.fax" :key="f.id">
                                                    <b-input-group>
<b-form-input :value="f.fax"  @change="f.fax=$event;editContactInPerson('fax', details.fax)" 
                                                        type="text" placeholder="Enter fax" class="cForm-input" />
                                                       <b-input-group-append>

                     <b-link style="margin-left:10px"
                    @click="(index==0)?addContactInPerson('fax', '+', index):addContactInPerson('fax', '-', index)">
                        {{(index==0)?'+':'-'}}
                    </b-link>


                                                    </b-input-group-append>
                                                    </b-input-group>
                                                </b-form-group>
                                            </b-col>
                                            <b-col cols="12"><br></b-col>
                                           <b-col sm="12" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="1" class="cForm" :label="'Adress: '+(index+1)" v-for="(a, index) in details.adress" :key="a.id">
                                                    <b-input-group>
                                                        <b-form-input :value="a.adress.split(';')[0]" @input="a.adress=$event+';'+a.adress.split(';')[1]+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')"  @change="editContactInPerson('adress', details.adress)" 
                                                        type="text" placeholder="Enter Adress" class="cForm-input" />
                                                        <b-form-input :value="a.adress.split(';')[1]" @input="a.adress=a.adress.split(';')[0]+';'+$event+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')"  @change="editContactInPerson('adress', details.adress)" 
                                                         type="text" placeholder="Enter Adress" class="cForm-input" />
                                                        <b-form-input :value="a.adress.split(';')[2]" @input="a.adress=a.adress.split(';')[0]+';'+a.adress.split(';')[1]+';'+$event;a.adress=a.adress.replace(undefined, '')"  @change="editContactInPerson('adress', details.adress)" 
                                                        type="text" placeholder="Enter Adress" class="cForm-input" />
                                                       <b-input-group-append>

                    <b-link style="margin-left:10px"
                    @click="(index==0)?addContactInPerson('adress', '+', index):addContactInPerson('adress', '-', (index-2))">
                        {{(index==0)?'+':'-'}}
                    </b-link> 

                                                    </b-input-group-append>
                                                    </b-input-group>
                                                </b-form-group>
                                            </b-col> 
                                        </b-row>



</b-container>

<b-container v-if="(addFactoryButton==false) && (details.id!=null)">
<b-row fluid>
{{test(details, optionsForFactory)}}
<b-container :key="block.id" class="border-bottom" style="padding:7px;"
v-for="(block, inc) in parseInt(details.content.length/optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length)">
 
<b-link style="text-decoration: none; font-size: inherit; line-height: 1.5;"
v-b-toggle="'block'+inc">
<span class="when-closed">+ {{blocks(details.content,
    optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length, inc)[0].content}}</span>
</b-link>
               

 <b-collapse :id="'block'+inc" visible>
    <b-col cols="12">
<b-form-group horizontal :label-cols="4"
v-for="(dataForRows, index) in blocks(details.content, optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length, inc)" :key="dataForRows.id"
class="cForm">

    <template slot="label">
        <b-link v-if="(index==0)&&(dataForRows.content.length > 0)"
        v-b-toggle="'block'+inc"
        >
            {{getDataTamplate(optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds, 'name', index)}}
        </b-link>
        <span v-else>
            {{getDataTamplate(optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds, 'name', index)}}
        </span>
    </template>
<b-row>
<b-col :cols="((index==0)&&(dataForRows.content.length > 0))?9:12">
<b-input  :type="getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'type', index)"
:value="dataForRows.content"  class="cForm-input" @change="updateContent(
$event,
optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length,
inc,
index,
details.id
)" />
</b-col>

    <b-col cols="3" v-if="(index==0)&&(dataForRows.content.length > 0)">
        <b-link @click="removeContent(
optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length,
inc,
details.id
        )">
            Remove
        </b-link>
    </b-col>
</b-row>


                </b-form-group>

                </b-col>
                
            </b-collapse>

</b-container>


    </b-row>


</b-container>

                 </container-body>
                                 <b-card-footer  v-if="(addFactoryButton==false) && (details.id!=null)">
 <b-input-group v-if="(addFactoryButton==false) && (details.id!=null)">
<b-form-input v-model="details.name" ></b-form-input>

 <b-button  @click="addBlock(optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length)">
    Add
</b-button>
</b-input-group>

            </b-card-footer>
             </container>
         </b-tab>
                               <b-tab title="Files">
                            <container>
                                <container-body>
                                     <b-table :items="filesPersonal" :fields="fieldsFiles" class="tableProject">
                                        <template slot="show_details" slot-scope="row">
                                            <b-link size="sm" @click.stop="row.toggleDetails" class="butMore">
                                                {{ row.detailsShowing ? '-' : '+'}}
                                            </b-link>
                                        </template>
                                        <template slot="row-details" slot-scope="row">
                                            <iframe type="iframe1" :style="'width:100%;height:'+(30.1*((row.item.pages==0)?0.25:row.item.pages)+1.5)+'cm'" frameborder="0" :name="'ifr1'+row.index" class="iframeclass" src="" :onload="loadDocToFrame(row.index)" v-if="row.item.gallery==undefined">
                                            </iframe>
                                            <form :target="'ifr1'+row.index" :action="(row.item.html!='file') ? '/pdf1':'/pdf2'" method="post" :ref="'ifrForm'+row.index">
                                                <input type="hidden" name="html" :value="row.item.html" style="display:none" v-if="(row.item.html!='file')" />
                                                <input type="hidden" name="id" :value="row.item.id" v-else />
                                            </form>
                                        </template>
                                    </b-table> 
                                </container-body>
                                <b-container>
                                    <b-collapse id="drop1">
                                        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent1" v-on:vdropzone-success="fsadd">
                                        </vue-dropzone>
                                    </b-collapse>
                                    <div style="background-color:#ced4da">
                                        <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal; With:100%" v-b-toggle="'drop1'">
                                            <span class="when-closed">+</span>
                                            <span class="when-opened">-</span>
                                        </b-link>
                                    </div>
                                </b-container>
                            </container>
                        </b-tab>
     </b-tabs>
 </b-card>

          </b-card-group>
      </container-body>
  </container>
</template>

<script>
import io from 'socket.io-client';
import axios from 'axios';
import {
    VueEditor,
    Quill
} from 'vue2-editor';
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
export default {
    components: {
        VueEditor,
        vueDropzone: vue2Dropzone
    },
  data(){
    return{     
                selectedOptFactory:null,
                optionsForFactory:[
                    // {name:'Bank details', rows: ['Bank Code', 'Bank Name', 'Account Number', 'BIC', 'IBAN']},
                    // {name:'type1', test2:'test2'},
                    // {name:'type3', test3:'test3'}
                ],
                files:[],
                filesPersonal:[],
                fieldsFiles: [{
                    key: 'show_details',
                    label: 'show'
                },
                {
                    key: 'name',
                    label: 'name',
                    sortable: true
                },
                {
                    key: 'added',
                    sortable: true
                }
            ],
            dropzoneOptions: {
                url: '/loadFiles',
                thumbnailWidth: 50,
                parallelUploads: 10
            },

            responseFiles: [],
      details:{
        id:null,
        start_work:null,
        end_work:null,
        position:null,
        name:null,
        short_name:null,
        salary:null,
        licens:null,
        educations:null,
        adress:null,
        files:null,
        mails:null,
        phons:null,
        faxs:null
      },
      tmp:{
                    person:null,
                    old:null,
                    adress:null,
                    data:null,
                    appeal:null,
                    dep:null,
                    pos:null,
                    other:null,
                    names:null,
                    customer_group:null,
                    mail:null,
                    phone:null,
                    fax:null,
                    adress:null
                    },
      addFactoryButton:true,
      moveToCopyRadio:'move',
      rowColor:'background-color:#c3e6cb',
      selected:[],
      items:[],
      nameNode:null,
      idNode:null,
      parId:null,
      oldId:0,
      selectedItems:[],
      fields_workers: [{
                    key: 'index',
                    label: 'index',
                    tdClass: 't_index',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'Name',
                    // tdClass: 't_pos_num',
                    sortable: true
                },
                {
                    key: 'position',
                    label: 'Position',
                    // tdClass: 't_price',
                    sortable: true
                },

                // {
                //     key: 'percent',
                //     tdClass: 't_percent',
                //     label: '%',
                //     sortable: true
                // },
                {   key: 'delete',
                    label: 'Del'
                }
            ],
        fields_factory: [{
                    key: 'index',
                    label: 'index',
                    tdClass: 't_index',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'Props Name',
                    // tdClass: 't_pos_num',
                    sortable: true
                },
  
                // {
                //     key: 'percent',
                //     tdClass: 't_percent',
                //     label: '%',
                //     sortable: true
                // },
                {   key: 'delete',
                    label: 'Del'
                }
            ],
          items_menu:[],
          drag1: null,
          drag2: null
    }

  },
    methods: {
test(details, optionsForFactory){
console.log(parseInt(details.content.length/optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length))
},
    blocks(arr, l, befor){
        befor = befor + 1
        var retArr=[]

        for (var i = (l*befor)-l; i < (l*befor); i++) {
            // console.log(i, l, befor)
            retArr.push(arr[i])
        }
        return retArr
            // if (index<l){

            //     return(v)
            // }

    },
    getDataTamplate(v, type, i){

    var x = i
    // if(i, i>=v.length){
    //     x = i%v.length
    // }
        if (v[x]!=undefined){
            return v[x][type]
        }
    },    
    addItemInTemplate(){
            axios.get('/add_Item_in_template_for_factory')
    },
    removeItemInTemplate(id){
            this.selectedOptFactory=null,
            axios.get('/remove_Item_in_template_for_factory', {
                params: {
                    id: id
                }
            })
    },
    updateItemInTemplate(id, value){
        axios.get('/update_Item_in_template_for_factory', {
                params: {
                    id: id,
                    value: value
                }
            })
    },
    addRowInTemplate(id){
        axios.get('/add_row_in_template_for_factory', {
            params: {
                id: id
            }
            })
    },
    removeRowInTemplate(id){
        axios.get('/remove_row_in_template_for_factory', {
            params: {
                id: id
            }
            })
    },
   updateRowInTemplate(id, value, type){
        axios.get('/update_row_in_template_for_factory', {
            params: {
                id: id,
                value: value,
                type: type
            }
            })
    },
    addBlock(l){
        axios.get('/add_block', {
            params: {
                id: this.details.id,
                l: l
            }
            })
    },


    loadDocToFrame(index) {
            setTimeout(() => {
                if (this.$refs['ifrForm' + index].submit() != undefined) this.$refs['ifrDocForm' + index].submit()
            }, 10);
        },

    getFilesPersonal(){
        axios.get('/files', {
            params: {
                id: 'personal-'+this.details.id
            }
            }).then(response => {
                this.filesPersonal = response.data
            })
    },

    sendingEvent1(file, xhr, formData) {
            xhr.setRequestHeader('number', 'personal-'+this.details.id);
        },
            fsadd() {
            this.$refs.myVueDropzone.removeAllFiles()
            this.$socket.send('getFilesPersonal')
        },



    addContactInPerson(fild, action, index){
        console.log(fild, action, index)
        if (action=='+'){
            this.details[fild].push({[fild]:''})
        } else{
             axios.get('/contact_in_person_remove_row', {
                 params: {
                         fild: fild,
                         id: this.details.id,
                         value: this.details[fild][index][fild],
                         type: 'personal'
                 }
             }).then(response =>{
                this.details[fild].splice(index, 1)
             })
        }
    },
    editContactInPerson(fild, value){
        // delete this.$options.sockets.onmessage;
        var sendArr=[]
        value.forEach((v)=>{
            sendArr.push(v[fild])
        })
        axios.get('/edit_contact_person', {
            params: {
                    fild: fild,
                    value: sendArr.join(),
                    id: this.details.id,
                    type: 'personal'
                }
        })
    },
        // updateCustomerAfter(){
        //            this.$options.sockets.onmessage = (data) => (data.data=='getPersonal') ? this.getPersonal(): ''

        // },




       inItemGetData(item){
        // console.log(item)
            // this.addFactoryButton?'part':'factory'
            this.details = item,
            axios.get('/files', {
            params: {
                id: 'personal-'+this.details.id
            }
            }).then(response => {
                this.filesPersonal = response.data
            })
       },
       getPersonal(){
  this.items = [] 
        // console.log(this.idNode);
        if (this.idNode!=null){
            axios.get('/personals', {
                params: {
                    id: this.idNode,
                    type: this.addFactoryButton?'part':'factory'
                }
            }).then(response => {
                if (this.addFactoryButton==true){
                 
                this.items = response.data.filter((v, i)=>{
                    // if(this.items.length!=0){
                    //     this.items[i].mail=['']
                    // }
                    v.mail =  (v.mail[0]==undefined)?[{mail:''}]:v.mail
                    v.phone =  (v.phone[0]==undefined)?[{phone:''}]:v.phone
                    v.fax =  (v.fax[0]==undefined)?[{fax:''}]:v.fax
                    v.adress = (v.adress[0]==undefined)?[{adress:';;'}]:v.adress 
                    v.adress = v.adress.filter((a)=>{
                    a.adress =a.adress.replace(/,/g, ';')

                        return a
                    })
                    return v
                })

            }else{
                this.items = response.data
                axios.get('/get_templates_for_factory')
                    .then(response=>{
                        this.optionsForFactory=response.data
                    }
                )

                if(this.details.id!=null){
                    this.items.forEach((v)=>{
                        if(v.id == this.details.id){
                            this.details = v
                        }
                    })
                }
            }
            console.log(response.data)
            })
            if (this.details!=null){
                    this.items.forEach((v)=>{
                    if(v.id == this.details.id){
                        this.details = v,
                        axios.get('/files', {
                        params: {
                            id: 'personal-'+this.details.id
                        }
                        }).then(response => {
                            this.filesPersonal = response.data
                        })
                    }
                })
                
            }
        }
        axios.get('/personal_menu').then(response => {
            this.items_menu=[];
               response.data.forEach((val)=>{
                         if (val.parrent==0){
                            val['children']=[]
                            this.items_menu.push(val);
                        }
               })
                response.data.forEach((valResp)=>{
                  function findLevel(obj, id) {
                        obj.forEach((val)=>{
                            if (val.id==id){
                                valResp['children']=[]
                                val.children.push(valResp);
                            } else{
                                if (val.children.length!=0){
                                    findLevel(val.children, id)
                                }
                            }
                        })
                    }

        findLevel(this.items_menu, valResp.parrent)  
               })
            })
        },
    
    allowDrag(model, component) {
      if (model.name === 'Node 0-1') {
        // can't be dragged
        return false;
      }
      // can be dragged
      return true;
    },
    
    allowDrop(model, component) {
      if (model.name === 'Node 2-2') {
        // can't be placed
        return false;
      }
      // can be placed
      return true;
    },
     allowDragModal(model, component) {
        return false;
    },
    
    allowDropModal(model, component) {
        return false;
    },   
    // curNodeClicked(model, component) {
    //     this.addFactoryButton = (model.type!='factory'),
    //     this.nameNode = model.name,
    //     this.idNode = model.id,


    //     this.details.id=null
    // },



curNodeClicked(model, component) { 
    this.addFactoryButton = (model.type!='factory'),
        this.nameNode = model.name,
        this.idNode=model.id,
        this.details.id=null,
        this.parId = model.parrent
        // console.log(this.idNode == this.oldId)
        // console.log(this.idNode, this.oldId)
        // if(this.idNode == this.oldId){
        //      if (this.items.length>0){
        //         this.items=[]
        //     } 
        // }
        // this.oldId = this.idNode
        // if ((model.parrent == 0) && component.folder == false){
        //     this.idNode = null
        // }
    },

    curNodeClickedModal(model, component){
        console.log('!!!'),
        this.idNodeModal=model.id
    },
    toModel(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    //val.name=enterVal
                    axios.get('/update_name_personal_menu', {
                        params: {
                            name: enterVal,
                            id: id
                        }
                    })
                } else {
                    if (val.children.length!=0){
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.items_menu, this.idNode)
    },
    remove(){
       if (this.idNode==null){
            alert('No menu item is selected for deletion.')
       }
       else {
            if (confirm("Are you sure want to remove?")) {
                axios.get('/remove_personal_menu', {
                    params: {
                        remove_id: this.idNode
                    }
                }).then(response=>{
                    this.idNode=null,
                    this.nameNode=null
                })
            }
        }
    },
    removeContent(count, id, detail){
            if (confirm("Are you sure want to remove?")) {
                 axios.get('/remove_block', {
                     params: {
                         remove_count: count,
                         remove_id: id,
                         detail_id: detail
                     }
                 })
            }
    },
    updateContent(val, count, inc, index, detail){
        axios.get('/update_block', {
             params: {
                 val: val,
                 count: count,
                 inc: inc,
                 index: index,
                 detail: detail
            }
        })
         
    },
    add(type){
      function findLevel(obj, id) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_personal_menu', {
                        params: {
                            parent_id: val.id,
                            type: type
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.items_menu, this.idNode)  
    },
    addRow(){
        if (this.idNode==null){
            alert('No menu item is selected for add.')
        } else {
            if (this.addFactoryButton){
                axios.get('/add_personal', {
                    params: {
                        id: this.idNode,
                        type: this.addFactoryButton?'part':'factory',
                        option: '',
                        option_id: ''
                    }
                })
            } else{
                this.$refs.attr.show()
            }
        }
    },
    addRowForFactory(option, id){
        axios.get('/add_personal', {
                    params: {
                        id: this.idNode,
                        type: this.addFactoryButton?'part':'factory',
                        option: option,
                        option_id: id
                    }
        })
        this.$refs.attr.hide()
    },
    delRow(id){
        if (confirm("Are you sure want to remove?")) {
            axios.get('/remove_personal', {
                params: {
                    id: id,
                    type: this.addFactoryButton?'part':'factory'
                }
            })
        }
    },
    updateDate(data, fild, id, type){
// delete this.$options.sockets.onmessage;
        axios.get('/update_personal', {
            params: {
                data: data,
                fild: fild,
                id: id,
                type: this.addFactoryButton?'part':'factory'
            }
        })
    },
    rowSelected(items) {
         if(this.selected.indexOf(items)==-1){
            this.selected.push(items)
            items._rowVariant='success'
         } else{
            this.selected.splice(this.selected.indexOf(items), 1)
            items._rowVariant=''
         }
    },
    mv_cp(){
        if (this.idNode==null){
            alert('No menu item is selected.')
        } else{
            if (this.selected.length==0){
                alert('No rows selected.')
            }
        }
        if ((this.idNode!=null)&&(this.selected.length!=0)){
            this.$refs.move.show()           
        }
    },
    okMoveToCopy(){
        this.selected=[],
        this.$refs.move.hide()
    },
    detectItem(items){
      var returnArr=[]
      var addCount=''
      function findLevel(obj) {
            obj.forEach((val)=>{
                    returnArr.push({name: addCount+val.name, id: val.id, type:val.type})
                    if(val.children.length!=0) {
                        addCount=addCount+"-"
                        findLevel(val.children)
                    } else{addCount=''}
            })
        }

        findLevel(items)  
        return returnArr
    },
    detectRowSise(items){
      var returnArr=[]
      var addCount=''
      function findLevel(obj) {
            obj.forEach((val)=>{
                    returnArr.push({name: addCount+val.name, id: val.id})
                    if(val.children.length!=0) {
                        addCount=addCount+"-"
                        findLevel(val.children)
                    } else{addCount=''}
            })
        }

        findLevel(items)  
        return returnArr.length
    },
    selectedModal(val){
        var price_ids=[]
        if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selected.length+
            ' rows in to '+val.name+"?")) {
            this.selected.forEach((val)=>{
                price_ids.push(val.id)
            })
             axios.get('/cp_mv_to_personal', {
                 params: {
                     price_ids: price_ids.join(),
                     new_menu: val.id,
                     operation: this.moveToCopyRadio,
                     type: this.addFactoryButton?'part':'factory'
                 }
             })
        }
    },
     dragHandler(model, component, e) {
    
    //    // console.log('dragHandler: ', model, component, e);
     },
    
     dragEnterHandler(model, component, e) {
    //    //  console.log('dragEnterHandler: ', model, component, e);
     },
    
     dragLeaveHandler(model, component, e) {
    //    // console.log('dragLeaveHandler: ', model, component, e);
     },
    
     dragOverHandler(model, component, e) {
    //    // console.log('dragOverHandler: ', model, component, e);
     },
    
    dragEndHandler(model, component, e) {
        //console.log('dragEndHandler: ', model, component, e);
        this.drag1=model.id;
        // console.log(this.drag1, this.drag2, this.items_menu);
        var type=[]
        function findLevel(obj, id, i) {
            obj.forEach((val)=>{
                    if (id==val.id){
                      if(val.type.length>2){
                        type[i]=val.type
                      }
                    }
                    else {
                        if(val.children.length!=0) {
                            findLevel(val.children, id, i)
                        }
                    }
            })
        }

       findLevel(this.items_menu, this.drag1, 1)
       findLevel(this.items_menu, this.drag2, 2)
       if ((type[1]=='factory') & (type[2]=='factory') | (type[1] != 'factory')) {
        axios.get('/change_parrent_menu_personal', {
            params: {
                drag1: this.drag1,
                drag2: this.drag2
            }
        }).then(response=>{
            this.drag1=null;
            this.drag2=null;          
        })
        } else{
            alert('You can not subordinate the enterprise department')
        }
    },
    
    dropHandler(model, component, e) {
       // console.log('dropHandler: ', model, component, e);
        this.drag2=model.id;
    }
  },
  
    

      mounted(){
             setTimeout(() => {
        this.$socket.send('getPersonal')
        this.$socket.send('getFilesPersonal')
        this.$options.sockets.onmessage = (data) => (data.data=='getPersonal') ? this.getPersonal(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getFilesPersonal') ? (this.getFilesPersonal()):''
        },1000);
        }

    }
</script>


