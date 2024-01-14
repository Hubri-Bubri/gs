<template>
  <div>
    <slot name="tableHead" :tableId="tableId" @click.prevent.self></slot>
    <input ref="unfocus" style="width: 0px; height: 0px; position: absolute; top: 0; left: 0; margin:0; padding:0; border: 0"></input>
        <div :class="{ 'table-dark': toggle }" :id="'partx'+value.parts.id">
          <b-table-simple small borderless responsive class="withoutBorderInInput">
            <b-thead>
              <b-tr>
                <b-th style='width:40px;'>
                  <b-icon icon='hash' aria-hidden="true" />
                  <b-icon icon='arrow-bar-right' aria-hidden="true" @click.stop="showPos=showPos?false:true" v-show="!showPos" />
                </b-th>
                <b-th v-show="showPos" style='min-width:70px;'>
                  <b-icon icon='arrow-bar-left' aria-hidden="true" @click.stop="showPos=showPos?false:true"  />
                  <b-icon :icon="'sort-numeric-'+sort" aria-hidden="true" class="ml-3"  @click.stop="sort=(sort=='down')?'up':'down';byField(sort)"/>
                </b-th>
                     <!-- <b-col :style="'width:'+(computedWithDesc(value.parts.checkbox_list.flavours)+(showPos?0:-10))+'%'">Description Head</b-col> -->
                <b-th :style="'max-width:'+(width/4.90)+'px;white-space: nowrap;overflow: hidden;'">{{$t('calcTable.description')}}</b-th>
                <b-th  class="text-center">=</b-th>
                <b-th style="width:72px;" class="text-center">{{$t('calcTable.unit')}}</b-th>
                <b-th  class="text-center">€</b-th>
                <b-th  class="text-center">∑</b-th>
                <b-th :style="'width:'+(computedWithPercent(value.parts.checkbox_list.flavours)*15+10)+'px;'">
                  <b-form inline >
                    <div v-for="(select_from_allSelected, key) in value.parts.checkbox_list.allSelected">
                      <b-form-checkbox plain :disabled="disablefild(null, null)" 
                      v-model="value.parts.checkbox_list.allSelected[key]"
                      @change="toggleAll($event, key)"  class="ccbox"
                      >&nbsp;</b-form-checkbox>
                    </div>
                  </b-form inline>
                </b-th>
                <b-th v-if="(butDiscPerc=='%')&&(discP>0)">-%</b-th>
                <b-th >{{$t('calcTable.calculation')}}</b-th>
                <b-th>
                  <b-form inline>
                    <b-form-checkbox :disabled="disablefild(null, null)" plain  v-if="showAllworkers()" class="ccbox"
                    @click.native.prevent.stop="subtoggleAllWorkers()" :checked="checkedAllWorkers()">&nbsp;</b-form-checkbox>
                  </b-form>
                </b-th>
                <b-th >X</b-th>
              </b-tr>
            </b-thead>
            <draggable v-model="value.parts.part_content" element="b-tbody" :options="{handle:'.handle', group:'a', animation:150}"
            :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)" @choose="move()">
                  <!-- calss="d-none d-xl-block???" -->

                  <!-- <div v-for="(content, subIndex) in value.parts.part_content" :class="colorIdent(value.parts.part_name, subIndex)"> -->

                  
                      <b-tr @mouseover="content.upHere = true" @mouseleave="content.upHere = false" 
                       :class="{howerRow: content.upHere, '': !content.upHere}" :key="content.id" 

                       v-for="(content, subIndex) in value.parts.part_content" 

                       >
                        <b-td :class="(content.unit=='%') ? 'text-center' : 'handle text-center'" 
                        :style="(content.done!=false) ? 'vertical-align:top;color:green' : 'vertical-align:top;'"
                          @click="content.upHere = false+selectRow(value.parts.part_name, subIndex)">
                             {{(subIndex+1)}} 
                        </b-td>
                        <b-td v-show="showPos" style="vertical-align:top;" >


                          <div
                          :contenteditable="!disablefild('position_number', content.id)"
                          :style="(content.done!=false) ? 'color:green' : ''"
                          class="diveditable"
                          @click.prevent.self
                          @blur="sendDataTable(content.id, 'position_number', $event.target.innerText);changeDisable('b', 'position_number', content.id);"
                          @focus="changeDisable('f', 'position_number', content.id)"
                          :id="'position_number'+content.id" v-html="content.position_number" />


           <!--                <b-input size="sm" @click.prevent.self :disabled="disablefild('position_number', content.id)" type="text"
                          placeholder="Unit"
                          :style="('min-width:'+wp[subIndex]+'ch;')+((content.done!=false) ? 'color:green;' : '')"
                          :value="content.position_number" @change="sendDataTable(content.id, 'position_number', $event)"
                          @focus.native="changeDisable('f', 'position_number', content.id)" @blur.native="changeDisable('b', 'position_number', content.id)"
                          :id="'position_number'+content.id"  /> -->
                        </b-td>
                        <b-tooltip triggers="none" :show="disablefild('position_number', content.id)" :target="'position_number'+content.id">
                         {{disablefildUser('position_number', content.id)}}
                        </b-tooltip>
                        <b-td :title="(content.description_work&&content.description_work!=0)?content.description_work:'(You have not added an explanation for this item)'">
                        
                      
                        <!-- <b-icon icon='calculator' aria-hidden="true"  @click="checkInEditor(content.description_head, content.id)"/> -->

<!--                         <b-form-textarea
                          :title="content.description_work"
                          size="sm"
                          :class="detectNewRow(content.description_head, 'desk_head'+content.id)"
                          :disabled="disablefild('desk_head', content.id)" type="text"
                          placeholder="Description Head" rosw="1" max-rows="6"
                          :style="(content.done!=false) ? 'color:green;' : ''"
                          :value="content.description_head"
                          @click.prevent.self
                          @change="sendDataTable(content.id, 'description_head', $event)"
                          @keyup.space.native="$event.target.value=checkInEditor($event.target.value, content.id)"
                          @keyup.native="content.description_head=$event.target.value"
                          @focus.native="changeDisable('f', 'desk_head', content.id)"
                          @blur.native="changeDisable('b', 'desk_head', content.id)"
                          :id="'desk_head'+content.id" /> -->

 <!-- :contenteditable="!disablefild('desk_head', content.id)" -->
                          <div
                          contenteditable="plaintext-only"
                         
                          
                          :style="(content.done!=false) ? 'color:green;width:100%;padding-left:4px;' : 'width:100%;padding-left:4px;'"
                          @click.prevent.self
                          @keyup.space="($event.target.innerHTML.indexOf('= ') != -1 )?(content.description_head = checkInEditor($event, content.id)):null"
                          @blur="sendDataTableHead(content.id, $event.target.innerHTML)"
                          @focus="changeDisable('f', 'desk_head', content.id)"
                          :id="'desk_head'+content.id" v-html="description(content.description_head)" />
                          <!-- <button @click="setCaret('desk_head'+content.id)">test</button> -->
        

                       
      <!--                   <b-col cols="1" class="text-left mr-0 ml-0 pr-0 pl-0">
                          <b-link style="text-decoration: none;font-weight: normal;" v-if="edopen=='desk_worck'+tableId+subIndex">
                            <span :style="'color:'+computedStylePlus(content.description_work)" @click="edopen=null">-</span>
                          </b-link>
                          <b-link style="text-decoration: none;font-weight: normal;" v-else>
                            <span :style="'color:'+computedStylePlus(content.description_work)" @click="edopen='desk_worck'+tableId+subIndex" >+</span>
                          </b-link>
                        </b-col> -->
                
                       
                        
                        <!--   <textarea rows="1" style="height:1em;" id="text"></textarea> -->
                        </b-td>
                        <b-tooltip triggers="none" :show="disablefild('desk_head', content.id)" :target="'desk_head'+content.id">
                            {{disablefildUser('desk_head', content.id)}}
                        </b-tooltip>

                        <b-td style="vertical-align:top;text-align:right;">
                          <div
                          :contenteditable="!disablefild('count', content.id)"
                          :style="(content.done!=false) ? 'color:green' : ''"
                          class="diveditable text-right"
                          @click.prevent.stop="selectAll('count'+content.id)"
                          @blur="toDigital($event.target.innerText, 'count', content.id)"
                          @focus="changeDisable('f', 'count', content.id)"
                          :id="'count'+content.id" v-html="valueDigital(content.count)" />

       <!--                     <b-input class="text-right" size="sm" @click.prevent.self :disabled="disablefild('count', content.id)"
                            @focus.native="$event.target.select();changeDisable('f', 'count', content.id);" type="text" :tabindex="(((tableId)*10)+(subIndex+1))"
                           placeholder="Count" 
                           :style="('min-width:'+wc[subIndex]+'ch;')+((content.done!=false) ? 'color:green;' : '')"
                           :value="content.count.toString().replace('.',',')"
                           @change="sendDataTable(content.id, 'count', $event.replace(',','.'))"
                            @blur.native="changeDisable('b', 'count', content.id)" :id="'count'+content.id"  /> -->


                        </b-td>
                        <b-tooltip triggers="none" :show="disablefild('count', content.id)" :target="'count'+content.id">
                            {{disablefildUser('count', content.id)}}
                        </b-tooltip>
                        <b-td style="vertical-align:top;">
                           <b-select  class="text-center"  size="sm" :value="valOrProc(content, subIndex)" :disabled="disablefild('unit', content.id)"
                             @change="persent($event, subIndex, value.parts.checkbox_list, value.parts.part_content.length);sendDataTable(content.id, 'unit', $event);" @focus.native="changeDisable('f', 'unit', content.id)" @blur.native="changeDisable('b', 'unit', content.id)" :ref="'unit'+content.id"
                             :style="(content.done!=false) ? 'color:green' : ''" :id="'unit'+content.id">
                              <option v-for="opt in unitType" :disabled="disOptPercent(value.parts.part_content, opt)">
                                 {{opt}} 
                              </option>
                           </b-select>
                        </b-td>
                        <b-tooltip triggers="none" :show="disablefild('unit', content.id)" :target="'unit'+content.id">
                            {{disablefildUser('unit', content.id)}}
                        </b-tooltip>
                        <b-td style="vertical-align:top;text-align:right;">


                          <div  v-if="content.unit!='%'"
                          :contenteditable="!disablefild('price', content.id)"
                          :style="(content.done!=false) ? 'color:green' : ''"
                          class="diveditable text-right"
                          @click.prevent.stop="selectAll('price'+content.id)"
                          @blur="toDigital($event.target.innerText, 'price', content.id)"
                          @focus="changeDisable('f', 'price', content.id)"
                          :id="'price'+content.id" v-html="valueDigital(content.price)" />

              <!--              <b-input  class="text-right" size="sm" v-if="content.unit!='%'" :disabled="disablefild('price', content.id)" @click.prevent.self type="text"
                           @focus.native="$event.target.select();changeDisable('f', 'price', content.id);"
                             placeholder="Price"
                              @change="sendDataTable(content.id, 'price', $event.replace(',','.'))" 
                             :value="content.price.replace('.',',')"

                            :style="('min-width:'+wpr[subIndex]+'ch;')+((content.done!=false) ? 'color:green;' : '')"
                             @blur.native="changeDisable('b', 'price', content.id)" :id="'price'+content.id" /> -->
                           <div v-else>
                              {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                value.parts.checkbox_list.selected, value.parts.part_content, 'summ')}}
                            </div>
                        </b-td>
                          <b-tooltip triggers="none" :show="disablefild('price', content.id)" :target="'price'+content.id">
                            {{disablefildUser('price', content.id)}}
                        </b-tooltip>
                        <b-td v-if="addtaxColapse==true"  style="vertical-align:top;">
                          <div :style="content.status=='yes' ? '' : 'color:grey'" 
                              :class="{ 'calttax': content.alttax }"
                              @click="(type!='Invoices')?sendDataTable(content.id, 'alttax', content.alttax ? false : true):''">
                              <div  class="text-right" v-if="content.unit!='%'" :title="content.count * content.price | thousandSeparator">
                                  {{(content.status=='no')?'0':$options.filters.thousandSeparator(content.count * content.price)}}
                              </div>
                              <div v-else  class="text-right" :style="(content.done!=false) ? 'color:green' : ''"
                              :title="persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator">
                                  {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                    value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator}}
                              </div>
                           </div>
                        </b-td>
                        <b-td v-else style="vertical-align:top;">
                           <div :style="content.status=='yes' ? '' : 'color:grey'">
                              <div  class="text-right" v-if="content.unit!='%'" :title="content.count * content.price | thousandSeparator" :style="(content.done!=false) ? 'color:green' : ''">
                                  {{(content.status=='no')?'0':$options.filters.thousandSeparator(content.count * content.price)}}
                              </div>
                              <div  class="text-right" v-else :title="persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator" :style="(content.done!=false) ? 'color:green' : ''">
                                  {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                    value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator}}
                              </div>
                           </div>
                        </b-td>
                        <b-td style="vertical-align:top;">
                          <b-form inline>
                           <div  v-for="(select_from_allSelected, key) in value.parts.checkbox_list.allSelected" >
                              <div v-for="(opt, indexSelect) in value.parts.checkbox_list.flavours[key]" v-if="indexSelect==subIndex" class="ccbox"
                               :class="classRow(value.parts, key)" :style="(content.done!=false) ? 'color:green' : ''">
                                  <b-form-checkbox plain 
                                  :disabled="boxDisable(content.unit, key, indexSelect)"
                                  :checked="value.parts.checkbox_list.selected[key]"
                                  :value="opt" 
                                  @change="checkbox_update($event, key, indexSelect);box($event, key, indexSelect)">
                                  &nbsp;
                                  </b-form-checkbox>
                              </div>
                           </div>
                         </b-form>
                        </b-td>
                        <b-td v-if="(butDiscPerc=='%')&&(discP>0)" style="vertical-align:top;">
                          <b-form inline>
                           <b-form-checkbox :disabled="disablefild(null, null)"   v-if="content.status=='yes'" @change="sendDataTable(content.id, 'without', $event)"
                           plain :checked="without(content.without)" :style="(content.done!=false) ? 'color:green' : ''" class="ccbox">&nbsp;</b-form-checkbox>
                           <b-form-checkbox  :disabled="disablefild(null, null)" v-else class="ccbox"
                           checked="true" disabled plain  :style="(content.done!=false) ? 'color:green' : ''">
                            <div style="display:none">{{content.without=false}}</div>&nbsp;
                          </b-form-checkbox>
                        </b-form>
                        </b-td>
                        <b-td v-if="butDiscPerc=='P'" style="display:none">
                          <!-- {{sendDataTable(content.id, 'without', false)}} -->
                          {{content.without=false}}
                        </b-td>
                        <b-td style="vertical-align:top;">
                           <b-form-select  size="sm"  :disabled="disablefild('calc', content.id)" style="min-width:45px" :options="calc" @change="sendDataTable(content.id, 'status', $event)"
                           :value="content.status" :style="(content.done!=false) ? 'color:green' : ''" @focus.native="changeDisable('f', 'calc', content.id)" @blur.native="changeDisable('b', 'calc', content.id)" :id="'calc'+content.id"  />
                        </b-td>
                         <b-tooltip  triggers="none" :show="disablefild('calc', content.id)" :target="'calc'+content.id">
                            {{disablefildUser('calc', content.id)}}
                        </b-tooltip>
                        <b-td   style="vertical-align:top;">
                          <b-form inline :title="content.done">
                        
                          <b-form-checkbox :disabled="disablefild(null, null)" v-if="selectedWorkers.length!=0 || content.done!=false"
                          plain  class="ccbox"
                          :checked="boxCecked(content.done)"
                          :style="(content.done!=false) ? 'color:green' : ''"
                          @click.native.prevent.stop="(type!='Invoices')?subchangeWorker(subIndex, content.id):''"
                          >&nbsp;</b-form-checkbox>
                        
                      </b-form>
                        </b-td>
                        <b-td   style="vertical-align:top;">
                          <b-icon icon="trash" aria-hidden="true" @click="subPartDel(content.id, subIndex);" :visible="!disablefild(null, null)"></b-icon>
                        </b-td> 
                     </b-tr>
                      <!--   <b-tr v-if="edopen=='desk_worck'+tableId+subIndex"> -->
             
                         
<!--                              <b-link v-b-toggle="'desk_worckI'+tableId+subIndex" class="butMore text-center"  v-if="content.description_from_price.length>0" style="width:3.3%">
                                 <span class="when-opened">-</span>
                                 <span class="when-closed">+</span>
                              </b-link> -->
                             <!--  <div style="width:3.3%"></div> -->




<!--                                 <vue-editor v-model="content.description_work"
                                :editorToolbar="customToolbar"
                                class="modEdit"
                                :disabled="disablefild('desk', content.id)"
                                @focus="changeDisable('f', 'desk', content.id)" 
                                :id="('t'+tableId + 'x' + subIndex)"
                                :ref="('t'+tableId + 'x' + subIndex)"
                                @text-change="checkInEditor($event, subIndex, content.id)"
                                @mouseleave.native="sendDataTable(content.id, 'description_work', content.description_work);changeDisable('b', 'desk', content.id)" /> -->







                               
            
                              
                              <!-- <b-icon icon='calculator' aria-hidden="true"  @click="checkInEditor('t'+tableId + 'x' + subIndex, content.id)"
                              style="position:relative;left:24px;top: 16px;width:25px;z-index:2;"/> -->
<!-- 
                              <span v-show="(disablefildUser(('t'+tableId + 'x' + subIndex), content.id)!='you')" style="position:relative;left:30px;top: 16px;width:18px;z-index:2;">
                              {{disablefildUser(('t'+tableId + 'x' + subIndex), content.id)}}</span> -->

                             <!--  <b-td colspan="12"><b-container>{{content.description_work}}</b-container></b-td> -->
<!--                               <vue-editor
                                :value="content.description_work"
                                :editorToolbar="customToolbar"
                                class="modEdit text-right"
                                style="position:relative;top: -20px;z-index:1;"
                                :id="('t'+tableId + 'x' + subIndex)"
                                :ref="('t'+tableId + 'x' + subIndex)"

                                :disabled="disablefild(('t'+tableId + 'x' + subIndex), content.id)?'disabled':false"
                                @focus="changeDisable('f', ('t'+tableId + 'x' + subIndex), content.id)"
                                @mouseleave.native="sendDataTable(content.id, 'description_work', $refs['t'+tableId + 'x' + subIndex][0].quill.getHTML());content.description_work = $refs['t'+tableId + 'x' + subIndex][0].quill.getHTML();changeDisable('b', ('t'+tableId + 'x' + subIndex), content.id);" 
                                @blur="sendDataTable(content.id, 'description_work', $refs['t'+tableId + 'x' + subIndex][0].quill.getHTML());content.description_work = $refs['t'+tableId + 'x' + subIndex][0].quill.getHTML();changeDisable('b', ('t'+tableId + 'x' + subIndex), content.id);" 

                                 >
                
                                 </vue-editor>
 -->
<!--                          <b-tooltip  triggers="none" :show="disablefild(('t'+tableId + 'x' + subIndex), content.id)" :target="('t'+tableId + 'x' + subIndex)+content.id">
                            {{disablefildUser(('t'+tableId + 'x' + subIndex), content.id)}}
                        </b-tooltip>
 -->

                              
                              <!-- <b-button @click="addtable('t'+tableId + 'x' + subIndex, content.id)">TABLE</b-button> -->
<!-- 

@mouseleave.native="sendDataTable(content.id, 'description_work', $refs['t'+tableId + 'x' + subIndex][0].quill.getHTML())"
  checkInEditor((($refs['t'+tableId + 'x' + subIndex]!=undefined)&&($refs['t'+tableId + 'x' + subIndex].length!=0)?$refs['t'+tableId + 'x' + subIndex][0].quill.getHTML():''), 't'+tableId + 'x' + subIndex, content.id);changeDisable('b', 'desk', content.id) -->
                               <!-- @focus="changeDisable('f', 'desk', content.id)" -->
                                            <!-- @blur="sendDataTable(content.id, 'description_work', ($event.getText()!='\n\n')?$event.getText():'');changeDisable('b', 'desk', content.id)"  -->

                             <!--  <b-collapse style="width:96%;font-size:12px;padding-left:1.8%" :id="'desk_worckI'+tableId+subIndex" v-if="content.description_from_price.length>0">
                                {{content.description_from_price}}
                              </b-collapse> -->
                       
               <!--          </b-tr> -->
               
                     <!--  </b-tbody> -->
                  <!-- </div> -->
               </draggable>
</b-table-simple>
         <b-row class="ttotalsumm">
               <b-col align-self="end" class="text-right" style="margin-right:22.6%">
               {{$t('projectDetail.total')}} {{ total(value.parts.part_content) | thousandSeparator }} €</b-col>
            </b-row>
            <span style="color:grey" v-if="(alttotal(value.parts.part_content)!=0)">
               <b-row class="ttotalsumm">
                  <b-col align-self="end" class="text-right" style="margin-right:22.6%">
                {{$t('projectDetail.totalAlternative')}} {{ alttotal(value.parts.part_content) | thousandSeparator}} €</b-col>
               </b-row>
            </span>
            <br>
            </div>






   

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
    props: ['value', 'addtaxColapse', 'color', 'selectedWorkers', 'toggle', 'tableId', 'type', 'funcStop', 'butDiscPerc', 'nowTableId', 'unitType', 'looks', 'discP'],
    data() {
        return {
        width: null,
        sort:'down',
        edopen:null,
        customToolbar: [
        [{ list: "check" }],
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
          // cpvalue:null,
          showPos:true,
          wc:[],
          wpr:[],
          wp:[],
	  stopTimmer:false,
          oldarray: [],
          selectedLenght: 0,
          stopDis: false,
          // window: {
          //   width: 0,
          //   height: 0
          // },
            // unit_type: ['Psch.', '%', 'Stück.', 'Sack.', 'm²'],
            calc: ['yes', 'no', 'etc', 'alternative'],
           
            // disable: []
        } //return
    }, //data
    computed: {
      // detectNewRow: function() {
      //       return function(val, id) {

      //         var el = document.getElementById(id)
      //         var h = !(el==null)?el.scrollHeight:0 
              
      //         var short = 'short'
      //         if (h>17) {
      //           short = 'notshort'
      //         }
      //         if (val.includes('\n')){
      //           short = 'notshort'
      //         }

      //         // console.log(h, el, short)
      //         return short
      //       }
      //   },
        computedStylePlus: function() {
            return function(val) {

              var  brcount = val.split('<br>').length-1
              var countchar = val.replace(' ', '').replace(/<[^>]+>/g, '').length;

              // console.log(val, countchar, brcount);
                if (countchar+brcount > 1) {
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
        computedWithPercent: function() {
          return function(val) {
            var count = 0;
              for (var obj in val) {
                count++
              }
            return count;
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
                    if (val.status == 'alternative') {
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
    selectAll(id){
    function selectElementContents(el) {
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
    }

    var el = document.getElementById(id);
    selectElementContents(el);
    },
    valueDigital(model){
      var value = model
      if (value == null){
        value = '0.0'
      }
      value = value.replace(',','.')
      // console.log(1, value)
      var value = parseFloat(value)
      // console.log(2, value)
      value = value.toString()
      value = value.replace('.',',')
      value = (value=='NaN')?0:value
      if (value.length < 3){
        value = '&nbsp;&nbsp;'+value
        // console.log(4, value)
      }
      return value
    },
    toDigital(event, fild, id){
      var value = event.toString().replace(',','.');
      value = parseFloat(value);
      value = (value.toString()=='NaN')?0:value;
      // console.log(value);
      this.sendDataTable(id, fild, value.toString());
      this.changeDisable('b', fild, id);
    },
    inputWidth(val, tw, index){
      tw[index] = val.length
    },
    description(val){
      if (val!=null){
        return val
      }
      if (val==null){
        return '(Not have a data)'
      }
    },
    //   resize(id) {
    //   let element = this.$refs['desk_head'+id][0];

    //   element.style.height = "17x";
    //   element.style.height = element.scrollHeight + "px";
    // },
      byField(direction) {
        function byField(field) {
          if (direction == 'down'){
            return (a, b) => a[field] > b[field] ? 1 : -1
          }
          if (direction == 'up'){
            return (a, b) => a[field] < b[field] ? 1 : -1
          }
        }        
        this.value.parts.part_content.sort(byField('position_number'))
      },
      checkedBox(vals, val){
        var result = false
        vals.filter((v)=>{
          if (v == val) {
            result = true
          } 
        })
        return result
      },
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
        return result
      },
      disablefildUser(fild, id){
        var result
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

              // this.$refs.unfocus.focus()

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
                axios.get('/update_id_in_one_table', {
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
          if(model.selected[obj].indexOf('temp'+(event.oldIndex+1)) >= 1){
            this.$set(model.selected[obj], model.selected[obj].indexOf('temp'+(event.oldIndex+1)), 'temp'+(event.newIndex+1))
            this.box(null, obj, event.oldIndex)
            this.box(model.flavours[obj][(event.newIndex)], obj, (event.newIndex))
          }
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
      // updateWidth() {
      //   this.width = window.innerWidth;
      // },
      // detectWidth(id){
      // var width=this.$refs['table'+id].el
      // console.log(width)
      // },
      sendDataTableHead(id, data){
   
      axios.get('/update_table_data', {
        params: {
          id: id,
          fild: 'description_head',
          data: data
        }
      })

      this.changeDisable('b', 'desk_head', id)
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
               if((v[fild]!=data) || (fild=='done') || (fild=='without') || (fild=='unit')){

                 // console.log(id, fild, data)
                  axios.get('/update_table_data', {
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
      sendDataTablee(id, fild, data){
        // console.log((id, fild, data))
        axios.get('/update_table_data_editor', {
          params: {
            id: id,
            fild: fild,
            data: data
          }
        })
      },
    checkbox_update(event, key, indexSelect){
      // console.log(event)
      if (event != 'column'){
        if (event == null){
              this.value.parts.checkbox_list.selected[key].splice(this.value.parts.checkbox_list.selected[key].indexOf('tepm'+(indexSelect+1)), 1)
        }else{
          this.value.parts.checkbox_list.selected[key]=event
             // this.value.parts.checkbox_list.selected[key].push(event)
        }
      }

      
        if(this.value.parts.checkbox_list.selected!=null){
          axios.post('update_checkbox_table', {
            
              id: this.value.parts.id,
              fild: 'selected',
              data: this.value.parts.checkbox_list.selected
            
          })
        }
      
    },
  //   checkInEditor(e, obj, id){
  //   if ((e.ops[1]!=undefined) && (e.ops[1].insert==' ')){
  //     var result
  //     var sval
  //     var separator
  //     var indexReplace, indexRuslt
  //     var safeEval = require('safe-eval')
  //       if(this.value.parts.part_content[obj].description_work!=(this.cpvalue?this.cpvalue.parts.part_content[obj].description_work:null)){
  //         var tname = 't' + this.tableId + 'x' + obj
  //         if(this.value.parts.part_content[obj].description_work!=null){
  //           if (this.value.parts.part_content[obj].description_work.indexOf(' ') != -1) {
  //             separator = (this.$refs[tname]!=undefined) && (this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getText():''
  //             separator = separator.replace(/\n/g, ' ')
  //             separator = separator.substring(0, separator.length - 1);
  //             separator = separator.split(' ')
  //             separator.splice(-1, 1)
  //             separator.forEach((val) => {
  //               if (val.search(/[a-zA-z=]/gim) == -1) {
  //                 if (val.search(/[-+*)(/]/gim) > -1) {
  //                   if (val.search(/[0-9]/gim) > -1) {
  //                     if (/[\d)]/.test(val[val.length - 1])) {
  //                       try {
  //                         result = this.$options.filters.thousandSeparator(safeEval(val))
  //                       } catch (e) {
  //                         result = '(not valid formula)'
  //                       }
  //                       sval = val.replace(/([-+*)(/])/gim, '$1&shy;') + '=' + result + ' '
  //                       indexRuslt = result.length ? result.length : 4
  //                       indexReplace = this.value.parts.part_content[obj].description_work.indexOf(val) + indexRuslt + 6
  //                       this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
  //                       this.value.parts.part_content[obj].description_work.replace(val, sval)
  //                       )
  //                       this.$refs[tname][0].quill.setSelection(indexReplace, 0)
  //                     }
  //                   }
  //                 }
  //               }
  //             })
  //           }
  //         }
  //       }
  //     this.cpvalue = JSON.parse(JSON.stringify(this.value))
  //     this.sendDataTable(id, 'description_work', this.value.parts.part_content[obj].description_work)
  //    }

  // }
//    checkInEditor(tname, id){
//       var result
//       var sval
//       var separator
//       var safeEval = require('safe-eval')
//       var valueHtml = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getHTML():''

//       if (valueHtml.indexOf('=') != -1) {
//               separator = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getText():''
//               separator = separator.replace(/\n/g, ' ')
//               separator = separator.substring(0, separator.length - 1)
//               separator = separator + ' '
//               separator = separator.split('= ')
//               separator.splice(-1, 1)
//               separator.forEach((val) => {
//               var calcval = val.split(' ')[val.split(' ').length-1]

//                 if (calcval.search(/[a-zA-z=]/gim) == -1) {
//                   if (calcval.search(/[-+*)(/]/gim) > -1) {
//                     if (calcval.search(/[0-9]/gim) > -1) {
//                       if (/[\d)]/.test(calcval[calcval.length - 1])) {
//                          var rcalcval = calcval.split(',').join('.')
//                         try {
//                           result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
//                         } catch (e) {
//                           result = '(not valid formula)'
//                         }
//                         sval = rcalcval+'='+result+' '

//                         this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
//                           valueHtml = valueHtml.replace(calcval+'=', sval)
//                         )
//                       }
//                     }
//                   }
//                 }
//               })
//             }

//      this.sendDataTablee(id, 'description_work', valueHtml)

// },

//  getCaretCharacterOffsetWithin(element) {
//     var caretOffset = 0;
//     var doc = element.ownerDocument || element.document;
//     var win = doc.defaultView || doc.parentWindow;
//     var sel;
//     if (typeof win.getSelection != "undefined") {
//         sel = win.getSelection();
//         if (sel.rangeCount > 0) {
//             var range = win.getSelection().getRangeAt(0);
//             var preCaretRange = range.cloneRange();
//             preCaretRange.selectNodeContents(element);
//             preCaretRange.setEnd(range.endContainer, range.endOffset);
//             caretOffset = preCaretRange.toString().length;
//         }
//     } else if ( (sel = doc.selection) && sel.type != "Control") {
//         var textRange = sel.createRange();
//         var preCaretTextRange = doc.body.createTextRange();
//         preCaretTextRange.moveToElementText(element);
//         preCaretTextRange.setEndPoint("EndToEnd", textRange);
//         caretOffset = preCaretTextRange.text.length;
//     }
//     return caretOffset;
// },

// setCaret(element) {
//     var el = element
//     element.focus()
//     window.getSelection().selectAllChildren(element)
//     window.getSelection().collapseToEnd()
// },
setCaret(element) {
  var el = document.getElementById(element)
  setTimeout(()=>{
    el.focus()
    window.getSelection().selectAllChildren(el)
    window.getSelection().collapseToEnd()
  }, 1);
},
   checkInEditor(value, id){
// var el = document.getElementById('desk_head'+id)
// var cursorPos = this.getCaretCharacterOffsetWithin(el)


      var result
      var sval
      var separator
      var safeEval = require('safe-eval')
      var valueHtml = (value.target.innerText.length!=0)?value.target.innerHTML:''

      if (valueHtml.indexOf('=') != -1) {
              separator = (value.target.innerText.length!=0)?value.target.innerText:''
              separator = separator.replace(/\n/g, ' ')
              separator = separator.substring(0, separator.length - 1)
              separator = separator + ' '
              separator = separator.split('= ')
              separator.splice(-1, 1)
              separator.forEach((val) => {
              var calcval = val.split(' ')[val.split(' ').length-1]

                if (calcval.search(/[a-zA-z=]/gim) == -1) {
                  if (calcval.search(/[-+*)(/]/gim) > -1) {
                    if (calcval.search(/[0-9]/gim) > -1) {
                      if (/[\d)]/.test(calcval[calcval.length - 1])) {
                         var rcalcval = calcval.split(',').join('.')
                        try {
                          result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
                        } catch (e) {
                          result = '(not valid formula)'
                        }
                        sval = rcalcval+'='+result+' '

                        // this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
                        //   valueHtml = valueHtml.replace(calcval+'=', sval)
                        // )
                         valueHtml = valueHtml.replace(calcval+'=', sval)
                      }
                    }
                  }
                }
              })
            }

     return valueHtml
     

},


//    checkInEditor(value, id){
//       var result
//       var sval
//       var separator
//       var safeEval = require('safe-eval')
//       var valueHtml = (value!=undefined)&&(value.length!=0)?value+' ':''
//       if (valueHtml.indexOf('=') != -1) {
//               separator = (value!=undefined)&&(value.length!=0)?value:''
//               separator = separator.replace(/\n/g, ' ')
//               separator = separator.substring(0, separator.length - 1)
//               separator = separator + ' '
//               console.log(separator)
//               separator = separator.split('=&nbsp;')
//               separator.splice(-1, 1)
//               separator.forEach((val) => {
//               var calcval = val.split(' ')[val.split(' ').length-1]
//                 if (calcval.search(/[a-zA-z=]/gim) == -1) {
//                   if (calcval.search(/[-+*)(/]/gim) > -1) {
//                     if (calcval.search(/[0-9]/gim) > -1) {
//                       if (/[\d)]/.test(calcval[calcval.length - 1])) {
//                          var rcalcval = calcval.split(',').join('.')
//                         try {
//                           result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
//                         } catch (e) {
//                           result = '(not valid formula)'
//                         }
//                         sval = rcalcval+'='+result+' '

//                        // console.log(sval)
//                           valueHtml = valueHtml.replace(calcval+'=', sval)
                        
//                       }
//                     }
//                   }
//                 }
//               })
//             }

//             // this.sendDataTable(id, 'description_head', valueHtml);
//             return valueHtml
//             // return valueHtml
//       // this.sendDataTable(id, 'description_head', valueHtml)
//      // this.sendDataTablee(id, 'description_head', valueHtml)

// },
  addtable(tname, id){
    var valueHtml = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname][0].quill.getHTML():''
      this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(
        valueHtml = valueHtml +'<p><span style="border:1px solid black;">1</span><span style="border:1px solid black;">1</span><span style="border:1px solid black;">1</span></p>'
      )

      this.sendDataTablee(id, 'description_work', valueHtml)
  }

  },
  mounted(){
    // window.addEventListener('resize', this.updateWidth);
    // this.updateWidth();
    this.scheckStatus();
  }

}
</script>