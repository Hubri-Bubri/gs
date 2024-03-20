<template>
  <b-container>
    <ModalEditor :image="initimage" @change="changeImage($event)" ref="zoneEditorModal" id="popup">
    </ModalEditor>
        
    <b-input-group class="pb-0 mb-0">
    <b-col cols="11" class="text-left p-2">
    <b-button @click="plus" size="sm"><b-icon icon="zoom-in"></b-icon></b-button>
    <b-button @click="minus" size="sm"><b-icon icon="zoom-out"></b-icon></b-button>
    <b-button  size="sm" @click="showquality=true" v-show="!showquality"><b-icon icon="image-fill"></b-icon></b-button>
    <b-form-input v-show="showquality" v-model="quality" @change="showquality=false" type="range" min="0" max="100" size="sm" style="max-width: 240px;padding-top: 15px;"></b-form-input>
    </b-col>
    <b-col cols="1" class="text-right">
    <print v-if="tmp.typeOfHead == 'Damage'"
    :windowPrint="windowPrint"
    :selectedCornty="selectedCornty"
    :project="project" :tmp="tmp"
    :account="account" :id="pid"
    :partx="[]" :head="tmp.typeOfHead"
    :addtaxColapsel="false"
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
    ></print>
  </b-col>
  </b-input-group>
    <div v-for="(table, index) in tables" :key="table.id">
      <damages-table :table="table" :quality="quality" :size="size" @edit="edit" :ref="'damage'+table.id" :id="tmp.id" :index="index" @switchDamagesGroup="switchDamagesGroup"></damages-table>
      <br />
    </div>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
    props: ['workers',
    'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList',
    'windowPrint', 'pid',
    'selectedCornty',
    'project',
    'tmp',
    'comments',
    'loadDamages',
    'account',
    'head',
    'addtaxColapse',
    'id',
    'customer',
    'person',
    'selectCustomer',
    'selectPerson'],

    data() {
      return {
        showDamagesGroup:0,
        tables:[],
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


      changeImage(e){
        axios.post('/updateImageDamage', {
          params: {
            newImage: e.dataUrl,
            schema: JSON.stringify(e.schema),
            id: this.cid
          }})
      },
      // updateDamage(newData, fild, id){
      //   axios.get('/updateDamage', {params: {
      //     newData: newData,
      //     fild: fild,
      //     id: id
      //   }})
      // },
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

      getTablesInDamages(id) {
        axios.get('/get_tables_in_damages', {
          params: {
            id: id
          }
        }).then(response => {
          this.tables = response.data
          if (response.data.length==0){
            this.$emit('switchDamages', false)
          }
        })
      },
      switchDamagesGroup(value, index){
        this.showDamagesGroup = this.showDamagesGroup + value

        if (this.tables.length==index+1) {
          if (this.showDamagesGroup==0){
            this.$emit('switchDamages', false)
          }
        }
      }
},

    
    mounted(){


      this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')


      if ((delimetr[0] == 'del_row_damage')||(delimetr[0] == 'del_table_damage')||(delimetr[0] == 'send_damage')) {
        delimetr[1].split(',').forEach((tableForReload)=>{
          this.$refs['damage'+tableForReload][0].getRowsInDamage(tableForReload)
          this.selectedTables=[]
        })
      }

      if (delimetr[0] == 'updateFildDamage') {
        var updateFild = (JSON.parse(data.data.split('updateFildDamage:')[1]))
        this.$refs['damage'+updateFild.table_id][0].getFild(updateFild)
      }
   }

   

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