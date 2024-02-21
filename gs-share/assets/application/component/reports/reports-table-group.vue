<template>
  <b-container>

    <print v-if="tmp.typeOfHead == 'Reports'"
    :windowPrint="windowPrint"
    :selectedCornty="selectedCornty"
    :project="project" :tmp="tmp"
    :account="account" :id="pid"
    :disc='disc' :discP='discP'
    :tax='tax' :taxDub='taxDub'
    :taxP='taxP' :taxPDub='taxPDub'
    :netto='netto' :brutto='brutto'
    :butDiscPerc='butDiscPerc'
    :partx='showTable()' :head="tmp.typeOfHead"
    :addtaxColapsel="addtaxColapse"
    :workers="workers" :comments="comments"
    :customer="customer"
    :person="person"
    :selectCustomer="selectCustomer"
    :selectPerson="selectPerson"
    :selectedDocsList="selectedDocsList"
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
    ref="print"
    >

    
    <b-col><b-button  size="sm" @click="worker" >
            {{$t('calcTableGroup.workers')}}
          </b-button></b-col>

      <!-- <b-col class="cForm col-12 col-lg-3" style="padding:0px;" slot="Type"></b-col>
      <b-col class="cForm col-12 col-lg-3" style="padding:0px;" slot="Work"></b-col> -->
    </print>
    

    <div v-for="(part, index) in showTable()" :key="part.id">
      <reports-table
      :value="part"
      :tableId="index"
      :workers="workers"
      :looks="looks"
      :selectedWorkers="selectedWorkers" 
      >

        <div slot-scope="table" slot="tableHead">
          <b-link style="width:100%" @click="toog(part.parts.id)">
            <span :id="'dp'+part.parts.id" style="display:none">+</span>
            <span :id="'dm'+part.parts.id">-</span>
          </b-link>
          <span :contenteditable="true" @blur="updateNameReport($event, part.parts.id, part.parts.part_name_report)" @click.prevent.self>
            {{part.parts.part_name_report?part.parts.part_name_report:part.parts.part_name}}
          </span>
        </div>
      </reports-table>

      <br>
    </div>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: [
    'value',
    'workers',
    'selectedDocsList',
    'addPdfs',
    'makemodalpdf',
    'typeDocsList',
    'windowPrint',
    'pid',
    'selectedCornty',
    'project',
    'tmp',
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
    'head',
    'addtaxColapse',
    'id',
    'customer',
    'person',
    'selectCustomer',
    'selectPerson',
    'looks',
    'selectedWorkers'
    ],
  methods: {
    toog(val){
      document.getElementById('dm'+val).style.display = document.getElementById('dev'+val).style.display = (document.getElementById('dev'+val).style.display=='none') ? '' : 'none'
      document.getElementById('dp'+val).style.display = (document.getElementById('dm'+val).style.display=='none') ? '' : 'none'
    },
    toogMeas(val){
      document.getElementById('measurementProtocolOpen'+val).style.display = document.getElementById('mestable'+val).style.display = (document.getElementById('mestable'+val).style.display=='none') ? '' : 'none'
      document.getElementById('measurementProtocolClose'+val).style.display = (document.getElementById('measurementProtocolOpen'+val).style.display=='none') ? '' : 'none'
    },
    selectedDocs(event){
      this.$emit('selectedDocs', event)
    },
    addPdf(){
      this.$emit('addPdf')
    },
    addPdfSep(){
      this.$emit('addPdfSep')
    },
    printPdf(){
      this.$emit('printPdf')
    },
    preview(){
      this.$emit('preview')
    },
    printOffer(){
      this.$emit('printOffer')
    },
    hideWindowPrint(){
      this.$emit('hideWindowPrint')
    },
    openWindowPrint(){
      this.$emit('openWindowPrint')
    },
    updateNameReport(newVal, id, partName) {
      if(newVal.target.innerText != partName){
        axios.get('/updateNameReport', {
          params: {
            nameReport: newVal.target.innerText.replace(/[\s]{2,}/, ''),
            id: id
          }
        })
      }
    }, 
    showTable(){
      return this.value.filter((v)=>{
        if(v.parts.reports_content.length>0){
          return v
        }
      })
    },
        worker() {
          this.$emit('worker')
        }
  }
}
</script>