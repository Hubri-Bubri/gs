<template>
  <b-container fluid ref="heightTableDocs">
    <b-row>
      <b-col cols="12" lg="3" class="block-1">
        <vue-drag-tree
        :data='itemsMenuDoc'
        :allowDrag='allowDrag'
        :allowDrop='allowDrop'
        :idNode="idNodeDoc"
        disableDBClick
        @current-node-clicked="curNodeClicked"
        @drag-end="dragEndHandler"
        @drop="dropHandler">
        </vue-drag-tree>
        <div hidden>{{selectedPriceDoc}}</div>
      </b-col>
      <b-col cols="12" lg="9" class="block-2 m-0 p-0">
        <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
        <b-table :items="foldershowfiles(responseFiles)" :fields="fieldsDocs"
        hover small stacked="lg"
        show-empty no-border-collapse
        >
          <template #cell(type)="row">
              <b-icon :icon="row.detailsShowing ?'file-earmark':'file-pdf'" aria-hidden="true" @click.stop="loadDocToFrame(row)"
              v-if="((row.item.name=='Orders') || (row.item.name=='Offers') || (row.item.name=='Invoices') || (row.item.name=='Damage Description'))"></b-icon>
               <b-icon :icon="row.detailsShowing ?'file-earmark':'file-pdf'" aria-hidden="true" v-else-if="row.item.name.includes('.pdf')" @click.stop="loadDocToFrame(row)"></b-icon>
               <b-icon :icon="row.detailsShowing ?'file-earmark':'file-pdf'" aria-hidden="true"  v-else @click.stop="loadDocToFrame(row)"></b-icon>
          </template>
          <template #cell(name)="row">
            <b-form-input  type="text" size="sm"
            @change="(detectUrl(row.item.html)!='/pdf1')?updatefilename($event+'.pdf', 'name', row.item.id):updatedocname($event, 'name', row.item.id)"
            :title="row.item.name.replace('.pdf', '')" :value="row.item.name.replace('.pdf', '')"
            @focus.native="(row.item.html!='html')?changeDisable('f', 'nameoffile', row.item.id):changeDisable('f', 'nameofdoc', row.item.id)"
            @blur.native="(row.item.html!='html')?changeDisable('b', 'nameoffile', row.item.id):changeDisable('b', 'nameofdoc', row.item.id)"
            :id="(row.item.html!='html')?'nameoffile'+row.item.id:'nameofdoc'+row.item.id"  /> 
          </template>
          <template #row-details="row">
            <iframe type="iframe1" :style="'width:100%;height:'+(30.1*row.item.pages+1.5)+'cm'" frameborder="0" :name="'ifr'+t+row.index" class="iframeclass" src="">
            </iframe>
            <form :target="'ifr'+t+row.index" :action="detectUrl(row.item.html)" method="post" :ref="'ifrForm'+row.index">
              <input type="hidden" name="id" :value="row.item.id" />
            </form>
          </template>
          <template #cell(delete)="it">
             <b-icon icon="trash" aria-hidden="true" @click.stop="(detectUrl(it.item.html)!='/pdf1')?filedel(it.item.id):docdel(it.item.id)"  />
          </template>
          <template #cell(added)="data">
            <div @click="rowSelected(data.item)" style="white-space: nowrap;"
            :title="data.item.added.split(' ')[0].split('-')[0]+'.'+data.item.added.split(' ')[0].split('-')[1]+'.'+data.item.added.split(' ')[0].split('-')[2]+' '+data.item.added.split(' ')[1]">
              {{data.item.added.split(' ')[0].split('-')[0]+'.'+data.item.added.split(' ')[0].split('-')[1]+'.'+data.item.added.split(' ')[0].split('-')[2]}}
            </div>
          </template>
          <template #cell(user)="data">
            <div @click="rowSelected(data.item)" :title="data.item.user"> {{data.item.user.replace(/[^A-Z]/g, '')}} </div>
          </template>
          <template #cell(number)="data">
            <div @click="rowSelected(data.item)" style="width:100px;"> {{data.item.number}} </div>
          </template>
        </b-table>
      </div>
      </b-col>
    </b-row>
  </b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: ['responseFiles', 'idNodeDoc', 't', 'itemsDoc', 'itemsMenuDoc', 'oldIdDoc', 'selectedPriceDoc', 'menuDocsTree', 'docsIds'],
  computed: {
fieldsDocs() {
			return [{
					key: 'type',
					label: '§',
					sortable: true
				},
				{
					key: 'name',
					label: this.$t('docs.name'),
					class: 'w-100',
					sortable: true
				},
				{
					key: 'number',
					label: '#'
				},
				{
					key: 'added',
					label: this.$t('docs.added'),
					sortable: true
				},
				{
					key: 'user',
					label: '👤',
					sortable: true
				},
				{
					key: 'delete',
					label: 'X'
				}
			]
		}
  },
  methods: {
    foldershowfiles(val){
      if (this.idNodeDoc != undefined){
        return val.filter((itemDoc)=>{
          if (this.idNodeDoc!=-1){
            if(this.idNodeDoc==itemDoc.folder_id){
              return itemDoc
            }
          }
          if (this.idNodeDoc==-1) {
            if((itemDoc.folder_id==null)|(itemDoc.folder_id==-1)){
              return itemDoc
            }
          }
        })
      }
    },
     rowSelected(items) {
      this.$emit('rowSelectedDoc', items)  
    },
    loded(){
      setTimeout(() => {
        this.$emit('loded', 'component', this.$refs.heightTableDocs.clientHeight, 220)
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
      this.$emit('curNodeClickedDoc', model, component)  
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
    detectUrl(val){
      var url = '/pdf1'
      if (val == 'company') url = '/pdf_file_from_company'
      if (val == 'customer') url = '/pdf_file_from_customer'
      if (val == 'person') url = '/pdf_file_from_person'
      if (val == 'sub') url = '/pdf_file_from_sub' 
      if (val == 'sperson') url = '/pdf_file_from_sperson' 
      if (val == 'file') url = '/pdf2'
      return url
    },
    loadDocToFrame(row) {
      this.$emit('loadDocToFrame', row)
    },
    docdel(val) {
      if (confirm("Are you sure?")) {
        axios.get('/deldoc', {
          params: {
            id: val
          }
        }).then(response => {});
      }
    },
    filedel(val) {
      this.$emit('filedel', val)
    },
    updatefilename(val, type, id){
      this.$emit('updatefilename', val, type, id)
    },
    updatedocname(val, type, id){
      this.$emit('updatedocname', val, type, id)
    },
    changeDisable(type_operation, fild, id){
      this.$emit('changeDisable', type_operation, fild, id)
    }
  },mounted(){
     this.$emit('loded', 'component', this.$refs.heightTableDocs.clientHeight, 220)
      this.$options.sockets.onmessage = (data) => (data.data=='getDocs') ? this.$emit('getDocs'): '';
  }
}
</script>