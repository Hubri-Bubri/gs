<template>
 <b-container fluid >

    <b-modal size="md" centered id="column" ref="column" title="Edit Column">
      <b-row>
        <b-col>
          <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="newFields" stacked :options="opt(fields)"/>
        </b-col>
        <b-col class="text-center">
          <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="newFields1" stacked :options="opt(fields1)"/>
               <b-button class="btn btn-light" @click="hideColumnfunc()">
                {{hideColumn?'hide':'show'}} this column
        </b-button>
        </b-col>
    </b-row>

         <template slot="modal-footer">
            <button type="button" class="btn btn-primary" @click="okColumn">OK</button> 
         </template>
      </b-modal>

                       
                            <b-row>

                               <b-collapse v-model="menuPriceTree" id="priceMenu"
                               v-click-outside="onClickOutside"
                                :style="'padding:0;position:fixed;z-index:10;top:'+howhight+'px;left:'+((howhight==37)?'16':'109')+'px;border-style: ridge;'">

                                    <b-row class="border border-right-0 border-left-0" style="
                                    padding: 0px;font-size: 12px; border-bottom: 2px solid #dee2e6 !important; margin: 0px;
                                    vertical-align: middle !important; border-spacing: 2px; border-color: grey; background-color:white;">
                                     <b-col> <b> Tree </b> </b-col>
                                    </b-row>
<vue-drag-tree
:data='itemsMenu'
:allowDrag='allowDrag'
:allowDrop='allowDrop'
:thrId="idNode"
:parId="parId"
disableDBClick
@drag="dragHandler"
@drag-enter="dragEnterHandler"
@current-node-clicked="curNodeClicked"
@drag-leave="dragLeaveHandler"
@drag-over="dragOverHandler"
@drag-end="dragEndHandler"
@drop="dropHandler">
<!-- 

    <i :class="[slotProps.isClicked ? 'fa fa-folder' : 'fa fa-folder']"
    style="font-size: 14px; color: #fd7e14;padding-left:10px;"></i>
    <span style="font-size: 14px;padding-left:10px;white-space: nowrap">{{slotProps.nodeName}}</span> -->

</vue-drag-tree>                              

</b-collapse>
                                <!-- <div style="width:100%;background-color: white;" class="border border-right-0 border-top-0 border-bottom-0"> -->

<div style="text-align: right;width:99%">
         <b-button size="sm" class="cForm-inputG" variant="outline-secondary" @click="hidePosition">
                                                    <i class="fas fa-columns">
                                                    </i>
                                                </b-button>
</div>

<!-- <div style="display:inherit;width100%">
 -->
<b-col :cols="hideColumn?6:12">
<b-table borderless  hover  class="tableProject" small :items="items" :fields="getFields(fields, newFields)"   v-columns-resizable>
                                             <template slot="&#35;" slot-scope="data" >
                                                <div @click="rowSelected(data.item)">
                                                {{ data.index + 1 }}
                                                </div>
                                              </template>
                                            <template slot="pos_num" slot-scope="row">
                                                <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
                                            </template>
                                                 <template slot="name" slot-scope="row">
                                                <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" @change="updateDate($event, 'name', row.item.id)"></b-input> -->
                                                <div :style="(row.item._rowVariant=='success')?rowColor:''+';width:100%;min-width:150px;'" contenteditable="true"  @blur="updateDate($event.target.innerText, 'name',  row.item.id)">{{row.item.name}}</div>
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
                                            
                                            <template slot="show_details" slot-scope="row">
                                                   <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
                                                        {{ row.detailsShowing ? '-' : '+'}}
                                                   </b-link>
                                            </template>
                                            <template slot="delete" slot-scope="row">
                                                   <b-link @click.prevent.stop="delRow(row.item.id)" class="fas fa-trash fa-w-16 text-center" />
                                            </template>
                                       
<!--                                             <template slot="row-details" slot-scope="row">
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @keyup.native="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
                                            </template> -->
                                            <template slot="row-details" slot-scope="row">
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
                                            </template>
                                    </b-table>
                                    
</b-col><b-col cols="6" v-show="hideColumn">
 <b-table borderless  hover  class="tableProject" small   :items="selectedPrice" :fields="getFields(fields1, newFields1)"   v-columns-resizable>
                                             <template slot="&#35;" slot-scope="data">
                                                <div @click="rowSelected(data.item)">
                                                  {{ data.index + 1 }}
                                                </div>
                                              </template>
                                            <template slot="pos_num" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" ></b-input>
                                            </template>
                                               <template slot="name" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" ></b-input>
                                            </template>
                                            <template slot="unit" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.unit" ></b-input>
                                            </template>
                                            <template slot="price" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.price" ></b-input>
                                            </template>
                                            <template slot="without" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.without"></b-input>
                                            </template>
                                            <template slot="percent" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.percent" ></b-input>
                                            </template>
                                         
                                            <template slot="show_details" slot-scope="row">
                                                   <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
                                                        {{ row.detailsShowing ? '-' : '+'}}
                                                   </b-link>
                                            </template>
                                           <!--  <template slot="delete" slot-scope="row">
                                                   <b-link @click.prevent.stop="delRow(row.item.id)" class="fas fa-trash fa-w-16 text-center" />
                                            </template> -->
                                            <template slot="row-details" slot-scope="row">
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" >{{row.item.desc}}</div>
                                            </template>
                                    </b-table>
   </b-col>  

                           
<!-- </div> -->
                                <!-- </div> -->
                            </b-row>
                       
                           <a name="finishList"></a>

                        
         
               </b-container>
                

</template>
<script>
import axios from 'axios';
import vClickOutside from 'v-click-outside';
export default {
    directives: {
      clickOutside: vClickOutside.directive
    },
    props: ['howhight', 'idNode', 'parId', 'items', 'itemsMenu', 'selectedPrice', 'menuPriceTree'],

  data(){
    return{
      // newFields:['&#35; ', 'Position', 'Name', 'i', 'Unit', 'Price', 'Without', '%', 'Del'],
      // newFields1:['&#35; ', 'Position', 'Name', 'i', 'Unit', 'Price', 'Without', '%'],
      newFields:['&#35; ', 'Position', 'i', 'Name', 'Price'],
      newFields1:['&#35; ','Name'],
      // menuPriceTree:false,
      // nodeDis:true,
      
      rowColor:'background-color:#c3e6cb',
      
      // items:[],
      // nameNode:null,
      // idNode:null,
      // parId:null,
      // oldId:0,
      hideColumn:false,
      
      fields: [{
                    key: '&#35;',
                    label: '&#35; ',
                    tdClass: 't_index_comp',
                    sortable: true
                },
                {
                    key: 'pos_num',
                    label: 'Position',
                    tdClass: 't_pos_num_comp',
                    sortable: true
                },
                          {
                    key: 'name',
                    label: 'Name',
                    tdClass: 't_name_comp',
                    sortable: true
                },
                {
                    key: 'show_details',
                    label: 'i',
                    tdClass: 't_desc_comp'
                },
                {
                    key: 'unit',
                    label: 'Unit',
                    tdClass: 't_unit_comp',
                    sortable: true
                },
                {
                    key: 'price',
                    label: 'Price',
                    tdClass: 't_price_comp',
                    sortable: true
                },
                {
                    key: 'without',
                    label: 'Without',
                    tdClass: 't_without_comp',
                    sortable: true
                },
                {
                    key: 'percent',
                    tdClass: 't_percent_comp',
                    label: '%',
                    sortable: true
                },
                {   key: 'delete',
                    label: 'Del',
                    tdClass: 't_del_comp'
                },
      
            ],
            fields1: [{
                    key: '&#35;',
                    label: '&#35; ',
                    tdClass: 't_index_comp',
                    sortable: true
                },
                {
                    key: 'pos_num',
                    label: 'Position',
                    tdClass: 't_pos_num_comp',
                    sortable: true
                },
                        {
                    key: 'name',
                    label: 'Name',
                    // tdClass: 't_name_comp',
                    sortable: true
                },
                {
                    key: 'show_details',
                    label: 'i',
                    tdClass: 't_desc_comp'
                },
                {
                    key: 'unit',
                    label: 'Unit',
                    tdClass: 't_unit_comp',
                    sortable: true
                },
                {
                    key: 'price',
                    label: 'Price',
                    tdClass: 't_price_comp',
                    sortable: true
                },
                {
                    key: 'without',
                    label: 'Without',
                    tdClass: 't_without_comp',
                    sortable: true
                },
                {
                    key: 'percent',
                    tdClass: 't_percent_comp',
                    label: '%',
                    sortable: true
                },
        

            ],

      fieldsForTable:[],
      fields1ForTable:[],
          // itemsMenu:[],
          drag1: null,
          drag2: null
    }

  },
    methods: {
    rowSelected(items) {
      this.$emit('rowSelected', items)  
    },
      hideColumnfunc(){
        this.hideColumn=this.hideColumn?false:true
      },
      getFields(val, val1){
        var retFilds=[]
        val.forEach((v)=>{
          var same = 0
          val1.forEach((v1)=>{
            // console.log(v, v1)
            if (v.label == v1){
              same = 1
            }
          })
          if (same == 1){
            retFilds.push(v)
          }
        })
       return (retFilds)
      },
      opt(val){
        var newOpt = []
        val.forEach((v)=>{
          newOpt.push(v.label)
        })
        return newOpt
      },
      okColumn(){
         this.$refs.column.hide()

         //this.fields.splice(1, 1)
      },

      hidePosition(){
         this.$refs.column.show()    
         //this.fields.splice(1, 1)
      },

        onClickOutside() {
          this.$emit('onClickOutside')
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
     this.$emit('curNodeClicked', model, component)  
    },
    curNodeClickedModal(model, component){
        // console.log('!!!'),
        this.idNodeModal=model.id
    },



    delRow(id){
        if (confirm("Are you sure want to remove?")) {
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
        //console.log('dragEndHandler: ', model, component, e);
        this.drag1=model.id;
//        console.log(this.drag1, this.drag2);
        axios.get('/change_parrent_menu', {
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
    }
  },
  //   watch: {
  //       idNode: {
  //           handler(newValue, oldValue) { // some function },
  //               // console.log(oldValue, newValue)
  //               this.oldId=oldValue
  // //         // deep: true
  //         }
  //      }
  //   },

      mounted(){

     // setTimeout(() => {
     //    this.$socket.send('getPrices')
     //    this.$options.sockets.onmessage = (data) => (data.data=='getPrices') ? this.getPrices(): ''
     //    },1000);

    var thElm;
    var startOffset;

    Array.prototype.forEach.call(
    document.querySelectorAll("table th"),
    function (th) {
        th.style.position = 'relative';

        var grip = document.createElement('div');
        grip.innerHTML = "&nbsp;";
        grip.style.top = 0;
        grip.style.right = 0;
        grip.style.bottom = 0;
        grip.style.width = '5px';
        grip.style.position = 'absolute';
        grip.style.cursor = 'col-resize';
        grip.addEventListener('mousedown', function (e) {
            thElm = th;
            startOffset = th.offsetWidth - e.pageX;
        });

        th.appendChild(grip);
    });

    document.addEventListener('mousemove', function (e) {
        if (thElm) {
            thElm.style.width = startOffset + e.pageX + 'px';
        }
    });

    document.addEventListener('mouseup', function () {
        thElm = undefined;
    });

        }
    }
</script>
<style type="text/css">
    @import url(//netdna.bootstrapcdn.com/font-awesome/3.2.1/css/font-awesome.css);
.ccbox label {
    margin-top: -3px;
    width: 15px;
    text-align: left;
}

.ccbox input[type=checkbox] {
    display: none;
}


/* to hide the checkbox itself */

.ccbox input[type=checkbox]+label:before {
    font-family: FontAwesome;
}

.ccbox input[type=checkbox]+label:before {
    content: "\f096";
    font-size: 14px;
    font-weight: 100;
}


/* unchecked icon */

.ccbox input[type=checkbox]:checked+label:before {
    content: "\f046";
    font-size: 14px;
    font-weight: 100;
}
.withoutPad {
    margin: 0px !important;
    margin-left: 5px !important;
    margin-top: 4px !important;
}


.t_index_comp { width: 2%; text-align: center; }
.t_pos_num_comp { width: 20%; }
.t_name_comp { width: 30%; }
.t_desc_comp { width: 2%; text-align: center; }
.t_unit_comp { width: 11%; }
.t_price_comp { width: 11%; }
.t_without_comp { width: 11%; }
.t_percent_comp { width: 11%; }
.t_del_comp{width: 2%; text-align: center; }



</style>


