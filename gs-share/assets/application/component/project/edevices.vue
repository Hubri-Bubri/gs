<template>
  <devices-table-group 
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
v-model="partx"
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
@addPdfSep="addPdfSep"
@printPdf="printPdf"
@preview="preview"
@printOffer="printOffer"

@worker="worker"
@hideWindowPrint="hideWindowPrint"
ref="deviceGroup"
  ></devices-table-group>
</template>

<script type="text/javascript">
import axios from 'axios';
export default {
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
            butDiscPerc: '%',
            netto: 0,
            brutto: 0
        }
},
  methods:{
              selectedDocs(event){
          this.$emit('selectedDocs', event)
        },
        addPdf() {
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
        worker() {
          this.$emit('worker')
        },
        hideWindowPrint(){
          this.$emit('hideWindowPrint')
        },
        openWindowPrint(){
          this.$emit('openWindowPrint')
        }
  },

  }

</script>