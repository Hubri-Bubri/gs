<template>
  <b-container fluid ref="heightTablePrice">
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
          <template #cell(name)="row">
          <div @click.prevent.stop="rowSelected(row.item)" :title="(row.item.desc&&row.item.desc.length!=0)?row.item.desc:'(You have not added an explanation for this item)'"
            v-html="row.item.name" />
          </template>
          <template #cell(unit)="row">
            <div @click.prevent.stop="rowSelected(row.item)"
            v-html="row.item.unit" />
          </template>
          <template #cell(price)="row">
          <div @click.prevent.stop="rowSelected(row.item)"
          v-html="row.item.price" />
          </template>
          <template #cell(without)="row">
            <div @click.prevent.stop="rowSelected(row.item)"
          v-html="row.item.without" />
          </template>
          <template #cell(percent)="row">
            <div @click.prevent.stop="rowSelected(row.item)"
        v-html="row.item.percent" />
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

            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.pos_num" ></b-input> -->
          </template>
          <template #cell(name)="row">

          <div :style="'max-width:'+(width/3.8)+'px;width:100%;padding-left:4px;'" :title="(row.item.desc)?row.item.desc:'(You have not added an explanation for this item)'"
          contenteditable="true" @click.prevent.self v-html="row.item.name"
          @blur="updateDate($event.target.innerHTML, 'name', row.item.id)" />

            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.name" ></b-input> -->
          </template>
          <template #cell(unit)="row">
          <div
          contenteditable="true" @click.prevent.self 
          class="diveditable"
          @blur="updateDate($event.target.innerHTML, 'unit', row.item.id)"
          v-html="row.item.unit" />


            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.unit" ></b-input> -->
          </template>
          <template #cell(price)="row">

          <div
          contenteditable="true" @click.prevent.self 
          class="diveditable"
          @blur="updateDate($event.target.innerHTML, 'price', row.item.id)"
          v-html="valueDigital(row.item.price)" />

            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.price" ></b-input> -->
          </template>
          <template #cell(without)="row">
            <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @blur="updateDate($event.target.innerHTML, 'without', row.item.id)"
        v-html="valueDigital(row.item.without)" />
            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.without"></b-input> -->
          </template>
          <template #cell(percent)="row">

            <div
        contenteditable="true" @click.prevent.self 
        class="diveditable"
        @blur="updateDate($event.target.innerHTML, 'percent', row.item.id)"
        v-html="valueDigital(row.item.percent)" />

            <!-- <b-input size="sm" :style="(row.item._rowVariant=='success')?rowColor:''" class="cForm-input" :value="row.item.percent" ></b-input> -->
          </template>
          <template #cell(show_details)="row">
            <b-link @click="row.toggleDetails"  style="text-decoration: none;font-weight: normal;">
              {{ row.detailsShowing ? '-' : '+'}}
            </b-link>
          </template>
          <template #row-details="row">
            <div contenteditable="true" @blur="updateDate($event.target.innerHTML, 'desc', row.item.id)">{{row.item.desc}}</div>
<!--             <div  :style="(row.item._rowVariant=='success')?rowColor:''" >{{row.item.desc}}</div>
 -->          </template>
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
      newFields:['#', this.$t('lists.position'), this.$t('customerDetail.name'), this.$t('lists.price')],
      newFields1:['#', this.$t('customerDetail.name'), 'i']
    }
  },
   computed: {
    // newFields(){
    //   return['#', this.$t('lists.position'), this.$t('customerDetail.name'), this.$t('lists.price')]
    // },
    // newFields1(){
    //   return['#', this.$t('customerDetail.name'), 'i']
    // },
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
        key: 'name',
        label: this.$t('customerDetail.name'), 
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
      {
        key: 'without',
        label: this.$t('lists.without'),
        sortable: true
      },
      {
        key: 'percent',
        label: '%',
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
        key: 'name',
        label: this.$t('customerDetail.name'), 
        sortable: true
      },
      {
        key: 'show_details',
        label: 'i'
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
      {
        key: 'without',
        label: this.$t('lists.without'),
        sortable: true
      },
      {
        key: 'percent',
        label: '%',
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
  },
  mounted(){
    window.addEventListener('resize', this.updateWidth);
    this.updateWidth();
    this.$emit('loded', 'component', this.$refs.heightTablePrice.clientHeight, 200)
  }

}
</script>