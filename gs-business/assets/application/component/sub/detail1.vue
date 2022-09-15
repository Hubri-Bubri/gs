axios<template>
    <container>
  <input ref="unfocus" style="width: 0px; height: 0px; position: absolute; top: 0; left: 0; margin:0; padding:0; border: 0;"></input>

    <b-modal size="sm" centered id="worker" ref="worker" title="Select Workers" body-class="workerHeight">
        <b-form-input type="text" v-model="searchWorker" style="margin-bottom: 4px !important;"/>
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="workers"/>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="selectedWorkers=[]">Clear</button>
           </template>
        </b-modal>
<b-modal size="lg" centered id="addTask" ref="addTask" title="Add Task">
  <b-row>
<b-col cols="6" class="text-right">
 Description of task:<br />
    <VueCtkDateTimePicker
    format="YYYY-MM-DD H:mm" v-model="startTask" no-label id="DateTimePicker1"
    input-size="sm" label="From:" minute-interval="10" >
    </VueCtkDateTimePicker><br />
    <VueCtkDateTimePicker
    format="YYYY-MM-DD H:mm" v-model="endTask" no-label id="DateTimePicker2"
    input-size="sm" label="To:" minute-interval="10" >
    </VueCtkDateTimePicker>
</b-col>
<b-col  cols="6" class="cForm">
      <b-form-textarea type='text' class="cForm-input" v-model="taskName" rows="6"/>
  </b-col>     
  </b-row>

<template slot="modal-footer">
  <b-button @click="newTaskSave" variant="primary">
    OK
  </b-button>
</template>
</b-modal>


 <b-modal centered id="customer" ref="customer" title="Add Customer" body-class="workerHeight">
  <b-row>
<b-col sm="3">
    <label>Name:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' :state="(this.customerName!='')?null:false" @keyup.native="searchZipName(customerName)" class="cForm-input" v-model="customerName" />
</b-col>

<b-col sm="3">
    <label>Zip code:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' v-model="customerZip" @keyup.native="searchZipCustomer(customerZip)" class="cForm-input"  />
</b-col>
<b-col sm="3">
    <label>City:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' v-model="customerCity" class="cForm-input"  />
</b-col>
<b-col sm="3">
    <label>Street:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text'  v-model="customerStreet" class="cForm-input"  />
<!--       <textarea>{{answer}}</textarea> -->
</b-col>
<b-col sm="3">
    <label>Tax Number:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' class="cForm-input" v-model="customerTax" />
</b-col>

<b-col sm="3">
    <label>Web-site:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' class="cForm-input"  v-model="customerWeb" />
</b-col>
<b-col sm="3">
    <label>Bic:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' class="cForm-input"  v-model="customerBic" />
</b-col>
<b-col sm="3">
    <label>Iban:</label>
</b-col>
<b-col sm="9" class="cForm">
       <b-form-input type='text' class="cForm-input"  v-model="customerIban" />
  </b-col>     
  </b-row>


        
         <b-row v-for="(mail, index) in countMailCustomer" :key="mail.id">
      <b-col sm="3">
        <label >mail{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countMailCustomer[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countMailCustomer.push('')">+</b-button>
       <b-button class="cForm-inputG"  v-else @click="countMailCustomer.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>

      <b-row v-for="(phone, index) in countPhoneCustomer" :key="phone.id">
      <b-col sm="3">
        <label >phone{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countPhoneCustomer[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countPhoneCustomer.push('')">+</b-button>
       <b-button class="cForm-inputG"  v-else @click="countPhoneCustomer.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>

            <b-row v-for="(fax, index) in countFaxCustomer" :key="fax.id">
      <b-col sm="3">
        <label >fax{{(index==0)?'':' '+(index+1)}}:</label>
      </b-col>
      <b-col sm="9" class="cForm">
        <b-input-group>
       <b-form-input type='text' class="cForm-input" v-model="countFaxCustomer[index]" />
       <b-button class="cForm-inputG" v-if="index==0" @click="countFaxCustomer.push('')">+</b-button>
       <b-button class="cForm-inputG"  v-else @click="countFaxCustomer.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>
        <b-row>
         <b-col sm="3">
        <label >Other: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <b-form-textarea v-model="countOtherCustomer"></b-form-textarea>
      </b-col>
    </b-row>
             <template slot="modal-footer">
                    <b-button @click="newCustomerSave" variant="primary">
                        OK
                    </b-button>
                </template>
</b-modal>

        <b-modal centered id="personModal" ref="personModal" title="Add Person" body-class="workerHeight">
  <b-row class="my-1">
      <b-col sm="3">
        <label >Firma: </label>
      </b-col>
      <b-col sm="9" class="cForm">
        <v-select taggable :createOption="newFirm" :class="(addFirm==null)?'selrequired':''" label="name" v-model="addFirm" :options="area" />
      </b-col>
      <b-col sm="3">
        <label >Appeal: </label>
      </b-col>
      <b-col sm="9" class="cForm">
        <v-select taggable label="name" v-model="addAppeal" :options="['Mr.', 'Mrs.', 'Miss', 'Ms']" />
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
       <b-button class="cForm-inputG"  v-else @click="countNamePerson.splice(index, 1)">-</b-button>
   </b-input-group>
   </b-col>
     </b-row>
<b-row>
      <b-col sm="3">
        <label >Deportament: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <v-select taggable label="name" v-model="addDep"  :options="['1', '2', '3', '4']" />
      </b-col>
        <b-col sm="3">
        <label >Position: </label>
      </b-col>
      <b-col sm="9" class="cForm">
       <v-select taggable label="name" v-model="addPos"  :options="['1', '2', '3', '4']" />
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
       <b-button class="cForm-inputG"  v-else @click="countMailPerson.splice(index, 1)">-</b-button>
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
       <b-button class="cForm-inputG"  v-else @click="countPhonePerson.splice(index, 1)">-</b-button>
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
       <b-button class="cForm-inputG"  v-else @click="countFaxPerson.splice(index, 1)">-</b-button>
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
        <b-modal size="lg" centered id="mails" ref="mails" title="Select mails and docs" body-class="workerHeight">

            <b-form-checkbox-group buttons  button-variant="light" style="width:30%" v-model="mailSelect" stacked :options="modalMail"/>

            <b-form-checkbox-group buttons  button-variant="light" style="width:60%"  stacked :options="modalFiles"/>
   
            <template slot="modal-footer">

                        <b-select taggable class="selBtn"  :options="['template1', 'template2']"></b-select>

              <button type="button" left class="btn btn-secondary" @click="sendmail()">Send</button>
           </template>
        </b-modal>
        <b-modal size="lg" centered ok-only id="map" title="Track">
            <b-embed type="iframe" aspect="16by9" :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+project.street">
            </b-embed>
        </b-modal>
        <b-modal size="lg" centered ok-only ref="printOffer1">
            <div slot="modal-title" class="w-100">
                <div>Print</div>
            </div>
            <iframe type="iframe1" style="width:100%;height:617px;" name="myIframe1" src="" />
        </b-modal>

        <b-modal size="lg" centered ok-only ref="printOffer">
            <div slot="modal-title" class="w-100">
                <div>Print
                </div>
            </div>
            <b-container fluid class="prokrutka" v-show="viewPrint" style="font-size:12px;"
            id="printPages" ref="printPages" v-if="tmp.type=='Damage Description'">
  <b-row>
                        <b-col cols="6" style="font-size:12px; font-weight: 100;" v-if="(customerContract.indexOf('Report')==-1)">
                            {{getCustomer()}}<br>
                            {{getPerson()}}<br>
                            {{getCustomerAdress()}}<br>
                            {{getCustomerAdress1()}}
                        </b-col>
                        <b-col cols="6" style="font-size:12px; font-weight: 100;" v-if="(customerContract.indexOf('Report')==-1)">
                            {{project.editor!=null?'Editor: '+project.editor:''}} <br v-if="project.editor!=null">
                            {{$security.table.account.tel!=null?'Telfon: '+$security.table.account.tel:''}} <br v-if="$security.table.account.tel!=null">
                            {{$security.table.account.fax!=null?'Fax: '+$security.table.account.fax:''}} <br v-if="$security.table.account.fax!=null">
                            {{$security.table.account.mail!=null?'E-mail: '+$security.table.account.mail:''}} 
                        </b-col>
                    </b-row>
                    <br>
                    <h5 v-if="(customerContract.indexOf('Report')==-1)">{{(tmpForDamageDescription.name.content==null)?tmp.typeOfHead:tmpForDamageDescription.name.content}}  Num.: {{tmp.number}}</h5>
                    <h5 v-else>Report  Num.: {{tmp.number}}</h5>
                    
                    <h6 v-if="(customerContract.indexOf('Report')==-1)">{{(tmpForDamageDescription.name.content==null)?tmp.typeOfHead:tmpForDamageDescription.name.content}} date: {{ getDateFormat(today) }}</h6>
                     <table width="100%" class="tablePadding">
                        <tr>
                            <td style="width:65%">Our services for you:<br>
                                <b>{{tmp.work}}</b>
                            </td>
                            <td style="width:35%">{{tmp.typeOfHead}} Number:<br>
                                <b>{{tmp.number}}</b>
                            </td>
                        </tr>
                       
                 <tr>
                            <td>Place of incident:<br>
                                <b>{{tmp.place}}</b>
                            </td>
                            <td>Сustomer Сontract: <br>
                                <b>{{(tmp.other!='')?tmp.other:"&nbsp;"}}</b>
                            </td>
                        </tr>
                         <tr>
                            <td :colspan="(tmp.insurance=='')?2:1">incident Address:<br v-if="(tmp.insurance!='')">
                                <b>{{project.street}}, {{project.zip}} {{project.city}}</b></td>
                            <!-- <td>Contract Number:<br>
                                <b>{{tmp.insurance}}</b>
                            </td> -->
                            <td v-if="tmp.insurance!=''">Insurance Number: <br>
                                <b>{{tmp.insurance}}</b>
                            </td>
                        </tr>
                    </table> <br>
                    <table width="100%" class="tablePadding" v-if="(customerContract.indexOf('Report')==-1)">
                      <tr>
                        <td>Event date:</td>
                        <td>{{getDateFormat(tmp.dateEvent)}}</td>
                        <td>Inspection date:</td>
                        <td>{{getDateFormat(tmp.dateInspect)}}</td>
                      </tr>
                      <tr>
                        <td>Damage reported:</td>
                        <td>{{getPerson()}}</td>
                        <td>Examining worker:</td>
                        <td>{{tmp.worker}}</td>
                      </tr>
                    </table>

<div v-if="(customerContract.indexOf('Report')==-1)"><br><br>
                    <p contenteditable="true" @input="firstText=$event.target.innerText">
                        {{firstText}}
                    </p>
                    <br> <br>
     

                    <br>
                    <br>
                          <b-row fluid v-for="(damage, index) in loadDamages" :key="damage.id">
 
                               <b-col cols="12">

                        <h6>{{damage.name}}</h6>
                       
                               </b-col>
                               <!-- <img :src="image" class="image mx-auto" :key="image" height="200px"> -->
                               

                             
                                  <b-col cols="6" v-for="image in damage.images" class="text-center border" :key="image.id">
                                    {{image.file_name}}<br>
                                      <b-img style="padding-top:5px;padding-bottom:5px;max-height:300px;max-width:350px;"
                                      :src="'/image_damage?id='+image.id"></b-img> <br>
                                    {{image.desc}}<br> <br>
                                  </b-col>

                             
                        
                            
                               
                                 <b-col cols="12">
                           {{damage.desc}}
                          
                                </b-col><br><br>
                              </b-row>
                            
                </div>
                <div v-else>

<b-container>
                      <b-row >
                            <b-col cols="2" class="text-center border"  contenteditable="true">
<b>Date</b>
                            </b-col>
                            <b-col cols="5" class="border"  contenteditable="true">
<b>Place - Description</b>             
                            </b-col>


                            <b-col cols="3" class="border"  contenteditable="true">
<b>Workers</b>                   
                            </b-col>

                            <b-col cols="2" class="border"  contenteditable="true">
<b>Time</b>                     
                            </b-col>
</b-row>
                     </b-container>       
                    </b-row>

                  <div  v-for="(damage, index) in loadDamages" :key="damage.id">
                    <b-container>
                     
                    <b-row  v-for="task in damage.tasks" :key="task.id">
                            <b-col cols="2" class="text-center border"  contenteditable="true">
                              {{task.data_time_start.split(' ')[0]}}
                            </b-col>
                            <b-col cols="5" class="border"  contenteditable="true">
                              {{damage.name}} - {{task.name}}
                            </b-col>
   
                            <b-col cols="3" class="border"  contenteditable="true" >
                            <div v-if="task.workers!=null">
                              <span  v-for="(woker, index) in task.workers.split(',')"><span v-if="index!=0">, </span> {{woker}}</span>
                            </div>
                            </b-col>
                                                     <b-col cols="2" class="border" v-if="task.data_time_end==null"  contenteditable="true">
                              {{ difTime(task.data_time_start, 's') }}
                              {{countWorker(task.workers)}}
                              <br>(unfinished)
                            </b-col>
                            <b-col cols="2" v-else class="border"  contenteditable="true">
                              {{ difTimeFinish(task.data_time_start, task.data_time_end, 's') }}
                              {{countWorker(task.workers)}}
                            </b-col>

                            
                    </b-row>
                     <b-row>

                    <b-col cols="10" class="text-right"><b>Hours:</b></b-col>
                    <b-col cols="2"> 

                    <div contenteditable="true"><b>{{summHour(damage.tasks, '(s)')}}</b></div>
                    </b-col>
                  </b-row>
                     <br>
                  </b-container>
                  </div>
                  <b-container>
                  <b-row>
                    <b-col cols="7"> </b-col>
                    <b-col cols="3"  class="border-top"> </b-col>
                    <b-col cols="2" class="border-top"> </b-col>

                    <b-col cols="7"> </b-col>
                    <b-col cols="3" class="text-right"> <b >Total Hours:</b></b-col>
                    <b-col cols="2">

                    <b  contenteditable="true" class="text-left">{{allhours('(s)')}}</b>
                    </b-col>
                  </b-row>
                </b-container>
                </div>
            <!--        <b-row fluid v-for="(damage, index) in loadDamages" :key="damage.id" v-else>
                      <b-row fluid>
                        <b-col cols="12" class="border">
                        <h6>{{damage.name}}</h6>
                        </b-col>
                      </b-row>
                        <b-row fluid v-for="task in damage.tasks"  :key="task.id">
                          <b-col cols="3" class="text-center border" :key="task.id">
                              {{task.data_time_start}}
                          </b-col>
                          <b-col cols="6" class="border">
                              {{task.name}}
                          </b-col>
                          <b-col cols="3" class="border">
                              hours
                          </b-col>                             
                       </b-row>        
                       <b-row fluid>
                         <b-col cols="12">
                             {{damage.desc}}
                        </b-col>
                      </b-row>
                  </b-row> -->
                    
                         

            </b-container>
            <b-container fluid class="prokrutka" v-show="viewPrint" style="font-size:12px;"
            id="printPages" ref="printPages" v-if="tmp.type!='Damage Description'">
                <div v-show="prices">
                    <b-row>
                        <b-col cols="6" style="font-size:12px; font-weight: 100;">
                            {{getCustomer()}}<br>
                            {{getPerson()}}<br>
                            {{getCustomerAdress()}}<br>
                            {{getCustomerAdress1()}}
                        </b-col>
                        <b-col cols="6" style="font-size:12px; font-weight: 100;">
                            {{project.editor!=null?'Editor: '+project.editor:''}} <br v-if="project.editor!=null">
                            {{$security.table.account.tel!=null?'Telfon: '+$security.table.account.tel:''}} <br v-if="$security.table.account.tel!=null">
                            {{$security.table.account.fax!=null?'Fax: '+$security.table.account.fax:''}} <br v-if="$security.table.account.fax!=null">
                            {{$security.table.account.mail!=null?'E-mail: '+$security.table.account.mail:''}} 
                        </b-col>
                    </b-row>
                    <br>
                    <h5>{{tmp.typeOfHead}}  Num.: {{(tmp.typeOfHead=='Invoices')?tmp.number.split(' ')[0].split('-')[0]+'-'+countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[2]:tmp.number}}</h5>
                    <h6>{{tmp.typeOfHead}}  date: {{ getDateFormat(today) }}</h6>

                    <table width="100%" class="tablePadding">
                        <tr>
                            <td style="width:65%">Our services for you:<br>
                                <b>{{tmp.work}}</b>
                            </td>
                            <td  style="width:35%">Project Number:<br>
                                <b>{{project.number}}</b>
                            </td>
                        </tr>
                       
                        <tr>
                            <td>incident Address:<br>
                                <b>{{project.street}}, {{project.zip}} {{project.city}}</b>
                                
                            </td>
                            <td>Сustomer Сontract: <br>
                                <b>{{(tmp.other!='')?tmp.other:"&nbsp;"}}</b>
                            </td>
                        </tr>
                         <tr>
                            <td :colspan="(tmp.insurance=='')?2:1">Place of incident:<br  v-if="(tmp.insurance!='')">
                              <b>{{tmp.place}}</b>
                              </td>
                            <td v-if="tmp.insurance!=''">Insurance Number: <br>
                                <b>{{tmp.insurance}}</b>
                            </td>
                      <!--       <td>Contract Number:<br>
                                <b>{{tmp.insurance}}</b>
                            </td> -->
                        </tr>
                    </table>
                    <br>
                    <p contenteditable="true" @input="firstText=$event.target.innerText">
                        {{tmpForOffer.first.content}}
                    </p>
                      <calculation-print
                        :disc='disc'
                        :discP='discP'
                        :tax='tax'
                        :taxDub='taxDub'
                        :taxP='taxP'
                        :taxPDub='taxPDub'
                        :netto='netto'
                        :brutto='brutto'
                        :butDiscPerc='butDiscPerc'
                        :partx='partx'
                        :head="tmp.typeOfHead"
                        v-model="addtaxColapse"
                        :type="'head'">
                      </calculation-print> 
                     <br>
                    <b>Payment terms:</b><br>
                    <p contenteditable="true" @input="secondText=$event.target.innerText">
                        {{tmpForOffer.second.content}}
                    </p>
                    <br>
                    <hr>
                </div>
                <h6>Service List To {{tmp.typeOfHead}} Num.: {{(tmp.typeOfHead=='Invoices')?tmp.number.split(' ')[0].split('-')[0]+'-'+countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[2]:tmp.number}}</h6>
                <h6>{{(dateForInvoice!=null)?'Date Of Finish Works: '+getDateFormat(dateForInvoice):''}}</h6>
                <table width="100%" style="border-color:#000" class="tablePadding">
                    <tr>
                        <td  style="width:65%">Project Number:<br>
                                <b>{{project.number}}</b>
                        </td>
                        <td style="width:35%">Сustomer Сontract: <br>
                             <b>{{(tmp.other!='')?tmp.other:"&nbsp;"}}</b>
                        </td>
                    </tr>




                    <tr>
                        <td  :colspan="(tmp.insurance=='')?2:1">Adress:<br  v-if="(tmp.insurance!='')">
                            <b>{{project.street}}, {{project.zip}} {{project.city}}</b>
                        </td>
                        <td v-if="tmp.insurance!=''" style="width:35%">Insurance Number: <br>
                             <b>{{tmp.insurance}}</b>
                        </td>
                       <!--  <td>Contract Number:<br>
                            <b>{{tmp.insurance}}</b>
                        </td> -->
                    </tr>
                </table>
                <br><br>


                  <calc-table-group-print v-model="partx" :addtaxColapse="addtaxColapse"
                :workers="workers" :comments="comments" :prices="prices" :commentOfTable="commentOfTable">
                </calc-table-group-print> 
                <calculation-print :align='"end"' :partx='partx'
                        :disc='disc'
                        :discP='discP'
                        :tax='tax'
                        :taxDub='taxDub'
                        :taxP='taxP'
                        :taxPDub='taxPDub'
                        :netto='netto'
                        :brutto='brutto'
                        :butDiscPerc='butDiscPerc'
                v-model="addtaxColapse" :summ="alltotal(this.partx)" v-show="prices"></calculation-print> 
                <br>
                <div v-show="comments" style="font-size:12px;" contenteditable="true" v-html="commentOfTable"></div>
                <br>
                <div v-show="(customerContract.indexOf('Cost Sharing')!=-1)">
                    <hr>
                    <h6>Cost Sharing Num.: {{(tmp.typeOfHead=='Invoices')?tmp.number.split(' ')[0].split('-')[0]+'-'+countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[2]:tmp.number}}</h6>
                    <table width="100%" style="border-color:#000" class="tablePadding">
                        <tr>
                            <td>Project Number:<br>
                                <b>{{project.number}}</b>
                            </td>
                            <td >Сustomer Сontract: <br>
                                 <b>{{(tmp.other!='')?tmp.other:"&nbsp;"}}</b>
                            </td>
                        </tr>





                        <tr>
                            <td :colspan="(tmp.insurance=='')?2:1">Adress:<br  v-if="(tmp.insurance!='')">
                                <b>{{project.street}}, {{project.zip}} {{project.city}}</b>
                            </td>
                            <td v-if="tmp.insurance!=''" >Insurance Number: <br>
                                 <b>{{tmp.insurance}}</b>
                            </td>
                           <!--  <td>Contract Number:<br>
                                <b>{{tmp.insurance}}</b>
                            </td> -->
                        </tr>
                    </table>
                    <br>
                    <p contenteditable="true" @input="threText=$event.target.innerText">
                        {{tmpForOfferSharing.first.content}}
                    </p>
                    <br><br><br><br>
                    <b-row align-h="around">
                        <b-col cols=3 style="border-top: 1px solid #000;" class="text-center">City And Date</b-col>
                        <b-col cols=3 style="border-top: 1px solid #000;" class="text-center">Stamp And Signature</b-col>
                    </b-row>
                    <br>
                    <p contenteditable="true" @input="fourText=$event.target.innerText">
                        {{tmpForOfferSharing.second.content}}
                    </p>
                </div>
                <div v-show="(customerContract.indexOf('Order Award')!=-1)">
                    <hr>
                    <h6>Order Award Num.: {{(tmp.typeOfHead=='Invoices')?tmp.number.split(' ')[0].split('-')[0]+'-'+countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[2]:tmp.number}}</h6>
                    <table width="100%" style="border-color:#000" class="tablePadding">
                        <tr>
                            <td>Project Number:<br>
                                <b>{{project.number}}</b>
                            </td>
                            <td >Сustomer Сontract: <br>
                                 <b>{{(tmp.other!='')?tmp.other:"&nbsp;"}}</b>
                            </td>
                        </tr>
   



                        <tr>
                            <td :colspan="(tmp.insurance=='')?2:1">Adress:<br  v-if="(tmp.insurance!='')">
                                <b>{{project.street}}, {{project.zip}} {{project.city}}</b>
                            </td>
                            <td v-if="tmp.insurance!=''" >Insurance Number: <br>
                                 <b>{{tmp.insurance}}</b>
                            </td>
                         <!--    <td >Contract Number:<br>
                                <b>{{tmp.insurance}}</b>
                            </td> -->
                        </tr>
                    </table>
                    <br>
                    <p contenteditable="true" @input="fiveText=$event.target.innerText">
                        {{tmpForOfferAward.first.content}}
                    </p>
                    <br><br><br><br>
                    <b-row align-h="around">
                        <b-col cols=3 style="border-top: 1px solid #000;" class="text-center">City And Date</b-col>
                        <b-col cols=3 style="border-top: 1px solid #000;" class="text-center">Stamp And Signature</b-col>
                    </b-row>
                    <br>
                    <p contenteditable="true" @input="sixText=$event.target.innerText">
                        {{tmpForOfferAward.second.content}}
                    </p>
                </div>
            </b-container>
            <iframe type="iframe" v-show="!viewPrint" style="width:100%;height:617px;" name="myIframe" src="" />
            <form target="myIframe" action="/pdf" method="post" style="display:none" ref="preForm">
                <input type="hidden" name="dateInspect" :value="tmp.dateInspect" />
                <input type="hidden" name="dateEvent" :value="tmp.dateEvent" />
                <input type="hidden" name="worker" :value="tmp.worker" />
                <textarea name="loadDamages">{{loadDamages}}</textarea>

                <input type="hidden" name="customerСontract" :value="(tmp.other!='')?tmp.other:' '" />
                <input type="hidden" name="getCustomer" :value="getCustomer()" />
                <input type="hidden" name="getPerson" :value="getPerson()" />
                <input type="hidden" name="getCustomerAdress" :value="getCustomerAdress()" />
                <input type="hidden" name="getCustomerAdress1" :value="getCustomerAdress1()" />
                <input type="hidden" name="offerHead" :value="tmp.typeOfHead" />
                <input type="hidden" name="subHead" :value="tmpForDamageDescription.name.content" />
                
                <input type="hidden" name="editor" :value="project.editor" />
                <input type="hidden" name="userTel" :value="$security.table.account.tel" />
                <input type="hidden" name="userFax" :value="$security.table.account.fax" />
                <input type="hidden" name="userMail" :value="$security.table.account.mail" />

                <input type="hidden" name="number" :value="tmp.number" />
                <input type="hidden" name="date" :value="getDateFormat(today)" />
                <input type="hidden" name="work" :value="tmp.work" />
                <input type="hidden" name="pNumber" :value="tmp.number" />
                <input type="hidden" name="street" :value="project.street" />
                <input type="hidden" name="zip" :value="project.zip" />
                <input type="hidden" name="city" :value="project.city" />
                <input type="hidden" name="insurance" :value="tmp.insurance" />
                <input type="hidden" name="place" :value="tmp.place" />
                <input type="hidden" name="finishWork" :value="(dateForInvoice!=null)?'Date Of Finish Works: '+getDateFormat(dateForInvoice):''" />
                <input type="hidden" name="firstText" :value="(tmp.typeOfHead=='Damage Description')?firstText:tmpForOffer.first.content" />
                <input type="hidden" name="secondText" :value="tmpForOffer.second.content" />
                <input type="hidden" name="positions" :value="partx" />
                <input type="hidden" name="comment" :value="commentOfTable" />
                <input type="hidden" name="project_id" :value="this.id" />
                <textarea name="tables">{{partx}}</textarea>
                 <calculation-print 
                        :disc='disc'
                        :discP='discP'
                        :tax='tax'
                        :taxDub='taxDub'
                        :taxP='taxP'
                        :taxPDub='taxPDub'
                        :netto='netto'
                        :brutto='brutto'
                        :butDiscPerc='butDiscPerc'
                 :partx='partx' v-model="addtaxColapse" :summ="alltotal(this.partx)" type="send" v-show="prices"></calculation-print>
                 <input type="hidden" name="addtaxColapse" :value="addtaxColapse" />
<!--                 <input type="hidden" name="alttax" :value="alttax" />
 -->                <input type="hidden" name="workers" :value="workers" />
                <input type="hidden" name="threText" :value="(customerContract.indexOf('Cost Sharing') != -1) ? tmpForOfferSharing.first.content : ''" />
                <input type="hidden" name="fourText" :value="(customerContract.indexOf('Cost Sharing') != -1) ? tmpForOfferSharing.second.content : ''" />
                <input type="hidden" name="fiveText" :value="(customerContract.indexOf('Order Award') != -1) ? tmpForOfferAward.first.content : ''" />
                <input type="hidden" name="sixText" :value="(customerContract.indexOf('Order Award') != -1) ? tmpForOfferAward.second.content : ''" />
                <input type="hidden" name="prices" :value="prices" />
                <input type="hidden" name="addPdf" :value="addPdfs" />
            </form>
            <div slot="modal-footer" class="w-100">
                <b-row>
                    <b-col cols="6" v-if="(tmp.typeOfHead!='Report')">
                       <b-form inline>
                      <b-col cols="4">Date Of Print</b-col>
                      <b-col cols="8"> 
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;"
                        size="sm" type="date" v-model="today" /></b-col>
                      </b-form>
                      
                    </b-col>
                    <b-col cols="6"> 
 <b-form inline v-if="tmp.typeOfHead=='Invoices'">
                        <b-col cols="4">End Works</b-col>
                        <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;" size="sm" type="date"
                           :state="(dateForInvoice==null)?false:null" v-model="dateForInvoice" />
                        </b-col>
                      </b-form>
 <b-form inline  v-if="(tmp.typeOfHead=='Offers') || (tmp.typeOfHead=='Orders')">

   <label class="col-md-7" style=" text-align: right;">Temp Offer:</label> 

          <b-select  class="col-md-5" @change="changeTmp($event, 'Offer')">
            <option v-for="opt in tempForModal.filter((v)=>{if (v.type.content=='Offer') return v})">{{opt.name.content}}</option>
          </b-select>

</b-form>

 <b-form inline  v-if="(tmp.typeOfHead=='Damage Description') && (customerContract.indexOf('Report')==-1)">

   <label class="col-md-7" style=" text-align: right;" >Head:</label> 

          <b-select  class="col-md-5" @change="changeTmp($event, 'DamageDescription'); ">
            <option v-for="opt in tempForModal.filter((v)=>{if (v.type.content=='Damage Description') return v})">{{opt.name.content}}</option>
          </b-select>

</b-form>

 <b-form inline v-show="(customerContract.indexOf('Cost Sharing')!=-1)"  v-if="(tmp.typeOfHead=='Offers') || (tmp.typeOfHead=='Orders')">

   <label class="col-md-7">Temp Cost Sharing:</label> 

          <b-select  class="col-md-5"  @change="changeTmp($event, 'Sharing')">
            <option v-for="opt in tempForModal.filter((v)=>{if (v.type.content=='Offer-Cost Sharing') return v})">{{opt.name.content}}</option>
          </b-select>

</b-form>


 <b-form inline v-show="(customerContract.indexOf('Order Award')!=-1)" v-if="(tmp.typeOfHead=='Offers') || (tmp.typeOfHead=='Orders')">

   <label class="col-md-7">Temp Order Award:</label> 

          <b-select  class="col-md-5"  @change="changeTmp($event, 'Award')">
            <option v-for="opt in tempForModal.filter((v)=>{if (v.type.content=='Offer-Order Award') return v})">{{opt.name.content}}</option>
          </b-select>

</b-form>
          
                        

                    </b-col>
                </b-row>
                <b-row style="padding-top:5px;">
                    <b-col cols="6">
              <b-button-group size="sm">
                            <b-button :variant=" (prices==true) ? 'outline-primary' : 'primary'" @click="price" v-if="tmp.type!='Damage Description'">
                                Working
                            </b-button>
                            <b-button :variant=" viewPrint ? 'outline-primary' : 'primary'" @click="preview">
                                Preview
                            </b-button>
                            <b-button variant="primary" @click="addPdf">
                                Add
                            </b-button>
                            <b-button variant="primary" href='mailto:test@test.test'>
                                Send Mail
                            </b-button>
                        </b-button-group>


                      
                    </b-col>
                    <b-col cols="6">
                         <b-form-checkbox-group buttons button-variant="outline-primary" v-model="customerContract" size="sm"
                        :options="['Cost Sharing', 'Order Award']" @change="updatePrew" v-if="tmp.type!='Damage Description'">
                        </b-form-checkbox-group>

                        <b-form-checkbox-group buttons button-variant="outline-primary" v-model="customerContract" size="sm"
                        :options="['Report']" @change="updatePrew(); tmp.typeOfHead=(customerContract.indexOf('Report')==-1)?'Report':'Damage Description'" v-if="tmp.type=='Damage Description'">
    
                        </b-form-checkbox-group>
                    </b-col>
                </b-row>
            </div>
        </b-modal>
        <b-form @submit.prevent="addOk">
            <b-modal size="md" centered id="addSame" ref="addSame" :title="'Add '+addhead">
                <b-form-group horizontal :label-cols="4" label="Order Number:" label-for="OrderNumber" style="padding: 5px;">
                    <b-form-input v-model="project.number" class="cForm-input" id="OrderNumber" disabled :state="null" type="text" placeholder="Enter number" />
                </b-form-group>
                <b-form-group horizontal :label-cols="4" label="Type Of Work:" label-for="work" style="padding: 5px;">
                    <b-form-select class="select" id="work" :options="works" v-model="add_offer.work" required />
                </b-form-group>
              <!--   <b-form-group horizontal :label-cols="4" label="Insurance Number:" label-for="InsuranceNumber" style="padding: 5px;padding-top: 8px;">
                    <b-form-input class="cForm-input" id="InsuranceNumber" :state="null" type="number" v-model="add_offer.insurance_number" placeholder="Enter number" required />
                </b-form-group>
                <b-form-group horizontal :label-cols="4" label="Place:" label-for="place" style="padding: 5px;">
                    <b-form-input class="cForm-input" id="place" placeholder="Enter place" :rows="2" :max-rows="4" required v-model="add_offer.place" />
                </b-form-group>
                <b-form-textarea class="cForm-text" id="textarea1" placeholder="Enter something" :rows="2" :max-rows="6" required v-model="add_offer.comment" /> -->
                <template slot="modal-footer">
                    <b-button type="submit" variant="primary" data-toggle="addSame">
                        OK
                    </b-button>
                </template>
            </b-modal>
        </b-form>
        
        <container-header class="container-fluid">
            <top-menu>
            </top-menu>
        </container-header>
        <container-body class="container-fluid">
            <b-card-group deck>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Project">
                            <container>
                                <container-body>
                                    <b-container style="padding: 0px;">
                                        <b-row>
                                            <b-col lg="6" md="12" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Project&nbsp;Number:">
                                                    <b-form-input  :state="null" disabled type="text" :value="project.number" placeholder="Enter project number" class="cForm-input" />
                                                </b-form-group>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Date:" >
                                                    <b-form-input  :state="null" type="date" @change="updateProject('date', $event)" :value="project.date" placeholder="Enter date" class="cForm-input" :disabled="disablefild('pdata', id)" @focus.native="changeDisable('f', 'pdata', id)" @blur.native="changeDisable('b', 'pdata', id)" :id="'pdata'+id"  />
                                                </b-form-group>

                                              <b-tooltip triggers="none" :show="disablefild('pdata', id)" :target="'pdata'+id">
                                              {{disablefildUser('pdata', id)}}
                                              </b-tooltip>

                                                </b-form-group>

                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Subcontractor:">
                                                    <b-form-input :state="null" type="text" disabled :value="project.editor" placeholder="Enter editor name" class="cForm-input"  />
                                                </b-form-group>
                                            

                                            </b-col>
                                            <b-col lg="6" md="12" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Zip code:" >
                                                    <b-form-input  :state="null" type="text" @change="searchZip($event)" :value="project.zip" placeholder="Enter zip code" class="cForm-input" :disabled="disablefild('pzip', id)" @focus.native="changeDisable('f', 'pzip', id)" @blur.native="changeDisable('b', 'pzip', id)" :id="'pzip'+id"  />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('pzip', id)" :target="'pzip'+id">
                                              {{disablefildUser('pzip', id)}}
                                              </b-tooltip>

                                          
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="City:" >
                                                    <b-form-input  :state="null" type="text" @change="updateProject('city', $event)" :value="project.city" placeholder="Enter city" class="cForm-input" :disabled="disablefild('pcity', id)" @focus.native="changeDisable('f', 'pcity', id)" @blur.native="changeDisable('b', 'pcity', id)" :id="'pcity'+id"  />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('pcity', id)" :target="'pcity'+id">
                                              {{disablefildUser('pcity', id)}}
                                              </b-tooltip>

                                                   <b-form-group horizontal :label-cols="4" class="cForm" label="Street:">
                                                    <b-input-group>
                                                        <b-form-input :state="null" type="text" @change="updateProject('street', $event)" :value="project.street" placeholder="Enter street" class="cForm-inputBeforG" :disabled="disablefild('pstreet', id)" @focus.native="changeDisable('f', 'pstreet', id)" @blur.native="changeDisable('b', 'pstreet', id)" :id="'pstreet'+id" />
                                                        <b-button v-b-modal.map class="cForm-inputG">
                                                            G
                                                        </b-button>
                                                    </b-input-group>
                                                    <b-tooltip triggers="none" :show="disablefild('pstreet', id)" :target="'pstreet'+id">
                                              {{disablefildUser('pstreet', id)}}
                                              </b-tooltip>
                                                </b-form-group>
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row>
                                            <b-col lg="6" md="12" class="cuestomRow">
                                                 <!-- <b-button  class="customButton" @click="getSubDetail(2)">
                                                            Show
                                                    </b-button> -->
                    
                                                <b-form-group horizontal :label-cols="4" class="cFormVsel" label="Customer:" >
                                                    <v-select :createOption="newFirm" taggable label="name" v-model="customer" :options="area" />
                                                </b-form-group>
                                           
                                                <b-form-group horizontal :label-cols="4" class="cFormVsel" label="Contact person:" >
                                                 <v-select :createOption="newPerson" taggable v-model="person" :options="availablePersons?availablePersons:[]"   />
                                                </b-form-group>
                                             
                                            </b-col>
                                            <b-col lg="6" md="12" class="cuestomRow">
                                                <b-form-group horizontal :label-cols="4" class="cFormVsel" label="E-mail:">
                                                <b-row>
                                                <v-select :createOption="insertCustomer(personMail, 'mail', person.id)" taggable v-model="personMail"
                                                v-if="person" :options="person?objToArrFPerson(person.mail, 'mail'):[]" style="padding-left: 16px;width: 83%;"  />
                                                 <b-button class="cForm-inputG" style="width: 12%;" @click="sendMail(person.mail)">Send</b-button>
                                                </b-row>
                                                </b-form-group>
                                             
                                                <b-form-group horizontal :label-cols="4" class="cFormVsel" label="Phone:">
                                                 <v-select :createOption="insertCustomer(personPhone, 'phone', person.id)" taggable v-model="personPhone" v-if="person" :options="person?objToArrFPerson(person.tel, 'phone'):[]"  />
                                                 </b-form-group>
                                              
                                                <b-form-group horizontal :label-cols="4" class="cFormVsel" label="Fax:" >
                                                <v-select :createOption="insertCustomer(personFax, 'fax', person.id)" taggable v-model="personFax" v-if="person" :options="person?objToArrFPerson(person.fax, 'fax'):[]"  />
                                              </b-form-group>
                                           
                                            </b-col>
                                        </b-row>
                                        <hr />
                                        <b-row>
                                            <b-col>
                                                <b-button class="customButton" @click="addSameModal('Offers')">
                                                    Add Offer
                                                </b-button>
                                                <b-button class="customButton" @click="showCommetnts">
                                                    Show comments
                                                </b-button>

                                                  <b-dropdown  text="Link For Workers" class="customDrop">
                                                    <b-dropdown-item  v-for="item in workersForSend" :key="item.id" v-clipboard="'http://it-vision.pro:8081/?#/project/user/'+id+'/'+item.value">{{item.text}}</b-dropdown-item>
                                                  </b-dropdown>

<!--                                                 <b-button class="customButton" @click="addSameModal('Damage Description')">
                                                    Damage Description
                                                </b-button> -->
<!--                                                 <b-button class="customButton">
                                                    Add Invoice
                                                </b-button> -->
                                            </b-col>
                                        </b-row>
                                    </b-container>
<!--                                     Offers
                                    <b-table class="tableProject" striped hover :items="offers.filter(function (val){ if(val.type=='offer') {return val}  })" :fields="fieldsOffer" @row-clicked="inItemClick">
                                        <template slot="offer_number" slot-scope="offer">
                                            {{ offer.item.offer_number }}
                                        </template>
                                        <template slot="status_set" slot-scope="offer">
                                            <b-form inline>
                                                <b-form-select v-model="offer.item.status_set" :options="options" />
                                                <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleOffer(offer.item.status_set)"></i>
                                            </b-form>
                                        </template>
                                        <template slot="delete" slot-scope="offer">
                                            <b-col align-self="center">
                                                <b-link @click="offerDel(offer.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>
                                    </b-table>
                                    Contracts
                                    <b-table class="tableProject" striped hover :items="getContracts(offers)" :fields="fieldsOffer" @row-clicked="inItemClick">
                                        <template slot="offer_number" slot-scope="offer">
                                            {{ offer.item.offer_number }}
                                        </template>
                                        <template slot="status_set" slot-scope="offer">
                                            <b-form inline>
                                                <b-form-select v-model="offer.item.status_set" :options="options" />
                                                <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleOffer(offer.item.status_set)"></i>
                                            </b-form>
                                        </template>
                                        <template slot="delete" slot-scope="offer">
                                            <b-col align-self="center">
                                                <b-link @click="offerDel(offer.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>
                                    </b-table>
                                    Invoices
                                    <b-table class="tableProject" striped hover :fields="fieldsInvoice" :items="invoices" @row-clicked="inItemClickInvoice">
                                       
                                        <template slot="show_details" slot-scope="invoice">
                                            <b-link size="sm" @click.stop="inItemClickCotract(invoice.item.offer_id)" class="butMore">
                                                {{ShowContract(invoice.item.offer_id)}}
                                            </b-link>
                                        </template>
                                        <template slot="offer_number" slot-scope="invoice">
                                            {{ invoice.item.inoice_number }}
                                        </template>
                                        <template slot="status_set" slot-scope="invoice">
                                            <b-form inline>
                                                <b-form-select v-model="invoice.item.status_set" :options="options" />
                                                <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleOffer(invoice.item.status_set)"></i>
                                            </b-form>
                                        </template>
                                        <template slot="delete" slot-scope="offer">
                                            <b-col align-self="center">
                                                <b-link @click="offerDel(item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template> @row-clicked="inItemClickInvoice"
                                    </b-table>
                                     Damage Description
                                     <b-table class="tableProject" striped hover :items="damages" :fields="fieldsDamages" @row-clicked="inItemClickDamage">
                                    </b-table> -->

<!-- //////////////////////////////////////////// -->

                                   <div v-for="name in types_for_tables" v-if="getItems(name.type)!=''">
                                   {{name.type}}

                                    <b-table stacked="lg" hover  class="tableProject" small  :items="getItems(name.type)"
                                    :fields="(name.type=='Damage Description')?fieldsTableD:fieldsTable" @row-clicked="inItemGetData">

                                        <template slot="number" slot-scope="it">
                                             <div v-if="it.item.number.split(' ')[1]">
                                             <b-link @click.stop="findRow(it.item.number, name.type)" class="fa fa-clone fa-w-16" />

                                               {{
                                                countDigitals(it.item.number.split(' ')[1])
                                                }}

                                                <!-- {{
                                                it.item.number.split(' ')[0].split('-')[0]
                                                +'-'+countDigitals(it.item.number.split(' ')[1])
                                                +'-'+it.item.number.split(' ')[0].split('-')[2]
                                                }} -->

                                           </div>
                                             <div v-else>{{ it.item.number.split(' ')[0] }}</div>
                                        </template>

                                        <template slot="delete" slot-scope="it">
                                            <b-col>
                                                <b-link @click.stop="offerDel(it.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>

                                      <template slot="status_set" slot-scope="it" >
                                          <line-chart :datas="dataCharts(it.item)" v-if="name.type=='Invoices'"
                                            :width="150"  :height="20" style="margin-left: -15px;">
                                          </line-chart>
                                          <b-form inline v-else>
                                                <b-form-select v-model="it.item.status_set" @change="updateItem($event, 'status_set', it.item.id)"
                                                class="w-100" :style="computeStyleOffer(it.item.status_set)">
                                                  <option v-for="opt in options" :style="computeStyleOffer(opt.text)">
                                                  {{opt.text}}
                                                  </option>
                                                </b-form-select>
                                            </b-form>
                                      </template>
                                    </b-table>
                                  </div>
<!-- //////////////////////////////////////////// -->
                                </container-body>
                            </container>
                        </b-tab>
                        <b-tab style="padding:0px;"  >
                           <template v-slot:title>
                            <div style="width:100%" v-b-toggle.priceMenu >Price List</div>
                          </template>
                           <price :selectedTransfer="partx" :type="tmp.typeOfHead"></price>
                        </b-tab>
                        <b-tab title="Docs">
                            <container>
                                <container-body>
                                <b-row>
                                  <b-col cols="2">
                                    <b-link v-b-toggle.generalDocs class="butMore">
                                      <span class="when-opened">- Documents</span>
                                      <span class="when-closed">+ Documents</span>
                                    </b-link>
                                </b-col>
                                </b-row>
                                <br/>
                                <b-collapse id="generalDocs">
                                    <b-table :items="responseFiles" :fields="fieldsDocs" stacked="lg" hover  class="tableProject" small >
                                        <template slot="type" slot-scope="row">
                                            <b-link size="sm" @click.stop="row.toggleDetails" :class="'butMore '">
                                                <i style="font-size:14px" :class="row.detailsShowing ? 'far fa-file' : 'fa fa-file-alt'" v-if="((row.item.name=='Orders') || (row.item.name=='Offers') || (row.item.name=='Invoices') || (row.item.name=='Damage Description'))"></i>
                                                <i style="font-size:14px" :class="row.detailsShowing ? 'far fa-file' : 'fa fa-file-pdf'" v-else-if="row.item.name.includes('.pdf')"></i>
                                                <i style="font-size:14px;color:#fecb53;" :class="row.detailsShowing ? 'fa fa-folder-open' : 'fa fa-folder'" v-else></i>
                                            </b-link>
                                        </template>
                                        <template slot="name" slot-scope="row">
                                            {{row.item.name.replace('.pdf', '')}}
                                        </template>
 <!--                                        <template slot="section" slot-scope="row">
                                            {{row.item.name.replace('.pdf', '')}}
                                        </template> -->
                                        <template slot="row-details" slot-scope="row">
                                            <iframe type="iframe1" :style="'width:100%;height:'+(30.1*row.item.pages+1.5)+'cm'" frameborder="0" :name="'ifr'+row.index" class="iframeclass" src="" :onload="loadDocToFrame(row.index)" v-if="row.item.gallery==undefined">
                                            </iframe>
                                            <div v-viewer class="images clearfix" v-else>
                                                <template v-for="image in row.item.gallery">
                                                    <img :src="image" class="image" :key="image" height="200px">
                                                </template>
                                            </div>
                                            <form :target="'ifr'+row.index" :action="(row.item.html!='file') ? '/pdf1':'/pdf2'" method="post" :ref="'ifrForm'+row.index">
                                                <input type="hidden" name="html" :value="row.item.id" style="display:none" v-if="(row.item.html!='file')" />
                                                <input type="hidden" name="id" :value="row.item.id" v-else />
                                            </form>
                                        </template>
                                    </b-table>
                                     </b-collapse>
                                     <br/>
                                  <b-row >
                                    <b-col cols="6">
                                      <b-form-group horizontal label-cols="7" label="Images group by:">
                                          <b-select class="customButton" v-model="selectedDamageImages" :options="labelForFieldsImages()"  />
                                      </b-form-group>
                                    </b-col>
                                  </b-row>
                                    <br/>

                                     <b-table v-viewer :items="domage_images" :fields="fieldsImages" stacked="lg" hover  class="tableProject" small v-if="selectedDamageImages=='Image'">
                                      <template slot="id" slot-scope="row">
                                        <img :src="row.item.id" class="image" height="200px">
                                      </template>
                                    </b-table>

 


                                    <div v-else  v-for="item in groupByFild(selectedDamageImages)">

                                    <b-link v-b-toggle="item.name" class="butMore">
                                      <span class="when-opened">- {{item.name}}</span>
                                      <span class="when-closed">+ {{item.name}}</span>
                                    </b-link>
                                    <b-collapse :id="item.name">
                                      <b-table  v-viewer :items="item.table" :fields="fieldsImages" stacked="lg" hover
                                      class="tableProject" small >
                                        <template slot="id" slot-scope="row">
                                          <img :src="row.item.id" class="image" height="200px">
                                        </template>
                                      </b-table>
                                    </b-collapse>
                                    </div>
                                   
                                </container-body>
                                <b-container>
                                    <b-collapse id="dropDoc">
                                        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="dropzoneOptions" v-on:vdropzone-sending="sendingEvent" v-on:vdropzone-success="fsadd">
                                        </vue-dropzone>
                                    </b-collapse>
                                    <div style="background-color:#ced4da">
                                        <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal; With:100%" v-b-toggle="'dropDoc'">
                                            <span class="when-closed"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder" aria-hidden="true"></i></span>
                                            <span class="when-opened"><i style="font-size:14px;color:#fecb53;" class="fa fa-folder-open" aria-hidden="true"></i></span>
                                        </b-link>
                                    </div>
                                </b-container>
                            </container>
                        </b-tab>


<!-- <b-tab title="Google" @click="google=true">
                    <container>
                                <container-body> -->
       <!--                                      <iframe 
    src="/google?link=https://www.google.ru/search?q=test&oq=test"
    style="
      position:relative;
      top:0;
      height:70vh;
      width:100%;
      overflow: yes;
      resize: vertical;
    border-bottom-width: 5px; /* Толщина линии внизу */
    border-bottom-style: solid; /* Стиль линии внизу */
    border-bottom-color: #000; /* Цвет линии внизу */



    "
    frameborder="0"
    name="myFrame"
/>  -->

<!--   <div class="iframe-container">
    <iframe src="https://benmarshall.me/" frameborder="0"></iframe>
  </div> -->
<!-- <multipane class="horizontal-panes" layout="horizontal" v-if="google">
<iframe class="pane" :style="{ height: '70%'}"
    src="https://www.baer-gs.de/"
    style="
      width:100%;
      height: 100hv;
      overflow: auto;
    "
    name="result" 
/>
  <multipane-resizer>
      <b-input v-model="q" style="margin:20px;width:95%;"></b-input>
</multipane-resizer>
<iframe class="pane" :style="{ flexGrow: 1}"
    :src="'/google?link=https://www.google.ru/search|q='+q"
    style="
      width:100%;
      height: 100hv;
      overflow: auto;
    "
    name="myFrame" 
/>
</multipane> -->
<!--  <iframe
    src="https://www.wikipedia.org/"
    frameborder="0"
    style="
    position:relative;
    bottom:0hv !important;
    height:30vh;width:100%;
    "
    name="myFrame"

/>  -->

<!-- <iframe
    src="https://www.wikipedia.org/"
    style="
      width:100%;
      height: 100hv;
      overflow: auto;
    "
    name="result" 
/> -->

 

<!--                                 </container-body>
</container>
                        </b-tab> -->


                    </b-tabs>
                </b-card>
                <b-card no-body class="gs-container">
                    <b-tabs card>
                        <b-tab title="Edit">
                            <container>
                                <container-header v-show="tmp.number != null">
                                    <b-row align-h="end">
                                        <b-container>
                                            <b-col cols="auto" class="cuestomRow">
                                                <b-button size="sm" class="cForm-inputG" variant="outline-secondary" @click="addPdfs=false, printOffer()">
                                                    <i class="fas fa-print">
                                                    </i>
                                                </b-button>
                                            </b-col>
                                        </b-container>
                                    </b-row>
                                </container-header>
                                <container-body>


                          <vue-editor :value="project.other" @input="updateProject('other', $event)" v-if="(tmp.number==null)" style="height:82vh">
                          </vue-editor>
                                    <!-- <b-container v-show="tmp.number != null">  <b-container> -->
                                    <b-container v-show="tmp.number != null">
                                                    <b-input type="text" hidden v-model="tmp.typeOfHead" />
                                        <b-row>
                                            <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" class="cuestomRow">
                                              <b-row>
                                              <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >
                                                <b-form-group  horizontal :label-cols="4" class="cForm" :label="tmp.typeOfHead+':'">
                                                    <b-form-input :state="null" disabled type="text"
                                                    :value="(tmp.typeOfHead=='Invoices')?countDigitals(tmp.number.split(' ')[1]):tmp.number" placeholder="Enter offer number" class="cForm-input"

                                                    @focus.native="changeDisable('f', 'ofnumber', tmp.id)" @blur.native="changeDisable('b', 'ofnumber', tmp.id)" :id="'ofnumber'+tmp.id"  />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('ofnumber', tmp.id)" :target="'ofnumber'+tmp.id">
                                               {{disablefildUser('ofnumber', tmp.id)}}
                                                 </b-tooltip>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Document:">
                                                    <b-form-input :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofdate', tmp.id)" :state="null" type="date" @change="updateItem($event, 'date', tmp.id)"
                                                    :value="tmp.date" placeholder="Enter date" class="cForm-input" 
                                                    @focus.native="changeDisable('f', 'ofdate', tmp.id)" @blur.native="changeDisable('b', 'ofdate', tmp.id)" :id="'ofdate'+tmp.id" 
                                                    />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('ofdate', tmp.id)" :target="'ofdate'+tmp.id">
                                               {{disablefildUser('ofdate', tmp.id)}}
                                                 </b-tooltip>
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Event" v-if="tmp.type=='Damage Description'">
                                                    <b-form-input :state="null" type="date" :disabled="disablefild('evdate', tmp.id)"
                                                    :value="tmp.dateEvent" @change="updateItem($event, 'dateEvent', tmp.id)" class="cForm-input" 

                                                      @focus.native="changeDisable('f', 'evdate', tmp.id)" @blur.native="changeDisable('b', 'evdate', tmp.id)" :id="'evdate'+tmp.id" 
                                                    />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('evdate', tmp.id)" :target="'evdate'+tmp.id">
                                               {{disablefildUser('evdate', tmp.id)}}
                                                 </b-tooltip>
                                              </b-col>
                                              <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Place:">
                                                   <b-form-input id="place" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofplace', tmp.id)" :state="null" type="text" @change="updateItem($event, 'place', tmp.id)"
                                                    :value="tmp.place" placeholder="Enter place" class="cForm-input"


                                                     @focus.native="changeDisable('f', 'ofplace', tmp.id)" @blur.native="changeDisable('b', 'ofplace', tmp.id)" :id="'ofplace'+tmp.id"  />


                                                </b-form-group>
                                                 <b-tooltip triggers="none" :show="disablefild('ofplace', tmp.id)" :target="'ofplace'+tmp.id">
                                               {{disablefildUser('ofplace', tmp.id)}}
                                                 </b-tooltip>

<b-form-group horizontal :label-cols="4" class="cForm" label="Order:">
                                                    <b-form-input id="other" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofother', tmp.id)" :state="null" type="text" @change="updateItem($event, 'other', tmp.id)"
                                                    :value="tmp.other" placeholder="Enter number" class="cForm-input" 

                                                    @focus.native="changeDisable('f', 'ofother', tmp.id)" @blur.native="changeDisable('b', 'ofother', tmp.id)" :id="'ofother'+tmp.id" 
                                                    />
                                                </b-form-group>
                                                 <b-tooltip triggers="none" :show="disablefild('ofother', tmp.id)" :target="'ofother'+tmp.id">
                                               {{disablefildUser('ofother', tmp.id)}}
                                                 </b-tooltip>

                                                 <b-form-group horizontal :label-cols="4" class="cForm" label="Insurance:" v-if="(tmp.type=='Damage Description')">
                                                    <b-form-input id="insurance" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofinsurance', tmp.id)" :state="null" type="text" @change="updateItem($event, 'insurance_number', tmp.id)"
                                                    :value="tmp.insurance" placeholder="Enter insurance namber" class="cForm-input" 
                                                    @focus.native="changeDisable('f', 'ofinsurance', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance', tmp.id)" :id="'ofinsurance'+tmp.id" 
                                                    />
                                                </b-form-group>
                                                 <b-tooltip triggers="none" :show="disablefild('ofinsurance', tmp.id)" :target="'ofinsurance'+tmp.id">
                                               {{disablefildUser('ofinsurance', tmp.id)}}
                                                 </b-tooltip>
                                               

                                              </b-col>
                                               <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >
                                                 <b-form-group horizontal :label-cols="4" class="cForm" label="Inspection&nbsp;date:" v-if="tmp.type=='Damage Description'">
                                                    <b-form-input :state="null" type="date"
                                                    :value="tmp.dateInspect" @change="updateItem($event, 'dateInspect', tmp.id)" class="cForm-input"

                                                      :disabled="disablefild('ofdateInspect', tmp.id)"

                                                     @focus.native="changeDisable('f', 'ofdateInspect', tmp.id)" @blur.native="changeDisable('b', 'ofdateInspect', tmp.id)" :id="'ofdateInspect'+tmp.id" 

                                                     />
                                                </b-form-group>
                                                 <b-tooltip triggers="none" :show="disablefild('ofdateInspect', tmp.id)" :target="'ofdateInspect'+tmp.id">
                                               {{disablefildUser('ofdateInspect', tmp.id)}}
                                                 </b-tooltip>

                                              <b-form-group horizontal :label-cols="4" class="cForm" label="Insurance:" v-if="(tmp.type!='Damage Description')">
                                                    <b-form-input id="insurance" :state="null" type="text" @change="updateItem($event, 'insurance_number', tmp.id)" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofinsurance2', tmp.id)"
                                                    :value="tmp.insurance" placeholder="Enter insurance namber" class="cForm-input" 

                                                     @focus.native="changeDisable('f', 'ofinsurance2', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance2', tmp.id)" :id="'ofinsurance2'+tmp.id" 

                                                    />
                                                </b-form-group>
                                                <b-tooltip triggers="none" :show="disablefild('ofinsurance2', tmp.id)" :target="'ofinsurance2'+tmp.id">
                                               {{disablefildUser('ofinsurance2', tmp.id)}}
                                                 </b-tooltip>

<b-button class="customButton" @click="addGropuDamage" v-if="(tmp.type=='Damage Description')">
                                        Add Group
</b-button>
<b-button class="customButton" @click="worker" v-if="(tmp.type=='Damage Description')">
                                        Workers
</b-button>

                                              </b-col>
                                          <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12"  v-if="(tmp.type=='Damage Description')">
                                                <b-form-group horizontal :label-cols="4" class="cForm" label="Examining&nbsp;worker:">
                                                   <b-form-select type="text" @change="updateItem($event, 'ExamWorker', tmp.id)"
                                                   :value="tmp.worker" :options="workers"
                                                   style="padding:0px;padding-left:2px;" class="cForm-input" />
                                                </b-form-group>

                                              </b-col>

                                              </b-row>
                                            </b-col>

                                            </b-form-row>


                                         <b-col lg="6" md="12" class="cuestomRow" v-if="tmp.type!='Damage Description'">
           <b-form-row>
              <b-col cols="4"  class="cForm-input">
                 Discont:
              </b-col>
              <b-col cols="3">
                 <b-input-group class="cForm-input">
                    <b-input id="disc" type="number" :disabled="tmp.typeOfHead=='Invoices'" v-model="discP" :state="null" 
                       placeholder="Summa&nbsp;of&nbsp;Percent" @change="discOfPercent();updateProjectTaxs();" class="cForm-input"/>
                    <b-input-group-append >
                       <div class="input-group-text lablelInInput" @click="butDiscPerc = (butDiscPerc == '%' ? 'P' : '%'); discOfPercent();updateProjectTaxs();">{{butDiscPerc}}</div>
                    </b-input-group-append>
                 </b-input-group>
              </b-col>
              <b-col cols="5">
                 <b-input-group class="cForm-input">
                    <b-input disabled id="sop" v-model="disc"  :state="null"  type="text"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input text-right" />
                         <b-input-group-append >
                            <div class="input-group-text lablelInInput">€</div>
                        </b-input-group-append>  
                 </b-input-group>
              </b-col>
           </b-form-row>
           <b-form-group horizontal :label-cols="7" class="cForm" label="Netto:" label-for="netto">
              <b-input-group  class="cForm-input">
                 <b-form-input id="netto" v-model="netto" :state="null"  type="text" 
                    placeholder="Enter netto" disabled class="cForm-input text-right" />
                    <b-input-group-append >
                        <div class="input-group-text lablelInInput">€</div>
                    </b-input-group-append>  
              </b-input-group>
           </b-form-group>
           <b-form-row>
              <b-col cols="3" class="cForm-input">
                 Tax:
              </b-col>
              <b-col cols="1" class="cForm-input" >
                 <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'" @click="saveCol($event)" :disabled="tmp.typeOfHead=='Invoices'">
                    <span class="when-closed">+</span>
                 </b-link>
              </b-col>
              <b-col cols="3">
                 <b-input-group class="cForm-input">
                    <b-input id="taxP" :disabled="tmp.typeOfHead=='Invoices'" v-model="taxP" :state="null"  type="number" @change="discOfPercent();updateProjectTaxs();"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input " />
                        <b-input-group-append ><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                 </b-input-group>
              </b-col>
              <b-col cols="5">
                 <b-input-group  class="cForm-input">
                    <b-input disabled id="tax" v-model="tax" :state="null"  type="text"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input text-right" />
                        <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                 </b-input-group>
              </b-col>
           </b-form-row>
           <b-collapse style="width:100%" id="addtax" v-model="addtaxColapse">
              <b-form-row>
                 <b-col cols="3"  class="cForm-input calttax">
                    Tax:
                 </b-col>
                 <b-col cols="1"  class="cForm-input">
                    <b-link style="text-decoration: none; font-weight: normal;" v-b-toggle="'addtax'"  @click="saveCol" :disabled="tmp.typeOfHead=='Invoices'">
                       <span class="when-opened">-</span>
                    </b-link>
                 </b-col>
                 <b-col cols="3">
                    <b-input-group   class="cForm-input">
                       <b-input v-model="taxPDub" :disabled="tmp.typeOfHead=='Invoices'" :state="null"  type="number" @change="discOfPercent();updateProjectTaxs();"
                          placeholder="Summa of Percent" class="cForm-input " />
                                   <b-input-group-append ><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                    </b-input-group>
                 </b-col>
                 <b-col cols="5">
                    <b-input-group  class="cForm-input">
                       <b-input disabled v-model="taxDub" disabled :state="null"  type="text"
                          placeholder="Summa of Percent" class="cForm-input text-right" />
                          <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                    </b-input-group>
                 </b-col>
              </b-form-row>
           </b-collapse>
           <b-form-group horizontal :label-cols="7" class="cForm" label="Brutto:" >
              <b-input-group  class="cForm-input">
                 <b-form-input v-model="brutto" :state="null"  type="text"
                    placeholder="Enter brutto" disabled class="cForm-input text-right" />
                   <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
              </b-input-group>
           </b-form-group>
        </b-col>
                                        </b-row>
                                        <!-- ---------------------------------------------- ------------------------- -->
                                        <calc-table-group v-model="partx" :id="tmp.id" :type="tmp.type" :butDiscPerc="butDiscPerc" :looks="looks"
                                        :responseFiles="responseFiles" :addtaxColapse="addtaxColapse" :opt='types_for_tables' :tmp="tmp"  v-on:changeSum="discOfPercent()" 
                                        :workers="workers" :funcStop="funcStop" :loadDamages="loadDamages" v-if="tmp.type!='Damage Description'">
                                        </calc-table-group>
<br/><br/>


                     
   
      <draggable v-model="loadDamages" :element="'div'" v-if="tmp.type=='Damage Description'"
      :options="{handle:'.handleTitle', group:'a', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="drag=false" >
                          <b-row fluid v-for="(damage, index) in loadDamages" 
                          :class="damage.up?'handleTitle table-dark':'handleTitle'" :key="damage.id">
 
                               <b-col cols="12">
                    <b-link v-b-toggle="'damage' + damage.id" class="butMore" style="width:100%">
                       <span class="when-opened">- </span>
                       <span class="when-closed">+ </span>
                    </b-link>
                    <i class="fas fa-dot-circle" style="font-size:12px" @click="damage.up=damage.up?false:true"></i> 
                    <span contenteditable="true" @blur="damageToBase('name', $event.target.innerText, damage.id)" @click.pervent.stop>
                        {{damage.name}}
                    </span>
                               </b-col>
                               <!-- <img :src="image" class="image mx-auto" :key="image" height="200px"> -->
                               

                               <b-collapse :id="'damage'+damage.id" style="width:98%;">
                                <draggable v-model="damage.images" :element="'div'" :options="{handle:'.handle', group:'b', animation:150}"
                                  :no-transition-on-drag="true" >
                                  <b-row v-for="(image, index) in damage.images" class="handle" :key="image.id">
                                    <b-col cols="1" class="text-center">
                                      {{(index+1)}}.
                                    </b-col>
                                    <b-col cols="5" class="text-center border" >
                                      <b-img style="padding-top:5px;padding-bottom:5px;max-height:200px;" :src="'/image_damage?id='+image.id"></b-img> 
                                    </b-col>
                                    <b-col cols="6">
                                      <div>{{image.file_name}}</div>
                                      <textarea style="padding-top:10px;height:80%;width:100%" :value="image.desc" @change="damageToBase('imageDesc', $event.target.value, image.id)" ></textarea>
                                    </b-col>
                                  </b-row>
                                 </draggable>
                                 <br>
                                 <b-row class="justify-content-md-center">
                                 <b-col cols="11" style="text-align:center">
                                </b-col>
                              </b-row>
                              

<b-row v-for="(task, index) in damage.tasks" class="border" :key="task.id" align-v="center">
                                    <b-col cols="1" class="text-center">
                                      {{(index+1)}}.
                                    </b-col>
                                    <b-col cols="3"  style="padding:0px">
    <VueCtkDateTimePicker style="padding:0px"
    format="YYYY-MM-DD H:mm" @change="update_task($event, 'data_time_start', task.id)" :value="task.data_time_start" no-label 
    input-size="sm" label="From:" minute-interval="10" >
    </VueCtkDateTimePicker>
    <VueCtkDateTimePicker style="padding:0px"
    format="YYYY-MM-DD H:mm" @change="update_task($event, 'data_time_end', task.id)" :value="task.data_time_end" no-label 
    input-size="sm" label="To:" minute-interval="10" >
    </VueCtkDateTimePicker>
                                    </b-col>
                                <b-col cols="2" class="text-center" v-if="task.data_time_end==null">
                                   <b-button @click="taskStop(task.id)" >    
                                    {{ difTime(task.data_time_start, 'l') }}
                                    </b-button>
                                  </b-col>
                                    <b-col cols="2" v-else class="text-center">
                                     {{ difTimeFinish(task.data_time_start, task.data_time_end, 's') }}
                                    <br>
                                    {{ difTimeFinish(task.data_time_start, task.data_time_end, 'l') }}
                                    </b-col>
                                    <b-col cols="5" class="text-center" style="padding:0px">
                                    <textarea style="padding-top:10px;height:100%;width:100%"
                                        @change="update_task($event.target.value, 'name', task.id)" :value="task.name" rows="2">
                                    </textarea>
                                    </b-col>
                                  <b-col cols="1" class="text-center">
       <b-form-checkbox class="withoutPad" :checked="task.workers!=null"
       plain style="margin: 0px;" :title="task.workers" @change="workersToTask(task.id, $event)"
        />
                                  </b-col>
                                  </b-row>
<b-row>
  <b-col cols="4">
  </b-col>
  <b-col cols="2" class="text-center">
    {{summHour(damage.tasks, 's')}}
  </b-col>
  </b-col>
  <b-col cols="6">
  </b-col>
</b-row>

<b-button @click="addTaskModal(damage.id)">Add task</b-button><br>
     <br/>    <br/> 

                              </b-collapse>
                            
                                                               <!-- <img :src="image" class="image mx-auto" :key="image" height="200px"> -->

           <br/>   
                          </b-row>
                         
                </draggable>
                                    </b-container>
                                </container-body>
                                <container-footer v-if="(generalComments==false)">
                                    <b-container>
                                        <b-collapse id="editor">
                                            <vue-editor id="refCommentOfTable" ref="refCommentOfTable" v-model="commentOfTable">
                                            </vue-editor>
                                        </b-collapse>
                                    <b-collapse id="drop" v-if="tmp.type=='Damage Description'">
                                        <vue-dropzone ref="myVueDropzone" id="dropzone" :options="sendToGroupForDamages" v-on:vdropzone-sending="sendingImageInGroupForDamages" v-on:vdropzone-success="fsadd">
                                        </vue-dropzone>
                                    </b-collapse>
                                        <b-input-group class="cForm-input">
                                            <b-input-group-prepend>
                                                <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal;" v-b-toggle="'editor'">
                                                    <span class="when-closed">+</span>
                                                    <span class="when-opened">-</span>
                                                </b-link>
                                                <b-link class="input-group-text lablelInInput" style="text-decoration: none;font-weight: normal; With:100%" v-b-toggle="'drop'" v-if="tmp.type=='Damage Description'">
                                                    <span class="when-closed">+</span>
                                                    <span class="when-opened">-</span>
                                                </b-link>
                                            </b-input-group-prepend>
                                            <b-form-input id="netto" :state="null" type="text"
                                             disabled class="cForm-input text-right" :value="(tmp.type=='Damage Description')?allhours('n'):allSumms()" />
                                            <b-input-group-append>
                                                <div class="input-group-text lablelInInput" v-if="tmp.type!='Damage Description'">€</div>
                                                <div class="input-group-text lablelInInput" v-else>&#8986;</div>
                                            </b-input-group-append>
                                        </b-input-group>
                                        </b-form-group>
                                    </b-container>
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
        id: String
    },
    data() {
        return {
          mailSelect:null,
          countCall:0,
          project_id:null,
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
            fieldsDocs: [
                {   
                    key: 'type',
                    label: 'type',
                    sortable: true
                },
                {
                    key: 'name',
                    label: 'name',
                    sortable: true
                },
                {
                    key: 'group',
                    label: 'section',
                    sortable: true
                },
                {
                    key: 'number',
                    sortable: true
                },
                {
                    key: 'date',
                    sortable: true
                },
                {
                    key: 'added',
                    sortable: true
                }
            ],
            fieldsImages: [
                {   
                    key: 'id',
                    label: 'Image',
                    sortable: true
                },
                {
                    key: 'file_name',
                    label: 'file_name',
                    sortable: true
                },
                {
                    key: 'date',
                    label: 'date',
                    sortable: true
                },
                {
                    key: 'user',
                    label: 'user',
                    sortable: true
                },
                {
                    key: 'from',
                    label: 'from',
                    sortable: true
                },
                {
                    key: 'type',
                    label: 'type',
                    sortable: true
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
                    label: 'Order'
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
                insurance_number: {
                    label: 'Insurance',
                    sortable: true
                },
                other: {
                    label: 'Order Number',
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

                delete: {
                    // label: "&#128465;",
                    // class: 'text-center'
                }
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

                delete: {
                    label: "&#128465;",
                    class: 'text-center'
                }
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
                delete: {
                    label: 'Delete',
                }
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
                },
                {
                    value: 'AsbestosRemoval',
                    text: 'Asbestos Removal'
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
                        testingCode: null,
                        looks: []
        } //return
    }, //data

    computed: {
        availablePersons() {
            if(this.customer){
                var persons = this.customer.persons.filter(function(elem, index, self) {
                    return index === self.indexOf(elem);
                })
              return  persons
            }else{
                return  false
            }
            
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
    sendmail(){
         axios.get('/send_mail', {
          params: {
            'from': this.$security.table.account.mail,
            'to': this.mailSelect.join()
          }
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
      disablefildUser(fild, id){
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
        axios.get('/changeDisableTableSub', {
          params: {
            type_operation: type_operation,
            fild: fild,
            id: id,
            'user': this.$security.account['first_name']+'_'+this.$security.account['second_name']
          }
        })
        if (type_operation == 'f'){
          setTimeout(()=>{

              this.$refs.unfocus.focus()

          }, 15000);
        }
},


    saveCol(){
      this.addtaxColapse =this.addtaxColapse?false:true
      this.taxPDub=0,
      this.taxDub=0,
         this.discOfPercent(),
         this.updateProjectTaxs()
    },
    
    copyTestingCode (workerId) {
          this.testingCode = workerId
          let testingCodeToCopy = document.querySelector('#testing-code')
          testingCodeToCopy.setAttribute('type', 'text')    // 不是 hidden 才能複製
          testingCodeToCopy.select()

          try {
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            alert('Testing code was copied ' + msg);
          } catch (err) {
            alert('Oops, unable to copy');
          }

          /* unselect the range */
          testingCodeToCopy.setAttribute('type', 'hidden')
          window.getSelection().removeAllRanges()
        },


      groupByFild(fild){
        var tables = []

        this.domage_images.forEach((v)=>{
          // console.log(v)
            var date = v.date
            var user = v.user
            var file_name = v.file_name
            var id = v.id
            var from = v.from
            var type = v.type

          if (fild == 'date'){
            var nameOfDate = v.date.split(' ')[0]
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'file_name':file_name}]})
            }else{
                tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'from':from, 'type':type, 'date':date.split(' ')[1]})
            }
          }
          if (fild == 'file_name'){
            var nameOfDate = v.file_name
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'date':date}]})
            }else{
                tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'date':date, 'from':from, 'type':type, 'date':date.split(' ')[1]})
            }
          }
          if (fild == 'user'){
            var nameOfDate = v.user
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'date':date}]})
            }else{
                tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'date':date, 'from':from, 'type':type, 'date':date})
            }
          }

        })
        return tables
      },
      labelForFieldsImages(){
        var labelsArr = [];
        
        this.fieldsImages.forEach((v)=>{
            labelsArr.push(v.label);
        })
        return labelsArr
      },
      getdomageImages(){
       // console.log(this.project.number)
       axios.get('/domage_images_sub', {
          params: {
            id: this.id,
            project: this.project.number
          }
        }).then(response => {
        this.domage_images =  response.data

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
      axios.get('/workers_task_sub', {
        params: {
          workers: event?this.selectedWorkers.join():'Null',
          id: id
        }
      })
    },
    updateItem(val, type, id){
      // alert()
      // if (this.updatePojectFunc==0){
        axios.get('/update_item_from_sub', {
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
      axios.get('/task_time_damage_sub', {
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
          axios.get('/update_task_sub', {
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
        // updateProjectAfter(){
        //     this.$options.sockets.onmessage = (data) => (data.data=='getSubDetail') ? this.getSubDetail(1): ''
        // },
        updateProject(fild, newData){
        // delete this.$options.sockets.onmessage;
        // console.log('?')
        axios.get('/updatSub', {params: {
                id: this.id,
                date: newData,
                fild: fild
        }}).then(response => {

            // this.updatePojectFunc=0

        })
        },
        updateProjectTaxs(){
          if (this.tmp.id!=null){
            axios.get('/updateProjectTaxsSub', {params: {
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
                // console.log('----------------------')
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
                      // console.log(sval.alttax)
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
           // console.log('1')
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
                    // console.log('2')
                    // console.log(this.project.number)
                    this.docs = (this.docs != response.data)?response.data:this.docs
                    axios.get('/files', {
                    params: {
                        id: this.project.number
                    }
                }).then(response => {
          // console.log('3')
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
var mergedArr = rows1.concat(rows2.concat(rows3))
this.files = (this.files != response.data)?response.data:this.files
var addFiles = []
// console.log(mergedArr)
mergedArr.forEach((item)=>{
axios.get('/get_tables_sub', {
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
                  if(val.name.split('.')[1] == 'pdf'){
                    if(v.parts!=undefined){
                      if (val.group.split(',').length>1){
                        ret = 0
                        var subval = []
                        val.group.split(',').forEach((valGroup)=>{
                          subval = JSON.parse(JSON.stringify(val))
                          subval.group = valGroup
                          if(subval.group==v.parts.id){
                            subval.group = v.parts.part_name + ' from ' + item.type
                            // console.log(subval.group)
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
                     if (ret == 1) {return val.name.split('.')[1] == 'pdf' }
                  })

                  addgroup = []
                  if(addFiles.length!=0) files = files.concat(addFiles)
                  
                  // console.log(addFiles, files)

                  files1 = files.filter((file, i) => {
                  
                  if(file.name.split('.')[1] != 'pdf'){
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
                // this.$socket.send('getFiles')

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
        },
        sendingImageInGroupForDamages(file, xhr, formData) {
          var groups=[]
          this.loadDamages.forEach((v)=>{
            if(v.up==true){
              groups.push(v.id)
            }
          })
            xhr.setRequestHeader('X-Group-Id', groups.join());
        },

        addPdf() {
            this.addPdfs = true
            this.$refs.printOffer.hide()
            setTimeout(() => {
                this.$refs.preForm.submit()
                setTimeout(() => {
                  this.docs2files()
                  }, 100);     
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
        axios.get('/table_data_sub', {
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

        axios.get('/invoice_data_table_sub', {
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
                      axios.get('/add_part_form_price_sub', {
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
    axios.get('/add_group_damage_sub', {
        params: {
          item_id: this.tmp.id
        }
    })
},
worker() {
          this.$refs.worker.show()
        },
damageToBase(fild, event, id){
       axios.get('/damage_update_sub', {
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
               axios.get('/add_same_sub', {
                    params: {
                        add_number: this.project.number,
                        add_insurance_number: '', // this.add_offer.insurance_number
                        add_place: '', // this.add_offer.place
                        add_work: this.add_offer.work, // this.add_offer.work
                        add_comment: '', // this.add_offer.comment
                        add_project_id: this.id,
                        type: this.addhead //this.addhead
                    }
                }).then(response => {
                    axios.get('/sub_detail_new', {
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
                axios.get('/del_item_sub', {
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

var rows = this.getItems('Orders').filter((v)=>{
    if(v.id==intId){
     return v
    }
})
    console.log(rows[0])
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
axios.get('/get_tables_sub', {
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
},

get_person(old, customer_id, person_id, personMail, personPhone, personFax){

console.log('!')

var countValPers=0
axios.get('/person_date', {
  params: {
  old: old
  }
}).then(response => {
  this.area = response.data;
  response.data.forEach((val)=>{


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

         // setTimeout(()=>{

         //                this.updatePojectFunc=0;
         //                // this.discOfPercent();
         //          }, 1000);
    
                             })
                         // })
                     // })
                    
                 // })
                
                     // this.customer.adress='response.data.street;';
                     // this.customer.adress1='response.data.zip++response.data.city;';
                     // this.customer.adress=response.data.street;
                     // this.customer.adress1=response.data.zip+' '+response.data.city;
             

            })
},
get_types_for_tables_f(call){
  axios.get('/get_types_for_tables', {
  }).then(response => {
    this.types_for_tables = response.data;
  });
  if (call=='socket'){
    this.sub_detail_new_f()
  }
},
get_workers_f(){
  axios.get('/get_workers_sub', {
  }).then(response => {
    this.workers = [],
    response.data.forEach((v)=>{
      this.workers.push((v.short_name!=null)?v.short_name:v.name),
      this.workersForSend.push({'value':v.id, 'text':((v.short_name!=null)?v.short_name:v.name)})   
    })
  })
},
sub_detail_new_f(){
  axios.get('/sub_detail_new', {
    params: {
      id: this.id
    }
  }).then(response => {
  
    response.data.filter((v)=>{
      v.netto = this.$options.filters.thousandSeparator(parseFloat(v.netto));
      v.brutto = this.$options.filters.thousandSeparator(parseFloat(v.brutto));
      return v;
    })

    this.items_table = response.data;

    // this.findRow(this.tmp.number, 'Offers')
    if (this.tmp.id!=undefined){
      var item_list = this.items_table.filter((v)=>{
        if (v.type == 'Orders' || v.type == 'Offers'){
          if (v.id == this.tmp.id){
            return v
          }
        }
      })
         this.inItemGetData(item_list[0], 0)

      // console.log(item_list)
    }
// and click
  })
},
getLoocks(){
   axios.get('/getLoocks_sub').then(response => {
      this.looks=[]
      this.looks = response.data
  })


},
project_detail_f(old){
  // console.log('!')
       axios.get('/sub_detail', {
                params: {
                    id: this.id
                }
            }).then(response => {
                 var nuls=3-response.data.id.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        response.data.id='0'+response.data.id
                    }

                    this.project.work = response.data.work,
                    this.project.number = response.data.id+'-'+response.data.project_number_year,
                    //this.project.number = response.data.project_number_year,
                    this.project.date = response.data.date,
                    this.project.street = response.data.street,
                    this.project.city = response.data.city,
                    this.project.zip = response.data.zip,
                    this.project.other = response.data.other,
                    this.project.editor = response.data.first_name + ' ' + response.data.second_name

                      // if(this.customer==null){ //или сменен
                      // console.log(1)
                      var customer_id=response.data.customer_id
                      var person_id=response.data.person_id
                      var personMail=response.data.mail
                      var personPhone=response.data.phone
                      var personFax=response.data.fax
                      this.get_person(old, customer_id, person_id, personMail, personPhone, personFax)
                      // }

this.docs2files()
this.getdomageImages()


            })
},
// get_person_new(){
//          axios.get('/sub_detail', {
//                 params: {
//                     id: this.id
//                 }
//             }).then(response => {
                
//                     // if(this.customer==null){ или сменен
//                       // console.log(this.customer)
//                       var customer_id=response.data.customer_id
//                       var person_id=response.data.person_id
//                       var personMail=response.data.mail
//                       var personPhone=response.data.phone
//                       var personFax=response.data.fax
//                       this.get_person(1, customer_id, person_id, personMail, personPhone, personFax)
//                     // }

//             })
// },
getSubDetail(old){
  if (this.types_for_tables.length==0){
    this.get_types_for_tables_f('native')
  }

  // if (this.items_table.length==0){
    this.sub_detail_new_f()
  // }


  if (this.workers.length==0){
    this.get_workers_f()
  }

  if(this.tmp.number!=null){
    var cliked = this.items_table.filter((val)=>{
      if (val.id==this.tmp.id){
        return val
      }
    })
    this.countCall = this.countCall + 1
    // console.log('inItemGetData', this.countCall)
     this.inItemGetData(cliked[0], 0)
  }

   // if(this.project_id==null){
    this.project_detail_f(old)
    this.project_id=this.id
   // }
}

},

    watch: {
    customer : function (val, oldval) {

    // if (this.updatePojectFunc==0){
//     this.updatePojectFunc=1
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
                        // setTimeout(()=>{
                        //      this.updateProjectAfter()
                        // }, 1000);
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
    // }
    },
     person : function (val, oldval) {
// if (this.updatePojectFunc==0){

   // this.updatePojectFunc=1
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
             // setTimeout(()=>{
             //      this.updateProjectAfter()
             // }, 1000);
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
// }
     },
      personMail : function (val, oldval) {
         // if (this.updatePojectFunc==0){
         //     this.updatePojectFunc=1
  if (this.person!=null){
  if(oldval==null){
   oldval={mail:-1}
  }

  if(val==null){
   val={mail:-1}
  }


              if(this.person.mail.findIndex(x => x.mail == this.personMail)!=-1){
                  this.updateProject('mail', this.person.mail.findIndex(x => x.mail == this.personMail))
                  // setTimeout(()=>{
                  //      this.updateProjectAfter()
                  // }, 1000);
              }

              // else{
              //     this.insertCustomer(val, 'mail', this.person.id, this.person.mail.length)
              // }
 }
//  this.updatePojectFunc=0
// }
      },


      personPhone : function (val, oldval) {
         // if (this.updatePojectFunc==0){
  if (this.person!=null){
  if(oldval==null){
   oldval={tel:-1}
  }

  if(val==null){
   val={tel:-1}
  }
              if(this.person.tel!=undefined && this.person.tel.findIndex(x => x.phone == this.personPhone)!=-1){
                  this.updateProject('phone', this.person.tel.findIndex(x => x.phone == this.personPhone))
                  // setTimeout(()=>{
                  //      this.updateProjectAfter()
                  // }, 1000);
                  }
              //     else{
              //     this.insertCustomer(val, 'phone', this.person.id, this.person.tel.length)
              // }
          }
      // }
      },
      personFax : function (val, oldval) {
        //console.log(this.updatePojectFunc)
        // if (this.updatePojectFunc==0){
        //      this.updatePojectFunc=1
  if (this.person!=null){
  if(oldval==null){
   oldval={fax:-1}
  }

  if(val==null){
   val={fax:-1}
  }


              if(this.person.fax.findIndex(x => x.fax == this.personFax)!=-1){
                  this.updateProject('fax', this.person.fax.findIndex(x => x.fax == this.personFax))
                  // setTimeout(()=>{
                  //      this.updateProjectAfter()
                  // }, 1000);
              }

              // else{
              //     this.insertCustomer(val, 'mail', this.person.id, this.person.mail.length)
              // }
 }
//  this.updatePojectFunc=0
// }
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
        
        this.$socket.send('getSubDetail')
        this.$options.sockets.onmessage = (data) => (data.data=='getSubDetail') ? (this.getSubDetail(1)): ''
        // this.$options.sockets.onmessage = (data) => (data.data=='get_person') ? (this.get_person(1,this.customer.id, this.person.id, this.personMail, this.personPhone, this.personFax)): '' //this.get_person(1)
        this.$options.sockets.onmessage = (data) => (data.data=='get_types_for_sub_tables_f') ? (this.get_types_for_tables_f('socket')): ''
        this.$options.sockets.onmessage = (data) => (data.data=='sub_detail_new_f') ? (this.sub_detail_new_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='get_workers_f') ? (this.get_workers_f()): ''
        // this.$options.sockets.onmessage = (data) => (data.data=='project_detail_f') ? (this.project_detail_f()): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getLoocksSub') ? (this.getLoocks()): ''



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