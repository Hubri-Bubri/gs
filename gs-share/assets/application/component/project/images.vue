<template>
  <b-container fluid :ref="heightImages">
      <b-row >
      <b-col lg="3" cols="12" class="block-1">
        <vue-drag-tree
        :data='itemsMenuImag'
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :idNode="idNodeImg"
        disableDBClick
        @current-node-clicked="curNodeClicked"
        @drag-end="dragEndHandler"
        @drop="dropHandler">
        </vue-drag-tree>
        <div hidden>{{selectedPriceImg}}</div>
      </b-col>
      <b-col lg="9" cols="12" class="block-2 m-0 pr-4" style="overflow-y:auto;">
    <b-input-group class="pb-0 mb-0">
    <b-col cols="12" class="text-right p-2">
    <b-button @click="plus" size="sm"><b-icon icon="zoom-in"></b-icon></b-button>
    <b-button @click="minus" size="sm"><b-icon icon="zoom-out"></b-icon></b-button>
    <b-button  size="sm" @click="showquality=true" v-show="!showquality"><b-icon icon="image-fill"></b-icon></b-button>
    <b-form-input v-show="showquality" v-model="quality" @change="showquality=false" type="range" min="0" max="100" size="sm" style="max-width: 240px;padding-top: 15px;"></b-form-input>
    </b-col>
  </b-input-group>
<b-card-group columns v-viewer class="images" :style="'column-count: '+size+';'">
  <b-card v-for="(row, index) in foldershowfiles(domageImages)" :key="row.id" :img-src="row.id+'&q='+quality" 
  @click.stop="showx('images', index)" class="cardimg text-justify" :border-variant="(row._rowVariant=='success')?'warning':''"
  :bg-variant="(row._rowVariant=='success')?'warning':''">
    <b-card-text @click.stop="$emit('imageInTableSelected', row)" style="cursor:pointer">
      {{row.date.split(' ')[1]}}
      <b-icon icon="trash" aria-hidden="true" @click.stop="filedel(row.id.split('=')[1])"  />
    </b-card-text>
  </b-card>
</b-card-group>
</b-col>
    </b-row>
  </b-container>
</template>
<script type="text/javascript">
export default {
  props: ['domageImages', 'idNodeImg', 'itemsMenuImag', 'selectedPriceImg', 'wwidth', 'heightTableImages'],
    data() {
      return {
        heightImages:null,
        size:6,
        quality:0,
        showquality:false
      }
    },
  methods: {
    plus(){
      this.size=this.size-1;
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs[this.heightImages].clientHeight, 250);
      }, 200);     
    },
    minus(){
      this.size=this.size+1;
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs[this.heightImages].clientHeight, 250);
      }, 200);    
    },
    foldershowfiles(val){
      if (this.idNodeImg != undefined){
        return val.filter((itemImg)=>{
          if (this.idNodeImg!=-1){
            if(this.idNodeImg==itemImg.folder_id){
              return itemImg
            }
          }
          if (this.idNodeImg==-1) {
            if((itemImg.folder_id==null)|(itemImg.folder_id==-1)){
              return itemImg
            }
          }
        })
      }
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs[this.heightImages].clientHeight, 250);
      }, 200);  
    },
    loded(){
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs[this.heightImages].clientHeight, 250)
      }, 200);     
    },
    allowDrag(model, component) {
      if (component.depth!=1){
        return true;
      }
      return false;
    },
    allowDrop(model, component) {
      if (component.depth==1){
        return true;
      }
      return false;
    },
    allowDragModal(model, component) {
      return false;
    },
    allowDropModal(model, component) {
      return false;
    },   
    curNodeClicked(model, component) { 
      this.$emit('pcurNodeClickedImg', model, component)  
    },
    curNodeClickedModal(model, component){
      this.idNodeModal=model.id
    },
    dragEndHandler(model, component, e) {
      this.drag1=model.id;
      axios.get('/change_parrent_menu_devices', {
        params: {
          drag1: this.drag1,
          drag2: this.drag2
        }
      }).then(response=>{
        this.drag1=null;
        this.drag2=null;          
      })
    },
    dropHandler(model, component, e) {
      this.drag2=model.id;
    },
    changeDisable(type_operation, fild, id){
      this.$emit('changeDisable', type_operation, fild, id)
    },
    filedel(val) {
      this.$emit('filedel', val)
    },
    image_in_table_selected(item){
      this.$emit('imageInTableSelected', item)
    },
    showx(classId, index){
      this.$emit('showx', classId, index)
    },
    updatefilename(val, type, id){
      this.$emit('updatefilename', val, type, id)
    },
  },mounted(){
    this.$options.sockets.onmessage = (data) => (data.data=='getDocs') ? this.$emit('getDocs'): '';
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
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs[this.heightImages].clientHeight, 250);
      }, 1500);
    }, 200);     
  }
}
</script>