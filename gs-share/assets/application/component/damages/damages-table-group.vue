<template>
  <b-container>
    <ModalEditor :image="initimage" @change="changeImage($event)" ref="zoneEditorModal" id="popup">
    </ModalEditor>
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
      ref="print"
      >
        <b-col lg="6" md="12"> 
          <b-input-group class="pb-0 mb-0">
    <b-col cols="12" class="text-left p-2">
    <b-button @click="plus" size="sm"><b-icon icon="zoom-in"></b-icon></b-button>
    <b-button @click="minus" size="sm"><b-icon icon="zoom-out"></b-icon></b-button>
    <b-button  size="sm" @click="showquality=true" v-show="!showquality"><b-icon icon="image-fill"></b-icon></b-button>
    <b-form-input v-show="showquality" v-model="quality" @change="showquality=false" type="range" min="0" max="100" size="sm" style="max-width: 240px;padding-top: 15px;"></b-form-input>
    </b-col>
  </b-input-group>
          

  
  
  </b-col>

        
        <b-col class="cForm col-12 col-lg-4" style="padding:0px;" slot="Type"></b-col>
        <b-col class="cForm col-12 col-lg-4" style="padding:0px;" slot="Work"></b-col>
      </print>
    <div v-for="(part, index) in showTable()" :key="part.id">
      <damages-table
      :value="part"
      :tableId="part.parts.damage_content"
      :nowTableId="value"
      :workers="workers"
      :index="index"
      :quality="quality"
      :size="size"
       @edit="edit"
      >
        <div slot-scope="table" slot="tableHead">
          <b-link style="width:100%" @click="toog(value[index].parts.id)">
            <span :id="'dp'+value[index].parts.id" style="display:none">+ {{value[index].parts.part_name}}</span>
            <span :id="'dm'+value[index].parts.id">- {{value[index].parts.part_name}}</span>
          </b-link>
          <b-icon icon="trash" aria-hidden="true" @click="delImageFromPart(value[index].parts.id)"></b-icon>
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

        heightImages:null,
        size:300,
        quality:0,
        showquality:false,

          initimage:{
              url:null,
              schema: null
          },
          cid:null,
      }
    },
    methods: {

      plus(){
      this.size=this.size+10;
  
    },
    minus(){
      this.size=this.size-10;
   
    },

      toog(val){
        document.getElementById('dm'+val).style.display = document.getElementById('damage'+val).style.display = (document.getElementById('damage'+val).style.display=='none') ? '' : 'none'
        document.getElementById('dp'+val).style.display = (document.getElementById('dm'+val).style.display=='none') ? '' : 'none'
      },
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
    },
    mounted(){
    this.heightImages='hi'+(Math.ceil(Math.random()*1000000))
    setTimeout(() => {
          if(this.wwidth<=768){
            this.size = 2
          }else{
            this.quality = 50
            if(this.wwidth<=1200){
              this.size = 3
            }else{
              if(this.wwidth<=1400){
                this.size = 4
              }else{
                if(this.wwidth<=1600){
                this.size = 5
                }else{
                  if(this.wwidth<=1800){
                    this.size = 6
                  }
                }
              }
            }
          }

    }, 200);     
  }

}
</script>