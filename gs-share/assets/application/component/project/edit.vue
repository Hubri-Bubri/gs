<template>
<div>
<b-button class="customButton btn-outline-secondary" @click="checkInEditor('other')" v-if="(tmp.number==null)"
style="position:relative;left:24px;top: 6px;width:18px;z-index:2;"><i class="fas fa-calculator"></i></b-button>
<span v-show="(disablefildUser('gencooment', id)!='you')" style="position:relative;left:30px;top: 6px;width:18px;z-index:2;" v-if="(tmp.number==null)">{{disablefildUser('gencooment', id)}}</span>

<vue-editor :value="project.other" :editorToolbar="customToolbar"
style="height:82vh;position:relative;top:-20px;z-index:1;" v-if="(tmp.number==null)"
class="text-right"  ref="other"

@focus="changeDisable('f', 'gencooment', id)"
@blur="writecomet();changeDisable('b', 'gencooment', id);"
:id="'gencooment'+id" 
:disabled="disablefild('gencooment', id)?'disabled':false"
/>



                                   <b-container v-show="tmp.number != null">
                                      <b-input type="text" hidden v-model="tmp.typeOfHead" />
                                        <b-row>
                                            <b-col :lg="(tmp.type!='Damage Description')?8:12" md="12" class="cuestomRow">
                                              <b-row>
                                              <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >

                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">{{tmp.typeOfHead}}:</b-col>
                                                  <b-col sm="8" cols="12" >

                                                    <b-form-input :state="null" disabled type="text" :value="

                                                    (tmp.typeOfHead=='Invoices')?(tmp.number.split(' ').length==5)?tmp.number.split(' ')[3]:
                                                    countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[1]:(tmp.typeOfHead=='SUB')
                                                    ?tmp.number.split(' ')[0]:(tmp.typeOfHead=='Sub Invoices')?tmp.number.split(' ')[3]:tmp.number" 

                                                    placeholder="Enter offer number" class="cForm-input"
                                                    @focus.native="changeDisable('f', 'ofnumber', tmp.id)" @blur.native="changeDisable('b', 'ofnumber', tmp.id)" :id="'ofnumber'+tmp.id"  />
                                                  </b-col>
                                                </b-form-row>

                                                <b-tooltip triggers="none" :show="disablefild('ofnumber', tmp.id)" :target="'ofnumber'+tmp.id">
                                               {{disablefildUser('ofnumber', tmp.id)}}
                                                 </b-tooltip>

                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Document:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofdate', tmp.id)" :state="null" type="date" @change="updateItem($event, 'date', tmp.id)"
                                                    :value="tmp.date" placeholder="Enter date" class="cForm-input" 
                                                    @focus.native="changeDisable('f', 'ofdate', tmp.id)" @blur.native="changeDisable('b', 'ofdate', tmp.id)" :id="'ofdate'+tmp.id" />
                                                  </b-col>
                                                </b-form-row>

                                                <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Place:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input id="place" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofplace', tmp.id)" :state="null" type="text" @change="updateItem($event, 'place', tmp.id)"
                                                    :value="tmp.place" placeholder="Enter place" class="cForm-input"
                                                     @focus.native="changeDisable('f', 'ofplace', tmp.id)" @blur.native="changeDisable('b', 'ofplace', tmp.id)" :id="'ofplace'+tmp.id"  />
                                                  </b-col>
                                                </b-form-row>
                                                  
                                                <b-tooltip triggers="none" :show="disablefild('ofdate', tmp.id)" :target="'ofdate'+tmp.id">
                                               {{disablefildUser('ofdate', tmp.id)}}
                                                 </b-tooltip>

                                                  <b-form-row v-if="tmp.type=='Damage Description'">
                                                  <b-col sm="4" cols="12" class="cForm">Event:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input :state="null" type="date" :disabled="disablefild('evdate', tmp.id)"
                                                    :value="tmp.dateEvent" @change="updateItem($event, 'dateEvent', tmp.id)" class="cForm-input" 
                                                      @focus.native="changeDisable('f', 'evdate', tmp.id)" @blur.native="changeDisable('b', 'evdate', tmp.id)" :id="'evdate'+tmp.id" 
                                                    />
                                                  </b-col>
                                                </b-form-row>
                                                
                                                <b-tooltip triggers="none" :show="disablefild('evdate', tmp.id)" :target="'evdate'+tmp.id">
                                               {{disablefildUser('evdate', tmp.id)}}
                                                 </b-tooltip>

                                              </b-col>
                                              <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >
                                                 <b-tooltip triggers="none" :show="disablefild('ofplace', tmp.id)" :target="'ofplace'+tmp.id">
                                               {{disablefildUser('ofplace', tmp.id)}}
                                                 </b-tooltip>

                                                 <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Order:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input id="other" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofother', tmp.id)" :state="null" type="text" @change="updateItem($event, 'other', tmp.id)"
                                                    :value="tmp.other" placeholder="Enter number" class="cForm-input" 
                                                    @focus.native="changeDisable('f', 'ofother', tmp.id)" @blur.native="changeDisable('b', 'ofother', tmp.id)" :id="'ofother'+tmp.id" 
                                                    />
                                                  </b-col>
                                                </b-form-row>
                                                 
                                                <b-form-row v-if="(tmp.type!='Damage Description')">
                                                  <b-col sm="4" cols="12" class="cForm">Insurance:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input id="insurance" :state="null" type="text" @change="updateItem($event, 'insurance_number', tmp.id)" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofinsurance2', tmp.id)"
                                                    :value="tmp.insurance" placeholder="Enter insurance number" class="cForm-input" 
                                                     @focus.native="changeDisable('f', 'ofinsurance2', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance2', tmp.id)" :id="'ofinsurance2'+tmp.id" 
                                                    /> 
                                                  </b-col>
                                                </b-form-row>

                                                  <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Ins.Name:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input :state="null" type="text"  class="cForm-input"  placeholder="Enter insurance name"
                                                      @change="updateItem($event, 'insurname', tmp.id)" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofinsurance3', tmp.id)" :value="tmp.insurname"
                                                      @focus.native="changeDisable('f', 'ofinsurance3', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance3', tmp.id)" :id="'ofinsurance3'+tmp.id" 
                                                  />
                                                  </b-col>
                                                </b-form-row>

                                                 <b-tooltip triggers="none" :show="disablefild('ofother', tmp.id)" :target="'ofother'+tmp.id">
                                               {{disablefildUser('ofother', tmp.id)}}
                                                 </b-tooltip>

                                                  <b-form-row v-if="(tmp.type=='Damage Description')">
                                                  <b-col sm="4" cols="12" class="cForm">Insurance:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                    <b-form-input id="insurance" :disabled="tmp.typeOfHead=='Invoices'||disablefild('ofinsurance', tmp.id)" :state="null" type="text" @change="updateItem($event, 'insurance_number', tmp.id)"
                                                    :value="tmp.insurance" placeholder="Enter insurance number" class="cForm-input" 
                                                    @focus.native="changeDisable('f', 'ofinsurance', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance', tmp.id)" :id="'ofinsurance'+tmp.id" 
                                                    />
                                                  </b-col>
                                                </b-form-row>

                                                 <b-tooltip triggers="none" :show="disablefild('ofinsurance', tmp.id)" :target="'ofinsurance'+tmp.id">
                                               {{disablefildUser('ofinsurance', tmp.id)}}
                                                 </b-tooltip>

                                              </b-col>
                                               <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12"  v-if="(tmp.type=='Damage Description')">

                                                  <b-form-row>
                                                  <b-col sm="4" cols="12" class="cForm">Examining&nbsp;worker:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                   <b-form-select type="text" @change="updateItem($event, 'ExamWorker', tmp.id)"
                                                   :value="tmp.worker" :options="workers"
                                                   style="padding:0px;padding-left:2px;" class="cForm-input" />
                                                  </b-col>
                                         </b-form-row>
                                               
                                              </b-col>
                                               <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12" >

                                                <b-form-row v-if="tmp.type=='Damage Description'">
                                                  <b-col sm="4" cols="12" class="cForm">Inspection&nbsp;date:</b-col>
                                                  <b-col sm="8" cols="12" >
                                                  <b-form-input :state="null" type="date"
                                                    :value="tmp.dateInspect" @change="updateItem($event, 'dateInspect', tmp.id)" class="cForm-input"
                                                      :disabled="disablefild('ofdateInspect', tmp.id)"
                                                     @focus.native="changeDisable('f', 'ofdateInspect', tmp.id)" @blur.native="changeDisable('b', 'ofdateInspect', tmp.id)" :id="'ofdateInspect'+tmp.id" 
                                                     />
                                                  </b-col>
                                               </b-form-row>
                                                 
                                                 <b-tooltip triggers="none" :show="disablefild('ofdateInspect', tmp.id)" :target="'ofdateInspect'+tmp.id">
                                               {{disablefildUser('ofdateInspect', tmp.id)}}
                                                 </b-tooltip>
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
                                              </b-row>
                                            </b-col>
                                            </b-form-row>
<b-col lg="4" md="12" class="cuestomRow" v-if="tmp.type!='Damage Description'">
 
                                                 <b-form-row>
                                                  
                                                  <b-col sm="4" cols="12" class="cForm">Discont:</b-col>
                                                  <b-col sm="3" cols="12" ><b-input-group class="cForm-input">
                    <b-input id="disc" type="number" :disabled="tmp.typeOfHead=='Invoices'" v-model="discP" :state="null" 
                       placeholder="Summa&nbsp;of&nbsp;Percent" @change="discOfPercent();updateProjectTaxs();" class="cForm-input"/>
                    <b-input-group-append class="fadeshow1">
                       <div class="input-group-text lablelInInput" @click="butDiscPerc = (butDiscPerc == '%' ? 'P' : '%'); discOfPercent();updateProjectTaxs();">{{butDiscPerc}}</div>
                    </b-input-group-append>
                 </b-input-group></b-col>
                                                  <b-col sm="5" cols="12" ><b-input-group class="cForm-input">
                    <b-input disabled id="sop" v-model="disc"  :state="null"  type="text"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input text-right" />
                         <b-input-group-append class="fadeshow1">
                            <div class="input-group-text lablelInInput">€</div>
                        </b-input-group-append>  
                 </b-input-group></b-col>
</b-form-row>

<b-form-row>
  <b-col sm="7" cols="12" class="cForm">Netto:</b-col>
  <b-col sm="5" cols="12" ><b-input-group  class="cForm-input">
                 <b-form-input id="netto" v-model="netto" :state="null"  type="text" 
                    placeholder="Enter netto" disabled class="cForm-input text-right" />
                    <b-input-group-append  class="fadeshow1">
                        <div class="input-group-text lablelInInput">€</div>
                    </b-input-group-append>  
              </b-input-group></b-col>
</b-form-row>

<b-form-row>
  <b-col sm="3" cols="12" class="cForm">Tax:</b-col>

  <b-col sm="1" cols="12"  style="height: 20px;">
    <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'" @click="saveCol($event)" :disabled="tmp.typeOfHead=='Invoices'">
      <span class="when-closed">+</span>
    </b-link>
  </b-col>

  <b-col sm="3" cols="12" ><b-input-group class="cForm-input">
                    <b-input id="taxP" :disabled="tmp.typeOfHead=='Invoices'" v-model="taxP" :state="null"  type="number" @change="discOfPercent();updateProjectTaxs();"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input " />
                        <b-input-group-append  class="fadeshow1"><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                 </b-input-group></b-col>
  <b-col sm="5" cols="12" ><b-input-group  class="cForm-input">
                    <b-input disabled id="tax" v-model="tax" :state="null"  type="text"
                       placeholder="Summa&nbsp;of&nbsp;Percent" class="cForm-input text-right " />
                        <b-input-group-append  class="fadeshow1"><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                 </b-input-group></b-col>
</b-form-row>
      
<b-collapse style="width:100%" id="addtax" v-model="addtaxColapse">
<b-form-row>
  <b-col sm="3" cols="12" class="cForm">Tax:</b-col>
  
  <b-col sm="1" cols="12" style="height: 20px;">
    <b-link style="text-decoration: none; font-weight: normal;" v-b-toggle="'addtax'"  @click="saveCol" :disabled="tmp.typeOfHead=='Invoices'">
      <span class="when-opened">-</span>
    </b-link>
  </b-col>

  <b-col sm="3" cols="12" ><b-input-group   class="cForm-input">
                       <b-input v-model="taxPDub" :disabled="tmp.typeOfHead=='Invoices'" :state="null"  type="number" @change="discOfPercent();updateProjectTaxs();"
                          placeholder="Summa of Percent" class="cForm-input " />
                                   <b-input-group-append  class="fadeshow1"><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                    </b-input-group></b-col>
  <b-col sm="5" cols="12" ><b-input-group  class="cForm-input">
                       <b-input disabled v-model="taxDub" disabled :state="null"  type="text"
                          placeholder="Summa of Percent" class="cForm-input text-right" />
                          <b-input-group-append  class="fadeshow1"><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                    </b-input-group></b-col>
</b-form-row>
 </b-collapse>        
 
<b-form-row>
  <b-col sm="7" cols="12" class="cForm">Brutto:</b-col>
  <b-col sm="5" cols="12" ><b-input-group  class="cForm-input">
                 <b-form-input v-model="brutto" :state="null"  type="text"
                    placeholder="Enter brutto" disabled class="cForm-input text-right" />
                   <b-input-group-append  class="fadeshow1"><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
              </b-input-group></b-col>
</b-form-row>

        </b-col>
                                        </b-row>
<calc-table-group
:windowPrint="windowPrint"
:works="works"
:selectedCornty="selectedCornty"
:project="project"
:account="$security.table.account"
:pid="id"
:disc='disc'
:discP='discP'
:tax='tax'
:taxDub='taxDub'
:taxP='taxP'
:taxPDub='taxPDub'
:netto='netto'
:brutto='brutto'
:comments="comments"
:value="partx"
:id="tmp.id"
:type="tmp.type"
:butDiscPerc="butDiscPerc"
:looks="looks"
:responseFiles="responseFiles"
:addtaxColapse="addtaxColapse"
:opt='typesForTables'
:tmp="tmp"
:workers="workers"
:funcStop="funcStop"
:loadDamages="loadDamages"
:customer="customer"
:person="person"
:selectCustomer="selectCustomer"
:selectPerson="selectPerson"
:selectedWorkers="selectedWorkers"

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

@changeSum="discOfPercent()"
></calc-table-group>
</b-container>

</div>
</template>
<script type="text/javascript">
import axios from 'axios';
import moment from 'moment';
import {VueEditor, Quill} from 'vue2-editor';
export default {
  components: {
    VueEditor,
  },
  props: [
  'tmp', 'project', 'looks',  'works', 'windowPrint',
  'selectedCornty', 'id', 'comments', 'responseFiles', 'selectedWorkers',
  'typesForTables', 'workers', 'funcStop', 'loadDamages',
  'partx', 'person', 'customer', 'selectCustomer', 'selectPerson',
  'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList'
  ],



  data(){
      return{
            addtaxColapse: null,
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
]
            }
    },
methods: {
writecomet(){
var newContent =  this.$refs['other'].quill.getHTML()
  if (newContent != '<p><br></p>') {
    this.$emit('projectOther', newContent);
    this.updateProject('other', newContent);
  }
},

   checkInEditor(tname){
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

     this.updateProject('other', valueHtml)

},
selectedDocs(event){
  this.$emit('selectedDocs', event)
},
addPdf() {
  this.$emit('addPdf')
},
printPdf() {
  this.$emit('printPdf')
},
preview() {
  this.$emit('preview')
},
printOffer() {
  this.$emit('printOffer')
},
worker() {
  this.$emit('worker')
},
hideWindowPrint(){
  this.$emit('hideWindowPrint')
},
openWindowPrint(){
  this.$emit('openWindowPrint')
},
remoteTax(id){

axios.get('/get_tables', {
  params: {
    id: id
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
     this.$emit('tabletopartx', tables)
})

},


    saveCol(){
      this.addtaxColapse =this.addtaxColapse?false:true
      this.taxPDub=0,
      this.taxDub=0,
         this.discOfPercent(),
         this.updateProjectTaxs()
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
            this.brutto = this.$options.filters.thousandSeparator(tmpNetto + tmpTax + tmpTax2)
        },
getPerson(){
this.$emit('getPerson')
},
getCustomer() {
this.$emit('getCustomer')
},
getCustomerAdress() {
this.$emit('getCustomerAdress')
},
getCustomerAdressOne() {
this.$emit('getCustomerAdressOne')
},
// countDigitals(val){
// this.$emit('countDigitals', val)
// },

      countDigitals(val){
        // console.log(val)
        var nuls=3-val.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        val='0'+val
                    }
        return val
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
          updateProject(fild, newData){
        axios.get('/updateProject', {params: {
                id: this.id,
                date: newData,
                fild: fild
        }}).then(response => {
          if (fild == 'other'){
             axios.get('/updateProject', {
              params: {
                  id: this.id,
                  date:  this.$security.table.account.first_name+'_'+this.$security.table.account.second_name,
                  fild: 'user'
                 }});
             axios.get('/updateProject', {
              params: {
                  id: this.id,
                  date: moment().format("DD.MM HH:mm"),
                  fild: 'datacomment'
                 }});
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
    },
        watch: {
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

  },

  }

</script>