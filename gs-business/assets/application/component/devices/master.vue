<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-modal size="md" centered id="move" ref="move" title="Move">
        <!-- @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" -->
        <b-form-select class="" id="move" v-model="selectedItems" :select-size="detectRowSise(items_menu)">
          <option v-for="item in detectItem(items_menu)" @click="selectedModal(item)">{{item.name}}</option>
        </b-form-select>
        <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['move', 'copy']" />
          <template slot="modal-footer">
       <!-- <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>-->
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button> 
          </template>
      </b-modal>
      <b-card header="Devices" class="gs-container">
        <container>
          <container-body  style="overflow: unset;">
            <b-row>
              <b-col cols="3" class="block-1">
                  <vue-drag-tree
                  :data='items_menu'
                  :allowDrag='allowDrag'
                  :allowDrop='allowDrop'
                  :idNode="idNode"
                  disableDBClick
                  @drag="dragHandler"
                  @drag-enter="dragEnterHandler" 
                  @current-node-clicked="curNodeClicked"
                  @drag-leave="dragLeaveHandler"
                  @drag-over="dragOverHandler"
                  @drag-end="dragEndHandler"
                  @drop="dropHandler"
                  :thrId="idNode"
                  :parId="parId">
                  </vue-drag-tree> 
              </b-col>
              <b-col cols="9" class="block-2">
                  <b-table :items="items" :fields="fields"
                  show-empty
                  sticky-header 
                            hover
                  style="max-height:100%"
                  >
                    <template #cell(#)="data">
                      <div @click="rowSelected(data.item)" class="text-center w-100">
                        {{ data.index + 1 }}
                      </div>
                    </template>
                    <template #cell(pos_num)="row">
                      <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
                    </template>
                    <template #cell(designation)="row">
                      <div contenteditable="true"  @blur="updateDate($event.target.innerText, 'designation', row.item.id)">{{row.item.designation}}</div>
                    </template>
                    <template #cell(kilowatt)="row">
                      <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.kilowatt" @change="updateDate($event, 'kilowatt', row.item.id)"></b-input>
                    </template>
                    <template #cell(time)="row">
                      <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.time" @change="updateDate($event, 'time', row.item.id)"></b-input>
                    </template>
                    <template #cell(manufacturer)="row">
                      <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.manufacturer" @change="updateDate($event, 'manufacturer', row.item.id)"></b-input>
                    </template>
                    <template #cell(serial)="row">
                      <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.serial" @change="updateDate($event, 'serial', row.item.id)"></b-input>
                    </template>
                    <template #cell(order)="row">
                      <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.order" @change="updateDate($event, 'order', row.item.id)"></b-input>
                    </template>
                    <template #cell(check_date)="row">
                      <b-input type="date" size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.check_date" @change="updateDate($event, 'check_date', row.item.id)"></b-input>
                    </template>
                    <template #cell(next_check_date)="row">
                      <b-input type="date" size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.next_check_date" @change="updateDate($event, 'next_check_date', row.item.id)"></b-input>
                    </template>
                    <template #cell(comment)="row">
                      <div contenteditable="true"  @blur="updateDate($event.target.innerText, 'comment', row.item.id)">{{row.item.comment}}</div>
                    </template>
                    <template #cell(delete)="row">
                      <b-link @click="delRow(row.item.id)" ><b-icon icon="trash" aria-hidden="true"></b-icon></b-link>
                    </template> 
                  </b-table>
                  <div hidden>{{ selected }}</div>
                </b-col>
              </b-row>
            </b-container>
          </container-body>
        </container>
        <b-card-footer>
          <b-col cols="12">
            <b-input-group>
              <b-input-group-append>
                <b-button @click="add">Add Part</b-button>
                <b-button @click="remove">Remove</b-button>
              </b-input-group-append>
              <b-input-group-append>
                <b-button @click="addRow">Add Row</b-button>
                <b-button @click="mv_cp">Move/Copy</b-button>
              </b-input-group-append>
              <b-form-input v-model="nameNode" :style="nodeDis?'background-color:grey':''"
              @click.native="nodeDis?nodeDisTurn():''" @change="nodeDis=true;toModel(nameNode)"></b-form-input>
            </b-input-group>
          </b-col>
        </b-card-footer>
      </b-card>
    </container-body>
  </container>
</template>
<script>
import axios from 'axios';
export default {
  data(){
    return{
      idNode:-1,
      nodeDis:true,
      moveToCopyRadio:'move',
      rowColor:'background-color:#c3e6cb',
      selected:[],
      items:[],
      nameNode:null,
      idNode:null,
      parId:null,
      oldId:0,
      selectedItems:[],
      fields: [
        {
          key: '#',
          label: '#'
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
          key: 'comment',
          label: 'Comment',
          sortable: true
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
        {
          key: 'delete',
          label: 'Del',
        }],
        items_menu:[],
        drag1: null,
        drag2: null
      }
    },
    methods: {
      modshow(v){
        var items_menu = this.items_menu
        this.items_menu = []
        this.items_menu = items_menu
      },
      nodeDisTurn(){
        if (confirm("Are you sure want to rename?")) {
          this.nodeDis = false
        }
      },
      getDevices(){
        if (this.idNode!=null){
          axios.get('/devices', {
            params: {
              id:this.idNode?this.idNode:0
            }
          }).then(response => {
            this.items = response.data
          })
        }
        axios.get('/devices_menu').then(response => {
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
        this.idNode=model.id,
        this.parId = model.parrent
        // console.log(this.idNode == this.oldId)
        // console.log(this.idNode, this.oldId)
        if(this.idNode == this.oldId){
          if (this.items.length>0){
            this.items=[]
          } else{
            axios.get('/devices', {
              params: {
                id: model.id
              }
            }).then(response => {
              this.items = response.data
            })
          }
        } else {
          axios.get('/devices', {
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
              axios.get('/update_name_devices_menu', {
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
          alert('No menu item is selected for deletion.')
        }
        else {
          if (confirm("Are you sure want to remove?")) {
            axios.get('/remove_devices_menu', {
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
              axios.get('/add_devices_menu', {
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
          alert('No menu item is selected for add.')
        } else {
          axios.get('/add_devices', {
            params: {
              id: this.idNode
            }
          })
        }
      // location.href = "#finishList"
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
            alert('No menu item is selected.')
        } else{
          if (this.selected.length==0){
            alert('No rows selected.')
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
        if (confirm("Are you sure to "+this.moveToCopyRadio+' '+this.selected.length+
        ' rows in to '+val.name+"?")) {
          this.selected.forEach((val)=>{
            price_ids.push(val.id)
          })
          axios.get('/cp_mv_to_devices', {
            params: {
              price_ids: price_ids.join(),
              new_menu: val.id,
              operation: this.moveToCopyRadio
            }
          })
        }
      },
      dragHandler(model, component, e) {
      // console.log('dragHandler: ', model, component, e);
      },
      dragEnterHandler(model, component, e) {
      //  console.log('dragEnterHandler: ', model, component, e);
      },
      dragLeaveHandler(model, component, e) {
      // console.log('dragLeaveHandler: ', model, component, e);
      },
      dragOverHandler(model, component, e) {
      // console.log('dragOverHandler: ', model, component, e);
      },
      dragEndHandler(model, component, e) {
      //console.log('dragEndHandler: ', model, component, e);
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
      }
    },
    mounted(){
      setTimeout(() => {
        this.$socket.send('getDevices')
        this.$options.sockets.onmessage = (data) => (data.data=='getDevices') ? this.getDevices(): ''
      },1000);

    }
  }
</script>