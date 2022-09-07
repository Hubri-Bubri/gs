<template>
 <b-container fluid>

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

                               <b-collapse v-model="menuDevicesTree" id="devicesMenu"
                               v-click-outside="onClickOutside"
                                :style="'padding:0;position:fixed;z-index:10;top:'+howhight+'px;left:'+((howhight==37)?'16':'209')+'px;border-style: ridge;'">

                                    <b-row class="border border-right-0 border-left-0" style="
                                    padding: 0px;font-size: 12px; border-bottom: 2px solid #dee2e6 !important; margin: 0px;
                                    vertical-align: middle !important; border-spacing: 2px; border-color: grey; background-color:white;">
                                     <b-col> <b> Tree </b> </b-col>
                                    </b-row>
<vue-drag-tree
:data='itemsMenuDev'
:allowDrag='allowDrag'
:allowDrop='allowDrop'
:thrId="idNodeDev"
:parId="parIdDev"
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
<b-table borderless  hover  class="tableProject" small :items="itemsDev" :fields="getFields(fields, newFields)"   v-columns-resizable>
                                             <template slot="&#35;" slot-scope="data" >
                                                <div @click="rowSelected(data.item)">
                                                {{ data.index + 1 }}
                                                </div>
                                              </template>
                                            <template slot="pos_num" slot-scope="row">
                                                <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
                                            </template>
                                                 <template slot="designation" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.designation" @change="updateDate($event, 'designation', row.item.id)"></b-input>
                                            </template>
                                            <template slot="kilowatt" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.kilowatt" @change="updateDate($event, 'kilowatt', row.item.id)"></b-input>
                                            </template>
                                            <template slot="time" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.time" @change="updateDate($event, 'time', row.item.id)"></b-input>
                                            </template>
                                            <template slot="manufacturer" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.manufacturer" @change="updateDate($event, 'manufacturer', row.item.id)"></b-input>
                                            </template>
                                            <template slot="serial" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.serial" @change="updateDate($event, 'serial', row.item.id)"></b-input>
                                            </template>
                                            <template slot="order" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.order" @change="updateDate($event, 'order', row.item.id)"></b-input>
                                            </template>                                            
                                            <template slot="check_date" slot-scope="row">
                                                <b-input size="sm" type="date" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.check_date" @change="updateDate($event, 'check_date', row.item.id)"></b-input>
                                            </template>
                                            <template slot="next_check_date" slot-scope="row">
                                                <b-input size="sm" type="date"  :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.next_check_date" @change="updateDate($event, 'next_check_date', row.item.id)"></b-input>
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
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'comment', row.item.id)">{{row.item.comment}}</div>
                                            </template>
                                    </b-table>
                                    
</b-col><b-col cols="6" v-show="hideColumn">
 <b-table borderless  hover  class="tableProject" small   :items="selectedPriceDev" :fields="getFields(fields1, newFields1)"   v-columns-resizable>
                                              <template slot="&#35;" slot-scope="data" >
                                                <div @click="rowSelected(data.item)">
                                                {{ data.index + 1 }}
                                                </div>
                                              </template>
                                            <template slot="pos_num" slot-scope="row">
                                                <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
                                            </template>
                                                 <template slot="designation" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.designation" @change="updateDate($event, 'designation', row.item.id)"></b-input>
                                            </template>
                                            <template slot="kilowatt" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.kilowatt" @change="updateDate($event, 'kilowatt', row.item.id)"></b-input>
                                            </template>
                                            <template slot="time" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.time" @change="updateDate($event, 'time', row.item.id)"></b-input>
                                            </template>
                                            <template slot="manufacturer" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.manufacturer" @change="updateDate($event, 'manufacturer', row.item.id)"></b-input>
                                            </template>
                                            <template slot="serial" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.serial" @change="updateDate($event, 'serial', row.item.id)"></b-input>
                                            </template>
                                            <template slot="order" slot-scope="row">
                                                <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.order" @change="updateDate($event, 'order', row.item.id)"></b-input>
                                            </template>                                            
                                            <template slot="check_date" slot-scope="row">
                                                <b-input size="sm" type="date" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.check_date" @change="updateDate($event, 'check_date', row.item.id)"></b-input>
                                            </template>
                                            <template slot="next_check_date" slot-scope="row">
                                                <b-input size="sm" type="date"  :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.next_check_date" @change="updateDate($event, 'next_check_date', row.item.id)"></b-input>
                                            </template>
                                            <template slot="show_details" slot-scope="row">
                                                   <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
                                                        {{ row.detailsShowing ? '-' : '+'}}
                                                   </b-link>
                                            </template>
                                             
<!--                                             <template slot="row-details" slot-scope="row">
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @keyup.native="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
                                            </template> -->
                                            <template slot="row-details" slot-scope="row">
                                                <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'comment', row.item.id)">{{row.item.comment}}</div>
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
    props: ['howhight', 'idNodeDev', 'parIdDev', 'itemsDev', 'oldIdDev', 'itemsMenuDev', 'selectedPriceDev'],

  data(){
    return{
      // newFields:['&#35; ', 'Position', 'Name', 'i', 'Unit', 'Price', 'Without', '%', 'Del'],
      // newFields1:['&#35; ', 'Position', 'Name', 'i', 'Unit', 'Price', 'Without', '%'],
      newFields:['&#35; ', 'Position',  'Designation', 'i', 'Watt', 'Time', 'Manufacturer'],
      newFields1:['&#35; ','Designation'],
      menuDevicesTree:false,
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
                    sortable: true
                },
                {
                    key: 'pos_num',
                    label: 'Position',
                    sortable: true
                },
                {
                    key: 'designation',
                    label: 'Designation',
                    sortable: true
                },
                {
                    key: 'show_details',
                    label: 'i',
                    tdClass: 't_desc_comp'
                },
                {
                    key: 'kilowatt',
                    label: 'Watt',
                    sortable: true
                },
                {
                    key: 'time',
                    label: 'Time',
                    sortable: true
                },
                {
                    key: 'manufacturer',
                    label: 'Manufacturer',
                    sortable: true
                },
                {
                    key: 'serial',
                    label: 'Serial',
                    sortable: true
                },
                {
                    key: 'order',
                    label: 'Order',
                    sortable: true
                },
                {
                    key: 'check_date',
                    label: 'Check',
                    sortable: true
                },
                {
                    key: 'next_check_date',
                    label: 'Next Check',
                    sortable: true
                },
                {   key: 'delete',
                    label: 'Del',
                },
      
            ],
            fields1: [{
                    key: '&#35;',
                    label: '&#35; ',
                    sortable: true
                },
                {
                    key: 'pos_num',
                    label: 'Position',
                    sortable: true
                },
                {
                    key: 'designation',
                    label: 'Designation',
                    sortable: true
                },
                {
                    key: 'show_details',
                    label: 'i',
                    tdClass: 't_desc_comp'
                },
                {
                    key: 'kilowatt',
                    label: 'Watt',
                    sortable: true
                },
                {
                    key: 'time',
                    label: 'Time',
                    sortable: true
                },
                {
                    key: 'manufacturer',
                    label: 'Manufacturer',
                    sortable: true
                },
                {
                    key: 'serial',
                    label: 'Serial',
                    sortable: true
                },
                {
                    key: 'order',
                    label: 'Order',
                    sortable: true
                },
                {
                    key: 'check_date',
                    label: 'Check',
                    sortable: true
                },
                {
                    key: 'next_check_date',
                    label: 'Next Check',
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
      this.$emit('rowSelectedDev', items)  
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
      onClickOutside (event) {
        this.menuDevicesTree=false
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
     this.$emit('curNodeClickedDev', model, component)  
    },
    curNodeClickedModal(model, component){
        // console.log('!!!'),
        this.idNodeModal=model.id
    },



    delRow(id){
        if (confirm("Are you sure want to remove?")) {
            axios.get('/remove_devices', {
                params: {
                    id: id
                }
            })
        }
    },
    updateDate(data, fild, id){
        axios.get('/update_devices', {
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


