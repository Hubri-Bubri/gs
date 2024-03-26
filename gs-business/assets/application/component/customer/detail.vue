<template>
  <container>
      <b-modal size="md" centered  ref="moveImag" :title="$t('projectDetail.move')">
         <b-form-select class="" v-model="selectedItems" :select-size="detectRowSise(itemsMenuImagSub)">
            <option v-for="(item, i) in detectItem(itemsMenuImagSub)" @click="selectedModalImag(item)" :key="i">{{item.name}}</option>
         </b-form-select>
         <template slot="modal-footer">
            <button type="button" class="btn btn-primary" @click="okMoveImg">OK</button> 
         </template>
      </b-modal>
      <b-modal size="md" centered  ref="moveImag2" :title="$t('projectDetail.move')">
         <b-form-select class="" v-model="selectedItems2" :select-size="detectRowSise(itemsMenuImagPerson)">
            <option v-for="(item, i) in detectItem(itemsMenuImagPerson)" @click="selectedModalImagPerson(item)" :key="i">{{item.name}}</option>
         </b-form-select>
         <template slot="modal-footer">
            <button type="button" class="btn btn-primary" @click="okMoveImg2">OK</button> 
         </template>
      </b-modal>
    <b-modal size="md" centered  ref="movedoc" :title="$t('projectDetail.move')">
      <b-form-select class="" v-model="selectedSub" :select-size="detectRowSise(itemsMenuDoc)">
        <option v-for="(item, i) in detectItem(itemsMenuDoc)" @click="selectedModalSub(item)" :key="i">{{item.name}}</option>
      </b-form-select>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveDoc">OK</button> 
      </template>
    </b-modal>
    <b-modal size="md" centered  ref="moveSperson" :title="$t('projectDetail.move')">
      <b-form-select class="" v-model="selectedSperson" :select-size="detectRowSise(itemsMenuSperson)">
        <option v-for="(item, i) in detectItem(itemsMenuSperson)" @click="selectedModalSperson(item)" :key="i">{{item.name}}</option>
      </b-form-select>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okMoveSperson">OK</button> 
      </template>
    </b-modal>
    <b-modal size="md" centered ok-only ref="contact" :title="$t('customerDetail.editContacts')">
      <b-form-group horizontal :label-cols="2" :label="contactEditType+' '+(index+1)"
      v-for="(val, index) in contactEditData" :key="val.id">
        <b-input-group>
          <b-form-input :value="contactEditData[index]"
          @change="contactEditData[index]=$event;updateContact();" type="text" />
          <template #append>
            <b-button  size="sm" >
              <b-icon :icon="(index==0)?'plus-lg':'trash'" aria-hidden="true"  @click="(index==0)?contactEditData.push(''):contactEditData.splice(index, 1);updateContact()" />
            </b-button>
          </template>
        </b-input-group>
      </b-form-group>
    </b-modal>
    <b-modal size="lg" centered ok-only id="map" :title="$t('projectDetail.track')">
      <b-embed type="iframe" aspect="16by9" :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
      'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
      'destination='+city+'+'+street">
      </b-embed>
    </b-modal>
    <b-modal centered id="personModal" ref="personModal" :title="$t('customerDetail.addPerson')"  size="lg" >
      <b-form-group :label="$t('customerDetail.appeal')+':'" label-cols="3">
        <b-select v-model="addAppeal"  :options="['Herr', 'Frau']" />
      </b-form-group>
      <b-form-group v-for="(name, index) in countNamePerson" :key="name.id" label-cols="3">
        <template #label>
         {{$t('customerDetail.name')}}{{(index==0)?'':' '+(index+1)}}:
        </template>
        <b-input-group>
          <b-form-input type='text' :state="(countNamePerson.length>=2 && countNamePerson[0].length>=1 && countNamePerson[1].length>=1)?null:false"
          v-model="countNamePerson[index]" />
          <b-button  v-if="index==0" @click="countNamePerson.push('')"><b-icon icon="plus-lg" aria-hidden="true"></b-icon></b-button>
          <b-button  v-else @click="countNamePerson.splice(index, 1)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-button>
        </b-input-group>
      </b-form-group>
      <b-form-group :label="$t('customerDetail.deportament')+':'" label-cols="3">
        <b-form-input type='text' v-model="addDep" />
      </b-form-group>
      <b-form-group :label="$t('customerDetail.position')+':'" label-cols="3">
        <b-form-input type='text' v-model="addPos" />
      </b-form-group>
      <b-form-group v-for="(mail, index) in countMailPerson" :key="mail.id" label-cols="3">
        <template #label>
          {{$t('customerDetail.mail')}}{{(index==0)?'':' '+(index+1)}}:
        </template>
        <b-input-group>
          <b-form-input type='text' v-model="countMailPerson[index]" />
          <b-button  v-if="index==0" @click="countMailPerson.push('')"><b-icon icon="plus-lg" aria-hidden="true"></b-icon></b-button>
          <b-button v-else @click="countMailPerson.splice(index, 1)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-button>
        </b-input-group>
      </b-form-group>
      <b-form-group v-for="(phone, index) in countPhonePerson" :key="phone.id" label-cols="3">
        <template #label>
          {{$t('customerDetail.phone')}}{{(index==0)?'':' '+(index+1)}}:
        </template>
        <b-input-group>
          <b-form-input type='text' v-model="countPhonePerson[index]" />
          <b-button  v-if="index==0" @click="countPhonePerson.push('')"><b-icon icon="plus-lg" aria-hidden="true"></b-icon></b-button>
          <b-button v-else @click="countPhonePerson.splice(index, 1)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-button>
        </b-input-group>
      </b-form-group>
      <b-form-group v-for="(fax, index) in countFaxPerson" :key="fax.id" label-cols="3">
        <template #label>
          fax{{(index==0)?'':' '+(index+1)}}:
        </template>
        <b-input-group>
          <b-form-input type='text' v-model="countFaxPerson[index]" />
          <b-button  v-if="index==0" @click="countFaxPerson.push('')"><b-icon icon="plus-lg" aria-hidden="true"></b-icon></b-button>
          <b-button v-else @click="countFaxPerson.splice(index, 1)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-button>
        </b-input-group>
      </b-form-group>
      <template slot="modal-footer">
        <b-button @click="newPersonSave" variant="primary">
          OK
        </b-button>
      </template>
    </b-modal>
    <container-header class="container-fluid">
      <top-menu></top-menu>
    </container-header>
    <container-body class="container-fluid">
      <b-card-group deck>
        <b-card no-body class="gs-container" :style="heightComponentforSm">
          <b-tabs card v-model="tabIndex" class="tabs">
            <b-tab>
              <template #title>
                <span v-if="name==undefined">{{$t('customerDetail.customer')}}</span>
                <span v-else :title="$t('customerDetail.customer')+' '+toName(name)">{{toName(name)}}</span>
              </template>
              <container>
                <container-body>
                  <b-container fluid ref="hcus">
                    <b-row>
                      <b-col cols="12"><br></b-col>
                      <b-col md="12" lg="6">
                        <b-form-group :label="$t('customerDetail.name')+':'" label-cols="2" label-size="sm">
                          <b-form-input @change="updateCustomer('name', $event.split(' ').join('_'))" :value="toName(name)" type="text"  placeholder="Enter Name" size="sm"/>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.zip')+':'" label-cols="2" label-size="sm">
                          <b-form-input @change="searchZipCustomer($event);updateCustomer('zip', $event)" :value="zip" type="text" :placeholder="$t('projects.ezip')" size="sm"/>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.city')+':'" label-cols="2" label-size="sm">
                          <b-form-input :value="city" @change="updateCustomer('city', $event)" type="text"  :placeholder="$t('projects.ecity')" size="sm"/>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.street')+':'" label-cols="2" label-size="sm" >
                          <b-input-group>
                            <b-form-input :value="street" @change="updateCustomer('street', $event)" type="text" :placeholder="$t('projects.estreet')" size="sm" />
                            <template #append><b-icon icon="pin-map" aria-hidden="true" v-b-modal.map /></template>
                          </b-input-group>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.date')+':'" label-cols="2" label-size="sm">
                          <b-form-input :value="date" @change="updateCustomer('data', $event);" type="date" placeholder="Enter date" size="sm"/>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.old')+':'" label-cols="2" label-size="sm">
                          <b-form-checkbox type="checkbox" switch @change="(old=old?0:1);updateCustomer('old', old);"  :checked="old=(old==0)?false:true" />
                        </b-form-group>
                      </b-col>
                      <b-col md="12" lg="6">
                        <b-form-group label="BIC:" label-cols="2" label-size="sm">
                           <b-form-input :value="bic" @change="updateCustomer('bic', $event)" type="text"  placeholder="Enter BIC number"  size="sm"/>
                        </b-form-group>
                        <b-form-group label="IBAN:" label-cols="2" label-size="sm">
                           <b-form-input  :value="iban" @change="updateCustomer('iban', $event)" type="text"  placeholder="Enter IBAN"  size="sm"/>
                        </b-form-group>
                        <b-form-group :label="$t('edit.tax')+':'" label-cols="2" label-size="sm">
                           <b-form-input :value="tax" @change="updateCustomer('tax', $event)" :state="null" type="text"  placeholder="Enter TAX" size="sm"/>
                        </b-form-group>
                        <b-form-group label="Web:" label-cols="2" label-size="sm">
                          <b-form-input :value="web" @change="updateCustomer('web', $event)" type="text"  placeholder="Enter Web" size="sm"/>
                        </b-form-group>
                         <b-form-group label="Mail:" label-cols="2" label-size="sm">
                          <b-input-group>
                            <b-form-select v-model="mail[0]" :options="mail" type="text" size="sm"/>
                            <template #append><b-icon icon="pencil-square" aria-hidden="true" @click.pervert="contactEdit('mail', mail)" class="m-1" /></template>
                          </b-input-group>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.phone')+':'" label-cols="2" label-size="sm">
                          <b-input-group>
                            <b-form-select v-model="phone[0]" :options="phone" type="text" size="sm"/>
                            <template #append><b-icon icon="pencil-square" aria-hidden="true" @click.pervert="contactEdit('phone', phone)" class="m-1"/></template>
                          </b-input-group>
                        </b-form-group>
                      </b-col>
                    </b-row>
                    <b-row align-h="between" align-v="end">
                      <b-col cols="12" md="6" lg="4">
                        <b-button @click="newPerson('')" size="sm">
                          {{$t('customerDetail.addPerson')}}
                        </b-button>
                      </b-col>
                      <b-col cols="12" md="6" lg="4">
                        <b-form-checkbox-group
                        class="text-sm-left text-md-left text-lg-right "
                        switches :options="[[$t('fields.showOld')]]"
                        @change="itemsFilter((show!='Show')?1:0);show=(show!='Show')?'Show':'Hide'" />
                      </b-col>
                    </b-row>
                    <b-table @row-clicked="inItemClick" hover :items="items" :fields="fields" stacked="lg">
                      <template #cell(in)="data">
                        <div class="text-center w-100">
                          {{ data.index + 1 }}
                        </div>
                      </template>
                      <template #cell(delete)="item">
                        <b-col class="text-right">
                          <b-button @click.pervert="personDel(item.item.person)" size="sm">
                            <b-icon icon="trash" aria-hidden="true"></b-icon>
                          </b-button>
                        </b-col>
                      </template>
                    </b-table>
                  </b-container>
                </container-body>
              </container>
            </b-tab>
            <b-tab :title="$t('projectDetail.docs')">
              <container>
                <container-body  style="overflow-x: hidden;">
                  <docs
                  v-if="detect('docs')"
                  ref="fileSub"
                  :responseFiles="responseFilesSub"
                  :fieldsDocs="fieldsDocs"
                  :t="2"
                  :idNodeDoc="idNodeFileSub"
                  :docsIds="docs_menu_ids"
                  :itemsMenuDoc="itemsMenuDoc"
                  :oldIdDoc="oldIdDoc"
                  :selectedPriceDoc="selectedPriceDoc"
                  :menuDocsTree="menuDocsTree"
                  @filedel="filedelSub"
                  @updatefilename="updatefilenameSub"
                  @loadDocToFrame="ploadDocToFrameSub"
                  @onClickOutsideDoc="menuDocsTree=false"
                  @curNodeClickedDoc="pcurNodeClickedDoc"
                  @rowSelectedDoc="prowSelectedDoc"
                  />
                  <!-- @changeDisable="changeDisable" -->
                </container-body>
                <container-footer style="z-index:2">
                  <b-collapse v-model="dropDoc" id="dropDoc3">
                    <vue-dropzone ref="myVueDropzone1" id="dz3" :options="dropzoneFilesSub" v-on:vdropzone-sending="sendingEventSub"
                    v-on:vdropzone-success="fsadd1" :forceFallback="true">
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
            <b-tab :title="$t('projectDetail.images')">
              <container>
                <container-body  style="overflow: hidden;">
                  <images
                  v-if="detect('images')"
                  :domageImages="responseImageSub"
                  ref="images1"
                  :wwidth="wwidth"
                  :idNodeImg="idNodeImg"
                  :itemsMenuImag="itemsMenuImagSub"
                  :selectedPriceImg="selectedPriceImg"
                  @imageInTableSelected="prowSelectedImg"
                  @pcurNodeClickedImg="pcurNodeClickedImg"
                  @filedel="filedelSub"
                  @showx="showxSub"
                  @loded="loded"
                  />
                </container-body>
                <container-footer style="z-index:2">
                                <b-collapse v-model="dropImage" id="dropImage2">
                                <vue-dropzone ref="myVueDropzone2" id="dz2"
                                :options="dropzoneImagesSub" v-on:vdropzone-sending="sendingEventSubImage"
                                v-on:vdropzone-success="fsadd2" :forceFallback="true" />
                              </b-collapse>
                              <b-input-group>
                                <template #prepend>
                                  <b-button @click="dropImage=dropImage?false:true">
                                    <b-icon :icon="dropImage?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                                  </b-button>
                                  <b-button @click="addImag">{{$t('projectDetail.plusPart')}}</b-button>
                                  <b-button @click="removeImag" :disabled="(nameNodeImag=='General Folder')?true:false">{{$t('projectDetail.remove')}}</b-button>
                                  <b-button @click="moveImag">{{$t('projectDetail.move')}}</b-button>
                                </template>
                                <b-form-input  v-model="nameNodeImag" :style="nodeDisImag?'background-color:grey':''"
                                :disabled="(nameNodeImag=='General Folder')?true:false"
                                @click.native="nodeDisImag?nodeDisTurnImag():''" @change="nodeDisImag=true;toModelImag(nameNodeImag)" />
                              </b-input-group>
                </container-footer>
              </container>
            </b-tab>
          </b-tabs>
        </b-card>
        <b-card no-body class="gs-container" v-if="firstSelected">
          <b-tabs card v-model="dubTabIndex">
            <b-tab :title="$t('customerDetail.person')">
              <container>
                <container-body>
                  <b-container>
                    <b-row v-if="tmp.person">
                      <b-col cols="12"><br></b-col>
                      <b-col lg="4" md="12">
                        <b-form-group  :label="$t('customerDetail.date')+':'" label-cols="2" label-size="sm">
                            <b-form-input :value="tmp.data" @change="updatePerson(tmp.person, $event, 'data');" type="date"  size="sm" />
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.old')+':'" label-cols="2" label-size="sm">
                            <b-form-checkbox switch @change="(tmp.old=tmp.old?0:1);updatePerson(tmp.person, tmp.old, 'old');"
                            :checked="tmp.old=(tmp.old==0)?false:true" />
                        </b-form-group>
                      </b-col>
                      <b-col md="12" lg="8">
                        <b-form-group :label="$t('customerDetail.fullName')+':'"  label-cols="2" label-size="sm">
                          <b-input-group>
                            <template #prepend>
                              <b-form-select class="select" v-model="tmp.appeal" :options="['Herr', 'Frau']"
                              @change="updatePerson(tmp.person,  $event, 'appeal')" size="sm" />
                            </template>
                            <b-form-input  @change="updatePerson(tmp.person, $event, 'names')" :value="tmp.names" type="text" size="sm"/>
                          </b-input-group>
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.position')+':'" label-cols="2" label-size="sm">
                          <b-form-input  @change="updatePerson(tmp.person, $event, 'pos')" :value="tmp.pos" type="text"  placeholder="Enter Position" size="sm" />
                        </b-form-group>
                        <b-form-group :label="$t('customerDetail.deportament')+':'" label-cols="2" label-size="sm">
                          <b-form-input  @change="updatePerson(tmp.person, $event, 'dep')" :value="tmp.dep"  type="text"  placeholder="Enter Department" size="sm" />
                        </b-form-group>
                      </b-col>
                      <b-col cols="12">
                        <br>
                      </b-col>
                      <b-col lg="4" md="12">
                        <b-form-group label-cols="2" label-size="sm" v-for="(m, index) in tmp.mail" :key="m.id">
                          <template #label>
                           {{$t('customerDetail.mail')}} {{(index+1)}}:
                          </template>
                          <b-input-group>
                            <b-form-input v-model="m.mail" @change="editContactInPerson('mail', tmp.mail)" type="text" placeholder="Enter mail" size="sm"/>
                            <template #append>
                                <b-icon :icon="(index==0)?'plus-lg':'trash'" aria-hidden="true"
                                @click.pervert="(index==0)?addContactInPerson('mail', '+', index):addContactInPerson('mail', '-', index)" />
                            </template>
                          </b-input-group>
                        </b-form-group>                                    
                      </b-col>
                      <b-col lg="4" md="12">
                        <b-form-group label-cols="2" label-size="sm" v-for="(p, index) in tmp.phone" :key="p.id">
                          <template #label>
                            {{$t('customerDetail.phone')}} {{(index+1)}}:
                          </template>
                          <b-input-group>
                            <b-form-input v-model="p.phone"  @change="editContactInPerson('phone', tmp.phone)" type="text" placeholder="Enter phone" size="sm"/>
                            <template #append>
                              <b-icon :icon="(index==0)?'plus-lg':'trash'" aria-hidden="true"
                              @click.pervert="(index==0)?addContactInPerson('phone', '+', index):addContactInPerson('phone', '-', index)" />
                            </template>
                          </b-input-group>
                        </b-form-group>                                    
                      </b-col>
                      <b-col lg="4" md="12">
                        <b-form-group label-cols="2" label-size="sm" v-for="(f, index) in tmp.fax" :key="f.id">
                          <template #label>
                            Fax {{(index+1)}}:
                          </template>
                          <b-input-group>
                            <b-form-input v-model="f.fax"  @change="editContactInPerson('fax', tmp.fax)" type="text" placeholder="Enter fax"  size="sm"/>
                            <template #append>
                              <b-icon :icon="(index==0)?'plus-lg':'trash'" aria-hidden="true"
                              @click.pervert="(index==0)?addContactInPerson('fax', '+', index):addContactInPerson('fax', '-', index)" />
                            </template>
                          </b-input-group>
                        </b-form-group>                                    
                      </b-col>
                      <b-col cols="12"><br></b-col>
                      <b-col lg="12">
                        <b-form-group label-cols="2" label-size="sm" v-for="(a, index) in tmp.adress" :key="a.id">
                          <template #label>
                            {{$t('customerDetail.adress')}} {{(index+1)}}:
                          </template>
                          <b-input-group>
                            <b-form-input :value="a.adress.split(';')[0]"
                            @input="a.adress=$event+';'+a.adress.split(';')[1]+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')"
                            @change="editContactInPerson('adress', tmp.adress)"
                            type="text" placeholder="Adress line 1" size="sm" />
                            <b-form-input :value="a.adress.split(';')[1]"
                            @input="a.adress=a.adress.split(';')[0]+';'+$event+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')"
                            @change="editContactInPerson('adress', tmp.adress)"
                            type="text" placeholder="Adress line 2" size="sm" />
                            <b-form-input :value="a.adress.split(';')[2]"
                            @input="a.adress=a.adress.split(';')[0]+';'+a.adress.split(';')[1]+';'+$event;a.adress=a.adress.replace(undefined, '')"
                            @change="editContactInPerson('adress', tmp.adress)"
                            type="text" placeholder="Adress line 3" size="sm" />
                            <template #append>
                              <b-icon :icon="(index==0)?'plus-lg':'trash'"
                              aria-hidden="true" @click.pervert="(index==0)?addContactInPerson('adress', '+', index):addContactInPerson('adress', '-', (index))" />
                            </template>
                          </b-input-group>
                        </b-form-group>                                    
                      </b-col>
                    </b-row>
                  </b-container>
                </container-body>
              </container>
            </b-tab>
            <b-tab :title="$t('projectDetail.docs')">
              <container>
                <container-body  style="overflow-x: hidden;">
                  <docs
                  ref="fileSperson"
                  :responseFiles="responseFilesSperson"
                  :fieldsDocs="fieldsDocs"
                  :t="3"
                  :idNodeDoc="idNodeFileSperson"
                  :docsIds="docs_menu_sperson_ids"
                  :itemsMenuDoc="itemsMenuSperson"
                  :oldIdDoc="oldIdSperson"
                  :selectedPriceDoc="selectedPriceDocSperson"
                  :menuDocsTree="menuDocsSpersonTree"
                  @filedel="filedelSperson"
                  @updatefilename="updatefilenameSperson"
                  @loadDocToFrame="ploadDocToFrameSperson"
                  @onClickOutsideDoc="menuDocsSpersonTree=false"
                  @curNodeClickedDoc="pcurNodeClickedSperson"
                  @rowSelectedDoc="prowSelectedSperson"
                  />
                  <!-- @changeDisable="changeDisable" -->
                </container-body>
                <container-footer style="z-index:2">
                  <b-collapse v-model="dropSperson" id="dropDoc3">
                    <vue-dropzone ref="myVueDropzone3" id="dz3" :options="dropzoneSperson" v-on:vdropzone-sending="sendingEventSperson"
                    v-on:vdropzone-success="fsadd3" :forceFallback="true">
                    </vue-dropzone>
                  </b-collapse>
                  <b-input-group>
                  <template #prepend>
                    <b-button @click="dropSperson=dropSperson?false:true">
                      <b-icon :icon="dropSperson?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                    </b-button>
                    <b-button @click="addSperson">{{$t('projectDetail.plusPart')}}</b-button>
                    <b-button @click="removeSperson" :disabled="(nameNodePerson=='General Folder')?true:false">{{$t('projectDetail.remove')}}</b-button>
                    <b-button @click="moveSperson">{{$t('projectDetail.move')}}</b-button>
                  </template>
                  <b-form-input v-model="nameNodePerson" :style="nodeDisPerson?'background-color:grey':''" :disabled="(nameNodePerson=='General Folder')?true:false"
                  @click.native="nodeDisPerson?nodeDisTurnPerson():''" @change="nodeDisPerson=true;toModelPerson(nameNodePerson)"></b-form-input>
                  </b-input-group>
                </container-footer>
              </container>
            </b-tab>
            <b-tab :title="$t('projectDetail.images')">
              <container>
                <container-body  style="overflow: hidden;" >
                  <images
                  v-if="detect('images2')"
                  :domageImages="responseImagesSperson"
                  ref="images2"
                  :wwidth="wwidth"
                  :idNodeImg="idNodeImgPerson"
                  :itemsMenuImag="itemsMenuImagPerson"
                  :selectedPriceImg="selectedPriceImg2"
                  @imageInTableSelected="prowSelectedImg2"
                  @pcurNodeClickedImg="pcurNodeClickedImg2"
                  @filedel="filedelSperson"
                  @showx="showxSperson"
                  @loded="loded"
                  />
                </container-body>
               <container-footer style="z-index:2">
                    <b-collapse v-model="dropSpersonImage" id="dropImage4">
                      <vue-dropzone ref="myVueDropzone4" id="dz4"
                      :options="dropzoneImagesSperson" v-on:vdropzone-sending="sendingEventSubImagePerson"
                      v-on:vdropzone-success="fsadd4" :forceFallback="true" />
                    </b-collapse>
                    <b-input-group>
                      <template #prepend>
                        <b-button @click="dropSpersonImage=dropSpersonImage?false:true">
                          <b-icon :icon="dropSpersonImage?'folder2-open':'folder2'" aria-hidden="true"></b-icon>
                        </b-button>
                        <b-button @click="addImagPerson">{{$t('projectDetail.plusPart')}}</b-button>
                        <b-button @click="removeImagPerson" :disabled="(nameNodeImagPerson=='General Folder')?true:false">{{$t('projectDetail.remove')}}</b-button>
                        <b-button @click="moveImagPerson">{{$t('projectDetail.move')}}</b-button>
                      </template>
                        <b-form-input  v-model="nameNodeImagPerson" :style="nodeDisImagPerson?'background-color:grey':''"
                        :disabled="(nameNodeImagPerson=='General Folder')?true:false"
                        @click.native="nodeDisImagPerson?nodeDisTurnImagPerson():''" @change="nodeDisImagPerson=true;toModelImagPerson(nameNodeImagPerson)" />
                    </b-input-group>
                </container-footer>
              </container>
            </b-tab>                         
          </b-tabs>
        </b-card>
      </b-card-group>
    </container-body>
  </container>
</template>
<script type="text/javascript">
import axios from 'axios';
import vue2Dropzone from 'vue2-dropzone'
import 'vue2-dropzone/dist/vue2Dropzone.min.css'
export default {
  components: {
    vueDropzone: vue2Dropzone
  },
  props: {
    id: String
  },
  data() {
    return {
      heightComponentforSm:'min-height:934px',
      dubTabIndex:null,
      idNodeImgPerson:-1,
      responseImagesSperson:[],
      selectedPriceImg2:[],
      oldIdNodeImgPerson:0,
      itemsMenuImagPerson:[],
      images_person_menu_ids:[],
      selectedItems2:[],
      nameNodeImagPerson:null,
      nodeDisImagPerson:true,
      tabIndex: null,
      idNodeImg:-1,
      itemsMenuImagSub:[],
      selectedPriceImg:[],
      wwidth:null,
      nodeDisImag:true,
      nameNodeImag:null,
      images_sub_menu_ids:[],
      selectedItems:[],
      oldIdImg:0,
      firstSelected:false,
      idNodeFileSub:-1,
      docs_menu_ids:[],
      itemsMenuDoc:[],
      oldIdDoc:0,
      selectedPriceDoc:[],
      menuDocsTree: false,
      nameNodeDoc:null,
      nodeDisDoc:true,
      idNodeFileSperson:-1,
      docs_menu_sperson_ids:[],
      itemsMenuSperson:[],
      oldIdSperson:0,
      selectedPriceDocSperson:[],
      menuDocsSpersonTree: false,
      nameNodePerson:null,
      nodeDisPerson:true,
      selectedSub:[],
      selectedSperson:[],
      dropImage:true,
      dropDoc:true,
      dropSperson:true,
      dropSpersonImage:true,
      responseImageSub:[],
      dropzoneFilesSub: {
        url: '/loadFilesToCustomer',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'application/pdf'
      },
      dropzoneImagesSub: {
        url: '/loadFilesToCustomer',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'image/*'
      },
      dropzoneSperson: {
        url: '/loadFilesToPerson',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'application/pdf'
      },
      dropzoneImagesSperson: {
        url: '/loadFilesToPerson',
        thumbnailWidth: 50,
        parallelUploads: 20,
        dictDefaultMessage: this.$t('alert.clickOrDrop'),
        acceptedFiles: 'image/*'
      },
      responseFilesSub: [],
      responseFilesSperson: [],
      show:"Show",
      contactEditType: null,
      contactEditData: [],
      countNamePerson: [''],
      countMailPerson: [''],
      countPhonePerson: [''],
      countFaxPerson: [''],
      countOtherPerson:null,
      addFirm:null,
      addAppeal:'Herr',
      addDep:'General',
      addPos:'Office Manager',
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
      bic: null,
      city: null,
      date: null,
      iban: null,
      numberId: null,
      name: null,
      old: null,
      other: null,
      status: null,
      street: null,
      tax: null,
      web: null,
      mail: [],
      phone: [],
      fax: [],
      zip: null,
      items:[],
      items1:[]
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
    fields() {
      return [{
        key: 'appeal',
        label: this.$t('customerDetail.appeal'),
        sortable: true
      },
      {
        key: 'names',
        label: this.$t('customerDetail.name'),
        sortable: true
      },
      {
        key: 'data',
        label: this.$t('fields.registred'),
        sortable: true
      },
      {
        key: 'pos',
        label: this.$t('customerDetail.position'),
        sortable: true
      },
      {
        key: 'dep',
        label: this.$t('customerDetail.deportament'),
        sortable: true
      },
      {
        key: 'delete',
        label: this.$t('docs.delete')
 
      }]
    }
  },
  methods: {
    toModelImag(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/update_name_images_customer_menu', {
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
        findLevel(this.itemsMenuImagSub, this.idNodeImg)
    },
    toModelImagPerson(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/update_name_images_sperson_menu', {
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
        findLevel(this.itemsMenuImagPerson, this.idNodeImgPerson)
    },
    nodeDisTurnImag(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDisImag = false
            }
       },
    nodeDisTurnImagPerson(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDisImagPerson = false
            }
       },
    selectedModalImagPerson(val){
        var files_ids=[]
            this.selectedPriceImg2.forEach((val)=>{
                  var id = val.id.split('=')
                  files_ids.push(id[1])
            })
             axios.get('/mv_files_person', {
                 params: {
                     files_ids: files_ids.join(),
                     new_menu: val.id
                 }
             }).then(response=>{
                     setTimeout(() => {
                this.getFilesSperson(this.tmp.person);
            }, 20);
        })                      
    },
    selectedModalImag(val){
        var files_ids=[]
            this.selectedPriceImg.forEach((val)=>{
                  var id = val.id.split('=')
                  files_ids.push(id[1])
            })
             axios.get('/mv_files_customer', {
                 params: {
                     files_ids: files_ids.join(),
                     new_menu: val.id
                 }
             }).then(response=>{
                setTimeout(() => {
                   this.getSubFiles();
            }, 20);
        })                      
    },
      okMoveImg(){
        this.selectedPriceImg=[],
        this.$refs.moveImag.hide()
    },
      okMoveImg2(){
        this.selectedPriceImg2=[],
        this.$refs.moveImag2.hide()
    },
          detect(type){
          if (type == 'docs'){
            if ((this.tabIndex==1)){
              return true;
            }
          }
          if (type == 'images'){
            if ((this.tabIndex==2)){
              return true;
            }
          }
          if (type == 'images2'){
            if ((this.dubTabIndex==2)){
              return true;
            }
          }
      },
moveImag(){
  this.$refs.moveImag.show()
},
moveImagPerson(){
  this.$refs.moveImag2.show()
},
      removeImagPerson(){
       if (this.idNodeImgPerson==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_image_sperson_menu', {
                    params: {
                        remove_id: this.idNodeImgPerson
                    }
                }).then(response=>{
                    this.idNodeImgPerson=null,
                    this.nameNodeImagPerson=null
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
                axios.get('/remove_image_customer_menu', {
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
    addImag(){
      var newName = this.$t('projectDetail.plusPart')
      function findLevel(obj, id, project) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_images_customer_menu', {
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
        findLevel(this.itemsMenuImagSub, this.idNodeImg, this.id)
    },
    addImagPerson(){
      var newName = this.$t('projectDetail.plusPart')
      function findLevel(obj, id, project) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_images_sperson_menu', {
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
        findLevel(this.itemsMenuImagPerson, this.idNodeImgPerson, this.tmp.person)
    },
    pcurNodeClickedImg(model, component) {
        this.nameNodeImag=model.name,
        this.idNodeImg=model.id
        if(this.idNodeImg == this.oldIdImg){
            this.$refs.images1.loded()
        }
        this.oldIdImg = this.idNodeImg
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeImg = null
        }
    },
    pcurNodeClickedImg2(model, component) {
        this.nameNodeImagPerson=model.name,
        this.idNodeImgPerson=model.id
        if(this.idNodeImgPerson == this.oldIdNodeImgPerson){
            this.$refs.images2.loded()
        }
        this.oldIdNodeImgPerson = this.idNodeImgPerson
        if ((model.parrent == 0) && component.folder == false){
            this.idNodeImgPerson = null
        }
    },
    loded(dir, elheight, add){
      this.sm2lg(dir, elheight, add)
    },
      sm2lg(dir, val, add){
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
    toName(val){
      if (val!=null){
        return val.split('_').join(' ')
      } else {
        return val
      }
    },
    selectedModalSub(val){
      var docs_ids=[]
      var files_ids=[]
      this.selectedPriceDoc.forEach((val)=>{
          files_ids.push(val.id)
      })
      axios.get('/mv_files_customer', {
        params: {
          files_ids: files_ids.join(),
          new_menu: val.id
        }
      }).then(response=>{
        setTimeout(() => {
          this.getCustomerDetail()
        }, 20);
      })                      
    },
    selectedModalSperson(val){
      var docs_ids=[]
      var files_ids=[]
      this.selectedPriceDocSperson.forEach((val)=>{
          files_ids.push(val.id)
      })
      axios.get('/mv_files_person', {
        params: {
          files_ids: files_ids.join(),
          new_menu: val.id
        }
      }).then(response=>{
        setTimeout(() => {
           this.getCustomerDetail()
        }, 20);
      })                      
    },   
    pcurNodeClickedDoc(model, component) {
      this.nameNodeDoc = model.name
      this.idNodeFileSub=model.id
      this.oldIdDoc = this.idNodeFileSub 
        if ((model.parrent == 0) && component.folder == false){
          this.idNodeFileSub = null
        }
    },
    pcurNodeClickedSperson(model, component) {
      this.nameNodePerson = model.name
      this.idNodeFileSperson=model.id
      this.oldIdSperson = this.idNodeFileSperson
        if ((model.parrent == 0) && component.folder == false){
          this.idNodeFileSperson = null
        }
    },
    removeDoc(){
      if (this.idNodeFileSub==null){
        alert(this.$t('alert.noItemSelectForDel'))
      }
      else {
        if (confirm(this.$t('alert.remove'))) {
          axios.get('/remove_docs_customer_menu', {
            params: {
              remove_id: this.idNodeFileSub
            }
          }).then(response=>{
            this.idNodeFileSub=null,
            this.nameNodeDoc=null
          })
        }
      } 
    },
    removeSperson(){
      if (this.idNodeFileSperson==null){
        alert(this.$t('alert.noItemSelectForDel'))
      }
      else {
        if (confirm(this.$t('alert.remove'))) {
          axios.get('/remove_docs_person_menu', {
            params: {
              remove_id: this.idNodeFileSperson
            }
          }).then(response=>{
            this.idNodeFileSperson=null,
            this.nameNodePerson=null
          })
        }
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
            axios.get('/add_docs_customer_menu', {
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
      findLevel(this.itemsMenuDoc, this.idNodeFileSub, this.id)
    },
    addSperson(){
      function findLevel(obj, id, project) {
        if (id==null){
          id=0,
          obj.push({id:0, children:[]})
        }
        obj.forEach((val)=>{
          if (val.id==id){
            axios.get('/add_person_menu', {
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
      findLevel(this.itemsMenuSperson, this.idNodeFileSperson, this.tmp.person)
    },
    toModelDoc(enterVal){
      function findLevel(obj, id) {
        obj.forEach((val)=>{
          if (val.id==id){
            axios.get('/update_name_docs_customer_menu', {
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
      findLevel(this.itemsMenuDoc, this.idNodeFileSub)
    },
    toModelPerson(enterVal){
      function findLevel(obj, id) {
        obj.forEach((val)=>{
          if (val.id==id){
            axios.get('/update_name_person_menu', {
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
      findLevel(this.itemsMenuSperson, this.idNodeFileSperson)
    },
    filedelSub(val) {
      if (confirm(this.$t('alert.sure'))) {
        axios.get('/delfile_customer', {
          params: {
            id: val
          }
        }).then(response => {});
      }
    },
    filedelSperson(val) {
      if (confirm(this.$t('alert.sure'))) {
        axios.get('/delfile_person', {
          params: {
            id: val
          }
        }).then(response => {});
      }
    },
    updatefilenameSub(val, type, id){
      axios.get('/updatefilename_customer', {
        params: {
          val: val,
          type: type,
          id: id
        }
      })
    },
    updatefilenameSperson(val, type, id){
      axios.get('/updatefilename_person', {
        params: {
          val: val,
          type: type,
          id: id
        }
      })
    },
    // changeDisable(type_operation, fild, id){
    //   this.stopDis=(type_operation=='f')
    //   axios.get('/changeDisableTable', {
    //     params: {
    //       type_operation: type_operation,
    //       fild: fild,
    //       id: id,
    //       'user': this.$security.account['first_name']+'_'+this.$security.account['second_name']
    //     }
    //   })
    //   if (type_operation == 'f'){
    //     setTimeout(()=>{}, 15000);
    //   }
    // },
    getFilesFirma(id){
      axios.get('/get_files_customer', {
        params: {
          id: id
        }
      }).then(response => {
        this.responseFilesSub = response.data.filter(function (v){
          if(v.name != undefined){
            if((v.name.split('.')[v.name.split('.').length-1]) == 'pdf'){ return v}
          }
        })
        this.responseImageSub = response.data.filter(function (v){
          if(v.file_name != undefined){
              return v
          }
        })
      })
    },
    getFilesSperson(id){
      axios.get('/docs_person_menu', {
        params: {
          project:id
        }
      }).then(response => {
        this.itemsMenuSperson=[];
        this.itemsMenuSperson.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
        this.docs_menu_sperson_ids.push(-1);
        response.data.forEach((val)=>{
          if (val.parrent==0){
            val['children']=[]
            this.itemsMenuSperson.push(val);
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
          this.docs_menu_sperson_ids.push(valResp.id);
          findLevel(this.itemsMenuSperson, valResp.parrent) 
        });
        this.responseFilesSperson=[];
        axios.get('/get_files_preson', {
          params: {
            id: id
          }
        }).then(response => {
          this.responseFilesSperson = response.data.filter(function (v){
            if(v.name != undefined){
              if((v.name.split('.')[v.name.split('.').length-1]) == 'pdf'){ return v}
            }
          })
          this.responseImagesSperson = response.data.filter(function (v){
            if(v.file_name != undefined){
                return v
            }
          })
        })
      axios.get('/images_customer_person_menu', {
                params: {
                    project:id
                }
            }).then(response => {
            this.itemsMenuImagPerson=[];
            this.itemsMenuImagPerson.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
            this.images_person_menu_ids.push(-1);
               response.data.forEach((val)=>{
                        if (val.parrent==0){
                            val['children']=[]
                            this.itemsMenuImagPerson.push(val);
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
                this.images_person_menu_ids.push(valResp.id)
                findLevel(this.itemsMenuImagPerson, valResp.parrent)  
               })
            })

      })
    },
    addContactInPerson(fild, action, index){
      if (action=='+'){
        this.tmp[fild].push({[fild]:''})
      } else {
        axios.get('/contact_in_person_remove_row', {
          params: {
            fild: fild,
            id: this.tmp.person,
            value: this.tmp[fild][index][fild],
            type: 'person'
          }
        }).then(response =>{
          this.tmp[fild].splice(index, 1)
        })
      }
    },
    editContactInPerson(fild, value){
      var sendArr=[]
      value.forEach((v)=>{
        sendArr.push(v[fild])
      })

      console.log(fild, sendArr, this.tmp.person)
      axios.get('/edit_contact_person', {
        params: {
          fild: fild,
          value: sendArr.join(),
          id: this.tmp.person,
          type: 'person'
        }
      })
    },
    personDel(val){
      if (confirm(this.$t('alert.sure'))) {
        axios.get('/del_person', {
          params: {
            id: val
          }
        })
      };
    },
    updatePerson(id, data, fild){
      axios.get('/updatePerson', {
        params: {
          fild: fild,
          data: data,
          id: id
        }
      })
    },
    updateContact(){
      axios.get('/updateContact', {params: {
        id: this.id,
        date: this.contactEditData.join(),
        type: this.contactEditType
      }})
    },
    getContact(id) {
      axios.get('/get_contact_person', {params: {
        id: id
      }}).then(response=>{
        this.tmp.mail =  (response.data.mail[0]==undefined)?[{mail:''}]:response.data.mail
        this.tmp.phone =  (response.data.phone[0]==undefined)?[{phone:''}]:response.data.phone
        this.tmp.fax =  (response.data.fax[0]==undefined)?[{fax:''}]:response.data.fax
        this.tmp.adress = (response.data.adress[0]==undefined)?[{adress:';;'}]:response.data.adress
        this.tmp.adress.forEach(function (val){
          val.adress =val.adress.replace(/,/g, ';')
        })
      })
    },
    inItemClick(item, index) {
      axios.get('/get_contact_person', {params: {
        id: item.person
      }}).then(response=>{
        this.tmp.mail =  (response.data.mail[0]==undefined)?[{mail:''}]:response.data.mail
        this.tmp.phone =  (response.data.phone[0]==undefined)?[{phone:''}]:response.data.phone
        this.tmp.fax =  (response.data.fax[0]==undefined)?[{fax:''}]:response.data.fax
        this.tmp.adress = (response.data.adress[0]==undefined)?[{adress:';;'}]:response.data.adress
        this.tmp.adress.forEach(function (val){
          val.adress =val.adress.replace(/,/g, ';')
        })
        this.tmp.appeal = item.appeal
        this.tmp.customer_group = item.customer_group
        this.tmp.data = item.data
        this.tmp.dep = item.dep
        this.tmp.names = item.names
        this.tmp.old = item.old
        this.tmp.other = item.other
        this.tmp.person = item.person
        this.tmp.pos = item.pos
        this.getFilesSperson(item.person)
        this.firstSelected=true
      })
    },    
    updateCustomer(fild, newData){
      axios.get('/updateCustomer', {params: {
        id: this.id,
        date: newData,
        fild: fild
      }})
    },
    newPersonSave(){
      this.updatePojectFunc=0
      if (this.countNamePerson[0].length>=1 && this.countNamePerson[1].length>=1){
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
            firm: this.id,
            appeal: this.addAppeal,
            dep: this.addDep,
            pos: this.addPos
          }
        })
      }
    },
    getSubFiles(){
    axios.get('/docs_customer_menu', {
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
      this.responseFilesSub=[];
      this.getFilesFirma(this.id)
              axios.get('/images_customer_menu', {
                params: {
                    project:this.id
                }
            }).then(response => {
            this.itemsMenuImagSub=[];
            this.itemsMenuImagSub.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
            this.images_sub_menu_ids.push(-1);
               response.data.forEach((val)=>{
                        if (val.parrent==0){
                            val['children']=[]
                            this.itemsMenuImagSub.push(val);
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
                this.images_sub_menu_ids.push(valResp.id)
                findLevel(this.itemsMenuImagSub, valResp.parrent)  
               })

            })
    })
  },
  getPersons(){
    axios.get('/get_persons', {
      params: {
        id: this.id
      }
    }).then(response => {
      this.items = response.data
      this.items1= response.data
      this.itemsFilter((this.show!='Show')?0:1)
    })

    setTimeout(() => {
      console.log('after')
        this.sm2lg('component', this.$refs['hcus'].clientHeight, 110)
        // this.sm2lg('edit', this.$refs.editList.$refs.editcomponet.clientHeight, 56)
    }, 100);
  },
  getCustomerDetail(){
    axios.get('/customer_detail', {
      params: {
        id: this.id
      }
    }).then(response => {
      this.bic = response.data.bic,
      this.city = response.data.city,
      this.date = response.data.data,
      this.iban = response.data.iban,
      this.numberId = response.data.id,
      this.name = response.data.name,
      this.old = response.data.old,
      this.other = response.data.other,
      this.status = response.data.status,
      this.street = response.data.street,
      this.tax = response.data.tax,
      this.web = response.data.web,
      this.zip = response.data.zip
      // this.getSubFiles()
      this.getPersons()
      axios.get('/get_contactData', {
        params: {
          customer: this.id,
          fild: 'mail'
        }
      }).then(response => {
        this.mail=[],
        response.data.forEach((val)=>{
          this.mail.push(val.mail)
        })
      }),
      axios.get('/get_contactData', {
        params: {
          customer: this.id,
          fild: 'phone'
        }
      }).then(response => {
        this.phone=[],
        response.data.forEach((val)=>{
          this.phone.push(val.phone)
        })
      }),
      axios.get('/get_contactData', {
        params: {
          customer: this.id,
          fild: 'fax'
        }
      }).then(response => {
        this.fax=[],
        response.data.forEach((val)=>{
          this.fax.push(val.fax)
        })
      })
      })
    },
        prowSelectedImg2(items) {
          if(this.selectedPriceImg2.indexOf(items)==-1){
              this.selectedPriceImg2 = this.selectedPriceImg2.filter((v)=>{
                  if (v.id != items.id){
                      return v
                  }
              });
              this.selectedPriceImg2.push(items);
              items._rowVariant='success';
           } else{
              this.selectedPriceImg2.splice(this.selectedPriceImg2.indexOf(items), 1)
              items._rowVariant=''
           }
        },
        prowSelectedImg(items) {
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
          this.city = city
        }
      })
    },
    okMoveDoc(){
      this.selectedPriceDoc=[],
      this.$refs.movedoc.hide()
    },
    okMoveSperson(){
      this.selectedPriceDocSperson=[],
      this.$refs.moveSperson.hide()
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
    prowSelectedSperson(items) {
      if(this.selectedPriceDocSperson.indexOf(items)==-1){
        this.selectedPriceDocSperson = this.selectedPriceDocSperson.filter((v)=>{
          if (v.id != items.id){
            return v
          }
        });
        this.selectedPriceDocSperson.push(items);
        items._rowVariant='success';
      } else {
        this.selectedPriceDocSperson.splice(this.selectedPriceDocSperson.indexOf(items), 1)
        items._rowVariant=''
      }
    },
    nodeDisTurnDoc(){
      if (confirm(this.$t('alert.rename'))) {
        this.nodeDisDoc = false
      }
    },
    nodeDisTurnPerson(){
      if (confirm(this.$t('alert.rename'))) {
        this.nodeDisPerson = false
      }
    },
    moveDoc(){
      this.$refs.movedoc.show()
    },
    moveSperson(){
      this.$refs.moveSperson.show()
    },
    showxSub(classId, index){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.index = index
      viewer.show()
    },      
    showxSperson(classId, index){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.index = index
      viewer.show()
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
    ploadDocToFrameSub(row) {
      row.toggleDetails();
      var index = row.index;
      if (row.detailsShowing == false) {
        setTimeout(() => {
          this.$refs.fileSub?this.$refs.fileSub.$refs['ifrForm' + index].submit():''
        }, 50);
      }
    },
    ploadDocToFrameSperson(row) {
      row.toggleDetails();
      var index = row.index;
      if (row.detailsShowing == false) {
        setTimeout(() => {
          this.$refs.fileSperson?this.$refs.fileSperson.$refs['ifrForm' + index].submit():''
        }, 50);
      }
    },
    sendingEventSub(file, xhr, formData) {
      xhr.setRequestHeader('X-Number', this.id);
      xhr.setRequestHeader('X-Folder', this.idNodeFileSub);
      xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
    },
    sendingEventSubImage(file, xhr, formData) {
      xhr.setRequestHeader('X-Number', this.id);
      xhr.setRequestHeader('X-Folder', this.idNodeImg);
      xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
    },
    sendingEventSperson(file, xhr, formData) {
      xhr.setRequestHeader('X-Number', this.tmp.person);
      xhr.setRequestHeader('X-Folder', this.idNodeFileSperson);
      xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
    },
    sendingEventSubImagePerson(file, xhr, formData) {
      xhr.setRequestHeader('X-Number', this.tmp.person);
      xhr.setRequestHeader('X-Folder', this.idNodeImgPerson);
      xhr.setRequestHeader('X-User',  this.$security.account['first_name']+'_'+this.$security.account['second_name']);
    },
    itemsFilter(val){
      if(val==1){
        var arr = this.items.filter(function(val){
          if (val.old==false){
            return val
          }
        })
        this.items=arr
      } else {
        this.items=this.items1
      }
    },
    contactEdit(type, val){
      this.contactEditType = this[type]?type:['']
      if (val.length==0){
        val.push('')  
      }
      this.contactEditData = val
      this.$refs.contact.show()
    },
    newPerson(val){
      this.countNamePerson=val.split(' '),
      this.countMailPerson=[''],
      this.countPhonePerson=[''],
      this.countFaxPerson=[''],
      this.countOtherPerson='',
      this.addFirm=this.customer,
      this.addAppeal='Herr',
      this.addDep='General',
      this.addPos='Office Manager'
      this.$refs.personModal.show()
    },
  },
  watch:{
    tabIndex: function(newv, oldv){
      if (oldv!=null){
        if (newv==0){
          setTimeout(() => {
              this.sm2lg('component', this.$refs['hcus'].clientHeight, 110)
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
    items (val) {
      val.forEach((v)=>{
        if (v.person==this.tmp.person){
          this.tmp.appeal=(v.appeal!=this.tmp.appeal)?v.appeal:this.tmp.appeal,
          this.tmp.dep=(v.dep!=this.tmp.dep)?v.dep:this.tmp.dep,
          this.tmp.names=(v.names!=this.tmp.names)?v.names:this.tmp.names,
          this.tmp.old=(this.tmp.old==false || this.tmp.old==0)?0:1,
          v.old=(v.old==false || v.old==0)?0:1,
          this.tmp.old=(v.old!=this.tmp.old)?v.old:this.tmp.old,
          this.tmp.other=(v.other!=this.tmp.other)?v.other:this.tmp.other,
          this.tmp.pos=(v.pos!=this.tmp.pos)?v.pos:this.tmp.pos,
          this.tmp.data=(v.data!=this.tmp.data)?v.data:this.tmp.data
        } 
      })
    },
  },
  mounted(){
    this.getCustomerDetail()
      this.getSubFiles()


      this.$options.sockets.onmessage = (data) => (data.data=='getCustomerFiles') ? this.getSubFiles(): ''
      this.$options.sockets.onmessage = (data) => (data.data=='getSubDetail') ? (this.getCustomerDetail()):''
      this.$options.sockets.onmessage = (data) => (data.data=='get_persons') ? (this.getPersons()):''
      this.$options.sockets.onmessage = (data) => (data.data=='getSubContact') ? (this.getContact(this.tmp.person)):''
      this.$options.sockets.onmessage = (data) => (data.data=='getPersonFiles') ? (this.getFilesSperson(this.tmp.person)):''

  }
}
</script>