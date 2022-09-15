<template>
    <container>
        <b-modal size="md" centered ok-only ref="contact" title="Edit Contacts">
            <b-form-group horizontal :label-cols="2" class="cForm" :label="contactEditType+' '+(index+1)"
            v-for="(val, index) in contactEditData"  :key="val.id">
                <b-input-group>
                    <b-form-input :value="contactEditData[index]"
                    @change="contactEditData[index]=$event;updateContact();" type="text" class="cForm-input" />
                    <b-link style="margin-left:10px"
                    @click="(index==0)?contactEditData.push(''):contactEditData.splice(index, 1);updateContact()">
                        {{(index==0)?'+':'-'}}
                    </b-link>
                </b-input-group>
            </b-form-group>
                            
          <!--   :createOption="insertCustomer(fax, 'fax')" -->
        </b-modal>
         <b-modal size="lg" centered ok-only id="map" title="Track">
            <b-embed type="iframe" aspect="16by9" :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+city+'+'+street">
            </b-embed>
        </b-modal>
    <b-modal centered id="personModal" ref="personModal" title="Add Person" body-class="workerHeight">
  <b-row class="my-1">
      <b-col sm="3">
        <label >Appeal: </label>
      </b-col>
      <b-col sm="9" class="cForm">
        <v-select taggable label="name" v-model="addAppeal" :options="['Herr', 'Frau']" />
      </b-col>
  </b-row>
      <b-row v-for="(name, index) in countNamePerson" :key="name.id">
      <b-col sm="3">
        <label >Name{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' :state="(countNamePerson.length>=2 && countNamePerson[0].length>=1 && countNamePerson[1].length>=1)?null:false" class="cForm-input" v-model="countNamePerson[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countNamePerson.push('')">+</b-button>
       <b-button class="cForm-inputG" v-else @click="countNamePerson.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>
<b-row>
      <b-col sm="3">
        <label >Deportament: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <v-select  taggable label="name" v-model="addDep" :options="['1', '2', '3', '4']" />
      </b-col>
        <b-col sm="3">
        <label >Position: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <v-select taggable label="name" v-model="addPos" :options="['1', '2', '3', '4']" />
      </b-col>
  </b-row>
        
         <b-row v-for="(mail, index) in countMailPerson" :key="mail.id">
      <b-col sm="3">
        <label >mail{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countMailPerson[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countMailPerson.push('')">+</b-button>
       <b-button class="cForm-inputG" v-else @click="countMailPerson.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>

      <b-row v-for="(phone, index) in countPhonePerson" :key="phone.id">
      <b-col sm="3">
        <label >phone{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countPhonePerson[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countPhonePerson.push('')">+</b-button>
       <b-button class="cForm-inputG" v-else @click="countPhonePerson.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>

            <b-row v-for="(fax, index) in countFaxPerson" :key="fax.id">
      <b-col sm="3">
        <label >fax{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countFaxPerson[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countFaxPerson.push('')">+</b-button>
       <b-button class="cForm-inputG" v-else @click="countFaxPerson.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>
        
        <b-row>
         <b-col sm="3">
        <label >Other: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <b-form-textarea v-model="countOtherPerson"></b-form-textarea>
      </b-col>
    </b-row>

         <template slot="modal-footer">
                    <b-button @click="newPersonSave" variant="primary">
                        OK
                    </b-button>
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
                        <b-tab title="Customer">
                            <container>
                                <container-body>
                                                                       <b-container>
                                        <b-row>
                                          <b-col md="12" lg="6" class="cuestomRow">
                                           <!--   <b-form-group horizontal :label-cols="4" class="cForm" label="Customer Id">
                                                <b-form-input :value="numberId" class="cForm-input" :state="null" disabled type="text" />
                                                </b-form-group> -->


                                              <b-row>
                                              <b-col sm="4" cols="12" class="cForm">Name:</b-col>
                                              <b-col sm="8" cols="12" ><b-form-input @change="searchZipName($event);updateCustomer('name', $event)" :value="name" :state="null" type="text"  placeholder="Enter Name" class="cForm-input" />
                                              </b-col>
                                              </b-row>




                                              <b-row>
                                              <b-col sm="4" cols="12" class="cForm">Zip:</b-col>
                                              <b-col sm="8" cols="12" ><b-form-input  @change="searchZipCustomer($event);updateCustomer('zip', $event)" :value="zip" :state="null" type="text"  placeholder="Enter zip code" class="cForm-input" />
                                              </b-col>
                                              </b-row>



                                                
                                              <b-row>
                                                <b-col sm="4" cols="12" class="cForm">City:</b-col>
                                                <b-col sm="8" cols="12" ><b-form-input :value="city" @change="updateCustomer('city', $event)" :state="null" type="text"  placeholder="Enter city" class="cForm-input" />
                                                </b-col>
                                              </b-row>

                                                
                                                <b-row>
                                              <b-col sm="4" cols="12" class="cForm">Street:</b-col>
                                               <b-col sm="8" cols="12" ><b-input-group>
                                                        <b-button v-b-modal.map class="cForm-inputG"  size="sm" variant="outline-secondary">
                                                            <i class="fa fa-map-marker" aria-hidden="true"></i>
                                                        </b-button>
                                                        <b-form-input  :value="street"  @change="updateCustomer('street', $event)" :state="null" type="text" placeholder="Enter street" class="cForm-inputBeforG" />
                                                  </b-input-group>
                                              </b-col>
                                              </b-row>

                                              
                                              <b-row>
                                                <b-col sm="4" cols="12" class="cForm">Date:</b-col>
                                                <b-col sm="8" cols="12" ><b-form-input :value="date" @change="updateCustomer('data', $event);"  :state="null" type="date"  placeholder="Enter date" class="cForm-input" />
                                                </b-col>
                                              </b-row>

                                               <b-row>
                                                <b-col sm="4"  cols="9" class="cForm">Old:</b-col>
                                                 <b-col sm="8" cols="3" ><b-form-checkbox type="checkbox" plain class="cForm-inputG"
                                                    @change="(old=old?0:1);updateCustomer('old', old);"  :checked="old=(old==0)?false:true"
                                                   ></b-form-checkbox>
                                                </b-col>
                                              </b-row>

                                            </b-col>
                                            <b-col md="12" lg="6" class="cuestomRow">

                                              <b-row>
                                                <b-col sm="4" cols="12" class="cForm">Web:</b-col>
                                                <b-col sm="8" cols="12" ><b-form-input :value="web" @change="updateCustomer('web', $event)" :state="null" type="text"  placeholder="Enter Web" class="cForm-input" />
                                                </b-col>
                                              </b-row>

                                              <b-form-row>
                                                <b-col md="2" sm="12" cols="12" class="cForm">Mail:</b-col>
                                                <b-col md="2" sm="2" cols="3"><b-link  class="cForm" @click.pervert="contactEdit('mail', mail)">Edit</b-link></b-col>
                                                <b-col md="8" sm="10" cols="9" class="text-right"><b-form-select v-model="mail[0]" :options="mail"  :state="null" type="text" class="customButton" style="width: 97%;" /></b-col>
                                              </b-form-row>

                                              <b-form-row>
                                                <b-col md="2" sm="12" cols="12" class="cForm">Phone:</b-col>
                                                <b-col md="2" sm="2" cols="3"><b-link  class="cForm" @click.pervert="contactEdit('phone', phone)">Edit</b-link></b-col>
                                                <b-col md="8" sm="10" cols="9" class="text-right"><b-form-select  v-model="phone[0]" :options="phone"  :state="null" type="text" class="customButton" style="width: 97%;"/></b-col>
                                              </b-form-row>
                                               
                                                    
                                                   <!--  <b-form-group horizontal :label-cols="4" class="cForm" label="Fax:" >
                                                         <b-row> <b-col cols="9">
                                                     <b-form-select class="select" v-model="fax[0]" :options="fax"  :state="null" type="text"  />
                                                               </b-col>
                                                    <b-col cols="3">
                                                    <b-link @click.pervert="contactEdit('fax', fax)" >Edit</b-link>
                                                </b-col>
                                                   </b-row>
                                                </b-form-group> -->

                                                 <b-row>
                                                <b-col sm="4" cols="12" class="cForm">BIC:</b-col>
                                                 <b-col sm="8" cols="12" ><b-form-input :value="bic" 
                                                    @change="updateCustomer('bic', $event)"  :state="null" type="text"  placeholder="Enter BIC number" class="cForm-input" />
                                                </b-col>
                                              </b-row>

                                              <b-row>
                                                <b-col sm="4" cols="12" class="cForm">IBAN:</b-col>
                                                 <b-col sm="8" cols="12" ><b-form-input  :value="iban"  
                                                    @change="updateCustomer('iban', $event)" :state="null" type="text"  placeholder="Enter IBAN" class="cForm-input" />
                                                </b-col>
                                              </b-row>
                                               
                                               <b-row>
                                                <b-col sm="4" cols="12" class="cForm">TAX:</b-col>
                                                <b-col sm="8" cols="12" ><b-form-input  :value="tax"  
                                                    @change="updateCustomer('tax', $event)" :state="null" type="text"  placeholder="Enter TAX" class="cForm-input" />
                                                </b-col>
                                              </b-row>
                                               
                                             
                                            </b-col>
                                        </b-row>
                                        <b-row align-h="between">
                                          <b-col cols="12" md="6" lg="4">
                                            <b-button @click="newPerson('')"
                                            class="customButton w-100">
                                                Add Person
                                            </b-button>
                                          </b-col>
                                          <b-col cols="12" md="6" lg="4">
                                            <b-button class="customButton w-100"
                                            @click.pervert="itemsFilter((show!='Show')?1:0); show=(show!='Show')?'Show':'Hide'">
                                                {{show}}
                                            </b-button>
                                          </b-col>
                                        </b-row>
                                        <b-table stacked="lg" @row-clicked="inItemClick" hover :items="items" :fields="fields"  class="tableProject" small >
                                          <template slot="in" slot-scope="data">
                                            {{ data.index + 1 }}
                                          </template>
                                         <template slot="delete" slot-scope="item">
                                            <b-col >
                                                <b-link @click.pervert="personDel(item.item.person)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>
                                        </b-table>
                                    </b-container>
                                </container-body>
                            </container>
                        </b-tab>
                          <b-tab title="Files">
                            <container>
                                <container-body>
                                     <b-table :items="files" :fields="fieldsFiles" class="tableProject">
                                        <template slot="show_details" slot-scope="row">
                                            <b-link size="sm" @click.stop="row.toggleDetails" class="butMore">
                                                {{ row.detailsShowing ? '-' : '+'}}
                                            </b-link>
                                        </template>
                                        <template slot="row-details" slot-scope="row">
                                            <iframe type="iframe1" :style="'width:100%;height:'+(30.1*((row.item.pages==0)?0.25:row.item.pages)+1.5)+'cm'" frameborder="0" :name="'ifr'+row.index" class="iframeclass" src="" :onload="loadDocToFrame(row.index)" v-if="row.item.gallery==undefined">
                                            </iframe>
                                            <form :target="'ifr'+row.index" :action="(row.item.html!='file') ? '/pdf1':'/pdf2'" method="post" :ref="'ifrForm'+row.index">
                                                <input type="hidden" name="html" :value="row.item.html" style="display:none" v-if="(row.item.html!='file')" />
                                                <input type="hidden" name="id" :value="row.item.id" v-else />
                                            </form>
                                        </template>
                                    </b-table> 
                                </container-body>
                                <b-container>
                                    <b-collapse id="drop">
                                        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd">
                                        </vue-dropzone>
                                    </b-collapse>
                                    <div style="background-color:#ced4da">
                                        <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal; With:100%" v-b-toggle="'drop'">
                                            <span class="when-closed">+</span>
                                            <span class="when-opened">-</span>
                                        </b-link>
                                    </div>
                                </b-container>
                            </container>
                        </b-tab>
                    </b-tabs>
                </b-card>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Person">
                         <container>
                                <container-body>
                            <b-container>
                                <b-row v-if="tmp.person">
                                      <b-col lg="6" md="12" class="cuestomRow" >


                                            <!--     <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Pos:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                     <b-form-input :value="tmp.person" :state="null" type="text" disabled class="cForm-input" />
                                                  </b-col>
                                                </b-form-row> -->



                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Data:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                     <b-form-input :value="tmp.data" @change="updatePerson(tmp.person, $event, 'data');" :state="null" type="date" class="cForm-input" />
                                                  </b-col>
                                                </b-form-row>

                                                 <b-form-row>
                                                  <b-col sm="4" cols="9" class="cForm">Old:</b-col>
                                                  <b-col sm="8" cols="3" >
                                                      <b-form-checkbox @change="(tmp.old=tmp.old?0:1);updatePerson(tmp.person, tmp.old, 'old');"  :checked="tmp.old=(tmp.old==0)?false:true" plain class="cForm-inputG"></b-form-checkbox>
                                                  </b-col>
                                                </b-form-row>

                                                

                                            </b-col>

                                          <b-col md="12" lg="6" class="cuestomRow">


                                              <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Full Name:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-input-group>   
                                                        <b-input-group-append>
                                                          <b-form-select class="select" style="width:65px;" label="name" v-model="tmp.appeal" :options="['Herr', 'Frau']"
                                                          @change="updatePerson(tmp.person,  $event, 'appeal')"/>
                                                        </b-input-group-append>
                                                        <b-form-input  @change="updatePerson(tmp.person, $event, 'names')"
                                                        :value="tmp.names" :state="null" type="text" class="cForm-input" />
                                                      </b-input-group>
                                                  </b-col>
                                                </b-form-row>

                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Position:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                     <b-form-input  @change="updatePerson(tmp.person, $event, 'pos')"
                                                    :value="tmp.pos" :state="null" type="text"  placeholder="Enter Position" class="cForm-input" />
                                                  </b-col>
                                                </b-form-row>

                                                    
                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Department:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                     <b-form-input  @change="updatePerson(tmp.person, $event, 'dep')"
                                                    :value="tmp.dep" :state="null" type="text"  placeholder="Enter Department" class="cForm-input" />
                                                  </b-col>
                                                </b-form-row>

                                                
                                             </b-col>
                                            <b-col cols="12">
                                             <br>
                                            </b-col> 

                                          <b-col lg="4" md="12" class="cuestomRow">
                                            <b-form-row  v-for="(m, index) in tmp.mail" :key="m.id">
                                              <b-col sm="4" cols="12" lg="3" class="cForm">Mail {{(index+1)}}:</b-col>
                                              <b-col sm="8" cols="12" lg="9">
                                                <b-input-group>
                                                  <b-form-input v-model="m.mail" @change="editContactInPerson('mail', tmp.mail)" type="text" placeholder="Enter mail" class="cForm-input" />
                                                    <b-input-group-append>
                                                      <b-link style="margin-left:10px" @click.pervert="(index==0)?addContactInPerson('mail', '+', index):addContactInPerson('mail', '-', index)">
                                                        {{(index==0)?'+':'-'}}
                                                      </b-link>
                                                    </b-input-group-append>
                                                </b-input-group>
                                              </b-col>
                                            </b-form-row>                                         
                                          </b-col>
                                          <b-col lg="4" md="12" class="cuestomRow">
                                            <b-form-row  v-for="(p, index) in tmp.phone" :key="p.id">
                                              <b-col sm="4" cols="12" lg="3" class="cForm">Phone {{(index+1)}}:</b-col>
                                              <b-col sm="8" cols="12" lg="9">
                                                <b-input-group>
                                                  <b-form-input v-model="p.phone" @change="editContactInPerson('phone', tmp.phone)" type="text" placeholder="Enter phone" class="cForm-input" />
                                                    <b-input-group-append>
                                                      <b-link style="margin-left:10px" @click.pervert="(index==0)?addContactInPerson('phone', '+', index):addContactInPerson('phone', '-', index)">
                                                          {{(index==0)?'+':'-'}}
                                                      </b-link>
                                                    </b-input-group-append>
                                                </b-input-group>
                                              </b-col>
                                            </b-form-row>
                                          </b-col>
                                          <b-col lg="4" md="12"  class="cuestomRow">
                                            <b-form-row  v-for="(f, index) in tmp.fax" :key="f.id">
                                              <b-col sm="4" cols="12" lg="3" class="cForm">Fax {{(index+1)}}:</b-col>
                                              <b-col sm="8" cols="12" lg="9">
                                                <b-input-group>
                                                  <b-form-input v-model="f.fax"  @change="editContactInPerson('fax', tmp.fax)" type="text" placeholder="Enter fax" class="cForm-input" />
                                                    <b-input-group-append>
                                                      <b-link style="margin-left:10px" @click.pervert="(index==0)?addContactInPerson('fax', '+', index):addContactInPerson('fax', '-', index)">
                                                          {{(index==0)?'+':'-'}}
                                                      </b-link>
                                                    </b-input-group-append>
                                                </b-input-group>
                                              </b-col>
                                            </b-form-row>
                                          </b-col>

                                          <b-col cols="12"><br></b-col>

                                           <b-col cols="12" class="cuestomRow">
                                             <b-form-row  v-for="(a, index) in tmp.adress" :key="a.id">
                                                <b-col sm="4" cols="12" lg="1" class="cForm">Adress {{(index+1)}}:</b-col>
                                                <b-col sm="8" cols="12" lg="11">
                                                  <b-input-group>
                                                    <b-form-input :value="a.adress.split(';')[0]" @input="a.adress=$event+';'+a.adress.split(';')[1]+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')" @change="editContactInPerson('adress', tmp.adress)"
                                                      type="text" placeholder="Adress line 1" class="cForm-input" />
                                                    <b-form-input :value="a.adress.split(';')[1]" @input="a.adress=a.adress.split(';')[0]+';'+$event+';'+a.adress.split(';')[2];a.adress=a.adress.replace(undefined, '')" @change="editContactInPerson('adress', tmp.adress)"
                                                      type="text" placeholder="Adress line 2" class="cForm-input" />
                                                    <b-form-input :value="a.adress.split(';')[2]" @input="a.adress=a.adress.split(';')[0]+';'+a.adress.split(';')[1]+';'+$event;a.adress=a.adress.replace(undefined, '')"  @change="editContactInPerson('adress', tmp.adress)"
                                                      type="text" placeholder="Adress line 3" class="cForm-input" />
                                                    <b-input-group-append>
                                                      <b-link style="margin-left:10px"
                                                      @click.pervert="(index==0)?addContactInPerson('adress', '+', index):addContactInPerson('adress', '-', (index))">
                                                          {{(index==0)?'+':'-'}}
                                                      </b-link>
                                                    </b-input-group-append>
                                                  </b-input-group>
                                                </b-col>
                                              </b-form-row>
                                            </b-col> 
                                        </b-row>
                                    </b-container>
                                </container-body>
                            </container>
                        </b-tab>
                           <b-tab title="Files">
                            <container>
                                <container-body>
                                     <b-table :items="filesCustomer" :fields="fieldsFiles" class="tableProject">
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
<script type="text/javascript">
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
    props: {
        id: String
    },
    data() {
        return {
                files:[],
                filesCustomer:[],
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
                show:"Show",
                contactEditType: null,
                contactEditData: [],
                countNamePerson: [''],
                countMailPerson: [''],
                countPhonePerson: [''],
                countFaxPerson: [''],
                countOtherPerson:null,
                addFirm:null,
                addAppeal:null,
                addDep:null,
                addPos:null,
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
                items1:[],
                fields: {
                    in: {
                    label: 'Number',
                    sortable: true,
                    class: 'n'
                    },
                    appeal: {
                    label: 'Appeal',
                    sortable: true,
                    class: 'a'
                    },
                    names: {
                    label: 'Name',
                    sortable: true,
                    class: 'number'
                    },
                    data: {
                    label: 'Registred',
                    sortable: true,
                    class: 'r'
                    },
                    pos: {
                    label: 'Position',
                    sortable: true,
                    class: 'number'
                    },
                    dep: {
                    label: 'Department',
                    sortable: true,
                    class: 'number'
                    },
                    delete: {
                    label: 'Delete',
                    class: 'del'
                    }
                }
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
    loadDocToFrame(index) {
            setTimeout(() => {
                if (this.$refs['ifrForm' + index].submit() != undefined) this.$refs['ifrDocForm' + index].submit()
            }, 10);
        },
    sendingEvent(file, xhr, formData) {
            xhr.setRequestHeader('number', 'customer-'+this.id);
        },
    sendingEvent1(file, xhr, formData) {
            xhr.setRequestHeader('number', 'person-'+this.tmp.person);
        },
        fsadd() {
            this.$refs.myVueDropzone.removeAllFiles()
            this.$socket.send('getFilesCustomer')
            this.$socket.send('getFilesPerson')
        },
    getFilesCustomer(){
        axios.get('/files', {
            params: {
                id: 'customer-'+this.id
            }
        }).then(response => {
            this.files = response.data
        })
    },
    getFilesPerson(){
        axios.get('/files', {
            params: {
                id: 'person-'+this.tmp.person
            }
            }).then(response => {
                this.filesCustomer = response.data
            })
    },

    addContactInPerson(fild, action, index){
        if (action=='+'){
            this.tmp[fild].push({[fild]:''})
        } else{
          // console.log(fild, action, index)
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
        // if (typeof value != 'String') {
           // console.log(value)
        //   var value1 = []
        //   value1.push(value)
        // }
        // else {
        //   console.log(2)
        //   var value1 = value
        // }
        
        var sendArr=[]
        value.forEach((v)=>{
            sendArr.push(v[fild])
        })
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
            if (confirm("Are you sure?")) {
                axios.get('/del_person', {
                    params: {
                        id: val
                    }
                })
            };
    },
    itemsFilter(val){
        if(val==1){
            var arr = this.items.filter(function(val){
            if (val.old==false){
                return val
            }
        })
        this.items=arr
        }else{
            this.items=this.items1
        }
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
    

    insertCustomer(val, type){
            if (confirm("Are you sure want to add "+type+": "+val[0]+" for "+this.name +" ?")) {
                axios.get('/add_contact_from_customer', {
                    params: {
                                type: type,
                                val: val[0],
                                id: this.id,
                            }
                    })
                }
        },
        contactEdit(type, val){

            this.contactEditType = this[type]?type:['']
            if (val.length==0){
              val.push('')  
            }
            this.contactEditData = val
            //console.log(typeof(this.contactEditData), this.contactEditData, val)
            this.$refs.contact.show()
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

                 // this.tmp.adress = item.adress
                 this.tmp.appeal = item.appeal
                 this.tmp.customer_group = item.customer_group
                 this.tmp.data = item.data
                 this.tmp.dep = item.dep
                 this.tmp.names = item.names
                 this.tmp.old = item.old
                 this.tmp.other = item.other
                 this.tmp.person = item.person
                 // this.tmp.data = item.person.data
                 this.tmp.pos = item.pos

                axios.get('/files', {
                    params: {
                        id: 'person-'+this.tmp.person
                    }
                }).then(response => {
                    this.filesCustomer = response.data
                })
                
                // item.mail = response.data.mail,
                // item.phone=response.data.phone,
                // item.fax=response.data.fax,
                // item.adress=response.data.adress,
              // console.log(item)
               //  this.tmp = item
            })


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
        // updateCustomerAfter(){
        //     this.$options.sockets.onmessage = (data) => (data.data=='getCustomerDetail') ? this.getCustomerDetail(): '';
        //     this.$options.sockets.onmessage = (data) => (data.data=='getCustomerContact') ? (this.getContact(this.tmp.person)):'';

        // },
        updateCustomer(fild, newData){
        axios.get('/updateCustomer', {params: {
                id: this.id,
                date: newData,
                fild: fild
        }})
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
                      this.zip = zip,
                      this.city = city,
                      this.street = street
                      
                  }
                })
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
                axios.get('/get_persons', {
                    params: {
                        id: this.id
                    }
                }).then(response => {
                    this.items = response.data
                    this.items1= response.data
                    this.itemsFilter((this.show!='Show')?0:1)
                }),
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

        }
    },
    watch:{
    
        items (val) {
            val.forEach((v)=>{
                if (v.person==this.tmp.person){
                    // this.tmp.adress=(v.adress!=this.tmp.adress)?v.adress:this.tmp.adress,
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
           setTimeout(() => {
        this.$socket.send('getCustomerDetail')
        this.$socket.send('getFilesCustomer')
        this.$socket.send('getFilesPerson')
        
        this.$options.sockets.onmessage = (data) => (data.data=='getCustomerDetail') ? (this.getCustomerDetail()):'';
        this.$options.sockets.onmessage = (data) => (data.data=='getCustomerContact') ? (this.getContact(this.tmp.person)):'';
        this.$options.sockets.onmessage = (data) => (data.data=='getFilesCustomer') ? (this.getFilesCustomer()):'';
        this.$options.sockets.onmessage = (data) => (data.data=='getFilesPerson') ? (this.getFilesPerson()):'';
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
    height: 15px;
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
}

.b-form-group {
    padding: 0px;
    height: 4px;
}

.customButton {
    padding: 1px;
    font-size: 10px;
    height: 16px;
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
@media screen and (min-width: 991px) {
    .n{
      text-align: center;
      width: 40px;
    }
    .a{
      width: 40px;
    }
    .r{
      width: 40px;
    }
    .del{
      text-align: center;
      width: 40px;
    }
}
</style>