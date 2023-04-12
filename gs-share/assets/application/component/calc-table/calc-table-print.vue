<template>
  <div style="border-bottom: 1px solid #bbb8b8;"><slot name="tableHead" :tableId="tableId"></slot>
            <div :class="{ 'table-dark': toggle }">
           
               <draggable v-model="value.parts.part_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
                  :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)">
                  <div v-for="(content, subIndex) in value.parts.part_content" :class="colorIdent(value.parts.part_name, subIndex)">
                     <b-form-row :key="content.id" >
                        <div class="tnumber text-center" :class="(content.unit=='%') ? '' : 'handle'">
                                  {{(subIndex+1)}} 
                        </div>
                        <div  class="tposition text-center"  style="font-weight: normal;" >
                           <!-- <b-input @click.prevent.self type="text" placeholder="Unit" :style="(content.done!=false) ? 'color:green' : ''"
                              class="cForm-input cinput" v-model="content.position_number" /> -->
                              {{content.position_number}}
                        </div>
                        <div contenteditable="true" class="tdeschead text-left"  style="font-weight: normal;"  :style="'width:'+computedWithDesc(value.parts.checkbox_list.flavours)+'%'">
                           <!-- <b-input  @click.prevent.self type="text" placeholder="Description Head" class="cForm-input"
                           :style="(content.done!=false) ? 'color:green' : ''" v-model="content.description_head" /> -->
                           {{content.description_head}} {{(content.unit=='%') ? 'for rows No.: '+forPosition(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content): '' }} 
                        </div>
            <!--             <div  class="tinfo text-center">
                           <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'desk_worck'+tableId+subIndex">
                              <span class="when-opened" :style="'color:'+computedStylePlus(content.description_work)">-</span>
                              <span class="when-closed" :style="'color:'+computedStylePlus(content.description_work)">+</span>
                           </b-link>
                        </div> -->
                        <div  class="tcount text-center"  style="font-weight: normal;" >
                          <!--  <b-input @click.prevent.self type="number"
                           placeholder="Count" class="cForm-input ainput" :style="(content.done!=false) ? 'color:green' : ''" v-model="content.count" /> -->
                           {{content.count}}
                        </div>
                        <div  class="tunit text-center" style="font-weight: normal;" >
                           <!-- <b-select v-model="content.unit" @input="persent(content.unit, subIndex, value.parts.checkbox_list, value.parts.part_content.length)"
                             class="select" style="min-width:45px" :style="(content.done!=false) ? 'color:green' : ''">
                              <option v-for="opt in unit_type" :disabled="disOptPercent(value.parts.part_content, opt)">
                                 {{opt}} 
                              </option>
                           </b-select> -->
                           {{content.unit}}
                        </div>
                        <div class="tprice text-right" style="font-weight: normal;" v-if="prices">
                           <!-- <input v-if="content.unit!='%'" @click.prevent.self type="number"
                             placeholder="Price" class="cForm-input form-control rinput"
                             v-model="content.price" :style="(content.done!=false) ? 'color:green' : ''" /> -->
                          <div v-if="content.unit!='%'" >
                             {{content.price}}
                           </div>
                           <div v-else>
                              {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                value.parts.checkbox_list.selected, value.parts.part_content, 'summ')}}
                            </div>
                        </div>
                        <div  class="tsumm text-right " style="font-weight: normal;" v-if="addtaxColapse==true && prices">
                           <div :style="content.status=='yes' ? '' : 'color:grey'" 
                              :class="{ 'calttax': content.alttax }"
                              @click="content.alttax = content.alttax ? false : true">
                              <div v-if="content.unit!='%'" :title="content.count * content.price | thousandSeparator">
                                  {{content.count * content.price | thousandSeparator}}
                              </div>
                              <div v-else class="text-right"  style="font-weight: normal;" 
                              :title="persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                              value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator">
                                  {{persent_to_str(subIndex, value.parts.checkbox_list.allSelected,
                                    value.parts.checkbox_list.selected, value.parts.part_content, '%') | thousandSeparator}}
                              </div>
                           </div>
                        </div>
                        <div v-else-if="prices"  class="tsumm text-right" style="font-weight: normal;" >
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
                      <!--   <div class="custom-control-inline tpercent">
                           <div  v-for="(select_from_allSelected, key) in value.parts.checkbox_list.allSelected" >
                              <div v-for="(opt, indexSelect) in value.parts.checkbox_list.flavours[key]" v-if="indexSelect==subIndex" class="ccbox"
                               :class="classRow(value.parts, key)" :style="(content.done!=false) ? 'color:green' : ''">
                                 <b-form-checkbox type="checkbox" plain
                                    :disabled="boxDisable(content.unit, key, indexSelect)"
                                    v-model="value.parts.checkbox_list.selected[key]"
                                    :value="opt" 
                                    class="withoutPad"
                                    @change="box($event, key, indexSelect)" />
                              </div>
                           </div>
                        </div> 
                        <div class="twithout text-center ccbox"  v-if="butDiscPerc=='%'">
                           <b-form-checkbox class="withoutPad"  plain style="margin: 0px;" v-model="content.without" :style="(content.done!=false) ? 'color:green' : ''" />
                        </div>
                        <div class="tcalc text-center">
                           <b-form-select class="select" style="min-width:45px" :options="calc" v-model="content.status" :style="(content.done!=false) ? 'color:green' : ''" />
                        </div> -->
                        <!-- <div class="tdone text-center ccbox">
                           <b-form-checkbox class="withoutPad" v-if="selectedWorkers.length!=0 || content.done!=false" plain style="margin: 0px;"
                           :disabled="selectedWorkers.length==0 && content.done==false" :checked="content.done!=false"
                           :style="(content.done!=false) ? 'color:green' : ''" :title="content.done" @change="changeWorker($event, subIndex)"
                           />
                        </div>
                        <div class="tdelete text-center">
                           <b-link @click="subPartDel(subIndex);" class="fas fa-trash fa-w-16" />
                        </div> -->
                        <div class="text-left">{{content.without?"*":""}}</div>
                     </b-form-row>
                     
                         <div v-if="comments" class="tdeschead text-left" contenteditable="true" :style="'width:'+(computedWithDesc(value.parts.checkbox_list.flavours)+13)+'%'"
                          style="font-weight: normal;padding-left:12%" v-html="content.description_work" />
                          

                           <!--    <vue-editor
                                 :id="('t'+tableId + 'x' + subIndex)"
                                 :ref="('t'+tableId + 'x' + subIndex)"
                                 v-model="content.description_work"
                                 :value="content.description_work" >
                              </vue-editor>
                              <b-link v-b-toggle="'desk_worckI'+tableId+subIndex" class="butMore"  v-if="content.description_from_price.length>0">
                                 <span class="when-opened" >-</span>
                                 <span class="when-closed">+</span>
                              </b-link> -->
                          <!--     <b-collapse style="width:100%;font-size: 12px;" :id="'desk_worckI'+tableId+subIndex"
                              v-if="content.description_from_price.length>0">
                                 {{content.description_from_price}}
                              </b-collapse>
                           -->
                       
                     
                  </div>
               </draggable>
            </div>
            <b-row class="ttotalsumm" v-if="prices">
               <b-col align-self="end" class="text-right" >
               Summ  {{value.parts.part_name}}: {{ total(value.parts.part_content) | thousandSeparator }}</b-col>
            </b-row>
            <span style="color:grey" v-if="prices">
               <b-row class="ttotalsumm" v-if="alttotal(value.parts.part_content)!=0">
                  <b-col align-self="end" class="text-right" >
                  Summ Alternative {{value.parts.part_name}}: {{ alttotal(value.parts.part_content) | thousandSeparator}}</b-col>
               </b-row>
            </span>
  </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
import {VueEditor, Quill} from 'vue2-editor';
export default {
    components: {
        draggable,
        VueEditor
    },
    props: ['value', 'addtaxColapse', 'color', 'selectedWorkers', 'toggle', 'tableId', 'comments', 'prices'],
    data() {
        return {
            unit_type: ['Psch.', '%', 'Stück.', 'Sack.'],
            calc: ['yes', 'no', 'etc', 'alternative'],
            butDiscPerc: '%',
            disable: []
        } //return
    }, //data
    computed: {
        computedStylePlus: function() {
            var vm = this;
            return function(val) {

                if (val.length > 0) {
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
              var w = this.prices ? 57.6 : 74.6 
                var count = 0;
                for (var obj in val) {
                    if (count == 0) {
                        w = w + 0.6
                    }
                    if (count >= 2) {
                        w = w - 1.7
                    }
                    w = w - 0.6
                    count++
                }
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
        },
        forPosition: function(){
             var vm = this;
            return function(subIndex, all_obj, selected, content) {
                var list = ''
                for (var obj in all_obj) {
                    if (selected[obj].indexOf('temp' + (subIndex + 1)) != -1) {
                        selected[obj].forEach(function(val, index) {
                            if (val != 'temp' + (subIndex + 1)) {
                                val = val.split('temp')
                                list +=  ' '+val[1]+','
                            }
                        })
                    }
                }

                    if (list != ''){
                      return list.replace(/.$/,".")
                    } else{
                     return 'no selected items'
                    }
            }
        }
    },
    methods: {
    checkMove(event, model){
        var obj
        for (obj in model.selected) {
          if(event.from!=event.to){
            model.selected[obj].splice(model.selected[obj].indexOf('temp'+(event.oldIndex+1)), 1)
            this.box(null, obj, event.oldIndex)
          } else{
          if(model.selected[obj].indexOf('temp'+(event.oldIndex+1)) >= 1){
            this.$set(model.selected[obj], model.selected[obj].indexOf('temp'+(event.oldIndex+1)), 'temp'+(event.newIndex+1))
            this.box(null, obj, event.oldIndex)
            this.box(model.flavours[obj][(event.newIndex)], obj, (event.newIndex))
          }
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
                this.disable.forEach(function(val) {
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
                        this.disable.forEach(function(dval) {
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
                                this.disable.forEach(function(dval1) {
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
        },
        box(event, obj, str) {
            if (event != null) {
                this.disable.push(obj + '-' + str)
            } else {
                this.disable.splice(this.disable.indexOf(obj + '-' + str), 1)
            }
            this.scheckStatus()
        },
        subPartDel(subDel_id) {
            if (confirm("Are you sure?")) {
                    this.value.parts.part_content.splice(subDel_id, 1);
                    for (var property in this.value.parts.checkbox_list.flavours) {
                        this.value.parts.checkbox_list.selected[property].splice(valuePart.parts.checkbox_list.selected[property]
                          .indexOf(this.value.parts.checkbox_list.flavours[property][subDel_id]), 1)
                        this.value.parts.checkbox_list.flavours[property].splice(subDel_id, 1)
                    }
                }
        },
        persent(val, index, checkbox_in_table, how_many_rows) {
            this.persentCounter = val
            if (val == '%') {
                 this.add_column_checkbox(checkbox_in_table, how_many_rows)
                 var obj = Object.keys(checkbox_in_table.flavours)[Object.keys(checkbox_in_table.flavours).length - 1]
                 checkbox_in_table.selected[obj].push(checkbox_in_table.flavours[obj][index])
            } else {
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
            this.scheckStatus()
        },
        toggleAll(event, target, model, persent) {
            model.allSelected[target] = event
            if (model.allSelected[target]) {
                var obj
                model.flavours[target].forEach((val, index) => {
                    if (persent[index].unit != '%') {
                        var count = 0
                        for (obj in model.allSelected) {
                            if (model.flavours[target][index] == model.selected[obj][model.selected[obj].indexOf(model.flavours[target][index])]) count++
                        }
                        if (count == 0) {
                            model.selected[target].push(model.flavours[target][index])
                            this.box(model.flavours[target][index], target, index)
                        }
                    }
                })
            } else {
                var obj
                model.flavours[target].forEach((val, index) => {
                    if (persent[index].unit != '%') {
                        if (model.selected[target].indexOf(model.flavours[target][index]) != -1) {
                            model.selected[target].splice(model.selected[target].indexOf(model.flavours[target][index]), 1)
                            this.box(null, target, index)
                        }
                    }
                })
            }
        },
        changeWorker(event, index){
          if(event==false){
              this.value.parts.part_content[index].done=false
          } else{
            this.value.parts.part_content[index].done=this.selectedWorkers
          }
        },
        toggleAllWorkers(event){
          if(event==false){
              this.value.parts.part_content.forEach(function(val){
                val.done=false
              })
          } else{
            this.value.parts.part_content.forEach((val)=>{
                val.done=this.selectedWorkers
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
      }
    },
    watch: {
        part: {
            handler: function(newVal) {
                var result
                var sval
                var separator
                var indexReplace, indexRuslt
                var safeEval = require('safe-eval')
                for (var obj in this.value.parts.part_content) {
                    var tname = 't' + this.tableId + 'x' + obj
                    if (this.value.parts.part_content[obj].description_work.indexOf(' ') != -1) {
                        separator = this.$refs[tname][0].quill.getText()
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
                                            this.value.parts.part_content[obj].description_work.replace(val, sval))
                                            this.$refs[tname][0].quill.setSelection(indexReplace, 0)
                                        }
                                    }
                                }
                            }
                        })
                    }
                }
            },
            deep: true,
        }
    }
}
</script>