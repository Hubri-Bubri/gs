<template>
 <b-container fluid ref="heightTableDevice">
    <b-modal size="md" centered id="column" ref="column" :title="$t('price.editColumn')">
      <b-row>
        <b-col>
          <b-form-checkbox-group buttons  style="width:100%" v-model="newFields" stacked :options="opt(fields)"/>
        </b-col>
        <b-col class="text-center">
          <b-form-checkbox-group buttons  style="width:100%" v-model="newFields1" stacked :options="opt(fields1)"/>
          <b-button class="btn btn-light" @click="hideColumnfunc()">
           {{hideColumn?$t('price.hide'):$t('price.show')}} {{$t('price.column')}}
          </b-button>
        </b-col>
      </b-row>
      <template slot="modal-footer">
        <button type="button" class="btn btn-primary" @click="okColumn">OK</button> 
      </template>
    </b-modal>
    <b-row>
      <b-col cols="12" lg="3" class="block-1" >
        <vue-drag-tree
        :data='itemsMenuDev'
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :idNode="idNodeDev"
        :parId="parIdDev"
        disableDBClick
        @current-node-clicked="curNodeClicked"
        @drag-end="dragEndHandler"
        @drop="dropHandler">
        </vue-drag-tree>                              
      </b-col>
      <b-col cols="12" :lg="hideColumn?5:9" class="block-2 m-0 p-0">
        <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
        <b-table :items="itemsDev" :fields="getFields(fields, newFields)"  hover small  show-empty stacked="lg" no-border-collapse>
          <template #cell(#)="data">
            <div @click="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
            <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
          </template>
          <template #cell(designation)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.designation" @change="updateDate($event, 'designation', row.item.id)"></b-input>
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
            <b-input size="sm" type="date" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.check_date" @change="updateDate($event, 'check_date', row.item.id)"></b-input>
          </template>
          <template #cell(next_check_date)="row">
            <b-input size="sm" type="date"  :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.next_check_date" @change="updateDate($event, 'next_check_date', row.item.id)"></b-input>
          </template>
          <template #cell(show_details)="row">
            <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
              {{ row.detailsShowing ? '-' : '+'}}
            </b-link>
          </template>
          <template #cell(delete)="row">
             <b-icon icon="trash" aria-hidden="true" @click.prevent.stop="delRow(row.item.id)"  />
          </template>
          <template #row-details="row">
            <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'comment', row.item.id)">{{row.item.comment}}</div>
          </template>
        </b-table>
      </div>
      </b-col>
      <b-col cols="4" v-show="hideColumn" class="block-2">
        <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
        <b-table  class="tableProject" :items="selectedPriceDev" :fields="getFields(fields1, newFields1)"  hover small  show-empty no-border-collapse>
          <template #cell(#)="data">
            <div @click="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
            <b-input  size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" @change="updateDate($event, 'pos_num', row.item.id)"></b-input>
          </template>
          <template #cell(designation)="row">
            <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.designation" @change="updateDate($event, 'designation', row.item.id)"></b-input>
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
            <b-input size="sm" type="date" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.check_date" @change="updateDate($event, 'check_date', row.item.id)"></b-input>
          </template>
          <template #cell(next_check_date)="row">
            <b-input size="sm" type="date"  :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.next_check_date" @change="updateDate($event, 'next_check_date', row.item.id)"></b-input>
          </template>
          <template #cell(show_details)="row">
            <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
              {{ row.detailsShowing ? '-' : '+'}}
            </b-link>
          </template>
          <template #row-details="row">
            <div contenteditable="true" :style="(row.item._rowVariant=='success')?rowColor:''" @blur="updateDate($event.target.innerText, 'comment', row.item.id)">{{row.item.comment}}</div>
          </template>
        </b-table>
      </div>
      </b-col>  
    </b-row>
  </b-container>
</template>
<script>
import axios from 'axios';
export default {
  props: ['howhight', 'idNodeDev', 'parIdDev', 'itemsDev', 'oldIdDev', 'itemsMenuDev', 'selectedPriceDev', 'menuDevicesTree'],
  data(){
    return{
      newFields:['#', this.$t('lists.position'), this.$t('lists.designation'), 'i', this.$t('lists.kilowatt'), this.$t('lists.time'), this.$t('lists.manufacturer')],
      newFields1:['#', this.$t('lists.designation')],
      rowColor:'background-color:#c3e6cb',
      hideColumn:false,
      fieldsForTable:[],
      fields1ForTable:[],
      drag1: null,
      drag2: null
    }
  },
  computed:{
     fields() {return[
           {
             key: '#',
             label: '#',
             sortable: true
           },
           {
             key: 'pos_num',
             label: this.$t('lists.position'),
             sortable: true
           },
           {
             key: 'designation',
             label: this.$t('lists.designation'),
             sortable: true
           },
           {
             key: 'show_details',
             label: 'i',
           },
           {
             key: 'kilowatt',
             label: this.$t('lists.kilowatt'), 
             sortable: true
           },
           {
             key: 'time',
             label: this.$t('lists.time'), 
             sortable: true
           },
           {
             key: 'manufacturer',
             label: this.$t('lists.manufacturer'), 
             sortable: true
           },
           {
             key: 'serial',
             label: this.$t('lists.serial'), 
             sortable: true
           },
           {
             key: 'order',
             label: this.$t('lists.order'), 
             sortable: true
           },
           {
             key: 'check_date',
             label: this.$t('lists.check_date'), 
             sortable: true
           },
           {
             key: 'next_check_date',
             label: this.$t('lists.next_check_date'), 
             sortable: true
           },
           {   key: 'delete',
               label: this.$t('docs.delete')
           }]},
      fields1() {return[{
              key: '#',
              label: '#',
              sortable: true
            },
            {
              key: 'pos_num',
              label: this.$t('lists.position'), 
              sortable: true
            },
            {
              key: 'designation',
              label: this.$t('lists.designation'), 
              sortable: true
            },
            {
              key: 'show_details',
              label: 'i',
            },
            {
              key: 'kilowatt',
              label: this.$t('lists.kilowatt'), 
              sortable: true
            },
            {
              key: 'time',
              label: this.$t('lists.time'), 
              sortable: true
            },
            {
              key: 'manufacturer',
              label: this.$t('lists.manufacturer'), 
              sortable: true
            },
            {
              key: 'serial',
              label: this.$t('lists.serial'), 
              sortable: true
            },
            {
              key: 'order',
              label: this.$t('lists.order'), 
              sortable: true
            },
            {
              key: 'check_date',
              label: this.$t('lists.check_date'), 
              sortable: true
            },
            {
              key: 'next_check_date',
              label: this.$t('lists.next_check_date'), 
              sortable: true
            }]}
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
    loded(){
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs.heightTableDevice.clientHeight, 200)
      }, 1);     
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
      this.$emit('curNodeClickedDev', model, component)  
    },
    curNodeClickedModal(model, component){
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
    }
  },mounted(){
    this.$emit('loded', 'component', this.$refs.heightTableDevice.clientHeight, 200)
  }
}
</script>