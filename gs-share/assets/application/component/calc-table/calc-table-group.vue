
<template>
   <draggable v-model="partx" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
     :no-transition-on-drag="true" @start="drag=true" @end="drag=false"><div>{{partx}}</div>
      <div style="width:100%" v-for="(part, index) in partx" :key="part.id">
         <b-form-checkbox style="width:100%" plain name="partx" class="withoutbox handleTitle"
            :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }"
            :value="part.parts.part_name+index"  @change="toggleItem(part.parts.part_name+index)">
            <b-link v-b-toggle="'partx' + index" class="butMore" style="width:100%">
               <span class="when-opened">-</span>
               <span class="when-closed">+ {{ thousandSeparator(total(part.parts.part_content)) }} €</span>
            </b-link>
            <i class="fas fa-dot-circle" style="font-size:12px"></i> 
            <span contenteditable="true" @input="toModel($event, index)" @click.prevent.self>{{part.parts.part_name}}</span>
            <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(part.parts.part_name+index);discOfPercent()"/>
         </b-form-checkbox>
         <b-collapse :id="'partx'+index">
            <div :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }">
               <div>
                  <b-form-row>
                     <div class="tnumber text-center">#</div>
                     <div class="tposition text-center">Position</div>
                     <div class="tdeschead text-center" :style="'width:'+computedWithDesc(part.parts.checkbox_list.flavours)+'%'">Description Head</div>
                     <div class="tinfo text-center"><i class="fas fa-info" style="font-size:10px;width:10px;padding:0px;"></i></div>
                     <div class="tcount text-center">=</div>
                     <div class="tunit text-center">Unit</div>
                     <div class="tprice text-center">€</div>
                     <div class="tsumm text-center">∑</div>
                     <div class="custom-control-inline tpercent">
                        <div  v-for="(select_from_allSelected, key) in part.parts.checkbox_list.allSelected" class="ccbox" :class="classRow(part.parts, key)">
                           <b-form-checkbox plain
                              v-model="part.parts.checkbox_list.allSelected[key]"
                              @change="toggleAll($event, key, part.parts.checkbox_list, part.parts.part_content)"
                              class="withoutPad"
                              />
                        </div>
                     </div>
                     <div class="twithout text-center"  v-if="butDiscPerc=='%'">-%</div>
                     <div class="tcalc text-center">Calculation</div>
                     <div class="tdelete text-center">X</div>
                  </b-form-row>
               </div>
               <draggable v-model="part.parts.part_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
                  :no-transition-on-drag="true" @start="drag=true" @end="drag=false">
                  <div v-for="(content, subIndex) in part.parts.part_content" :class="colorIdent(part.parts.part_name, subIndex)">
                     <b-form-row style="height:20px;" @mouseover="content.upHere = true" @mouseleave="content.upHere = false" 
                       :class="{howerRow: content.upHere, '': !content.upHere}" :key="content.id" >
                        <div class="tnumber text-center" :class="(content.unit=='%') ? '' : 'handle'" style="font-weight: normal;" 
                          @click="content.upHere = false; selectRow(part.parts.part_name, subIndex)">
                                  {{(subIndex+1)}}
                        </div>
                        <div  class="tposition text-center">
                           <b-input @click.prevent.self type="text" placeholder="Unit"
                              class="cForm-input cinput" v-model="content.position_number" />
                        </div>
                        <div class="tdeschead text-center" :style="'width:'+computedWithDesc(part.parts.checkbox_list.flavours)+'%'">
                           <b-input  @click.prevent.self type="text" placeholder="Description Head" class="cForm-input"
                              v-model="content.description_head" />
                        </div>
                        <div  class="tinfo text-center">
                           <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'desk_worck'+index+subIndex">
                              <span class="when-opened" :style="'color:'+computedStylePlus(content.description_work)">-</span>
                              <span class="when-closed" :style="'color:'+computedStylePlus(content.description_work)">+</span>
                           </b-link>
                        </div>
                        <div  class="tcount text-center">
                           <b-input @click.prevent.self @input="discOfPercent" type="number"
                           placeholder="Count" class="cForm-input ainput" v-model="content.count" />
                        </div>
                        <div  class="tunit text-center">
                           <b-select v-model="content.unit" @input="persent(content.unit, subIndex, part.parts.checkbox_list, part.parts.part_content.length)"
                             class="select" style="min-width:45px">
                              <option v-for="opt in unit_type" :disabled="disOptPercent(part.parts.part_content, opt)">
                                 {{opt}} 
                              </option>
                           </b-select>
                        </div>
                        <div class="tprice text-right" style="font-weight: normal;">
                           <input v-if="content.unit!='%'" @click.prevent.self @input="discOfPercent" type="number"
                             placeholder="Price" class="cForm-input form-control rinput"
                             v-model="content.price"/>
                           <div v-else>
                              {{persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, 'summ')}}
                            </div>
                        </div>
                        <div  class="tsumm text-right " style="font-weight: normal;" v-if="addtaxColapse==true">
                           <div :style="content.status=='yes' ? '' : 'color:grey'"
                              :class="{ 'calttax': alttax[subIndex] }"
                              @click="alttax[subIndex] = alttax[subIndex] ? false : true; discOfPercent()">
                              <div v-if="content.unit!='%'" :title="thousandSeparator(content.count * content.price)">
                                  {{thousandSeparator(content.count * content.price)}}
                              </div>
                              <div v-else class="text-right" :title="thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))">
                                  {{thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))}}
                              </div>
                           </div>
                        </div>
                        <div v-else  class="tsumm text-right" style="font-weight: normal;" >
                           <div :style="content.status=='yes' ? '' : 'color:grey'">
                              <div v-if="content.unit!='%'" :title="thousandSeparator(content.count * content.price)">
                                  {{thousandSeparator(content.count * content.price)}}
                              </div>
                              <div v-else :title="thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))">
                                  {{thousandSeparator(persent_to_str(subIndex, part.parts.checkbox_list.allSelected, part.parts.checkbox_list.selected, part.parts.part_content, '%'))}}
                              </div>
                           </div>
                        </div>
                        <div class="custom-control-inline tpercent">
                           <div  v-for="(select_from_allSelected, key) in part.parts.checkbox_list.allSelected" >
                              <div v-for="(opt, indexSelect) in part.parts.checkbox_list.flavours[key]" v-if="indexSelect==subIndex" class="ccbox"
                               :class="classRow(part.parts, key)">
                                 <b-form-checkbox type="checkbox" plain
                                    :disabled="boxDisable(content.unit, key, indexSelect)"
                                    v-model="part.parts.checkbox_list.selected[key]"
                                    :value="opt" 
                                    class="withoutPad"
                                    @change="box($event, key, indexSelect)" />
                              </div>
                           </div>
                        </div>
                        <div class="twithout text-center ccbox"  v-if="butDiscPerc=='%'">
                           <b-form-checkbox class="withoutPad"  @input="discOfPercent" plain style="margin: 0px;" v-model="content.without"/>
                        </div>
                        <div class="tcalc text-center">
                           <b-form-select @input="discOfPercent" class="select" style="min-width:45px" :options="calc" v-model="content.status" />
                        </div>
                        <div class="tdelete text-center">
                           <b-link @click="subPartDel(part.parts.part_name+index, subIndex);discOfPercent()" class="fas fa-trash fa-w-16" />
                        </div>
                     </b-form-row>
                     <b-form-row >
                        <b-col cols="12" @click.prevent.self style="width:10%">
                           <b-collapse style="width:100%" :id="'desk_worck'+index+subIndex">
                              <vue-editor
                                 :id="('t'+index + 'x' + subIndex)"
                                 :ref="('t'+index + 'x' + subIndex)"
                                 v-model="content.description_work"
                                 :value="content.description_work" >
                              </vue-editor>
                              <b-link v-b-toggle="'desk_worckI'+index+subIndex" class="butMore"  v-if="content.description_from_price.length>0">
                                 <span class="when-opened" >-</span>
                                 <span class="when-closed">+</span>
                              </b-link>
                              <b-collapse style="width:100%;font-size: 12px;" :id="'desk_worckI'+index+subIndex" v-if="content.description_from_price.length>0">
                                 {{content.description_from_price}}
                              </b-collapse>
                           </b-collapse>
                        </b-col>
                     </b-form-row>
                  </div>
               </draggable>
            </div>
            <b-row class="ttotalsumm">
               <b-col align-self="end" class="text-right" style="margin-right:20.4%">General {{ thousandSeparator(total(part.parts.part_content)) }}</b-col>
            </b-row>
            <span style="color:grey">
               <b-row class="ttotalsumm">
                  <b-col align-self="end" class="text-right" style="margin-right:20.4%">Alternative {{thousandSeparator(alttotal(part.parts.part_content))}}</b-col>
               </b-row>
            </span>
            <br>
         </b-collapse>
      </div>
   </draggable>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
import {  VueEditor, Quill  } from 'vue2-editor';

var partx = [
{parts:{part_name:'part1',

checkbox_list: {
   flavours: {},
    selected: {},
    allSelected: {},
    indeterminate: {}
}, 

part_content:[{
upHere : false,
сheckbox:'true',
count:'1',
description_head:'headDesk',
description_work:'',
description_from_price: '',
discount:'666%',
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'3',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'4',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'5',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},
{
upHere : false,
сheckbox:'true',
count:'2',
description_head:'headDesk',
description_work:'deskWork',
description_from_price: 'Generic generation and manipulation of text is challenging and has limited success compared to recent deep generative modeling in visual domain. This paper aims at generating plausible natural language sentences, whose attributes are dynamically controlled by learning disentangled latent representations with designated semantics. We propose a new neural generative model which combines variational auto-encoders and holistic attribute discriminators for effective imposition of semantic structures. With differentiable approximation to discrete text samples, explicit constraints on independent attribute controls, and efficient collaborative learning of generator and discriminators, our model learns highly interpretable representations from even only word annotations, and produces realistic sentences with desired attributes. Quantitative evaluation validates the accuracy of sentence and attribute generation.',
discount:'666%', 
position_number:'01.05.010',
price:'666',
status:'yes',
summa:'999',
unit:'Ps.',
without: false
},

]}}
]


  
export default {
    components: {
        draggable,
        VueEditor
    },
  props: {
    props: ['partx']
  },
  data() {
    return {
        addtaxColapse: false,
        alttax:[],
        unit_type:['Psch.', '%', 'Stück.', 'Sack.'],
        calc:['yes', 'no', 'etc', 'alternative'],
        butDiscPerc: '%',
        disc:0,
        discP:10,
        tax:0,
        tax2:0,
        taxP:19,
        taxP2:0,
        netto:0,
        brutto:0,
   persentCounter:0,
        counter: -1,
        moveToCopyRadio: 'Move',
        moveToCopy:[],
        tmpArr:[],
        oldColor:[],
        color:[],
      disable: [],
      toggle: [],
      partx: partx,




    } //return
  }, //data
  
  computed: {


    computedStylePlus: function () {
      var vm = this;
      return function (val) {
  
        if (val.length>0){
            return 'blue;'
        } else{
            return 'gray;'
        }

      }
    },

    colorIdent: function () {
      var vm = this;
      return function (part, subIndex) {
           if (this.color.indexOf(part+'-'+subIndex) != -1 ){
                return 'greenrow'
           } else{
                return ''
           }
         // return this.color[part+'-'+subIndex] ? 'green' : '';
      }
    },
computedWithDesc: function () {
      var vm = this;
      return function (val) {
        var w = 35;
        var count = 0;
          for (var obj in val) { 
             if(count==0){
                w=w+0.6
             }
             if(count>=2){
                w=w-1.7
             }
                w=w-0.6
                count++
            }
        
        return w;
      }
    },



    alltotal: function () {
      var vm = this;
      return function (value) {

        var summa=0
        value.forEach(function (val) {
            val.parts.part_content.forEach(function (val1) {
            if (val1.status=='yes') {
            summa+=val1.count * val1.price
            }
            })
        })

          return summa;
      };
   },
altalltotal: function () {
      var vm = this;
      return function (value) {

        var summa=0
        value.forEach(function (val) {
            val.parts.part_content.forEach(function (val1) {
            if (val1.status!='yes') {
            summa+=val1.count * val1.price
            }
            })
        })

          return summa;
      };
   },
    total: function () {
      var vm = this;
      return function (value) {
        var summa=0
        value.forEach(function (val) {
             if (val.status=='yes') {
            summa+=val.count * val.price
        }
        })
          return summa;  //количество разрядов
      };
   },
    alttotal: function () {
      var vm = this;
      return function (value) {
        var summa=0
        value.forEach(function (val) {
             if (val.status!='yes') {
            summa+=val.count * val.price
        }
        })
          return summa;  //количество разрядов
      };
   },
    persent_to_str: function(){
        var vm = this;
        return function (subIndex, all_obj, selected, content, summOrPercent){
            var summa=0
            for (var obj in all_obj) {

                if(selected[obj].indexOf('temp'+(subIndex+1))!=-1){
                    selected[obj].forEach(function(val, index){
                        if (val!='temp'+(subIndex+1)){
                            val=val.split('temp')
                            val[1]--

                                summa += content[val[1]].count*content[val[1]].price
                            
                        }
                    })
                }

            }

        var persent_from_summa = ((summa/100)*content[(subIndex)].count)
        content[(subIndex)].price = persent_from_summa/content[(subIndex)].count
        if (summOrPercent=='%'){
        return persent_from_summa
        }
        if (summOrPercent=='summ'){
        return summa.toFixed(2);
        }}
    }
  },
  methods: {
    disOptPercent(part, opt){
    var count=0
    part.forEach(function (val){
        if(val.unit=='%'){
            count++
        } 
    })

    if((part.length / count) < 2.5 && opt=='%'){
        return true
    }
},
    toModel(newVal, part){
   partx[part].parts.part_name=newVal.target.innerText
    },
   thousandSeparator(str) {
    return str
    },

    discOfPercent(){
  

var tmpDisc, tmpNetto, tmpTax, tmpTax2
        if(this.butDiscPerc=='%'){
            var add = 0
            partx.forEach((val)=>{
                val.parts.part_content.forEach((sval)=>{
                    if (sval.without==true){
                        add = add + ((sval.count*sval.price/100)*this.discP)
                    }
                })
            })
            this.disc=this.thousandSeparator((this.alltotal(partx)/100)*this.discP-add)
            tmpDisc=(this.alltotal(partx)/100)*this.discP-add
        }else{
            this.disc=this.thousandSeparator(this.discP)
            tmpDisc=this.discP   
        }

        this.netto=this.thousandSeparator(this.alltotal(partx)-tmpDisc)
        tmpNetto=this.alltotal(partx)-tmpDisc


        var addt = 0
        var addt2 = 0
            partx.forEach((val)=>{
                val.parts.part_content.forEach((sval, index)=>{
                if(sval.status=='yes'){
                    if (this.alttax[index]!=true){
                        addt = addt + (sval.count*sval.price)
                    } else{
                        addt2 = addt2 + (sval.count*sval.price)
                    }
                }
                })
            })
  
        this.tax=this.thousandSeparator(addt*(this.taxP/100))
        tmpTax=(addt*(this.taxP/100))

        this.tax2=this.thousandSeparator(addt2*(this.taxP2/100))
     //   tmpTax2=  addt2*(this.taxP2/100)
        tmpTax2=0

        this.brutto=this.thousandSeparator(tmpNetto+tmpTax+tmpTax2)

    },
selectRow(part, subIndex){
if (this.color.indexOf(part+'-'+subIndex) != -1) {
    this.color.splice(this.color.indexOf(part+'-'+subIndex), 1)
} else{
this.color.push(part+'-'+subIndex)
}
},
 

    classRow(arrayColumnOfPart, keyindex){
        var countPercent=-1
        arrayColumnOfPart.part_content.forEach(function(val, index){
          if(arrayColumnOfPart.part_content[index].upHere==true && val.unit=='%'){
                for (var i=0; i <= index; i++) {
                     if (countPercent < index && arrayColumnOfPart.part_content[i].unit == '%'){
                                              countPercent++
                         }
                }  
            }
         })
        if('in'+countPercent==keyindex){
            return 'upHereColumn'
        }
    },
  
    boxDisable(unit, obj, str){
      if(unit=='%'){
        return true
      } else{  
        var dis=0
        this.disable.forEach(function(val){
        var vals=val.split('-')
            if(vals[0] != obj){
                if (vals[1]==str){
                    dis++
                }
            }
        })         
        if (dis!=0){
          return true
        }        
      }
    },
    scheckStatus(){
        partx.forEach((part)=>{
            var obj 
                for (obj in part.parts.checkbox_list.selected){
                    var countStr=0
                    var check=0
                    
                    part.parts.part_content.forEach((val, index)=>{
                        if(val.unit == '%') {
                            countStr++
                        }else{
                            var dis
                            this.disable.forEach(function(dval){
                                dis=dval.split('-')
                               
                                if (index==dis[1]){
                                    check++
                                } 
                            })
                        }
                        if((countStr+check)==part.parts.checkbox_list.flavours[obj].length){
                        var objAls
                        for (objAls in part.parts.checkbox_list.allSelected){
                            if (objAls==obj){
                                var dis1
                                var uncheck=0
                                this.disable.forEach(function(dval1){
                                    dis1=dval1.split('-')
                                   
                                    if (objAls==dis1[0]){
                                        uncheck++
                                    } 
                                })
                                if(uncheck!=0){
                                this.$set(part.parts.checkbox_list.allSelected, objAls, true)
                                }
                            } 
                        }
                    }else{
                        this.$set(part.parts.checkbox_list.allSelected, obj, false)
                        }
                    
                    })
              
                  
                
                }

        })

    },
    box(event, obj, str){
    if (event!=null){
    this.disable.push(obj+'-'+str)} else{this.disable.splice(this.disable.indexOf(obj+'-'+str), 1)}
    this.scheckStatus()
    },
  
    tmouseOver: function(){
      this.show = true;   
    },
    mouseOut:function(){
      this.show=false;
    },
 
    computeStyleOffer(value) {
        switch (value) {
                case 'Open': return {'color': '#F5DEB3'};
                case 'Done': return {'color': 'green'};
                case 'Invoice': return {'color':'orange'};
                case 'Desiccation': return {'color':'grey'};
                case 'Leakage_Detection': return {'color':'red'};
                case 'Restoration': return {'color':'blue'};
            }
        },
   

         toggleItem: function (key) {
        var i = this.toggle.indexOf(key)
        if (i < 0) {
        this.toggle.push(key)
      } else {
        this.toggle.splice(i, 1)
      }
    },
    partDel(del_id){
       // console.log(del_id);
              if(confirm("Are you sure?"))partx.filter(function (valuePart, index) {
                if(valuePart.parts.part_name+index == del_id){
                       partx.splice(index, 1);
                } 
        });
    },
    subPartDel(del_id, subDel_id){
       // console.log(del_id);
              if(confirm("Are you sure?"))partx.filter(function (valuePart, index) {
                if(valuePart.parts.part_name+index == del_id){
                   valuePart.parts.part_content.splice(subDel_id, 1);

//console.log(valuePart.parts.checkbox_list.selected)
                  for (var property in valuePart.parts.checkbox_list.flavours) {
//определить значение и удалить по нему
                      valuePart.parts.checkbox_list.selected[property].splice(valuePart.parts.checkbox_list.selected[property].indexOf(valuePart.parts.checkbox_list.flavours[property][subDel_id]), 1)   
                      valuePart.parts.checkbox_list.flavours[property].splice(subDel_id, 1)
                    }      
                 

            } 
        });
    },
persent(val, index, checkbox_in_table, how_many_rows){
    this.persentCounter=val
    if (val=='%'){
        //почему 3 раза сработала????
        this.add_column_checkbox(checkbox_in_table, how_many_rows)
        
        for (var obj in checkbox_in_table.flavours) {
          }  
    checkbox_in_table.selected[obj].push(checkbox_in_table.flavours[obj][index])

    }
    else {
          for (var obj in checkbox_in_table.flavours) {
             var valCecked = checkbox_in_table.flavours[obj][index]
             if(checkbox_in_table.selected[obj].indexOf(valCecked)!=-1 ){
                this.remove_column_checkbox(checkbox_in_table, obj)
             }
        }
    }
},

remove_column_checkbox(checkbox_in_table, key){
this.$delete(checkbox_in_table.indeterminate, key)
this.$delete(checkbox_in_table.allSelected, key)
this.$delete(checkbox_in_table.flavours, key)
this.$delete(checkbox_in_table.selected, key)
},    
add_column_checkbox(checkbox_in_table, how_many_rows){
var sum_of_property = 0
for (var property in checkbox_in_table.allSelected) {
  sum_of_property += 1
}

var flavour = new Array()
for (var row = 1; row<=how_many_rows; row++) {
  flavour.push('temp'+row)
}

this.$set(checkbox_in_table.allSelected, 'in'+sum_of_property, false)
this.$set(checkbox_in_table.flavours, 'in'+sum_of_property, flavour)
this.$set(checkbox_in_table.indeterminate, 'in'+sum_of_property, false)
this.$set(checkbox_in_table.selected, 'in'+sum_of_property, [])
this.scheckStatus()
},
toggleAll(event, target, model, persent) {

    model.allSelected[target]=event
    if (model.allSelected[target]){
    var obj
          model.flavours[target].forEach( (val, index) => {
           
            if(persent[index].unit!='%'){
                var count = 0
                for (obj in model.allSelected) {
                  if (model.flavours[target][index] == model.selected[obj][model.selected[obj].indexOf(model.flavours[target][index])]) count++
                }
                if (count == 0){
                   
                    model.selected[target].push(model.flavours[target][index])
                    this.box(model.flavours[target][index], target, index)
                }
            } 
        })

    }
    else {
    var obj
         model.flavours[target].forEach( (val, index) => {
            if(persent[index].unit!='%'){
                if(model.selected[target].indexOf(model.flavours[target][index])!=-1){
                model.selected[target].splice(model.selected[target].indexOf(model.flavours[target][index]), 1)
                 this.box(null, target, index)
            }}
        })
    }

              
    }
 },
   
watch: { 
  partx: {
    handler: function(newVal) {
            var result
            var sval
            var separator
            var indexReplace, indexRuslt
            var safeEval = require('safe-eval')
            

        partx.forEach((part, index) => {
        for (var obj in newVal[index].parts.part_content) {
             var tname = 't'+index+'x'+obj
            if(newVal[index].parts.part_content[obj].description_work.indexOf(' ')!=-1) {
            separator = this.$refs[tname][0].quill.getText()
            separator = separator.replace(/\n/g, ' ')
            separator = separator.substring(0, separator.length - 1);
             separator=separator.split(' ')
             separator.splice(-1,1)
             separator.forEach((val)=>{
                if(val.search(/[a-zA-z=]/gim)==-1){
                if(val.search(/[-+*)(/]/gim)>-1){
                if(val.search(/[0-9]/gim)>-1){
                if(/[\d)]/.test(val[val.length-1])){
                 
                try {
                    result= this.thousandSeparator(safeEval(val))
                    } catch(e) {
                    result= '(not valid formula)'
                  }
                sval=val.replace(/([-+*)(/])/gim, '$1&shy;')+'='+result+' '
                indexRuslt = result.length ? result.length : 4
                indexReplace = partx[index].parts.part_content[obj].description_work.indexOf(val)+indexRuslt+6
                this.$refs[tname][0].quill.clipboard.dangerouslyPasteHTML(partx[index].parts.part_content[obj].description_work.replace(val, sval))
                this.$refs[tname][0].quill.setSelection(indexReplace, 0)
               }
           }
       }
        }
             })
             

            }

      }
 })
    },
    deep: true, 
},


  }

}
</script>