<template>
<div>
<b-container v-if="type!='send'" style="padding-left:0px;">
    <b-row v-if="type!='head' && disc!='0,00'" style="padding-top:3px;" :align-h="align">
           <b-col cols="3">
                 Summ Net Amounts: </b-col>
                 <b-col cols="2" style="padding-right: 0px;" class="text-right">{{summ | thousandSeparator}} €</b-col>
            </b-row>
  <b-row   v-if="type!='head' && disc!='0,00'"  style="padding-top:3px;" :align-h="align">
           <b-col cols="3">
                 Discont: {{discP}}{{butDiscPerc}}</b-col>
                 <b-col cols="2"   class="text-right" style="border-bottom: 1px solid #000; padding-right: 0px;" >{{disc}} €</b-col>
            </b-row>
  <b-row   style="padding-top:3px;"  :align-h="align">
<b-col cols="3"><div v-if="disc!='0,00' && type!='head'">Subtotal:</div><div v-else>Sum Of {{head}} Netto:</div>
             </b-col><b-col cols="2"  style="padding-right: 0px;" class="text-right">{{netto}} €
             </b-col>
           </b-row>
  <b-row style="padding-top:3px;" :align-h="align">
 <b-col cols="3">
                 Added tax: {{taxP}}% </b-col>
                 <b-col cols="2"  style="padding-right: 0px;" class="text-right">{{tax}} €</b-col>
         </b-row>
   <b-row style="padding-top:3px;" :align-h="align" v-if="value">
                  <b-col cols="3">   Added tax: {{taxPDub}}% </b-col>
                  <b-col cols="2"  style="padding-right: 0px;" class="text-right">  {{taxDub}} € </b-col>
         </b-row>
        <b-row style="padding-top:3px;" :align-h="align">
      <b-col cols="3"><b v-if="type=='head'">Sum Of {{head}} Brutto:</b>
        <div v-else>Brutto Amounts:</div>
      </b-col>
            <b-col cols="2" style="border-top: 3px double #000; padding-top: 2px;padding-right: 0px;" class="text-right"  v-if="type=='head'"><b>{{brutto}} €</b></b-col>
            <b-col cols="2" style="border-bottom: 3px double #000;padding-right: 0px;" class="text-right" v-else>{{brutto}} €</b-col>
           </b-row>
</b-container>
  <div v-else>
    <input type="hidden" name="summ" :value="summ | thousandSeparator" />
    <input type="hidden" name="summ1" :value="netto" />
    <input type="hidden" name="discP" :value="discP" />
    <input type="hidden" name="butDiscPerc" :value="butDiscPerc" />
    <input type="hidden" name="disc" :value="disc" />
    <input type="hidden" name="netto" :value="snetto" />
    <input type="hidden" name="taxP" :value="taxP" />
    <input type="hidden" name="tax" :value="tax" />
    <input type="hidden" name="taxP2" :value="taxPDub" />
    <input type="hidden" name="tax2" :value="taxDub" />
    <input type="hidden" name="brutto" :value="brutto" />
  </div>
<!--   {{value, partx, type, summ, align, tax, taxDub, taxP, taxPDub, disc, discP, netto, brutto, butDiscPerc}}
 --></div>
</template>

<script type="text/javascript">
export default {
    props: ['value', 'partx', 'type', 'summ', 'align', 'tax', 'taxDub', 'taxP', 'taxPDub', 'disc', 'discP', 'netto', 'brutto', 'butDiscPerc', 'head'],
    data() {
        return {
        snetto:0,

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
                this.sdisc = this.$options.filters.thousandSeparator((summa / 100) * this.discP - add)
                tmpDisc = (summa / 100) * this.discP - add
            } else {
                this.sdisc = this.$options.filters.thousandSeparator(this.discP)
                tmpDisc = this.discP
            }

            this.snetto = this.$options.filters.thousandSeparator(summa - tmpDisc)
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

            this.stax = this.$options.filters.thousandSeparator(addt * (this.taxP / 100))
            tmpTax = (addt * (this.taxP / 100))
            this.staxDub = this.$options.filters.thousandSeparator(addt2 * (this.taxPDub / 100))
            //   tmpTax2=  addt2*(this.taxPDub/100)
            tmpTax2 = 0
            this.sbrutto = this.$options.filters.thousandSeparator(tmpNetto + tmpTax + tmpTax2)

        },


    },

    mounted() {
      this.discOfPercent()
    }

}
</script>