<template>
  <div>
    <print v-if="tmp.typeOfHead == 'Devices'"
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
    <b-col></b-col>

      <!-- <b-col class="cForm col-12 col-lg-3" style="padding:0px;" slot="Type"></b-col>
      <b-col class="cForm col-12 col-lg-3" style="padding:0px;" slot="Work"></b-col> -->
    </print>
    
    <div v-for="(part, index) in showTable()" :key="part.id">
      <devices-table
      :value="part"
      :tableId="index"
      :workers="workers">
        <div slot-scope="table" slot="tableHead">
          <b-link style="width:100%" @click="toog(part.parts.id)">
            <span :id="'dp'+part.parts.id" style="display:none">+</span>
            <span :id="'dm'+part.parts.id">-</span>
          </b-link>
          <span :contenteditable="true" @blur="updateNameDevice($event, part.parts.id, part.parts.part_name_device)" @click.prevent.self>
            {{part.parts.part_name_device?part.parts.part_name_device:part.parts.part_name}}
          </span>
        </div>
      </devices-table>

      <devices-measurement
      :value="part"
      :tableId="index"
      :workers="workers">
        <div slot-scope="table" slot="tableHead"> 
          <b-link style="width:100%" @click="toogMeas(part.parts.id)">
            <span :id="'measurementProtocolClose'+part.parts.id" style="display:none">+ {{$t('measurement.measurementProtocol')}}</span>
            <span :id="'measurementProtocolOpen'+part.parts.id">- {{$t('measurement.measurementProtocol')}}</span>
          </b-link>
        </div>
      </devices-measurement>
      <br>
    </div>
  </div>
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
    'selectPerson'
  ],
  methods: {
    toog(val){
      console.log('dev'+val)
      console.log(document.getElementById('dev'+val))

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
    updateNameDevice(newVal, id, partName) {
      if(newVal.target.innerText != partName){
        axios.get('/updateNameDevice', {
          params: {
            nameDevice: newVal.target.innerText.replace(/[\s]{2,}/, ''),
            id: id
          }
        })
      }
    }, 
    showTable(){
      return this.value.filter((v)=>{
        if(v.parts.devices_content.length>0){
          return v
        }
      })
    }
  }
}
</script>