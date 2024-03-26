<template>
  <container>
    <b-modal size="md" centered  ref="movedoc" :title="$t('projectDetail.move')">
      <b-form-select class="" v-model="selectedPersonalDoc" :select-size="detectRowSise(itemsMenuDoc)">
        <option v-for="(item, i) in detectItem(itemsMenuDoc)" @click="selectedModal(item)" :key="i">{{item.name}}</option>
      </b-form-select>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveDoc">OK</button> 
      </template>
    </b-modal>
    <b-modal size="lg" centered id="attr" ref="attr" :title="$t('company.selectType')">
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
                    :value="(index!=0)?item.type:'text'" @change="updateRowInTemplate(item.id, $event, 'type')" :options="['text', 'color', 'date', 'datetime', 'datetime-local', 'email', 'number', 'range', 'search', 'tel', 'time', 'url', 'month', 'week', 'switch']"></b-form-select>
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
            {{$t('company.addItem')}}    
          </button>
          <button type="button" class="btn btn-secondary"  @click="removeItemInTemplate(selectedOptFactory)">
            {{$t('company.removeItem')}} 
          </button>
        </b-input-group-append>
        <b-form-input :value="optionsForFactory[optionsForFactory.findIndex(x => x.id == selectedOptFactory)].name"
        @input="updateItemInTemplate(selectedOptFactory, $event)"></b-form-input>
        <b-input-group-append>
          <button type="button" class="btn btn-primary"
          @click="addRowForFactory(optionsForFactory[optionsForFactory.findIndex(x => x.id == selectedOptFactory)].name, selectedOptFactory)">OK</button> 
        </b-input-group-append>
      </template>
    </b-modal>
    <b-modal size="md" centered id="move" ref="movePersonal" :title="$t('projectDetail.move')">
      <b-form-select class="" id="move" v-model="selectedItems" :select-size="detectRowSise(items_menu)">
        <option v-for="item in detectItem(items_menu)" :disabled="addFactoryButton?item.type=='factory':item.type=='part'" @click="selectedModalPersonal(item)">{{item.name}}</option>
      </b-form-select>
      <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="[$t('company.copy'), $t('company.move')]" />
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button> 
      </template>
    </b-modal>
    <container-header class="container-fluid">
      <top-menu></top-menu>
    </container-header>
    <container-body class="container-fluid">
      <b-card-group deck>
        <b-card no-body class="gs-container">
          <b-tabs card>
            <b-tab :title="$t('topMenu.companyData')">
              <container>
                <container-body>
                  <b-container>
                    <b-row>
                      <b-col cols="4" > 
                        <vue-drag-tree
                        :data='items_menu'
                        :allowDrag='allowDrag'
                        :allowDrop='allowDrop'
                        :idNode="idNode"
                        :parId="parId"
                        disableDBClick
                        @current-node-clicked="curNodeClicked"
                        @drag-end="dragEndHandler"
                        @drop="dropHandler">
                        </vue-drag-tree>  
                      </b-col> 
                      <b-col cols="8">

                        <b-table :items="items" :fields="addFactoryButton?fieldsWorkers:fieldsFactory"
                        hover sticky-header no-border-collapse style="max-height:100%" stacked="lg"
                        @row-clicked="inItemGetData" @row-dblclicked="rowSelected" >
                          <template #cell(index)="data">
                            {{ data.index + 1 }}
                          </template>
                          <template #cell(delete)="row">
                            <b-link @click="delRow(row.item.id)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-link>
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
                    <b-button :disabled="addFactoryButton" @click="add('factory')">{{$t('company.addFactory')}}</b-button>
                    <b-button :disabled="idNode==129" @click="add('part')">{{$t('projectDetail.plusPart')}}</b-button>
                    <b-button :disabled="idNode==129" @click="remove">{{$t('projectDetail.remove')}}</b-button>
                  </b-input-group-append>
                  <b-form-input v-model="nameNode" @input="toModel"></b-form-input>
                  <b-input-group-append>
                    <b-button @click="addRow">{{$t('projectDetail.plusRow')}}</b-button>
                      <b-button @click="mv_cp">{{$t('company.mv_cp')}}</b-button>
                  </b-input-group-append>
                </b-input-group>
              </b-card-footer>
          </b-tab>
        </b-tabs>
      </b-card>
      <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab :title="$t('company.details')">
                            <container>
                                <container-body>

 <b-container v-if="(addFactoryButton) && (details.id!=null)">

<b-row>
<b-col sm="6" class="cuestomRow">
<b-form-group horizontal :label-cols="4" class="cForm" label="ID:">
<b-form-input :state="null" disabled type="text" :value="details.id" class="cForm-input" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" :label="$t('project.startDate')+':'">
<b-form-input :state="null" type="date"  :value="details.start_work" placeholder="Enter date" class="cForm-input" @change="updateDate($event, 'start_work', details.id)" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" :label="$t('project.endDate')+':'">
<b-form-input :state="null" type="date"  :value="details.end_work" placeholder="Enter date" class="cForm-input" @change="updateDate($event, 'end_work', details.id)" />
</b-form-group>
</b-col>

<b-col sm="6" class="cuestomRow">
<b-form-group horizontal :label-cols="4" class="cForm" :label="$t('customerDetail.name')+':'">
<b-form-input :state="null" type="text" :value="details.name" placeholder="Enter name" class="cForm-input" @change="updateDate($event, 'name', details.id)" />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" :label="$t('company.shortName')+':'">
<b-form-input :state="null" type="text" :value="details.short_name" placeholder="Enter Short Name" class="cForm-input" @change="updateDate($event, 'short_name', details.id)"  />
</b-form-group>
<b-form-group horizontal :label-cols="4" class="cForm" :label="$t('customerDetail.position')+':'">
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
                                                <b-form-group horizontal :label-cols="4" class="cForm" :label="$t('customerDetail.phone')+': '+(index+1)" v-for="(p, index) in details.phone" :key="p.id">
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
                                                <b-form-group horizontal :label-cols="1" class="cForm"  :label="$t('customerDetail.adress')+': '+(index+1)" v-for="(a, index) in details.adress" :key="a.id">
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


<b-form-checkbox v-if="getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'type', index)=='switch'"
:checked="dataForRows.content==1?true:false" name="check-button" switch class="cForm-input"
@change="updateContent(
$event,
optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length,
inc,
index,
details.id
)" />


<vue-editor  v-if="getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'type', index)=='textarea'"
:value="dataForRows.content" :editorToolbar="customToolbar"
@blur="writecomet(optionsForFactory, details, index, inc)" :ref="'editorId'+getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'id', index)"
/>

<b-input v-if="getDataTamplate(optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds, 'type', index)!='textarea' && getDataTamplate(optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds, 'type', index)!='switch'" :type="getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'type', index)"
:value="dataForRows.content"
class="cForm-input"
@change="updateContent(
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
        {{$t('projectDetail.remove')}}
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
    {{$t('projectDetail.add')}}
</b-button>
</b-input-group>

            </b-card-footer>
             </container>
         </b-tab>
                      

                        <b-tab>
                          <template #title>
                          {{$t('projectDetail.docs')}}
                          </template>
                            <container>
                               <container-body  style="overflow-x: hidden;">
                                <docs
                                ref="presonalDocs"
                                :responseFiles="responseFiles"
                                :fieldsDocs="fieldsDocs"
                                :t="2"
                                :idNodeDoc="idNodeFile"
                                :docsIds="docs_menu_ids"
                                :itemsMenuDoc="itemsMenuDoc"
                                :oldIdDoc="oldIdDoc"
                                :selectedPriceDoc="selectedPriceDoc"
                                :menuDocsTree="menuDocsTree"
                                @filedel="filedel"
                                @updatefilename="updatefilename"
                                @loadDocToFrame="ploadDocToFrame"
                                @onClickOutsideDoc="menuDocsTree=false"
                                @curNodeClickedDoc="pcurNodeClickedDoc"
                                @rowSelectedDoc="prowSelectedDoc"
                                />
                                </container-body>

                <container-footer style="z-index:2">
                  <b-collapse v-model="dropDoc" id="dropDoc3">
                    <vue-dropzone ref="myVueDropzone3" id="dz3" :options="dropzoneFiles" v-on:vdropzone-sending="sendingEvent"
                    v-on:vdropzone-success="fsadd3" :forceFallback="true">
                    </vue-dropzone>
                  </b-collapse>
                  <b-input-group>
                  <template #prepend>
                    <b-button @click="dropDoc=dropDoc?false:true">
                      <b-icon :icon="dropDoc?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                    </b-button>
                    <b-button @click="addDoc">{{$t('projectDetail.plusPart')}}</b-button>
                    <b-button @click="removeDoc" :disabled="(nameNodeDoc=='General Folder')?true:false">{{$t('projectDetail.remove')}}</b-button>
                    <b-button @click="moveDoc">{{$t('projectDetail.move')}}</b-button>
                  </template>
                  <b-form-input v-model="nameNodeDoc" :style="nodeDisDoc?'background-color:grey':''" :disabled="(nameNodeDoc=='General Folder')?true:false"
                  @click.native="nodeDisDoc?nodeDisTurnDoc():''" @change="nodeDisDoc=true;toModelDoc(nameNodeDoc)"></b-form-input>
                  </b-input-group>
                </container-footer>

                            </container>
                        </b-tab>


                        <b-tab v-if="false">

                            <template #title>
                             {{$t('projectDetail.images')}}
                          </template>

                          <container>
                            <container-body  style="overflow-x: hidden;" ref="images">


                 <images
                  :domageImages="responseImages"
                  :fieldsImages="fieldsImages"
                  :selectedDamageImages="selectedDamageImages"
                  :optImages="optImages"
                  @resetFilds="presetFilds"
                  @chvalueimages="pchvalueimages"
                  @updatefilename="updatefilename"
                  @showx="showx"
                  @filedel="filedel"
                  @selectimagesarr="pselectimagesarr"
                  @allselrow="pallselrow"
                  @allselrowin="pallselrowin"
                  @imageInTableSelected="pimageInTableSelected"
                  ></images>

                            </container-body>



              <container-footer style="z-index:2">
                  <b-collapse v-model="dropImage" id="dropImage4">
                    <vue-dropzone ref="myVueDropzone2" id="dz2"
                    :options="dropzoneImages" v-on:vdropzone-sending="sendingEvent"
                    v-on:vdropzone-success="fsadd2" :forceFallback="true">
                    </vue-dropzone>
                  </b-collapse>
                  <b-button @click="dropImage=dropImage?false:true">
                    <b-icon :icon="dropImage?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                  </b-button>
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

                      customToolbar: [
                      [{ list: "check" }],
                ['bold', 'italic', 'underline', 'strike'],        
                [{ 'color': [] }, { 'background': [] }],   
                [{ 'align': [] }],
              ], 
                idNodeFile:-1,
                docs_menu_ids:[],
                itemsMenuDoc:[],
                oldIdDoc:0,
                selectedPriceDoc:[],
                menuDocsTree: false,
                nameNodeDoc:null,
                nodeDisDoc:true,

                selectedPersonalDoc:[],

                dropImage:true,
                optImages:[],
                selectedDamageImages:'Image',
                domageImages:[],
                dropDoc:true,
                selectedOptFactory:null,
                optionsForFactory:[

                ],

                files:[],

      dropzoneFiles: {
        url: '/loadFilesToCompany',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'application/pdf'
      },

      dropzoneImages: {
        url: '/loadFilesToCompany',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'image/*'
      },

            responseFiles: [],
            responseImages: [],
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
          items_menu:[],
          drag1: null,
          drag2: null
    }

  },
   computed: {
    fieldsDocs(){
      return[
      {
        key: 'type',
        label: this.$t('docs.file'),
        sortable: true
      },
      {
        key: 'name',
        label: this.$t('docs.name'),
        sortable: true
      },
      {
        key: 'number',
        label: '#',
        sortable: true
      },
      {
        key: 'added',
        label: this.$t('docs.added'),
        sortable: true
      },
      {
        key: 'user',
        label: this.$t('docs.user'),
        sortable: true
      },
      {
        key: 'delete',
        label: this.$t('docs.delete')
      }]},

      fieldsImages(){
      return[{   
        key: 'id',
        label: this.$t('docs.images'),
        sortable: true
      },
      {
        key: 'file_name',
        label: this.$t('docs.name'),
        sortable: true
      },
      {
        key: 'date',
        label: this.$t('docs.added'),
        sortable: true
      },
      {
        key: 'user',
        label: this.$t('docs.user'),
        sortable: true
      },
      {
        key: 'delete',
        label: this.$t('docs.delete')
      }]},

    fieldsWorkers(){
      return[{
          key: 'index',
          label: '#'
        },
        {
          key: 'name',
          label: this.$t('customerDetail.name'),
          sortable: true
        },
        {
          key: 'position',
          label: this.$t('customerDetail.position'),
          sortable: true
        },
        {
          key: 'delete',
          label: this.$t('docs.delete')
        }]},
    fieldsFactory(){
      return[{
          key: 'index',
          label: '#'
        },
        {
          key: 'name',
          label: this.$t('company.propsName'),
          sortable: true
        },
        {
          key: 'delete',
          label: this.$t('docs.delete')
        }]}
  },
    methods: {
      writecomet(optionsForFactory, details, index, inc){
      var newContent =  this.$refs['editorId'+this.getDataTamplate(optionsForFactory[optionsForFactory
.findIndex(x => x.id == details.option)].filds, 'id', index)][0].quill.getHTML()
        if (newContent != '<p><br></p>') {
          this.updateContent(
          newContent,
          optionsForFactory[optionsForFactory.findIndex(x => x.id == details.option)].filds.length,
          inc,
          index,
          details.id
          )
        }
      },
    pcurNodeClickedDoc(model, component) {
      this.nameNodeDoc = model.name
      this.idNodeFile=model.id
      this.oldIdDoc = this.idNodeFile 
        if ((model.parrent == 0) && component.folder == false){
          this.idNodeFile = null
        }
    },
    prowSelectedDoc(items) {
      if(this.selectedPriceDoc.indexOf(items)==-1){
        this.selectedPriceDoc = this.selectedPriceDoc.filter((v)=>{
          if (v.id != items.id){
            return v
          }
        });
        this.selectedPriceDoc.push(items);
        items._rowVariant='success';
      } else {
        this.selectedPriceDoc.splice(this.selectedPriceDoc.indexOf(items), 1)
        items._rowVariant=''
      }
    },
      addDoc(){
      function findLevel(obj, id, project) {
        if (id==null){
          id=0,
          obj.push({id:0, children:[]})
        }
        obj.forEach((val)=>{
          if (val.id==id){
            axios.get('/add_docs_personal_menu', {
              params: {
                parent_id: val.id,
                project: project
              }
            })
          } else {
            if (val.children.length!=0) {
              findLevel(val.children, id, project)
            }
          }
        })
      }
      findLevel(this.itemsMenuDoc, this.idNodeFile, this.details.id)
    },  
    removeDoc(){
      if (this.idNodeFile==null){
        alert(this.$t('alert.noItemSelectForDel'))
      }
      else {
        if (confirm(this.$t('alert.remove'))) {
          axios.get('/remove_docs_personal_menu', {
            params: {
              remove_id: this.idNodeFile
            }
          }).then(response=>{
            this.idNodeFile=null,
            this.nameNodeDoc=null
          })
        }
      } 
    },
    moveDoc(){
      this.$refs.movedoc.show()
    },
    okMoveDoc(){
      this.selectedPriceDoc=[],
      this.$refs.movedoc.hide()
    },
    nodeDisTurnDoc(){
      if (confirm(this.$t('alert.rename'))) {
        this.nodeDisDoc = false
      }
    },
    toModelDoc(enterVal){
      function findLevel(obj, id) {
        obj.forEach((val)=>{
          if (val.id==id){
            axios.get('/update_name_docs_personal_menu', {
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
      findLevel(this.itemsMenuDoc, this.idNodeFile)
    },
    selectedModal(val){
      console.log(1)
      var docs_ids=[]
      var files_ids=[]
      this.selectedPriceDoc.forEach((val)=>{
          files_ids.push(val.id)
      })
      axios.get('/mv_files_company', {
        params: {
          files_ids: files_ids.join(),
          new_menu: val.id
        }
      }).then(response=>{
        setTimeout(() => {
          this.getPersonal()
        }, 20);
      })                      
    },

getFilesPersonal(id){
      axios.get('/docs_personal_menu', {
        params: {
          project:id
        }
      }).then(response => {
        this.itemsMenuDoc=[];
        this.itemsMenuDoc.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
        this.docs_menu_ids.push(-1);
        response.data.forEach((val)=>{
          if (val.parrent==0){
            val['children']=[]
            this.itemsMenuDoc.push(val);
          }
        });
        response.data.forEach((valResp)=>{
          function findLevel(obj, id)  {
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
          this.docs_menu_ids.push(valResp.id);
          findLevel(this.itemsMenuDoc, valResp.parrent) 
        });
        this.responseFiles=[];
        axios.get('/get_files_company', {
          params: {
            id: id
          }
        }).then(response => {
          this.responseFiles = response.data.filter(function (v){
            if(v.name != undefined){
              if((v.name.split('.')[v.name.split('.').length-1]) == 'pdf'){ return v}
            }
          })
          this.responseImages = response.data.filter(function (v){
            if(v.file_name != undefined){
                return v
            }
          })
        })
      })
    },


      butifsel(){
          var detectState = 0
         this.domageImages.forEach(function(v){
            if (v._rowVariant!='') detectState = detectState + 1
         })
         return (detectState>0)
      },
pimageInTableSelected(item){
  item._rowVariant=(item._rowVariant=='secondary')?'':'secondary';
},

     showx(classId, index){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.index = index
      viewer.show()
    },       
    pallselrow(){
      this.domageImages.forEach((v)=>{
          v._rowVariant='secondary'
      })
    },
    pallselrowin(table){
      table.forEach((v)=>{
          v._rowVariant='secondary'
      })
    },

    presetFilds(){
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].tdClass=''
        this.domageImages.forEach((v)=>{
          v._rowVariant=''
        })
    },
      pchvalueimages(val){
  this.selectedDamageImages=val
},
pselectimagesarr(group){
var imagesarr = []
if (this.selectedDamageImages=='Image'){
  this.domageImages.forEach((si)=>{
    if(si._rowVariant=='secondary'){
       imagesarr.push(si.id.split('=')[1])
    }
  })
  this.updatefilenames(group, 'group',imagesarr.join())
}
console.log(this.groupByFild(this.selectedDamageImages))
  if (op=='-'){
    this.selectedImages.splice(this.selectedImages.indexOf(it), 1)
  }
},  

        fsadd2() {
                this.$refs.myVueDropzone2.removeAllFiles()
        },
        fsadd3() {
                this.$refs.myVueDropzone3.removeAllFiles()
        },
        sendingEvent(file, xhr, formData) {


      xhr.setRequestHeader('X-Number', this.details.id);
      xhr.setRequestHeader('X-Folder', this.idNodeFile);
      xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
        },

        filedel(val) {
            if (confirm(this.$t('alert.sure'))) {
                axios.get('/delfile_company', {
                    params: {
                        id: val
                    }
                }).then(response => {});
            }
        },
    updatefilename(val, type, id){
        axios.get('/updatefilename_company', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        })
    },


        ploadDocToFrame(row) {
            row.toggleDetails();
            var index = row.index;
            if (row.detailsShowing == false) {
                setTimeout(() => {
                  this.$refs.presonalDocs?this.$refs.presonalDocs.$refs['ifrForm' + index].submit():''
                }, 50);
            }
        },


    blocks(arr, l, befor){
        befor = befor + 1
        var retArr=[]

        for (var i = (l*befor)-l; i < (l*befor); i++) {
            retArr.push(arr[i])
        }
        return retArr

    },
    getDataTamplate(v, type, i){

    var x = i

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

    addContactInPerson(fild, action, index){
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
    
       inItemGetData(item){
       
            this.details = item,
          
            this.getFilesPersonal(this.details.id)


       },
       getPersonal(){
        this.items = [] 
        if (this.idNode!=null){
            axios.get('/personals', {
                params: {
                    id: this.idNode,
                    type: this.addFactoryButton?'part':'factory'
                }
            }).then(response => {
                if (this.addFactoryButton==true){
                 
                this.items = response.data.filter((v, i)=>{
                
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
            })
         
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


          var id = 0
            if (this.idNode != null) {
                id = this.idNode
                if (this.details.id != null) {
                    if (this.details.id != null) {
                        id = 'personal-' + this.details.id
                    }
                }
            }
             

        },
    
    allowDrag(model, component) {
      if (model.name === 'Node 0-1') {
        return false;
      }
      return true;
    },
    
    allowDrop(model, component) {
      if (model.name === 'Node 2-2') {
        return false;
      }
      return true;
    },
     allowDragModal(model, component) {
        return false;
    },
    
    allowDropModal(model, component) {
        return false;
    },   
 
curNodeClicked(model, component) { 
    this.addFactoryButton = (model.type!='factory'),
        this.nameNode = model.name,
        this.idNode=model.id,
        this.details.id=null,
        this.parId = model.parrent

        this.getPersonal()

     
    },

    curNodeClickedModal(model, component){
        this.idNodeModal=model.id
    },
    toModel(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
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
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
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
            alert(this.$t('alert.noSelectedForAdd'))
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
        if (confirm(this.$t('alert.remove'))) {
            axios.get('/remove_personal', {
                params: {
                    id: id,
                    type: this.addFactoryButton?'part':'factory'
                }
            })
        }
    },
    updateDate(data, fild, id, type){
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
            alert(this.$t('alert.noItemSelect'))
        } else{
            if (this.selected.length==0){
                alert(this.$t('alert.noRowsSelected'))
            }
        }
        if ((this.idNode!=null)&&(this.selected.length!=0)){
            this.$refs.movePersonal.show()           
        }
    },
    okMoveToCopy(){
        this.selected=[],
        this.$refs.movePersonal.hide()
    },
    detectItem(items){
      var returnArr=[]
      var addCount=''
      function findLevel(obj) {
            obj.forEach((val)=>{
                    returnArr.push({name: addCount+val.name, id: val.id, type:val.type})
                    if(val.children.length!=0) {
                        addCount=addCount
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
    selectedModalPersonal(val){
        var price_ids=[]
        if (confirm(this.$t('alert.to')+" "+this.moveToCopyRadio+' '+this.selected.length+
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
     
    dragEndHandler(model, component, e) {
        this.drag1=model.id;
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
            alert(this.$t('alert.youCanNotSubordinateTheEnterpriseDepartment'))
        }
    },
    
    dropHandler(model, component, e) {
        this.drag2=model.id;
    }
  },
  
    

      mounted(){
        this.getPersonal()
        this.$options.sockets.onmessage = (data) => (data.data=='getPersonal') ? this.getPersonal(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getPersonalFiles') ? (this.getFilesPersonal(this.details.id)):''

        }

    }
</script>
