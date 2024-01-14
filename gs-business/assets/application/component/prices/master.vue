<template>
    <container class="container-fluid">
        <container-header>
            <top-menu></top-menu>
        </container-header>
        <container-body>
     <b-modal size="md" centered id="move" ref="move" :title="$t('projectDetail.move')">
        <!-- @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" -->
         <b-form-select class="" id="move" v-model="selectedItems" :select-size="detectRowSise(items_menu)">
            <option v-for="item in detectItem(items_menu)" @click="selectedModal(item)">{{item.name}}</option>
         </b-form-select>

         <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="[$t('company.copy'), $t('company.move')]" />
         <template slot="modal-footer">
<!--             <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>-->
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button> 
         </template>
      </b-modal>
            <b-card :header="$t('projectDetail.priceList')" class="gs-container">
                 <container>
                    <container-body  style="overflow: unset;">
                        <!-- <b-container fluid> -->
                            <!-- <b-row>  -->
                                <!-- <div style="padding:0;width:29%;height:70%;overflow-y:auto;overflow-x:hidden;position:fixed;">  -->
      <!--                               <b-row class="border border-right-0 border-left-0" style="
                                    padding: 0px;font-size: 12px; border-bottom: 2px solid #dee2e6 !important;
                                    vertical-align: middle !important; border-spacing: 2px; border-color: grey;">
                                     <b-col> <b> Tree </b> </b-col>
                                    </b-row> -->

<!--     <vue-drag-tree :data='items_menu' :allowDrag='allowDrag' :allowDrop='allowDrop'  disableDBClick
    @drag="dragHandler" @drag-enter="dragEnterHandler"  @current-node-clicked="curNodeClicked"
    @drag-leave="dragLeaveHandler" @drag-over="dragOverHandler" @drag-end="dragEndHandler"
    @drop="dropHandler" :thrId="idNode" :parId="parId"></vue-drag-tree>  -->
<b-row>
  <b-col cols="3" class="block-1">
   <vue-drag-tree
    :data='items_menu'
   :allowDrag='allowDrag'
   :allowDrop='allowDrop'
   :idNode="idNode"

   disableDBClick
   @current-node-clicked='curNodeClicked'
   @drag="dragHandler"
   @drag-enter="dragEnterHandler"
   @drag-leave="dragLeaveHandler"
   @drag-over="dragOverHandler"
   @drag-end="dragEndHandler"
   @drop="dropHandler"
   >
    <!-- customize your node here if don't like the default / 如果你不喜欢默认样式，可以在这里定制你自己的节点 -->
<!--     <span :class="[slotProps.isClicked ? 'i-am-clicked' : 'i-am-not-clicked']"></span>
    <span class='i-am-node-name'>{{slotProps.nodeName}}</span> -->
    </vue-drag-tree>

</b-col>
<b-col cols="9" class="block-2">



                               <!--      <b-button @click="idNode=null; modshow(items_menu);">
                                        Clear
                                    </b-button>
 -->
                                <!-- </div>  -->
                                <!-- <div style="padding:0;width:30%;">&nbsp;</div> -->
                                <!-- <div style="padding:0; width:70%;background-color: white;" class="border border-right-0 border-top-0 border-bottom-0"> -->
                      
                            <!--              <b-table borderless  hover  class="tableProject fi" small   :items="items" :fields="fields"
                                         >
                                             <template slot="index" slot-scope="data" >
                                                <div @click="rowSelected(data.item)">
                                                {{ data.index + 1 }}
                                                </div>
                                              </template>
                                            <template slot="pos_num" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
                                            </template>
                                            <template slot="unit" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.unit" @change="updateDate($event, 'unit', row.item.id)"></b-input>
                                            </template>
                                            <template slot="price" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.price" @change="updateDate($event, 'price', row.item.id)"></b-input>
                                            </template>
                                            <template slot="without" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.without" @change="updateDate($event, 'without', row.item.id)"></b-input>
                                            </template>
                                            <template slot="percent" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.percent" @change="updateDate($event, 'percent', row.item.id)"></b-input>
                                            </template>
                                            <template slot="name" slot-scope="row">
                                                <b-input size="sm" style="min-width:150px;" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" @change="updateDate($event, 'name', row.item.id)"></b-input>
                                            </template>
                                            <template slot="desc" slot-scope="row">
                                                <div contenteditable="true"  @blur="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
                                            </template>
                                            <template slot="delete" slot-scope="row">
                                                   <b-link @click="delRow(row.item.id)" class="fas fa-trash fa-w-16 text-center" />
                                            </template> 
                                    </b-table> -->
<div class="sticky-header-lg b-table-sticky-header m-0 p-0">
  <b-table-simple hover  show-empty no-border-collapse stacked="lg">
  <b-thead>
    <b-tr  >
      <b-th v-for="(fild, index) in fields" :key="fild.key">{{fild.label}}</b-th>
    </b-tr>
  </b-thead>

    <draggable  :element="'tbody'" :options="{handle:'.handle',  group:'a', animation:150}"
                  :no-transition-on-drag="true" @end="checkMove" >
    <b-tr v-for="(tr, index) in items"  :key="tr.key" :variant="tr._rowVariant">
      <b-td @click="rowSelected(tr)" class="handle"> {{ index + 1 }}  </b-td>
      <b-td>
      <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @click.prevent.self
        @blur="updateDate($event.target.innerHTML, 'pos_num', tr.id)"
        v-html="tr.pos_num" />
      </b-td>
<!--         <b-input size="sm" :value="tr.pos_num" @change="updateDate($event, 'pos_num', tr.id)"></b-input></b-td> -->
      <!-- <b-td >
        <b-input size="sm" style="min-width:150px;" :style="(tr._rowVariant=='success')?rowColor:''"
        class="cForm-input" :value="tr.name" @change="updateDate($event, 'name', tr.id)"></b-input></b-td> -->


      <b-td style="width:35%">

  <div :style="'max-width:'+(width/3.8)+'px;width:100%;padding-left:4px;'"
  contenteditable="true" @click.prevent.self v-html="tr.name"
  @blur="updateDate($event.target.innerHTML, 'name', tr.id)" />

<!--         <b-form-textarea size="sm"
        rows="1"
        max-rows="8"
        :disabled="disablefild('priceName', tr.id)"
        :value="tr.name"
        @change="updateDate($event, 'name', tr.id)"
        /> -->
      </b-td>
<!--         <div  :contenteditable="!disablefild('priceName', tr.id)"
        @focus="changeDisable('f', 'priceName', tr.id)" @blur="updateDate($event.target.innerText, 'name', tr.id);changeDisable('b', 'priceName', tr.id);"
        
        :id="'priceName'+tr.id" >{{tr.name}}</div></b-td> -->
      <!-- <b-tooltip triggers="none" :show="disablefild('priceName', tr.id)" :target="'priceName'+tr.id">{{disablefildUser('priceName', tr.id)}}</b-tooltip> -->
      

      <b-td  style="width:35%">

  <div :style="'max-width:'+(width/3.8)+'px;width:100%;padding-left:4px;'"
  :contenteditable="true" @click.prevent.self v-html="tr.desc"
  @blur="updateDate($event.target.innerHTML, 'desc', tr.id)" />
<!--         <b-form-textarea size="sm"
        rows="1"
        max-rows="8"
        :disabled="disablefild('priceDesc', tr.id)"
        :value="tr.desc"
        @change="updateDate($event, 'desc', tr.id)"
        /> -->
<!-- 
        <div  :contenteditable="!disablefild('priceDesc', tr.id)"
        @focus="changeDisable('f', 'priceDesc', tr.id)"  @blur="updateDate($event.target.innerText, 'desc', tr.id);changeDisable('b', 'priceDesc', tr.id)"

        :id="'priceDesc'+tr.id" >{{tr.desc}}</div> -->
      </b-td>


      <b-td>
            <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @click.prevent.self
        @blur="updateDate($event.target.innerHTML, 'unit', tr.id)"
        v-html="tr.unit" />
        <!-- <b-input size="sm" :value="tr.unit" @change="updateDate($event, 'unit', tr.id)"></b-input> -->
      </b-td>
      <b-td>
            <div
        :id="'price-'+tr.id"
        contenteditable="true"
        class="diveditable"
        @click.prevent.stop="selectAll('price-'+tr.id)"
        @blur="updateDate($event.target.innerHTML, 'price', tr.id)"
        v-html="valueDigital(tr.price)" />
        <!-- <b-input size="sm" :value="tr.price" @change="updateDate($event, 'price', tr.id)"></b-input> -->
      </b-td>
<!--       <b-td>
            <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @click.prevent.self
        @blur="updateDate($event.target.innerHTML, 'without', tr.id)"
        v-html="valueDigital(tr.without)" />

      </b-td> -->
<!--       <b-td>
            <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @click.prevent.self
        @blur="updateDate($event.target.innerHTML, 'percent', tr.id)"
        v-html="valueDigital(tr.percent)" />
      </b-td> -->
      <b-td><b-link @click="delRow(tr.id)"><b-icon icon="trash" aria-hidden="true"></b-icon></b-link></b-td>
    </b-tr>
</draggable>
</b-table-simple>
</div>
</b-col>
</b-row>

                                    <div hidden>{{ selected }}</div>
                                <!-- </div> -->
                            <!-- </b-row> -->
                             
                        <!-- </b-container> -->
                        <!-- <a name="finishList"></a> -->
                    </container-body>
                </container>
                <b-card-footer>
                    <b-col cols="12">
                        <b-input-group>
                            <b-input-group-append>
                                <b-button @click="add">{{$t('projectDetail.plusPart')}}</b-button>
                                <b-button @click="remove">{{$t('projectDetail.remove')}}</b-button>
                            </b-input-group-append>
                           
                           <b-input-group-append>
                                <b-button @click="addRow">{{$t('projectDetail.plusRow')}}</b-button>
                                <b-button @click="mv_cp">{{$t('projectDetail.move')}}</b-button>
                            </b-input-group-append>

                                <b-form-input class="sqare" v-model="nameNode" :style="nodeDis?'background-color:grey':''"
                                @click.native="nodeDis?nodeDisTurn():''" @change="nodeDis=true;toModel(nameNode)"></b-form-input>
                     
                            
                        </b-input-group>
                    </b-col>
                </b-card-footer>
            </b-card>
        </container-body>
    </container>
</template>
<script>

import draggable from 'vuedraggable';
import axios from 'axios';
export default {
    components: {
        draggable
    },
  data(){
    return{
      idNode:-1,
      looks: [],
      nodeDis:true,
      moveToCopyRadio:'move',
      rowColor:'background-color:#c3e6cb',
      selected:[],
      items:[],
      nameNode:null,
      idNode:null,
      parId:null,
      triId:null,
      oldId:0,
      selectedItems:[],
          items_menu:[],
          drag1: null,
          drag2: null
    }

  },
   computed: {
    fields(){
      return[
      {
        key: 'index',
        label: '#',
        sortable: true
      },
      {
        key: 'pos_num',
        label: this.$t('lists.position'), 
        sortable: true
      },
      {
        key: 'name',
        label: this.$t('customerDetail.name'), 
        sortable: true
      },
      {
        key: 'desc',
        label: this.$t('calcTable.description'), 
        sortable: true
      },
      {
        key: 'unit',
        label: this.$t('calcTable.unit'), 
        sortable: true
      },
      {
        key: 'price',
        label: this.$t('lists.price'), 
        sortable: true
      },
                // {
                //     key: 'without',
                //     label: 'Without',
                //     sortable: true
                // },
                // {
                //     key: 'percent',
                //     label: '%',
                //     sortable: true
                // },
      {
        key: 'delete',
        label: this.$t('docs.delete')
      }
    ]
  }
    },
    methods: {
selectAll(id){
function selectElementContents(el) {
    var range = document.createRange();
    range.selectNodeContents(el);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
}

var el = document.getElementById(id);
selectElementContents(el);
},
    valueDigital(model){
      var value = model
      if (value == null){
        value = '0.0'
      }
      value = value.replace(',','.')
      // console.log(1, value)
      var value = parseFloat(value)
      // console.log(2, value)
      value = value.toString()
      value = value.replace('.',',')
      value = (value=='NaN')?0:value
      if (value.length < 3){
        value = '&nbsp;&nbsp;'+value+'&nbsp;&nbsp;'
        // console.log(4, value)
      }
      return value
    },
      updateWidth() {
        this.width = window.innerWidth;
      },
getLoocks(){
   axios.get('/getLoocks').then(response => {
      this.looks=[]
      this.looks = response.data
  })
},
      disablefildUser(fild, id){
        var result 
              this.looks.forEach((val)=>{
                    if (val.rows_id == id) {
                      if (val.fild == fild) {
                        result = val.user
                      }
                    }
                })
        return result
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
          return result
      },


      checkMove(event){
                     axios.get('/update_id_in_prise', {
                      params: {
                        newid: this.items[event.newIndex].id,
                        oldid: this.items[event.oldIndex].id
                      }
                  })
        },
        modshow(v){
            var items_menu = this.items_menu
            this.items_menu = []
            this.items_menu = items_menu
        },
       nodeDisTurn(){
          if (confirm(this.$t('alert.rename'))) {
               this.nodeDis = false
            }
       },
       getPrices(){
        if (this.idNode!=null){
            axios.get('/prices', {
                params: {
                    id:this.idNode?this.idNode:0
                }
            }).then(response => {
                this.items = response.data
            })
        }
        axios.get('/price_menu').then(response => {
            this.items_menu=[];
               response.data.forEach((val)=>{
                         if (val.parrent==0){
                            val['children']=[]
                            this.items_menu.push(val);
                        }
               });

                response.data.forEach((valResp)=>{
                  function findLevel(obj, id) {
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

        findLevel(this.items_menu, valResp.parrent)  
               });
            })
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
     curNodeClicked(model, component) { 
        this.nameNode = model.name,
        this.idNode = model.id,
        this.parId = model.parrent
        // console.log(this.idNode == this.oldId)
        // console.log(this.idNode, this.oldId)
        if(this.idNode == this.oldId){
          if (this.items.length>0){
                this.items=[]
          } else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
            }).then(response => {
                 this.items = response.data
            })
          }
        }else{
            axios.get('/prices', {
                 params: {
                     id: model.id
                 }
             }).then(response => {
                 this.items = response.data
             })
        }
        this.oldId = this.idNode
        if ((model.parrent == 0) && component.folder == false){
            this.idNode = null
        }
    },
    curNodeClickedModal(model, component){
        this.idNodeModal=model.id
    },
    toModel(enterVal){
        function findLevel(obj, id) {
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/update_name_price_menu', {
                        params: {
                            name: enterVal,
                            id: id
                        }
                    })
                } else {
                    if (val.children.length!=0){
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.items_menu, this.idNode)
    },
    remove(){
       if (this.idNode==null){
            alert(this.$t('alert.noItemSelectForDel'))
       }
       else {
            if (confirm(this.$t('alert.remove'))) {
                axios.get('/remove_price_menu', {
                    params: {
                        remove_id: this.idNode
                    }
                }).then(response=>{
                    this.idNode=null,
                    this.nameNode=null
                })
            }
        }
    },
    add(){

      function findLevel(obj, id) {
        if (id==null){
            id=0,
            obj.push({id:0, children:[]})
        }
            obj.forEach((val)=>{
                if (val.id==id){
                    axios.get('/add_price_menu', {
                        params: {
                            parent_id: val.id
                        }
                    })
                } else {
                    if(val.children.length!=0) {
                        findLevel(val.children, id)
                    }
                }
            })
        }

        findLevel(this.items_menu, this.idNode)
        
        
       
    },
    addRow(){
        if (this.idNode==null){
            alert(this.$t('alert.noSelectedForAdd'))
        } else {
            axios.get('/add_price', {
                params: {
                    id: this.idNode
                }
            })
        }

    location.href = "#finishList"

    },
    delRow(id){
        if (confirm(this.$t('alert.remove'))) {
            axios.get('/remove_price', {
                params: {
                    id: id
                }
            })
        }
    },
    updateDate(data, fild, id){
        axios.get('/update_price', {
            params: {
                data: data,
                fild: fild,
                id: id
            }
        })
    },
    rowSelected(items) {
         if(this.selected.indexOf(items)==-1){
            this.selected = this.selected.filter((v)=>{
                if (v.id != items.id){
                    return v
                }
            });
            this.selected.push(items);
            items._rowVariant='success';
         } else{
            this.selected.splice(this.selected.indexOf(items), 1)
            items._rowVariant=''
         }
    },
    mv_cp(){
        if (this.idNode==null){
            alert(this.$t('alert.noItemSelect'))
        } else{
            if (this.selected.length==0){
                alert(this.$t('alert.noRowsSelected'))
            }
        }
        if ((this.idNode!=null)&&(this.selected.length!=0)){
            this.$refs.move.show()           
        }
    },
    okMoveToCopy(){
        this.selected=[],
        this.$refs.move.hide()
    },
    detectItem(items){
      var returnArr=[]
      var addCount=''
      function findLevel(obj) {
            obj.forEach((val)=>{
                    returnArr.push({name: addCount+val.name, id: val.id})
                    if(val.children.length!=0) {
                        addCount=addCount+"-"
                        findLevel(val.children)
                    } else{addCount=''}
            })
        }

        findLevel(items)  
        return returnArr
    },
    detectRowSise(items){
      var returnArr=[]
      var addCount=''
      function findLevel(obj) {
            obj.forEach((val)=>{
                    returnArr.push({name: addCount+val.name, id: val.id})
                    if(val.children.length!=0) {
                        addCount=addCount+"-"
                        findLevel(val.children)
                    } else{addCount=''}
            })
        }

        findLevel(items)  
        return returnArr.length
    },
    selectedModal(val){
        var price_ids=[]
        if (confirm(this.$t('alert.to')+" "+this.moveToCopyRadio+' '+this.selected.length+
            ' rows in to '+val.name+"?")) {
            this.selected.forEach((val)=>{
                price_ids.push(val.id)
            })
             axios.get('/cp_mv_to_price', {
                 params: {
                     price_ids: price_ids.join(),
                     new_menu: val.id,
                     operation: this.moveToCopyRadio
                 }
             })
        }
    },
     dragHandler(model, component, e) {
    
    //    // console.log('dragHandler: ', model, component, e);
     },
    
     dragEnterHandler(model, component, e) {
    //    //  console.log('dragEnterHandler: ', model, component, e);
     },
    
     dragLeaveHandler(model, component, e) {
    //    // console.log('dragLeaveHandler: ', model, component, e);
     },
    
     dragOverHandler(model, component, e) {
    //    // console.log('dragOverHandler: ', model, component, e);
     },
    
    dragEndHandler(model, component, e) {
        console.log('dragEndHandler: ', model, component, e);
        this.drag1=model.id;
        // console.log(this.drag1, this.drag2);
        // axios.get('/change_parrent_menu', {
        //     params: {
        //         drag1: this.drag1,
        //         drag2: this.drag2
        //     }
        // }).then(response=>{
        //     this.drag1=null;
        //     this.drag2=null;          
        // })
    },
    
    dropHandler(model, component, e) {
       // console.log('dropHandler: ', model, component, e);
        this.drag2=model.id;
    }
  },
  
    
mounted(){
    window.addEventListener('resize', this.updateWidth);
    this.updateWidth();
  setTimeout(() => {
        this.$socket.send('getPrices')
        this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
        this.$options.sockets.onmessage = (data) => (data.data=='getLoocks') ? (this.getLoocks()): ''
        },1000);

        }
    }
</script>
/*<style type="text/css">

</style>*/