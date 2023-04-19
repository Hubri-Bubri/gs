<template>
  <b-container fluid >
    <b-modal size="md" centered id="column" ref="column" title="Edit Column">
      <b-row>
        <b-col>
          <b-form-checkbox-group buttons  style="width:100%" v-model="newFields" stacked :options="opt(fields)"/>
        </b-col>
        <b-col class="text-center">
          <b-form-checkbox-group buttons  style="width:100%" v-model="newFields1" stacked :options="opt(fields1)"/>
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
      <b-col cols="3" class="block-1">
        <vue-drag-tree
        :data='itemsMenu'
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :idNode="idNode"
        :parId="parId"
        disableDBClick
        @drag="dragHandler"
        @drag-enter="dragEnterHandler"
        @current-node-clicked="curNodeClicked"
        @drag-leave="dragLeaveHandler"
        @drag-over="dragOverHandler"
        @drag-end="dragEndHandler"
        @drop="dropHandler">
        </vue-drag-tree>                              
      </b-col>
      <b-col :cols="hideColumn?5:9" class="block-2">
        <b-table hover :items="items" :fields="getFields(fields, newFields)" small sticky-header  style="max-height:100%">
          <template #cell(#)="data">
            <div @click="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
            <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
          </template>
          <template #cell(name)="row">
       <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" @change="updateDate($event, 'name', row.item.id)"></b-input> -->
            <div :style="(row.item._rowVariant=='success')?rowColor:''+';width:100%;min-width:150px;'" contenteditable="true"  @blur="updateDate($event.target.innerText, 'name',  row.item.id)">{{row.item.name}}</div>
          </template>
          <template #cell(unit)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.unit" @change="updateDate($event, 'unit', row.item.id)"></b-input>
          </template>
          <template #cell(price)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.price" @change="updateDate($event, 'price', row.item.id)"></b-input>
          </template>
          <template #cell(without)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.without" @change="updateDate($event, 'without', row.item.id)"></b-input>
          </template>
          <template #cell(percent)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.percent" @change="updateDate($event, 'percent', row.item.id)"></b-input>
          </template>
          <template #cell(show_details)="row">
            <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
              {{ row.detailsShowing ? '-' : '+'}}
            </b-link>
          </template>
          <template #cell(delete)="row">
            <b-icon icon="trash" aria-hidden="true" @click.prevent.stop="delRow(row.item.id)"  />
            <!-- <b-link @click.prevent.stop="delRow(row.item.id)" class="fas fa-trash fa-w-16 text-center" /> -->
          </template>
          <template #row-details="row">
            <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'desc', row.item.id)">{{row.item.desc}}</div>
          </template>
        </b-table>  <span hidden>{{selectedPrice}}</span>                           
      </b-col>
      <b-col cols="4" v-show="hideColumn" class="block-2">
        <b-table:items="selectedPrice" :fields="getFields(fields1, newFields1)"  hover small  sticky-header  style="max-height:100%">
          <template #cell(#)="data">
            <div @click="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" ></b-input>
          </template>
          <template #cell(name)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" ></b-input>
          </template>
          <template #cell(unit)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.unit" ></b-input>
          </template>
          <template #cell(price)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.price" ></b-input>
          </template>
          <template #cell(without)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.without"></b-input>
          </template>
          <template #cell(percent)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.percent" ></b-input>
          </template>
          <template #cell(show_details)="row">
            <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
              {{ row.detailsShowing ? '-' : '+'}}
            </b-link>
          </template>
          <template #row-details="row">
            <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" >{{row.item.desc}}</div>
          </template>
        </b-table>
      </b-col>
    </b-row>
  </b-container>
</template>
<script>
import axios from 'axios';
export default {
  props: ['howhight', 'idNode', 'parId', 'items', 'itemsMenu', 'selectedPrice', 'menuPriceTree'],
  data(){
    return{
      newFields:['#', 'Position', 'i', 'Name', 'Price'],
      newFields1:['#','Name'],
      rowColor:'background-color:#c3e6cb',
      hideColumn:false,
      fields: [
      {
        key: '#',
        label:'#'
      },
      {
        key: 'pos_num',
        label: 'Position',
        sortable: true
      },
      {
        key: 'name',
        label: 'Name',
        sortable: true
      },
      {
        key: 'show_details',
        label: 'i'
        // tdClass: 'text-center'
      },
      {
        key: 'unit',
        label: 'Unit',
        sortable: true
      },
      {
        key: 'price',
        label: 'Price',
        sortable: true
      },
      {
        key: 'without',
        label: 'Without',
        sortable: true
      },
      {
        key: 'percent',
        label: '%',
        sortable: true
      },
      {
        key: 'delete',
        label: 'Del'
      }],
      fields1: [
      {
        key: '#',
        label:'#'
      },
      {
        key: 'pos_num',
        label: 'Position',
        sortable: true
      },
      {
        key: 'name',
        label: 'Name',
        sortable: true
      },
      {
        key: 'show_details',
        label: 'i'
        // tdClass: 'text-center'
      },
      {
        key: 'unit',
        label: 'Unit',
        sortable: true
      },
      {
        key: 'price',
        label: 'Price',
        sortable: true
      },
      {
        key: 'without',
        label: 'Without',
        sortable: true
      },
      {
        key: 'percent',
        label: '%',
        sortable: true
      }],
      fieldsForTable:[],
      fields1ForTable:[],
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
    },
    hidePosition(){
      this.$refs.column.show()    
    },
    onClickOutside() {
      this.$emit('onClickOutside')
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
      this.$emit('curNodeClicked', model, component)  
    },
    curNodeClickedModal(model, component){
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
  }
}
</script>