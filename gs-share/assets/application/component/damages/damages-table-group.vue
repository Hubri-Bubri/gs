<template>
  <b-container>
      <b-modal size="xl" no-close-on-esc no-close-on-backdrop
      hide-header-close ref="zoneEditorModal" ok-only>
        <gs-paint :image="initimage" @change="changeImage($event)"></gs-paint>
      </b-modal>
            <!-- @ok="$refs.zoneEditor.printThis()+(setEdit=false)" -->

      {{tmp.typeOfHead}}
      <print v-if="tmp.typeOfHead == 'Damage'"
      :windowPrint="windowPrint"
      :selectedCornty="selectedCornty"
      :project="project" :tmp="tmp"
  
      :account="account" :id="pid"
      :disc='disc' :discP='discP'
      :tax='tax' :taxDub='taxDub'
      :taxP='taxP' :taxPDub='taxPDub'
      :netto='netto' :brutto='brutto'
      :butDiscPerc='butDiscPerc'
      :partx='value' :head="tmp.typeOfHead"
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
      >
      <b-col lg="6" md="12">


      </b-col>
<b-col class="cForm col-12 col-lg-4" style="padding:0px;" slot="Type">

</b-col>

<b-col class="cForm col-12 col-lg-4" style="padding:0px;" slot="Work">

</b-col>


</print>




    <div v-for="(part, index) in showTable()" :key="part.id">
      <damages-table
      :value="part"
      :tableId="index"
      :workers="workers"
      :index="index"
      @edit="edit"
      >
      <div slot-scope="table" slot="tableHead">

      <b-link v-b-toggle="'dev' + table.tableId" class="butMore" style="width:100%">
          <span class="when-opened">- {{part.parts.part_name}}</span>
          <span class="when-closed">+ {{part.parts.part_name}}</span>
      </b-link>

       <b-link  class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="delImageFromPart(value[index].parts.id)"/>
      </div>
      </damages-table>

            <br>
    </div>
   </b-container>
</template>

<script type="text/javascript">
import axios from 'axios';
export default {
    props: ['value', 'workers',
     'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList',
    'windowPrint', 'pid',
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
    'selectPerson'],
    data() {
      return {
          initimage:{
              url:null,
              schema: null
          },
          cid:null,
      }
    },
    methods: {
changeImage(e){
  axios.post('/updateImageDamage', {
    params: {
      newImage: e.dataUrl,
      schema: JSON.stringify(e.schema),
      id: this.cid
    }})
  },
  updateDamage(newData, fild, id){
    axios.get('/updateDamage', {params: {
      newData: newData,
      fild: fild,
      id: id
    }})
  },
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
hideWindowPrint(){
  this.$emit('hideWindowPrint')
},
openWindowPrint(){
  this.$emit('openWindowPrint')
},     

edit(content){
  this.$refs['zoneEditorModal'].show();
  this.initimage.url = '/image_edit?id='+content.imgId;
  // console.log(content.schema)
  this.initimage.schema = JSON.parse(content.schema);
  this.cid=content.id;
},


delImageFromPart(part){
  if (confirm("Are you sure?")){
    axios.get('/delImageFromPart', {
      params: {
        id: part
      }
    })
  }
},
      showTable(){
        return this.value.filter((v)=>{
          if(v.parts.damage_content.length>0){
            return v
          }
        })
      }
    }

}
</script>