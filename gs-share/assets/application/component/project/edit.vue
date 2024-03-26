<template>
	<div ref="editcomponet">
		<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
		@mouseover="cloudHover = true" @mouseleave="cloudHover = false"
		@click="writecomet();cloudChange=false;cloudLoad=true;" v-if="(tmp.number==null)">
		<b-icon stacked icon="circle-fill" :animation="cloudLoad?'throb':null" variant="primary" v-show="cloudLoad||cloudHover"></b-icon>
		<b-icon stacked icon="cloud-upload" scale="0.5" :variant="cloudHover?'light':'dark'" v-show="!cloudLoad"></b-icon>
		<b-icon stacked icon="circle" variant="info" v-show="cloudChange"></b-icon>
		</b-iconstack>
		<span v-if="(tmp.number==null)" style="position:relative;left:24px;top:15px;z-index:2;">{{(timeSave!=null)?$t('alert.LastSaveIn')+': '+timeSave:''}}</span>
		<b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
		@click="checkInEditor('other')" v-if="(tmp.number==null)" @mouseover="calcHover = true" @mouseleave="calcHover = false">
		<b-icon stacked icon="circle-fill" variant="primary" v-show="calcHover"></b-icon>
		<b-icon stacked icon="calculator" scale="0.5" :variant="calcHover?'light':'dark'"></b-icon>
		</b-iconstack>

		<vue-editor :value="project.other" :editorToolbar="customToolbar"
			style="position:relative;top:-20px;z-index:1;" v-if="(tmp.number==null)"
			class="text-right"  ref="other"
			@blur="save()"
			:id="'gencooment'+id" 
			/>
		<b-container v-if="tmp.number != null">
			<b-input type="text" hidden v-model="tmp.typeOfHead" />
			<b-row>
				<b-col cols="12"><br></b-col>
				<b-col lg="8" md="12">
					<b-row>
						<b-col lg="6" md="12" >
							<b-form-group :label="$t('fields.number')+':'" label-cols="4" label-size="sm">
								{{(tmp.typeOfHead=='Invoices')?(tmp.number.split(' ').length==5)?tmp.number.split(' ')[3]:
								countDigitals(tmp.number.split(' ')[1])+'-'+tmp.number.split(' ')[0].split('-')[1]:(tmp.typeOfHead=='SUB')
								?tmp.number.split(' ')[0]:(tmp.typeOfHead=='Sub Invoices')?tmp.number.split(' ')[3]:tmp.number}}
							</b-form-group>
							<b-form-group :label="$t('edit.document')+':'" label-cols="4" label-size="sm">
								<b-form-input  size="sm"
								type="date" @change="updateItem($event, 'date', tmp.id, tmp.date)"
								:value="tmp.date" placeholder="Enter date"  
                />
							</b-form-group>
							<b-form-group :label="$t('edit.place')+':'" label-cols="4" label-size="sm">
								<b-form-input  type="text"   size="sm"
								@change="updateItem($event, 'place', tmp.id, tmp.place)" :value="tmp.place" placeholder="Enter place"   />
							</b-form-group>
						</b-col>
						<b-col lg="6" md="12" >
							<b-form-group :label="$t('edit.order')+':'" label-cols="4" label-size="sm">
								<b-form-input   :state="null" type="text" size="sm"
								@change="updateItem($event, 'other', tmp.id, tmp.other)"
								:value="tmp.other" placeholder="Enter number" />
							</b-form-group>
							<b-form-group :label="$t('edit.insurance')+':'" label-cols="4" label-size="sm" >
								<b-form-input  size="sm" :state="null" type="text"
                @change="updateItem($event, 'insurance_number', tmp.id, tmp.insurance_number)"
                :value="tmp.insurance_number" placeholder="Enter insurance number"
                 />
							</b-form-group>
							<b-form-group :label="$t('edit.insName')+':'" label-cols="4" label-size="sm">
								<b-form-input  size="sm" :state="null" type="text"  placeholder="Enter insurance name"
								@change="updateItem($event, 'insurname', tmp.id, tmp.insurname)" :value="tmp.insurname"
                 />
							</b-form-group>
						</b-col>
						<b-col lg="6" md="12" >
						</b-col>
					</b-row>
				</b-col>
			<b-col lg="4" md="12" >
					<b-form-group :label="$t('edit.discont')+':'" label-cols="4" label-size="sm">
						<b-input-group>
							<b-input id="disc" type="number" size="sm" :value="tmp.discP" min="0" max="100"
              @change="updateDiscont(Math.abs($event), 'discP', tmp.id, tmp.discP)" />
							<b-link @click="updateDiscont((tmp.butDiscPerc == '%' ? 'P' : '%'), 'butDiscPerc', tmp.id, tmp.butDiscPerc)"
              style="white-space: nowrap;text-decoration:none;">
							{{tmp.butDiscPerc}}
							</b-link>
							<b-col class="text-right" style="white-space: nowrap;">
								{{tmp.gen_discont}} €
							</b-col>
						</b-input-group>
					</b-form-group>
						<b-form-group :label="$t('edit.netto')+':'" label-cols="4" label-size="sm">
						<b-col class="text-right" style="white-space: nowrap;">{{tmp.gen_summa}} €</b-col>
					</b-form-group>
					<b-form-group :label="$t('edit.taxCountName')+((tmp.addtaxColapse=='true')?' 1':'')+':'" label-cols="4" label-size="sm">
						<b-input-group>
  							<b-input id="taxP" :value="tmp.taxP" size="sm" @change="updateItem($event, 'taxP', tmp.id, tmp.taxP)"
								type="number" />
							%
							<b-col class="text-right" style="white-space: nowrap;">
								{{tmp.tax}} € <b-link  style="text-decoration: none;" @click="updateItem((tmp.addtaxColapse == 'true' ? 'false' : 'true'), 'addtaxColapse', tmp.id, tmp.addtaxColapse)"
              v-show="tmp.addtaxColapse!='true'">
								+
							</b-link>
              <span v-show="tmp.addtaxColapse=='true'">&nbsp;&nbsp;&nbsp;</span>
							</b-col>
						</b-input-group>
					</b-form-group>
						<b-form-group :label="$t('edit.taxCountName')+' 2:'" label-cols="4" label-size="sm" v-show="tmp.addtaxColapse=='true'">
							<b-input-group>
								<b-input id="taxP" :value="tmp.taxPDub" size="sm"  @change="updateItem($event, 'taxPDub', tmp.id, tmp.taxPDub)" type="number" />
								  %
								<b-col class="text-right"  style="white-space: nowrap;">
									{{tmp.taxDub}} € <b-link style="text-decoration: none;" @click="updateItem((tmp.addtaxColapse == 'true' ? 'false' : 'true'), 'addtaxColapse', tmp.id, tmp.addtaxColapse)">
									&mdash;
								</b-link>
								</b-col>
							</b-input-group>
						</b-form-group>
					<b-form-group :label="$t('edit.brutto')+':'" label-cols="4" label-size="sm">
						<b-col class="text-right"  style="white-space: nowrap;">
							{{tmp.brutto}} €
						</b-col>
					</b-form-group>
				</b-col> 
			</b-row>
			<calc-table-group v-if="tmp.id"
			:works="works"
			:pid="id"
      :key="tmp.id"
			:tmp="tmp"
			:workers="workers"
			:selectedWorkers="selectedWorkers"
	  	:availableMails="availableMails"
			:plan="plan"
      :opt='typesForTables'
			@seltable="seltable"
			@sendMail="$emit('sendMail', availableMails)"
      @worker="worker"
      @openWindowPrint="openWindowPrint"
			ref="calcGroup"
			></calc-table-group>
		</b-container>
  </div>
</template>
<script type = "text/javascript">
import axios from 'axios';
import moment from 'moment';
import {
	VueEditor
}
from 'vue2-editor';
export default {
	components: {
		VueEditor,
	},
	props: ['tmp', 'project', 'works', 'availableMails', 'id', 'selectedWorkers', 'typesForTables', 'workers', 'plan'],
	data() {
		return {
			timeSave: null,
			calcHover: false,
			cloudHover: false,
			cloudChange: false,
			cloudLoad: false,
			addtaxColapse: null,
			tax: 0,
			taxDub: 0,
			taxP: 0,
			taxPDub: 0,
			disc: 0,
			discP: 0,
			butDiscPerc: '%',
			netto: 0,
			brutto: 0,
			customToolbar: [
				[{
					list: "check"
				}],
				['bold', 'italic', 'underline', 'strike'],
				[{
					'color': []
				}, {
					'background': []
				}],
				[{
					'align': []
				}],
			]
		}
	},
	methods: {
		linkForWorkersToEdit(user, host, projectNumer, itemMenuImag){
			console.log(user, host, projectNumer, itemMenuImag)
		this.$refs.calcGroup.linkForWorkersToCalcGroup(user, host, projectNumer, itemMenuImag)
	},
    openWindowPrint(type){
      this.$emit('openWindowPrint', type)
    },
save(){
  this.writecomet();
  this.cloudChange=false;
  this.cloudLoad=true;
  this.timeSave = moment().format("DD.MM HH:mm")
},
writecomet(){
var newContent =  this.$refs['other'].quill.getHTML()
  if (newContent != '<p><br></p>') {
    this.$emit('projectOther', newContent);
    this.updateProject('other', newContent);
  }
},
checkInEditor(tname){
      var result
      var sval
      var separator
      var safeEval = require('safe-eval')
      var valueHtml = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname].quill.getHTML():''

      if (valueHtml.indexOf('=') != -1) {
              separator = (this.$refs[tname]!=undefined)&&(this.$refs[tname].length!=0)?this.$refs[tname].quill.getText():''
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

                        this.$refs[tname].quill.clipboard.dangerouslyPasteHTML(
                          valueHtml = valueHtml.replace(calcval+'=', sval)
                        )
                      }
                    }
                  }
                }
              })
            }

     this.updateProject('other', valueHtml)
},
updateProject(fild, newData){
        axios.post('/updateProject', {
                id: this.id,
                date: newData,
                fild: fild
        }).then(response => {
          if (fild == 'other'){
             axios.post('/updateProject', {
              
                  id: this.id,
                  date:  this.$security.table.account.first_name+'_'+this.$security.table.account.second_name,
                  fild: 'user'
                 }).then(response => {
                  this.cloudLoad = false;
                 });
             axios.post('/updateProject', {
              
                  id: this.id,
                  date: moment().format("DD.MM HH:mm"),
                  fild: 'datacomment'
                 });
          }
        })
        },

    seltable(id, e){
      this.$emit('seltable', id, e)
    },
		worker() {
			this.$emit('worker')
		},
		countDigitals(val) {
			var nuls = 3 - val.toString().length
			for (var i = 0; i <= nuls; i++) {
				val = '0' + val
			}
			return val
		},
		updateDiscont(val, type, id, old) {
      if (old != val) {
      axios.get('/update_item_discont', {
				params: {
          val: val,
				  type: type,
				  id: id
				}
			})
    }
		},
		updateItem(val, type, id, old) {
      		if (old != val) {
				axios.get('/update_item_from_project', {
				params: {
					val: val,
					type: type,
					id: id
				}
				})
      		}
		},
	},
}
</script>