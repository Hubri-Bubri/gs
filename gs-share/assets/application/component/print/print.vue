<template>
   <div>
    <hr />
    <b-row align-h="between" class="pr-2">
        <slot></slot>
        <b-button size="sm" @click="printOffer()" class="printForMobile"
        v-if="!(((tmp.typeOfHead=='Invoices')&&(tmp.number.split(' ').length==5))||(tmp.typeOfHead=='StandingOrder'))">
          <b-icon icon="printer" aria-hidden="true"></b-icon>
        </b-button>
    </b-row>
    <br/>
      <b-modal size="lg" centered ok-only no-close-on-esc no-close-on-backdrop hide-header-close  :visible="windowPrint" v-if="makemodalpdf">
         <div slot="modal-title" class="w-100">
            <div>{{$t('print.print')}}</div>
         </div>


     
                <b-container v-show="printBusy">
                <b-row align-v="center" class="text-center" style="width:100%;height:550px;">
                    <b-col>
                <strong class="text-info">
                <b-spinner class="align-middle"  ></b-spinner>
                    {{$t('projects.loading')}}...
                </strong>
                    </b-col>
                </b-row>
                </b-container>
                

         <iframe v-show="printBusy==false" type="iframe" style="width:100%;height:550px;" name="myIframe"  @load="loadFrame"></iframe>


         <form target="myIframe" action="/pdf" method="post" style="display:none" ref="preForm">
            <input type="text" name="dateInspect" :value="tmp.dateInspect" />
            <input type="text" name="dateEvent" :value="tmp.dateEvent" />
            <input type="text" name="worker" :value="tmp.worker" />
            <!-- <textarea name="loadDamages">{{loadDamages}}</textarea> -->
            <input type="text" name="customerСontract" :value="tmp.other" />

            <input type="text" name="getCustomer" :value="getCustomer()" />
            <input type="text" name="getPerson" :value="getPerson()" />
            <input type="text" name="getCustomerAdress" :value="getCustomerAdress()" />
            <input type="text" name="getCustomerAdress1" :value="getCustomerAdressOne()" />

            <input type="text" name="offerHead" :value="tmp.typeOfHead" />
            <input type="text" name="subHead" :value="tmpForDamageDescription.name.content" />
           <!--  <input type="text" name="editor" :value="project.editor" /> -->
            <input type="text" name="editor" :value="this.$security.table.account.first_name +' '+ this.$security.table.account.second_name" />
            <input type="text" name="userTel" :value="account.tel" />
            <input type="text" name="userFax" :value="account.fax" />
            <input type="text" name="userMail" :value="account.mail" />
            <input type="text" name="number" :value="(tmp.typeOfHead=='Invoices')?countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[1]:tmp.number" />
            <input type="text" name="date" :value="getDateFormat(today)" />
            <input type="text" name="work" :value="tmp.work" />
            <input type="text" name="pNumber" :value="project.number" />
            <input type="text" name="street" :value="project.street1" />
            <input type="text" name="zip" :value="project.zip1" />
            <input type="text" name="contry" :value="selectedCornty.code" />
            <input type="text" name="area" :value="project.area" />
            <input type="text" name="city" :value="project.city1" />
            <input type="text" name="dateProject" :value="project.date" />
            <input type="text" name="insurance" :value="tmp.insurance" />
            <input type="text" name="insurname" :value="tmp.insurname" />
            <input type="text" name="place" :value="tmp.place" />
            <input type="text" name="finishWork" :value="dateForInvoice?(stworks?'Die Arbeit wurde ausgeführt: vom '+getDateFormat(stworks)+' bis ':'Datum der Fertigstellung der Arbeiten: ')+getDateFormat(dateForInvoice):''" />
            <input type="text" name="stworks" :value="stworks|dateInverse"  />
            <input type="text" name="fworks" :value="dateForInvoice|dateInverse"  />
            <input type="text" name="inspected" :value="dateForInspect|dateInverse"  />
            <input type="text" name="inspectedby" :value="byForInspect"  />
            <input type="text" name="positions" :value="partx" />
            <input type="text" name="comment" :value="tmp.comment" />
            <input type="text" name="project_id" :value="this.id" />
            <input type="text" name="selected_docs_list" :value="selectedDocsList" />
            <textarea name="tables" :value="JSON.stringify(partx).split('\\n').join('<br />')" />
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
               :partx='partx' :value="addtaxColapse" :summ="alltotal(this.partx)" type="send" />
            <input type="text" name="addtaxColapse" :value="addtaxColapse" />
            <input type="text" name="workers" :value="workers" />
            <input type="text" name="addPdf" :value="addPdfs" />
            <button type="submit">!!!!</button>
         </form>
         <div slot="modal-footer" class="w-100">
            <b-row align-v="start">
               <b-col cols="6" align-self="end">
                  <b-form inline  v-if="tmp.typeOfHead!='Devices'">
                     <b-col cols="4">{{$t('print.dateOfPrint')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;"
                           size="sm" type="date" v-model="today" @change="preview" />
                     </b-col>
                  </b-form>
                   <b-form inline v-if="tmp.typeOfHead=='SUB' || tmp.typeOfHead=='Invoices'">
                     <b-col cols="4">{{$t('print.startWorks')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           v-model="stworks"  @change="preview" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="tmp.typeOfHead!='Devices' & tmp.typeOfHead!='Damage' & tmp.typeOfHead!='Reports'">
                     <b-col cols="4">{{$t('print.endWorks')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           v-model="dateForInvoice"  @change="preview" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="tmp.typeOfHead=='Damage'">
                     <b-col cols="4">{{$t('print.inspectDate')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           v-model="dateForInspect"  @change="preview" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="tmp.typeOfHead=='Damage'">
                     <b-col cols="4">{{$t('print.inspectBy')}}</b-col>
                     <b-col cols="8">
                <b-form-select style="color:#000; padding-left: 5px !important; font-size: 16px;" size="sm"  :disabled="addDocument"
                     :options="workers" :value="byForInspect" @change="toByForInspect($event)" >
                  </b-form-select>
                     </b-col>
                  </b-form>

                  <b-button-group size="sm" style="padding-top: 15px !important;padding-left: 15px !important;">
                    <b-button variant="primary" @click="(printBusy=true)+$emit('hideWindowPrint')" >
                        {{$t('print.close')}} 
                     </b-button>
                     <b-button variant="primary" @click="printPdf" >
                        {{$t('print.print')}} 
                     </b-button>
                     <b-button variant="primary" @click="addPdf" :disabled="addDocument">
                        {{ addDocument?$t('projectDetail.docInProgress'):$t('projectDetail.add') }}
                        <b-iconstack font-scale="1" v-if="addDocument">
                          <b-icon stacked icon="circle-fill" animation="throb" variant="info"></b-icon>
                        </b-iconstack>
                     </b-button>
                     <b-button variant="primary" @click="addPdfSep" v-if="tmp.typeOfHead=='Devices'" :disabled="addDocument">
                        {{$t('print.addSeparated')}} 
                     </b-button>                     
                  </b-button-group>
               </b-col>
               <b-col cols="6">
                   <b-form-select buttons text-field="name" value-field="id" button-variant="outline-primary" 
                     :options="typeDocsList" @change="selectedDocs($event)" :value="selectedDocsList"
                     multiple :select-size="(tmp.typeOfHead=='Damage')?7:(tmp.typeOfHead=='Devices')?3:5">
                  </b-form-select>
               </b-col>
            </b-row>
         </div>
      </b-modal>
   </div>
</template>
<script>
import axios from 'axios';
export default {
    props: [
    'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList',
    'windowPrint',
    'selectedCornty',
    'project',
    'tmp',
    'workers',
    'comments',
    'loadDamages',
    'account',
    'disc',
    'discP',
    'tax',
    'taxDub',
    'taxP',
    'taxPDub',
    'netto',
    'brutto',
    'butDiscPerc',
    'partx',
    'head',
    'addtaxColapse',
    'id',
    'customer',
    'person',
    'selectCustomer',
    'selectPerson'
    ],
    data() {
        return {
          printBusy:true,
          addDocument:false,
          stworks:null,
          customerContract: [],
          today: (new Date().getFullYear() + '-' +
                    (((new Date().getFullYear() + '-' + (new Date().getMonth() + 1)).length == 6) ? '0' + (new Date().getMonth() + 1) : (new Date().getMonth() + 1))) +
                '-' +
                (((new Date().getFullYear() + '-' + (new Date().getDate())).length == 6) ? '0' + (new Date().getDate()) : (new Date().getDate())),
            dateForInvoice: null,
            dateForInspect: null,
            byForInspect: null,
            tmpForOffer: {
                name: {
                    connect: null
                },
                first: {
                    connect: null
                },
                second: {
                    connect: null
                }
            },
            tmpForDamageDescription: {
                name: {
                    connect: null
                },
                first: {
                    connect: null
                },
                second: {
                    connect: null
                }
            },
            tmpForOfferSharing: {
                name: {
                    connect: null
                },
                first: {
                    connect: null
                },
                second: {
                    connect: null
                }
            },
            tmpForOfferAward: {
                name: {
                    connect: null
                },
                first: {
                    connect: null
                },
                second: {
                    connect: null
                }
            },
        }
    },
    methods: {
      loadFrame(){
        if (this.addDocument)
          {
            this.addDocument=false;
            this.$emit('hideWindowPrint')
          }
      },
        previewPDFForm(){
          setTimeout(() => {
            this.$refs.preForm.submit()
          }, 20);
        },
        getCustomer() {
            if (this.customer) return this.selectCustomer.name
        },
        getCustomerAdress() {
            if (this.customer) return this.selectCustomer.adress
        },
        getCustomerAdressOne() {
            if (this.customer) return this.selectCustomer.adress1
        },
        getPerson() {
            if (this.person) return this.selectPerson.name
        },

        selectedDocs(event){
          this.printBusy=true;
          this.$emit('selectedDocs', event)
          
        },
        addPdf() {
          this.addDocument=true;
          this.$emit('addPdf')
        },
        addPdfSep() {
          this.$emit('addPdfSep')
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
        toByForInspect(val){
         this.byForInspect = val;
         setTimeout(()=>{
               this.preview();
            }, 20);
        },
        countDigitals(val) {
            var nuls = 3 - val.toString().length
            for (var i = 0; i <= nuls; i++) {
                val = '0' + val
            }
            return val
        },
        getDateFormat(val) {
            if (val != null) {
              if (val != ''){
                var t = val.split('-')
                var y = t[0]
                var m = t[1]
                var d = t[2]
                return d + '.' + m + '.' + y
            }}
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
    },
    mounted(){
        this.$options.sockets.onmessage = (data) => (data.data=='preview') ? this.printBusy=false: ''
    }
}
</script>