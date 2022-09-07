<template>
        <b-col sm="6" class="cuestomRow">
           <b-form-row>
              <b-col cols="4"  class="cForm-input">
                 Discont:
              </b-col>
              <b-col cols="3">
                 <b-input-group class="cForm-input">
                    <b-input id="disc" type="number" v-model="discP" :state="null" 
                       placeholder="Summa of Percent" @input="discOfPercent()" class="cForm-input"/>
                    <b-input-group-append >
                       <div class="input-group-text lablelInInput" @click="butDiscPerc = (butDiscPerc == '%' ? 'P' : '%'); discOfPercent()">{{butDiscPerc}}</div>
                    </b-input-group-append>
                 </b-input-group>
              </b-col>
              <b-col cols="5">
                 <b-input-group class="cForm-input">
                    <b-input disabled id="sop" v-model="disc"  :state="null"  type="text"
                       placeholder="Summa of Percent" class="cForm-input text-right" />
                         <b-input-group-append >
                            <div class="input-group-text lablelInInput">€</div>
                        </b-input-group-append>  
                 </b-input-group>
              </b-col>
           </b-form-row>
           <b-form-group horizontal :label-cols="7" class="cForm" label="Netto:" label-for="netto">
              <b-input-group  class="cForm-input">
                 <b-form-input id="netto" v-model="netto" :state="null"  type="text" 
                    placeholder="Enter netto" disabled class="cForm-input text-right" />
                    <b-input-group-append >
                        <div class="input-group-text lablelInInput">€</div>
                    </b-input-group-append>  
              </b-input-group>
           </b-form-group>
           <b-form-row>
              <b-col cols="3" class="cForm-input">
                 Added tax:
              </b-col>
              <b-col cols="1" class="cForm-input">
                 <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'">
                    <span class="when-closed">+</span>
                 </b-link>
              </b-col>
              <b-col cols="3">
                 <b-input-group class="cForm-input">
                    <b-input id="taxP" v-model="taxP" :state="null"  type="number" @input="discOfPercent()"
                       placeholder="Summa of Percent" class="cForm-input " />
                        <b-input-group-append ><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                 </b-input-group>
              </b-col>
              <b-col cols="5">
                 <b-input-group  class="cForm-input">
                    <b-input disabled id="tax" v-model="tax" :state="null"  type="text"
                       placeholder="Summa of Percent" class="cForm-input text-right" />
                        <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                 </b-input-group>
              </b-col>
           </b-form-row>
           <b-collapse style="width:100%" id="addtax" :value="value" @input="onAddtaxCollapse">
              <b-form-row>
                 <b-col cols="3"  class="cForm-input calttax">
                    Added tax:
                 </b-col>
                 <b-col cols="1"  class="cForm-input">
                    <b-link style="text-decoration: none;font-weight: normal;" v-b-toggle="'addtax'">
                       <span class="when-opened">-</span>
                    </b-link>
                 </b-col>
                 <b-col cols="3">
                    <b-input-group   class="cForm-input">
                       <b-input id="taxP" v-model="taxPDub" :state="null"  type="number" @input="discOfPercent()"
                          placeholder="Summa of Percent" class="cForm-input " />
                                   <b-input-group-append ><div class="input-group-text lablelInInput">%</div></b-input-group-append>  
                    </b-input-group>
                 </b-col>
                 <b-col cols="5">
                    <b-input-group  class="cForm-input">
                       <b-input disabled id="tax" v-model="taxDub" :state="null"  type="text"
                          placeholder="Summa of Percent" class="cForm-input text-right" />
                          <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
                    </b-input-group>
                 </b-col>
              </b-form-row>
           </b-collapse>
           <b-form-group horizontal :label-cols="7" class="cForm" label="Brutto:" label-for="brutto">
              <b-input-group  class="cForm-input">
                 <b-form-input id="brutto" v-model="brutto" :state="null"  type="text"
                    placeholder="Enter brutto" disabled class="cForm-input text-right" />
                   <b-input-group-append ><div class="input-group-text lablelInInput">€</div></b-input-group-append>  
              </b-input-group>
           </b-form-group>
        </b-col>
</template>

<script type="text/javascript">
export default {
    props: ['value', 'partx', 'tax', 'taxDub', 'taxP', 'taxPDub', 'disc', 'discP'],
    data() {
        return {
            unit_type: ['Psch.', '%', 'Stück.', 'Sack.'],
            calc: ['yes', 'no', 'etc', 'alternative'],
            butDiscPerc: '%',
            netto: 0,
            brutto: 0,
            persentCounter: 0
        }
    },
 
    methods: {
        onAddtaxCollapse($event){
          { this.$emit('input', $event) }
        },
        discOfPercent() {
            var tmpDisc, tmpNetto, tmpTax, tmpTax2
            var summa = 0
                this.partx.forEach(function(val) {
                    val.parts.part_content.forEach(function(val1) {
                        if (val1.status == 'yes') {
                            summa += val1.count * val1.price
                        }
                    })
                })

            if (this.butDiscPerc == '%') {
                var add = 0
                this.partx.forEach((val) => {
                    val.parts.part_content.forEach((sval) => {
                        if (sval.without == true) {
                            add = add + ((sval.count * sval.price / 100) * this.discP)
                        }
                    })
                })
                this.disc = this.$options.filters.thousandSeparator((summa / 100) * this.discP - add)
                tmpDisc = (summa / 100) * this.discP - add
            } else {
                this.disc = this.$options.filters.thousandSeparator(this.discP)
                tmpDisc = this.discP
            }

            this.netto = this.$options.filters.thousandSeparator(summa - tmpDisc)
            tmpNetto = summa - tmpDisc


            var addt = 0
            var addt2 = 0
            this.partx.forEach((val) => {
                val.parts.part_content.forEach((sval, index) => {
                    if (sval.status == 'yes') {
                        if (sval.alttax != true) {
                            addt = addt + (sval.count * sval.price)
                        } else {
                            addt2 = addt2 + (sval.count * sval.price)
                        }
                    }
                })
            })

            this.tax = this.$options.filters.thousandSeparator(addt * (this.taxP / 100))
            tmpTax = (addt * (this.taxP / 100))
            this.taxDub = this.$options.filters.thousandSeparator(addt2 * (this.taxPDub / 100))
            //   tmpTax2=  addt2*(this.taxPDub/100)
            tmpTax2 = 0
            this.brutto = this.$options.filters.thousandSeparator(tmpNetto + tmpTax + tmpTax2)

        },


    },

    watch: {
        partx: {
            handler: function() {
                this.discOfPercent()
            },
            deep: true,
        },
    }

}
</script>
