<template>
  <b-container>
    <b-row align-v="center">
      <b-link style="text-decoration: none" @click="toog(table.id)">
        <div
          :id="'p'+table.id"
          style="display: none; vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-down" font-scale="1" />
        </div>
        <div :id="'m'+table.id" style="vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-up" font-scale="1" />
        </div>
      </b-link>
      <b-form-checkbox
        plain
        @change="$emit('seltable', table.id, $event)"
        v-model="tablechecked" />
      <div :id="'s'+table.id" style="display: none;">
        <span v-show="table.summa!='0,00'" align-self="end" class="text-right">{{$t('projectDetail.total')}} {{table.summa}} €</span>
        <span v-show="table.alt_summa!='0,00'" align-self="end" class="text-right" > {{$t('projectDetail.totalAlternative')}} {{table.alt_summa}} €</span>
        &nbsp;|&nbsp;
      </div>
      <div
        contenteditable
        class="diveditable"
        @click.prevent.self
        @blur="tableRename($event.target.innerText, table.id, table.name)"
        v-html="table.name"></div>
      <b-icon
        icon="trash"
        aria-hidden="true"
        @click="$emit('tableDelete', table.id, item_id)"
        style="cursor: pointer" />
    </b-row>
    <div :id="'table'+table.id">
      <b-table-simple small borderless responsive class="editTable">
        <b-thead>
          <b-tr>
            <b-th style="width:40px;text-align:left;text-wrap: nowrap;">
              #
              <b-link>
                <b-icon
                  icon="arrow-bar-right"
                  aria-hidden="true"
                  @click.stop="showPos=showPos?false:true"
                  v-show="!showPos" />
              </b-link>
            </b-th>
            <b-th v-show="showPos" style="min-width: 70px">
              <b-link>
                <b-icon
                  icon="arrow-bar-left"
                  aria-hidden="true"
                  @click.stop="showPos=showPos?false:true" />
              </b-link>
              <b-link disabled @click.stop="sort=(sort=='down')?'up':'down';byField(sort)">
                <b-icon
                  :icon="'sort-numeric-'+sort"
                  aria-hidden="true"
                  class="ml-3"
                />
              </b-link>
            </b-th>
            <b-th style="white-space: nowrap;overflow: hidden;">
              {{$t('calcTable.description')}}
            </b-th>
            <b-th>
              =
            </b-th>
            <b-th>
              {{$t('calcTable.unit')}}
            </b-th>
            <b-th>€</b-th>
            <b-th>∑</b-th>
            <b-th
              :style="(inPercent<(unitPercent.length-1))?'border-right: 1px solid; border-color: #dddddd;text-align:left':''"
              v-if="unitPercent.length>0"
              v-for="(partPercent, inPercent) in unitPercent"
              :key="partPercent">
              <b-form-checkbox
                plain
                disabled
                class="ccbox"
                style="color: gray; padding-left: 0">&nbsp;</b-form-checkbox>
            </b-th>
            <b-th v-if="(butDiscPerc=='%')&&(discP>0)">
              -{{discP}}<b-icon icon="percent" aria-hidden="true" />
            </b-th>
            <b-th><b-icon icon="calculator" aria-hidden="true" /></b-th>
            <b-th>
              <b-form-checkbox
                plain
                disabled
                v-show="this.selectedWorkers.length>0"
                class="ccbox"
                style="color: gray"
                >&nbsp;</b-form-checkbox>
            </b-th>
            <b-th style="text-align:right;">X</b-th>
          </b-tr>
        </b-thead>
        <b-tbody>
          <b-tr
            :key="content.id"
            v-for="(content, index) in rows"
            :variant="(content.status!='yes')?'dark':((content.done!=false)&&(content.done!=''))?'success':''">
            <b-td>
              {{(index+1)}}
            </b-td>
            <b-td v-show="showPos">
              <div
                contenteditable
                class="diveditable"
                @click.prevent.self
                @blur="sendDataTable(content.id, 'position_number', $event.target.innerText, index, content.position_number);"
                :id="'position_number'+content.id"
                v-html="content.position_number" />
            </b-td>
            <b-td style="width:100%;" :title="(content.description_work&&content.description_work!=0)?content.description_work:'(You have not added an explanation for this item)'">
              <div
                contenteditable="plaintext-only"
                style="width: 100%; padding-left: 4px"
                @click.prevent.self
                @keyup.space="($event.target.innerHTML.indexOf('= ') != -1 )?(content.description_head = checkInEditor($event, content.id)):null"
                @blur="sendDataTable(content.id, 'description_head', $event.target.innerHTML, index, content.description_head)"
                :id="'description_head'+content.id"
                v-html="description(content.description_head)" />
            </b-td>
            <b-td>
              <div
                contenteditable
                class="diveditable text-right"
                @click.prevent.stop="selectAll('count'+content.id)"
                @blur="forSumm(content.id, 'count', $event.target.innerText, index, content.count, item_id)"
                :id="'count'+content.id"
                v-html="content.count" />
            </b-td>
            <b-td>
              <b-dropdown
                size="sm"
                :text="content.unit"
                variant="link"
                no-caret
                class="maxHeight outUnderline">
                <b-dropdown-item-button
                  :key="opt"
                  v-for="opt in unitType"
                  @click="chenge_unit_type(content.id, opt, index, content.unit, item_id);">
                  {{opt}}
                </b-dropdown-item-button>
              </b-dropdown>
            </b-td>
            <b-td>
              <div
                :contenteditable="(content.unit!='%')"
                class="diveditable"
                @click.prevent.stop="selectAll('price'+content.id)"
                @blur="forSumm(content.id, 'price', $event.target.innerText, index, content.price, item_id)"
                :id="'price'+content.id"
                v-html="content.price" />
            </b-td>
            <b-td
              :style="(addtaxColapse?'cursor:pointer;':'')"
              :title="content.summa"
              @click="(addtaxColapse)?chengeTax(content.id, (content.alttax=='true')?'':'true', index, content.alttax, item_id):''">
              {{content.summa}}<sub v-if="addtaxColapse">&nbsp;<b>{{content.alttax?2:1}}</b></sub>
            </b-td>
            <b-td
              :style="(inPercent<(unitPercent.length-1))?'border-right: 1px solid; border-color: #dddddd;':''"
              v-if="unitPercent.length>0"
              v-for="(partPercent, inPercent) in unitPercent"
              :key="partPercent">
              <div v-if="(partPercent.split('in')[1]==content.id)&&(content.unit=='%')">
                <b-icon icon="check-circle-fill" aria-hidden="true"></b-icon>
              </div>
              <b-form-checkbox
                plain
                v-if="(partPercent.split('in')[1]!=content.id)&&(content.unit!='%')"
                class="ccbox"
                style="padding-left:0;"
                :checked="content.checked_for_percent==partPercent"
                @change="checked_for_percent(content.id, partPercent, $event, index, content.checked_for_percent, item_id)"
                >&nbsp;</b-form-checkbox>
            </b-td>
            <b-td
              v-if="(butDiscPerc=='%')&&(discP>0)"
              >
              <b-form-checkbox
                
                @change="sendDiscont(content.id, $event?'false':'true', index, content.without, item_id)"
                plain
                :checked="(content.without=='true')?false:true"
                class="ccbox"
                >&nbsp;</b-form-checkbox>

            </b-td>
            <b-td >
              <b-dropdown
                size="sm"
                variant="link"
                no-caret
                class="outUnderline"
                :text="$t('calcTableGroup.'+content.status+'.short')"
                >
                <b-dropdown-item-button
                  @click="sendModeCalc(content.id, 'yes', index, content.status, item_id)"
                  >{{$t('calcTableGroup.yes.long')}}</b-dropdown-item-button>
                <b-dropdown-item-button
                  @click="sendModeCalc(content.id, 'no', index, content.status, item_id)"
                  >{{$t('calcTableGroup.no.long')}}</b-dropdown-item-button>
                <b-dropdown-item-button
                  @click="sendModeCalc(content.id, 'etc', index, content.status, item_id)"
                  >{{$t('calcTableGroup.etc.long')}}</b-dropdown-item-button>
                <b-dropdown-item-button
                  @click="sendModeCalc(content.id, 'alternative', index, content.status, item_id)"
                  >{{$t('calcTableGroup.alternative.long')}}</b-dropdown-item-button>
              </b-dropdown>
            </b-td>
            <b-td  :title="content.done">
              <b-form-checkbox
                v-if="selectedWorkers.length!=0 || content.done!=false"
                plain
                class="ccbox"
                :checked="((content.done!='')&&(content.done!=false))"
                @change="workersToDone(content.id, $event, index, content.done)"
                >&nbsp;</b-form-checkbox>
            </b-td>
            <b-td >
              <b-icon
                icon="trash"
                aria-hidden="true"
                @click="rowDel(content.id, index, item_id);"
                style="cursor: pointer" />
            </b-td>
          </b-tr>
        </b-tbody>
      </b-table-simple>
      <b-row v-show="table.discont!='0,00'">
        <b-col align-self="end" class="text-right" style="margin-right: 22.6%">
          {{$t('edit.discont')}} {{table.discont}} € </b-col>
      </b-row>
      <b-row v-show="table.summa!='0,00'">
        <b-col align-self="end" class="text-right" style="margin-right: 22.6%;">
          {{$t('projectDetail.total')}} {{table.summa}} €</b-col>
      </b-row>
      <b-row v-show="table.alt_summa!='0,00'">
        <b-col align-self="end" class="text-right" style="margin-right: 22.6%;color:grey">
          {{$t('projectDetail.totalAlternative')}} {{table.alt_summa}} €</b-col>
      </b-row>
      <br>
      <div class="text-center" v-show="rowsBusy">
        <strong v-if="rowsLoading" class="text-info">
          <b-spinner class="align-middle"></b-spinner>
          {{$t('projects.loading')}}...
        </strong>
        <div v-else class="text-center">{{$t('projects.empty')}}</div>
      </div>
    </div>
    <hr style="padding: 0; margin: 5px; display: none" :id="'hr'+table.id" />
  </b-container>
</template>
<script type = "text/javascript">
import axios from 'axios';
export default {
   props: ['checkbox_list', 'selectedWorkers', 'addtaxColapse', 'butDiscPerc', 'discP', 'unitType', 'item_id', 'table', 'unitPercent'],
   data() {
      return {
        //  unitPercent:[],
         tablechecked: false,
         rows: [],
         rowsBusy: true,
         rowsLoading: true,
         rowBusy: true,
         rowLoading: true,
         sort: 'down',
         showPos: true,
      }
   },
   methods: {
      getRowsInTable(id) {
         axios.get('/get_rows_in_table', {
            params: {
               id: id
            }
         }).then(response => {
            this.rows = response.data;
            this.rowsLoading = false;
            this.rowsBusy = (response.data.length > 0) ? false : true;
            this.tablechecked = false;
         })
      },
      getFild(updateFild) {
        this.rows[updateFild.index][updateFild.fild] = updateFild.value;
      },
      update_part_parametrs(update){
        if (this.table.id == update.table_id){
          this.table.summa = update.toSumm
          this.table.alt_summa = update.altSumm
          this.table.discont = update.toDiscont
        }
      },
      toog(val) {
         document.getElementById('m' + val).style.display = document.getElementById('table' + val).style.display = (document.getElementById('table' + val).style.display == 'none') ? '' : 'none'
         document.getElementById('s' + val).style.display = document.getElementById('p' + val).style.display = (document.getElementById('m' + val).style.display == 'none') ? '' : 'none'
         document.getElementById('hr' + val).style.display = (document.getElementById('m' + val).style.display == 'none') ? '' : 'none'
      },
      byField(direction) {
        function byField(field) {
          if (direction == 'down'){
            return (a, b) => a[field] > b[field] ? 1 : -1
          }
          if (direction == 'up'){
            return (a, b) => a[field] < b[field] ? 1 : -1
          }
        }        
        this.rows.sort(byField('position_number'))
      },
      chenge_unit_type(id, opt, index, old, item_id) {
         if (old != opt) {
            if (((old == '%')&&(opt != '%'))||((old != '%')&&(opt == '%'))) {
              this.$emit('chengeCountPresents', this.unitPercent, (opt == '%'), id, this.table.id);
              axios.get('/chenge_unit_type', {
                params: {
                    table_id: this.table.id,
                    id: id,
                    data: opt,
                    index: index,
                    item_id : item_id
                }
              })
            }
            else{
              this.sendDataTable(id, 'unit', opt, index, old);
            }
         }
      },
      checked_for_percent(id, partPercent, event, index, old, item_id) {
        axios.get('/checked_for_percent', {
                params: {
                    table_id: this.table.id,
                    id: id,
                    event: event,
                    index: index,
                    part_percent:partPercent,
                    old: (old==null)?'null':old,
                    item_id : item_id
                }
              })
      },
      forSumm(id, fild, data, index, old, item_id) {
         if (old != data) {
            axios.get('/update_for_summ', {
               params: {
                  table_id: this.table.id,
                  id: id,
                  fild: fild,
                  data: data,
                  index: index,
                  item_id : item_id
               }
            });
         }
      },
      sendDiscont(id, data, index, old, item_id) {
         if (old != data) {
            axios.get('/send_discont', {
               params: {
                  table_id: this.table.id,
                  id: id,
                  data: data,
                  index: index,
                  item_id : item_id
               }
            });
         }
      },
      sendModeCalc(id, data, index, old, item_id) {
         if (old != data) {
            axios.get('/send_mode_calc', {
               params: {
                  table_id: this.table.id,
                  id: id,
                  data: data,
                  index: index,
                  item_id : item_id
               }
            });
         }
      },
      chengeTax(id, data, index, old, item_id){
        if (old != data) {
              axios.get('/chenge_tax', {
                params: {
                    table_id: this.table.id,
                    id: id,
                    data: data,
                    index: index,
                    item_id : item_id
                }
              });
        }
      },
      sendDataTable(id, fild, data, index, old) {
         if (old != data) {
            axios.get('/update_table_data', {
               params: {
                  table_id: this.table.id,
                  id: id,
                  fild: fild,
                  data: data,
                  index: index
               }
            });
         }
      },
      tableRename(newVal, id, partName) {
            if(newVal!= partName){
                axios.get('/update_part', {
                  params: {
                    part_name: newVal,
                    id: id
                  }
                })
            }
        },
      workersToDone(id, event, index, old) {
         if (event == false) {
            if (confirm("Are you sure?")) {
               this.sendDataTable(id, 'done', '', index, old)
            }
         }
         if (event == true) {
            this.sendDataTable(id, 'done', this.selectedWorkers.join("\n"), index, old)
         }
      },
      selectAll(id) {
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
      rowDel(id, index, item_id) {
         if (confirm("Are you sure?")) {
            axios.get('/del_row_from_table', {
               params: {
                  table_id: this.table.id,
                  index: index,
                  id: id,
                  item_id : item_id
               }
            })
         }
      },
      description(val) {
         if (val != null) {
            return val
         }
         if (val == null) {
            return '(Not have a data)'
         }
      },
      checkInEditor(value, id) {
         var result
         var sval
         var separator
         var safeEval = require('safe-eval')
         var valueHtml = (value.target.innerText.length != 0) ? value.target.innerHTML : ''
         if (valueHtml.indexOf('=') != -1) {
            separator = (value.target.innerText.length != 0) ? value.target.innerText : ''
            separator = separator.replace(/\n/g, ' ')
            separator = separator.substring(0, separator.length - 1)
            separator = separator + ' '
            separator = separator.split('= ')
            separator.splice(-1, 1)
            separator.forEach((val) => {
               var calcval = val.split(' ')[val.split(' ').length - 1]
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
                           sval = rcalcval + '=' + result + ' '
                           valueHtml = valueHtml.replace(calcval + '=', sval)
                        }
                     }
                  }
               }
            })
         }
         return valueHtml
      },
   },
   mounted() {
    // unitPercent=((this.table.obj!='')&&(this.table.obj!=null))?this.table.obj.split(','):[];
    this.getRowsInTable(this.table.id);
   }
}
</script>