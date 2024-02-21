<template>
  <b-container fluid ref="heightTableReports">
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
      <b-col cols="12" :lg="hideColumn?5:9" class="block-2 m-0 p-0">
        <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
        <b-table hover :items="items" :fields="getFields(fields, newFields)" small stacked="lg"
        show-empty no-border-collapse >
          <template #cell(#)="data">
            <div @click.prevent.stop="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
            <b-col @click.prevent.stop="rowSelected(row.item)"
            class="diveditable"
            v-html="row.item.pos_num" />
          </template>
          <template #cell(service)="row">
            <div @click.prevent.stop="rowSelected(row.item)"
            v-html="row.item.service" />
          </template>
          <template #cell(time)="row">
          <div @click.prevent.stop="rowSelected(row.item)"
          v-html="row.item.time" />
          </template>
          
          <template #cell(delete)="row">
            <b-icon icon="trash" aria-hidden="true" @click.prevent.stop="delRow(row.item.id)"></b-icon>
          </template>
        </b-table>
      </div>
      </b-col>
      <b-col cols="4" v-show="hideColumn" class="block-1">
        <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
 <b-table :items="selectedPrice" :fields="getFields(fields1, newFields1)"  hover small 
 show-empty no-border-collapse>
          <template #cell(#)="data">
            <div @click="rowSelected(data.item)" class="text-center w-100">
              {{ data.index + 1 }}
            </div>
          </template>
          <template #cell(pos_num)="row">
          <div
          contenteditable="true"
          @click.prevent.self 
          class="diveditable"
          @blur="updateDate($event.target.innerHTML, 'pos_num', row.item.id)"
          v-html="row.item.pos_num" />
          </template>
          <template #cell(service)="row">
          <div
          contenteditable="true" @click.prevent.self 
          class="diveditable"
          @blur="updateDate($event.target.innerHTML, 'service', row.item.id)"
          v-html="row.item.service" />
          </template>
          <template #cell(time)="row">
          <div
          contenteditable="true" @click.prevent.self 
          class="diveditable"
          @blur="updateDate($event.target.innerHTML, 'time', row.item.id)"
          v-html="valueDigital(row.item.time)" />
          </template>


        </b-table>
      </div>
      </b-col>
    </b-row>
       <span hidden="">{{selectedPrice}}</span>    
  </b-container>
</template>
<script>
import axios from 'axios';
export default {
  props: ['howhight', 'idNode', 'parId', 'items', 'itemsMenu', 'selectedPrice', 'menuPriceTree'],
  data(){
    return{
      rowColor:'background-color:#c3e6cb',
      hideColumn:false,
      fieldsForTable:[],
      fields1ForTable:[],
      drag1: null,
      drag2: null,
      newFields:['#', this.$t('lists.position'), this.$t('reports.service'), this.$t('reports.time')],
      newFields1:['#', this.$t('customerDetail.name'), 'i']
    }
  },
   computed: {
    fields(){
      return[
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
        key: 'service',
        label: this.$t('reports.service'), 
        sortable: true
      },
      {
        key: 'time',
        label: this.$t('reports.time'), 
        sortable: true
      },
      {
        key: 'delete',
        label: this.$t('docs.delete')
      }
    ]
  },
      fields1(){
      return[
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
        key: 'service',
        label: this.$t('reports.service'), 
        sortable: true
      },
      {
        key: 'time',
        label: this.$t('reports.time'), 
        sortable: true
      }
    ]
  }
    },
  methods: {
    valueDigital(model){
      var value = parseFloat(model)
      value = value.toString()
      value = value.replace('.',',')
      value = (value=='NaN')?0:value
      if (value.length < 3){
        value = '&nbsp;&nbsp;'+value+'&nbsp;&nbsp;'
      }
      return value
    },
    updateWidth() {
        this.width = window.innerWidth;
    },
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
    // onClickOutside() {
    //   this.$emit('onClickOutside')
    // },
    loded(){
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs.heightTablePrice.clientHeight, 200)
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
      this.$emit('curNodeClicked', model, component)
    },
    curNodeClickedModal(model, component){
        this.idNodeModal=model.id
    },
    delRow(id){
      if (confirm("Are you sure want to remove?")) {
        axios.get('/remove_report', {
          params: {
            id: id
          }
        })
      }
    },
    updateDate(data, fild, id){
      axios.get('/update_report', {
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
      axios.get('/change_parrent_menu_reports', {
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
    window.addEventListener('resize', this.updateWidth);
    this.updateWidth();
    this.$emit('loded', 'component', this.$refs.heightTableReports.clientHeight, 200)
  }

}
</script>