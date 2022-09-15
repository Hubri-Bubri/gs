<template>
  <b-container fluid>
      <b-table  stacked="lg" @row-clicked="$emit('dataToFoot', $event)" class="tableProject" striped hover  :items="items_search()" :fields="fieldsTable"  busy.sync="isBusy">
        <template slot="status_set" slot-scope="it" >
          <span style="height:30px;">
            <line-chart :datas="dataCharts(it.item)" :height="50" style="max-width:200px;" />
          </span>
        </template>
        <template slot="street1" slot-scope="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.street1}}</span>
          </div>
        </template>
        <template slot="name" slot-scope="data">
          <div class="text-container">
            <span  class="text-content"> {{data.item.names}}</span>
          </div>
        </template>
        <template slot="netto" slot-scope="it" >
       <!--    {{it.item.netto|thousandSeparator}} -->
        </template>
        <template slot="brutto" slot-scope="it" >
<!--           {{it.item.brutto|thousandSeparator}} -->
        </template>
        <template slot="days" slot-scope="it">
          <div style="padding-right:30px;">
            {{difdate(it.item.date)}}
          </div>
        </template>
        <template slot="number" slot-scope="it">
          {{it.item.number.split('-')[0]+'-'+it.item.date.split('-')[0]}} 
 <!--          <div v-if="it.item.number.split(' ').length==3">
            {{
              countDigitals(it.item.number.split(' ')[1])
              +'-'+
              it.item.number.split(' ')[0].split('-')[1]
            }}
          </div>
          <div v-if="it.item.number.split(' ').length==5">
            {{
              it.item.number.split(' ')[0]+' - '+it.item.number.split(' ')[3]
            }}
          </div> -->
        </template>
        <template slot="cnumber" slot-scope="it">

          <b-link :to="'/project/detail/'+it.item.project_id"  v-if="it.item.cnumber.split(' ').length==3">
            {{
              countDigitals(it.item.cnumber.split(' ')[0])
            }}
          </b-link>
          <b-link :to="'/project/detail/'+it.item.project_id"  v-if="it.item.cnumber.split(' ').length==5">
            {{
              it.item.cnumber.split(' ')[2]
            }}
          </b-link>
        </template>
        <template slot="date" slot-scope="data">
          {{data.item.date | dateInverse}}
        </template>
        <template slot="netto" slot-scope="data">
          <span v-if="data.item.number.split(' ').length==1">{{data.item.netto|thousandSeparator}}</span>
          <span v-if="data.item.number.split(' ').length==3">{{data.item.netto|thousandSeparator}}</span>
          <span v-if="data.item.number.split(' ').length==5">{{data.item.netto|thousandSeparator}}</span>
        </template>
        <template slot="brutto" slot-scope="data">
          <span v-if="data.item.number.split(' ').length==1">{{data.item.brutto|thousandSeparator}}</span>
          <span v-if="data.item.number.split(' ').length==3">{{data.item.brutto|thousandSeparator}}</span>
          <span v-if="data.item.number.split(' ').length==5">{{data.item.brutto|thousandSeparator}}</span>

        </template>
      </b-table>

<div v-show="(this.items_search().length==0)&&startSpin">
 <Spinner size="large"></Spinner>
</div>


</b-container>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
    props: [
      'result', 'items',  'selected', 'rowId', 'brutto', 'op',
      'comment', 'typesForTablesOpt', 'fieldsTable', 'options', 'keyword'
  ],   data() {
        return {
          startSpin:true}
        },

    methods: {

 items_search() {
        this.fieldsTable.number.variant =
        this.fieldsTable.cnumber.variant =
        this.fieldsTable.date.variant =
        this.fieldsTable.street1.variant =
        this.fieldsTable.name.variant =
        this.fieldsTable.netto.variant =
        this.fieldsTable.brutto.variant =
        this.fieldsTable.days.variant = ''
      if (this.keyword){
         return this.items.filter(item =>{
            var numberInv = this.countDigitals(item.cnumber.split(' ')[1])+'-'+item.cnumber.split(' ')[0].split('-')[1]
            var numberSubInv = item.number.split(' ')[1]
            var numberContr = this.countDigitals(item.cnumber.split(' ')[0])
            var numberSubContr = item.number.split(' ')[0]
            var diferdate = this.difdate(item.date).toString()
            var comm = (item.comment?item.comment:'')

          if (item.id[0]!='s'?numberInv.includes(this.keyword):numberSubInv.includes(this.keyword)){
            this.fieldsTable.number.variant = 'info'
            return true
          }
          if (item.id[0]!='s'?numberContr.includes(this.keyword):numberSubContr.includes(this.keyword)){
            this.fieldsTable.cnumber.variant = 'info'
            return true
          }
          if (this.$options.filters.dateInverse(item.date).includes(this.keyword)){
            this.fieldsTable.date.variant = 'info'
            return true
          }
          if (item.street1.includes(this.keyword)){
            this.fieldsTable.street1.variant = 'info'
            return true
          }
          if (item.names.includes(this.keyword)){
            this.fieldsTable.name.variant = 'info'
            return true
          }
           if (this.$options.filters.thousandSeparator(item.netto).includes(this.keyword)){
            this.fieldsTable.netto.variant = 'info'
            return true
          } 
             if (this.$options.filters.thousandSeparator(item.brutto).includes(this.keyword)){
            this.fieldsTable.brutto.variant = 'info'
            return true
          }
            if (diferdate.includes(this.keyword)){
            this.fieldsTable.days.variant = 'info'
            return true
          } 
            if (comm.includes(this.keyword)){
            this.fieldsTable.number.variant =
            this.fieldsTable.cnumber.variant =
            this.fieldsTable.insurance_number.variant =
            this.fieldsTable.date.variant =
            this.fieldsTable.place.variant =
            this.fieldsTable.netto.variant =
            this.fieldsTable.brutto.variant =
            this.fieldsTable.days.variant = 'info'
            return true
          } 

          })
        }
        else{
            return this.items
        }
},

    countDigitals(val){
      if (val != undefined){
        var nuls=3-val.toString().length
                    for (var i = 0; i <= nuls; i++) {
                        val='0'+val
                    }
        return val
        }
    },

    difdate(val){
        var date1 = new Date(val)
        var date2 = new Date()
        var daysLag = Math.ceil(Math.abs(date2.getTime() - date1.getTime()) / (1000 * 3600 * 24))
        return (-14+(daysLag-1))
    },


        dataCharts(val){
        var brutto=(val.brutto < 0) ? -val.brutto : val.brutto
        var pay=this.summFromRow(val, brutto)*100/brutto
        var withOut=100-(this.summFromRow(val, brutto)*100/brutto)
       var t = 'i'
        if (val.type=="Sub Invoices"){
            t = 's'
        }
        if (val.type=="Invoices"){
            t = 'i'
        }
        // pay = Math.round(pay)
        // withOut = Math.round(withOut)
        return [pay, withOut, t]
        },
  
        summFromRow(row, brutto){
            var result = 0
            row.op.forEach((v)=>{
                 result = parseFloat(result) + parseFloat(v.value)
            })
            if (result>brutto){
                result = brutto
            }
            if (result<(-brutto)){
                result = -brutto
            }
            return result
        },

},
      mounted(){
    
        setTimeout(()=>{
               this.startSpin = false
            }, 5000);
      }

    }
</script>
<style type="text/css">
.status{
    width: 200px;
}
.text-container {
    position: relative;
    display: block;
    width: 100%;
    height: calc(2em + -5px);
    overflow: hidden;
    white-space: normal;
}
.text-content {
  word-break: break-all;
  position: relative;
  display: block;
  max-height: 3em;
}
</style>