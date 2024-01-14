<template>
<container>
  <input ref="unfocus" style="width: 0px; height: 0px; position: absolute; top: 0; left: 0; margin:0; padding:0; border: 0;"></input>
<!--     <b-modal size="md" centered id="move" ref="move" title="Move">
        // @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" //
         <b-form-select class="" id="move" v-model="selectedItems" :select-size="detectRowSise(itemsMenu)">
            <option v-for="item in detectItem(itemsMenu)" @click="selectedModal(item)">{{item.name}}</option>
         </b-form-select>

         <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['move', 'copy']" />
         <template slot="modal-footer">
        //<button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>//
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button> 
         </template>
      </b-modal> -->

    <b-modal size="md" centered  ref="movedoc" :title="$t('projectDetail.move')">
         <b-form-select class="" v-model="selectedItems" :select-size="detectRowSise(itemsMenuDoc)">
            <option v-for="(item, i) in detectItem(itemsMenuDoc)" @click="selectedModalDoc(item)" :key="i">{{item.name}}</option>
         </b-form-select>

         <template slot="modal-footer">
            <button type="button" class="btn btn-primary" @click="okMoveDoc">OK</button> 
         </template>
      </b-modal>

    <b-modal size="md" centered  ref="moveImag" :title="$t('projectDetail.move')">
         <b-form-select class="" v-model="selectedItems" :select-size="detectRowSise(itemsMenuImag)">
            <option v-for="(item, i) in detectItem(itemsMenuImag)" @click="selectedModalImag(item)" :key="i">{{item.name}}</option>
         </b-form-select>

         <template slot="modal-footer">
            <button type="button" class="btn btn-primary" @click="okMoveImg">OK</button> 
         </template>
      </b-modal>

<b-modal size="sm" centered  :title="$t('projectDetail.selectWorkers')" body-class="workerHeight" v-model="workerModal"  no-close-on-esc no-close-on-backdrop hide-header-close>
    <b-form-input type="text" v-model="searchWorker" style="margin-bottom: 4px !important;" />
    <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="availableWorkers" />
            <template slot="modal-footer">
                  <b-container fluid>
                    <b-row  align-h="between">
                      <b-col class="text-left">
                        <b-button type="button" variant="primary" @click="selectedWorkers=[]">{{$t('projectDetail.clear')}}</b-button>
                      </b-col>
                      <b-col class="text-right">
                        <b-button type="button" variant="primary" @click="closeWorkerModal">OK</b-button>
                      </b-col>
                    </b-row>
                  </b-container>
           </template>
        </b-modal>

<b-modal size="lg" centered ok-only id="map" :title="$t('projectDetail.track')"  v-model="mapmodal" no-close-on-esc no-close-on-backdrop hide-header-close>
  <b-embed type="iframe" aspect="16by9"
    :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
    'origin='+addressfild+'&'+
    'destination='+(project.street1+', '+project.zip1+' '+project.city1).replace('undefined', '')"
    >
  </b-embed>
<template slot="modal-footer">
<b-button type="button" variant="outline-secondary"  @click="mapmodalhide">{{$t('projectDetail.close')}}</b-button>
</template>
</b-modal>

          <!-- <b-form @submit.prevent="addOk"> -->
            <b-modal size="md" centered  v-model="addSameModalWindow" :title="$t('projectDetail.addOffers')"  no-close-on-esc no-close-on-backdrop hide-header-close>
<!--                 <b-form-group horizontal :label-cols="4" label="Order #:" label-for="OrderNumber" style="padding: 5px;">
                    <b-form-input v-model="project.number" class="cForm-input" id="OrderNumber" disabled :state="null" type="text" placeholder="Enter number" />
                </b-form-group> -->
                <b-form-group horizontal :label-cols="4" :label="$t('projectDetail.typeOfWork')+':'" label-for="work" style="padding: 5px;">
                    <b-form-select class="select" id="work" :options="works" v-model="add_offer.work" required />
                </b-form-group>
                <template slot="modal-footer">
                  <b-container fluid>
                    <b-row  align-h="between">
                      <b-col class="text-left">
                        <b-button @click="closeaddok" variant="primary">
                            {{$t('projectDetail.close')}}
                        </b-button>
                      </b-col>
                      <b-col class="text-right">
                        <b-button type="submit" variant="primary" @click="addOk">
                            {{$t('projectDetail.add')}}
                        </b-button>
                      </b-col>
                    </b-row>
                  </b-container>
                </template>
            </b-modal>
        <!-- </b-form> -->
  <b-modal size="xl" v-model="mailmodal" no-close-on-esc no-close-on-backdrop hide-header-close>
          <b-row>
            <b-col cols="12" md="4">
              <b-form-checkbox-group buttons text-field="name" value-field="item"  v-model="mailSelect"
              stacked style="width:100%" class="cheboxscorl" :options="filtered(((abook==false)?modalMail:abooklist),searchmail)" />
              <b-input-group>
              <b-form-input type='text' :placeholder="$t('projectDetail.esearchMailAdress')" v-model="searchmail" />
                <b-input-group-append>
                   <b-form-checkbox button
                      stacked
                      @change="cheabook"
                      v-model="abook" 
                      >{{$t('projectDetail.addressBook')}}
                    </b-form-checkbox>
                  </b-input-group-append>
              </b-input-group>
            </b-col>
            <b-col cols="12" md="8"><div class="cheboxscorl">
              <b-form-checkbox-group buttons text-field="name" value-field="item"
              button-variant="light" v-model="selectedFiles"
              stacked style="width:100%"
              :options="filtered(modalFiles, searchfile)" />
                </div>
              <b-form-input type='text' :placeholder="$t('projectDetail.searchNameOfFile')" v-model="searchfile" />
            </b-col>
          </b-row>
          <br>
            <b-form-input type='text' :placeholder="$t('projectDetail.subject')" v-model="subject" />
<vue-editor id="content" ref="content" class="mail" v-model="content" :editorToolbar="customToolbar" />
  <template slot="modal-footer">
    <b-form inline>
    <b-button type="button" @click="mailmodalhide">{{$t('projectDetail.close')}}</b-button>
    <b-form-checkbox button v-if="(selectedFiles && selectedFiles.length ? selectedFiles.length : 0)>=2"
    stacked @change="checkattach('chek')" v-model="split">{{$t('projectDetail.split')}}
    </b-form-checkbox>
    <b-form-input type="text" v-model="filename" @input="checkattach('inp')"
    :placeholder="$t('projectDetail.nameOfSingleAttachment')" v-if="(selectedFiles && selectedFiles.length ? selectedFiles.length : 0)>=2"></b-form-input>
    <b-button :disabled="(mailSelect.length==0)"  @click="sendmail()" >{{$t('projectDetail.send')}}</b-button>
  </b-form>
  </template>
</b-modal>


  <b-modal size="lg" v-model="timetableMailModal" no-close-on-esc no-close-on-backdrop hide-header-close>
          <b-row>
            <b-col cols="12" md="6">
              <b-form-checkbox-group buttons text-field="name" value-field="item"  v-model="mailSelectPlan"
              stacked style="width:100%" class="cheboxscorl" :options="filtered(((abook==false)?modalMail:abooklist),searchmail)" />
              <b-input-group>
              <b-form-input type='text' :placeholder="$t('projectDetail.esearchMailAdress')" v-model="searchmail" />
                <b-input-group-append>
                   <b-form-checkbox button
                      stacked
                      @change="cheabook"
                      v-model="abook" 
                      >{{$t('projectDetail.addressBook')}}
                    </b-form-checkbox>
                  </b-input-group-append>
              </b-input-group>
            </b-col>

            <b-col cols="12" md="6" class="text-center">
              <b-col class="text-center">{{$t('projectDetail.delivery')}}:</b-col>
              <br>
              <div v-if="(cheatypedate==null)?(!Number.isNaN(Number(selectedDateForSend))):cheatypedate">
              <b-form-radio-group buttons 
              button-variant="light" v-model="selectedDateForSend"
               style="width:100%"
              :options="[1,2,3,4,5,6,7]" />

              <b-form-radio-group buttons 
              button-variant="light" v-model="selectedDateForSend"
               style="width:100%"
              :options="[8,9,10,11,12,13,14]" />

              <b-form-radio-group buttons 
              button-variant="light" v-model="selectedDateForSend"
               style="width:100%"
              :options="[15,16,17,18,19,20,21]" />

              <b-form-radio-group buttons 
              button-variant="light" v-model="selectedDateForSend"
               style="width:100%"
              :options="[22,23,24,25,26,27,28]" />
              </div>
              <div v-if="(cheatypedate==null)?(Number.isNaN(Number(selectedDateForSend))):!cheatypedate">
              <b-form-radio-group buttons 
              button-variant="light" v-model="selectedDateForSend"
              stacked style="width:100%"
              :options="monthpart" />
              </div>
              <br>
            <b-row  align-v="center" align-h="around">
            <b-form-checkbox button
            stacked :checked="(cheatypedate==null)?(!Number.isNaN(Number(selectedDateForSend))):cheatypedate"
              @change="(cheatypedate=$event);pushToWorkDays=($event==true)?false:pushToWorkDays"

            >{{$t('projectDetail.mothToDays')}}
            </b-form-checkbox>

            <b-form-checkbox button
            stacked 
            v-model="pushToWorkDays" v-if="(cheatypedate==null)?(Number.isNaN(Number(selectedDateForSend))):!cheatypedate"
            >{{$t('projectDetail.pushToWorkDays')}}
            </b-form-checkbox>
            </b-row>
            </b-col>

          </b-row>
          <br>
            <b-form-input type='text' :placeholder="$t('projectDetail.subject')" v-model="subjectPlan" />
<vue-editor id="contentPlan" ref="contentPlan" class="mail" v-model="contentPlan" :editorToolbar="customToolbar" />
  <template slot="modal-footer">
<b-container>
  <b-row align-v="center" align-h="between">
    <b-col cols="4">
      <b-form-checkbox switch v-model="autoSend">
        {{autoSend?$t('projectDetail.autoSend'):$t('projectDetail.notAutoSend')}}
      </b-form-checkbox>
    </b-col>
    <b-col cols="4">
      <b-form-checkbox switch @change="selperiodFinishWork=!autoDate?null:selperiodFinishWork" v-model="autoDate">
        {{autoDate?$t('projectDetail.autoDate'):$t('projectDetail.notAutoDate')}}
      </b-form-checkbox>
    </b-col>
    <b-col cols="4">
      <b-form-radio-group
        :disabled="!autoDate"
        v-model="selperiodFinishWork"
        :options="periodFinishWork"
      ></b-form-radio-group>
    </b-col>
  </b-row>

  <b-row align-v="center" align-h="between">
    <b-col cols="2">
      <b-button type="button" @click="timetableMailModalHide">
        {{$t('projectDetail.close')}}
      </b-button>
    </b-col>
    <b-col cols="2">
      {{$t('projectDetail.nameOfInvoice')+':'}}
    </b-col>
    <b-col cols="3">
      <b-form-input type="text" v-model="filename"></b-form-input>
    </b-col>
    <b-col cols="2" v-if="(detectPeriod!=null)">
      <b-button :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
      @click="sendtimetablemail('remove_mail')" variant="danger" >
        {{$t('projectDetail.removeplaning')}}
      </b-button>
    </b-col>
    <b-col cols="3" v-if="(detectPeriod!=null)">
      <b-button :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
      @click="sendtimetablemail('replan_mail')" variant="primary" >
        {{$t('projectDetail.replaning')}}
      </b-button>
    </b-col>
    <b-col cols="3" v-if="(detectPeriod==null)">
      <b-button :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
      @click="sendtimetablemail('plan_mail')" variant="success" >
        {{$t('projectDetail.planing')}}
      </b-button>
    </b-col>
  </b-row>
</b-container>
  </template>
</b-modal>



        <container-header class="container-fluid">
            <top-menu>
            </top-menu>
        </container-header>
        <container-body class="container-fluid" >
            <b-card-group deck>
                <b-card no-body class="gs-container" :style="heightComponentforSm">
                    <b-tabs card v-model="tabIndex"  class="tabs">
                        <b-tab>
                        <template #title>
                            
                            <span v-if="project.number==undefined">{{projectfild.content}}</span>
                            <span v-else :title="projectfild.content+' '+project.number">{{project.number}}</span>
          
                        </template>
                        <container>
                          <container-body  ref="project">
                              <b-container ref="hproject">
                               <project
                                :dislink="!(selectedTables.length<=1)"
                                :projectfild="projectfild"
                                :project="project"
                                :id="id"
                                :typesForTables="typesForTables"
                                :area="area"
                                :availablePersons="availablePersons"
                                :availablePhons="availablePhons"
                                :availableMails="availableMails"
                                :countries="countries"
                                :looks="looks"
                                :tmp="tmp"
                                :workersForSend="workersForSend"
                                :selectCustomer="selectCustomer"
                                :selectPerson="selectPerson"
                                :selectMail="selectMail"
                                :selectPhone="selectPhone"
                                :itemsTable="itemsTable" 
                                :selectedCornty="selectedCornty"
                                :responseFiles="responseFiles"
                                :selrow="selrow"
                                :showsubarr="showsubarr"
                                ref="calProject"
                                @linkForWorkers="linkForWorkers"
                                @addSameModal="addSameModal"
                                @sendMail="sendMail"
                                @openmap="mapmodalshow"
                                @offerDel="pofferDel"
                                @inItemGetData="pinItemGetData"
                                @getcontact="pgetcontact"
                                @getperson="pgetperson"
                                @showCommetnts="showCommetnts()"
                               ></project>
                             </b-container>
                            </container-body>
                        </container>
                        </b-tab>
                        <b-tab style="padding:0px;"  >
                        <template #title>
                            {{$t('projectDetail.priceList')}}
                            <!-- <b-link @click="menuPriceTree=menuPriceTree?false:true">Price List</b-link> -->
                          </div>
                        </template>
                        <container>
                          <container-body>
                              <price v-if="(tabIndex==1) && (comtomodal!='pricelist')"
                              @loded="loded"
                              ref="priceChild1"
                              :menuPriceTree="menuPriceTree"
                              :idNode="idNode"
                              :items="itemsPrice"
                              :itemsMenu="itemsMenu"
                              :oldId="oldId"
                              :selectedPrice="selectedPrice"
                              @curNodeClicked="pcurNodeClicked"
                              @rowSelected="prowSelected"
                              ></price>
                          </container-body>
                <container-footer style="overflow: hidden;">
                        <b-input-group>
                            <b-button @click="addPrice">{{$t('projectDetail.plusPart')}}</b-button>
                            <b-button @click="removePrice">{{$t('projectDetail.remove')}}</b-button>
                            <b-button @click="addRowPrice">{{$t('projectDetail.plusRow')}}</b-button>
                            <!-- <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="mv_cpPrice">mv/cp</b-button></b-col> -->

                            <b-button  @click="sendPrice" :disabled="selectedTables.length<=0">{{$t('projectDetail.send')}}</b-button>
                              <b-button  @click="$refs.priceChild1.hidePosition()" >
                                <b-icon icon="layout-three-columns" aria-hidden="true"></b-icon>
                                <!-- <i class="fas fa-columns"></i> -->
                              </b-button>
                           <b-form-input  v-model="nameNode" :style="nodeDis?'background-color:grey':''"
                                @click.native="nodeDis?nodeDisTurn():''" @change="nodeDis=true;toModel(nameNode)"></b-form-input>
                            
                            
                       </b-input-group>
                </container-footer>
         

                          </container>
                        </b-tab>
<b-tab style="padding:0px;"  >
                        <template #title>
                            {{$t('projectDetail.devicesList')}}
                            <!-- <b-link @click="menuDevicesTree=menuDevicesTree?false:true">Devices List</b-link> -->
                            </div>
                        </template>
                        <container>
                          <container-body>
                            <devices v-if="(tabIndex==2) && (comtomodal!='deviceslist')"
                            @loded="loded"
                            ref="devChild1"

                            :idNodeDev="idNodeDev"
 
                            :itemsDev="itemsPriceDev"
                            :itemsMenuDev="itemsMenuDev"
                            :oldIdDev="oldIdDev"
                            :selectedPriceDev="selectedPriceDev"
                            :menuDevicesTree="menuDevicesTree"

                       
                            @curNodeClickedDev="pcurNodeClickedDev"
                            @rowSelectedDev="prowSelectedDev"

                            ></devices>
                                 <!-- @onClickOutsideDev="menuDevicesTree=false" -->
                          </container-body>
                        <container-footer>
                          <b-input-group>
                             <b-button @click="addDevice">{{$t('projectDetail.plusPart')}}</b-button>
                             <b-button @click="removeDevice">{{$t('projectDetail.remove')}}</b-button>
                             <b-button @click="addRowDevice">{{$t('projectDetail.plusRow')}}</b-button>
                             <!--  <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="mv_cpDevice">mv/cp</b-button></b-col> -->
                              <b-button @click="sendDevice">{{$t('projectDetail.send')}}</b-button>
                              
                              <b-button @click="$refs.devChild1.hidePosition()" >
                                <b-icon icon="layout-three-columns" aria-hidden="true"></b-icon>
                                <!-- <i class="fas fa-columns"></i> -->
                              </b-button>
                                               
                              <b-form-input v-model="nameNodeDev" :style="nodeDisDev?'background-color:grey':''"
                                  @click.native="nodeDisDev?nodeDisTurnDev():''" @change="nodeDisDev=true;toModelDev(nameNodeDev)"></b-form-input>
                            
                              
                          </b-input-group>


                        </container-footer>
         

                          </container>
                        </b-tab>
                        <b-tab>
                          <template #title>
                              <!-- <b-link @click="menuDocsTree=menuDocsTree?false:true">Docs</b-link> -->
                              {{$t('projectDetail.docs')}}
                          </template>
                            <container>
                               <container-body style="overflow: hidden;">                    
                                    <docs v-if="detect('docs')"
                                    @loded="loded"
                                    ref="docs2"
                                    :responseFiles="responseFiles"
                                    :fieldsDocs="fieldsDocs"
                                    :t="2"
                       
                                    @filedel="filedel"
                                    @updatefilename="updatefilename"
                                    @updatedocname="updatedocname"
                                    @changeDisable="changeDisable"
                                    @loadDocToFrame="ploadDocToFrame"

                                    :idNodeDoc="idNodeDoc"
                                    :docsIds="docs_menu_ids"
                                    :itemsDoc="itemsPriceDoc"
                                    :itemsMenuDoc="itemsMenuDoc"
                                    :oldIdDoc="oldIdDoc"
                                    :selectedPriceDoc="selectedPriceDoc"
                                    :menuDocsTree="menuDocsTree"
                                   
                                    @curNodeClickedDoc="pcurNodeClickedDoc"
                                    @rowSelectedDoc="prowSelectedDoc"
                            

                                    >
                                    </docs>
 <!-- @onClickOutsideDoc="menuDocsTree=false" -->
                                </container-body>
                                


                        <container-footer style="z-index:2">
                                    <b-collapse v-model="dropDoc" id="dropDoc3">
                                        <vue-dropzone ref="myVueDropzone3" id="dz3" :options="dropzoneOptions1" v-on:vdropzone-sending="sendingEvent"
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
                              <b-form-input  v-model="nameNodeDoc" :style="nodeDisDoc?'background-color:grey':''"
                              :disabled="(nameNodeDoc=='General Folder')?true:false"
                                  @click.native="nodeDisDoc?nodeDisTurnDoc():''" @change="nodeDisDoc=true;toModelDoc(nameNodeDoc)"></b-form-input>
                                </b-input-group>
                        </container-footer>

                            </container>
                        </b-tab>


                        <b-tab>

                            <template #title>
                              {{$t('projectDetail.images')}}
                            </template>

                          <container>
                            <container-body style="overflow: hidden;">

                             <images
                              v-if="detect('images')"
                              :domageImages="domageImages"
                              ref="images1"
                              :wwidth="wwidth"
                              :idNodeImg="idNodeImg"
                              :itemsMenuImag="itemsMenuImag"
                              :selectedPriceImg="selectedPriceImg"
                              @imageInTableSelected="prowSelectedImg"
                              @pcurNodeClickedImg="pcurNodeClickedImg"
                              @filedel="filedel"
                              @showx="showx"
                              @loded="loded"
                             ></images>
                             <!-- @updatefilename="updatefilename" -->

                            </container-body>
                            <container-footer style="z-index:2">
                              <b-collapse v-model="dropImage" id="dropImage2">
                                <vue-dropzone ref="myVueDropzone2" id="dz2"
                                :options="dropzoneOptions2" v-on:vdropzone-sending="sendingEventImage"
                                v-on:vdropzone-success="fsadd2" :forceFallback="true" />
                              </b-collapse>
                              <b-input-group>
                                <template #prepend>
                                  <b-button @click="dropImage=dropImage?false:true">
                                    <b-icon :icon="dropImage?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                                  </b-button>
                                  <b-button @click="addImag">{{$t('projectDetail.plusPart')}}</b-button>
                                  <b-button @click="removeImag" :disabled="(nameNodeDoc=='General Folder')?true:false">{{$t('projectDetail.remove')}}</b-button>
                                  <b-button @click="moveImag">{{$t('projectDetail.move')}}</b-button>
                                </template>
                                <b-form-input  v-model="nameNodeImag" :style="nodeDisImag?'background-color:grey':''"
                                :disabled="(nameNodeImag=='General Folder')?true:false"
                                @click.native="nodeDisImag?nodeDisTurnImag():''" @change="nodeDisImag=true;toModelImag(nameNodeImag)" />
                                <b-button v-show="butifsel()" @click="sendtodamage()">{{$t('projectDetail.send')}}</b-button>
                              </b-input-group>
                            </container-footer>
                          </container>
                        </b-tab>
                    </b-tabs>
                </b-card>
                <b-card no-body class="gs-container" :style="heightEditforSm">
                    <b-tabs card v-model="dubTabIndex">
                        <b-tab ref="Edit">
                          <template #title>
                            {{tmp.typeOfHead?$t('oneCountAlret.'+tmp.typeOfHead):$t('fields.other')}}
                          </template>
                            <container>
                                <container-body>
                                  <edit ref="editList"
                                  :tmp="tmp"
                                  :project="project"
                                  :looks="looks"
                                  :works="works"
                                  @loded="loded"
                                  :selectedCornty="selectedCornty"
                                  :id="id"
                                  :comments="comments"
                                  :responseFiles="responseFiles"
                                  :typesForTables="typesForTables"
                                  :workers="workers"
                                  :funcStop="funcStop"

                                  :plan="plan"
                                  :partx="partx"
                                  :customer="customer"
                                  :person="person"
                                  :selectCustomer="selectCustomer"
                                  :selectPerson="selectPerson"
                                  :selectedWorkers="selectedWorkers"

                                  :windowPrint="windowPrint"
                                  :selectedDocsList="selectedDocsList"
                                  :addPdfs="addPdfs"
                                  :makemodalpdf="makemodalpdf"
                                  :typeDocsList="typeDocsList"

                                  :availableMails="availableMails"
                                  @sendMail="sendTimeTableMail"
                                  @seltable="seltable"
                                  @projectOther="projectOther"
                                  @selectedDocs="selectedDocs"
                                  @addPdf="addPdf"
                                  @printPdf="printPdf"
                                  @preview="preview"
                                  @printOffer="printOffer"

                                  @worker="worker"
                                  @hideWindowPrint="hideWindowPrint"
      
                                  @tabletopartx="tabletopartx"
                                  @countDigitals="countDigitals"
                                  ></edit>
                                </container-body>
                                <container-footer v-if="(generalComments==false)" :style="openEditor?'margin-top:-26px':''">
                                  
                               
                                       



<!-- 

<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
@mouseover="cloudHover = true" @mouseleave="cloudHover = false"
@click="writecomet();changeDisable('b', 'gencooment', id);cloudChange=false;cloudLoad=true;" v-if="(tmp.number==null)">
  <b-icon stacked icon="circle-fill" :animation="cloudLoad?'throb':null" variant="primary" v-show="cloudLoad||cloudHover"></b-icon>
  <b-icon stacked icon="cloud-upload" scale="0.5" :variant="cloudHover?'light':'dark'" v-show="!cloudLoad"></b-icon>
  <b-icon stacked icon="circle" variant="info" v-show="cloudChange"></b-icon>
</b-iconstack>

<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
@click="checkInEditor('other')" v-if="(tmp.number==null)" @mouseover="calcHover = true" @mouseleave="calcHover = false">
  <b-icon stacked icon="circle-fill" variant="primary" v-show="calcHover"></b-icon>
  <b-icon stacked icon="calculator" scale="0.5" :variant="calcHover?'light':'dark'"></b-icon>
</b-iconstack>

<span v-show="(disablefildUser('gencooment', id)!='you')" style="position:relative;left:30px;top: 16px;width:18px;z-index:2;" v-if="(tmp.number==null)">{{disablefildUser('gencooment', id)}}</span>
<vue-editor :value="project.other" :editorToolbar="customToolbar"
style="height:82vh;position:relative;top:-20px;z-index:1;" v-if="(tmp.number==null)"
class="text-right"  ref="other"

@focus="changeDisable('f', 'gencooment', id);cloudChange=true;"
:id="'gencooment'+id" 
:disabled="disablefild('gencooment', id)?'disabled':false"
/> -->


                                 
<!-- <b-button class="customButton btn-outline-secondary" @click="checkInEditor('refCommentOfTable', tmp.id)" v-if="(openEditor==true)"
style="position:relative;left:24px;top: 26px;width:18px;z-index:2;"><i class="fas fa-calculator"></i></b-button> -->

<!-- 
<b-icon icon='calculator' aria-hidden="true"  @click="checkInEditor('refCommentOfTable', tmp.id)" v-if="(openEditor==true)"
style="position:relative;left:24px;top: 36px;width:25px;z-index:2;"/> -->


<b-iconstack font-scale="3" style="position:relative;left:24px;top:44px;z-index:2;"
@mouseover="cloudHover=true" @mouseleave="cloudHover=false"
@click="updateItem($refs['refCommentOfTable'].quill.getHTML(), 'comment', tmp.id);tmp.comment=$refs['refCommentOfTable'].quill.getHTML();
changeDisable('b', 'refCommentOfTable', tmp.id);cloudChange=false;cloudLoad=true;" v-if="(openEditor==true)">
  <b-icon stacked icon="circle-fill" :animation="cloudLoad?'throb':null" variant="primary" v-show="cloudLoad||cloudHover"></b-icon>
  <b-icon stacked icon="cloud-upload" scale="0.5" :variant="cloudHover?'light':'dark'" v-show="!cloudLoad"></b-icon>
  <b-icon stacked icon="circle" variant="info" v-show="cloudChange"></b-icon>
</b-iconstack>

<b-iconstack font-scale="3" style="position:relative;left:24px;top:44px;z-index:2;"
@click="checkInEditor('refCommentOfTable', tmp.id)" v-if="(openEditor==true)" @mouseover="calcHover = true" @mouseleave="calcHover = false">
  <b-icon stacked icon="circle-fill" variant="primary" v-show="calcHover"></b-icon>
  <b-icon stacked icon="calculator" scale="0.5" :variant="calcHover?'light':'dark'"></b-icon>
</b-iconstack>

<span v-show="(disablefildUser('refCommentOfTable', tmp.id)!='you')" style="position:relative;left:30px;top: 36px;width:18px;z-index:2;"
v-if="(openEditor==true)">{{disablefildUser('refCommentOfTable', tmp.id)}}</span>

<vue-editor :value="tmp.comment" :editorToolbar="customToolbar"  v-if="(openEditor==true)"
@focus="changeDisable('f', 'refCommentOfTable', tmp.id);cloudChange=true;"
:disabled="disablefild('refCommentOfTable', tmp.id)?'disabled':false"
style="position:relative;top:0px;z-index:1;" 
class="text-right"  ref="refCommentOfTable" id="refCommentOfTable"

 />

                         
                                        <b-input-group class="cForm-input">
                                        <b-col cols="text-right">
                                                <b-button size="sm"
                                                v-if="(openEditor==false)" @click="openEditor=true">
                                                  +
                                                </b-button>
                                                <b-button size="sm"
                                                v-if="(openEditor==true)" @click="openEditor=false">
                                                  -
                                                </b-button>
                                        </b-col>
                                        <b-col class="text-right">
                                          {{allSumms()}} €
                                        </b-col>
                                        </b-input-group>
                                        
                    
                                </container-footer>
                            </container>
                        </b-tab>
                          <b-tab v-if="devicesTab()" ref="devices">
                          <template #title>
                            {{$t('projectDetail.devices')}}
  </template>
                            <container>
                                <container-body >
                                  <edevices
                                  :tmp="tmp"
                                  :project="project"
                                  :selectedCornty="selectedCornty"
                                  :id="id"
                                  :workers="workers"
                                  :partx="partx"
                                  :customer="customer"
                                  :person="person"
                                  :selectCustomer="selectCustomer"
                                  :selectPerson="selectPerson"
                                  :selectedWorkers="selectedWorkers"
                                  :selectedDocsList="selectedDocsList"
                                  :windowPrint="windowPrint"
                                  :addPdfs="addPdfs"
                                  :makemodalpdf="makemodalpdf"
                                  :typeDocsList="typeDocsList"
                                  @selectedDocs="selectedDocs"
                                  @addPdf="addPdf"
                                  @addPdfSep="addPdfSep"
                                  @printPdf="printPdf"
                                  @preview="preview"
                                  @printOffer="printOffer"
                                  @hideWindowPrint="hideWindowPrint"
                                  ref="edeviceList"
                                  ></edevices>
                              </container-body>
                              </container>        
                        </b-tab>
                        <b-tab v-if="damageTab()" ref="damage">
                          <template #title>
                            {{$t('projectDetail.damage')}}
                          </template>
                            <container>
                                <container-body >
                                  <damage
                                  :tmp="tmp"
                                  :project="project"
                                  :selectedCornty="selectedCornty"
                                  :id="id"
                                  :workers="workers"
                                  :partx="partx"
                                  :customer="customer"
                                  :person="person"
                                  :selectCustomer="selectCustomer"
                                  :selectPerson="selectPerson"
                                  :selectedWorkers="selectedWorkers"
                                  :selectedDocsList="selectedDocsList"
                                  :windowPrint="windowPrint"
                                  :addPdfs="addPdfs"
                                  :makemodalpdf="makemodalpdf"
                                  :typeDocsList="typeDocsList"

                                  @selectedDocs="selectedDocs"
                                  @addPdf="addPdf"
                                  @addPdfSep="addPdfSep"
                                  @printPdf="printPdf"
                                  @preview="preview"
                                  @printOffer="printOffer"
                                  @hideWindowPrint="hideWindowPrint"
                                  ref="damageList"
                                  ></damage>
                              </container-body>
                              </container>        
                        </b-tab>
                    </b-tabs>
                </b-card>
            </b-card-group>
        </container-body>
    </container>
</template>
<script type="text/javascript">

// import io from 'socket.io-client';
import draggable from 'vuedraggable';
import axios from 'axios';
// import moment from 'moment';
// import { Multipane, MultipaneResizer } from 'vue-multipane';
import {
    VueEditor
} from 'vue2-editor';
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
const items = [];
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
        VueCtkDateTimePicker
        // Multipane,
        // MultipaneResizer,
    },
    props: {
        id: String
    },
    data() {
        return {
        hideNumberOfYear:null,
        selectedTables:[],
        dislink:false,
        wcval:null,
        wcadd:null,
        weval:null,
        weadd:null,
        heightEditforSm:'',
        heightComponentforSm:'min-height:934px',
        wwidth:null,
        beforeSubject:null,
        beforeMail:null,
        pushToWorkDays:true,
        selperiodFinishWork:null,
        autoSend:false,
        autoDate:false,
        cheatypedate:null,
        plan:null,
        planid:null,
        selectedDateForSend:null,
        detectPeriod:null,
        cloudHover:false,
        cloudLoad:false,
        cloudChange:false,
        calcHover:false,
        openEditor:false,
        menuPriceTree: false,
        menuDevicesTree: false,
        menuDocsTree: false,
        // menuImgsTree: false,
        beforeTab: null,
        tabIndex: null,
        dubTabIndex: null, 

        makemodalpdf:false,
        windowPrint:false,

        selectedDocsList:[],
        typeDocsList:[],
        docs_menu_ids:[],
        images_menu_ids:[],

        workerModal:false,
        addSameModalWindow:false,
        
        mapmodal:false,
        mail_date:'',
        mail_address:'',
        mail_logo:'',
        filename:'',
        split:'Split',
        abook:false,
        abooklist:null,
        searchfile:'',
        searchmail:'',
        subject:null,
        content:null, //component
        subjectPlan:null,
        contentPlan:null, //component
        modalMail:[],
        modalFiles:[],
        selectedFiles:null,
        mailSelect:[],
        mailSelectPlan:[],

        dropImage:true,
        dropDoc:true,
        dropDoc2:false,
        nodeDis:true,
        nodeDisDev:true,
        nodeDisDoc:true,
        nodeDisImag:true,
        nameNode:null,
        nameNodeDev:null,
        nameNodeDoc:null,
        nameNodeImag:null,
        idNode:null,
        idNodeDev:null,
        idNodeDoc:-1,
        idNodeImg:-1,
        itemsPrice:[],
        itemsPriceDev:[],
        itemsPriceDoc:[],
        // itemsPriceImg:[],
        oldId:0,
        oldIdDev:0,
        oldIdDoc:0,
        oldIdImg:0,
        itemsMenu:[],
        itemsMenuDev:[],
        itemsMenuDoc:[],
        itemsMenuImag:[],
        selectedItems:[],

        moveToCopyRadio:'move',
        selectedPrice:[],
        selectedPriceDev:[],
        selectedPriceDoc:[],
        selectedPriceImg:[],

        tabxmodal:false,
        mailmodal:false,
        timetableMailModal:false,
        titlex:null,
        comtomodal:null,
        projectfild:{content:'Project'},
        addressfild:'Earth',
        // optImages:[],
        selrow:null,
        customToolbar: [
        [{ list: "check" }],
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  // ['blockquote', 'code-block'],
  // [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  // [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  // [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  // [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  // [{ 'direction': 'rtl' }],                         // text direction
  // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  // [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  // [{ 'font': [] }],
  [{ 'align': [] }],
  // ['clean']                                         // remove formatting button
],        
          tabxhtml:null,
          fs:true,
          //component
          selectCustomer:{id:null},
          selectPerson:{id:null},
          selectMail:{id:null},
          selectPhone:{id:null},

          showsubarr:[], ///component

 
         
          subdata:[],
          langPdf:'de',

          countCall:0,
          project_id:null,
          // selectedDamageImages:'Image',
          domageImages:[],
          selectedLenght: 0,
          dateForInvoice:null,
          google: false,
          q:'baer-gs',
          generalCommentContet:null,
          generalComments:true,
          searchWorker:null,
          selectedWorkers:[],
          startTask:null,
          endTask:null,
          tasktime:'',
          taskName:null,
          task_table_id:null,
          newList:[],
          typesForTables:[],
          itemsTable:[],
            funcStop:0,
            invoices: [],
            partx: [],
            countries:[],
            updatePojectFunc:0,


            ws:null,

            persentCounter: 0,
            damages:[],
dropzoneOptions1: {
            url: 'loadFiles',
            thumbnailWidth: 50,
            parallelUploads: 20,
            dictDefaultMessage: this.$t('alert.clickOrDrop'),
            acceptedFiles: 'application/pdf'
        },
dropzoneOptions2: {
            url: 'loadFiles',
            thumbnailWidth: 50,
            parallelUploads: 20,
            dictDefaultMessage: this.$t('alert.clickOrDrop'),
            acceptedFiles: 'image/*'
        },
            // dropzoneOptions1: {
            //     url: '/loadFiles',
            //     thumbnailWidth: 50,
            //     parallelUploads: 20
            // },


            docs: [],
            files: [],
            responseFiles: [],
            addPdfs: false,
            resp: null,
            viewPrint: true,
            comments: true,

            workers: [],
            workersForSend:[],
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
                    label: 'Insurance #',
                    sortable: true
                },

                other: {
                    label: 'Other',
                    sortable: true
                },
                status_set: {
                    label: 'Status',
                    sortable: true
                },
                show_details: {
                    key: 'show_details',
                    label: 'Order'
                }
            },
            //////////////////////////////////////////component
            fieldsTable: {
                number: {
                    label: 'Number',
                    sortable: true
                },
                date: {
                    label: 'Date',
                    sortable: true
                },
                insurance_number: {
                    label: 'Insurance',
                    sortable: true
                },
                other: {
                    label: "Order",
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
                    sortable: true
                },
                delete: {
                    label: 'Delete',
                    class: 'delete'
                    // class: 'text-center'
                }
            },
            fieldsTableD: {
                number: {
                    label: '#'
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
                    label: 'Insurance',
                    sortable: true
                },
                 status_set: {
                    label: 'Status',
                    sortable: true
                },

                delete: {
                  label: 'Delete'
                }
            },
            ////////////////////////////////////////////
            fieldsOffer: {
                offer_number: {
                    label: 'Offer',
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
                    label: 'Insurance',
                    sortable: true
                },
                other: {
                    label: 'Other',
                    sortable: true
                },
                status_set: {
                    label: 'Status',
                    sortable: true
                },
                delete: {
                    label: 'Delete',
                    class: 'delete'
                }
            },
            fieldsDamages:{
                damage_number: {
                    label: 'Offer #',
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
                    label: 'Insurance',
                    sortable: true
                },
                other: {
                    label: 'Other',
                    sortable: true
                }
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
                area:null,
                number: null,
                editor: null,
                date: null,
                street: null,
                city: null,
                zip: null,
                other:null
            },


            selectedCornty: {code:null},
            customer: {id:null, persons:[]},
            person: {id:null},
            personMail: null,
            personPhone: null,



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
                    label: 'Position #',
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
                insurname: null,
                place: null,
                comment: null
            },
            count_offer_number: 0,
            works: [],
            tmp: {
                number: null,
                date: null,
                place: null,
                insurance: null,
                insurname: null,
                work: null,
                other: null,
                parts: null,
                typeOfHead:'Offer',
                dateEvent:null,
                dateInspect:null,
                worker:null,
                comment:''
            },
            commentOfTable: '',
            area: [],
            availablePersons: [],
            availableMails: [],
            availablePhons: [], 
            looks: []
        } //return
    }, //data
    computed: {
      periodFinishWork(){
        return[{
          text: this.$t('projectDetail.prevperiod'),
          value: 'previous'
        },
        {
          text: this.$t('projectDetail.curperiod'),
          value: 'current' }]
        },
      monthpart(){
        return[{   
        value: 'mstart',
        text: this.$t('projectDetail.mstart')
          },
          {
        value: 'mmidle',
        text: this.$t('projectDetail.mmidle')
          },
          {
        value: 'mend',
        text: this.$t('projectDetail.mend')
          }]
      },
      fieldsDocs() {
        return[
      {   
        key: 'type',
        label: '§',
        sortable: true
      },
      {
        key: 'name',
        label: this.$t('docs.name'),
        class:'w-100',
        sortable: true
      },
      {
        key: 'number',
        label: '#'
      },
      {
        key: 'added',
        label: this.$t('docs.added'),
        sortable: true
      },
      {
        key: 'user',
        label: '👤',
        sortable: true
      },
      {
        key: 'delete',
        label: 'X'
      }
      ]},
      availableWorkers() {
        if (this.searchWorker) {
            return this.workers.filter(item => {
                return item.toLowerCase().includes(this.searchWorker.toLowerCase());
            });
          }
          return this.workers
        }
      
    
    },
    sockets:{
    connect: function(){
      console.log('socket connected')
    },
    customEmit: function(val){
      console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
    }
  },
    methods: {
    linkForWorkers(user){
      var host=window.location.host
      if (this.selectedTables.length > 0){
        this.partx.forEach((valuePart)=> {
          if (valuePart.parts.id == this.selectedTables[0]){
            var notHaveFoolder = 1
            this.itemsMenuImag[0].children.forEach((folder)=>{
              if ((folder.name == valuePart.parts.part_name)&(notHaveFoolder==1)){
                notHaveFoolder = 0
                this.$clipboard('https://'+host+'/#/I/'+user+'/'+this.project.number+'/'+folder.name.replace(' ', '_'))
              }
            })
            if (notHaveFoolder == 1){
              if (confirm('"'+valuePart.parts.part_name+'" '+this.$t('projectDetail.notExist'))) {
                axios.get('/add_images_menu', {
                  params: {
                    parent_id: '-1',
                    project: this.id,
                    newName: valuePart.parts.part_name
                  }
                }).then(response=>{
                  this.$clipboard('https://'+host+'/#/I/'+user+'/'+this.project.number+'/'+response.data.name.replace(' ', '_'))
                })
              } else{
                this.$clipboard('https://'+host+'/#/I/'+user+'/'+this.project.number+'/'+'General+Folder')
              }
            }
          }
        })
      } else {
        this.$clipboard('https://'+host+'/#/I/'+user+'/'+this.project.number+'/'+'General+Folder')
      } 
    },
      seltable(){
        this.selectedTables = []
        this.partx.forEach((valuePart)=> {
          if (valuePart.parts.toggle) {
            this.selectedTables.push(valuePart.parts.id)
          }
        })
      },
      loded(dir, elheight, add){
        this.sm2lg(dir, elheight, add)
      },
      sm2lg(dir, val, add){
        // console.log(dir, val, add)
        var result 
        function changeSm2Lg(wwidth, height, add){
          if(wwidth<=768){
            if(height!=undefined){
              return 'min-height:'+(height+add)+'px;'
            }
          }
        }
        result =  (changeSm2Lg(this.wwidth, val, add))
        if (dir == 'component'){
          this.wcval = val
          this.wcadd = add
          this.heightComponentforSm=result
        }
        if (dir == 'edit'){
          this.weval = val
          this.weadd = add
          this.heightEditforSm=result
        }
      },
      detect(type){
          if (type == 'docs'){
            if ((this.tabIndex==3) && (this.comtomodal!='docs')){
              // this.idNodeDoc=-1;
              return true;
            }
          }
          if (type == 'images'){
            if ((this.tabIndex==4) && (this.comtomodal!='images')){
              // this.idNodeDoc=-1;
              return true;
            }
          }
          //  else{
          //   this.idNodeDoc=-1;
          //   this.responseFiles.forEach((item)=>{
          //     if (item._showDetails==true){
          //       item._showDetails = false
          //     }
          //     // (item._showDetails==true)?false:item._showDetails
          //   })
          // }
        
      },
moveDoc(){
  this.$refs.movedoc.show()
},
moveImag(){
  this.$refs.moveImag.show()
},
projectOther(val){
this.project.other = val
}, 

 checkInEditor(tname, id){
      var result
      var sval
      var separator
      var safeEval = require('safe-eval')
      var valueHtml = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname].quill.getHTML():''

      if (valueHtml.indexOf('=') != -1) {
              separator = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname].quill.getText():''
              separator = separator.replace(/\n/g, ' ')
              separator = separator.substring(0, separator.length - 1)
              separator = separator + ' '
              separator = separator.split('= ')
              separator.splice(-1, 1)
              separator.forEach((val) => {
              var calcval = val.split(' ')[val.split(' ').length-1]

                if (calcval.search(/[a-zA-z=]/gim) == -1) {
                  if (calcval.search(/[-+*)(/]/gim) > -1) {
                    if (calcval.search(/[0-9]/gim) > -1) {
                      if (/[\d)]/.test(calcval[calcval.length - 1])) {
                         var rcalcval = calcval.split(',').join('.')
                        try {
                          result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
                        } catch (e) {
                          result = '(not valid formula)'
                        }
                        sval = rcalcval+'='+result+' '

                        this.$refs[tname].quill.clipboard.dangerouslyPasteHTML(
                          valueHtml = valueHtml.replace(calcval+'=', sval)
                        )
                      }
                    }
                  }
                }
              })
            }

  this.updateItem(valueHtml, 'comment', id)
  this.tmp.comment = valueHtml
},
      butifsel(){
          var detectState = 0
         this.domageImages.forEach(function(v){
            if (v._rowVariant!='') detectState = detectState + 1
         })
         return (detectState>0)
      },
      // sendtodamage(){
      //   var detectState = []
      //    this.domageImages.forEach(function(v){
      //       if (v._rowVariant!='') detectState.push(v.id.split('image?id=')[1])
      //    })
      //   console.log(detectState)
      // },



    sendtodamage(){
        var ids=[]
        // var names=[]
        // // console.log(this.selectedTransfer)
        // this.partx.forEach((valuePart)=> {
        //         if (valuePart.parts.toggle) {
        //             // valuePart.parts.part_content.forEach((v)=>{
        //                 // item_id = v.item_id
        //                 names.push(valuePart.parts.id)
        //             // })
        //         }
        // })
        this.domageImages.forEach((v, i)=>{
            if (v._rowVariant!='') ids.push(v.id.split('image?id=')[1])
        })

        // function onlyUnique(value, index, self) { 
        //     return self.indexOf(value) === index;
        // }

        // var unique = names.filter(onlyUnique)

        axios.get('/send_damage', {
                  params: {
                        ids: ids.join(),
                        names: this.selectedTables.join()
                  }
        }).then(response=>{
            this.domageImages.forEach(v=>{
               v._rowVariant=''  
            })
        })
    },



        damageTab(){
          var countDev = 0
          this.partx.forEach((valuePart)=> {
            if(valuePart.parts.damage_content.length>0){
              countDev = countDev + 1
            }
          })
          return (countDev>0)
        },
        devicesTab(){
          var countDev = 0
          this.partx.forEach((valuePart)=> {
            if(valuePart.parts.devices_content.length>0){
              countDev = countDev + 1
            }
          })
          return (countDev>0)
        },
        selectedDocs(event){
          this.selectedDocsList = []
          this.selectedDocsList = event
          // console.log(this.selectedDocsList)
          // setTimeout(() => {
            this.preview()
           // }, 20);
        },
        addPdf() {
            this.addPdfs=true;
            // console.log(this.addPdfs)
            // this.$refs.printOffer.hide()
            // this.hideWindowPrint()
            // setTimeout(() => {
            
            // setTimeout(() => {
              this.preview()
                //   this.docs2files()
                //   }, 100);     
            // }, 20);
        },
        addPdfSep() {
            this.addPdfs='separator';
            // console.log(this.addPdfs)
            // this.$refs.printOffer.hide()
            this.hideWindowPrint()
            // setTimeout(() => {
            
            // setTimeout(() => {
              this.preview()
                //   this.docs2files()
                //   }, 100);     
            // }, 20);
        },
        printPdf() {
            this.preview()
            setTimeout(function() {
                window.frames["myIframe"].focus();
                window.frames["myIframe"].print();
            }, 2000);
        },
        preview() {
          if (this.$refs.editList != undefined) {
            if (this.$refs.editList.$refs.calcGroup.$refs.print!=undefined){
              this.$refs.editList.$refs.calcGroup.$refs.print.previewPDFForm();
            }
          }
          if (this.$refs.damageList != undefined) {
            if (this.$refs.damageList.$refs.damageGroup.$refs.print!=undefined){
              this.$refs.damageList.$refs.damageGroup.$refs.print.previewPDFForm();
            }

          }
          if (this.$refs.edeviceList != undefined) {
            if (this.$refs.edeviceList.$refs.deviceGroup.$refs.print!=undefined){
              this.$refs.edeviceList.$refs.deviceGroup.$refs.print.previewPDFForm();
            }
          }
        },
        printOffer() {
        this.addPdfs=false;
        this.makemodalpdf=true;
        axios.get('/get_type_docs', {
              params: {
                   type: this.tmp.typeOfHead
                 }
        }).then(response => {
          this.typeDocsList = response.data
          if (this.tmp.typeOfHead ==  'Offers') {this.selectedDocsList=['31']}
          if (this.tmp.typeOfHead == 'Invoices') {this.selectedDocsList=['14']}
          if (this.tmp.typeOfHead == 'Orders') {this.selectedDocsList=['38']}
          if (this.tmp.typeOfHead == 'SUB') {this.selectedDocsList=['41']}
          if (this.tmp.typeOfHead == 'Devices') {this.selectedDocsList=['45']}
            if (this.tmp.typeOfHead == 'Damage') {this.selectedDocsList=['48']}
          // setTimeout(() => {
            this.openWindowPrint()
            // this.$refs.printOffer.show()
            this.preview()
           // }, 20);
        })  
        },

addSameModal(){
 
        this.add_offer.comment=null
        this.add_offer.place=null
        this.add_offer.insurance_number=null
        this.add_offer.work=null

        this.addSameModalWindow=true
      },
      cheabook(){  //component
    if (this.abooklist == null){
    this.abooklist = []
    axios.get('/get_addresbook', {
        }).then(response => {
          response.data.forEach((val)=>{
            this.abooklist.push({item:val.mail, name:val.mail})    
            })
        })
    }
  },

  checkattach(val){  //component
  if (val =='chek' ) this.filename=''
  if (val== 'inp'){
    if (this.filename=='') {this.split='Split'} else{this.split=''}
  }
  },
  filtered(val1, val2) {  //component
    if ((val1!=undefined) && (val2!=undefined)){
      return val1.filter(v => {
        return v.name.toLowerCase().includes(val2.toLowerCase())
      })
    }
  },


  sendMail(val){ //component
    var namePerson = this.selectPerson.name.split(' ')
    var name = (namePerson.length==3)?namePerson[0]+' '+namePerson[2]:this.selectPerson.name
    if ((this.content==null) || (this.content =='')) {
      this.modalMail=[]
      this.modalFiles=[]
      this.selectedFiles=[]
      this.mailSelect=[]

      var subject = this.beforeSubject
      var number=(this.tmp.typeOfHead=='Invoices')?(this.tmp.number.split(' ').length==5)?this.tmp.number.split(' ')[3]:
      this.countDigitals(this.tmp.number.split(' ')[1])+'-'+this.tmp.number.split(' ')[0].split('-')[1]:(this.tmp.typeOfHead=='SUB')?
      this.tmp.number.split(' ')[0]:(this.tmp.typeOfHead=='Sub Invoices')?this.tmp.number.split(' ')[3]:this.tmp.number

      subject = subject.split('@Number').join(number?number:'')
      subject = subject.split('@Document').join(this.tmp.date?this.tmp.date:'')
      subject = subject.split('@Place').join(this.tmp.place?this.tmp.place:'')
      subject = subject.split('@Order').join(this.tmp.other?this.tmp.other:'')
      subject = subject.split('@Insurance').join(this.tmp.insurance?this.tmp.insurance:'')
      subject = subject.split('@InsName').join(this.tmp.insurname?this.tmp.insurname:'')

      this.subject = subject 

      var content = this.beforeMail
      content = content.split('@Respect').join('geehrte'+(('Herr' == name.split(' ')[0])?'r':''))
      content = content.split('@Person').join(name)

      content = content.split('@EditorName').join(this.$security.table.account.first_name)
      content = content.split('@EditorSurname').join(this.$security.table.account.second_name)
      content = content.split('@EditorPhone').join(this.$security.table.account.tel)
      content = content.split('@EditorEmail').join(this.$security.table.account.mail)
      content = content.split('@CompanyWebSite').join(this.mail_date)
      content = content.split('@CompanyAddress').join(this.mail_address)

      var invPress = content.split('<p>@InvPress?')[1]
      invPress = invPress.split('</p>')[0]
      var offerPress = content.split('<p>@OfferPress?')[1]
      offerPress = offerPress.split('</p>')[0]
      var subPress = content.split('<p>@SUBPress?')[1]
      subPress = subPress.split('</p>')[0]

      if (this.tmp.type=='Invoices'){
        content = content.split('<p>@InvPress?'+invPress+'</p>').join(invPress)
      } 
      if (this.tmp.type!='Invoices'){
        content = content.split('<p>@InvPress?'+invPress+'</p>').join('')
      }
      if (this.tmp.type=='Offers'){
        content = content.split('<p>@OfferPress?'+offerPress+'</p>').join(offerPress)
      }
      if (this.tmp.type!='Offers'){
        content = content.split('<p>@OfferPress?'+offerPress+'</p>').join('')
      }
      if (this.tmp.type=='SUB'){
        content = content.split('<p>@SUBPress?'+subPress+'</p>').join(subPress)
      }
      if (this.tmp.type!='SUB'){
        content = content.split('<p>@SUBPress?'+subPress+'</p>').join('')
      }

      this.content = content
      this.filename=''
      }
            this.modalMail=[]

            var subIvoice = false
            if(this.tmp.typeOfHead=='Invoices') {
              if(this.tmp.number.split(' ')[3]!=undefined){
                subIvoice = true
              }
            }
            if(this.tmp.typeOfHead=='Sub Invoices') {
              if(this.tmp.number.split(' ')[3]!=undefined){
                subIvoice = true
              }
            }

            if((this.tmp.type == 'SUB') || subIvoice) {
              axios.get('/get_sub_emails', {
              params: {
                factory:this.tmp.number.split(' ')[0]
              }
              }).then(response => {
                  this.modalMail = response.data
              })
            }
            else{
              this.modalMail.push({item:this.selectCustomer.customerMail, name:this.selectCustomer.customerMail})  
              val.forEach((val)=>{
                this.modalMail.push({item:val.mail, name:val.mail})
              })
            }

            this.modalFiles=[]
            this.responseFiles.forEach((val)=>{
            var t = (val.html=='file')?'f':'d'
            this.modalFiles.push({item:t+'-'+val.id, name:val.name.split('.pdf')[0]})    
            })

            this.mailmodalshow()
          
        },

  sendTimeTableMail(val){ //component
    var subjectFromPlan = null
    var contentFromPlan = null
    var filenameFromPlan = null
    
       axios.get('/get_plan', {
              params: {
                   id: this.tmp.id
                 }
        }).then(response => {
          if (response.data != null){
          this.mailSelectPlan = response.data.to.split(',')
          this.selectedDateForSend = response.data.period
          this.detectPeriod = response.data.period
          subjectFromPlan = response.data.subject
          contentFromPlan = response.data.content
          filenameFromPlan  = response.data.name
          this.planid = response.data.id
          this.selperiodFinishWork = response.data.autoPeriodWorks
          if(response.data.autoDate==1) this.autoDate = true
          if((response.data.autoDate==0)&&(response.data.autoDate==null)) {
            this.autoDate = false
            this.selperiodFinishWork = null
          }
          if(response.data.autosend==1) this.autoSend = true
          if(response.data.autosend==0) this.autoSend = false

          if(response.data.pushToWorkDays==1) this.pushToWorkDays = true
          if(response.data.pushToWorkDays==0) this.pushToWorkDays = false
       }


    var namePerson = this.selectPerson.name.split(' ')
    var name = (namePerson.length==3)?namePerson[0]+' '+namePerson[2]:this.selectPerson.name
    if ((this.contentPlan==null) || (this.contentPlan =='')) {
      this.modalMail=[]
      this.mailSelect=[]
      
      


      // var number=(this.tmp.typeOfHead=='Invoices')?(this.tmp.number.split(' ').length==5)?this.tmp.number.split(' ')[3]:
      // this.countDigitals(this.tmp.number.split(' ')[1])+'-'+this.tmp.number.split(' ')[0].split('-')[1]:
      // (this.tmp.typeOfHead=='SUB')?this.tmp.number.split(' ')[0]:
      // (this.tmp.typeOfHead=='Sub Invoices')?this.tmp.number.split(' ')[3]:this.tmp.number

      // var subject=(this.tmp.place?(this.tmp.place+' - '):'')+
      // (this.tmp.insurance?(this.tmp.insurance+' - '):'')+(this.tmp.other?(this.tmp.other+' - '):'')
      // subject = subject + number
      // this.subjectPlan=(subject!='')?(subject+' intern'):''

      // if (subjectFromPlan!=null){
      //   this.subjectPlan = subjectFromPlan
      // }

      // var content=(this.tmp.type!='SUB' ? 'Sehr geehrte'+(('Herr' == name.split(' ')[0])?'r':'')+' '+name : 'Sehr geehrte Damen und Herren') +',<br/>'+
      // (this.tmp.type=='Invoices'?'anbei erhalten Sie unsere Rechnung, mit der Bitte, um Prüfung sowie zeitnahen Ausgleich.':'')+
      // (this.tmp.type=='Offers'?'anbei unser KV mit bitte zum beauftragen.':'')+
      // (this.tmp.type=='SUB'?'anbei erhalten Sie Auftrag für o.g. Projekt':'')
      // +'<br/><p sytle="padding-bottom:4px;">Mit freundlichen Gr&uuml;&szlig;en</p><p>&nbsp;</p><b>'+
      // this.$security.table.account.first_name +' '+ this.$security.table.account.second_name
      // +'</b><hr color="black" style="width: 345px; padding: 0px; margin: 0px;" align="left" sytle="padding-bottom:4px;"/><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/phone-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'
      // +this.$security.table.account.tel+
      // '</p><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/email-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'
      // +this.$security.table.account.mail+
      // '<p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/link-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'+this.mail_date+'</p><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/address-icon-2x.png" alt="" width="13"  sytle="padding-bottom:4px;" />&nbsp;&nbsp;'+this.mail_address+'</p><p style="width:345px;height:106px;padding-top:2px;"><img src="'+this.mail_logo+'" style="max-height:100px;max-width:345px;"/></p>'
      // this.contentPlan = content


      var subject = this.beforeSubject

      var number=(this.tmp.typeOfHead=='Invoices')?(this.tmp.number.split(' ').length==5)?this.tmp.number.split(' ')[3]:
      this.countDigitals(this.tmp.number.split(' ')[1])+'-'+this.tmp.number.split(' ')[0].split('-')[1]:(this.tmp.typeOfHead=='SUB')?
      this.tmp.number.split(' ')[0]:(this.tmp.typeOfHead=='Sub Invoices')?this.tmp.number.split(' ')[3]:this.tmp.number

      subject = subject.split('@Number').join(number?number:'')
      subject = subject.split('@Document').join(this.tmp.date?this.tmp.date:'')
      subject = subject.split('@Place').join(this.tmp.place?this.tmp.place:'')
      subject = subject.split('@Order').join(this.tmp.other?this.tmp.other:'')
      subject = subject.split('@Insurance').join(this.tmp.insurance?this.tmp.insurance:'')
      subject = subject.split('@InsName').join(this.tmp.insurname?this.tmp.insurname:'')

      if (subjectFromPlan!=null){
        this.subjectPlan = subjectFromPlan
      } else{
        this.subjectPlan = subject 
      }

      var content = this.beforeMail
      content = content.split('@Respect').join('geehrte'+(('Herr' == name.split(' ')[0])?'r':''))
      content = content.split('@Person').join(name)

      content = content.split('@EditorName').join(this.$security.table.account.first_name)
      content = content.split('@EditorSurname').join(this.$security.table.account.second_name)
      content = content.split('@EditorPhone').join(this.$security.table.account.tel)
      content = content.split('@EditorEmail').join(this.$security.table.account.mail)
      content = content.split('@CompanyWebSite').join(this.mail_date)
      content = content.split('@CompanyAddress').join(this.mail_address)

      var invPress = content.split('<p>@InvPress?')[1]
      invPress = invPress.split('</p>')[0]
      var offerPress = content.split('<p>@OfferPress?')[1]
      offerPress = offerPress.split('</p>')[0]
      var subPress = content.split('<p>@SUBPress?')[1]
      subPress = subPress.split('</p>')[0]

      if (this.tmp.type=='Invoices'){
        content = content.split('<p>@InvPress?'+invPress+'</p>').join(invPress)
      } 
      if (this.tmp.type!='Invoices'){
        content = content.split('<p>@InvPress?'+invPress+'</p>').join('')
      }
      if (this.tmp.type=='Offers'){
        content = content.split('<p>@OfferPress?'+offerPress+'</p>').join(offerPress)
      }
      if (this.tmp.type!='Offers'){
        content = content.split('<p>@OfferPress?'+offerPress+'</p>').join('')
      }
      if (this.tmp.type=='SUB'){
        content = content.split('<p>@SUBPress?'+subPress+'</p>').join(subPress)
      }
      if (this.tmp.type!='SUB'){
        content = content.split('<p>@SUBPress?'+subPress+'</p>').join('')
      }

      this.contentPlan = content



      this.filename=this.$t('oneCountAlret.Invoices')+' @InvNo'
      }

      if (contentFromPlan!=null){
        this.contentPlan = contentFromPlan
      }

      if (filenameFromPlan!=null){
        this.filename = filenameFromPlan
      }
      
            this.modalMail=[]

            var subIvoice = false
            if(this.tmp.typeOfHead=='Invoices') {
              if(this.tmp.number.split(' ')[3]!=undefined){
                subIvoice = true
              }
            }
            if(this.tmp.typeOfHead=='Sub Invoices') {
              if(this.tmp.number.split(' ')[3]!=undefined){
                subIvoice = true
              }
            }

            if((this.tmp.type == 'SUB') || subIvoice) {
              axios.get('/get_sub_emails', {
              params: {
                factory:this.tmp.number.split(' ')[0]
              }
              }).then(response => {
                  this.modalMail = response.data
              })
            }
            else{
              this.modalMail.push({item:this.selectCustomer.customerMail, name:this.selectCustomer.customerMail})  
              val.forEach((val)=>{
                this.modalMail.push({item:val.mail, name:val.mail})
              })
            }

            this.timeTableMailModalShow()
           })
        },

    sendmail(){  //component
    if (this.mailSelect.length<1) alert(this.$t('alert.noRecipients'))
    if (this.subject==null) alert(this.$t('alert.noSubject'))
    if ((this.subject!=null) && (this.mailSelect.length>=1)){
      if (this.selectedFiles!=null) {
        var files=this.selectedFiles.join()
      } else {var files='_'}
      var from=this.$security.table.account.mail;
      var to=this.mailSelect.join();
      axios.post('/send_mail', {

            from:from,
            to:to,
            subject: this.subject,
            content: (this.content==null)?'':this.content,
            filename: this.filename,
            files:files

        }).then(response => {
          this.mailmodalhide()
          this.$refs.calProject.showAlert(this.mailSelect.join())
          this.content = null
        })
      
    }
    },

sendtimetablemail(type){
var from=this.$security.table.account.mail;
var to=this.mailSelectPlan.join();
var params = null 
if (type =='plan_mail') {
  params = {
  'item': this.tmp.id,
  'period': this.selectedDateForSend,
  'from': from,
  'to': to,
  'subject': this.subjectPlan,
  'name': this.filename,
  'autosend' : this.autoSend,
  'autodate' : this.autoDate?1:0,
  'autoperiodworks' : this.selperiodFinishWork,
  'pushToWorkDays':this.pushToWorkDays?1:0,
  'content': (this.contentPlan==null)?'':this.contentPlan
  
  }
}
if (type =='replan_mail') {
  // console.log(this.autoSend)
  params = {
    'item': this.tmp.id,
    'period': this.selectedDateForSend,
    'from': from,
    'to': to,
    'subject': this.subjectPlan,
    'name': this.filename,
    'autosend' : this.autoSend,
    'autodate' : this.autoDate?1:0,
    'autoperiodworks' : this.selperiodFinishWork,
    'pushToWorkDays':this.pushToWorkDays?1:0,
    'content': (this.contentPlan==null)?'':this.contentPlan,
    'id': this.planid
  }
}
if(type =='remove_mail'){params={id:this.planid}}

    if (this.mailSelectPlan.length<1) alert(this.$t('alert.noRecipients'))
    if (this.subjectPlan==null) alert(this.$t('alert.noSubject'))
    if ((this.subjectPlan!=null) && (this.mailSelectPlan.length>=1)){


      axios.post('/'+type, params)
      this.timetableMailModalHide()
      this.contentPlan = null
    }
    },

mapmodalhide(){
    this.mapmodal=false;
    if (this.comtomodal!=null) this.tabxmodal=true;

},
mapmodalshow(){
    this.mapmodal=true;
},
mailmodalhide(){
    this.mailmodal=false;
    if (this.comtomodal!=null) this.tabxmodal=true;
},

timetableMailModalHide(){
    this.contentPlan=null;
    this.planid=null;
    this.timetableMailModal=false;
    this.detectPeriod=null;
    this.selectedDateForSend=null;
    this.mailSelectPlan=[];
    if (this.comtomodal!=null) this.tabxmodal=true;
},

mailmodalshow(){
    this.mailmodal=true;
},
timeTableMailModalShow(){
    this.timetableMailModal=true;
},
closeaddok(){
    this.addSameModalWindow=false;
    if (this.comtomodal!=null) this.tabxmodal=true;  
},
openWindowPrint(){
  this.windowPrint=true;
},
hideWindowPrint(){
  this.windowPrint=false;
  if (this.comtomodal!=null) this.tabxmodal=true;
},
tabletopartx(tables){
  this.partx=[];
  this.partx = tables;
},
        ploadDocToFrame(row) {
            row.toggleDetails();
            var index = row.index;
            if (row.detailsShowing == false) {
              this.dropDoc=false
                setTimeout(() => {

                  // this.$refs.docs1?this.$refs.docs1.$refs['ifrForm' + index].submit():''
                  this.$refs.docs2?this.$refs.docs2.$refs['ifrForm' + index].submit():''

                }, 50);
            }
        },
    prowSelected(items) {
        // console.log(items)
         if(this.selectedPrice.indexOf(items)==-1){
            this.selectedPrice = this.selectedPrice.filter((v)=>{
                if (v.id != items.id){
                    return v
                }
            });
            this.selectedPrice.push(items);
            items._rowVariant='success';
         } else{
            this.selectedPrice.splice(this.selectedPrice.indexOf(items), 1)
            items._rowVariant=''
         }
    },

    prowSelectedDev(items) {
         if(this.selectedPriceDev.indexOf(items)==-1){
            this.selectedPriceDev = this.selectedPriceDev.filter((v)=>{
                if (v.id != items.id){
                    return v
                }
            });
            this.selectedPriceDev.push(items);
            items._rowVariant='success';
         } else{
            this.selectedPriceDev.splice(this.selectedPriceDev.indexOf(items), 1)
            items._rowVariant=''
         }
    },

    prowSelectedDoc(items) {
        // console.log(items)
         if(this.selectedPriceDoc.indexOf(items)==-1){
            this.selectedPriceDoc = this.selectedPriceDoc.filter((v)=>{
                if (v.id != items.id){
                    return v
                }
            });
            this.selectedPriceDoc.push(items);
            items._rowVariant='success';
         } else{
            this.selectedPriceDoc.splice(this.selectedPriceDoc.indexOf(items), 1)
            items._rowVariant=''
         }
    },
    prowSelectedImg(items) {
        // console.log(items)
         if(this.selectedPriceImg.indexOf(items)==-1){
            this.selectedPriceImg = this.selectedPriceImg.filter((v)=>{
                if (v.id != items.id){
                    return v
                }
            });
            this.selectedPriceImg.push(items);
            items._rowVariant='success';
         } else{
            this.selectedPriceImg.splice(this.selectedPriceImg.indexOf(items), 1)
            items._rowVariant=''
         }
    },

    // selectedModal(val){
    //     var price_ids=[]
    //     if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selectedPrice.length+
    //         ' rows in to '+val.name+"?")) {
    //         this.selectedPrice.forEach((val)=>{
    //             price_ids.push(val.id)
    //         })
    //          axios.get('/cp_mv_to_price', {
    //              params: {
    //                  price_ids: price_ids.join(),
    //                  new_menu: val.id,
    //                  operation: this.moveToCopyRadio
    //              }
    //          })
    //     }
    // },
    selectedModalDoc(val){

        var docs_ids=[]
        var files_ids=[]
        // if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selectedPriceDoc.length+
        //     ' rows in to '+val.name+"?")) {
            this.selectedPriceDoc.forEach((val)=>{
                if (val.html != 'file') {
                  docs_ids.push(val.id)
                } else{
                  files_ids.push(val.id)
                }
            })
              // console.log(docs_ids)
             axios.get('/mv_docs', {
                 params: {
                     docs_ids: docs_ids.join(),
                     files_ids: files_ids.join(),
                     new_menu: val.id
                 }
             }).then(response=>{
              // this.$socket.send('getProjectDetail')
              // alert();
     
                setTimeout(() => {
                   
                   this.getDocs();
                //   }, 100);     
            }, 20);
                      // this.getdomageImages()
             // this.getDocs();
        })                      
        // }
    },

    selectedModalImag(val){

        var files_ids=[]
        // if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selectedPriceDoc.length+
        //     ' rows in to '+val.name+"?")) {
            this.selectedPriceImg.forEach((val)=>{
                  var id = val.id.split('=')
                  // console.log(id[1])
                  files_ids.push(id[1])

                
            })
              // console.log(docs_ids)
             axios.get('/mv_images', {
                 params: {
                     files_ids: files_ids.join(),
                     new_menu: val.id
                 }
             }).then(response=>{
              // this.$socket.send('getProjectDetail')
              // alert();
     
                setTimeout(() => {
                   
                   this.getDocs();
                //   }, 100);     
            }, 20);
                      // this.getdomageImages()
             // this.getDocs();
        })                      
        // }
    },

    //   okMoveToCopy(){
    //     this.selectedPrice=[],
    //     this.$refs.move.hide()
    // },
      okMoveDoc(){
        this.selectedPriceDoc=[],
        this.$refs.movedoc.hide()
    },

      okMoveImg(){
        this.selectedPriceImg=[],
        this.$refs.moveImag.hide()
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
      detectItem(items){
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
        return returnArr
    },
    sendPrice(){
        var ids=[]
        // var names=[]
        // console.log(this.selectedTransfer)
        // this.partx.forEach((valuePart)=> {
        //         if (valuePart.parts.toggle) {
        //             // valuePart.parts.part_content.forEach((v)=>{
        //                 // item_id = v.item_id
        //                 names.push(valuePart.parts.id)
        //             // })
        //         }
        // })
        this.selectedPrice.forEach((v, i)=>{
            ids.push(v.id)
        })

        // function onlyUnique(value, index, self) { 
        //     return self.indexOf(value) === index;
        // }

        // var unique = names.filter(onlyUnique)
        console.log(this.selectedTables)
        axios.get('/send_price', {
                  params: {
                        ids: ids.join(),
                        names: this.selectedTables.join()
                  }
        }).then(response=>{
            this.selectedPrice=[]
            this.selectedTables=[]
            this.itemsPrice.forEach(v=>{
               v._rowVariant=''  
            })
        })
    },
    sendDevice(){
        var ids=[]
        // var names=[]
        // console.log(this.selectedTransfer)
        // this.partx.forEach((valuePart)=> {
        //         if (valuePart.parts.toggle) {
        //             // valuePart.parts.part_content.forEach((v)=>{
        //                 // item_id = v.item_id
        //                 names.push(valuePart.parts.id)
        //             // })
        //         }
        // })
        this.selectedPriceDev.forEach((v, i)=>{
            ids.push(v.id)
        })

        // function onlyUnique(value, index, self) { 
        //     return self.indexOf(value) === index;
        // }

        // var unique = names.filter(onlyUnique)

        axios.get('/send_devices', {
                  params: {
                        ids: ids.join(),
                        names: this.selectedTables.join()
                  }
        }).then(response=>{
            this.selectedPriceDev=[]
            this.itemsPriceDev.forEach(v=>{
               v._rowVariant=''  
            })
        })
    },
      mv_cpPrice(){
        if (this.idNode==null){
            alert(this.$t('alert.noItemSelect'))
        } else{
            if (this.selectedPrice.length==0){
                alert(this.$t('alert.noRowsSelected'))
            }
        }
        if ((this.idNode!=null)&&(this.selectedPrice.length!=0)){
            this.$refs.move.show()           
        }
    },
      mv_cpDevice(){
        if (this.idNodeDev==null){
            alert(this.$t('alert.noItemSelect'))
        } else{
            if (this.selectedPriceDev.length==0){
                alert(this.$t('alert.noRowsSelected'))
            }
        }
        if ((this.idNodeDev!=null)&&(this.selectedPriceDev.length!=0)){
            this.$refs.moveDev.show()           // новое окно нужно сделать
        }
    },
    addRowPrice(){
        if (this.idNode==null){
            alert(this.$t('alert.noSelectedForAdd'))
        } else {
            axios.get('/add_price', {
                params: {
                    id: this.idNode
                }
            })
        }
         location.href = "#finishList"
    },
    addRowDevice(){
        if (this.idNodeDev==null){
            alert(this.$t('alert.noSelectedForAdd'))
        } else {
            axios.get('/add_devices', {
                params: {
                    id: this.idNodeDev
                }
            })
        }
         location.href = "#finishList"
    },

    removePrice(){
       if (this.idNode==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_price_menu', {
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
    removeDevice(){
       if (this.idNodeDev==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_devices_menu', {
                    params: {
                        remove_id: this.idNodeDev
                    }
                }).then(response=>{
                    this.idNodeDev=null,
                    this.nameNodeDev=null
                })
            }
        } 
    },
    removeDoc(){
       if (this.idNodeDoc==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_docs_menu', {
                    params: {
                        remove_id: this.idNodeDoc
                    }
                }).then(response=>{
                    this.idNodeDoc=null,
                    this.nameNodeDoc=null
                })
            }
        } 
    },
    removeImag(){
       if (this.idNodeImg==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_image_menu', {
                    params: {
                        remove_id: this.idNodeImg
                    }
                }).then(response=>{
                    this.idNodeImg=null,
                    this.nameNodeImag=null
                })
            }
        } 
    },
          addPrice(){
      function findLevel(obj, id) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_price_menu', {
                        params: {
                            parent_id: val.id
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.itemsMenu, this.idNode)  
    },
          addDevice(){
      function findLevel(obj, id) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_devices_menu', {
                        params: {
                            parent_id: val.id
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.itemsMenuDev, this.idNodeDev)  
    },
    addDoc(){
      var newName = this.$t('projectDetail.plusPart');
      function findLevel(obj, id, project) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){

                    axios.get('/add_docs_menu', {
                        params: {
                            parent_id: val.id,
                            project: project,
                            newName: newName
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id, project, newName)
                    }
                }
            })
        }

        findLevel(this.itemsMenuDoc, this.idNodeDoc, this.id)
    },
    addImag(){
      var newName = this.$t('projectDetail.plusPart')
      function findLevel(obj, id, project) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_images_menu', {
                        params: {
                            parent_id: val.id,
                            project: project,
                            newName: newName
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id, project, newName)
                    }
                }
            })
        }

        findLevel(this.itemsMenuImag, this.idNodeImg, this.id)
    },
       getPrices(){


        // delete this.$options.sockets.onmessage;


        if (this.idNode!=null){
            axios.get('/prices', {
                params: {
                    id:this.idNode?this.idNode:0
                }
            }).then(response => {
                this.itemsPrice = response.data
                // this.$socket.send('getPrices')
                // this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
            })
        }
        axios.get('/price_menu').then(response => {
            this.itemsMenu=[];
               response.data.forEach((val)=>{
                         if (val.parrent==0){
                            val['children']=[]
                            this.itemsMenu.push(val);
                        }
               });

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

        findLevel(this.itemsMenu, valResp.parrent)  
               });

             


            })
        },
       getDevices(){


        // delete this.$options.sockets.onmessage;


        if (this.idNodeDev!=null){
            axios.get('/devices', {
                params: {
                    id:this.idNodeDev?this.idNodeDev:0
                }
            }).then(response => {
                this.itemsPriceDev = response.data
                // this.$socket.send('getPrices')
                // this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
            })
        }
        axios.get('/devices_menu').then(response => {
            this.itemsMenuDev=[];
               response.data.forEach((val)=>{
                         if (val.parrent==0){
                            val['children']=[]
                            this.itemsMenuDev.push(val);
                        }
               });

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

        findLevel(this.itemsMenuDev, valResp.parrent)  
               });
            })
        },
   getDocs(){

        // delete this.$options.sockets.onmessage;
        // if (this.idNodeDoc!=null){
        //     axios.get('/dooocs', {
        //         params: {
        //             id:this.idNodeDoc?this.idNodeDoc:0
        //         }
        //     }).then(response => {
        //         this.itemsPriceDoc = response.data
        //         // this.$socket.send('getPrices')
        //         // this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
        //     })
        // }
        
        
        
        axios.get('/docs_menu', {
                params: {
                    project:this.id
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
                this.docs2files();



        axios.get('/images_menu', {
                params: {
                    project:this.id
                }
            }).then(response => {
            this.itemsMenuImag=[];
            this.itemsMenuImag.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
            this.images_menu_ids.push(-1);
               response.data.forEach((val)=>{
                        if (val.parrent==0){
                            val['children']=[]
                            // console.log(val)
                            this.itemsMenuImag.push(val);
                        }
               });

                response.data.forEach((valResp)=>{
                  function findLevel(obj, id)  {
                        obj.forEach((val)=>{
                            if (val.id==id){
                                valResp['children']=[]
                                // console.log(valResp)
                                val.children.push(valResp);
                            } else{
                                if (val.children.length!=0){
                                    findLevel(val.children, id)
                                }
                            }
                        })
                    }
                this.images_menu_ids.push(valResp.id)
                findLevel(this.itemsMenuImag, valResp.parrent)  
               })
            })
             // console.log(this.itemsMenuImag)
            this.getdomageImages()     
          })
        },
    toModel(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    //val.name=enterVal
                    axios.get('/update_name_price_menu', {
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

        findLevel(this.itemsMenu, this.idNode)
    },
    toModelDev(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    //val.name=enterVal
                    axios.get('/update_name_devices_menu', {
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

        findLevel(this.itemsMenuDev, this.idNodeDev)
    },
    toModelDoc(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    //val.name=enterVal
                    axios.get('/update_name_docs_menu', {
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

        findLevel(this.itemsMenuDoc, this.idNodeDoc)
    },
    toModelImag(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    //val.name=enterVal
                    axios.get('/update_name_images_menu', {
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

        findLevel(this.itemsMenuImag, this.idNodeImg)
    },
    nodeDisTurn(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDis = false
            }
       },
    nodeDisTurnDev(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDisDev = false
            }
       },
    nodeDisTurnDoc(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDisDoc = false
            }
       },
    nodeDisTurnImag(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDisImag = false
            }
       },

    pcurNodeClicked(model, component) {
        this.nameNode = model.name,
        this.idNode=model.id
        if(this.idNode == this.oldId){
             if (this.itemsPrice.length>0){
                this.itemsPrice=[]
            } else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPrice = response.data;
                 this.$refs.priceChild1.loded();
             })
            }
        }else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPrice = response.data;
                 this.$refs.priceChild1.loded();
             })
        }
        this.oldId = this.idNode
        if ((model.parrent == 0) && component.folder == false){
            this.idNode = null
        }
    },

    pcurNodeClickedDev(model, component) {
        this.nameNodeDev = model.name,
        this.idNodeDev=model.id

        if(this.idNodeDev == this.oldIdDev){
             if (this.itemsPriceDev.length>0){
                this.itemsPriceDev=[]
            } else{
            axios.get('/devices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPriceDev = response.data;
                 this.$refs.devChild1.loded();
             })
            }
        }else{
            axios.get('/devices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPriceDev = response.data;
                 this.$refs.devChild1.loded();
             })
        }
        this.oldIdDev = this.idNodeDev
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeDev = null
        }
    },

    pcurNodeClickedDoc(model, component) {
        this.nameNodeDoc = model.name,
        this.idNodeDoc=model.id

        if(this.idNodeDoc == this.oldIdDoc){
             if (this.itemsPriceDoc.length>0){
                this.itemsPriceDoc=[]
            } 
            this.$refs.docs2.loded()
        //     else{
        //     axios.get('/show_docs', {
        //          params: {
        //              id: model.id
        //          }
        //      }).then(response => {
        //          this.itemsPriceDoc = response.data;
        //          this.$refs.docs2.loded();
        //      })
        //     }
        // }else{
        //     axios.get('/show_docs', {
        //          params: {
        //              id: model.id
        //          }
        //      }).then(response => {
        //          this.itemsPriceDoc = response.data;
        //          this.$refs.docs2.loded();
        //      })
        }
        this.oldIdDoc = this.idNodeDoc
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeDoc = null
        }
    },
    pcurNodeClickedImg(model, component) {
        this.nameNodeImag = model.name,
        this.idNodeImg=model.id

        if(this.idNodeImg == this.oldIdImg){
            //  if (this.itemsPriceImg.length>0){
            //     this.itemsPriceImg=[]
            // } 
            this.$refs.images1.loded()
        }
        //     else{
        //     // axios.get('/show_imgs', {
        //     //      params: {
        //     //          id: model.id
        //     //      }
        //     //  }).then(response => {
        //          // this.itemsPriceImg = response.data;
        //          this.$refs.images1.loded();
        //      // })
        //     }
        // }else{
            // axios.get('/show_imgs', {
            //      params: {
            //          id: model.id
            //      }
            //  }).then(response => {
                 // this.itemsPriceImg = response.data;
                 // this.$refs.images1.loded();
             // })
        // }
        this.oldIdImg = this.idNodeImg
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeImg = null
        }
    },

    fschange(title, name){
    this.titlex = title
    this.comtomodal = name
    this.tabxmodal=true

    },
    showx(classId, index){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.index = index
      viewer.show()

    },
    subcontract(id){
      var subcont = false
      this.subdata.forEach(function(val){
        subcont = (val.order_id==id)
      })
      return subcont
    },
    loadsub(id){
       axios.get('/sub_order', {
        }).then(response => {
          this.subdata = response.data
        })
  },

  
 disablefild(fild, id){
        var result = false
              this.looks.forEach((val)=>{
                    if (val.rows_id == id) {
                      if (val.fild == fild) {
                        result = true
                      }
                    }
                })
        if (this.stopDis==true) result = false
        if (this.type=='Invoices') result = true
        return result
      },
      disablefildUser(fild, id){ //component
        var result 
        // var result = (this.type=='Invoices') ? '' : 'you'
              this.looks.forEach((val)=>{
                    if (val.rows_id == id) {
                      if (val.fild == fild) {
                        result = val.user
                      }
                    }
                })
        return result
      },
      changeDisable(type_operation, fild, id){
        this.stopDis=(type_operation=='f')
        axios.get('/changeDisableTable', {
          params: {
            type_operation: type_operation,
            fild: fild,
            id: id,
            'user': this.$security.account['first_name']+'_'+this.$security.account['second_name']
          }
        })
        if (type_operation == 'f'){
          setTimeout(()=>{
          }, 15000);
        }
},

    // presetFilds(){
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].thClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].thClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].thClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].thClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].tdClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].tdClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].tdClass=''
    //     this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].tdClass=''
    //     this.domageImages.forEach((v)=>{
    //       v._rowVariant=''
    //     })
    // },
    // pallselrow(){
    //   this.domageImages.forEach((v)=>{
    //       v._rowVariant='success'
    //   })
    // },
    // pallselrowin(table){
    //   table.forEach((v)=>{
    //       v._rowVariant='success'
    //   })
    // },


      getdomageImages(){
        // console.log(this.project.number)
       axios.get('/domage_images', {
          params: {
            id: this.id,
            project: (this.project.number==null)?'0001':this.project.number
          }
        }).then(response => {

        this.domageImages = response.data.filter(function (v){
          if((v.file_name.split('.')[v.file_name.split('.').length-1]) != 'pdf'){ return v}
        })
         console.log(this.domageImages)
        })

        // console.log((this.project.number==null)?'0001':this.project.number, this.domageImages )
      },
      // countWorker(val){
      //   if (val != null) {
      //     return '* '+val.split(',').length
      //   }
      // },
      countDigitals(val){
        // console.log(val)
        var nuls=3-val.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        val='0'+val
                    }
        return val
      },
    // workersToTask(id, event){
    //   axios.get('/workers_task', {
    //     params: {
    //       workers: event?this.selectedWorkers.join():'Null',
    //       id: id
    //     }
    //   })
    // },
    updateItem(val, type, id){
        axios.post('/update_item_from_project', {
               
                   val: val,
                   type: type,
                   id: id
                 
        }).then(response => {
                  this.cloudLoad = false;
                 });
    },
    updatefilename(val, type, id){
        axios.get('/updatefilename', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        })
    },
 updatefilenames(val, type, id){
        axios.get('/updatefilenames', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        })
    },
    updatedocname(val, type, id){
        axios.get('/updatedocname', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        })
    },
    showCommetnts(){
    this.tmp.number=null,
    this.tmp.typeOfHead=null,
    this.tmp.id=null,
    this.generalComments=true
    if(this.dubTabIndex==0){
      setTimeout(() => {
        this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 56)
      }, 300)
    }
    },


    // displaytime() {
    // var self = this
    // this.tasktime = moment().format("YYYY-MM-DD HH:mm:ss");
    // setTimeout(self.displaytime, 1000)
    // },
    // difTime(val, t){
    // var start = moment(val, "YYYY-MM-DD HH:mm:ss.SSS");
    // var diffrent = moment(this.tasktime,"YYYY-MM-DD HH:mm:ss")
    // .diff(moment(start,"YYYY-MM-DD HH:mm:ss"), "seconds")
    // var sec = diffrent;
    // var h = sec/3600 ^ 0;
    // var m = (sec-h*3600)/60 ^ 0;
    // var s = sec-h*3600-m*60;
    // if((t=='s') | (t=='l')){
    // return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+((t=='l')?":"+(s<10?"0"+s:s):''))
    // }
    // if((t=='x')){
    // return diffrent
    // }
    // },
    // difTimeFinish(start, end, t){
    // var diffrent = moment(end,"YYYY-MM-DD HH:mm:ss")
    // .diff(moment(start,"YYYY-MM-DD HH:mm:ss"), "seconds")
    // var sec = diffrent;
    // var h = sec/3600 ^ 0;
    // var m = (sec-h*3600)/60 ^ 0;
    // var s = sec-h*3600-m*60;
    // if((t=='s') | (t=='l')){
    // return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m)+((t=='l')?":"+(s<10?"0"+s:s):''))
    // }
    // if((t=='x')){
    // return diffrent
    // }
    // },
    // summHour(tasks, t){
    // var totallHours=0
    // var totallHoursS=0
    //   tasks.forEach((v)=>{
    //     if(v.data_time_start!=null & v.data_time_end!=null){
    //       totallHours = totallHours + parseInt(this.difTimeFinish(v.data_time_start, v.data_time_end, 'x'))
    //       var temp = parseInt(this.difTimeFinish(v.data_time_start, v.data_time_end, 'x'))
    //       temp = temp*((v.workers==null)?1:v.workers.split.length)
    //       totallHoursS = totallHoursS + temp
    //     } else{
    //       totallHours = totallHours + parseInt(this.difTime(v.data_time_start, 'x'))
    //       var temp = parseInt(this.difTime(v.data_time_start, 'x'))
    //       temp = temp*((v.workers==null)?1:v.workers.split.length)
    //       totallHoursS = totallHoursS + temp
    //     }
    //   })
    // var sec = (t=='(s)')?totallHoursS:totallHours;
    // var h = sec/3600 ^ 0;
    // var m = (sec-h*3600)/60 ^ 0;
    // var s = sec-h*3600-m*60;
    // if(t=='s'){
    // return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    // }
    // if(t=='(s)'){
    // return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    // }
    // if(t=='x'){
    // return totallHours
    // }
    // if(t=='xs'){
    // return totallHoursS
    // }
    // },
    // allhours(val){
    // var hours = 0
    //   this.loadDamages.forEach((v)=>{
    //     if (val == 'n'){
    //     var result = this.summHour(v.tasks, 'x')
    //     }
    //     if (val == '(s)'){
    //     var result = this.summHour(v.tasks, 'xs')
    //     }
    //     hours = hours + parseInt(result)
    //   })
    // var sec = hours;
    // var h = sec / 3600 ^ 0;
    // var m = (sec - h * 3600) / 60 ^ 0;
    // var s = sec - h * 3600 - m * 60;
    // return ((h<10?"0"+h:h)+":"+(m<10?"0"+m:m))
    // },
    // taskStop(id){
    //   axios.get('/task_time_damage', {
    //         params: {
    //              id: id
    //            }
    //   })
    // },
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
                }
            }).then(response=>{
                this.newPerson('')

                this.addFirm={name: this.customerName, id: response.data.id}
            })
  }          
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
                        id: (this.project.number==null)?'0001':this.project.number
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
if(mergedArr.length==0){
  mergedArr.push({'id':0})
}

this.files = (this.files != response.data)?response.data:this.files

var addFiles = []
mergedArr.forEach((item)=>{
axios.get('/get_tables', {
            params: {
              id: item.id
            }
        }).then(response => {
          var filesarr = response.data

          //this.$delete(filesarr, filesarr.length-1)
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

            var change = 0
            if (this.responseFiles.length != this.docs.concat(files).length){
              change = 1
            }
            if (this.responseFiles.length==0) {
              change = 1
            }

            this.responseFiles.forEach((v, i)=> {
              if(this.docs.concat(files)[i]!=undefined){
                if (v.name != this.docs.concat(files)[i].name) {
                  change = 1
                }
              } 
            })


          
                if(change == 1) //хотя лучше элименты сравнить, что бы не закрывался фрейм с пдф
                { this.responseFiles  = this.docs.concat(files) }
          
                 })
        })
        })
              })
        },
        // fsadd() {
        //         this.$refs.myVueDropzone.removeAllFiles()
        // },
        fsadd1() {
                this.$refs.myVueDropzone1.removeAllFiles()
        },
        fsadd2() {
                this.$refs.myVueDropzone2.removeAllFiles()
        },
        fsadd3() {
                this.$refs.myVueDropzone3.removeAllFiles()
        },
        fsadd4() {
                this.$refs.myVueDropzone4.removeAllFiles()
        },
        sendingEvent(file, xhr, formData) {
            var selectTables = []
            this.partx.forEach(function(val, index) {
                if (val.parts.toggle) {
                    selectTables.push(val.parts.id)
                }
            })
            xhr.setRequestHeader('X-Number', this.project.number);
            xhr.setRequestHeader('X-Folder', this.idNodeDoc);
            xhr.setRequestHeader('X-Group', selectTables);
            xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
        },
        sendingEventImage(file, xhr, formData) {
            var selectTables = []
            this.partx.forEach(function(val, index) {
                if (val.parts.toggle) {
                    selectTables.push(val.parts.id)
                }
            })
            xhr.setRequestHeader('X-Number', this.project.number);
            xhr.setRequestHeader('X-Folder', this.idNodeImg);
            xhr.setRequestHeader('X-Group', selectTables);
            xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
        },
        // sendingImageInGroupForDamages(file, xhr, formData) {
        //   var groups=[]
        //   this.loadDamages.forEach((v)=>{
        //     if(v.up==true){
        //       groups.push(v.id)
        //     }
        //   })
        //     xhr.setRequestHeader('X-Group-Id', groups.join());
        // },
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
            if (this.customer) return this.selectCustomer.name
        },
        getCustomerAdress() {
            if (this.customer) return this.selectCustomer.adress
        },
        getCustomerAdress1() {
            if (this.customer) return this.selectCustomer.adress1
        },
        getPerson() {
            if (this.person) return this.selectPerson.name
        },

        allSumms() {
          var allSumms = this.$t('projectDetail.general')+': ' + this.$options.filters.thousandSeparator(this.alltotal(this.partx));
          var altSumms = this.$t('projectDetail.alternative')+': ' + this.$options.filters.thousandSeparator(this.altalltotal(this.partx));
          var returnSumms = (this.altalltotal(this.partx)==0)?(allSumms):(allSumms + ' I ' + altSumms);
          if(this.dubTabIndex==0){
            setTimeout(() => {
              if(this.weval!=this.$refs.editList.$refs.editcomponet.clientHeight){
                this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 82)
              }
            }, 300);
          }
          return returnSumms;
        },
        alltotal: function() {
            var summa = 0

            this.partx.forEach(function(val) {
                val.parts.part_content.forEach(function(val1) {
                    if (val1.status == 'yes') {
                        summa += val1.count * val1.price
                        // console.log(val1.count+'*'+val1.price+'='+(val1.count * val1.price))
                    }
                })
            })
            // console.log('=='+summa+'==')
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
// inItemClickCotract(val){
//  var item = this.offers.filter(function(v){
//     if(v.id==val){
//       return v
//     }
//  })
// this.inItemClick(item[0], 0)
// }, 
//         inItemClick(item, index) {
//         this.tmp.typeOfHead = 'Offer',
//         this.tmp.number = item.offer_number,
//         this.tmp.date = item.date,
//         this.tmp.place = item.place,
//         this.tmp.insurname = item.insurname,
//         this.tmp.insurance = item.insurance_number,
//         this.tmp.work = item.work,
//         this.tmp.other = item.other,
//         this.tmp.type=item.type,
//         this.tmp.id=item.id,
//         this.tmp.comment=item.comment
//         axios.get('/table_data', {
//             params: {
//               id: item.id
//             }
//         }).then(response => {
//             this.partx=[],
//             response.data.forEach((val)=>{
//             var addofnew=0
//             this.partx.forEach((px)=>{
//               if(px.parts.part_name==val.part_name){
//                 addofnew=1
//               }
//             })
//             if(addofnew==0){
//             this.partx.push(
//                 {
//                         parts: {
//                             part_name: val.part_name,
//                             part_name_device: val.part_name_device,
//                             toggle: false,
//                             checkbox_list: {
//                                 flavours: {},
//                                 selected: {},
//                                 allSelected:  {},
//                                 indeterminate: {}
//                             },
//                             part_content: [{
//                                     upHere: false,
//                                     сheckbox: 'true',
//                                     count: val.count,
//                                     description_head: val.description_head,
//                                     description_work: val.description_work,
//                                     description_from_price: val.description_from_price,
//                                     discount: val.discount,
//                                     position_number: val.position_number,
//                                     price: val.price,
//                                     status: val.status,
//                                     alttax: val.alttax,
//                                     summa: val.summa,
//                                     unit: val.unit,
//                                     without: val.without,
//                                     done: val.done,
//                                     id_row: val.id,
//                                     item_id: val.item_id,
//                                     part_name: val.part_name
//                             }]
//                         }
//                   }
//             )
//           } else{
//             var indexOfPart=(this.partx.findIndex(x => x.parts.part_name == val.part_name))
// this.partx[indexOfPart].parts.part_content.push(
//                              {
//                                      upHere: false,
//                                      сheckbox: 'true',
//                                      count: val.count,
//                                      description_head: val.description_head,
//                                      description_work: val.description_work,
//                                      description_from_price: val.description_from_price,
//                                      discount: val.discount,
//                                      position_number: val.position_number,
//                                      price: val.price,
//                                      status: val.status,
//                                      alttax: val.alttax,
//                                      summa: val.summa,
//                                      unit: val.unit,
//                                      without: val.without,
//                                      done: val.done,
//                                      id_row: val.id,
//                                      item_id: val.item_id,
//                                      part_name: val.part_name
//                                  }
//                              )

//                   }
//         })
// })
//         },
//         inItemClickInvoice(item, index) {
//         this.tmp.typeOfHead = 'Invoice',
//         this.tmp.number = item.inoice_number,
//         this.tmp.date = item.date,
//         this.tmp.place = item.place,
//         this.tmp.insurance = item.insurance_number,
//         this.tmp.insurname = item.insurname,
//         this.tmp.work = item.work,
//         this.tmp.other = item.other,
//         this.tmp.type='invoice',
//         this.tmp.id=item.id
//         axios.get('/invoice_data_table', {
//             params: {
//               id: item.id
//             }
//         }).then(response => {
//              this.partx=[]
//             response.data.forEach((val)=>{
//             var addofnew=0
//             this.partx.forEach((px)=>{
//               if(px.parts.part_name==val.part_name){
//                 addofnew=1
//               }
//             })
//             if(addofnew==0){
//             this.partx.push({
//                             parts: {
//                             part_name: val.part_name,
//                             toggle: false,
//                             checkbox_list: {
//                                 flavours: {},
//                                 selected: {},
//                                 allSelected: {},
//                                 indeterminate: {}
//                             },
//                             part_content: [{
//                                     upHere: false,
//                                     сheckbox: 'true',
//                                     count: val.count,
//                                     description_head: val.description_head,
//                                     description_work: val.description_work,
//                                     description_from_price: val.description_from_price,
//                                     discount: val.discount,
//                                     position_number: val.position_number,
//                                     price: val.price,
//                                     status: val.status,
//                                     alttax: val.alttax,
//                                     summa: val.summa,
//                                     unit: val.unit,
//                                     without: val.without,
//                                     done: val.done,
//                                     id_row: val.id,
//                                     item_id: val.item_id,
//                                     part_name: val.part_name
//                                 }

//                             ]
//                         }
//                 }
//             )
//           } else{
//             var indexOfPart=(this.partx.findIndex(x => x.parts.part_name == val.part_name))
// this.partx[indexOfPart].parts.part_content.push(
//                              {      
//                                     upHere: false,
//                                     сheckbox: 'true',
//                                     count: val.count,
//                                     description_head: val.description_head,
//                                     description_work: val.description_work,
//                                     description_from_price: val.description_from_price,
//                                     discount: val.discount,
//                                     position_number: val.position_number,
//                                     price: val.price,
//                                     status: val.status,
//                                     alttax: val.alttax,
//                                     summa: val.summa,
//                                     unit: val.unit,
//                                     without: val.without,
//                                     done: val.done,
//                                     id_row: val.id,
//                                     item_id: val.item_id,
//                                     part_name: val.part_name
//                                  }

//                              )
                         
//                   }
//         })
// })
//         },
        // inItemClickPrice(item, index) {
        //     this.partx.forEach((valuePart, index)=> {
        //         if (valuePart.parts.toggle) {
        //             for (var property in valuePart.parts.checkbox_list.flavours) {
        //                 valuePart.parts.checkbox_list.flavours[property].push('temp' + valuePart.parts.checkbox_list.flavours[property].length)
        //             }
        //             valuePart.parts.part_content.push({ //сheckbox:item.checkbox,
        //                 position_number: item.position_number,
        //                 description_head: item.description_head,
        //                 description_work: item.description_work,
        //                 description_from_price: item.description_from_price,
        //                 count: item.count,
        //                 discount: item.discount,
        //                 price: item.price,
        //                 status: item.status,
        //                 alttax: false,
        //                 summa: item.summa,
        //                 unit: item.unit,
        //                 without: item.without,
        //                 upHere: false,
        //                 toggle: false,
        //                 сheckbox: item.сheckbox
        //             });
        //               this.funcStop=1
        //               axios.get('/add_part_form_price', {
        //                   params: {
        //                       part_name: valuePart.parts.part_name,
        //                       type: (this.tmp.type==undefined)?'invoice':this.tmp.type,
        //                       item_id: this.tmp.id,
        //                       position_number: item.position_number,
        //                       description_head: item.description_head,
        //                       description_work: item.description_work,
        //                       description_from_price: item.description_from_price,
        //                       count: item.count,
        //                       discount: item.discount,
        //                       price: item.price,
        //                       status: item.status,
        //                       alttax: false,
        //                       summa: item.summa,
        //                       unit: item.unit,
        //                       without: item.without
        //                    }
        //               }).then(response =>{
        //                 this.funcStop=0
        //               })
        //         }
        //     });
        // },
inItemClickDamage(item, index) {
  this.tmp.typeOfHead = 'Damage',
  this.tmp.number = item.damage_number,
  this.tmp.place = item.place,
  this.tmp.insurance = item.insurance_number,
  this.tmp.insurname = item.insurname,
  this.tmp.work = item.work,
  this.tmp.other = item.other,
  this.tmp.type='damage',
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
  this.workerModal=true
},
closeWorkerModal(){
  this.workerModal=false;
  if (this.comtomodal!=null) this.tabxmodal=true;
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
        // keyupMethod(event) {
        //     if (event.keyCode === 113) {
        //         this.tmouseOver()
        //     }
        //     if (event.keyCode === 27) {
        //         this.mouseOut()
        //     }
        // },
        // tmouseOver: function() {
        //     this.show = true;
        // },
        // mouseOut: function() {
        //     this.show = false;
        // },
        // newTab() {
        //     this.tabs.push(this.tabCounter++)
        // },
        addOk(work) {
            this.addSameModalWindow=false
            if (this.comtomodal!=null) this.tabxmodal=true
               axios.get('/add_same', {
                    params: {
                        add_number: (this.project.number==null)?'0001':this.project.number,
                        add_insurance_number: '', // this.add_offer.insurance_number
                        add_place: '', // this.add_offer.place
                        add_work: work, // this.add_offer.work
                        add_comment: '', // this.add_offer.comment
                        add_project_id: this.id,
                        type: 'Offers'
                    }
                }).then(response => {
                    axios.get('/project_detail_new', {
                      params: {
                        id: this.id
                      }
                    }).then(response => {

                        this.itemsTable = response.data;
                    })
                })
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
            }
        },
        docDel(id, number) {
            if (confirm(this.$t('alert.sure'))) {
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
            if (confirm(this.$t('alert.sure'))) {
                axios.get('/del_file', {
                    params: {
                        id: id,
                        number: number
                    }
                }).then(response => {
                    this.files = response.data
                })
            }
        },
        filedel(val) {
            if (confirm(this.$t('alert.sure'))) {
                axios.get('/delfile', {
                    params: {
                        id: val
                    }
                }).then(response => {});
            }
        },





/////////////////////////////////////////////////////////////////////  component for files function
getItems(type){
  if (type != 'Orders'){
    if (type != 'SUB'){
        if (type != 'Sub Invoices'){
          if (type != 'Invoices'){
            return this.itemsTable.filter((v)=>{
              if (v.type == type){
                v._rowVariant = (v.id==this.selrow)?'secondary':''
                return v }})}}}}

if (type == 'Orders')  {
  var orderandsub = []
  var onlisub = []
  this.itemsTable.forEach((v)=>{
    if (v.type == 'Orders'){
      v._rowVariant = (v.id==this.selrow)?'secondary':''
      var xid = v.id
      onlisub = []
      this.itemsTable.forEach((vx)=>{
        if (vx.type == 'SUB'){
          var intId=parseInt(vx.number.split(' ')[1])
          if (xid == intId) {
            vx._rowVariant = "primaryHide"
            this.showsubarr.forEach((ss)=>{
              if (intId == ss) {
                vx._rowVariant = (vx.id==this.selrow)?'secondary':''
              }
            })
                 onlisub.push(vx)
          }
        }
      })
      var mer=[]
      mer.push(v)
      var segmer =  mer.concat(onlisub)
      orderandsub = JSON.parse(JSON.stringify(orderandsub.concat(segmer)));
    }
  })
  return orderandsub
  }

  if (type == 'Invoices'){
    var invoices =[]
    this.itemsTable.forEach((v)=>{
      if(v.type == 'Invoices'){
        v._rowVariant = (v.id==this.selrow)?'secondary':'',
        invoices.push(v)
      }
      if(v.type == 'Sub Invoices'){
        v._rowVariant = (v.id==this.selrow)?'secondary':'',
        invoices.push(v)
      }
    })
    return invoices
  }
},
//////////////////////////////////////
///////////////////////////////////////component
pinItemGetData(item, index) {
  this.inItemGetData(item, index)


},
pgetcontact(id){
this.get_contact(id)
},
pgetperson(id, mnew){
this.get_person(id, mnew)
},
pofferDel(del_id){
this.offerDel(del_id)
},
paddOk(work){
this.addOk(work)
},

inItemGetData(item, index) {
      if (item!=undefined) {
  axios.get('/get_plan', {
    params: {
      id: item.id
    }
  }).then(response => {
      this.plan = response.data
 
      this.selrow = item.id,
      item._rowVariant = (item.id==this.selrow)?'secondary':'',
      this.generalComments=false,
      this.tmp.typeOfHead = item.type,
      // console.log(item.type),
      this.beforeTab = item.type,
      this.tmp.number = item.number,
      this.tmp.date = item.date,
      this.tmp.place = item.place,
      this.tmp.insurance = item.insurance_number,
      this.tmp.insurname = item.insurname,
      this.tmp.work = item.work,
      this.tmp.other = item.other,
      this.tmp.type=item.type,
      this.tmp.id=item.id,
      this.tmp.dateEvent = item.dateEvent,
      this.tmp.dateInspect = item.dateInspect,
      this.tmp.worker = item.ExamWorker,
      this.tmp.comment=item.comment
       })
      }

    setTimeout(() => {
      // console.log(this.tabxmodal)

          if (this.$refs.editList != undefined) {
            if (item != undefined) {
              this.$refs.editList.remoteTax(item.id)
            }
          }
      
      // this.$refs.edit1.remoteTax(item.id)

     
    }, 300)
  // }
},

//////////////////////////////////////////////////
get_person(id, mnew){
  // console.log(2)
    axios.get('/get_persons', {
      params: {
      id: id
      }
      }).then(response => {
        this.availablePersons=[]
        response.data.forEach((it)=>{
        this.availablePersons.push({id:it.person, name:it.appeal+' '+it.names})
      })
      this.availablePersons.sort(function(a, b){
        var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase()
        if (nameA<nameB) return -1
        if (nameA>nameB) return 1
        return 0 
      })
      // this.area = this.area.filter((it)=>{
      //   if (it.id!=0){return it}
      // })
      if(mnew==true){
        this.selectPerson={id:this.availablePersons[0].id, name:this.availablePersons[0].name}
        this.get_contact(this.selectPerson.id)
      }
    })
},
get_contact(id){
  axios.get('/get_contact_person', {
    params: {
    id: id
    }
    }).then(response => {
      this.availableMails=[]
      this.availablePhons=[]
      this.availableMails = response.data.mail
      // console.log(response.data.mail)
      this.availablePhons = response.data.phone
      this.selectMail=this.availableMails[0]?this.availableMails[0].mail:null
      this.selectPhone=this.availablePhons[0]?this.availablePhons[0].phone:null
    })
},

get_types_for_tables_f(call){
  axios.get('/get_types_for_tables', {
  }).then(response => {
    this.typesForTables = response.data.filter(function (v){
      if((v.type!='SUB')&&(v.type!='Sub Invoices')&&(v.type!='Damage Description')){
        return v
      }
    });
  });
  if (call=='socket'){
    this.project_detail_new_f()
  }
},
get_workers_f(){
  axios.get('/get_workers', {
  }).then(response => {
    this.workers = [],
    response.data.forEach((v)=>{
      this.workers.push((v.short_name!=null)?v.short_name:v.name),
      this.workersForSend.push({'value':v.id, 'text':((v.short_name!=null)?v.short_name:v.name)})   
    })
  })
},
get_type_works(){
  axios.get('/get_type_works', {
  }).then(response => {
    this.works = response.data;
    this.works.unshift(this.$t('calcTableGroup.work'))
  })
},

// pimageInTableSelected(item){
//   item._rowVariant=(item._rowVariant=='success')?'':'success';
// },

// pchvalueimages(val){
//   this.selectedDamageImages=val
// },
// pselectimagesarr(group){
// var imagesarr = []
// if (this.selectedDamageImages=='Image'){
//   this.domageImages.forEach((si)=>{
//     if(si._rowVariant=='success'){
//        imagesarr.push(si.id.split('=')[1])
//     }
//   })
//   this.updatefilenames(group, 'group',imagesarr.join())
// }
// // console.log(this.groupByFild(this.selectedDamageImages))
//   // if (op=='-'){
//   //   this.selectedImages.splice(this.selectedImages.indexOf(it), 1)
//   // }
// },
project_detail_new_f(){

  // var optImages = [{id:0, value:'Undefined'}]
  axios.get('/project_detail_new', {
    params: {
      id: this.id
    }
  }).then(response => {
    response.data.filter((v)=>{

    // axios.get('/get_tables', {
    //   params: {
    //     id: v.id
    //   }
    // }).then(response => {
      // if ((v.type!='Invoices') && (v.type!='Sub Invoices')) {
      //   for (let i = 0; i < (response.data.length-1); i++) {
      //       optImages.push({id:response.data[i].parts.id, value:response.data[i].parts.part_name})
      //   }
      // }
      // if(optImages!=this.optImages){
      //   this.optImages = optImages
      // }
    // })
       if(v.number.split(' ').length!=5){
        v.netto = this.$options.filters.thousandSeparator(parseFloat(v.netto));
        v.brutto = this.$options.filters.thousandSeparator(parseFloat(v.brutto));
      } else{
        v.netto = '-'+this.$options.filters.thousandSeparator(parseFloat(v.netto));
        v.brutto = '-'+this.$options.filters.thousandSeparator(parseFloat(v.brutto));
      }
      return v;
    })
    this.itemsTable = response.data;
    setTimeout(() => {
        this.sm2lg('component', this.$refs['hproject'].clientHeight, 110)
        this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 56)
        
    }, 10);
    if (this.tmp.id!=undefined){
      var item_list = this.itemsTable.filter((v)=>{
        if (v.type == 'Orders' || v.type == 'Offers'){
          if (v.id == this.tmp.id){
            return v
          }
        }
      })
         this.inItemGetData(item_list[0], 0)
    }
  })
},
getLoocks(){
   axios.get('/getLoocks').then(response => {
      this.looks=[]
      this.looks = response.data
  })
},
project_detail_f(old){

  axios.get('/project_detail', {
        params: {
              id: this.id
        }
  }).then(response => {
     // console.log(response.data)
                      if (response.data!=null){
                      var num = response.data.project_number
                      var nuls=3-num.toString().length
                      for (var i = 0; i <= nuls; i++) {
                          num='0'+num
                      }
                      this.project.work=response.data.work,
                      this.project.number= num+((this.hideNumberOfYear!=1)?('-' + response.data.project_number_year):''),
                      this.project.date=response.data.date,
                      this.project.edate=response.data.edate,
                      this.project.street1=response.data.street1,
                      this.project.city1=response.data.city1,
                      this.project.area=response.data.area,
                      this.selectedCornty=(this.countries[this.countries.findIndex(x => x.code == response.data.country)])?this.countries[this.countries.findIndex(x => x.code == response.data.country)]:{code: null},
                      this.project.zip1=response.data.zip1,
                      this.project.other=response.data.other,
                      this.project.editor=response.data.first_name + ' ' + response.data.second_name,
                      this.selectCustomer={id:response.data.customer_id, name:response.data.name, adress:response.data.street, adress1:response.data.zip+' '+response.data.city,  customerMail:response.data.customerMail},
                      this.area=[{id:response.data.customer_id, name:response.data.name, adress:response.data.street, adress1:response.data.zip+' '+response.data.city}],
                      this.selectPerson={id:response.data.person_id, name:response.data.appeal+' '+response.data.names},
                      this.get_contact(this.selectPerson.id),
                      this.availablePersons=[{id:response.data.person_id, name:response.data.appeal+' '+response.data.names}],
                      // this.selectMail={id:response.data.mail, name:response.data.names}
                      // this.availableMails.push(response.data.customerMail)
                      // this.selectPhone={id:response.data.phone, name:response.data.names}
                      // this.availablePhons=[{id:response.data.phone, name:response.data.names}]
                      
                      // this.docs2files()
                      // this.getdomageImages()

                
                      
                      axios.get('/customer').then(response => {

                        response.data.forEach((it)=>{
                          if(this.selectCustomer.id!=it.id) this.area.push({id:it.id, name:it.name})
                        })
                        // console.log(this.selectCustomer.customerMail)
                        this.area.sort(function(a, b){
                          var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase()
                          if (nameA<nameB) return -1
                          if (nameA>nameB) return 1
                          return 0 
                        })
                      })
                     this.get_person(this.selectCustomer.id, false)
                    }
        })

},
getProjectDetail(old){
  // alert()
  axios.get('/date_logo').then(response => {
          var separator = response.data.date_logo_address.split('- ')[0]+'- ';
          var address = response.data.date_logo_address.split(separator)[1];
          this.mail_address = address;
          this.mail_logo = response.data.date_logo_image;
          this.mail_date = response.data.date_logo.match(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig)[0];
          
        })


  if (this.typesForTables.length==0){
    this.get_types_for_tables_f('native')
  }
    this.project_detail_new_f()
  if (this.workers.length==0){
    this.get_workers_f()
  }
  if(this.tmp.number!=null){
    var cliked = this.itemsTable.filter((val)=>{
      if (val.id==this.tmp.id){
        return val
      }
    })
    this.countCall = this.countCall + 1
    this.inItemGetData(cliked[0], 0)
  }
  // console.log(0)
    this.project_detail_f(old)
    this.project_id=this.id
}
},
  watch: {
    tabIndex: function(newv, oldv){
      if (oldv!=null){
        if (newv==0){
          setTimeout(() => {
              this.sm2lg('component', this.$refs['hproject'].clientHeight, 110)
          }, 10);
        }
      }

    },
    wwidth: function() {
      if ((this.wcval!=null)&&(this.wcadd!=null)){
        this.sm2lg('component', this.wcval, this.wcadd)
      }
      if ((this.weval!=null)&&(this.weadd!=null)){
        this.sm2lg('edit', this.weval, this.weadd)
      }
    },
    mapmodal: function(value) {
      if (value == false){
        this.mapmodalhide()
      }
    },
    mailmodal: function(value) {
      if (value == false){
        this.mailmodalhide()
      }
    },

    dubTabIndex: function(value){
          if(this.$refs.devices!=undefined){
            if (this.$refs.devices.localActive){
              this.tmp.typeOfHead = 'Devices'
            }
          }
          if(this.$refs.damage!=undefined){
            if (this.$refs.damage.localActive){
              this.tmp.typeOfHead = 'Damage'
            }
          }
          if (((this.$refs.devices==undefined)||(this.$refs.devices.localActive==false))&&
            ((this.$refs.damage==undefined)||(this.$refs.damage.localActive==false))){
              this.tmp.typeOfHead = this.beforeTab
          }
    }






    // tabxmodal:function(value) {
    //    if (value == false){
    //     this.comtomodal=null
    //   }
    // }
  }, 
      mounted(){
      axios.get('/countries').then(response => {
        this.countries=response.data
      });
      axios.get('/variables').then(response => {
        this.addressfild=response.data[1].content.split(' ').join('+')
        this.beforeSubject=response.data[2].content
        this.beforeMail=response.data[3].content
        this.hideNumberOfYear = response.data[4].content
      });
      this.getProjectDetail(1);
      this.get_type_works();
     setTimeout(() => {
        this.getPrices();
        this.getDevices();
        this.getDocs();
        // this.$socket.send('getProjectDetail')
        // this.$socket.send('get_type_works')
        // this.$socket.send('getPrices')
        // this.$socket.send('getDevices')
        // this.$socket.send('getDocs')

       

        this.$options.sockets.onmessage = (data) => (data.data=='getProjectDetail') ? (this.getProjectDetail(1)): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_types_for_tables_f') ? (this.get_types_for_tables_f('socket')): ''
        this.$options.sockets.onmessage = (data) => (data.data=='project_detail_new_f') ? (this.project_detail_new_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_workers_f') ? (this.get_workers_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_type_works') ? (this.get_type_works()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getLoocks') ? (this.getLoocks()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getDevices') ? this.getDevices(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getDocs') ? this.getDocs(): ''
        // this.displaytime()
        },1000);
        },
    created: function() {
      const onResize = () => this.wwidth = window.innerWidth; //После определения ширина окна и  мобильного режима, должна примениться рассчитаная длина списка
      onResize();
      window.addEventListener('resize', onResize);
      this.$once('hook:beforeDestroy', () => window.removeEventListener('resize', onResize));
    }
}
</script>
<style type="text/css">
.cheboxscorl {
    overflow-x: hidden;
    height: 200px;
    overflow-y: auto;
}

.raz { 
  -moz-appearance: textfield;
}
.raz::-webkit-inner-spin-button { 
  display: none;
}

@media only screen and (min-width : 992px) {
  .b-table-sticky-header {
    overflow-y: auto;
    max-height: 100%
  }
  .b-table-sticky-header > .table.b-table > thead > tr > th {
    position: sticky !important;
    background-color: #fff;
  }
  .block-1 {
    height: calc(87vh - 7rem);overflow-y: auto;
  }
  .block-2 {
    height: calc(87vh - 7rem);overflow-x: hidden; overflow-y: hidden;
  }
  .editorsm2lg{
    height: calc(85vh - 5rem);position:relative;top:-20px;z-index:1;
  }
  .forFinger{
    display: none;
  }
/*  .cardimg img{
    max-height:250px;
    max-width:250px; //нужна пропорция при изминении размера
  }*/
  .cardimg .card-body{
    height: 100% !important;
  }
}
@media only screen and (max-width : 992px) { 
  .cardimg .card-body{
/*    height: 27px !important;
    overflow-y: hidden !important;*/
    display: none !important;
  }
  .tabs{
    min-height: 100vh;
  }
  .b-table-sticky-header {
    max-height: unset;
  }
  .sticky-header-lg{
    overflow-x:hidden;
  }
  .printForMobile{
    display: none;
  }
}
.dropzone .dz-preview .dz-image {
  width: 250px !important;
  height: 250px !important;
}



</style>