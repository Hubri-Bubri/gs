<template>

                                  <b-table :items="responseFiles" :fields="fieldsDocs" stacked="lg" hover  class="tableProject" small >
                                        <template slot="type" slot-scope="row">
                                            <b-link size="sm" @click.stop="loadDocToFrame(row)" class="butMore">
                                                <i style="font-size:14px" :class="row.detailsShowing ? 'far fa-file' : 'fa fa-file-alt'" v-if="((row.item.name=='Orders') || (row.item.name=='Offers') || (row.item.name=='Invoices') || (row.item.name=='Damage Description'))"></i>
                                                <i style="font-size:14px" :class="row.detailsShowing ? 'far fa-file' : 'fa fa-file-pdf'" v-else-if="row.item.name.includes('.pdf')"></i>
                                                <i style="font-size:14px" :class="row.detailsShowing ? 'far fa-file' : 'fa fa-file-pdf'" v-else></i>
                                            </b-link>
                                        </template>
                                        <template slot="name" slot-scope="row">
                                           <b-form-input :state="null" type="text" @change="(row.item.html=='file')?updatefilename($event+'.pdf', 'name', row.item.id):updatedocname($event, 'name', row.item.id)" :title="row.item.name.replace('.pdf', '')"
                                           :value="row.item.name.replace('.pdf', '')" class="cForm-input" @focus.native="(row.item.html=='file')?changeDisable('f', 'nameoffile', row.item.id):changeDisable('f', 'nameofdoc', row.item.id)"
                                           @blur.native="(row.item.html=='file')?changeDisable('b', 'nameoffile', row.item.id):changeDisable('b', 'nameofdoc', row.item.id)" :id="(row.item.html=='file')?'nameoffile'+row.item.id:'nameofdoc'+row.item.id"  style="width:95%" /> 
                                        </template>
                                        <template slot="row-details" slot-scope="row">
                                            <iframe type="iframe1" :style="'width:100%;height:'+(30.1*row.item.pages+1.5)+'cm'" frameborder="0" :name="'ifr'+t+row.index" class="iframeclass" src="">
                                            </iframe>
                                           
                                            <form :target="'ifr'+t+row.index" :action="(row.item.html!='file') ? '/pdf1':'/pdf2'" method="post" :ref="'ifrForm'+row.index">
                                                <input type="hidden" name="html" :value="row.item.id" style="display:none" v-if="(row.item.html!='file')" />
                                                <input type="hidden" name="id" :value="row.item.id" v-else />
                                            </form>
                                        </template>
                                        <template slot="delete" slot-scope="it">
                                           <b-col>
                                              <b-link @click.stop="(it.item.html=='file')?filedel(it.item.id):docdel(it.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>
                              <template slot="added" slot-scope="data">
                                {{data.item.added | dateInverse}}
                              </template>
                                    </b-table>

</template>
<script type="text/javascript">
import axios from 'axios';

export default {
  components: {
    
  },
  props: ['responseFiles', 'fieldsDocs', 't'],
  data(){
      return{
       
            }
    },
  
    methods: {
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
},

    },
    mounted(){

    }
  }

</script>