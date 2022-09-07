<template>
  <div>
    <slot name="tableHead" :tableId="tableId" @click.prevent.self></slot>
    <input ref="unfocus" style="width: 0px; height: 0px; position: absolute; top: 0; left: 0; margin:0; padding:0; border: 0"></input>
         <b-collapse visible :id="'partx'+tableId">
            <div :class="{ 'table-dark': toggle }"> <!--v-if="window.width>1200"-->
               <div class="headtablewarp">
                  <b-form-row class="headtable">

                     <div class="tnumber text-center" @click="selectionRows">#</div>
                     <div class="tposition text-center"><b-link @click.stop="showPos=showPos?false:true">
                     {{showPos?'Position':'+'}}
                      </b-link></div>
                     <div class="tdeschead text-center" :style="'width:'+(computedWithDesc(value.parts.checkbox_list.flavours)+(showPos?0:-10))+'%'">Description Head</div>
                     <div class="tinfo text-center"><i class="fas fa-info" style="font-size:10px;width:10px;padding:0px;"></i></div>
                     <div class="tcount text-center">=</div>
                     <div class="tunit text-center">Unit</div>
                     <div class="tprice text-center">€</div>
                     <div class="tsumm text-center">∑</div>
                     <div class="custom-control-inline tpercent">
                        <div  v-for="(select_from_allSelected, key) in value.parts.checkbox_list.allSelected"
                        class="ccbox" :class="classRow(value.parts, key)">
                           <b-form-checkbox plain :disabled="disablefild(null, null)"
                              v-model="value.parts.checkbox_list.allSelected[key]"
                              @change="toggleAll($event, key)"
                              class="withoutPad" />
                        </div>
                     </div>
                     <div class="twithout text-center" v-if="butDiscPerc=='%'">-%</div>
                     <div class="tcalc text-center">Calculation</div>
                     <div class="tdone text-center ccbox">
                       <b-form-checkbox :disabled="disablefild(null, null)" plain class="withoutPad" v-if="showAllworkers()"
                       @click.native.prevent.stop="(type!='Invoices')?subtoggleAllWorkers():''" :checked="checkedAllWorkers()" />
                     </div>
                     <div class="tdelete text-center">X</div>
                  </b-form-row>
               </div>
               <draggable v-model="value.parts.part_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
                  :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)" @choose="move()"> <!-- calss="d-none d-xl-block???" -->

                  <div v-for="(content, subIndex) in value.parts.part_content" :class="colorIdent(value.parts.part_name, subIndex)" class="rowwrap">
                      <b-form-row @mouseover="(type!='Invoices')?content.upHere = true:''" @mouseleave="(type!='Invoices')?content.upHere = false:''" 
                       :class="{howerRow: content.upHere, '': !content.upHere}" :key="content.id" class="formrowwrap">
                         

                         <div class="tnumber text-center" :class="((content.unit=='%')||(type=='Invoices')) ? '' : 'handle'"
                        :style="(content.done!=false) ? 'color:green' : ''"
                          @click="(type!='Invoices')?content.upHere = false+selectRow(value.parts.part_name, subIndex):''">
                             <span class="labeldat">#</span> <span class="mw100"> </span>{{(subIndex+1)}} 
                        </div>

                        

                        <div  class="tposition text-center" v-show="showPos">
                           <b-input @click.prevent.self :disabled="disablefild('position_number', content.id)" type="text" placeholder="Unit" :style="(content.done!=false) ? 'color:green' : ''"
                              class="cForm-input cinput" :value="content.position_number" @change="sendDataTable(content.id, 'position_number', $event)" @focus.native="changeDisable('f', 'position_number', content.id)" @blur.native="changeDisable('b', 'position_number', content.id)" :id="'position_number'+content.id"  />
                        </div>

                        

                        <b-tooltip v-if="type!='Invoices'" triggers="none" :show="disablefild('position_number', content.id)" :target="'position_number'+content.id">
                         {{disablefildUser('position_number', content.id)}}
                        </b-tooltip>

                        <div class="tdeschead text-center" :style="'width:'+computedWithDesc(value.parts.checkbox_list.flavours)+'%'">
                           <b-input  @click.prevent.self :disabled="disablefild('desk_head', content.id)" type="text" placeholder="Description Head" class="cForm-input"
                           :style="(content.done!=false) ? 'color:green' : ''" :value="content.description_head" @change="sendDataTable(content.id, 'description_head', $event)" @focus.native="changeDisable('f', 'desk_head', content.id)" @blur.native="changeDisable('b', 'desk_head', content.id)" :id="'desk_head'+content.id" />
                        </div>

                        

                        <b-tooltip  v-if="type!='Invoices'" triggers="none" :show="disablefild('desk_head', content.id)" :target="'desk_head'+content.id">
                            {{disablefildUser('desk_head', content.id)}}
                        </b-tooltip>

                        <div  class="tinfo text-center">
                           <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'desk_worck'+tableId+subIndex">
                              <span class="when-opened" :style="'color:'+computedStylePlus(content.description_work)">-</span>
                              <span class="when-closed" :style="'color:'+computedStylePlus(content.description_work)">+</span>
                           </b-link>
                        </div>

                        

                        <div  class="tcount text-center">
                           <b-input @click.prevent.self :disabled="disablefild('count', content.id)" @focus.native="$event.target.select();changeDisable('f', 'count', content.id);" type="text" :tabindex="(((tableId)*10)+(subIndex+1))"
                           placeholder="Count" class="cForm-input ainput" :style="(content.done!=false) ? 'color:green' : ''" :value="content.count.toString().replace('.',',')"
                           @change="sendDataTable(content.id, 'count', $event.replace(',','.'))"  @blur.native="changeDisable('b', 'count', content.id)" :id="'count'+content.id"  />
                        </div>

                        

                        <b-tooltip  v-if="type!='Invoices'" triggers="none" :show="disablefild('count', content.id)" :target="'count'+content.id">
                            {{disablefildUser('count', content.id)}}
                        </b-tooltip>

                        <div  class="tunit text-center">
                           <b-select :value="valOrProc(content, subIndex)" :disabled="disablefild('unit', content.id)"
                             class="select" style="min-width:45px"
                             @change="persent($event, subIndex, value.parts.checkbox_list, value.parts.part_content.length);sendDataTable(content.id, 'unit', $event);" @focus.native="changeDisable('f', 'unit', content.id)" @blur.native="changeDisable('b', 'unit', content.id)" :ref="'unit'+content.id"
                             :style="(content.done!=false) ? 'color:green' : ''" :id="'unit'+content.id">
                              <option v-for="opt in unitType" :disabled="disOptPercent(value.parts.part_content, opt)">
                                 {{opt}} 
                              </option>
                           </b-select>
                        </div>

                        

                        <b-tooltip  v-if="type!='Invoices'" triggers="none" :show="disablefild('unit', content.id)" :target="'unit'+content.id">
                            {{disablefildUser('unit', content.id)}}
                        </b-tooltip>

                        <div class="tprice text-right" style="font-weight: normal;">
                           <b-input v-if="content.unit!='%'" :disabled="disablefild('price', content.id)" @click.prevent.self type="text"  @focus.native="$event.target.select();changeDisable('f', 'price', content.id);"
                             placeholder="Price" class="cForm-input form-control rinput"
                              @change="sendDataTable(content.id, 'price', $event.replace(',','.'))" 
                             :value="content.price.replace('.',',')" :style="(content.done!=false) ? 'color:green' : ''"  @blur.native="changeDisable('b', 'price', content.id)" :id="'price'+content.id" />
                           <div v-else>
                              {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                value.parts.checkbox_list.selected, value.parts.part_content, 'summ')}}
                            </div>
                        </div>

                        

                          <b-tooltip  v-if="type!='Invoices'" triggers="none" :show="disablefild('price', content.id)" :target="'price'+content.id">
                            {{disablefildUser('price', content.id)}}
                        </b-tooltip>




                        <div  class="tsumm text-right " style="font-weight: normal;" v-if="addtaxColapse==true">
                           <div :style="content.status=='yes' ? '' : 'color:grey'" 
                              :class="{ 'calttax': content.alttax }"
                              @click="(type!='Invoices')?sendDataTable(content.id, 'alttax', content.alttax ? false : true):''">
                              <div v-if="content.unit!='%'" :title="content.count * content.price | thousandSeparator">
                                  {{content.count * content.price | thousandSeparator}}
                              </div>
                              <div v-else class="text-right"
                              :title="persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator">
                                  {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                    value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator}}

                                 <!--   {{sendDataTable(content.id, 'price', persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
value.parts.checkbox_list.selected, value.parts.part_content, '%') )}}  -->


                              </div>
                           </div>
                        </div>


                        <div v-else  class="tsumm text-right" style="font-weight: normal;" >
                           <div :style="content.status=='yes' ? '' : 'color:grey'">
                              <div v-if="content.unit!='%'" :title="content.count * content.price | thousandSeparator">
                                  {{content.count * content.price | thousandSeparator}}
                              </div>
                              <div v-else :title="persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator">
                                  {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                    value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator}}
                              </div>
                           </div>
                        </div>

                        

                        <div class="custom-control-inline tpercent"><span class="labeldat">+%</span><span class="mw100"> </span> 
                           <div  v-for="(select_from_allSelected, key) in value.parts.checkbox_list.allSelected" >
                              <div v-for="(opt, indexSelect) in value.parts.checkbox_list.flavours[key]" v-if="indexSelect==subIndex" class="ccbox"
                               :class="classRow(value.parts, key)" :style="(content.done!=false) ? 'color:green' : ''">
                               <!-- {{value.parts.checkbox_list.selected[key]}} -->
                             <!--     <b-form-checkbox type="checkbox" plain -->
                                  <b-form-checkbox type="checkbox" plain 
                                    :disabled="boxDisable(content.unit, key, indexSelect)||type=='Invoices'"
                                    :checked="value.parts.checkbox_list.selected[key]"
                                    :value="opt" 
                                    class="withoutPad"
                                    @change="checkbox_update($event, key, indexSelect);box($event, key, indexSelect)">
                                    </b-form-checkbox>
                              </div>
                           </div>
                        </div>
                        
                        

                        <div class="twithout text-center ccbox"  v-if="butDiscPerc=='%'"><span class="labeldat">-%</span><span class="mw100"> </span>
                           <b-form-checkbox :disabled="disablefild(null, null)" class="withoutPad"  v-if="content.status=='yes'" @change="sendDataTable(content.id, 'without', $event)"
                           plain style="margin: 0px;" :checked="without(content.without)" :style="(content.done!=false) ? 'color:green' : ''" />

                           <b-form-checkbox class="withoutPad" :disabled="disablefild(null, null)" v-else  checked="true" disabled plain style="margin: 0px;"  :style="(content.done!=false) ? 'color:green' : ''">
                            <div style="display:none">{{content.without=false}}</div>
                          </b-form-checkbox>
                        </div>
                        <div v-else style="display:none">
                          {{sendDataTable(content.id, 'without', false)}}
                          {{content.without=false}}
                        </div>

                        

                        <div class="tcalc text-center">
                           <b-form-select class="select" :disabled="disablefild('calc', content.id)" style="min-width:45px" :options="calc" @change="sendDataTable(content.id, 'status', $event)"
                           :value="content.status" :style="(content.done!=false) ? 'color:green' : ''" @focus.native="changeDisable('f', 'calc', content.id)" @blur.native="changeDisable('b', 'calc', content.id)" :id="'calc'+content.id"  />
                        </div>

                        

                         <b-tooltip  v-if="type!='Invoices'" triggers="none" :show="disablefild('calc', content.id)" :target="'calc'+content.id">
                            {{disablefildUser('calc', content.id)}}
                        </b-tooltip>
                        <div class="tdone text-center ccbox">
                               <b-form-checkbox class="withoutPad" :disabled="disablefild(null, null)" v-if="selectedWorkers.length!=0 || content.done!=false" plain style="margin: 0px;"
                           :checked="boxCecked(content.done)"
                           :style="(content.done!=false) ? 'color:green' : ''" :title="content.done"    @click.native.prevent.stop="(type!='Invoices')?subchangeWorker(subIndex, content.id):''"
                          
                           />
                        </div>

                        

                        <div class="tdelete text-center">
                           <b-link @click="subPartDel(content.id, subIndex);" class="fas fa-trash fa-w-16" :disabled="disablefild(null, null)" />
                        </div> 
                        
                          
                          <hr class="mline" />
                     </b-form-row>
                     <b-form-row >
                        <b-col cols="12" @click.prevent.self style="width:10%">
                           <b-collapse style="width:100%;" :id="'desk_worck'+tableId+subIndex">
                         
<!--                              <b-link v-b-toggle="'desk_worckI'+tableId+subIndex" class="butMore text-center"  v-if="content.description_from_price.length>0" style="width:3.3%">
                                 <span class="when-opened">-</span>
                                 <span class="when-closed">+</span>
                              </b-link> -->
                             <!--  <div style="width:3.3%"></div> -->



                              <vue-editor v-model="content.description_work"
                                :editorToolbar="customToolbar"
                                class="modEdit"
                                :disabled="disablefild('desk', content.id)"
                                @focus="changeDisable('f', 'desk', content.id)" 
                                :id="('t'+tableId + 'x' + subIndex)"
                                :ref="('t'+tableId + 'x' + subIndex)"
                                @text-change="checkInEditor($event, subIndex, content.id)"
                                @mouseleave.native="sendDataTable(content.id, 'description_work', content.description_work);changeDisable('b', 'desk', content.id)" />

                               <!-- @focus="changeDisable('f', 'desk', content.id)" -->
                                            <!-- @blur="sendDataTable(content.id, 'description_work', ($event.getText()!='\n\n')?$event.getText():'');changeDisable('b', 'desk', content.id)"  -->

                             <!--  <b-collapse style="width:96%;font-size:12px;padding-left:1.8%" :id="'desk_worckI'+tableId+subIndex" v-if="content.description_from_price.length>0">
                                {{content.description_from_price}}
                              </b-collapse> -->
                           </b-collapse>
                        </b-col>
                     </b-form-row>

                  </div>
               </draggable>

            </div>






            <b-row class="ttotalsumm">
               <b-col align-self="end" class="text-right" style="margin-right:22.6%">
               General {{ total(value.parts.part_content) | thousandSeparator }}</b-col>
            </b-row>
            <span style="color:grey">
               <b-row class="ttotalsumm">
                  <b-col align-self="end" class="text-right" style="margin-right:22.6%">
                  Alternative {{ alttotal(value.parts.part_content) | thousandSeparator}}</b-col>
               </b-row>
            </span>
            <br>
         </b-collapse>
  </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
import {VueEditor, Quill} from 'vue2-editor';
import axios from 'axios';
export default {
    components: {
        draggable,
        VueEditor
    },
    props: ['value', 'addtaxColapse', 'color', 'selectedWorkers', 'toggle', 'tableId', 'type', 'funcStop', 'butDiscPerc', 'nowTableId', 'unitType', 'looks'],
    data() {
        return {
        customToolbar: [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  // ['blockquote', 'code-block'],
  // [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  // [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  // [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  // [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  // [{ 'direction': 'rtl' }],                         // text direction
  // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
  // [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
  [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
  // [{ 'font': [] }],
  [{ 'align': [] }],
  // ['clean']                                         // remove formatting button
],
          // oldValue:null,
          cpvalue:null,
          showPos:true,
	  stopTimmer:false,
          oldarray: [],
          selectedLenght: 0,
          stopDis: false,
          window: {
            width: 0,
            height: 0
          },
            // unit_type: ['Psch.', '%', 'Stück.', 'Sack.', 'm²'],
            calc: ['yes', 'no', 'etc', 'alternative'],
           
            // disable: []
        } //return
    }, //data
    computed: {
        computedStylePlus: function() {
            return function(val) {
                if ((val.replace(/<[^>]+>/g, '').length) > 1) {
                    return 'blue;'
                } else {
                    return 'gray;'
                }
              }
        },
        colorIdent: function() {
            var vm = this;
            return function(partName, subIndex) {
                if (this.color.indexOf(partName + '-' + subIndex) != -1) {
                    return 'greenrow'
                } else {
                    return ''
                }
            }
        },
        computedWithDesc: function() {
            var vm = this;
            return function(val) {
                // var w = 32.8;
                var w = 32.8;
                var count = 0;
                for (var obj in val) {
                    if (count == 0) {
                        w = w + 0.6
                    }
                    if (count >= 2) {
                        w = w - 1.7
                    }
                     w = w - 0.6
                    //w = w - 7
                    count++
                }
                if (this.showPos==false) w=w+10
                return w;
            }
        },
        total: function() {
            var vm = this;
            return function(value) {
                var summa = 0
                value.forEach(function(val) {
                    if (val.status == 'yes') {
                        summa += val.count * val.price
                    }
                }) 
                return summa; //количество разрядов
            };
        },
        alttotal: function() {
            var vm = this;
            return function(value) {
                var summa = 0
                value.forEach(function(val) {
                    if (val.status != 'yes') {
                        summa += val.count * val.price
                    }
                })
                this.$emit('changeSum');
                return summa;
            };
        },
        persent_to_str: function() {
            var vm = this;
            return function(subIndex, all_obj, selected, content, summOrPercent) {
                var summa = 0
                for (var obj in all_obj) {
                    if (selected[obj].indexOf('temp' + (subIndex + 1)) != -1) {
                        selected[obj].forEach(function(val, index) {
                            if (val != 'temp' + (subIndex + 1)) {
                                val = val.split('temp')
                                val[1]--

                                var countx
                                var pricex

                                if (content[val[1]] == undefined){
                                  countx = 0
                                  pricex = 0
                                } else{
                                  countx = content[val[1]].count 
                                  pricex = content[val[1]].price
                                }

                                summa += countx * pricex
                            }
                        })
                    }
                }
                var persent_from_summa = ((summa / 100) * content[(subIndex)].count)
                content[(subIndex)].price = persent_from_summa / content[(subIndex)].count
                if (summOrPercent == '%') {
                    return persent_from_summa
                }
                if (summOrPercent == 'summ') {
                    return summa.toFixed(2);
                }
            }
        }
    },
    methods: {
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
        if (this.type=='Invoices') result = true
        
        return result
      },
      disablefildUser(fild, id){
        var result = (this.type=='Invoices') ? '' : 'you'
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
        if ((type_operation == 'f') & (this.stopTimmer==false)){
          setTimeout(()=>{

              this.$refs.unfocus.focus()

          }, 15000);
        }
	if (type_operation == 'b'){
		this.stopTimmer=true
	}

      },
      valOrProc(val, subIndex){
        if(val.unit=='f-proc'){
          val.unit = '%';
          this.persent('%', subIndex, this.value.parts.checkbox_list, this.value.parts.part_content.length);
          this.sendDataTable(val.id, 'unit', '%');
          return '%';
        } else {
          if(val.unit=='%'){
            val.count=(val.count==0)?1:val.count;  
          }
          return val.unit;
        }
        
      },
      without(val){
         //console.log(this.value.parts.part_content)
         if (val == 'false' || val == '' || val == null) {
            return false          
         } else{
            return true
         }

        
      },
      // chengeRow(){
      //   console.log(this.content.upHere)
      // },
      move(){
       this.oldarray =  JSON.parse(JSON.stringify(this.value.parts.part_content))
      },
      checkMove(event, model){
         this.nowTableId.forEach((v)=>{
            if(v.parts.id!=this.value.parts.id){
                v.parts.part_content.forEach((v1)=>{
                 if(v1.id == this.oldarray[event.oldIndex].id){
                    axios.get((document.URL.split('/')[4]=='sub')?'/update_id_sub':'/update_id', {
                      params: {
                        newIndex: event.newIndex,
                        oldPart: this.value.parts.id,
                        oldIndex: event.oldIndex,
                        newPart: v.parts.id
                      }
                  })
                 }
              })
            }
            if(v.parts.id==this.value.parts.id){
              if(v.parts.part_content.length==this.oldarray.length){


                axios.get((document.URL.split('/')[4]=='sub')?'/update_id_in_one_table_sub':'/update_id_in_one_table', {
                      params: {
                        newIndex: event.newIndex,
                        oldIndex: event.oldIndex,
                        newPart: v.parts.id
                      }
                   })
               }
            }
         })

        var obj
        for (obj in model.selected) {
          // if(event.from!=event.to){
          //   model.selected[obj].splice(model.selected[obj].indexOf('temp'+(event.oldIndex+1)), 1)
          //   this.box(null, obj, event.oldIndex)
          // } else{
          if(model.selected[obj].indexOf('temp'+(event.oldIndex+1)) >= 1){
            this.$set(model.selected[obj], model.selected[obj].indexOf('temp'+(event.oldIndex+1)), 'temp'+(event.newIndex+1))
            this.box(null, obj, event.oldIndex)
            this.box(model.flavours[obj][(event.newIndex)], obj, (event.newIndex))
          }
          // }
        }

      },
        disOptPercent(part, opt) {
            var count = 0
            part.forEach(function(val) {
                if (val.unit == '%') {
                    count++
                }
            })
            if ((part.length / count) < 2.5 && opt == '%') {
                return true
            }
        },
        selectionRows(){
          if(this.value.parts.part_content.length == this.color.length){
            this.value.parts.part_content.forEach((val, index)=>{
              this.selectRow(this.value.parts.part_name, index)  
            })
          } else{
            this.value.parts.part_content.forEach((val, index)=>{
                if(this.color[this.color.indexOf(this.value.parts.part_name+ '-' + index)]==undefined){
                this.selectRow(this.value.parts.part_name, index)
              }
            })
          }
          
        },
        selectRow(part, subIndex) {
            if (this.color.indexOf(part + '-' + subIndex) != -1) {
                this.color.splice(this.color.indexOf(part + '-' + subIndex), 1)
            } else {
                this.color.push(part + '-' + subIndex)
            }
        },
        classRow(arrayColumnOfPart, keyindex) {
            var countPercent = -1
            arrayColumnOfPart.part_content.forEach(function(val, index) {
                if (arrayColumnOfPart.part_content[index].upHere == true && val.unit == '%') {
                    for (var i = 0; i <= index; i++) {
                        if (countPercent < index && arrayColumnOfPart.part_content[i].unit == '%') {
                            countPercent++
                        }
                    }
                }
            })
            if ('in' + countPercent == keyindex) {
                return 'upHereColumn'
            }
        },
        boxDisable(unit, obj, str) {

            if (unit == '%') {
                return true
            } else {
                var dis = 0
                this.value.parts.checkbox_list.disable.forEach(function(val) {
                    var vals = val.split('-')
                    if (vals[0] != obj) {
                        if (vals[1] == str) {
                            dis++
                        }
                    }
                })
                if (dis != 0) {
                    return true
                }
            }
        },
        scheckStatus() {
            var obj
            for (obj in this.value.parts.checkbox_list.selected) {
                var countStr = 0
                var check = 0
                this.value.parts.part_content.forEach((val, index) => {
                    if (val.unit == '%') {
                        countStr++
                    } else {
                        var dis
                        this.value.parts.checkbox_list.disable.forEach(function(dval) {
                            dis = dval.split('-')
                            if (index == dis[1]) {
                                check++
                            }
                        })
                    }
                    if ((countStr + check) == this.value.parts.checkbox_list.flavours[obj].length) {
                        var objAls
                        for (objAls in this.value.parts.checkbox_list.allSelected) {
                            if (objAls == obj) {
                                var dis1
                                var uncheck = 0
                                this.value.parts.checkbox_list.disable.forEach(function(dval1) {
                                    dis1 = dval1.split('-')
                                    if (objAls == dis1[0]) {
                                        uncheck++
                                    }
                                })
                                if (uncheck != 0) {
                                    this.$set(this.value.parts.checkbox_list.allSelected, objAls, true)
                                }
                            }
                        }
                    } else {
                        this.$set(this.value.parts.checkbox_list.allSelected, obj, false)
                    }

                })
            }



                 // console.log(this.value.parts.checkbox_list.selected)
        },
        box(event, obj, str) {
                  // this.oldValue =  JSON.parse(JSON.stringify(this.value.parts.checkbox_list))
            var turn=''
            if (event != null) {
                this.value.parts.checkbox_list.disable.push(obj + '-' + str)
            } else {
                this.value.parts.checkbox_list.disable.splice(this.value.parts.checkbox_list.disable.indexOf(obj + '-' + str), 1)
            }
            this.scheckStatus()
        },
        subPartDel(subDel_id, subIndex) {
            if (confirm("Are you sure?")) {
              this.persent(1, subIndex, this.value.parts.checkbox_list, this.value.parts.part_content.length)

                axios.get((document.URL.split('/')[4]=='sub')?'/del_row_from_table_sub':'/del_row_from_table', {
                      params: {
                        id: subDel_id
                      }
                  })
                    // this.value.parts.part_content.splice(subDel_id, 1);
                    // for (var property in this.value.parts.checkbox_list.flavours) {
                    //     this.value.parts.checkbox_list.selected[property].splice(valuePart.parts.checkbox_list.selected[property]
                    //       .indexOf(this.value.parts.checkbox_list.flavours[property][subDel_id]), 1)
                    //     this.value.parts.checkbox_list.flavours[property].splice(subDel_id, 1)
                    // }
                }
        },
        persent(val, index, checkbox_in_table, how_many_rows) {
            this.persentCounter = val
            if (val == '%') {
                 this.add_column_checkbox(checkbox_in_table, how_many_rows)
                 var obj = Object.keys(checkbox_in_table.flavours)[Object.keys(checkbox_in_table.flavours).length - 1]
                 checkbox_in_table.selected[obj].push(checkbox_in_table.flavours[obj][index])
            }
            else {
                for (var obj in checkbox_in_table.flavours) {
                    var valCecked = checkbox_in_table.flavours[obj][index]
                    if (checkbox_in_table.selected[obj].indexOf(valCecked) != -1) {
                        this.remove_column_checkbox(checkbox_in_table, obj)
                    }
                }
            }
        },
        remove_column_checkbox(checkbox_in_table, key) {
            this.$delete(checkbox_in_table.indeterminate, key)
            this.$delete(checkbox_in_table.allSelected, key)
            this.$delete(checkbox_in_table.flavours, key)
            this.$delete(checkbox_in_table.selected, key)
            this.checkbox_update('column', 0, 0)
        },
        add_column_checkbox(checkbox_in_table, how_many_rows) {
            var sum_of_property = 0
            for (var property in checkbox_in_table.allSelected) {
                sum_of_property += 1
            }
            var flavour = new Array()
            for (var row = 1; row <= how_many_rows; row++) {
                flavour.push('temp' + row)
            }

            this.$set(checkbox_in_table.allSelected, 'in' + sum_of_property, false)
            this.$set(checkbox_in_table.flavours, 'in' + sum_of_property, flavour)
            this.$set(checkbox_in_table.indeterminate, 'in' + sum_of_property, false)
            this.$set(checkbox_in_table.selected, 'in' + sum_of_property, [])
            
            this.checkbox_update('column', 0, 0)
            
            this.scheckStatus()
        },
        toggleAll(event, target) {
            this.value.parts.checkbox_list.allSelected[target] = event
            if (this.value.parts.checkbox_list.allSelected[target]) {
                var obj
                this.value.parts.checkbox_list.flavours[target].forEach((val, index) => {
                    if (this.value.parts.part_content[index].unit != '%') {
                        var count = 0
                        for (obj in this.value.parts.checkbox_list.allSelected) {
                            if (this.value.parts.checkbox_list.flavours[target][index] == this.value.parts.checkbox_list.selected[obj][this.value.parts.checkbox_list.selected[obj]
                              .indexOf(this.value.parts.checkbox_list.flavours[target][index])]) count++
                        }
                        if (count == 0) {
                            this.value.parts.checkbox_list.selected[target].push(this.value.parts.checkbox_list.flavours[target][index])
                            this.box(this.value.parts.checkbox_list.flavours[target][index], target, index)
                        }
                    }
                })

            } else {
                var obj
                this.value.parts.checkbox_list.flavours[target].forEach((val, index) => {
                    if (this.value.parts.part_content[index].unit != '%') {
                        if (this.value.parts.checkbox_list.selected[target].indexOf(this.value.parts.checkbox_list.flavours[target][index]) != -1) {
                            this.value.parts.checkbox_list.selected[target].splice(this.value.parts.checkbox_list.selected[target].indexOf(this.value.parts.checkbox_list.flavours[target][index]), 1)
                            this.box(null, target, index)
                        }
                    }
                })
 
            }
this.checkbox_update('column', 0, 0)
        },
      //   subchangeWorker(event){
      //      console.log(event);
      // event.stopPropagation();

      //   },
      boxCecked(val){
        var ret
        if((val=='')&&(val==false)){
          ret = false
        } else{
          ret = true
        }
        return ret
      },
        subchangeWorker(index, id){
          var event = (this.value.parts.part_content[index].done=='');

          if(event==false){
            if(confirm("Are you sure?")) {
              this.changeWorker(false, index, id)
            }
          }
          if(event==true){
             this.changeWorker(true, index, id)
          }
        },
        changeWorker(event, index, id){
          if(event==false){
            this.value.parts.part_content[index].done=false
          } else{
            this.value.parts.part_content[index].done=this.selectedWorkers
          }

          this.sendDataTable(id, 'done', (event==false)?false:this.value.parts.part_content[index].done.join())
        },


        subtoggleAllWorkers(event){
        var event = !this.checkedAllWorkers()

          if(event==false){
            if(confirm("Are you sure?")) {
              this.toggleAllWorkers(false)
            }
          }
          if(event==true){
             this.toggleAllWorkers(true)
          }
        },

        toggleAllWorkers(event){
          if(event==false){
              this.value.parts.part_content.forEach((val)=>{
                val.done=false
                this.sendDataTable(val.id, 'done', '')
              })
          } else{
            this.value.parts.part_content.forEach((val)=>{
                val.done=this.selectedWorkers
                this.sendDataTable(val.id, 'done', this.selectedWorkers.join())
              })
          }
        },
        showAllworkers(){
          var countDone = 0
          this.value.parts.part_content.forEach(function(val){
              if (val.done != false) countDone++
          })
          if (this.selectedWorkers.length!=0 || countDone!=0) return true
        },
      checkedAllWorkers(){
        var countDone = 0
          this.value.parts.part_content.forEach(function(val){
              if (val.done != false) countDone++
          })
          if(countDone == this.value.parts.part_content.length || this.selectedWorkers==0){
            return true
          } else{
            return false
          }
      },
      sendDataTable(id, fild, data){
        if(fild=='without'){
           if (data == 'false' || data == '' || data == null) {
                data = 'Null'          
             } else{
                data = 'true'
             }
        }
        // data = (fild=='without')?((data=='')?'true':'false'):data
        data = (data=='')?'Null':data
        this.value.parts.part_content.forEach((v)=>{
             if(v.id==id){
              // v[fild]=isNaN(v[fild])?0:v[fild] ??
               if((v[fild]!=data) || (fild=='done') || (fild=='without') || (fild=='description_work') || (fild=='unit')){
                // console.log(id, fild, data)
                  axios.get((document.URL.split('/')[4]=='sub')?'/update_table_data_sub':'/update_table_data', {
                      params: {
                        id: id,
                        fild: fild,
                        data: data
                      }
                  })
               }
             }
        })

      },
    //   handleResize() {
    //   this.window.width = window.innerWidth;
    //   this.window.height = window.innerHeight;
    // },
    checkbox_update(event, key, indexSelect){
      if (event != 'column'){
        if (event == null){
 
             this.value.parts.checkbox_list.selected[key].splice(this.value.parts.checkbox_list.selected[key].indexOf('tepm'+(indexSelect+1)), 1)
        }else{
             this.value.parts.checkbox_list.selected[key].push(event)
        }
      }
        if(this.value.parts.checkbox_list.selected!=null){
          axios.get((document.URL.split('/')[4]=='sub')?'/update_checkbox_table_sub':'/update_checkbox_table', {
            params: {
              id: this.value.parts.id,
              fild: 'selected',
              data: this.value.parts.checkbox_list.selected
            }
          })
        }
      
    },
    checkInEditor(e, obj, id){
    if ((e.ops[1]!=undefined) && (e.ops[1].insert==' ')){
      var result
      var sval
      var separator
      var indexReplace, indexRuslt
      var safeEval = require('safe-eval')
        if(this.value.parts.part_content[obj].description_work!=(this.cpvalue?this.cpvalue.parts.part_content[obj].description_work:null)){
          var tname = 't' + this.tableId + 'x' + obj
          if(this.value.parts.part_content[obj].description_work!=null){
            if (this.value.parts.part_content[obj].description_work.indexOf(' ') != -1) {
              separator = (this.$refs[tname]!=undefined) && (this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getText():''
              separator = separator.replace(/\n/g, ' ')
              separator = separator.substring(0, separator.length - 1);
              separator = separator.split(' ')
              separator.splice(-1, 1)
              separator.forEach((val) => {
                if (val.search(/[a-zA-z=]/gim) == -1) {
                  if (val.search(/[-+*)(/]/gim) > -1) {
                    if (val.search(/[0-9]/gim) > -1) {
                      if (/[\d)]/.test(val[val.length - 1])) {
                        try {
                          result = this.$options.filters.thousandSeparator(safeEval(val))
                        } catch (e) {
                          result = '(not valid formula)'
                        }
                        sval = val.replace(/([-+*)(/])/gim, '$1&shy;') + '=' + result + ' '
                        indexRuslt = result.length ? result.length : 4
                        indexReplace = this.value.parts.part_content[obj].description_work.indexOf(val) + indexRuslt + 6
                        this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
                        this.value.parts.part_content[obj].description_work.replace(val, sval)
                        )
                        this.$refs[tname][0].quill.setSelection(indexReplace, 0)
                      }
                    }
                  }
                }
              })
            }
          }
        }
      this.cpvalue = JSON.parse(JSON.stringify(this.value))
      this.sendDataTable(id, 'description_work', this.value.parts.part_content[obj].description_work)
     }
    // if (
    // ((e.ops[0]!=undefined) && (e.ops[0].delete>0)) ||
    // ((e.ops[1]!=undefined) && (e.ops[1].delete>0)) ||
    // ((e.ops[0]!=undefined) && (e.ops[0].attributes!=undefined)) ||
    // ((e.ops[1]!=undefined) && (e.ops[1].attributes!=undefined)) ||
    // ((e.ops[1]!=undefined) && (e.ops[1].insert=='\n'))
    // ){
    //   this.sendDataTable(id, 'description_work', this.value.parts.part_content[obj].description_work)
    // }
  }
  },
    // watch: {
    //     value: {
    //         handler: function() {
    //             var result
    //             var sval
    //             var separator
    //             var indexReplace, indexRuslt
    //             var safeEval = require('safe-eval')
    //             for (var obj in this.value.parts.part_content) {
    //               if(this.value.parts.part_content[obj].description_work!=(this.cpvalue?this.cpvalue.parts.part_content[obj].description_work:null)){
    //                 console.log(this.value.parts.part_content[obj].description_work)
    //                 var tname = 't' + this.tableId + 'x' + obj
    //                 if(this.value.parts.part_content[obj].description_work!=null){
    //                 if (this.value.parts.part_content[obj].description_work.indexOf(' ') != -1) {
    //                     separator = (this.$refs[tname]!=undefined) && (this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getText():''
    //                     separator = separator.replace(/\n/g, ' ')
    //                     separator = separator.substring(0, separator.length - 1);
    //                     separator = separator.split(' ')
    //                     separator.splice(-1, 1)
    //                     separator.forEach((val) => {
    //                         if (val.search(/[a-zA-z=]/gim) == -1) {
    //                             if (val.search(/[-+*)(/]/gim) > -1) {
    //                                 if (val.search(/[0-9]/gim) > -1) {
    //                                     if (/[\d)]/.test(val[val.length - 1])) {
    //                                         try {
    //                                             result = this.$options.filters.thousandSeparator(safeEval(val))
    //                                         } catch (e) {
    //                                             result = '(not valid formula)'
    //                                         }
    //                                         sval = val.replace(/([-+*)(/])/gim, '$1&shy;') + '=' + result + ' '
    //                                         indexRuslt = result.length ? result.length : 4
    //                                         indexReplace = this.value.parts.part_content[obj].description_work.indexOf(val) + indexRuslt + 6
    //                                         this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
    //                                         this.value.parts.part_content[obj].description_work.replace(val, sval)
    //                                         )
    //                                         this.$refs[tname][0].quill.setSelection(indexReplace, 0)
    //                                     }
    //                                 }
    //                             }
    //                         }
    //                     })
    //                 }
    //               }
    //             }
    //           }
    //             this.cpvalue = JSON.parse(JSON.stringify(this.value))
    //         },
    //         deep: true,
    //     }
    // },
         mounted(){
            this.scheckStatus()
         
         },
  //         created() {
  //   window.addEventListener('resize', this.handleResize)
  //   this.handleResize();
  // },
  //        destroyed() {
  //   window.removeEventListener('resize', this.handleResize)
  // },
}
</script>
<style type="text/css">
.modEdit  .ql-toolbar {
/*  display: none;*/
}
.modEdit {
  width: 100%;
  padding-left: 15px;
  padding-right: 35px;
}
.ql-editor{
    font-size: 13px !important;
    min-height: 0px !important;
}




@media screen and (min-width: 991px) {
  .tnumber {
      font-size: 12px;
      font-weight: normal;
      width: 5%;
      max-width: 20px;
  }
  .tposition {
      font-size: 12px;
      font-weight: bold;
      width: 10%;
  }
  .tdeschead {
      font-size: 12px;
      font-weight: bold;
      width: 32%;
  }
  .tinfo {
      font-size: 12px;
      font-weight: bold;
      width: 5%;
      max-width: 20px;
  }
  .tcount {
      font-size: 12px;
      font-weight: bold;
      width: 4%;
  }
  .tunit {
      font-size: 12px;
      font-weight: bold;
      width: 8%;
  }
  .tprice {
      font-size: 12px;
      font-weight: bold;
      width: 8%;
  }
  .tsumm {
      font-size: 12px;
      font-weight: bold;
      padding-top: 2px;
      overflow: hidden;
      width: 9%;
  }
  .ttotalsumm {
      font-size: 12px;
      font-weight: bold;
      padding-top: 2px;
  }
  .twithout {
      font-size: 12px;
      font-weight: bold;
      width: 6%;
      max-width: 25px;
  }
  .tpercent {
      font-size: 12px;
      font-weight: bold;
      min-width: 5%;
      padding-left: 10px;
      margin-right: 5px;
  }
  .tcalc {
      font-size: 12px;
      font-weight: bold;
      width: 10%;
  }
  .tdone {
       font-size: 12px;
      font-weight: bold;
      width: 6%;
      max-width: 25px;
  }
  .tdelete {
      font-size: 12px;
      padding: 0;
      margin: 0;
      width: 2%;
  }

  .labeldat{
    display: none;
  }
  .headtable {
    width:100%;
    white-space: nowrap;
    flex-wrap:nowrap;
  }
  .headtablewarp {
    width:100%;
    white-space: nowrap;
    flex-wrap:nowrap;
  }
  .rowwrap {
    width:100%;
    white-space: nowrap;
    flex-wrap:nowrap;
  }
  .formrowwrap {
    height:20px;
    width:100%;
    white-space: nowrap;
    flex-wrap:nowrap;
  }
  .mline{
    display: none;
  }
  .mw100{
    display: none;
  }
}

@media screen and (max-width: 990px) {
  .tnumber {
        padding: 2px;
      font-size: 12px;
      font-weight: normal;
      width: 5%;
      width: 100%;
      text-align: left !important;
  }
  .tposition {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
  }
  .tposition .cinput{
    text-align: left !important;
  }
  .tdeschead {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100% !important;
  }
  .tinfo {
      padding: 10px;
      font-size: 18px;
      font-weight: bold;
      width: 5%;
      width: 100%;
      text-align: left !important;
  }
  .tcount {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
      text-align: left !important;
  }
  .tcount .ainput{
    text-align: left !important;
  }
  .tunit {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
      text-align: left !important;
  }
  select {
    padding-left: 2px !important;
  }
  .tprice {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
      text-align: left !important;
  }
  .tprice .rinput{
    text-align: left !important;
  }
  .tsumm {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;

      overflow: hidden;
      width: 100%;
      text-align: left !important;
  }
  .ttotalsumm {
      font-size: 12px;
      font-weight: bold;
      padding-top: 2px;
  }
  .twithout {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
      text-align: left !important;
          display: inline-flex;
    margin-right: 1rem;
        white-space: nowrap;
  }

  .tpercent {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;

      margin-right: 0px;
  }
  .tcalc {
        padding: 2px;
      font-size: 12px;
      font-weight: bold;
      width: 100%;
  }
  .tdone {
       font-size: 12px;
      font-weight: bold;
      width: 6%;
      width: 100%;
  }
  .tdelete {
        padding: 2px;
      font-size: 12px;

      margin: 0;
      width: 100%;
      text-align: left !important;
  }
  .headtable{
    display: none;
  }
  .headtablewarp{
    width:100%;
/*    white-space: nowrap;
    flex-wrap:nowrap;*/
  }
  .rowwrap {
    width:100%;
/*    white-space: nowrap;
    flex-wrap:nowrap;*/
  }
  .formrowwrap {
    display: block;
    padding:  2px; 
    margin: 2px;
  }
  .labeldat {
    text-align: right;
    font-weight: bold;
    font-style: normal;
  }
  .mline{
    background: #000;
  }
  .mw100{
    width: 100%;
  }
}
</style>