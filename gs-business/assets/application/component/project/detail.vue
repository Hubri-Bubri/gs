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

<b-modal size="sm" centered  title="Select Workers" body-class="workerHeight" v-model="workerModal"  no-close-on-esc no-close-on-backdrop hide-header-close>
        <b-form-input type="text" v-model="searchWorker" style="margin-bottom: 4px !important;"/>
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="workers"/>
            <template slot="modal-footer">
                  <b-container fluid>
                    <b-row  align-h="between">
                      <b-col class="text-left">
                        <b-button type="button" variant="primary" @click="selectedWorkers=[]">Clear</b-button>
                      </b-col>
                      <b-col class="text-right">
                        <b-button type="button" variant="primary" @click="closeWorkerModal">OK</b-button>
                      </b-col>
                    </b-row>
                  </b-container>
           </template>
        </b-modal>

<b-modal size="lg" centered ok-only id="map" title="Track"  v-model="mapmodal" no-close-on-esc no-close-on-backdrop hide-header-close>
  <b-embed type="iframe" aspect="16by9"
    :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
    'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+'destination='+project.street1">
  </b-embed>
<template slot="modal-footer">
<b-button type="button" variant="outline-secondary"  @click="mapmodalhide">Close</b-button>
</template>
</b-modal>

          <b-form @submit.prevent="addOk">
            <b-modal size="md" centered  v-model="addSameModalWindow" :title="'Add Offers'"  no-close-on-esc no-close-on-backdrop hide-header-close>
                <b-form-group horizontal :label-cols="4" label="Order #:" label-for="OrderNumber" style="padding: 5px;">
                    <b-form-input v-model="project.number" class="cForm-input" id="OrderNumber" disabled :state="null" type="text" placeholder="Enter number" />
                </b-form-group>
                <b-form-group horizontal :label-cols="4" label="Type Of Work:" label-for="work" style="padding: 5px;">
                    <b-form-select class="select" id="work" :options="works" v-model="add_offer.work" required />
                </b-form-group>
                <template slot="modal-footer">
                  <b-container fluid>
                    <b-row  align-h="between">
                      <b-col class="text-left">
                        <b-button @click="closeaddok" variant="primary">
                            Close
                        </b-button>
                      </b-col>
                      <b-col class="text-right">
                        <b-button type="submit" variant="primary">
                            Add
                        </b-button>
                      </b-col>
                    </b-row>
                  </b-container>
                </template>
            </b-modal>
        </b-form>
  <b-modal class="mail" centeredbody-class="workerHeight" v-model="mailmodal" no-close-on-esc no-close-on-backdrop hide-header-close>
          <b-row>
            <b-col cols="12" md="4">
              <b-form-checkbox-group buttons text-field="name" value-field="item" button-variant="light" v-model="mailSelect"
              stacked style="width:100%" class="sleft cheboxscorl" :options="filtered(((abook==false)?modalMail:abooklist),searchmail)" />
       
              <b-input-group>
              <b-form-input type='text' placeholder="Search mail adress" v-model="searchmail" />
                <b-input-group-append>
                   <b-form-checkbox-group buttons
                   button-variant="outline-secondary"
                      stacked
                      @change="cheabook"
                      v-model="abook" 
                      :options="['Address Book']">
                    </b-form-checkbox-group>
                  </b-input-group-append>
              </b-input-group>
            </b-col>
            <b-col cols="12" md="8"><div class="cheboxscorl">
              <b-form-checkbox-group buttons text-field="name" value-field="item"
              button-variant="light" v-model="selectedFiles"
              stacked style="width:100%" class="sleft"
              :options="filtered(modalFiles, searchfile)" />
                </div>
              <b-form-input type='text' placeholder="Search name of file" v-model="searchfile" />
            </b-col>
          </b-row>
          <br>
            <b-form-input type='text' placeholder="Subject" v-model="subject" />
<vue-editor id="content" ref="content" class="mail" v-model="content" :editorToolbar="customToolbar" />
<template slot="modal-footer">

<b-button type="button" variant="outline-secondary"  @click="mailmodalhide">Close</b-button>

  <b-input-group v-if="(selectedFiles && selectedFiles.length ? selectedFiles.length : 0)>=2">
    <b-input-group-prepend>
      <b-form-checkbox-group buttons
        stacked
        button-variant="outline-secondary"
        @change="checkattach('chek')"
        v-model="split" 
        :options="['Split']">
      </b-form-checkbox-group>
    </b-input-group-prepend>
    <b-form-input type="text" v-model="filename" @input="checkattach('inp')" placeholder="Name of single attachment"></b-form-input>
  </b-input-group>
  <div v-else style="width:100%"> </div>

            <b-button  @click="sendmail()" variant="outline-secondary">Send</b-button>
           </template>
        </b-modal>


<b-modal class="mail" v-model="tabxmodal" centered no-close-on-esc no-close-on-backdrop hide-header-close>
  <template #modal-header>

    <span v-if="(comtomodal!='pricelist') && (comtomodal!='deviceslist')">{{titlex}}</span>

    <span v-b-toggle.priceMenu  v-if="comtomodal=='pricelist'">Price List</span>
    <span v-b-toggle.devicesMenu  v-if="comtomodal=='deviceslist'">Devices List</span>
  
  </template>
  <project v-if="comtomodal=='project'"
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

  @addSameModal="addSameModal"
  @openmap="mapmodalshow"
  @sendMail="sendMail"
  @offerDel="pofferDel"
  @inItemGetData="pinItemGetData"
  @getcontact="pgetcontact"
  @getperson="pgetperson"
  @showCommetnts="showCommetnts()"
  ></project>
  <price v-if="comtomodal=='pricelist'"
  :howhight="37"
  :idNode="idNode"
  :parId="parId"
  :items="itemsPrice"
  :itemsMenu="itemsMenu"
  :oldId="oldId"
  :selectedPrice="selectedPrice"
  @rowSelected="prowSelected"
  @curNodeClicked="pcurNodeClicked"
  ></price>
  <devices v-if="comtomodal=='deviceslist'"
  :howhight="37"
  :idNodeDev="idNodeDev"
  :parIdDev="parIdDev"
  :itemsDev="itemsPriceDev"
  :itemsMenuDev="itemsMenuDev"
  :oldIdDev="oldIdDev"
  :selectedPriceDev="selectedPriceDev"
  @curNodeClickedDev="pcurNodeClickedDev"
  @rowSelectedDev="prowSelectedDev"
  ></devices>
  <docs v-show="comtomodal=='docs'"
  :t="1"
  :responseFiles="responseFiles"
  :fieldsDocs="fieldsDocs"
  ref="docs1"
  @filedel="filedel"
  @updatefilename="updatefilename"
  @updatedocname="updatedocname"
  @changeDisable="changeDisable"
  @loadDocToFrame="ploadDocToFrame"
  ></docs>
  <images v-show="comtomodal=='images'"
  :domageImages="domageImages"
  :fieldsImages="fieldsImages"
  :selectedDamageImages="selectedDamageImages"
  :optImages="optImages"
  @resetFilds="presetFilds"
  @chvalueimages="pchvalueimages"
  @selectimagesarr="pselectimagesarr"
  @updatefilename="updatefilename"
  @allselrow="pallselrow"
  @allselrowin="pallselrowin"
  @showx="showx"
  @filedel="filedel"
  @imageInTableSelected="pimageInTableSelected"
  ></images>
  <edit ref="edit1" v-show="comtomodal=='edit'"
  :tmp="tmp"
  :project="project"
  :looks="looks"
  :works="works"

  :selectedCornty="selectedCornty"
  :id="id"
  :comments="comments"
  :responseFiles="responseFiles"
  :typesForTables="typesForTables"
  :workers="workers"
  :funcStop="funcStop"
  
  :partx="partx"
  :customer="customer"
  :person="person"
  :selectCustomer="selectCustomer"
  :selectPerson="selectPerson"
  :windowPrint="windowPrint"
  :selectedWorkers="selectedWorkers"
  :typeDocsList="typeDocsList"


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
  <edevices  v-if="comtomodal=='devices'"
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
  ></edevices> 
  <template slot="modal-footer">
    <b-col  align-self="end">
      <b-button v-if="(comtomodal=='docs') || (comtomodal=='images') || (comtomodal=='edit') || (comtomodal=='project') || (comtomodal=='devices')"
      type="button" variant="outline-secondary"  @click="tabxmodal=false;comtomodal=null;">Close</b-button>
    </b-col>


    <b-form-row v-if="comtomodal=='pricelist'" class="w-100">
      <b-col lg="1" cols="3" style="padding:1px;text-align:left;"><b-button type="button"  variant="outline-secondary"  @click="tabxmodal=false;comtomodal=null;">Close</b-button></b-col>
      <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addPrice">+Part</b-button></b-col>
      <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100"  style="padding-left:0px;padding-right:0px;" @click="removePrice">Remove</b-button></b-col>
      <b-col lg="7" cols="12" style="padding:1px;"><b-form-input class="w-100" v-model="nameNode" :style="nodeDis?'background-color:grey':''"
      @click.native="nodeDis?nodeDisTurn():''" @change="nodeDis=true;toModel(nameNode)"></b-form-input>
      </b-col>
      <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="addRowPrice">+Row</b-button></b-col>
      <!-- <b-col lg="1" cols="3" style="padding:1px;"><b-button class="w-100" @click="mv_cpPrice">mv/cp</b-button></b-col> -->
      <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="sendPrice">Send</b-button></b-col>
    </b-form-row>
    <b-form-row v-if="comtomodal=='deviceslist'" class="w-100">
      <b-col lg="1" cols="3" style="padding:1px;text-align:left;"><b-button type="button"  variant="outline-secondary"  @click="tabxmodal=false;comtomodal=null;">Close</b-button></b-col>
      <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addDevice">+Part</b-button></b-col>
      <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100"  style="padding-left:0px;padding-right:0px;" @click="removeDevice">Remove</b-button></b-col>
      <b-col lg="7" cols="12" style="padding:1px;"><b-form-input class="w-100" v-model="nameNodeDev" :style="nodeDisDev?'background-color:grey':''"
        @click.native="nodeDisDev?nodeDisTurnDev():''" @change="nodeDisDev=true;toModelDev(nameNodeDev)"></b-form-input>
      </b-col>
      <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="addRowDevice">+Row</b-button></b-col>
      <!--  <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="mv_cpDevice">mv/cp</b-button></b-col> -->
      <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="sendDevice">Send</b-button></b-col>
    </b-form-row>
    <b-container v-if="comtomodal=='docs'" fluid>
      <b-collapse v-model="dropDoc" id="dropDoc1">
        <vue-dropzone ref="myVueDropzone1" id="dz1" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd1">
        </vue-dropzone>
      </b-collapse>
      <div style="background-color:#ced4da">
        <b-link class="input-group-text " style="text-decoration: none;font-weight: normal; With:100%" @click="dropDoc=dropDoc?false:true">
          <span class="when-closed"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder" aria-hidden="true"></i></span>
          <span class="when-opened"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder-open" aria-hidden="true"></i></span>
        </b-link>
      </div>
    </b-container>
    <b-container v-if="comtomodal=='images'"  fluid>
      <b-collapse id="dropImage4"  v-model="dropImage" >
        <vue-dropzone ref="myVueDropzone4" id="dz4" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd4">
        </vue-dropzone>
      </b-collapse>
      <div style="background-color:#ced4da">
        <b-link class="input-group-text " style="text-decoration: none;font-weight: normal; With:100%" @click="dropImage=dropImage?false:true">
          <span class="when-closed"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder" aria-hidden="true"></i></span>
          <span class="when-opened"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder-open" aria-hidden="true"></i></span>
        </b-link>
      </div>
    </b-container>
    <b-container v-if="comtomodal=='edit'" fluid>
      <b-collapse id="editor1">
        <vue-editor id="refCommentOfTable" ref="refCommentOfTable" v-model="tmp.comment" @blur="updateItem(tmp.comment, 'comment', tmp.id)">
        </vue-editor>
      </b-collapse>
      <b-input-group>
        <b-input-group-prepend>
          <b-link class="input-group-text " style="text-decoration: none;font-weight: normal;" v-b-toggle="'editor1'">
            <span class="when-closed">+</span>
            <span class="when-opened">-</span>
          </b-link>                        
        </b-input-group-prepend>
        <b-form-input id="netto" :state="null" type="text" disabled class=" text-right" :value="allSumms()" />
        <b-input-group-append>
          <div class="input-group-text ">€</div>
        </b-input-group-append>
      </b-input-group>
    </b-container>
  </template>
</b-modal>

        <container-header class="container-fluid">
            <top-menu>
            </top-menu>
        </container-header>
        <container-body class="container-fluid" >
            <b-card-group deck>
                <b-card no-body class="gs-container">
                    <b-tabs card v-model="tabIndex" >
                        <b-tab>
                        <template #title>
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange(projectfild.content, 'project')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                            </svg>
                            {{projectfild.content}}
                        </template>
                        <container>
                            <container-body  style="overflow-x: hidden;" ref="project">
                              <b-container>
                               <project
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
                            <div style="width:100%"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Price List', 'pricelist')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                            </svg> <span v-b-toggle.priceMenu>Price List</span></div>
                        </template>
                        <container>
                          <container-body >
                            <price v-if="(tabIndex==1) && (comtomodal!='pricelist')"
                            :howhight="105"
                            :idNode="idNode"
                            :parId="parId"
                            :items="itemsPrice"
                            :itemsMenu="itemsMenu"
                            :oldId="oldId"
                            :selectedPrice="selectedPrice"

                            @curNodeClicked="pcurNodeClicked"
                            @rowSelected="prowSelected"
                            ></price>
                    
                          </container-body>

                <container-footer>
                        <b-form-row>
                            <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addPrice">+Part</b-button></b-col>
                            <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100"  style="padding-left:0px;padding-right:0px;" @click="removePrice">Remove</b-button></b-col>
                            <b-col lg="8" cols="12" style="padding:1px;"><b-form-input class="w-100" v-model="nameNode" :style="nodeDis?'background-color:grey':''"
                                @click.native="nodeDis?nodeDisTurn():''" @change="nodeDis=true;toModel(nameNode)"></b-form-input>
                            </b-col>
                            <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addRowPrice">+Row</b-button></b-col>
                            <!-- <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="mv_cpPrice">mv/cp</b-button></b-col> -->
                            <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="sendPrice">Send</b-button></b-col>
                        </b-form-row>
                </container-footer>
         

                          </container>
                        </b-tab>
<b-tab style="padding:0px;"  >
                        <template #title>
                            <div style="width:100%"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Devices List', 'deviceslist')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                            </svg> <span v-b-toggle.devicesMenu>Devices List</span></div>
                        </template>
                        <container>
                          <container-body >
                            <devices v-if="(tabIndex==2) && (comtomodal!='deviceslist')"
                            :howhight="105"
                            :idNodeDev="idNodeDev"
                            :parIdDev="parIdDev"
                            :itemsDev="itemsPriceDev"
                            :itemsMenuDev="itemsMenuDev"
                            :oldIdDev="oldIdDev"
                            :selectedPriceDev="selectedPriceDev"

                            @curNodeClickedDev="pcurNodeClickedDev"
                            @rowSelectedDev="prowSelectedDev"
                            ></devices>
                          </container-body>
                        <container-footer>
                          <b-form-row>
                              <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addDevice">+Part</b-button></b-col>
                              <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" style="padding-left:0px;padding-right:0px;" @click="removeDevice">Remove</b-button></b-col>
                              <b-col lg="8" cols="12" style="padding:1px;"><b-form-input class="w-100" v-model="nameNodeDev" :style="nodeDisDev?'background-color:grey':''"
                                  @click.native="nodeDisDev?nodeDisTurnDev():''" @change="nodeDisDev=true;toModelDev(nameNodeDev)"></b-form-input>
                              </b-col>
                              <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="addRowDevice">+Row</b-button></b-col>
                             <!--  <b-col lg="1" cols="4" style="padding:1px;"><b-button class="w-100" @click="mv_cpDevice">mv/cp</b-button></b-col> -->
                              <b-col lg="1" cols="6" style="padding:1px;"><b-button class="w-100" @click="sendDevice">Send</b-button></b-col>
                          </b-form-row>
                        </container-footer>
         

                          </container>
                        </b-tab>
                        <b-tab>
                          <template #title>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Docs', 'docs')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                              </svg> Docs
                          </template>
                            <container>
                               <container-body  style="overflow-x: hidden;">
                                    <docs
                                    :responseFiles="responseFiles"
                                    :fieldsDocs="fieldsDocs"
                                    :t="2"
                                    ref="docs2"
                                    @filedel="filedel"
                                    @updatefilename="updatefilename"
                                    @updatedocname="updatedocname"
                                    @changeDisable="changeDisable"
                                    @loadDocToFrame="ploadDocToFrame"
                                    >
                                    </docs>
                                </container-body>
                                <b-container  fluid>
                                    <b-collapse v-model="dropDoc" id="dropDoc3">
                                        <vue-dropzone ref="myVueDropzone3" id="dz3" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd3">
                                        </vue-dropzone>
                                    </b-collapse>
                                    <div style="background-color:#ced4da">
                                        <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal; With:100%" @click="dropDoc=dropDoc?false:true">
                                            <span class="when-closed"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder" aria-hidden="true"></i></span>
                                            <span class="when-opened"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder-open" aria-hidden="true"></i></span>
                                        </b-link>
                                    </div>
                                </b-container>
                            </container>
                        </b-tab>


                        <b-tab>

                            <template #title>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Images', 'images')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                              </svg> Images
                          </template>

                          <container>
                            <container-body  style="overflow-x: hidden;" ref="images">

                             <images
                             :domageImages="domageImages"
                             :fieldsImages="fieldsImages"
                             :selectedDamageImages="selectedDamageImages"
                             :optImages="optImages"
                             @resetFilds="presetFilds"
                             @chvalueimages="pchvalueimages"
                             @selectimagesarr="pselectimagesarr"
                             @updatefilename="updatefilename"
                             @allselrow="pallselrow"
                             @allselrowin="pallselrowin"
                             @showx="showx"
                             @filedel="filedel"
                             @imageInTableSelected="pimageInTableSelected"
                             ></images>
                            </container-body>
                             <b-container fluid>
                                    <b-collapse id="dropImage2"  v-model="dropImage" >
                                        <vue-dropzone ref="myVueDropzone2" id="dz2" :options="dropzoneOptions"v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd2">
                                        </vue-dropzone>
                                    </b-collapse>
                             <b-input-group>
                                        <b-link class="input-group-text form-control lablelInInput" style="border-radius:0px;text-decoration:none;font-weight:normal;background-color:#ced4da;" @click="dropImage=dropImage?false:true">
                                            <span class="when-closed"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder" aria-hidden="true"></i></span>
                                            <span class="when-opened"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder-open" aria-hidden="true"></i></span>
                                        </b-link>
                                          <b-input-group-append>
                                             <b-button v-show="butifsel()" @click="sendtodamage()" class="lablelInInput" style="padding-top:0px;padding-bottom:0px;line-height:18px;border-radius: 0px;">Send</b-button>
                                         </b-input-group-append>
                               </b-input-group>
                                </b-container>
                          </container>
                        </b-tab>
                    </b-tabs>
                </b-card>
                <b-card no-body class="gs-container">
                    <b-tabs card v-model="dubTabIndex">
                        <b-tab ref="Edit">
                          <template #title>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Edit', 'edit')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                              </svg> Edit
                          </template>
                            <container>
                                <container-body >
                                  <edit ref="edit"
                                  :tmp="tmp"
                                  :project="project"
                                  :looks="looks"
                                  :works="works"
                                  
                                  :selectedCornty="selectedCornty"
                                  :id="id"
                                  :comments="comments"
                                  :responseFiles="responseFiles"
                                  :typesForTables="typesForTables"
                                  :workers="workers"
                                  :funcStop="funcStop"


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
                                <container-footer v-show="(generalComments==false)">
                                  
                                    <b-container>
                                        <b-collapse id="editor">
                                            <vue-editor id="refCommentOfTable" ref="refCommentOfTable" v-model="tmp.comment" @blur="updateItem(tmp.comment, 'comment', tmp.id)">
                                            </vue-editor>
                                        </b-collapse>
                                        <b-input-group class="cForm-input">
                                            <b-input-group-prepend>
                                                <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal;" v-b-toggle="'editor'">
                                                    <span class="when-closed">+</span>
                                                    <span class="when-opened">-</span>
                                                </b-link>
                                               
                                            </b-input-group-prepend>
                                            <b-form-input id="netto" :state="null" type="text"
                                             disabled class="cForm-input text-right" :value="allSumms()" />
                                            <b-input-group-append>
                                                <div class="input-group-text lablelInInput">€</div>
                                                
                                            </b-input-group-append>
                                        </b-input-group>
                                        
                                    </b-container>
                                </container-footer>
                            </container>
                        </b-tab>
                          <b-tab v-if="devicesTab()" ref="devices">
                          <template #title>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Devices', 'devices')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                              </svg> 
                            Devices
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
                                  ></edevices>
                              </container-body>
                              </container>        
                        </b-tab>
                        <b-tab v-if="damageTab()" ref="damage">
                          <template #title>
                              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen cForm-inputG fsbutton" viewBox="0 0 16 16" @click="fschange('Damage', 'damage')">
                                <path d="M1.5 1a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4A1.5 1.5 0 0 1 1.5 0h4a.5.5 0 0 1 0 1h-4zM10 .5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 16 1.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zM.5 10a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 0 14.5v-4a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v4a1.5 1.5 0 0 1-1.5 1.5h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5z"/>
                              </svg> 
                            Damage
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
import io from 'socket.io-client';
import draggable from 'vuedraggable';
import axios from 'axios';
import moment from 'moment';
import { Multipane, MultipaneResizer } from 'vue-multipane';
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
        VueCtkDateTimePicker,
        Multipane,
        MultipaneResizer,
    },
    props: {
        id: String
    },
    data() {
        return {
        beforeTab: null,
        tabIndex: null,
        dubTabIndex: null, 

        makemodalpdf:false,
        windowPrint:false,

        selectedDocsList:[],
        typeDocsList:[],
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
        modalMail:[],
        modalFiles:[],
        selectedFiles:null,
        mailSelect:null,



        dropImage:false,
        dropDoc:false,
        nodeDis:true,
        nodeDisDev:true,
        nameNode:null,
        nameNodeDev:null,

        idNode:null,
        idNodeDev:null,
        parId:null,
        parIdDev:null,
        itemsPrice:[],
        itemsPriceDev:[],
        oldId:0,
        oldIdDev:0,
        itemsMenu:[],
        itemsMenuDev:[],
        selectedItems:[],

        moveToCopyRadio:'move',
        selectedPrice:[],
        selectedPriceDev:[],

        tabxmodal:false,
        mailmodal:false,
        titlex:null,
        comtomodal:null,
        projectfild:{content:'Project'},
        optImages:[],
        selrow:null,
        customToolbar: [
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
          selectedDamageImages:'Image',
          domageImages:[],
          selectedLenght: 0,
          dateForInvoice:null,
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
          typesForTables:[],
          itemsTable:[],
            funcStop:0,
            invoices: [],
            partx: [],
            countries:[ 
  {name: 'Afghanistan', code: 'AF'}, 
  {name: 'Åland Islands', code: 'AX'}, 
  {name: 'Albania', code: 'AL'}, 
  {name: 'Algeria', code: 'DZ'}, 
  {name: 'American Samoa', code: 'AS'}, 
  {name: 'AndorrA', code: 'AD'}, 
  {name: 'Angola', code: 'AO'}, 
  {name: 'Anguilla', code: 'AI'}, 
  {name: 'Antarctica', code: 'AQ'}, 
  {name: 'Antigua and Barbuda', code: 'AG'}, 
  {name: 'Argentina', code: 'AR'}, 
  {name: 'Armenia', code: 'AM'}, 
  {name: 'Aruba', code: 'AW'}, 
  {name: 'Australia', code: 'AU'}, 
  {name: 'Austria', code: 'AT'}, 
  {name: 'Azerbaijan', code: 'AZ'}, 
  {name: 'Bahamas', code: 'BS'}, 
  {name: 'Bahrain', code: 'BH'}, 
  {name: 'Bangladesh', code: 'BD'}, 
  {name: 'Barbados', code: 'BB'}, 
  {name: 'Belarus', code: 'BY'}, 
  {name: 'Belgium', code: 'BE'}, 
  {name: 'Belize', code: 'BZ'}, 
  {name: 'Benin', code: 'BJ'}, 
  {name: 'Bermuda', code: 'BM'}, 
  {name: 'Bhutan', code: 'BT'}, 
  {name: 'Bolivia', code: 'BO'}, 
  {name: 'Bosnia and Herzegovina', code: 'BA'}, 
  {name: 'Botswana', code: 'BW'}, 
  {name: 'Bouvet Island', code: 'BV'}, 
  {name: 'Brazil', code: 'BR'}, 
  {name: 'British Indian Ocean Territory', code: 'IO'}, 
  {name: 'Brunei Darussalam', code: 'BN'}, 
  {name: 'Bulgaria', code: 'BG'}, 
  {name: 'Burkina Faso', code: 'BF'}, 
  {name: 'Burundi', code: 'BI'}, 
  {name: 'Cambodia', code: 'KH'}, 
  {name: 'Cameroon', code: 'CM'}, 
  {name: 'Canada', code: 'CA'}, 
  {name: 'Cape Verde', code: 'CV'}, 
  {name: 'Cayman Islands', code: 'KY'}, 
  {name: 'Central African Republic', code: 'CF'}, 
  {name: 'Chad', code: 'TD'}, 
  {name: 'Chile', code: 'CL'}, 
  {name: 'China', code: 'CN'}, 
  {name: 'Christmas Island', code: 'CX'}, 
  {name: 'Cocos (Keeling) Islands', code: 'CC'}, 
  {name: 'Colombia', code: 'CO'}, 
  {name: 'Comoros', code: 'KM'}, 
  {name: 'Congo', code: 'CG'}, 
  {name: 'Congo, The Democratic Republic of the', code: 'CD'}, 
  {name: 'Cook Islands', code: 'CK'}, 
  {name: 'Costa Rica', code: 'CR'}, 
  {name: 'Cote D\'Ivoire', code: 'CI'}, 
  {name: 'Croatia', code: 'HR'}, 
  {name: 'Cuba', code: 'CU'}, 
  {name: 'Cyprus', code: 'CY'}, 
  {name: 'Czech Republic', code: 'CZ'}, 
  {name: 'Denmark', code: 'DK'}, 
  {name: 'Djibouti', code: 'DJ'}, 
  {name: 'Dominica', code: 'DM'}, 
  {name: 'Dominican Republic', code: 'DO'}, 
  {name: 'Ecuador', code: 'EC'}, 
  {name: 'Egypt', code: 'EG'}, 
  {name: 'El Salvador', code: 'SV'}, 
  {name: 'Equatorial Guinea', code: 'GQ'}, 
  {name: 'Eritrea', code: 'ER'}, 
  {name: 'Estonia', code: 'EE'}, 
  {name: 'Ethiopia', code: 'ET'}, 
  {name: 'Falkland Islands (Malvinas)', code: 'FK'}, 
  {name: 'Faroe Islands', code: 'FO'}, 
  {name: 'Fiji', code: 'FJ'}, 
  {name: 'Finland', code: 'FI'}, 
  {name: 'France', code: 'FR'}, 
  {name: 'French Guiana', code: 'GF'}, 
  {name: 'French Polynesia', code: 'PF'}, 
  {name: 'French Southern Territories', code: 'TF'}, 
  {name: 'Gabon', code: 'GA'}, 
  {name: 'Gambia', code: 'GM'}, 
  {name: 'Georgia', code: 'GE'}, 
  {name: 'Germany', code: 'DE'}, 
  {name: 'Ghana', code: 'GH'}, 
  {name: 'Gibraltar', code: 'GI'}, 
  {name: 'Greece', code: 'GR'}, 
  {name: 'Greenland', code: 'GL'}, 
  {name: 'Grenada', code: 'GD'}, 
  {name: 'Guadeloupe', code: 'GP'}, 
  {name: 'Guam', code: 'GU'}, 
  {name: 'Guatemala', code: 'GT'}, 
  {name: 'Guernsey', code: 'GG'}, 
  {name: 'Guinea', code: 'GN'}, 
  {name: 'Guinea-Bissau', code: 'GW'}, 
  {name: 'Guyana', code: 'GY'}, 
  {name: 'Haiti', code: 'HT'}, 
  {name: 'Heard Island and Mcdonald Islands', code: 'HM'}, 
  {name: 'Holy See (Vatican City State)', code: 'VA'}, 
  {name: 'Honduras', code: 'HN'}, 
  {name: 'Hong Kong', code: 'HK'}, 
  {name: 'Hungary', code: 'HU'}, 
  {name: 'Iceland', code: 'IS'}, 
  {name: 'India', code: 'IN'}, 
  {name: 'Indonesia', code: 'ID'}, 
  {name: 'Iran, Islamic Republic Of', code: 'IR'}, 
  {name: 'Iraq', code: 'IQ'}, 
  {name: 'Ireland', code: 'IE'}, 
  {name: 'Isle of Man', code: 'IM'}, 
  {name: 'Israel', code: 'IL'}, 
  {name: 'Italy', code: 'IT'}, 
  {name: 'Jamaica', code: 'JM'}, 
  {name: 'Japan', code: 'JP'}, 
  {name: 'Jersey', code: 'JE'}, 
  {name: 'Jordan', code: 'JO'}, 
  {name: 'Kazakhstan', code: 'KZ'}, 
  {name: 'Kenya', code: 'KE'}, 
  {name: 'Kiribati', code: 'KI'}, 
  {name: 'Korea, Democratic People\'S Republic of', code: 'KP'}, 
  {name: 'Korea, Republic of', code: 'KR'}, 
  {name: 'Kuwait', code: 'KW'}, 
  {name: 'Kyrgyzstan', code: 'KG'}, 
  {name: 'Lao People\'S Democratic Republic', code: 'LA'}, 
  {name: 'Latvia', code: 'LV'}, 
  {name: 'Lebanon', code: 'LB'}, 
  {name: 'Lesotho', code: 'LS'}, 
  {name: 'Liberia', code: 'LR'}, 
  {name: 'Libyan Arab Jamahiriya', code: 'LY'}, 
  {name: 'Liechtenstein', code: 'LI'}, 
  {name: 'Lithuania', code: 'LT'}, 
  {name: 'Luxembourg', code: 'LU'}, 
  {name: 'Macao', code: 'MO'}, 
  {name: 'Macedonia, The Former Yugoslav Republic of', code: 'MK'}, 
  {name: 'Madagascar', code: 'MG'}, 
  {name: 'Malawi', code: 'MW'}, 
  {name: 'Malaysia', code: 'MY'}, 
  {name: 'Maldives', code: 'MV'}, 
  {name: 'Mali', code: 'ML'}, 
  {name: 'Malta', code: 'MT'}, 
  {name: 'Marshall Islands', code: 'MH'}, 
  {name: 'Martinique', code: 'MQ'}, 
  {name: 'Mauritania', code: 'MR'}, 
  {name: 'Mauritius', code: 'MU'}, 
  {name: 'Mayotte', code: 'YT'}, 
  {name: 'Mexico', code: 'MX'}, 
  {name: 'Micronesia, Federated States of', code: 'FM'}, 
  {name: 'Moldova, Republic of', code: 'MD'}, 
  {name: 'Monaco', code: 'MC'}, 
  {name: 'Mongolia', code: 'MN'}, 
  {name: 'Montserrat', code: 'MS'}, 
  {name: 'Morocco', code: 'MA'}, 
  {name: 'Mozambique', code: 'MZ'}, 
  {name: 'Myanmar', code: 'MM'}, 
  {name: 'Namibia', code: 'NA'}, 
  {name: 'Nauru', code: 'NR'}, 
  {name: 'Nepal', code: 'NP'}, 
  {name: 'Netherlands', code: 'NL'}, 
  {name: 'Netherlands Antilles', code: 'AN'}, 
  {name: 'New Caledonia', code: 'NC'}, 
  {name: 'New Zealand', code: 'NZ'}, 
  {name: 'Nicaragua', code: 'NI'}, 
  {name: 'Niger', code: 'NE'}, 
  {name: 'Nigeria', code: 'NG'}, 
  {name: 'Niue', code: 'NU'}, 
  {name: 'Norfolk Island', code: 'NF'}, 
  {name: 'Northern Mariana Islands', code: 'MP'}, 
  {name: 'Norway', code: 'NO'}, 
  {name: 'Oman', code: 'OM'}, 
  {name: 'Pakistan', code: 'PK'}, 
  {name: 'Palau', code: 'PW'}, 
  {name: 'Palestinian Territory, Occupied', code: 'PS'}, 
  {name: 'Panama', code: 'PA'}, 
  {name: 'Papua New Guinea', code: 'PG'}, 
  {name: 'Paraguay', code: 'PY'}, 
  {name: 'Peru', code: 'PE'}, 
  {name: 'Philippines', code: 'PH'}, 
  {name: 'Pitcairn', code: 'PN'}, 
  {name: 'Poland', code: 'PL'}, 
  {name: 'Portugal', code: 'PT'}, 
  {name: 'Puerto Rico', code: 'PR'}, 
  {name: 'Qatar', code: 'QA'}, 
  {name: 'Reunion', code: 'RE'}, 
  {name: 'Romania', code: 'RO'}, 
  {name: 'Russian Federation', code: 'RU'}, 
  {name: 'RWANDA', code: 'RW'}, 
  {name: 'Saint Helena', code: 'SH'}, 
  {name: 'Saint Kitts and Nevis', code: 'KN'}, 
  {name: 'Saint Lucia', code: 'LC'}, 
  {name: 'Saint Pierre and Miquelon', code: 'PM'}, 
  {name: 'Saint Vincent and the Grenadines', code: 'VC'}, 
  {name: 'Samoa', code: 'WS'}, 
  {name: 'San Marino', code: 'SM'}, 
  {name: 'Sao Tome and Principe', code: 'ST'}, 
  {name: 'Saudi Arabia', code: 'SA'}, 
  {name: 'Senegal', code: 'SN'}, 
  {name: 'Serbia and Montenegro', code: 'CS'}, 
  {name: 'Seychelles', code: 'SC'}, 
  {name: 'Sierra Leone', code: 'SL'}, 
  {name: 'Singapore', code: 'SG'}, 
  {name: 'Slovakia', code: 'SK'}, 
  {name: 'Slovenia', code: 'SI'}, 
  {name: 'Solomon Islands', code: 'SB'}, 
  {name: 'Somalia', code: 'SO'}, 
  {name: 'South Africa', code: 'ZA'}, 
  {name: 'South Georgia and the South Sandwich Islands', code: 'GS'}, 
  {name: 'Spain', code: 'ES'}, 
  {name: 'Sri Lanka', code: 'LK'}, 
  {name: 'Sudan', code: 'SD'}, 
  {name: 'Suriname', code: 'SR'}, 
  {name: 'Svalbard and Jan Mayen', code: 'SJ'}, 
  {name: 'Swaziland', code: 'SZ'}, 
  {name: 'Sweden', code: 'SE'}, 
  {name: 'Switzerland', code: 'CH'}, 
  {name: 'Syrian Arab Republic', code: 'SY'}, 
  {name: 'Taiwan, Province of China', code: 'TW'}, 
  {name: 'Tajikistan', code: 'TJ'}, 
  {name: 'Tanzania, United Republic of', code: 'TZ'}, 
  {name: 'Thailand', code: 'TH'}, 
  {name: 'Timor-Leste', code: 'TL'}, 
  {name: 'Togo', code: 'TG'}, 
  {name: 'Tokelau', code: 'TK'}, 
  {name: 'Tonga', code: 'TO'}, 
  {name: 'Trinidad and Tobago', code: 'TT'}, 
  {name: 'Tunisia', code: 'TN'}, 
  {name: 'Turkey', code: 'TR'}, 
  {name: 'Turkmenistan', code: 'TM'}, 
  {name: 'Turks and Caicos Islands', code: 'TC'}, 
  {name: 'Tuvalu', code: 'TV'}, 
  {name: 'Uganda', code: 'UG'}, 
  {name: 'Ukraine', code: 'UA'}, 
  {name: 'United Arab Emirates', code: 'AE'}, 
  {name: 'United Kingdom', code: 'GB'}, 
  {name: 'United States', code: 'US'}, 
  {name: 'United States Minor Outlying Islands', code: 'UM'}, 
  {name: 'Uruguay', code: 'UY'}, 
  {name: 'Uzbekistan', code: 'UZ'}, 
  {name: 'Vanuatu', code: 'VU'}, 
  {name: 'Venezuela', code: 'VE'}, 
  {name: 'Viet Nam', code: 'VN'}, 
  {name: 'Virgin Islands, British', code: 'VG'}, 
  {name: 'Virgin Islands, U.S.', code: 'VI'}, 
  {name: 'Wallis and Futuna', code: 'WF'}, 
  {name: 'Western Sahara', code: 'EH'}, 
  {name: 'Yemen', code: 'YE'}, 
  {name: 'Zambia', code: 'ZM'}, 
  {name: 'Zimbabwe', code: 'ZW'} 
],
            updatePojectFunc:0,


            ws:null,

            persentCounter: 0,
            damages:[],

            fieldsDocs: [
                {   
                    key: 'type',
                    label: 'File',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'Name',
                    sortable: true
                },
                {
                    key: 'number',
                    label: '#',
                    sortable: true
                },
                {
                    key: 'added',
                    label: 'Date / Time',
                    sortable: true
                },
                {
                    key: 'user',
                    label: 'User',
                    sortable: true
                },
                {
                  key: 'delete',
                  label: 'Delete'
                }
            ],
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
                },
                {
                  key: 'delete',
                  label: 'Delete',
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
                    sortable: true,
                    class: 'pn'
                },
                date: {
                    label: 'Date',
                    sortable: true,
                    class: 'st'
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
                    sortable: true,
                    class: 'text-lg-right'
                },

                brutto: {
                    label: 'Brutto',
                    sortable: true,
                    class: 'text-lg-right'
                },

                 status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status text-left'
                },
                delete: {
                    label: 'Delete',
                    class: 'delete'
                    // class: 'text-center'
                }
            },
            fieldsTableD: {
                number: {
                    label: '#',
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
                 status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
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
    // computed: {
    //     availablePersons() {
    //         if(this.customer){
    //             var persons = this.customer.persons.filter(function(elem, index, self) {
    //                 return index === self.indexOf(elem);
    //             })
    //           return  persons.sort((a, b) => (a > b ? 1 : -1));
    //         }else{
    //             return  false
    //         }
    //     }
    // },
    sockets:{
    connect: function(){
      console.log('socket connected')
    },
    customEmit: function(val){
      console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
    }
  },
    methods: {
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
        var names=[]
        // console.log(this.selectedTransfer)
        this.partx.forEach((valuePart)=> {
                if (valuePart.parts.toggle) {
                    // valuePart.parts.part_content.forEach((v)=>{
                        // item_id = v.item_id
                        names.push(valuePart.parts.id)
                    // })
                }
        })
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
                        names: names.join()
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
          setTimeout(() => {
            this.preview()
           }, 20);
        },
        addPdf() {
            this.addPdfs=true;
            // console.log(this.addPdfs)
            // this.$refs.printOffer.hide()
            this.hideWindowPrint()
            // setTimeout(() => {
            
            setTimeout(() => {
              this.preview()
                //   this.docs2files()
                //   }, 100);     
            }, 20);
        },
        addPdfSep() {
            this.addPdfs='separator';
            // console.log(this.addPdfs)
            // this.$refs.printOffer.hide()
            this.hideWindowPrint()
            // setTimeout(() => {
            
            setTimeout(() => {
              this.preview()
                //   this.docs2files()
                //   }, 100);     
            }, 20);
        },
        printPdf() {
            this.preview()
            setTimeout(function() {
                window.frames["myIframe"].focus();
                window.frames["myIframe"].print();
            }, 2000);
        },
        preview() {
          // window.forms["preForm"].submit();
           document.getElementById("preForm").submit();
 // this.$refs.preForm.submit()
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
          if (this.tmp.typeOfHead == 'Orders') {this.selectedDocsList=['40']}
          if (this.tmp.typeOfHead == 'SUB') {this.selectedDocsList=['41']}
          if (this.tmp.typeOfHead == 'Devices') {this.selectedDocsList=['45']}
            if (this.tmp.typeOfHead == 'Damage') {this.selectedDocsList=['48']}
          setTimeout(() => {
            this.openWindowPrint()
            // this.$refs.printOffer.show()
            this.preview()
           }, 20);
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
      var subject=(this.tmp.place?(this.tmp.place+' - '):'')+(this.tmp.insurance?(this.tmp.insurance+' - '):'')+(this.tmp.other?(this.tmp.other+' - '):'')+(this.tmp.number?(this.tmp.number+' '):'')
      this.subject=(subject!='')?(subject+'intern'):''
      var content='Sehr geehrte'+(('Herr' == name.split(' ')[0])?'r':'')+' '+name+',<br/><br/><br/><p sytle="padding-bottom:4px;">Mit freundlichen Gr&uuml;&szlig;en</p><p>&nbsp;</p><b>'+
      this.$security.table.account.first_name +' '+ this.$security.table.account.second_name
      +'</b><hr color="black" style="width: 345px; padding: 0px; margin: 0px;" align="left" sytle="padding-bottom:4px;"/><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/phone-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'
      +this.$security.table.account.tel+
      '</p><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/email-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'
      +this.$security.table.account.mail+
      '<p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/link-icon-2x.png" alt="" width="13" />&nbsp;&nbsp;'+this.mail_date+'</p><p><img style="float: left; background-color: #f2547d;" src="https://cdn2.hubspot.net/hubfs/53/tools/email-signature-generator/icons/address-icon-2x.png" alt="" width="13"  sytle="padding-bottom:4px;" />&nbsp;&nbsp;'+this.mail_address+'</p><p style="width:345px;height:106px;padding-top:2px;"><img src="'+this.mail_logo+'" style="max-height:100px;max-width:345px;"/></p>'
      this.content = content
      this.filename=''
}
this.modalMail=[]
            val.forEach((val)=>{
            this.modalMail.push({item:val.mail, name:val.mail})    
            })
            this.modalFiles=[]
            this.responseFiles.forEach((val)=>{
            var t = (val.html=='file')?'f':'d'
            this.modalFiles.push({item:t+'-'+val.id, name:val.name.split('.pdf')[0]})    
            })


            this.mailmodalshow()
          
        },
    sendmail(){  //component
    if (this.mailSelect.length<1) alert('No recipients')
    if (this.subject==null) alert('No subject')
    if ((this.subject!=null) && (this.mailSelect.length>=1)){
      if (this.selectedFiles!=null) {
        var files=this.selectedFiles.join()
      } else {var files='_'}
      var from=this.$security.table.account.mail;
      var to=this.mailSelect.join();
      axios.get('/send_mail', {
          params: {
            from:from,
            to:to,
            subject: this.subject,
            content: (this.content==null)?'':this.content,
            filename: this.filename,
            files:files
          }
        })
      this.mailmodalhide()
      this.content = null
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
mailmodalshow(){
    this.mailmodal=true;
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
                setTimeout(() => {

                  this.$refs.docs1?this.$refs.docs1.$refs['ifrForm' + index].submit():''
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
        // console.log(items)
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

    selectedModal(val){
        var price_ids=[]
        if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selectedPrice.length+
            ' rows in to '+val.name+"?")) {
            this.selectedPrice.forEach((val)=>{
                price_ids.push(val.id)
            })
             axios.get('/cp_mv_to_price', {
                 params: {
                     price_ids: price_ids.join(),
                     new_menu: val.id,
                     operation: this.moveToCopyRadio
                 }
             })
        }
    },
      okMoveToCopy(){
        this.selectedPrice=[],
        this.$refs.move.hide()
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
        var names=[]
        // console.log(this.selectedTransfer)
        this.partx.forEach((valuePart)=> {
                if (valuePart.parts.toggle) {
                    // valuePart.parts.part_content.forEach((v)=>{
                        // item_id = v.item_id
                        names.push(valuePart.parts.id)
                    // })
                }
        })
        this.selectedPrice.forEach((v, i)=>{
            ids.push(v.id)
        })

        // function onlyUnique(value, index, self) { 
        //     return self.indexOf(value) === index;
        // }

        // var unique = names.filter(onlyUnique)

        axios.get('/send_price', {
                  params: {
                        ids: ids.join(),
                        names: names.join()
                  }
        }).then(response=>{
            this.selectedPrice=[]
            this.itemsPrice.forEach(v=>{
               v._rowVariant=''  
            })
        })
    },
    sendDevice(){
        var ids=[]
        var names=[]
        // console.log(this.selectedTransfer)
        this.partx.forEach((valuePart)=> {
                if (valuePart.parts.toggle) {
                    // valuePart.parts.part_content.forEach((v)=>{
                        // item_id = v.item_id
                        names.push(valuePart.parts.id)
                    // })
                }
        })
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
                        names: names.join()
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
            alert('No menu item is selected.')
        } else{
            if (this.selectedPrice.length==0){
                alert('No rows selected.')
            }
        }
        if ((this.idNode!=null)&&(this.selectedPrice.length!=0)){
            this.$refs.move.show()           
        }
    },
      mv_cpDevice(){
        if (this.idNodeDev==null){
            alert('No menu item is selected.')
        } else{
            if (this.selectedPriceDev.length==0){
                alert('No rows selected.')
            }
        }
        if ((this.idNodeDev!=null)&&(this.selectedPriceDev.length!=0)){
            this.$refs.moveDev.show()           // новое окно нужно сделать
        }
    },
    addRowPrice(){
        if (this.idNode==null){
            alert('No menu item is selected for add.')
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
            alert('No menu item is selected for add.')
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
            alert('No menu item is selected for deletion.')
       }
       else {
            if (confirm("Are you sure want to remove?")) {
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
            alert('No menu item is selected for deletion.')
       }
       else {
            if (confirm("Are you sure want to remove?")) {
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

        findLevel(this.itemsMenu, this.idNode)  
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
    nodeDisTurn(){
          if (confirm("Are you sure want to rename?")) {
               this.nodeDis = false
            }
       },
    nodeDisTurnDev(){
          if (confirm("Are you sure want to rename?")) {
               this.nodeDisDev = false
            }
       },

    pcurNodeClicked(model, component) {
        this.nameNode = model.name,
        this.idNode=model.id,
        this.parId = model.parrent
        if(this.idNode == this.oldId){
             if (this.itemsPrice.length>0){
                this.itemsPrice=[]
            } else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPrice = response.data
             })
            }
        }else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPrice = response.data
             })
        }
        this.oldId = this.idNode
        if ((model.parrent == 0) && component.folder == false){
            this.idNode = null
        }
    },

    pcurNodeClickedDev(model, component) {
        this.nameNodeDev = model.name,
        this.idNodeDev=model.id,
        this.parIdDev = model.parrent

        if(this.idNodeDev == this.oldIdDev){
             if (this.itemsPriceDev.length>0){
                this.itemsPriceDev=[]
            } else{
            axios.get('/devices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPriceDev = response.data
             })
            }
        }else{
            axios.get('/devices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.itemsPriceDev = response.data
             })
        }
        this.oldIdDev = this.idNodeDev
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeDev = null
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
        var result = (this.type=='Invoices') ? '' : 'you'
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

    presetFilds(){
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].thClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'date')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'file_name')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'user')].tdClass=''
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == 'group')].tdClass=''
        this.domageImages.forEach((v)=>{
          v._rowVariant=''
        })
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


      getdomageImages(){
       axios.get('/domage_images', {
          params: {
            id: this.id,
            project: this.project.number
          }
        }).then(response => {

        this.domageImages = response.data.filter(function (v){
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
    workersToTask(id, event){
      axios.get('/workers_task', {
        params: {
          workers: event?this.selectedWorkers.join():'Null',
          id: id
        }
      })
    },
    updateItem(val, type, id){
        axios.get('/update_item_from_project', {
              params: {
                   val: val,
                   type: type,
                   id: id
                 }
        }).then(response => {})
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
    },


    displaytime() {
    var self = this
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
            this.responseFiles = this.docs.concat(files)
                 })
        })
        })
              })
        },
        fsadd() {
                this.$refs.myVueDropzone.removeAllFiles()
        },
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
        this.tmp.insurname = item.insurname,
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
                            }]
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
        },
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
        addOk(work) {
            this.addSameModalWindow=false
            if (this.comtomodal!=null) this.tabxmodal=true
               axios.get('/add_same', {
                    params: {
                        add_number: this.project.number,
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
            if (confirm("Are you sure?")) {
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
                    this.files = response.data
                })
            }
        },
        filedel(val) {
            if (confirm("Are you sure?")) {
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
  this.selrow = item.id,
  item._rowVariant = (item.id==this.selrow)?'secondary':'',
  this.generalComments=false,
  this.tmp.typeOfHead = item.type,
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
  this.tmp.worker = item.ExamWorker
  }
setTimeout(() => { 
  this.$refs.edit.remoteTax(item.id)
  this.$refs.edit1.remoteTax(item.id)
}, 200)
},
//////////////////////////////////////////////////
get_person(id, mnew){
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
    this.works = response.data
  })
},

pimageInTableSelected(item){
  item._rowVariant=(item._rowVariant=='secondary')?'':'secondary';
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
// console.log(this.groupByFild(this.selectedDamageImages))
  // if (op=='-'){
  //   this.selectedImages.splice(this.selectedImages.indexOf(it), 1)
  // }
},
project_detail_new_f(){
  var optImages = [{id:0, value:'Undefined'}]
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
            optImages.push({id:response.data[i].parts.id, value:response.data[i].parts.part_name})
        }
      }
      if(optImages!=this.optImages){
        this.optImages = optImages
      }
    })

      if(v.number.split(' ').length!=5){
        v.netto = this.$options.filters.thousandSeparator(parseFloat(v.netto));
        v.brutto = this.$options.filters.thousandSeparator(parseFloat(v.brutto));
      } else{
        v.netto = this.$options.filters.thousandSeparator(-parseFloat(v.netto));
        v.brutto = this.$options.filters.thousandSeparator(-parseFloat(v.brutto));
      }
      return v;
    })
    this.itemsTable = response.data;
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
      if (response.data!=null){
                      var num = response.data.id
                      var nuls=3-num.toString().length
                      for (var i = 0; i <= nuls; i++) {
                          num='0'+num
                      }
                      this.project.work=response.data.work,
                      this.project.number=num+'-'+response.data.project_number_year,
                      this.project.date=response.data.date,
                      this.project.street1=response.data.street1,
                      this.project.city1=response.data.city1,
                      this.project.area=response.data.area,
                      this.selectedCornty=(this.countries[this.countries.findIndex(x => x.code == response.data.country)])?this.countries[this.countries.findIndex(x => x.code == response.data.country)]:{code: null},
                      this.project.zip1=response.data.zip1,
                      this.project.other=response.data.other,
                      this.project.editor=response.data.first_name + ' ' + response.data.second_name,
                      this.selectCustomer={id:response.data.customer_id, name:response.data.name, adress:response.data.street, adress1:response.data.zip+' '+response.data.city},
                      this.area=[{id:response.data.customer_id, name:response.data.name, adress:response.data.street, adress1:response.data.zip+' '+response.data.city}],
                      this.selectPerson={id:response.data.person_id, name:response.data.appeal+' '+response.data.names},
                      this.get_contact(this.selectPerson.id),
                      this.availablePersons=[{id:response.data.person_id, name:response.data.appeal+' '+response.data.names}],
                      // this.selectMail={id:response.data.mail, name:response.data.names}
                      // this.availableMails=[{id:response.data.mail, name:response.data.names}]
                      // this.selectPhone={id:response.data.phone, name:response.data.names}
                      // this.availablePhons=[{id:response.data.phone, name:response.data.names}]
                      this.docs2files()
                      this.getdomageImages()

                

                      axios.get('/customer').then(response => {
                        response.data.forEach((it)=>{
                            if(this.selectCustomer.id!=it.id) this.area.push({id:it.id, name:it.name})
                        })
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
    this.project_detail_f(old)
    this.project_id=this.id
}
},
  watch: {
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

        if (this.$refs.devices.localActive){
          // this.beforeTab = this.tmp.typeOfHead
          this.tmp.typeOfHead = 'Devices'
        }
        if (this.$refs.damage.localActive){
          // this.beforeTab = this.tmp.typeOfHead
          this.tmp.typeOfHead = 'Damage'
        }
        if ((this.$refs.devices.localActive==false)&&(this.$refs.damage.localActive==false)){
          // if ((this.tmp.typeOfHead == 'Devices')&(this.tmp.typeOfHead == 'Damage')){
            this.tmp.typeOfHead = this.beforeTab
          // }
        }
    }






    // tabxmodal:function(value) {
    //    if (value == false){
    //     this.comtomodal=null
    //   }
    // }
  }, 
      mounted(){
     setTimeout(() => {

        this.$socket.send('getProjectDetail')
        this.$socket.send('get_type_works')
        this.$socket.send('getPrices')
        this.$socket.send('getDevices')
        this.$options.sockets.onmessage = (data) => (data.data=='getProjectDetail') ? (this.getProjectDetail(1)): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_types_for_tables_f') ? (this.get_types_for_tables_f('socket')): ''
        this.$options.sockets.onmessage = (data) => (data.data=='project_detail_new_f') ? (this.project_detail_new_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_workers_f') ? (this.get_workers_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_type_works') ? (this.get_type_works()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getLoocks') ? (this.getLoocks()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getDevices') ? this.getDevices(): ''
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
  white-space: nowrap;
    font-size: 12px;
    height: 20px;
}
.cForm-input {
    font-size: 12px;
    height: 19px;
}
input::-webkit-date-and-time-value {
  text-align: left;
}
.cForm-inputG {
    height: 19px;
    width: 20px;
    font-size: 10px;
    padding: 0px;
    margin-right: 2px;
    margin-left: 0px !important;
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
.customDrop button {
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
@import url(//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css);
.ccbox label {
    margin-top: -3px;
    width: 15px;
    text-align: left;
}
.ccbox input[type=checkbox] {
    display: none;
}
.ccbox input[type=checkbox]+label:before {
    font-family: FontAwesome;
}
.ccbox input[type=checkbox]+label:before {
    content: "\f096";
    font-size: 14px;
    font-weight: 100;
}
.ccbox input[type=checkbox]:checked+label:before {
    content: "\f046";
    font-size: 14px;
    font-weight: 100;
}
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
  overflow: hidden;
  background: #eee;
}
.horizontal-panes > .pane ~ .pane {
  border-top: 1px solid #ccc;
}
.sleft > .btn{
  text-align: left !important;
}
.cheboxscorl{
  overflow-x: hidden;
  height: 200px;
  overflow-y: auto;
}

#mails{
  padding: 0 !important;
  margin: 0 !important; 
}
.mail .modal {
  background-color: #fff;
}
.mail .modal-dialog {

  max-width: 100% !important;
  height: 100vh !important;
  margin: 0px !important;
}
.mail .modal-dialog .modal-content {
  border: 0px !important;
  height: 100% !important;
}
/*.mail .ql-container{
 height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}*/

.status{
    width: 200px;
}
.delete{
    /*min-width: 40px !important;*/
}
.table-primaryHide{
  display: none;
}

@media screen and (min-width: 992px) {
    .pn{
      min-width:140px;
      white-space: nowrap;
    }
    .st{
      /*width:70px;    */
    }
}
@media screen and (max-width: 991px) {
    .hidenotlg{
      display: none;
    }
}
.text-container {
    position: relative;
    display: block;
    width: 100%;
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
#content{
  min-height: 100px !important;
}

.fsbutton{
    display: none;
}
.active .fsbutton{
    display: inline;
}

@media only screen and (min-width: 991px) {
    .fadeshow1 {
        display: none;
    }
}

@media only screen and (max-width: 1780px) {
    .fadeshow1 {
        display: none;
    }
}
@media only screen and (min-width: 1781px) {
    .fadeshow1 {
        display: block;
    }
}
@media only screen and (max-width: 990px) {
    .fadeshow1 {
        display: block;
    }
}
</style>