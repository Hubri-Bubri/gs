
<template>
    <container>
        <b-card-group deck  style="width: 100%; margin:0px;">
            <b-card no-body class="gs-container">
                <b-tabs card style="min-height: 97vh;">
                    <b-tab :title="workerName">
      
                        <container-body>
                            <b-row class="m-2 p-2">
                                <b-col lg="3" cols="12" >
                                    <vue-drag-tree
                                    :data='itemsMenuImag'
                                    :allowDrag='allowDrag'
                                    :allowDrop='allowDrop'
                                    :idNode="idNodeImg"
                                    disableDBClick
                                    @current-node-clicked="pcurNodeClickedImg"
                                    >
                                    </vue-drag-tree>
                                </b-col>
                                <b-col cols="12" class="d-lg-none">&nbsp;</b-col>
                                <b-col lg="9" cols="12">


   <b-input-group class="pb-0 mb-0">
    <b-col cols="12" class="text-right p-2">
    <b-button @click="plus" size="sm"><b-icon icon="zoom-in"></b-icon></b-button>
    <b-button @click="minus" size="sm"><b-icon icon="zoom-out"></b-icon></b-button>
     <b-button  size="sm" @click="showquality=true" v-show="!showquality"><b-icon icon="image-fill"></b-icon></b-button>
    <b-form-input v-show="showquality" v-model="quality" @change="showquality=false" type="range" min="0" max="100"
    size="sm" style="max-width: 240px;padding-top: 15px;"></b-form-input>
    </b-col>
  </b-input-group>
  <!-- <b-col cols="12"> -->
<b-card-group columns v-viewer class="images" :style="'column-count: '+size+';'">
  <b-card v-for="(row, index) in foldershowfiles(domageImages)" :key="row.id" :img-src="row.id+'&q='+quality"
  @click.stop="showx('images', index)" class="cardimg text-justify"
  :border-variant="(row._rowVariant=='success')?'warning':''"
  :bg-variant="(row._rowVariant=='success')?'warning':''">
    <b-card-text @click.stop="$emit('imageInTableSelected', row)" style="cursor:pointer">
      {{row.date.split(' ')[1]}}
      <b-icon icon="trash" aria-hidden="true" @click.stop="filedel(row.id.split('=')[1])"  />
    </b-card-text>
  </b-card>
</b-card-group>

                                </b-col>
                            </b-row>
                        </container-body>
                        <container-footer>
                            <vue-dropzone ref="myVueDropzone" id="dropzone"
                            :options="dropzoneOptions"
                            v-on:vdropzone-sending="sendingEventImage"
                            v-on:vdropzone-success="fsadd"
                            :forceFallback="true">
                            </vue-dropzone>
                        </container-footer>
                    </b-tab>
                </b-tabs>
            </b-card>
        </b-card-group>
    </container>
</template>
<script type="text/javascript">
import axios from 'axios';
import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.min.css';
export default {
    components: {
        vueDropzone: vue2Dropzone
    },
    props: {
        id: String,
        user: String,
        foolder: String
    },
    data() {
        return {
        foolderId:-1,
        projectId:null,
        wwidth:null,
        size:6,
        quality:0,
        showquality:false,
        domageImages:[],
        optImages:[],
        idNodeImg:-1,
        images_menu_ids:[],
        itemsPriceImg:[],
        oldIdImg:0,
        itemsMenuImag:[],
        // selectedPriceImg:[],
        menuImgsTree: false,
        docs_menu_ids:[],
        workerName:null ,
        modalFiles:[],
        itemsTable:[],
dropzoneOptions: {
            url: 'loadFilesWorkers',
            // thumbnailWidth: 50,
            parallelUploads:50,
              thumbnailWidth: 250,
              thumbnailHeight: 250,
            // uploadMultiple: true,
            // timeout:1,
            chunkSize:100,
            // forceFallback:true,
            forceChunking:true,
            dictDefaultMessage: this.$t('alert.clickOrDrop'),
            acceptedFiles: 'image/*',
            accept: function(file, done) {
                // this.$refs.myVueDropzone.removeFile(file)
                // console.log("uploaded"); //debuging the upload
                done();
            },
        },

        docs: [],
        files: [],

        project: {
            number: null,
        },
        tmp: {
            number: null,
            },
        } //return
    }, //data
    sockets:{
        connect: function(){
          console.log('socket connected')
        },
        customEmit: function(val){
          console.log('this method fired by socket server. eg: io.emit("customEmit", data)')
        }
    },
    computed: {
        fieldsImages() {
            return[{   
                key: 'id',
                label: this.$t('docs.images'),
                sortable: true,
                thClass:''
            },
            {
                key: 'date',
                label: this.$t('docs.added'),
                sortable: true,
                thClass:''
            },
            {
                key: 'user',
                label: this.$t('docs.user'),
                sortable: true,
                thClass:''
            },
            {
                key: 'delete',
                label: this.$t('docs.delete'),
                thClass:''
            }]},
    },
    methods: {
    plus(){
      this.size=this.size-1;
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs.heightTableImages.clientHeight, 250);
      }, 200);     
    },
    minus(){
      this.size=this.size+1;
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs.heightTableImages.clientHeight, 250);
      }, 200);    
    },
    foldershowfiles(val){
        // console.log(val)
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
    },

    allowDrag(model, component) {
      if (component.depth!=1){
      // if (model.name === 'Node 0-1') {
      // can't be dragged
        return true;
      }
      // can be dragged
      return false;
    },
    allowDrop(model, component) {
      if (component.depth==1){
      // can't be placed
        return true;
      }
      // can be placed
      return false;
    },
    allowDragModal(model, component) {
      return false;
    },
    allowDropModal(model, component) {
      return false;
    },   
    // curNodeClicked(model, component) { 
    //   this.$emit('pcurNodeClickedImg', model, component)  
    // },
    curNodeClickedModal(model, component){
      this.idNodeModal=model.id
    },
    dragHandler(model, component, e) {
      // console.log('dragHandler: ', model, component, e);
    },
    dragEnterHandler(model, component, e) {
      // console.log('dragEnterHandler: ', model, component, e);
    },
    dragLeaveHandler(model, component, e) {
      // console.log('dragLeaveHandler: ', model, component, e);
    },
    dragOverHandler(model, component, e) {
      // console.log('dragOverHandler: ', model, component, e);
     },
    dragEndHandler(model, component, e) {
    // console.log('dragEndHandler: ', model, component, e);
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
       // console.log('dropHandler: ', model, component, e);
      this.drag2=model.id;
    },
























        filedel(val) {
            if (confirm(this.$t('alert.sure'))) {
                axios.get('/delfile', {
                    params: {
                        id: val
                    }
                }).then(response => {});
            }
        },
        // prowSelectedImg(items) {
        //     if(this.selectedPriceImg.indexOf(items)==-1){
        //         this.selectedPriceImg = this.selectedPriceImg.filter((v)=>{
        //             if (v.id != items.id){
        //                 return v
        //             }
        //         });
        //         this.selectedPriceImg.push(items);
        //         items._rowVariant='success';
        //     } else{
        //         this.selectedPriceImg.splice(this.selectedPriceImg.indexOf(items), 1)
        //         items._rowVariant=''
        //     }
        // },
        pcurNodeClickedImg(model, component) {
        // console.log(model, component)
            // this.nameNodeImag = model.name,
            this.idNodeImg=model.id
            if(this.idNodeImg == this.oldIdImg){
                 if (this.itemsPriceImg.length>0){
                    this.itemsPriceImg=[]
                } else{
                axios.get('/show_imgs', {
                     params: {
                         id: model.id
                     }
                 }).then(response => {
                     this.itemsPriceImg = response.data;

                 })
                }
            }else{
                axios.get('/show_imgs', {
                     params: {
                         id: model.id
                     }
                 }).then(response => {
                     this.itemsPriceImg = response.data;

                 })
            }
            this.oldIdImg = this.idNodeImg
            if ((model.parrent == 0) && component.folder == false){
                this.idNodeImg = null
            }
        },
        getdomageImages(){
       if (this.projectId != null ){ 
       axios.get('/domage_images', {
          params: {
            id: this.projectId,
            project: (this.project.number==null)?'0001':this.project.number
          }
        }).then(response => {
        this.domageImages = response.data.filter(function (v){
          if((v.file_name.split('.')[v.file_name.split('.').length-1]) != 'pdf'){ return v}
        })

        })
        }
        // console.log((this.project.number==null)?'0001':this.project.number, this.domageImages )
      },
        getDocs(){
            if (this.projectId != null) {
            axios.get('/images_menu', {
                params: {
                    project:this.projectId
                }
            }).then(response => {
                this.itemsMenuImag=[];
                this.itemsMenuImag.push({id: -1, name: 'General Folder', parrent: 0, children:[]});
                this.images_menu_ids.push(-1);
                response.data.forEach((val)=>{
                    if (val.parrent==0){
                        val['children']=[]
                        this.itemsMenuImag.push(val);
                    }
                });
                response.data.forEach((valResp)=>{
                    function findLevel(obj, id)  {
                        obj.forEach((val)=>{
                            if (val.id==id){
                                valResp['children']=[]
                                val.children.push(valResp);
                            } else{
                                if (val.children.length!=0){
                                    findLevel(val.children, id)
                                }
                            }
                        })
                    }
                    this.images_menu_ids.push(valResp.id);
                    findLevel(this.itemsMenuImag, valResp.parrent)  
               });
            })
        this.getdomageImages();
        }
    },
    showx(classId, index){
      const viewer = this.$el.querySelector('.'+classId).$viewer
      viewer.index = index
      viewer.show()

    },
    fsadd() {
// this.items.forEach((n, i) => setTimeout(() => n.show = true, i * 1000));


this.$refs.myVueDropzone.dropzone.getAcceptedFiles().forEach((file, i) => setTimeout(() => this.$refs.myVueDropzone.removeFile(file), i * 250));
// {   
//     this.$refs.myVueDropzone.removeFile(file);
// });

        // this.$refs.myVueDropzone.removeAllFiles()
    },
        sendingEventImage(file, xhr, formData) {
            var selectTables = []
            // this.partx.forEach(function(val, index) {
            //     if (val.parts.toggle) {
            //         selectTables.push(val.parts.id)
            //     }
            // })
            xhr.setRequestHeader('X-Number', this.project.number);
            xhr.setRequestHeader('X-Folder', this.foolderId);
            xhr.setRequestHeader('X-id', this.projectId);
            xhr.setRequestHeader('X-User',  this.workerName);
        },
    getProjectDetail(old){
        axios.get('/get_workers').then(response => {
          response.data.filter((v)=>{
            
            if (v.id==this.user){
               this.workerName = (v.short_name!=null)?v.short_name:v.name

            }
          })
        })
        axios.get('/project_user', {
            params: {
                id: this.id
            }
        }).then(response => {
            this.projectId = response.data.id
            this.getDocs()
            if (response.data!=null){
                        var num = response.data.project_number
                      var nuls=3-num.toString().length
                      for (var i = 0; i <= nuls; i++) {
                          num='0'+num
                      }

            this.project.number=num+'-'+response.data.project_number_year,
            this.getdomageImages()
            
            }
        })
    }
    },
    mounted(){
    this.getProjectDetail(1)
    

    setTimeout(() => {
        // this.$socket.send('getProjectDetail')
        this.$options.sockets.onmessage = (data) => (data.data=='getProjectDetail') ? (this.getProjectDetail(1)): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getDocs') ? this.getDocs(): ''

        this.itemsMenuImag[0].children.forEach((val)=>{

            if (val.name == this.foolder.replace('_', ' ')) {
                // console.log(val, this.foolder.replace('_', ' '))
                this.foolderId = val.id
            }
        })
            this.idNodeImg=parseInt(this.foolderId)


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

        },1000);
        },
        created: function() {
      const onResize = () => this.wwidth = window.innerWidth; //После определения ширина окна и  мобильного режима, должна примениться рассчитаная длина списка
      onResize();
      window.addEventListener('resize', onResize);
      this.$once('hook:beforeDestroy', () => window.removeEventListener('resize', onResize));
    }
}
</script>