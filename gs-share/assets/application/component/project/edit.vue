<template>

<div ref="editcomponet">
<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
@mouseover="cloudHover = true" @mouseleave="cloudHover = false"
@click="writecomet();changeDisable('b', 'gencooment', id);cloudChange=false;cloudLoad=true;" v-if="(tmp.number==null)">
  <b-icon stacked icon="circle-fill" :animation="cloudLoad?'throb':null" variant="primary" v-show="cloudLoad||cloudHover"></b-icon>
  <b-icon stacked icon="cloud-upload" scale="0.5" :variant="cloudHover?'light':'dark'" v-show="!cloudLoad"></b-icon>
  <b-icon stacked icon="circle" variant="info" v-show="cloudChange"></b-icon>
</b-iconstack>
<span v-if="(tmp.number==null)" style="position:relative;left:24px;top:15px;z-index:2;">{{(timeSave!=null)?$t('alert.LastSaveIn')+': '+timeSave:''}}</span>

<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
@click="checkInEditor('other')" v-if="(tmp.number==null)" @mouseover="calcHover = true" @mouseleave="calcHover = false">
  <b-icon stacked icon="circle-fill" variant="primary" v-show="calcHover"></b-icon>
  <b-icon stacked icon="calculator" scale="0.5" :variant="calcHover?'light':'dark'"></b-icon>
</b-iconstack>

<span v-show="(disablefildUser('gencooment', id)!='you')" style="position:relative;left:30px;top: 16px;width:18px;z-index:2;"
v-if="(tmp.number==null)">{{disablefildUser('gencooment', id)}}</span>

<vue-editor :value="project.other" :editorToolbar="customToolbar"
style="position:relative;top:-20px;z-index:1;" v-if="(tmp.number==null)"
class="text-right"  ref="other"
@blur="save()"
@focus="changeDisable('f', 'gencooment', id);cloudChange=true;"
:id="'gencooment'+id" 
:disabled="disablefild('gencooment', id)?'disabled':false"
/>


                                   <b-container v-show="tmp.number != null">
                                      <b-input type="text" hidden v-model="tmp.typeOfHead" />
                                        <b-row>
                                             <b-col cols="12"><br></b-col>
                                            <b-col lg="8" md="12">
                                              <b-row>
                                              <b-col lg="6" md="12" >
                                              <!-- <b-form-group :label="tmp.typeOfHead+':'" label-cols="4" label-size="sm"> -->
                                              <b-form-group :label="$t('fields.number')+':'" label-cols="4" label-size="sm">
                                                {{(tmp.typeOfHead=='Invoices')?(tmp.number.split(' ').length==5)?tmp.number.split(' ')[3]:
                                                countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[1]:(tmp.typeOfHead=='SUB')
                                                ?tmp.number.split(' ')[0]:(tmp.typeOfHead=='Sub Invoices')?tmp.number.split(' ')[3]:tmp.number}}
                                              </b-form-group>
                                              <b-tooltip triggers="none" :show="disablefild('ofnumber', tmp.id)" :target="'ofnumber'+tmp.id">
                                               {{disablefildUser('ofnumber', tmp.id)}}
                                              </b-tooltip>

                                              <b-form-group :label="$t('edit.document')+':'" label-cols="4" label-size="sm">
                                                <b-form-input disabled :disabled="disablefild('ofdate', tmp.id)"
                                                type="date" @change="updateItem($event, 'date', tmp.id)"
                                                :value="tmp.date" placeholder="Enter date"  
                                                @focus.native="changeDisable('f', 'ofdate', tmp.id)"
                                                @blur.native="changeDisable('b', 'ofdate', tmp.id)" :id="'ofdate'+tmp.id" size="sm"/>
                                              </b-form-group>

                                              <b-form-group :label="$t('edit.place')+':'" label-cols="4" label-size="sm">
                                                <b-form-input disabled type="text"  :disabled="disablefild('ofplace', tmp.id)" 
                                                @change="updateItem($event, 'place', tmp.id)"
                                                :value="tmp.place" placeholder="Enter place" 
                                                @focus.native="changeDisable('f', 'ofplace', tmp.id)"
                                                @blur.native="changeDisable('b', 'ofplace', tmp.id)" :id="'ofplace'+tmp.id" size="sm"/>
                                              </b-form-group>
                                                 
                                                <b-tooltip triggers="none" :show="disablefild('ofdate', tmp.id)" :target="'ofdate'+tmp.id">
                                               {{disablefildUser('ofdate', tmp.id)}}
                                                 </b-tooltip>

                                       <!--        <b-form-group label="Event:" label-cols="4" label-size="sm" v-if="tmp.type=='Damage Description'">
                                                <b-form-input disabled :state="null" type="date" :disabled="disablefild('evdate', tmp.id)"
                                                :value="tmp.dateEvent" @change="updateItem($event, 'dateEvent', tmp.id)"
                                                @focus.native="changeDisable('f', 'evdate', tmp.id)" size="sm"
                                                @blur.native="changeDisable('b', 'evdate', tmp.id)" :id="'evdate'+tmp.id"/>
                                              </b-form-group> -->

                                  <!--               <b-tooltip triggers="none" :show="disablefild('evdate', tmp.id)" :target="'evdate'+tmp.id">
                                               {{disablefildUser('evdate', tmp.id)}}
                                                 </b-tooltip> -->

                                              </b-col>
                                              <b-col lg="6" md="12" >
                                                 <b-tooltip triggers="none" :show="disablefild('ofplace', tmp.id)" :target="'ofplace'+tmp.id">
                                               {{disablefildUser('ofplace', tmp.id)}}
                                                 </b-tooltip>


                                              <b-form-group :label="$t('edit.order')+':'" label-cols="4" label-size="sm">
                                                <b-form-input disabled :disabled="disablefild('ofother', tmp.id)" :state="null" type="text"
                                                @change="updateItem($event, 'other', tmp.id)"
                                                :value="tmp.other" placeholder="Enter number" size="sm"
                                                @focus.native="changeDisable('f', 'ofother', tmp.id)"
                                                @blur.native="changeDisable('b', 'ofother', tmp.id)" :id="'ofother'+tmp.id" />
                                              </b-form-group>


                                              <b-form-group :label="$t('edit.insurance')+':'" label-cols="4" label-size="sm" >
                                                <b-form-input disabled  :state="null" type="text" @change="updateItem($event, 'insurance_number', tmp.id)"
                                                :disabled="disablefild('ofinsurance2', tmp.id)"
                                                :value="tmp.insurance" placeholder="Enter insurance number" size="sm"
                                                @focus.native="changeDisable('f', 'ofinsurance2', tmp.id)" @blur.native="changeDisable('b', 'ofinsurance2', tmp.id)"
                                                :id="'ofinsurance2'+tmp.id"  />
                                              </b-form-group>

                                               <b-form-group :label="$t('edit.insName')+':'" label-cols="4" label-size="sm">
                                                <b-form-input disabled :state="null" type="text"  placeholder="Enter insurance name"
                                                @change="updateItem($event, 'insurname', tmp.id)"
                                                :disabled="disablefild('ofinsurance3', tmp.id)" :value="tmp.insurname"
                                                @focus.native="changeDisable('f', 'ofinsurance3', tmp.id)" size="sm"
                                                @blur.native="changeDisable('b', 'ofinsurance3', tmp.id)" :id="'ofinsurance3'+tmp.id"  />
                                               </b-form-group>

                                                 <b-tooltip triggers="none" :show="disablefild('ofother', tmp.id)" :target="'ofother'+tmp.id">
                                               {{disablefildUser('ofother', tmp.id)}}
                                                 </b-tooltip>

<!-- 
                                               <b-form-group label="Insurance:" label-cols="4" label-size="sm" v-if="(tmp.type=='Damage Description')">
                                                <b-form-input disabled  :disabled="disablefild('ofinsurance', tmp.id)" :state="null" type="text"
                                                @change="updateItem($event, 'insurance_number', tmp.id)" size="sm"
                                                :value="tmp.insurance" placeholder="Enter insurance number" 
                                                @focus.native="changeDisable('f', 'ofinsurance', tmp.id)"
                                                @blur.native="changeDisable('b', 'ofinsurance', tmp.id)" :id="'ofinsurance'+tmp.id"   />
                                               </b-form-group> -->
<!-- 
                                                 <b-tooltip triggers="none" :show="disablefild('ofinsurance', tmp.id)" :target="'ofinsurance'+tmp.id">
                                               {{disablefildUser('ofinsurance', tmp.id)}}
                                                 </b-tooltip> -->

                                              </b-col>
      <!--                                          <b-col :lg="(tmp.type!='Damage Description')?6:12" md="12"  v-if="(tmp.type=='Damage Description')">

                                                <b-form-group label="Exam.worker:" label-cols="4" label-size="sm">
                                                  <b-form-select type="text" @change="updateItem($event, 'ExamWorker', tmp.id)"
                                                  :value="tmp.worker" :options="workers" size="sm"
                                                  />
                                               </b-form-group>

                                              </b-col> -->
                                               <b-col lg="6" md="12" >

      <!--                                           <b-form-group label="Ins.date:" label-cols="4" label-size="sm" v-if="tmp.type=='Damage Description'">
                                                  <b-form-input disabled :state="null" type="date"
                                                  :value="tmp.dateInspect" @change="updateItem($event, 'dateInspect', tmp.id)"
                                                  :disabled="disablefild('ofdateInspect', tmp.id)"
                                                  @focus.native="changeDisable('f', 'ofdateInspect', tmp.id)" @blur.native="changeDisable('b', 'ofdateInspect', tmp.id)"
                                                  :id="'ofdateInspect'+tmp.id" 
                                                  />
                                               </b-form-group> -->
                                                 
              <!--                                    <b-tooltip triggers="none" :show="disablefild('ofdateInspect', tmp.id)" :target="'ofdateInspect'+tmp.id">
                                               {{disablefildUser('ofdateInspect', tmp.id)}}
                                                 </b-tooltip> -->
                                                <b-tooltip triggers="none" :show="disablefild('ofinsurance2', tmp.id)" :target="'ofinsurance2'+tmp.id">
                                               {{disablefildUser('ofinsurance2', tmp.id)}}
                                                 </b-tooltip>

<!-- <b-button  @click="addGropuDamage" v-if="(tmp.type=='Damage Description')" size="sm">
                                        Add Group
</b-button>
<b-button  @click="worker" v-if="(tmp.type=='Damage Description')" size="sm">
                                        Workers
</b-button> -->
                                              </b-col>
                                              </b-row>
                                            </b-col>
                                            <!-- </b-form-row> -->
<b-col lg="4" md="12" >
 
                                            
                                                <b-form-group :label="$t('edit.discont')+':'" label-cols="4" label-size="sm">
                                                  <b-input-group>
                                                    
                                                      <b-input id="disc" type="number"  v-model="discP" class="raz"
                                                      size="sm" @change="updateProjectTaxs();discOfPercent();"/>
                                                    
                                                    
                                                      <span @click="butDiscPerc = (butDiscPerc == '%' ? 'P' : '%');discOfPercent();updateProjectTaxs();" style="white-space: nowrap;">
                                                        {{butDiscPerc}}
                                                      </span>
                                                    
                                                    <b-col class="text-right" style="white-space: nowrap;">
                                                      {{disc}} €
                                                    </b-col>
                                                  </b-input-group>
                                               </b-form-group>


                                                <b-form-group :label="$t('edit.netto')+':'" label-cols="4" label-size="sm">
                                                  <b-col class="text-right" style="white-space: nowrap;">{{netto}} €</b-col>
                                               </b-form-group>

                                              <b-form-group :label="$t('edit.tax')+':'" label-cols="4" label-size="sm">
                                                  <b-input-group>
                                                    
                                                      <b-link v-b-toggle="'addtax'" @click="saveCol($event)" >
                                                        <span class="when-closed">+</span>
                                                      </b-link>
                                                      <b-input id="taxP" v-model="taxP" :state="null" size="sm" class="raz"
                                                      type="number" @change="discOfPercent();updateProjectTaxs();"/>%
                                                     
                                                    <b-col class="text-right" style="white-space: nowrap;">
                                                      {{tax}} €
                                                    </b-col>
                                                  </b-input-group>
                                               </b-form-group>
                                               <b-collapse style="width:100%" id="addtax" v-model="addtaxColapse">
                                                <b-form-group :label="$t('edit.tax')+':'" label-cols="4" label-size="sm">
                                                  <b-input-group>

                                                    <b-link v-b-toggle="'addtax'" @click="saveCol" >
                                                      <span class="when-opened">-</span>
                                                    </b-link>

                                                    <b-input id="taxP" v-model="taxPDub" :state="null" size="sm" class="raz"
                                                    type="number" @change="discOfPercent();updateProjectTaxs();"/>%
                                                    <b-col class="text-right"  style="white-space: nowrap;">
                                                      {{taxDub}} €
                                                    </b-col>
                                                  </b-input-group>
                                               </b-form-group>
                                               </b-collapse>  

 <b-form-group :label="$t('edit.brutto')+':'" label-cols="4" label-size="sm">
                           <b-col class="text-right"  style="white-space: nowrap;">
                                                   {{brutto}} €
                                         </b-col>
                                               </b-form-group>



      

 


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

:availableMails="availableMails"
:plan="plan"
@seltable="$emit('seltable')"
@sendMail="$emit('sendMail', availableMails)"

@selectedDocs="selectedDocs"
@addPdf="addPdf"
@printPdf="printPdf"
@preview="preview"
@printOffer="printOffer"

@worker="worker"
@hideWindowPrint="hideWindowPrint"

@changeSum="discOfPercent()"
ref="calcGroup"
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
  'tmp', 'project', 'looks',  'works', 'windowPrint', 'availableMails',
  'selectedCornty', 'id', 'comments', 'responseFiles', 'selectedWorkers',
  'typesForTables', 'workers', 'funcStop', 'loadDamages', 'plan',
  'partx', 'person', 'customer', 'selectCustomer', 'selectPerson',
  'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList'
  ],



  data(){
      return{
            timeSave: null,
            calcHover: false,
            cloudHover: false,
            cloudChange: false,
            cloudLoad: false,
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

save(){
  this.writecomet();
  this.changeDisable('b', 'gencooment', this.id);
  this.cloudChange=false;
  this.cloudLoad=true;
  this.timeSave = moment().format("DD.MM HH:mm")
  // console.log(this.timeSave)
},
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
                var add2 = 0
                this.partx.forEach((val) => {
                    val.parts.part_content.forEach((sval) => {
                        if (sval.without == true) {
                          if(sval.alttax==true) add2 = add2 + ((sval.count * sval.price / 100) * this.discP)
                          if(sval.alttax!=true) add = add + ((sval.count * sval.price / 100) * this.discP)
                        }
                    })
                })

                this.disc = this.$options.filters.thousandSeparator((summa / 100) * this.discP - (add+add2))
                tmpDisc = (summa / 100) * this.discP - (add+add2)
                // console.log(tmpDisc)
            } else {
                this.disc = this.$options.filters.thousandSeparator(this.discP)
                tmpDisc = this.discP
            }
            // console.log(this.discP)

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
            // console.log(add, add2)
            if (this.butDiscPerc == '%') {
              addt=(addt-((addt/100)*(this.discP)))+add //плюс потери с without
              addt2=(addt2-((addt2/100)*(this.discP)))+add2
              // console.log(addt)
            }
            if (this.butDiscPerc == 'P') {
              addt=addt-(addt/100)*(this.discP*100/summa)
              addt2=addt2-(addt2/100)*(this.discP*100/summa)
            }
            // console.log(this.$options.filters.thousandSeparator(addt * (this.taxP / 100)), addt, this.taxP)
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
        axios.post('/update_item_from_project', {
              
                   val: val,
                   type: type,
                   id: id
              
        })
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
        axios.post('/updateProject', {
                id: this.id,
                date: newData,
                fild: fild
        }).then(response => {
          if (fild == 'other'){
             axios.post('/updateProject', {
              
                  id: this.id,
                  date:  this.$security.table.account.first_name+'_'+this.$security.table.account.second_name,
                  fild: 'user'
                 }).then(response => {
                  this.cloudLoad = false;
                 });
             axios.post('/updateProject', {
              
                  id: this.id,
                  date: moment().format("DD.MM HH:mm"),
                  fild: 'datacomment'
                 });
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
          // if (this.type=='Invoices') result = true
          return result
      },
      disablefildUser(fild, id){
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

  // mounted(){
  //   setTimeout(() => {
  //       this.$emit('loded', 'edit', this.$refs.other.$el.clientHeight, 0)
  //   }, 100);     
  // }

  }

</script>
<style type="text/css">
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

/*.withoutBorderInInput input[type=text]{
  box-shadow: none;
}
.withoutBorderInInput input[type=text]:focus:not([readonly]) {
  box-shadow: none;
}
.withoutBorderInInput textarea{
  overflow-y: auto;
}*/
/*.short {
  overflow-y: hidden !important;
  max-height: 17px !important;
}
.notshort {
  overflow-y: auto !important;
}

*/



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
/*.flag a{
  padding: 5px !important;
}*/
/*@import url('https://fonts.googleapis.com/css2?family=Inconsolata&display=swap');

.tx {
  width: 100%;
  min-height: 17px;
  height: 17px;
  padding: 2px;
  resize: none;
  overflow: hidden;
  background-color: transparent;
  border: 2px solid #000;
  border-radius: 4px;
  font-family: "Inconsolata", monospace;
  font-size: 0.710938rem;
  color: #000;
  box-shadow: none;
}

.tx:focus {
  box-shadow: none;
  outline: none;
}*/
</style>