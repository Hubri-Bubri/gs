<template>
  <container>
    <input
      ref="unfocus"
      style="
        width: 0px;
        height: 0px;
        position: absolute;
        top: 0;
        left: 0;
        margin: 0;
        padding: 0;
        border: 0;
      "
    />
    <b-modal size="md" centered ref="movedoc" :title="$t('projectDetail.move')">
      <b-form-select
        class=""
        v-model="selectedItems"
        :select-size="detectRowSise(itemsMenuDoc)"
      >
        <option
          v-for="(item, i) in detectItem(itemsMenuDoc)"
          @click="selectedModalDoc(item)"
          :key="i"
        >
          {{item.name}}
        </option>
      </b-form-select>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveDoc">
          OK
        </button>
      </template>
    </b-modal>
    <b-modal
      size="md"
      centered
      ref="moveImag"
      :title="$t('projectDetail.move')"
    >
      <b-form-select
        class=""
        v-model="selectedItems"
        :select-size="detectRowSise(itemsMenuImag)"
      >
        <option
          v-for="(item, i) in detectItem(itemsMenuImag)"
          @click="selectedModalImag(item)"
          :key="i"
        >
          {{item.name}}
        </option>
      </b-form-select>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveImg">
          OK
        </button>
      </template>
    </b-modal>
    <b-modal
      size="sm"
      centered
      :title="$t('projectDetail.selectWorkers')"
      body-class="workerHeight"
      v-model="workerModal"
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
    >
      <b-form-input
        type="text"
        v-model="searchWorker"
        style="margin-bottom: 4px !important"
      />
      <b-form-checkbox-group
        buttons
        button-variant="light"
        style="width: 100%"
        v-model="selectedWorkers"
        stacked
        :options="availableWorkers"
      />
      <template slot="modal-footer">
        <b-container fluid>
          <b-row align-h="between">
            <b-col class="text-left">
              <b-button
                type="button"
                variant="primary"
                @click="selectedWorkers=[]"
                >{{$t('projectDetail.clear')}}</b-button
              >
            </b-col>
            <b-col class="text-right">
              <b-button
                type="button"
                variant="primary"
                @click="closeWorkerModal"
                >OK</b-button
              >
            </b-col>
          </b-row>
        </b-container>
      </template>
    </b-modal>
    <b-modal
      size="lg"
      centered
      ok-only
      id="map"
      :title="$t('projectDetail.track')"
      v-model="mapmodal"
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
    >
      <b-embed
        type="iframe"
        aspect="16by9"
        :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+    'origin='+addressfild+'&'+    'destination='+(project.street1+', '+project.zip1+' '+project.city1).replace('undefined', '')"
      >
      </b-embed>
      <template slot="modal-footer">
        <b-button
          type="button"
          variant="outline-secondary"
          @click="mapmodalhide"
          >{{$t('projectDetail.close')}}</b-button
        >
      </template>
    </b-modal>
    <b-modal
      size="md"
      centered
      v-model="addSameModalWindow"
      :title="$t('projectDetail.addOffers')"
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
    >
      <b-form-group
        horizontal
        :label-cols="4"
        :label="$t('projectDetail.typeOfWork')+':'"
        label-for="work"
        style="padding: 5px"
      >
        <b-form-select
          class="select"
          id="work"
          :options="works"
          v-model="add_offer.work"
          required
        />
      </b-form-group>
      <template slot="modal-footer">
        <b-container fluid>
          <b-row align-h="between">
            <b-col class="text-left">
              <b-button @click="closeaddok" variant="primary">
                {{$t('projectDetail.close')}}
              </b-button>
            </b-col>
            <b-col class="text-right">
              <b-button
                type="submit"
                variant="primary"
                @click="addOk(add_offer.work)"
              >
                {{$t('projectDetail.add')}}
              </b-button>
            </b-col>
          </b-row>
        </b-container>
      </template>
    </b-modal>
    <b-modal
      size="xl"
      v-model="mailmodal"
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
    >
      <b-row>
        <b-col cols="12" md="4">
          <b-form-checkbox-group
            buttons
            text-field="name"
            value-field="item"
            v-model="mailSelect"
            stacked
            style="width: 100%"
            class="cheboxscorl"
            :options="filtered(((abook==false)?modalMail:abooklist),searchmail)"
          />
          <b-input-group>
            <b-form-input
              type="text"
              :placeholder="$t('projectDetail.esearchMailAdress')"
              v-model="searchmail"
            />
            <b-input-group-append>
              <b-form-checkbox button stacked @change="cheabook" v-model="abook"
                >{{$t('projectDetail.addressBook')}}
              </b-form-checkbox>
            </b-input-group-append>
          </b-input-group>
        </b-col>
        <b-col cols="12" md="8">
          <div class="cheboxscorl">
            <b-form-checkbox-group
              buttons
              text-field="name"
              value-field="item"
              button-variant="light"
              v-model="selectedFiles"
              stacked
              style="width: 100%"
              :options="filtered(modalFiles, searchfile)"
            />
          </div>
          <b-form-input
            type="text"
            :placeholder="$t('projectDetail.searchNameOfFile')"
            v-model="searchfile"
          />
        </b-col>
      </b-row>
      <br />
      <b-form-input
        type="text"
        :placeholder="$t('projectDetail.subject')"
        v-model="subject"
      />
      <vue-editor
        id="content"
        ref="content"
        class="mail"
        v-model="content"
        :editorToolbar="customToolbar"
      />
      <template slot="modal-footer">
        <b-form inline>
          <b-button
            type="button"
            @click="mailmodalhide"
            >{{$t('projectDetail.close')}}</b-button
          >
          <b-form-checkbox
            button
            v-if="(selectedFiles && selectedFiles.length ? selectedFiles.length : 0)>=2"
            stacked
            @change="checkattach('chek')"
            v-model="split"
            >{{$t('projectDetail.split')}}
          </b-form-checkbox>
          <b-form-input
            type="text"
            v-model="filename"
            @input="checkattach('inp')"
            :placeholder="$t('projectDetail.nameOfSingleAttachment')"
            v-if="(selectedFiles && selectedFiles.length ? selectedFiles.length : 0)>=2"
          >
          </b-form-input>
          <b-button
            :disabled="(mailSelect.length==0)"
            @click="sendmail()"
            >{{$t('projectDetail.send')}}</b-button
          >
        </b-form>
      </template>
    </b-modal>
    <b-modal
      size="lg"
      v-model="timetableMailModal"
      no-close-on-esc
      no-close-on-backdrop
      hide-header-close
    >
      <b-row>
        <b-col cols="12" md="6">
          <b-form-checkbox-group
            buttons
            text-field="name"
            value-field="item"
            v-model="mailSelectPlan"
            stacked
            style="width: 100%"
            class="cheboxscorl"
            :options="filtered(((abook==false)?modalMail:abooklist),searchmail)"
          />
          <b-input-group>
            <b-form-input
              type="text"
              :placeholder="$t('projectDetail.esearchMailAdress')"
              v-model="searchmail"
            />
            <b-input-group-append>
              <b-form-checkbox button stacked @change="cheabook" v-model="abook"
                >{{$t('projectDetail.addressBook')}}
              </b-form-checkbox>
            </b-input-group-append>
          </b-input-group>
        </b-col>
        <b-col cols="12" md="6" class="text-center">
          <b-col class="text-center">{{$t('projectDetail.delivery')}}:</b-col>
          <br />
          <div
            v-if="(cheatypedate==null)?(!Number.isNaN(Number(selectedDateForSend))):cheatypedate"
          >
            <b-form-radio-group
              buttons
              button-variant="light"
              v-model="selectedDateForSend"
              style="width: 100%"
              :options="[1,2,3,4,5,6,7]"
            />
            <b-form-radio-group
              buttons
              button-variant="light"
              v-model="selectedDateForSend"
              style="width: 100%"
              :options="[8,9,10,11,12,13,14]"
            />
            <b-form-radio-group
              buttons
              button-variant="light"
              v-model="selectedDateForSend"
              style="width: 100%"
              :options="[15,16,17,18,19,20,21]"
            />
            <b-form-radio-group
              buttons
              button-variant="light"
              v-model="selectedDateForSend"
              style="width: 100%"
              :options="[22,23,24,25,26,27,28]"
            />
          </div>
          <div
            v-if="(cheatypedate==null)?(Number.isNaN(Number(selectedDateForSend))):!cheatypedate"
          >
            <b-form-radio-group
              buttons
              button-variant="light"
              v-model="selectedDateForSend"
              stacked
              style="width: 100%"
              :options="monthpart"
            />
          </div>
          <br />
          <b-row align-v="center" align-h="around">
            <b-form-checkbox
              button
              stacked
              :checked="(cheatypedate==null)?(!Number.isNaN(Number(selectedDateForSend))):cheatypedate"
              @change="(cheatypedate=$event);pushToWorkDays=($event==true)?false:pushToWorkDays"
              >{{$t('projectDetail.mothToDays')}}
            </b-form-checkbox>
            <b-form-checkbox
              button
              stacked
              v-model="pushToWorkDays"
              v-if="(cheatypedate==null)?(Number.isNaN(Number(selectedDateForSend))):!cheatypedate"
              >{{$t('projectDetail.pushToWorkDays')}}
            </b-form-checkbox>
          </b-row>
        </b-col>
      </b-row>
      <br />
      <b-form-input
        type="text"
        :placeholder="$t('projectDetail.subject')"
        v-model="subjectPlan"
      />
      <vue-editor
        id="contentPlan"
        ref="contentPlan"
        class="mail"
        v-model="contentPlan"
        :editorToolbar="customToolbar"
      />
      <template slot="modal-footer">
        <b-container>
          <b-row align-v="center" align-h="between">
            <b-col cols="4">
              <b-form-checkbox switch v-model="autoSend">
                {{autoSend?$t('projectDetail.autoSend'):$t('projectDetail.notAutoSend')}}
              </b-form-checkbox>
            </b-col>
            <b-col cols="4">
              <b-form-checkbox
                switch
                @change="selperiodFinishWork=!autoDate?null:selperiodFinishWork"
                v-model="autoDate"
              >
                {{autoDate?$t('projectDetail.autoDate'):$t('projectDetail.notAutoDate')}}
              </b-form-checkbox>
            </b-col>
            <b-col cols="4">
              <b-form-radio-group
                :disabled="!autoDate"
                v-model="selperiodFinishWork"
                :options="periodFinishWork"
              >
              </b-form-radio-group>
            </b-col>
          </b-row>
          <b-row align-v="center" align-h="between">
            <b-col cols="2">
              <b-button type="button" @click="timetableMailModalHide">
                {{$t('projectDetail.close')}}
              </b-button>
            </b-col>
            <b-col cols="2"> {{$t('projectDetail.nameOfInvoice')+':'}} </b-col>
            <b-col cols="3">
              <b-form-input type="text" v-model="filename"> </b-form-input>
            </b-col>
            <b-col cols="2" v-if="(detectPeriod!=null)">
              <b-button
                :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
                @click="sendtimetablemail('remove_mail')"
                variant="danger"
              >
                {{$t('projectDetail.removeplaning')}}
              </b-button>
            </b-col>
            <b-col cols="3" v-if="(detectPeriod!=null)">
              <b-button
                :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
                @click="sendtimetablemail('replan_mail')"
                variant="primary"
              >
                {{$t('projectDetail.replaning')}}
              </b-button>
            </b-col>
            <b-col cols="3" v-if="(detectPeriod==null)">
              <b-button
                :disabled="(selectedDateForSend==null)||(mailSelectPlan.length==0)"
                @click="sendtimetablemail('plan_mail')"
                variant="success"
              >
                {{$t('projectDetail.planing')}}
              </b-button>
            </b-col>
          </b-row>
        </b-container>
      </template>
    </b-modal>
    <container-header class="container-fluid">
      <top-menu> </top-menu>
    </container-header>
    <container-body class="container-fluid">
      <b-card-group deck>
        <b-card no-body class="gs-container" :style="heightComponentforSm">
          <b-tabs card v-model="tabIndex" class="tabs">
            <b-tab>
              <template #title>
                <span
                  v-if="project.number==undefined"
                  >{{projectfild.content}}</span
                >
                <span
                  v-else
                  :title="projectfild.content+' '+project.number"
                  >{{project.number}}</span
                >
              </template>
              <container>
                <container-body ref="project">
                  <b-container ref="hproject">
                    <project
                      :dislink="(selectedTables.length!=1)"
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
                      :tablesBusy="tablesBusy"
                      :tableLoading="tableLoading"
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
                    >
                    </project>
                  </b-container>
                </container-body>
              </container>
            </b-tab>
            <b-tab style="padding: 0px">
              <template #title> {{$t('projectDetail.priceList')}} </template>
              <container>
                <container-body>
                  <price
                    v-if="(tabIndex==1) && (comtomodal!='pricelist')"
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
                  >
                  </price>
                </container-body>
                <container-footer style="overflow: hidden">
                  <b-input-group>
                    <!-- <b-button
                      @click="addPrice"
                      >{{$t('projectDetail.plusPart')}}</b-button
                    > -->
                    <b-button
                      @click="removePrice"
                      >{{$t('projectDetail.remove')}}</b-button
                    >
                    <b-button
                      @click="sendPrice"
                      :disabled="(selectedTables.length<=0)||(selectedPrice.length<=0)"
                      >{{$t('projectDetail.send')}}</b-button
                    >
                    <b-button @click="$refs.priceChild1.hidePosition()">
                      <b-icon icon="layout-three-columns" aria-hidden="true">
                      </b-icon>
                    </b-button>
                    <b-form-input
                      v-model="nameNode"
                      :style="nodeDis?'background-color:grey':''"
                      @click.native="nodeDis?nodeDisTurn():''"
                      @change="nodeDis=true;toModel(nameNode)"
                    >
                    </b-form-input>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab style="padding: 0px">
              <template #title> {{$t('projectDetail.devicesList')}} </template>
              <container>
                <container-body>
                  <devices
                    v-if="(tabIndex==2) && (comtomodal!='deviceslist')"
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
                  >
                  </devices>
                </container-body>
                <container-footer>
                  <b-input-group>
                    <b-button
                      @click="addDevice"
                      >{{$t('projectDetail.plusPart')}}</b-button
                    >
                    <b-button
                      @click="removeDevice"
                      >{{$t('projectDetail.remove')}}</b-button
                    >
                    <b-button
                      @click="sendDevice"
                      :disabled="selectedTables.length<=0"
                      >{{$t('projectDetail.send')}}</b-button
                    >
                    <b-button @click="$refs.devChild1.hidePosition()">
                      <b-icon icon="layout-three-columns" aria-hidden="true">
                      </b-icon>
                    </b-button>
                    <b-form-input
                      v-model="nameNodeDev"
                      :style="nodeDisDev?'background-color:grey':''"
                      @click.native="nodeDisDev?nodeDisTurnDev():''"
                      @change="nodeDisDev=true;toModelDev(nameNodeDev)"
                    >
                    </b-form-input>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab>
              <template #title> {{$t('projectDetail.docs')}} </template>
              <container>
                <container-body style="overflow: hidden">
                  <docs
                    v-if="detect('docs')"
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
                    @getDocs="getDocs()"
                  >
                  </docs>
                </container-body>
                <container-footer style="z-index: 2">
                  <b-collapse v-model="dropDoc" id="dropDoc3">
                    <vue-dropzone
                      ref="myVueDropzone3"
                      id="dz3"
                      :options="dropzoneOptions1"
                      v-on:vdropzone-sending="sendingEvent"
                      v-on:vdropzone-success="fsadd3"
                      :forceFallback="true"
                    >
                    </vue-dropzone>
                  </b-collapse>
                  <b-input-group>
                    <template #prepend>
                      <b-button @click="dropDoc=dropDoc?false:true">
                        <b-icon
                          :icon="dropDoc?'folder2-open':'folder2'"
                          aria-hidden="true"
                        >
                        </b-icon>
                      </b-button>
                      <b-button
                        @click="addDoc"
                        >{{$t('projectDetail.plusPart')}}</b-button
                      >
                      <b-button
                        @click="removeDoc"
                        :disabled="(nameNodeDoc=='General Folder')?true:false"
                        >{{$t('projectDetail.remove')}}</b-button
                      >
                      <b-button
                        @click="moveDoc"
                        >{{$t('projectDetail.move')}}</b-button
                      >
                    </template>
                    <b-form-input
                      v-model="nameNodeDoc"
                      :style="nodeDisDoc?'background-color:grey':''"
                      :disabled="(nameNodeDoc=='General Folder')?true:false"
                      @click.native="nodeDisDoc?nodeDisTurnDoc():''"
                      @change="nodeDisDoc=true;toModelDoc(nameNodeDoc)"
                    >
                    </b-form-input>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab>
              <template #title> {{$t('projectDetail.images')}} </template>
              <container>
                <container-body style="overflow: hidden">
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
                    @getDocs="getDocs()"
                  >
                  </images>
                </container-body>
                <container-footer style="z-index: 2">
                  <b-collapse v-model="dropImage" id="dropImage2">
                    <vue-dropzone
                      ref="myVueDropzone2"
                      id="dz2"
                      :options="dropzoneOptions2"
                      v-on:vdropzone-sending="sendingEventImage"
                      v-on:vdropzone-success="fsadd2"
                      :forceFallback="true"
                    />
                  </b-collapse>
                  <b-input-group>
                    <template #prepend>
                      <b-button @click="dropImage=dropImage?false:true">
                        <b-icon
                          :icon="dropImage?'folder2-open':'folder2'"
                          aria-hidden="true"
                        >
                        </b-icon>
                      </b-button>
                      <b-button
                        @click="addImag"
                        >{{$t('projectDetail.plusPart')}}</b-button
                      >
                      <b-button
                        @click="removeImag"
                        :disabled="(nameNodeDoc=='General Folder')?true:false"
                        >{{$t('projectDetail.remove')}}</b-button
                      >
                      <b-button
                        @click="moveImag"
                        >{{$t('projectDetail.move')}}</b-button
                      >
                    </template>
                    <b-form-input
                      v-model="nameNodeImag"
                      :style="nodeDisImag?'background-color:grey':''"
                      :disabled="(nameNodeImag=='General Folder')?true:false"
                      @click.native="nodeDisImag?nodeDisTurnImag():''"
                      @change="nodeDisImag=true;toModelImag(nameNodeImag)"
                    />
                    <b-button
                      v-show="butifsel()"
                      @click="sendtodamage()"
                      :disabled="selectedTables.length<=0"
                      >{{$t('projectDetail.send')}}</b-button
                    >
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab style="padding: 0px">
              <template #title> {{$t('projectDetail.reportList')}} </template>
              <container>
                <container-body>
                  <reports
                    v-if="(tabIndex==5) && (comtomodal!='reportList')"
                    @loded="loded"
                    ref="reportChild1"
                    :menuPriceTree="menuReportTree"
                    :idNode="idNodeReport"
                    :items="itemsReport"
                    :itemsMenu="itemsMenuReport"
                    :oldId="oldIdReport"
                    :selectedPrice="selectedReport"
                    @curNodeClicked="pcurNodeClickedReport"
                    @rowSelected="prowSelectedReport"
                  >
                  </reports>
                </container-body>
                <container-footer style="overflow: hidden">
                  <b-input-group>
                    <b-button
                      @click="addReport"
                      >{{$t('projectDetail.plusPart')}}</b-button
                    >
                    <b-button
                      @click="removeReport"
                      >{{$t('projectDetail.remove')}}</b-button
                    >
                    <b-button
                      @click="sendReport"
                      :disabled="selectedTables.length<=0"
                      >{{$t('projectDetail.send')}}</b-button
                    >
                    <b-button @click="$refs.reportChild1.hidePosition()">
                      <b-icon icon="layout-three-columns" aria-hidden="true">
                      </b-icon>
                    </b-button>
                    <b-form-input
                      v-model="nameNodeReport"
                      :style="nodeDisReport?'background-color:grey':''"
                      @click.native="nodeDisReport?nodeDisTurnReport():''"
                      @change="nodeDisReport=true;toModelReport(nameNodeReport)"
                    >
                    </b-form-input>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
          </b-tabs>
        </b-card>
        <b-card no-body class="gs-container" :style="heightEditforSm">
          <b-tabs card v-model="dubTabIndex">
            <b-tab ref="Edit">
              <!-- !{{tmp.typeOfHead}}! -->
              <template #title>
                {{tmp.type?$t('oneCountAlret.'+tmp.type):$t('fields.other')}}
              </template>
              <container>
                <container-body>
                  <edit
                    ref="editList"
                    :tmp="tmp"
                    :project="project"
                    :looks="looks"
                    :works="works"
                    :selectedCornty="selectedCornty"
                    :id="id"
                    :comments="comments"

                    :typesForTables="typesForTables"
                    :workers="workers"
                    :plan="plan"

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

                    @loded="loded"
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
                    
                    @countDigitals="countDigitals"
                  >
                  </edit>
                  <!-- :funcStop="funcStop" -->
                  <!-- @tabletopartx="tabletopartx" -->
                  <!-- :rowsBusy="rowsBusy" -->
                  <!-- :rowsLoading="rowsLoading" -->
                  <!-- :partx="partx" -->
                </container-body>
                <container-footer
                  v-if="(generalComments==false)"
                  :style="openEditor?'margin-top:-26px':''"
                >
                  <b-iconstack
                    font-scale="3"
                    style="
                      position: relative;
                      left: 24px;
                      top: 44px;
                      z-index: 2;
                    "
                    @mouseover="cloudHover=true"
                    @mouseleave="cloudHover=false"
                    @click="updateItem($refs['refCommentOfTable'].quill.getHTML(), 'comment', tmp.id);tmp.comment=$refs['refCommentOfTable'].quill.getHTML();changeDisable('b', 'refCommentOfTable', tmp.id);cloudChange=false;cloudLoad=true;"
                    v-if="(openEditor==true)"
                  >
                    <b-icon
                      stacked
                      icon="circle-fill"
                      :animation="cloudLoad?'throb':null"
                      variant="primary"
                      v-show="cloudLoad||cloudHover"
                    >
                    </b-icon>
                    <b-icon
                      stacked
                      icon="cloud-upload"
                      scale="0.5"
                      :variant="cloudHover?'light':'dark'"
                      v-show="!cloudLoad"
                    >
                    </b-icon>
                    <b-icon
                      stacked
                      icon="circle"
                      variant="info"
                      v-show="cloudChange"
                    >
                    </b-icon>
                  </b-iconstack>
                  <b-iconstack
                    font-scale="3"
                    style="
                      position: relative;
                      left: 24px;
                      top: 44px;
                      z-index: 2;
                    "
                    @click="checkInEditor('refCommentOfTable', tmp.id)"
                    v-if="(openEditor==true)"
                    @mouseover="calcHover = true"
                    @mouseleave="calcHover = false"
                  >
                    <b-icon
                      stacked
                      icon="circle-fill"
                      variant="primary"
                      v-show="calcHover"
                    >
                    </b-icon>
                    <b-icon
                      stacked
                      icon="calculator"
                      scale="0.5"
                      :variant="calcHover?'light':'dark'"
                    >
                    </b-icon>
                  </b-iconstack>
                  <span
                    v-show="(disablefildUser('refCommentOfTable', tmp.id)!='you')"
                    style="
                      position: relative;
                      left: 30px;
                      top: 36px;
                      width: 18px;
                      z-index: 2;
                    "
                    v-if="(openEditor==true)"
                    >{{disablefildUser('refCommentOfTable', tmp.id)}}</span
                  >
                  <vue-editor
                    :value="tmp.comment"
                    :editorToolbar="customToolbar"
                    v-if="(openEditor==true)"
                    @focus="changeDisable('f', 'refCommentOfTable', tmp.id);cloudChange=true;"
                    :disabled="disablefild('refCommentOfTable', tmp.id)?'disabled':false"
                    style="position: relative; top: 0px; z-index: 1"
                    class="text-right"
                    ref="refCommentOfTable"
                    id="refCommentOfTable"
                  />
                  <b-input-group class="cForm-input">
                    <b-col cols="text-right">
                      <b-button
                        size="sm"
                        v-if="(openEditor==false)"
                        @click="openEditor=true"
                      >
                        +
                      </b-button>
                      <b-button
                        size="sm"
                        v-if="(openEditor==true)"
                        @click="openEditor=false"
                      >
                        -
                      </b-button>
                    </b-col>
                    <b-col class="text-right">{{$t('projectDetail.general')}}: {{tmp.gen_summa}} € </b-col>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab v-if="devicesTab()" ref="devices">
              <template #title> {{$t('projectDetail.devices')}} </template>
              <container>
                <container-body>
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
                  >
                  </edevices>
                </container-body>
              </container>
            </b-tab>
            <b-tab v-if="damageTab()" ref="damage">
              <template #title> {{$t('projectDetail.damage')}} </template>
              <container>
                <container-body>
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
                    :wwidth="wwidth"
                    @selectedDocs="selectedDocs"
                    @addPdf="addPdf"
                    @addPdfSep="addPdfSep"
                    @printPdf="printPdf"
                    @preview="preview"
                    @printOffer="printOffer"
                    @hideWindowPrint="hideWindowPrint"
                    ref="damageList"
                  >
                  </damage>
                </container-body>
              </container>
            </b-tab>
            <b-tab v-if="reportsTab()" ref="reports">
              <template #title> {{$t('projectDetail.reports')}} </template>
              <container>
                <container-body>
                  <ereports
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
                    :selectedDocsList="selectedDocsList"
                    :windowPrint="windowPrint"
                    :addPdfs="addPdfs"
                    :makemodalpdf="makemodalpdf"
                    :typeDocsList="typeDocsList"
                    :looks="looks"
                    @worker="worker"
                    :selectedWorkers="selectedWorkers"
                    @selectedDocs="selectedDocs"
                    @addPdf="addPdf"
                    @addPdfSep="addPdfSep"
                    @printPdf="printPdf"
                    @preview="preview"
                    @printOffer="printOffer"
                    @hideWindowPrint="hideWindowPrint"
                    ref="ereportsList"
                  >
                  </ereports>
                </container-body>
              </container>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-card-group>
    </container-body>
  </container>
</template>
<script type = "text/javascript">
import draggable from 'vuedraggable';
import axios from 'axios';
import {
	VueEditor
}
from 'vue2-editor';
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
import VueCtkDateTimePicker from 'vue-ctk-date-time-picker';
import 'vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css';
const items = [];
export default {
	components: {
		VueEditor,
		vueDropzone: vue2Dropzone,
		draggable,
		VueCtkDateTimePicker
	},
	props: {
		id: String
	},
	data() {
		return {
			// rowsBusy: true,
			// rowsLoading: true,
			tablesBusy: true,
			tableLoading: true,
			hideNumberOfYear: null,
			selectedTables: [],
			wcval: null,
			wcadd: null,
			weval: null,
			weadd: null,
			heightEditforSm: '',
			heightComponentforSm: 'min-height:934px',
			wwidth: null,
			beforeSubject: null,
			beforeMail: null,
			pushToWorkDays: true,
			selperiodFinishWork: null,
			autoSend: false,
			autoDate: false,
			cheatypedate: null,
			plan: null,
			planid: null,
			selectedDateForSend: null,
			detectPeriod: null,
			cloudHover: false,
			cloudLoad: false,
			cloudChange: false,
			calcHover: false,
			openEditor: false,
			menuPriceTree: false,
			menuDevicesTree: false,
			menuDocsTree: false,
			beforeTab: null,
			tabIndex: null,
			dubTabIndex: null,
			makemodalpdf: false,
			windowPrint: false,
			selectedDocsList: [],
			typeDocsList: [],
			docs_menu_ids: [],
			images_menu_ids: [],
			workerModal: false,
			addSameModalWindow: false,
			mapmodal: false,
			mail_date: '',
			mail_address: '',
			mail_logo: '',
			filename: '',
			split: 'Split',
			abook: false,
			abooklist: null,
			searchfile: '',
			searchmail: '',
			subject: null,
			content: null,
			subjectPlan: null,
			contentPlan: null,
			modalMail: [],
			modalFiles: [],
			selectedFiles: null,
			mailSelect: [],
			mailSelectPlan: [],
			oldIdReport: 0,
			idNodeReport: null,
			itemsReport: [],
			itemsMenuReport: [],
			selectedReport: [],
			nameNodeReport: null,
			nodeDisReport: true,
			dropImage: true,
			dropDoc: true,
			nodeDis: true,
			nodeDisDev: true,
			nodeDisDoc: true,
			nodeDisImag: true,
			nameNode: null,
			nameNodeDev: null,
			nameNodeDoc: null,
			nameNodeImag: null,
			idNode: null,
			idNodeDev: null,
			idNodeDoc: -1,
			idNodeImg: -1,
			itemsPrice: [],
			itemsPriceDev: [],
			itemsPriceDoc: [],
			oldId: 0,
			oldIdDev: 0,
			oldIdDoc: 0,
			oldIdImg: 0,
			itemsMenu: [],
			itemsMenuDev: [],
			itemsMenuDoc: [],
			itemsMenuImag: [],
			selectedItems: [],
			menuReportTree: false,
			moveToCopyRadio: 'move',
			selectedPrice: [],
			selectedPriceDev: [],
			selectedPriceDoc: [],
			selectedPriceImg: [],
			tabxmodal: false,
			mailmodal: false,
			timetableMailModal: false,
			comtomodal: null,
			projectfild: {
				content: 'Project'
			},
			addressfild: 'Earth',
			selrow: null,
			customToolbar: [
				[{
					list: "check"
				}],
				['bold', 'italic', 'underline', 'strike'],
				[{
					'color': []
				}, {
					'background': []
				}],
				[{
					'align': []
				}],
			],
			fs: true,
			selectCustomer: {
				id: null
			},
			selectPerson: {
				id: null
			},
			selectMail: {
				id: null
			},
			selectPhone: {
				id: null
			},
			showsubarr: [],
			countCall: 0,
			project_id: null,
			domageImages: [],
			generalComments: true,
			searchWorker: null,
			selectedWorkers: [],
			typesForTables: [],
			itemsTable: [],
			funcStop: 0,
			invoices: [],
			partx: [],
			countries: [],
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
			docs: [],
			files: [],
			responseFiles: [],
			addPdfs: false,
			resp: null,
			comments: true,
			workers: [],
			workersForSend: [],
			items: items,
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
				area: null,
				number: null,
				editor: null,
				date: null,
				street: null,
				city: null,
				zip: null,
				other: null
			},
			selectedCornty: {
				code: null
			},
			customer: {
				id: null,
				persons: []
			},
			person: {
				id: null
			},
			show: false,
			tabs: [],
			add_offer: {
				work: null,
				insurance_number: null,
				insurname: null,
				place: null,
				comment: null
			},
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
				typeOfHead: 'Offer',
				dateEvent: null,
				dateInspect: null,
				worker: null,
				comment: ''
			},
			commentOfTable: '',
			area: [],
			availablePersons: [],
			availableMails: [],
			availablePhons: [],
			looks: []
		}
	},
	computed: {
		periodFinishWork() {
			return [{
					text: this.$t('projectDetail.prevperiod'),
					value: 'previous'
				},
				{
					text: this.$t('projectDetail.curperiod'),
					value: 'current'
				}
			]
		},
		monthpart() {
			return [{
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
				}
			]
		},
		fieldsDocs() {
			return [{
					key: 'type',
					label: '§',
					sortable: true
				},
				{
					key: 'name',
					label: this.$t('docs.name'),
					class: 'w-100',
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
			]
		},
		availableWorkers() {
			if (this.searchWorker) {
				return this.workers.filter(item => {
					return item.toLowerCase().includes(this.searchWorker.toLowerCase());
				});
			}
			return this.workers
		}
	},
	sockets: {
		connect: function () {
			console.log('socket connected')
		},
		customEmit: function (val) {
			console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
		}
	},
	methods: {
    update_item(update){
      this.itemsTable = this.itemsTable.filter((item)=>{
        if (item.id == update.item_id){
          item[update.type] = update.val
          this.tmp[update.type] = update.val
        }
        return item
      })
    },
		linkForWorkers(user) {
			var host = window.location.host
			if (this.selectedTables.length > 0) {
				this.partx.forEach((valuePart) => {
					if (valuePart.parts.id == this.selectedTables[0]) {
						var notHaveFoolder = 1
						this.itemsMenuImag[0].children.forEach((folder) => {
							if ((folder.name == valuePart.parts.part_name) & (notHaveFoolder == 1)) {
								notHaveFoolder = 0
								this.$clipboard('https://' + host + '/#/I/' + user + '/' + this.project.number + '/' + folder.name.replace(' ', '_'))
							}
						})
						if (notHaveFoolder == 1) {
							if (confirm('"' + valuePart.parts.part_name + '" ' + this.$t('projectDetail.notExist'))) {
								axios.get('/add_images_menu', {
									params: {
										parent_id: '-1',
										project: this.id,
										newName: valuePart.parts.part_name
									}
								}).then(response => {
									this.$clipboard('https://' + host + '/#/I/' + user + '/' + this.project.number + '/' + response.data.name.replace(' ', '_'))
								})
							}
							else {
								this.$clipboard('https://' + host + '/#/I/' + user + '/' + this.project.number + '/' + 'General+Folder')
							}
						}
					}
				})
			}
			else {
				this.$clipboard('https://' + host + '/#/I/' + user + '/' + this.project.number + '/' + 'General+Folder')
			}
		},
		seltable(emitSelectedTables) {
      this.selectedTables = emitSelectedTables
      // console.log(this.selectedTables)
    },
		loded(dir, elheight, add) {
			this.sm2lg(dir, elheight, add)
		},
		sm2lg(dir, val, add) {
			var result
			function changeSm2Lg(wwidth, height, add) {
				if (wwidth <= 768) {
					if (height != undefined) {
						return 'min-height:' + (height + add) + 'px;'
					}
				}
			}
			result = (changeSm2Lg(this.wwidth, val, add))
			if (dir == 'component') {
				this.wcval = val
				this.wcadd = add
				this.heightComponentforSm = result
			}
			if (dir == 'edit') {
				this.weval = val
				this.weadd = add
				this.heightEditforSm = result
			}
		},
		detect(type) {
			if (type == 'docs') {
				if ((this.tabIndex == 3) && (this.comtomodal != 'docs')) {
					return true;
				}
			}
			if (type == 'images') {
				if ((this.tabIndex == 4) && (this.comtomodal != 'images')) {
					return true;
				}
			}
		},
		moveDoc() {
			this.$refs.movedoc.show()
		},
		moveImag() {
			this.$refs.moveImag.show()
		},
		projectOther(val) {
			this.project.other = val
		},
		checkInEditor(tname, id) {
			var result
			var sval
			var separator
			var safeEval = require('safe-eval')
			var valueHtml = (this.$refs[tname] != undefined) && (this.$refs[tname].length != 0) ? this.$refs[tname].quill.getHTML() : ''
			if (valueHtml.indexOf('=') != -1) {
				separator = (this.$refs[tname] != undefined) && (this.$refs[tname].length != 0) ? this.$refs[tname].quill.getText() : ''
				separator = separator.replace(/\n/g, ' ')
				separator = separator.substring(0, separator.length - 1)
				separator = separator + ' '
				separator = separator.split('= ')
				separator.splice(-1, 1)
				separator.forEach((val) => {
					var calcval = val.split(' ')[val.split(' ').length - 1]
					if (calcval.search(/[a-zA-z=]/gim) == -1) {
						if (calcval.search(/[-+*)(/]/gim) > -1) {
							if (calcval.search(/[0-9]/gim) > -1) {
								if (/[\d)]/.test(calcval[calcval.length - 1])) {
									var rcalcval = calcval.split(',').join('.')
									try {
										result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
									}
									catch (e) {
										result = '(not valid formula)'
									}
									sval = rcalcval + '=' + result + ' '
									this.$refs[tname].quill.clipboard.dangerouslyPasteHTML(
										valueHtml = valueHtml.replace(calcval + '=', sval)
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
		butifsel() {
			var detectState = 0
			this.domageImages.forEach(function (v) {
				if (v._rowVariant != '') detectState = detectState + 1
			})
			return (detectState > 0)
		},
		sendtodamage() {
			var ids = []
			this.domageImages.forEach((v, i) => {
				if (v._rowVariant != '') ids.push(v.id.split('image?id=')[1])
			})
			axios.get('/send_damage', {
				params: {
					ids: ids.join(),
					names: this.selectedTables.join()
				}
			}).then(response => {
				this.domageImages.forEach(v => {
					v._rowVariant = ''
				})
			})
		},
		reportsTab() {
			var countDev = 0
			this.partx.forEach((valuePart) => {
				if (valuePart.parts.reports_content.length > 0) {
					countDev = countDev + 1
				}
			})
			return (countDev > 0)
		},
		damageTab() {
			var countDev = 0
			this.partx.forEach((valuePart) => {
				if (valuePart.parts.damage_content.length > 0) {
					countDev = countDev + 1
				}
			})
			return (countDev > 0)
		},
		devicesTab() {
			var countDev = 0
			this.partx.forEach((valuePart) => {
				if (valuePart.parts.devices_content.length > 0) {
					countDev = countDev + 1
				}
			})
			return (countDev > 0)
		},
		selectedDocs(event) {
			this.selectedDocsList = []
			this.selectedDocsList = event
			this.preview()
		},
		addPdf() {
			this.addPdfs = true;
			this.preview()
		},
		addPdfSep() {
			this.addPdfs = 'separator';
			this.hideWindowPrint()
			this.preview()
		},
		printPdf() {
			this.preview()
			setTimeout(function () {
				window.frames["myIframe"].focus();
				window.frames["myIframe"].print();
			}, 2000);
		},
		preview() {
			if (this.$refs.editList != undefined) {
				if (this.$refs.editList.$refs.calcGroup.$refs.print != undefined) {
					this.$refs.editList.$refs.calcGroup.$refs.print.previewPDFForm();
				}
			}
			if (this.$refs.damageList != undefined) {
				if (this.$refs.damageList.$refs.damageGroup.$refs.print != undefined) {
					this.$refs.damageList.$refs.damageGroup.$refs.print.previewPDFForm();
				}
			}
			if (this.$refs.edeviceList != undefined) {
				if (this.$refs.edeviceList.$refs.deviceGroup.$refs.print != undefined) {
					this.$refs.edeviceList.$refs.deviceGroup.$refs.print.previewPDFForm();
				}
			}
			if (this.$refs.ereportsList != undefined) {
				if (this.$refs.ereportsList.$refs.reportGroup.$refs.print != undefined) {
					this.$refs.ereportsList.$refs.reportGroup.$refs.print.previewPDFForm();
				}
			}
		},
		printOffer() {
			this.addPdfs = false;
			this.makemodalpdf = true;
			axios.get('/get_type_docs', {
				params: {
					type: this.tmp.typeOfHead
				}
			}).then(response => {
				this.typeDocsList = response.data
				if (this.tmp.typeOfHead == 'Offers') {
					this.selectedDocsList = ['31']
				}
				if (this.tmp.typeOfHead == 'Invoices') {
					this.selectedDocsList = ['14']
				}
				if (this.tmp.typeOfHead == 'Orders') {
					this.selectedDocsList = ['38']
				}
				if (this.tmp.typeOfHead == 'SUB') {
					this.selectedDocsList = ['41']
				}
				if (this.tmp.typeOfHead == 'Devices') {
					this.selectedDocsList = ['45']
				}
				if (this.tmp.typeOfHead == 'Damage') {
					this.selectedDocsList = ['48']
				}
				if (this.tmp.typeOfHead == 'Reports') {
					this.selectedDocsList = ['50']
				}
				this.openWindowPrint()
				this.preview()
			})
		},
		addSameModal() {
			this.add_offer.comment = null
			this.add_offer.place = null
			this.add_offer.insurance_number = null
			this.add_offer.work = null
			this.addSameModalWindow = true
		},
		cheabook() {
			if (this.abooklist == null) {
				this.abooklist = []
				axios.get('/get_addresbook', {}).then(response => {
					response.data.forEach((val) => {
						this.abooklist.push({
							item: val.mail,
							name: val.mail
						})
					})
				})
			}
		},
		checkattach(val) {
			if (val == 'chek') this.filename = ''
			if (val == 'inp') {
				if (this.filename == '') {
					this.split = 'Split'
				}
				else {
					this.split = ''
				}
			}
		},
		filtered(val1, val2) {
			if ((val1 != undefined) && (val2 != undefined)) {
				return val1.filter(v => {
					return v.name.toLowerCase().includes(val2.toLowerCase())
				})
			}
		},
		sendMail(val) {
			var namePerson = this.selectPerson.name.split(' ')
			var name = (namePerson.length == 3) ? namePerson[0] + ' ' + namePerson[2] : this.selectPerson.name
			if ((this.content == null) || (this.content == '')) {
				this.modalMail = []
				this.modalFiles = []
				this.selectedFiles = []
				this.mailSelect = []
				var subject = this.beforeSubject
				var number = (this.tmp.typeOfHead == 'Invoices') ? (this.tmp.number.split(' ').length == 5) ? this.tmp.number.split(' ')[3] :
					this.countDigitals(this.tmp.number.split(' ')[1]) + '-' + this.tmp.number.split(' ')[0].split('-')[1] : (this.tmp.typeOfHead == 'SUB') ?
					this.tmp.number.split(' ')[0] : (this.tmp.typeOfHead == 'Sub Invoices') ? this.tmp.number.split(' ')[3] : this.tmp.number
				subject = subject.split('@Number').join(number ? number : '')
				subject = subject.split('@Document').join(this.tmp.date ? this.tmp.date : '')
				subject = subject.split('@Place').join(this.tmp.place ? this.tmp.place : '')
				subject = subject.split('@Order').join(this.tmp.other ? this.tmp.other : '')
				subject = subject.split('@Insurance').join(this.tmp.insurance ? this.tmp.insurance : '')
				subject = subject.split('@InsName').join(this.tmp.insurname ? this.tmp.insurname : '')
				this.subject = subject
				var content = this.beforeMail
				content = content.split('@Respect').join('geehrte' + (('Herr' == name.split(' ')[0]) ? 'r' : ''))
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
				if (this.tmp.type == 'Invoices') {
					content = content.split('<p>@InvPress?' + invPress + '</p>').join(invPress)
				}
				if (this.tmp.type != 'Invoices') {
					content = content.split('<p>@InvPress?' + invPress + '</p>').join('')
				}
				if (this.tmp.type == 'Offers') {
					content = content.split('<p>@OfferPress?' + offerPress + '</p>').join(offerPress)
				}
				if (this.tmp.type != 'Offers') {
					content = content.split('<p>@OfferPress?' + offerPress + '</p>').join('')
				}
				if (this.tmp.type == 'SUB') {
					content = content.split('<p>@SUBPress?' + subPress + '</p>').join(subPress)
				}
				if (this.tmp.type != 'SUB') {
					content = content.split('<p>@SUBPress?' + subPress + '</p>').join('')
				}
				this.content = content
				this.filename = ''
			}
			this.modalMail = []
			var subIvoice = false
			if (this.tmp.typeOfHead == 'Invoices') {
				if (this.tmp.number.split(' ')[3] != undefined) {
					subIvoice = true
				}
			}
			if (this.tmp.typeOfHead == 'Sub Invoices') {
				if (this.tmp.number.split(' ')[3] != undefined) {
					subIvoice = true
				}
			}
			if ((this.tmp.type == 'SUB') || subIvoice) {
				axios.get('/get_sub_emails', {
					params: {
						factory: this.tmp.number.split(' ')[0]
					}
				}).then(response => {
					this.modalMail = response.data
				})
			}
			else {
				this.modalMail.push({
					item: this.selectCustomer.customerMail,
					name: this.selectCustomer.customerMail
				})
				val.forEach((val) => {
					this.modalMail.push({
						item: val.mail,
						name: val.mail
					})
				})
			}
			this.modalFiles = []
			this.responseFiles.forEach((val) => {
				var t = (val.html == 'file') ? 'f' : 'd'
				this.modalFiles.push({
					item: t + '-' + val.id,
					name: val.name.split('.pdf')[0]
				})
			})
			this.mailmodalshow()
		},
		sendTimeTableMail(val) {
			var subjectFromPlan = null
			var contentFromPlan = null
			var filenameFromPlan = null
			axios.get('/get_plan', {
				params: {
					id: this.tmp.id
				}
			}).then(response => {
				if (response.data != null) {
					this.mailSelectPlan = response.data.to.split(',')
					this.selectedDateForSend = response.data.period
					this.detectPeriod = response.data.period
					subjectFromPlan = response.data.subject
					contentFromPlan = response.data.content
					filenameFromPlan = response.data.name
					this.planid = response.data.id
					this.selperiodFinishWork = response.data.autoPeriodWorks
					if (response.data.autoDate == 1) this.autoDate = true
					if ((response.data.autoDate == 0) && (response.data.autoDate == null)) {
						this.autoDate = false
						this.selperiodFinishWork = null
					}
					if (response.data.autosend == 1) this.autoSend = true
					if (response.data.autosend == 0) this.autoSend = false
					if (response.data.pushToWorkDays == 1) this.pushToWorkDays = true
					if (response.data.pushToWorkDays == 0) this.pushToWorkDays = false
				}
				var namePerson = this.selectPerson.name.split(' ')
				var name = (namePerson.length == 3) ? namePerson[0] + ' ' + namePerson[2] : this.selectPerson.name
				if ((this.contentPlan == null) || (this.contentPlan == '')) {
					this.modalMail = []
					this.mailSelect = []
					var subject = this.beforeSubject
					var number = (this.tmp.typeOfHead == 'Invoices') ? (this.tmp.number.split(' ').length == 5) ? this.tmp.number.split(' ')[3] :
						this.countDigitals(this.tmp.number.split(' ')[1]) + '-' + this.tmp.number.split(' ')[0].split('-')[1] : (this.tmp.typeOfHead == 'SUB') ?
						this.tmp.number.split(' ')[0] : (this.tmp.typeOfHead == 'Sub Invoices') ? this.tmp.number.split(' ')[3] : this.tmp.number
					subject = subject.split('@Number').join(number ? number : '')
					subject = subject.split('@Document').join(this.tmp.date ? this.tmp.date : '')
					subject = subject.split('@Place').join(this.tmp.place ? this.tmp.place : '')
					subject = subject.split('@Order').join(this.tmp.other ? this.tmp.other : '')
					subject = subject.split('@Insurance').join(this.tmp.insurance ? this.tmp.insurance : '')
					subject = subject.split('@InsName').join(this.tmp.insurname ? this.tmp.insurname : '')
					if (subjectFromPlan != null) {
						this.subjectPlan = subjectFromPlan
					}
					else {
						this.subjectPlan = subject
					}
					var content = this.beforeMail
					content = content.split('@Respect').join('geehrte' + (('Herr' == name.split(' ')[0]) ? 'r' : ''))
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
					if (this.tmp.type == 'Invoices') {
						content = content.split('<p>@InvPress?' + invPress + '</p>').join(invPress)
					}
					if (this.tmp.type != 'Invoices') {
						content = content.split('<p>@InvPress?' + invPress + '</p>').join('')
					}
					if (this.tmp.type == 'Offers') {
						content = content.split('<p>@OfferPress?' + offerPress + '</p>').join(offerPress)
					}
					if (this.tmp.type != 'Offers') {
						content = content.split('<p>@OfferPress?' + offerPress + '</p>').join('')
					}
					if (this.tmp.type == 'SUB') {
						content = content.split('<p>@SUBPress?' + subPress + '</p>').join(subPress)
					}
					if (this.tmp.type != 'SUB') {
						content = content.split('<p>@SUBPress?' + subPress + '</p>').join('')
					}
					this.contentPlan = content
					this.filename = this.$t('oneCountAlret.Invoices') + ' @InvNo'
				}
				if (contentFromPlan != null) {
					this.contentPlan = contentFromPlan
				}
				if (filenameFromPlan != null) {
					this.filename = filenameFromPlan
				}
				this.modalMail = []
				var subIvoice = false
				if (this.tmp.typeOfHead == 'Invoices') {
					if (this.tmp.number.split(' ')[3] != undefined) {
						subIvoice = true
					}
				}
				if (this.tmp.typeOfHead == 'Sub Invoices') {
					if (this.tmp.number.split(' ')[3] != undefined) {
						subIvoice = true
					}
				}
				if ((this.tmp.type == 'SUB') || subIvoice) {
					axios.get('/get_sub_emails', {
						params: {
							factory: this.tmp.number.split(' ')[0]
						}
					}).then(response => {
						this.modalMail = response.data
					})
				}
				else {
					this.modalMail.push({
						item: this.selectCustomer.customerMail,
						name: this.selectCustomer.customerMail
					})
					val.forEach((val) => {
						this.modalMail.push({
							item: val.mail,
							name: val.mail
						})
					})
				}
				this.timeTableMailModalShow()
			})
		},
		sendmail() {
			if (this.mailSelect.length < 1) alert(this.$t('alert.noRecipients'))
			if (this.subject == null) alert(this.$t('alert.noSubject'))
			if ((this.subject != null) && (this.mailSelect.length >= 1)) {
				if (this.selectedFiles != null) {
					var files = this.selectedFiles.join()
				}
				else {
					var files = '_'
				}
				var from = this.$security.table.account.mail;
				var to = this.mailSelect.join();
				axios.post('/send_mail', {
					from: from,
					to: to,
					subject: this.subject,
					content: (this.content == null) ? '' : this.content,
					filename: this.filename,
					files: files
				}).then(response => {
					this.mailmodalhide()
					this.$refs.calProject.showAlert(this.mailSelect.join())
					this.content = null
				})
			}
		},
		sendtimetablemail(type) {
			var from = this.$security.table.account.mail;
			var to = this.mailSelectPlan.join();
			var params = null
			if (type == 'plan_mail') {
				params = {
					'item': this.tmp.id,
					'period': this.selectedDateForSend,
					'from': from,
					'to': to,
					'subject': this.subjectPlan,
					'name': this.filename,
					'autosend': this.autoSend,
					'autodate': this.autoDate ? 1 : 0,
					'autoperiodworks': this.selperiodFinishWork,
					'pushToWorkDays': this.pushToWorkDays ? 1 : 0,
					'content': (this.contentPlan == null) ? '' : this.contentPlan
				}
			}
			if (type == 'replan_mail') {
				params = {
					'item': this.tmp.id,
					'period': this.selectedDateForSend,
					'from': from,
					'to': to,
					'subject': this.subjectPlan,
					'name': this.filename,
					'autosend': this.autoSend,
					'autodate': this.autoDate ? 1 : 0,
					'autoperiodworks': this.selperiodFinishWork,
					'pushToWorkDays': this.pushToWorkDays ? 1 : 0,
					'content': (this.contentPlan == null) ? '' : this.contentPlan,
					'id': this.planid
				}
			}
			if (type == 'remove_mail') {
				params = {
					id: this.planid
				}
			}
			if (this.mailSelectPlan.length < 1) alert(this.$t('alert.noRecipients'))
			if (this.subjectPlan == null) alert(this.$t('alert.noSubject'))
			if ((this.subjectPlan != null) && (this.mailSelectPlan.length >= 1)) {
				axios.post('/' + type, params)
				this.timetableMailModalHide()
				this.contentPlan = null
			}
		},
		mapmodalhide() {
			this.mapmodal = false;
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		mapmodalshow() {
			this.mapmodal = true;
		},
		mailmodalhide() {
			this.mailmodal = false;
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		timetableMailModalHide() {
			this.contentPlan = null;
			this.planid = null;
			this.timetableMailModal = false;
			this.detectPeriod = null;
			this.selectedDateForSend = null;
			this.mailSelectPlan = [];
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		mailmodalshow() {
			this.mailmodal = true;
		},
		timeTableMailModalShow() {
			this.timetableMailModal = true;
		},
		closeaddok() {
			this.addSameModalWindow = false;
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		openWindowPrint() {
			this.windowPrint = true;
		},
		hideWindowPrint() {
			this.windowPrint = false;
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		// tabletopartx(tables) {
		// 	this.partx = [];
		// 	this.partx = tables;
		// 	this.rowsLoading = false;
		// 	if (this.partx.length > 0) {
		// 		this.rowsBusy = false;
		// 	}
		// 	else {
		// 		this.rowsBusy = true;
		// 	}
		// },
		ploadDocToFrame(row) {
			row.toggleDetails();
			var index = row.index;
			if (row.detailsShowing == false) {
				this.dropDoc = false
				setTimeout(() => {
					this.$refs.docs2 ? this.$refs.docs2.$refs['ifrForm' + index].submit() : ''
				}, 50);
			}
		},
		prowSelected(items) {
			if (this.selectedPrice.indexOf(items) == -1) {
				this.selectedPrice = this.selectedPrice.filter((v) => {
					if (v.id != items.id) {
						return v
					}
				});
				this.selectedPrice.push(items);
				items._rowVariant = 'success';
			}
			else {
				this.selectedPrice.splice(this.selectedPrice.indexOf(items), 1)
				items._rowVariant = ''
			}
		},
		prowSelectedDev(items) {
			if (this.selectedPriceDev.indexOf(items) == -1) {
				this.selectedPriceDev = this.selectedPriceDev.filter((v) => {
					if (v.id != items.id) {
						return v
					}
				});
				this.selectedPriceDev.push(items);
				items._rowVariant = 'success';
			}
			else {
				this.selectedPriceDev.splice(this.selectedPriceDev.indexOf(items), 1)
				items._rowVariant = ''
			}
		},
		prowSelectedReport(items) {
			if (this.selectedReport.indexOf(items) == -1) {
				this.selectedReport = this.selectedReport.filter((v) => {
					if (v.id != items.id) {
						return v
					}
				});
				this.selectedReport.push(items);
				items._rowVariant = 'success';
			}
			else {
				this.selectedReport.splice(this.selectedReport.indexOf(items), 1)
				items._rowVariant = ''
			}
		},
		prowSelectedDoc(items) {
			if (this.selectedPriceDoc.indexOf(items) == -1) {
				this.selectedPriceDoc = this.selectedPriceDoc.filter((v) => {
					if (v.id != items.id) {
						return v
					}
				});
				this.selectedPriceDoc.push(items);
				items._rowVariant = 'success';
			}
			else {
				this.selectedPriceDoc.splice(this.selectedPriceDoc.indexOf(items), 1)
				items._rowVariant = ''
			}
		},
		prowSelectedImg(items) {
			if (this.selectedPriceImg.indexOf(items) == -1) {
				this.selectedPriceImg = this.selectedPriceImg.filter((v) => {
					if (v.id != items.id) {
						return v
					}
				});
				this.selectedPriceImg.push(items);
				items._rowVariant = 'success';
			}
			else {
				this.selectedPriceImg.splice(this.selectedPriceImg.indexOf(items), 1)
				items._rowVariant = ''
			}
		},
		selectedModalDoc(val) {
			var docs_ids = []
			var files_ids = []
			this.selectedPriceDoc.forEach((val) => {
				if (val.html != 'file') {
					docs_ids.push(val.id)
				}
				else {
					files_ids.push(val.id)
				}
			})
			axios.get('/mv_docs', {
				params: {
					docs_ids: docs_ids.join(),
					files_ids: files_ids.join(),
					new_menu: val.id
				}
			}).then(response => {
				setTimeout(() => {
					this.getDocs();
				}, 20);
			})
		},
		selectedModalImag(val) {
			var files_ids = []
			this.selectedPriceImg.forEach((val) => {
				var id = val.id.split('=')
				files_ids.push(id[1])
			})
			axios.get('/mv_images', {
				params: {
					files_ids: files_ids.join(),
					new_menu: val.id
				}
			}).then(response => {
				setTimeout(() => {
					this.getDocs();
				}, 20);
			})
		},
		okMoveDoc() {
			this.selectedPriceDoc = [],
				this.$refs.movedoc.hide()
		},
		okMoveImg() {
			this.selectedPriceImg = [],
				this.$refs.moveImag.hide()
		},
		detectRowSise(items) {
			var returnArr = []
			var addCount = ''
			function findLevel(obj) {
				obj.forEach((val) => {
					returnArr.push({
						name: addCount + val.name,
						id: val.id
					})
					if (val.children.length != 0) {
						addCount = addCount + "-"
						findLevel(val.children)
					}
					else {
						addCount = ''
					}
				})
			}
			findLevel(items)
			return returnArr.length
		},
		detectItem(items) {
			var returnArr = []
			var addCount = ''
			function findLevel(obj) {
				obj.forEach((val) => {
					returnArr.push({
						name: addCount + val.name,
						id: val.id
					})
					if (val.children.length != 0) {
						addCount = addCount + "-"
						findLevel(val.children)
					}
					else {
						addCount = ''
					}
				})
			}
			findLevel(items)
			return returnArr
		},
		sendPrice() {
			var ids = [] //приходят объекты, поэтому приходиться делать новый список
			this.selectedPrice.forEach((v, i) => {
				ids.push(v.id)
			})

			axios.get('/send_price', {
				params: {
					ids: ids.join(),
					names: this.selectedTables.join()
				}
			}).then(response => {
				this.selectedPrice = []
				// this.selectedTables = []
				this.itemsPrice.forEach(v => {
					v._rowVariant = ''
				})
			})
		},
		sendDevice() {
			var ids = []
			this.selectedPriceDev.forEach((v, i) => {
				ids.push(v.id)
			})
			axios.get('/send_devices', {
				params: {
					ids: ids.join(),
					names: this.selectedTables.join()
				}
			}).then(response => {
				this.selectedPriceDev = []
				this.itemsPriceDev.forEach(v => {
					v._rowVariant = ''
				})
			})
		},
		sendReport() {
			var ids = []
			this.selectedReport.forEach((v, i) => {
				ids.push(v.id)
			})
			axios.get('/send_reports', {
				params: {
					ids: ids.join(),
					names: this.selectedTables.join()
				}
			}).then(response => {
				this.selectedReport = []
				this.itemsReport.forEach(v => {
					v._rowVariant = ''
				})
			})
		},
		removePrice() {
			if (this.idNode == null) {
				alert(this.$t('alert.noItemSelectForDel'))
			}
			else {
				if (confirm(this.$t('alert.remove'))) {
					axios.get('/remove_price_menu', {
						params: {
							remove_id: this.idNode
						}
					}).then(response => {
						this.idNode = null,
							this.nameNode = null
					})
				}
			}
		},
		removeDevice() {
			if (this.idNodeDev == null) {
				alert(this.$t('alert.noItemSelectForDel'))
			}
			else {
				if (confirm(this.$t('alert.remove'))) {
					axios.get('/remove_devices_menu', {
						params: {
							remove_id: this.idNodeDev
						}
					}).then(response => {
						this.idNodeDev = null,
							this.nameNodeDev = null
					})
				}
			}
		},
		removeDoc() {
			if (this.idNodeDoc == null) {
				alert(this.$t('alert.noItemSelectForDel'))
			}
			else {
				if (confirm(this.$t('alert.remove'))) {
					axios.get('/remove_docs_menu', {
						params: {
							remove_id: this.idNodeDoc
						}
					}).then(response => {
						this.idNodeDoc = null,
							this.nameNodeDoc = null
					})
				}
			}
		},
		removeImag() {
			if (this.idNodeImg == null) {
				alert(this.$t('alert.noItemSelectForDel'))
			}
			else {
				if (confirm(this.$t('alert.remove'))) {
					axios.get('/remove_image_menu', {
						params: {
							remove_id: this.idNodeImg
						}
					}).then(response => {
						this.idNodeImg = null,
							this.nameNodeImag = null
					})
				}
			}
		},
		removeReport() {
			if (this.idNodeReport == null) {
				alert(this.$t('alert.noItemSelectForDel'))
			}
			else {
				if (confirm(this.$t('alert.remove'))) {
					axios.get('/remove_report_menu', {
						params: {
							remove_id: this.idNodeReport
						}
					}).then(response => {
						this.idNodeReport = null,
							this.nameNodeReport = null
					})
				}
			}
		},
		addPrice() {
			function findLevel(obj, id) {
				if (id == null) {
					id = 0,
						obj.push({
							id: 0,
							children: []
						})
				}
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/add_price_menu', {
							params: {
								parent_id: val.id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenu, this.idNode)
		},
		addDevice() {
			function findLevel(obj, id) {
				if (id == null) {
					id = 0,
						obj.push({
							id: 0,
							children: []
						})
				}
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/add_devices_menu', {
							params: {
								parent_id: val.id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenuDev, this.idNodeDev)
		},
		addDoc() {
			var newName = this.$t('projectDetail.plusPart');
			function findLevel(obj, id, project) {
				if (id == null) {
					id = 0,
						obj.push({
							id: 0,
							children: []
						})
				}
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/add_docs_menu', {
							params: {
								parent_id: val.id,
								project: project,
								newName: newName
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id, project, newName)
						}
					}
				})
			}
			findLevel(this.itemsMenuDoc, this.idNodeDoc, this.id)
		},
		addImag() {
			var newName = this.$t('projectDetail.plusPart')
			function findLevel(obj, id, project) {
				if (id == null) {
					id = 0,
						obj.push({
							id: 0,
							children: []
						})
				}
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/add_images_menu', {
							params: {
								parent_id: val.id,
								project: project,
								newName: newName
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id, project, newName)
						}
					}
				})
			}
			findLevel(this.itemsMenuImag, this.idNodeImg, this.id)
		},
		addReport() {
			function findLevel(obj, id) {
				if (id == null) {
					id = 0,
						obj.push({
							id: 0,
							children: []
						})
				}
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/add_report_menu', {
							params: {
								parent_id: val.id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenuReport, this.idNodeReport)
		},
		getPrices() {
			if (this.idNode != null) {
				axios.get('/prices', {
					params: {
						id: this.idNode ? this.idNode : 0
					}
				}).then(response => {
					this.itemsPrice = response.data
				})
			}
			axios.get('/price_menu').then(response => {
				this.itemsMenu = [];
				response.data.forEach((val) => {
					if (val.parrent == 0) {
						val['children'] = []
						this.itemsMenu.push(val);
					}
				});
				response.data.forEach((valResp) => {
					function findLevel(obj, id) {
						obj.forEach((val) => {
							if (val.id == id) {
								valResp['children'] = []
								val.children.push(valResp);
							}
							else {
								if (val.children.length != 0) {
									findLevel(val.children, id)
								}
							}
						})
					}
					findLevel(this.itemsMenu, valResp.parrent)
				});
			})
		},
		getDevices() {
			if (this.idNodeDev != null) {
				axios.get('/devices', {
					params: {
						id: this.idNodeDev ? this.idNodeDev : 0
					}
				}).then(response => {
					this.itemsPriceDev = response.data
				})
			}
			axios.get('/devices_menu').then(response => {
				this.itemsMenuDev = [];
				response.data.forEach((val) => {
					if (val.parrent == 0) {
						val['children'] = []
						this.itemsMenuDev.push(val);
					}
				});
				response.data.forEach((valResp) => {
					function findLevel(obj, id) {
						obj.forEach((val) => {
							if (val.id == id) {
								valResp['children'] = []
								val.children.push(valResp);
							}
							else {
								if (val.children.length != 0) {
									findLevel(val.children, id)
								}
							}
						})
					}
					findLevel(this.itemsMenuDev, valResp.parrent)
				});
			})
		},
		getReports() {
			if (this.idNodeDev != null) {
				axios.get('/reports', {
					params: {
						id: this.idNodeReport ? this.idNodeReport : 0
					}
				}).then(response => {
					this.itemsReport = response.data
				})
			}
			axios.get('/reports_menu').then(response => {
				this.itemsMenuReport = [];
				response.data.forEach((val) => {
					if (val.parrent == 0) {
						val['children'] = []
						this.itemsMenuReport.push(val);
					}
				});
				response.data.forEach((valResp) => {
					function findLevel(obj, id) {
						obj.forEach((val) => {
							if (val.id == id) {
								valResp['children'] = []
								val.children.push(valResp);
							}
							else {
								if (val.children.length != 0) {
									findLevel(val.children, id)
								}
							}
						})
					}
					findLevel(this.itemsMenuReport, valResp.parrent)
				});
			})
		},
		getDocs() {
			axios.get('/docs_menu', {
				params: {
					project: this.id
				}
			}).then(response => {
				this.itemsMenuDoc = [];
				this.itemsMenuDoc.push({
					id: -1,
					name: 'General Folder',
					parrent: 0,
					children: []
				});
				this.docs_menu_ids.push(-1);
				response.data.forEach((val) => {
					if (val.parrent == 0) {
						val['children'] = []
						this.itemsMenuDoc.push(val);
					}
				});
				response.data.forEach((valResp) => {
					function findLevel(obj, id) {
						obj.forEach((val) => {
							if (val.id == id) {
								valResp['children'] = []
								val.children.push(valResp);
							}
							else {
								if (val.children.length != 0) {
									findLevel(val.children, id)
								}
							}
						})
					}
					this.docs_menu_ids.push(valResp.id);
					findLevel(this.itemsMenuDoc, valResp.parrent)
				});
				this.responseFiles = [];
				this.docs2files();
				axios.get('/images_menu', {
					params: {
						project: this.id
					}
				}).then(response => {
					this.itemsMenuImag = [];
					this.itemsMenuImag.push({
						id: -1,
						name: 'General Folder',
						parrent: 0,
						children: []
					});
					this.images_menu_ids.push(-1);
					response.data.forEach((val) => {
						if (val.parrent == 0) {
							val['children'] = []
							this.itemsMenuImag.push(val);
						}
					});
					response.data.forEach((valResp) => {
						function findLevel(obj, id) {
							obj.forEach((val) => {
								if (val.id == id) {
									valResp['children'] = []
									val.children.push(valResp);
								}
								else {
									if (val.children.length != 0) {
										findLevel(val.children, id)
									}
								}
							})
						}
						this.images_menu_ids.push(valResp.id)
						findLevel(this.itemsMenuImag, valResp.parrent)
					})
				})
				this.getdomageImages()
			})
		},
		toModel(enterVal) {
			function findLevel(obj, id) {
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/update_name_price_menu', {
							params: {
								name: enterVal,
								id: id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenu, this.idNode)
		},
		toModelDev(enterVal) {
			function findLevel(obj, id) {
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/update_name_devices_menu', {
							params: {
								name: enterVal,
								id: id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenuDev, this.idNodeDev)
		},
		toModelDoc(enterVal) {
			function findLevel(obj, id) {
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/update_name_docs_menu', {
							params: {
								name: enterVal,
								id: id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenuDoc, this.idNodeDoc)
		},
		toModelImag(enterVal) {
			function findLevel(obj, id) {
				obj.forEach((val) => {
					if (val.id == id) {
						axios.get('/update_name_images_menu', {
							params: {
								name: enterVal,
								id: id
							}
						})
					}
					else {
						if (val.children.length != 0) {
							findLevel(val.children, id)
						}
					}
				})
			}
			findLevel(this.itemsMenuImag, this.idNodeImg)
		},
		nodeDisTurn() {
			if (confirm(this.$t('alert.rename'))) {
				this.nodeDis = false
			}
		},
		nodeDisTurnDev() {
			if (confirm(this.$t('alert.rename'))) {
				this.nodeDisDev = false
			}
		},
		nodeDisTurnReport() {
			if (confirm(this.$t('alert.rename'))) {
				this.nodeDisReport = false
			}
		},
		nodeDisTurnDoc() {
			if (confirm(this.$t('alert.rename'))) {
				this.nodeDisDoc = false
			}
		},
		nodeDisTurnImag() {
			if (confirm(this.$t('alert.rename'))) {
				this.nodeDisImag = false
			}
		},
		pcurNodeClicked(model, component) {
			this.nameNode = model.name,
				this.idNode = model.id
			if (this.idNode == this.oldId) {
				if (this.itemsPrice.length > 0) {
					this.itemsPrice = []
				}
				else {
					axios.get('/prices', {
						params: {
							id: model.id
						}
					}).then(response => {
						this.itemsPrice = response.data;
						this.$refs.priceChild1.loded();
					})
				}
			}
			else {
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
			if ((model.parrent == 0) && component.folder == false) {
				this.idNode = null
			}
		},
		pcurNodeClickedDev(model, component) {
			this.nameNodeDev = model.name,
				this.idNodeDev = model.id
			if (this.idNodeDev == this.oldIdDev) {
				if (this.itemsPriceDev.length > 0) {
					this.itemsPriceDev = []
				}
				else {
					axios.get('/devices', {
						params: {
							id: model.id
						}
					}).then(response => {
						this.itemsPriceDev = response.data;
						this.$refs.devChild1.loded();
					})
				}
			}
			else {
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
			if ((model.parrent == 0) && component.folder == false) {
				this.idNodeDev = null
			}
		},
		pcurNodeClickedReport(model, component) {
			this.nameNodeReport = model.name,
				this.idNodeReport = model.id
			if (this.idNodeReport == this.oldIdReport) {
				if (this.itemsReport.length > 0) {
					this.itemsReport = []
				}
				else {
					axios.get('/reports', {
						params: {
							id: model.id
						}
					}).then(response => {
						this.itemsReport = response.data;
						this.$refs.reportChild1.loded();
					})
				}
			}
			else {
				axios.get('/reports', {
					params: {
						id: model.id
					}
				}).then(response => {
					this.itemsReport = response.data;
					this.$refs.reportChild1.loded();
				})
			}
			this.oldIdReport = this.idNodeReport
			if ((model.parrent == 0) && component.folder == false) {
				this.idNodeReport = null
			}
		},
		pcurNodeClickedDoc(model, component) {
			this.nameNodeDoc = model.name,
				this.idNodeDoc = model.id
			if (this.idNodeDoc == this.oldIdDoc) {
				if (this.itemsPriceDoc.length > 0) {
					this.itemsPriceDoc = []
				}
				this.$refs.docs2.loded()
			}
			this.oldIdDoc = this.idNodeDoc
			if ((model.parrent == 0) && component.folder == false) {
				this.idNodeDoc = null
			}
		},
		pcurNodeClickedImg(model, component) {
			this.nameNodeImag = model.name,
				this.idNodeImg = model.id
			if (this.idNodeImg == this.oldIdImg) {
				this.$refs.images1.loded()
			}
			this.oldIdImg = this.idNodeImg
			if ((model.parrent == 0) && component.folder == false) {
				this.idNodeImg = null
			}
		},
		showx(classId, index) {
			const viewer = this.$el.querySelector('.' + classId).$viewer
			viewer.index = index
			viewer.show()
		},
		disablefild(fild, id) {
			var result = false
			this.looks.forEach((val) => {
				if (val.rows_id == id) {
					if (val.fild == fild) {
						result = true
					}
				}
			})
			if (this.stopDis == true) result = false
			if (this.type == 'Invoices') result = true
			return result
		},
		disablefildUser(fild, id) {
			var result
			this.looks.forEach((val) => {
				if (val.rows_id == id) {
					if (val.fild == fild) {
						result = val.user
					}
				}
			})
			return result
		},
		changeDisable(type_operation, fild, id) {
			this.stopDis = (type_operation == 'f')
			axios.get('/changeDisableTable', {
				params: {
					type_operation: type_operation,
					fild: fild,
					id: id,
					'user': this.$security.account['first_name'] + '_' + this.$security.account['second_name']
				}
			})
			if (type_operation == 'f') {
				setTimeout(() => {}, 15000);
			}
		},
		getdomageImages() {
			axios.get('/domage_images', {
				params: {
					id: this.id,
					project: (this.project.number == null) ? '0001' : this.project.number
				}
			}).then(response => {
				this.domageImages = response.data.filter(function (v) {
					if ((v.file_name.split('.')[v.file_name.split('.').length - 1]) != 'pdf') {
						return v
					}
				})
			})
		},
		countDigitals(val) {
			var nuls = 3 - val.toString().length
			for (var i = 0; i <= nuls; i++) {
				val = '0' + val
			}
			return val
		},
		updateItem(val, type, id) {
			axios.post('/update_item_from_project', {
				val: val,
				type: type,
				id: id
			}).then(response => {
				this.cloudLoad = false;
			});
		},
		updatefilename(val, type, id) {
			axios.get('/updatefilename', {
				params: {
					val: val,
					type: type,
					id: id
				}
			})
		},
		updatedocname(val, type, id) {
			axios.get('/updatedocname', {
				params: {
					val: val,
					type: type,
					id: id
				}
			})
		},
		showCommetnts() {
			this.tmp.number = null,
				this.tmp.typeOfHead = null,
				this.tmp.id = null,
				this.generalComments = true
			if (this.dubTabIndex == 0) {
				setTimeout(() => {
					this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 56)
				}, 300)
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
				this.docs = (this.docs != response.data) ? response.data : this.docs
				axios.get('/files', {
					params: {
						id: (this.project.number == null) ? '0001' : this.project.number
					}
				}).then(response => {
					var rows1 = this.getItems('Offers').filter((v) => {
						v.type = 'Offers'
						return v
					})
					var rows2 = this.getItems('Orders').filter((v) => {
						v.type = 'Orders'
						return v
					})
					var rows3 = this.getItems('Invoices').filter((v) => {
						v.type = 'Invoices'
						return v
					})
					var mergedArr = rows1.concat(rows2.concat(rows3))
					if (mergedArr.length == 0) {
						mergedArr.push({
							'id': 0
						})
					}
					this.files = (this.files != response.data) ? response.data : this.files
					var addFiles = []
					mergedArr.forEach((item) => {
						axios.get('/get_tables_for_docs', {
							params: {
								id: item.id
							}
						}).then(response => {
							var filesarr = response.data
							files = this.files.filter(function (val) {
								var ret
								filesarr.forEach((v) => {
									ret = 1
									if (val.name.split('.')[val.name.split('.').length - 1] == 'pdf') {
										if (v.parts != undefined) {
											if (val.group.split(',').length > 1) {
												ret = 0
												var subval = []
												val.group.split(',').forEach((valGroup) => {
													subval = JSON.parse(JSON.stringify(val))
													subval.group = valGroup
													if (subval.group == v.parts.id) {
														subval.group = v.parts.part_name + ' from ' + item.type
														addFiles.push(subval)
													}
												})
											}
											if (ret == 1) {
												if (val.group == v.parts.id) {
													val.group = v.parts.part_name + ' from ' + item.type
												}
											}
										}
									}
								})
								if (ret == 1) {
									return val.name.split('.')[val.name.split('.').length - 1] == 'pdf'
								}
							})
							addgroup = []
							if (addFiles.length != 0) files = files.concat(addFiles)
							files1 = files.filter((file, i) => {
								if (file.name.split('.')[file.name.split('.').length - 1] != 'pdf') {
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
							var change = 0
							if (this.responseFiles.length != this.docs.concat(files).length) {
								change = 1
							}
							if (this.responseFiles.length == 0) {
								change = 1
							}
							this.responseFiles.forEach((v, i) => {
								if (this.docs.concat(files)[i] != undefined) {
									if (v.name != this.docs.concat(files)[i].name) {
										change = 1
									}
								}
							})
							if (change == 1) //хотя лучше элименты сравнить, что бы не закрывался фрейм с пдф
							{
								this.responseFiles = this.docs.concat(files)
							}
						})
					})
				})
			})
		},
		fsadd2() {
			this.$refs.myVueDropzone2.removeAllFiles()
		},
		fsadd3() {
			this.$refs.myVueDropzone3.removeAllFiles()
		},
		sendingEvent(file, xhr, formData) {
			var selectTables = []
			this.partx.forEach(function (val, index) {
				if (val.parts.toggle) {
					selectTables.push(val.parts.id)
				}
			})
			xhr.setRequestHeader('X-Number', this.project.number);
			xhr.setRequestHeader('X-Folder', this.idNodeDoc);
			xhr.setRequestHeader('X-Group', selectTables);
			xhr.setRequestHeader('X-User', this.$security.account['first_name'] + '_' + this.$security.account['second_name']);
		},
		sendingEventImage(file, xhr, formData) {
			var selectTables = []
			this.partx.forEach(function (val, index) {
				if (val.parts.toggle) {
					selectTables.push(val.parts.id)
				}
			})
			xhr.setRequestHeader('X-Number', this.project.number);
			xhr.setRequestHeader('X-Folder', this.idNodeImg);
			xhr.setRequestHeader('X-Group', selectTables);
			xhr.setRequestHeader('X-User', this.$security.account['first_name'] + '_' + this.$security.account['second_name']);
		},
		// allSumms() {
		// 	var allSumms = this.$t('projectDetail.general') + ': ' + this.$options.filters.thousandSeparator(this.alltotal(this.partx));
		// 	var altSumms = this.$t('projectDetail.alternative') + ': ' + this.$options.filters.thousandSeparator(this.altalltotal(this.partx));
		// 	var returnSumms = (this.altalltotal(this.partx) == 0) ? (allSumms) : (allSumms + ' I ' + altSumms);
		// 	if (this.dubTabIndex == 0) {
		// 		setTimeout(() => {
		// 			if (this.weval != this.$refs.editList.$refs.editcomponet.clientHeight) {
		// 				this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 82)
		// 			}
		// 		}, 300);
		// 	}
		// 	return returnSumms;
		// },
		// alltotal: function () {
		// 	var summa = 0
		// 	this.partx.forEach(function (val) {
		// 		val.parts.part_content.forEach(function (val1) {
		// 			if (val1.status == 'yes') {
		// 				summa += val1.count * val1.price
		// 			}
		// 		})
		// 	})
		// 	return summa;
		// },
		// altalltotal: function () {
		// 	var summa = 0
		// 	this.partx.forEach(function (val) {
		// 		val.parts.part_content.forEach(function (val1) {
		// 			if (val1.status != 'yes') {
		// 				summa += val1.count * val1.price
		// 			}
		// 		})
		// 	})
		// 	return summa;
		// },
		worker() {
			this.workerModal = true
		},
		closeWorkerModal() {
			this.workerModal = false;
			if (this.comtomodal != null) this.tabxmodal = true;
		},
		addOk(work) {
			this.addSameModalWindow = false
			if (this.comtomodal != null) this.tabxmodal = true
			axios.get('/add_same', {
				params: {
					add_number: (this.project.number == null) ? '0001' : this.project.number,
					add_insurance_number: '',
					add_place: '',
					add_work: work,
					add_comment: '',
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
					this.tablesBusy = false;
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
		getItems(type) {
			if (type != 'Orders') {
				if (type != 'SUB') {
					if (type != 'Sub Invoices') {
						if (type != 'Invoices') {
							return this.itemsTable.filter((v) => {
								if (v.type == type) {
									v._rowVariant = (v.id == this.selrow) ? 'secondary' : ''
									return v
								}
							})
						}
					}
				}
			}
			if (type == 'Orders') {
				var orderandsub = []
				var onlisub = []
				this.itemsTable.forEach((v) => {
					if (v.type == 'Orders') {
						v._rowVariant = (v.id == this.selrow) ? 'secondary' : ''
						var xid = v.id
						onlisub = []
						this.itemsTable.forEach((vx) => {
							if (vx.type == 'SUB') {
								var intId = parseInt(vx.number.split(' ')[1])
								if (xid == intId) {
									vx._rowVariant = "primaryHide"
									this.showsubarr.forEach((ss) => {
										if (intId == ss) {
											vx._rowVariant = (vx.id == this.selrow) ? 'secondary' : ''
										}
									})
									onlisub.push(vx)
								}
							}
						})
						var mer = []
						mer.push(v)
						var segmer = mer.concat(onlisub)
						orderandsub = JSON.parse(JSON.stringify(orderandsub.concat(segmer)));
					}
				})
				return orderandsub
			}
			if (type == 'Invoices') {
				var invoices = []
				this.itemsTable.forEach((v) => {
					if (v.type == 'Invoices') {
						v._rowVariant = (v.id == this.selrow) ? 'secondary' : '',
							invoices.push(v)
					}
					if (v.type == 'Sub Invoices') {
						v._rowVariant = (v.id == this.selrow) ? 'secondary' : '',
							invoices.push(v)
					}
				})
				return invoices
			}
		},
		pinItemGetData(item, index) {
			this.inItemGetData(item, index)
		},
		pgetcontact(id) {
			this.get_contact(id)
		},
		pgetperson(id, mnew) {
			this.get_person(id, mnew)
		},
		pofferDel(del_id) {
			this.offerDel(del_id)
		},
		inItemGetData(item, index) {
			if (item != undefined) {
				axios.get('/get_plan', {
					params: {
						id: item.id
					}
				}).then(response => {
					this.plan = response.data
					this.selrow = item.id,
						item._rowVariant = (item.id == this.selrow) ? 'secondary' : '',
						this.generalComments = false,
						// this.tmp.typeOfHead = ((this.tmp.typeOfHead != 'Devices') & (this.tmp.typeOfHead != 'Damage') & (this.tmp.typeOfHead != 'Reports')) ? item.type : this.tmp.typeOfHead,
						this.beforeTab = item.type,
            this.tmp = item
						// this.tmp.number = item.number,
						// this.tmp.date = item.date,
						// this.tmp.place = item.place,
						// this.tmp.insurance = item.insurance_number,
						// this.tmp.insurname = item.insurname,
						// this.tmp.work = item.work,
						// this.tmp.other = item.other,
						// this.tmp.type = item.type,
						// this.tmp.id = item.id,
						// this.tmp.dateEvent = item.dateEvent,
						// this.tmp.dateInspect = item.dateInspect,
						// this.tmp.worker = item.ExamWorker,
						// this.tmp.comment = item.comment
            // console.log(item)
				})
			}
			// setTimeout(() => {
			// 	if (this.$refs.editList != undefined) {
			// 		if (item != undefined) {
			// 			this.$refs.editList.remoteTax(item.id)
			// 		}
			// 	}
			// }, 300)
			// }
		},
		get_person(id, mnew) {
			axios.get('/get_persons', {
				params: {
					id: id
				}
			}).then(response => {
				this.availablePersons = []
				response.data.forEach((it) => {
					this.availablePersons.push({
						id: it.person,
						name: it.appeal + ' ' + it.names
					})
				})
				this.availablePersons.sort(function (a, b) {
					var nameA = a.name.toLowerCase(),
						nameB = b.name.toLowerCase()
					if (nameA < nameB) return -1
					if (nameA > nameB) return 1
					return 0
				})
				if (mnew == true) {
					this.selectPerson = {
						id: this.availablePersons[0].id,
						name: this.availablePersons[0].name
					}
					this.get_contact(this.selectPerson.id)
				}
			})
		},
		get_contact(id) {
			axios.get('/get_contact_person', {
				params: {
					id: id
				}
			}).then(response => {
				this.availableMails = []
				this.availablePhons = []
				this.availableMails = response.data.mail
				this.availablePhons = response.data.phone
				this.selectMail = this.availableMails[0] ? this.availableMails[0].mail : null
				this.selectPhone = this.availablePhons[0] ? this.availablePhons[0].phone : null
			})
		},
		get_types_for_tables_f(call) {
			axios.get('/get_types_for_tables', {}).then(response => {
				this.typesForTables = response.data.filter(function (v) {
					if ((v.type != 'SUB') && (v.type != 'Sub Invoices') && (v.type != 'Damage Description')) {
						return v
					}
				});
				this.tableLoading = false;
			});
			if (call == 'socket') {
				this.project_detail_new_f()
			}
		},
		get_workers_f() {
			axios.get('/get_workers', {}).then(response => {
				this.workers = [],
					response.data.forEach((v) => {
						this.workers.push((v.short_name != null) ? v.short_name : v.name),
							this.workersForSend.push({
								'value': v.id,
								'text': ((v.short_name != null) ? v.short_name : v.name)
							})
					})
			})
		},
		get_type_works() {
			axios.get('/get_type_works', {}).then(response => {
				this.works = response.data;
				this.works.unshift(this.$t('calcTableGroup.work'))
			})
		},
		project_detail_new_f() {
 			axios.get('/project_detail_new', {
				params: {
					id: this.id
				}
			}).then(response => {
				// response.data.filter((v) => {
				// 	if (v.number.split(' ').length != 5) {
				// 		v.netto = this.$options.filters.thousandSeparator(parseFloat(v.netto));
				// 		v.brutto = this.$options.filters.thousandSeparator(parseFloat(v.brutto));
				// 	}
				// 	else {
				// 		v.netto = '-' + this.$options.filters.thousandSeparator(parseFloat(v.netto));
				// 		v.brutto = '-' + this.$options.filters.thousandSeparator(parseFloat(v.brutto));
				// 	}
				// 	return v;
				// })
				this.itemsTable = response.data;
				if (this.itemsTable.length > 0) {
					this.tablesBusy = false;
				}
				else {
					this.tablesBusy = true;
				}
				setTimeout(() => {
					this.sm2lg('component', this.$refs['hproject'].clientHeight, 110)
					this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 56)
				}, 10);
        // console.log(this.itemsTable)
				if (this.tmp.id != undefined) {
					var item_list = this.itemsTable.filter((v) => {
						if (v.type == 'Orders' || v.type == 'Offers'|| v.type == 'Invoices') {
							if (v.id == this.tmp.id) {
								return v
							}
						}
					})
  					this.inItemGetData(item_list[0], 0)
				}
			})
		},
		getLoocks() {
			axios.get('/getLoocks').then(response => {
				this.looks = []
				this.looks = response.data
			})
		},
		project_detail_f(old) {
			axios.get('/project_detail', {
				params: {
					id: this.id
				}
			}).then(response => {
				if (response.data != null) {
					var num = response.data.project_number
					var nuls = 3 - num.toString().length
					for (var i = 0; i <= nuls; i++) {
						num = '0' + num
					}
					this.project.work = response.data.work,
						this.project.number = num + ((this.hideNumberOfYear != 1) ? ('-' + response.data.project_number_year) : ''),
						this.project.date = response.data.date,
						this.project.edate = response.data.edate,
						this.project.street1 = response.data.street1,
						this.project.city1 = response.data.city1,
						this.project.area = response.data.area,
						this.selectedCornty = (this.countries[this.countries.findIndex(x => x.code == response.data.country)]) ? this.countries[this.countries.findIndex(x => x.code == response.data.country)] : {
							code: null
						},
						this.project.zip1 = response.data.zip1,
						this.project.other = response.data.other,
						this.project.editor = response.data.first_name + ' ' + response.data.second_name,
						this.selectCustomer = {
							id: response.data.customer_id,
							name: response.data.name,
							adress: response.data.street,
							adress1: response.data.zip + ' ' + response.data.city,
							customerMail: response.data.customerMail
						},
						this.area = [{
							id: response.data.customer_id,
							name: response.data.name,
							adress: response.data.street,
							adress1: response.data.zip + ' ' + response.data.city
						}],
						this.selectPerson = {
							id: response.data.person_id,
							name: response.data.appeal + ' ' + response.data.names
						},
						this.get_contact(this.selectPerson.id),
						this.availablePersons = [{
							id: response.data.person_id,
							name: response.data.appeal + ' ' + response.data.names
						}],
						axios.get('/customer').then(response => {
							response.data.forEach((it) => {
								if (this.selectCustomer.id != it.id) this.area.push({
									id: it.id,
									name: it.name
								})
							})
							this.area.sort(function (a, b) {
								var nameA = a.name.toLowerCase(),
									nameB = b.name.toLowerCase()
								if (nameA < nameB) return -1
								if (nameA > nameB) return 1
								return 0
							})
						})
					this.get_person(this.selectCustomer.id, false)
				}
			})
		},
		getProjectDetail(old) {
			axios.get('/date_logo').then(response => {
				var separator = response.data.date_logo_address.split('- ')[0] + '- ';
				var address = response.data.date_logo_address.split(separator)[1];
				this.mail_address = address;
				this.mail_logo = response.data.date_logo_image;
				this.mail_date = response.data.date_logo.match(/(\b(https?|ftp|file):\/\/[-A-Z0-9+&@#\/%?=~_|!:,.;]*[-A-Z0-9+&@#\/%=~_|])/ig)[0];
			})
			if (this.typesForTables.length == 0) {
				this.get_types_for_tables_f('native')
			}
			this.project_detail_new_f()
			if (this.workers.length == 0) {
				this.get_workers_f()
			}
			if (this.tmp.number != null) {
				var cliked = this.itemsTable.filter((val) => {
					if (val.id == this.tmp.id) {
						return val
					}
				})
				this.countCall = this.countCall + 1
				this.inItemGetData(cliked[0], 0)
			}
			this.project_detail_f(old)
			this.project_id = this.id
		}
	},
	watch: {
		tabIndex: function (newv, oldv) {
			if (oldv != null) {
				if (newv == 0) {
					setTimeout(() => {
						this.sm2lg('component', this.$refs['hproject'].clientHeight, 110)
					}, 10);
				}
			}
		},
		wwidth: function () {
			if ((this.wcval != null) && (this.wcadd != null)) {
				this.sm2lg('component', this.wcval, this.wcadd)
			}
			if ((this.weval != null) && (this.weadd != null)) {
				this.sm2lg('edit', this.weval, this.weadd)
			}
		},
		mapmodal: function (value) {
			if (value == false) {
				this.mapmodalhide()
			}
		},
		mailmodal: function (value) {
			if (value == false) {
				this.mailmodalhide()
			}
		},
		dubTabIndex: function (value) {
			if (this.$refs.devices != undefined) {
				if (this.$refs.devices.localActive) {
					this.tmp.typeOfHead = 'Devices'
				}
			}
			if (this.$refs.reports != undefined) {
				if (this.$refs.reports.localActive) {
					this.tmp.typeOfHead = 'Reports'
				}
			}
			if (this.$refs.damage != undefined) {
				if (this.$refs.damage.localActive) {
					this.tmp.typeOfHead = 'Damage'
				}
			}
			if (((this.$refs.devices == undefined) || (this.$refs.devices.localActive == false)) &&
				((this.$refs.damage == undefined) || (this.$refs.damage.localActive == false)) &&
				((this.$refs.reports == undefined) || (this.$refs.reports.localActive == false))
			) {
				this.tmp.typeOfHead = this.beforeTab
			}
		}
	},
	mounted() {
		axios.get('/countries').then(response => {
			this.countries = response.data
		});
		axios.get('/variables').then(response => {
			this.addressfild = response.data[1].content.split(' ').join('+')
			this.beforeSubject = response.data[2].content
			this.beforeMail = response.data[3].content
			this.hideNumberOfYear = response.data[4].content
		});
		this.getProjectDetail(1);
		this.get_type_works();
		setTimeout(() => {
			this.getPrices();
			this.getDevices();
			this.getDocs();
			this.getReports();
			this.$options.sockets.onmessage = (data) => (data.data == 'getProjectDetail') ? (this.getProjectDetail(1)) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'get_types_for_tables_f') ? (this.get_types_for_tables_f('socket')) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'project_detail_new_f') ? (this.project_detail_new_f()) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'get_workers_f') ? (this.get_workers_f()) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'get_type_works') ? (this.get_type_works()) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'getLoocks') ? (this.getLoocks()) : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'getPrices') ? this.getPrices() : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'getDevices') ? this.getDevices() : ''
			this.$options.sockets.onmessage = (data) => (data.data == 'getReports') ? this.getReports() : ''


      this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')

      if (delimetr[0] == 'update_item') {
        var item = (JSON.parse(data.data.split('update_item:')[1]))
        this.update_item(item)
      }

    }



		}, 1000);
	},
	created: function () {
		const onResize = () => this.wwidth = window.innerWidth; //После определения ширина окна и  мобильного режима, должна примениться рассчитаная длина списка
		onResize();
		window.addEventListener('resize', onResize);
		this.$once('hook:beforeDestroy', () => window.removeEventListener('resize', onResize));
	}
}
</script>
<style type="text/css">
.maxHeight .dropdown-menu{
  max-height: 300px;
  overflow-y: auto;
},
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
  .cardimg .card-body{
    height: 100% !important;
  }
}
@media only screen and (max-width : 992px) { 
  .cardimg .card-body{
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
.cindex{
  width: 10px;
}
/* .cservice{
  
} */
.cdate{
  width: 100px;
}
.ctime{
  width: 100px;
}
.cworkers{
  width: 200px;
}
.cdel{
  width: 10px;
}



.ql-editor{
      font-size: 12px !important;
      min-height: 0px !important;
  }
  .ql-editor ul[data-checked=true] > li::before {
    content: '✓' !important;
  }
  .ql-editor ul[data-checked=false] > li::before {
    content: '☐' !important;
  }
.ccbox label {
  white-space: nowrap;
    display: inline;
    margin-top: -3px;
    width: 15px;
    text-align: left;
}
.ccbox input[type=checkbox] {
    display: none;
}


.ccbox input[type=checkbox]+label:before {
  white-space: nowrap;
  display: inline;
    content: "☐";
    font-size: 14px;
    font-weight: 100;
}
.ccbox input[type=checkbox]:checked+label:before {
  white-space: nowrap;
  display: inline;
    content: "✓";
    font-size: 14px;
    font-weight: 100;
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
.greenrow .form-row {
    background-color: #c8e6c9;
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
.diveditable {
  padding-left:4px;
  padding-right:4px;
  display: inline;
  white-space: nowrap;
}
.diveditable br {
  display: none;
}
.calttax{
  text-decoration: underline;
}
.editTable{
  overflow-x:unset;
  overflow-y:unset;
}
.editTable table thead th {
 text-align: center;
}
.outUnderline .btn-link {
text-decoration: none;
text-transform: none;
}
</style>