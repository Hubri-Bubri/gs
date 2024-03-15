<template>
	<!-- <div ref="editcomponet"> -->
		<!-- <b-iconstack font-scale="3" style="position:relative;left:24px;top:25px;z-index:2;"
		@mouseover="cloudHover = true" @mouseleave="cloudHover = false"
		@click="writecomet();changeDisable('b', 'gencooment', id);cloudChange=false;cloudLoad=true;" v-if="(tmp.number==null)">
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
		<span v-show="(disablefildUser('gencooment', id)!='you')" style="position:relative;left:30px;top: 16px;width:18px;z-index:2;"
			v-if="(tmp.number==null)">{{disablefildUser('gencooment', id)}}</span>
		<vue-editor :value="project.other" :editorToolbar="customToolbar"
			style="position:relative;top:-20px;z-index:1;" v-if="(tmp.number==null)"
			class="text-right"  ref="other"
			@blur="save()"
			@focus="changeDisable('f', 'gencooment', id);cloudChange=true;"
			:id="'gencooment'+id" 
			:disabled="disablefild('gencooment', id)?'disabled':false"
			/> -->
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
							<!-- <b-tooltip triggers="none" :show="disablefild('ofnumber', tmp.id)" :target="'ofnumber'+tmp.id">
								{{disablefildUser('ofnumber', tmp.id)}}
							</b-tooltip> -->
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
							<!-- <b-tooltip triggers="none" :show="disablefild('ofdate', tmp.id)" :target="'ofdate'+tmp.id">
								{{disablefildUser('ofdate', tmp.id)}}
							</b-tooltip> -->
						</b-col>
						<b-col lg="6" md="12" >
							<!-- <b-tooltip triggers="none" :show="disablefild('ofplace', tmp.id)" :target="'ofplace'+tmp.id">
								{{disablefildUser('ofplace', tmp.id)}}
							</b-tooltip> -->
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
							<!-- <b-tooltip triggers="none" :show="disablefild('ofother', tmp.id)" :target="'ofother'+tmp.id">
								{{disablefildUser('ofother', tmp.id)}}
							</b-tooltip> -->
						</b-col>
						<b-col lg="6" md="12" >
							<!-- <b-tooltip triggers="none" :show="disablefild('ofinsurance2', tmp.id)" :target="'ofinsurance2'+tmp.id">
								{{disablefildUser('ofinsurance2', tmp.id)}}
							</b-tooltip> -->
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
			:windowPrint="windowPrint"
			:works="works"
			:selectedCornty="selectedCornty"
			:project="project"
			:account="$security.table.account"
			:pid="id"
			:comments="comments"
      :key="tmp.id"

			:tmp="tmp"
			:workers="workers"
			:customer="customer"
			:person="person"
			:selectCustomer="selectCustomer"
			:selectPerson="selectPerson"
			:selectedWorkers="selectedWorkers"
			:selectedDocsList="selectedDocsList"
			:addPdfs="addPdfs"
			:makemodalpdf="makemodalpdf"
			:typeDocsList="typeDocsList"
			:availableMails="availableMails"
			:plan="plan"
      :opt='typesForTables'

			@seltable="seltable"
			@sendMail="$emit('sendMail', availableMails)"
			@selectedDocs="selectedDocs"
			@addPdf="addPdf"
			@printPdf="printPdf"
			@preview="preview"
			@printOffer="printOffer"
			@worker="worker"
			@hideWindowPrint="hideWindowPrint"
			ref="calcGroup"
			></calc-table-group>

			<!-- :disc='disc'
			:discP='discP'
			:tax='tax'
			:taxDub='taxDub'
			:taxP='taxP'
			:taxPDub='taxPDub'
			:netto='netto'
			:brutto='brutto' -->

      <!-- :loadDamages="loadDamages" -->
      <!-- :funcStop="funcStop" -->
      <!-- :value="partx" -->
      <!-- :rowsLoading = "rowsLoading" -->
      <!-- :rowsBusy = "rowsBusy" -->
      <!-- @changeSum="discOfPercent()" -->
		</b-container>
	<!-- </div> -->
</template>
<script type = "text/javascript">
import axios from 'axios';
import moment from 'moment';
import {
	VueEditor,
	Quill
}
from 'vue2-editor';
export default {
	components: {
		VueEditor,
	},
	props: [
		'tmp', 'project', 'looks', 'works', 'windowPrint', 'availableMails',
		'selectedCornty', 'id', 'comments','selectedWorkers',
		'typesForTables', 'workers', 'plan',
		 'person', 'customer', 'selectCustomer', 'selectPerson',
		'selectedDocsList', 'addPdfs', 'makemodalpdf', 'typeDocsList'
	],
	data() {
		return {
      // partx:null,
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
			// unit_type: ['Psch.', '%', 'Stück.', 'Sack.'],
			// calc: ['yes', 'no', 'etc', 'alternative'],
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
    seltable(id, e){
      this.$emit('seltable', id, e)
    },
		// save() {
		// 	this.writecomet();
		// 	this.changeDisable('b', 'gencooment', this.id);
		// 	this.cloudChange = false;
		// 	this.cloudLoad = true;
		// 	this.timeSave = moment().format("DD.MM HH:mm")
		// },
		// writecomet() {
		// 	var newContent = this.$refs['other'].quill.getHTML()
		// 	if (newContent != '<p><br></p>') {
		// 		this.$emit('projectOther', newContent);
		// 		this.updateProject('other', newContent);
		// 	}
		// },
		// checkInEditor(tname) {
		// 	var result
		// 	var sval
		// 	var separator
		// 	var safeEval = require('safe-eval')
		// 	var valueHtml = (this.$refs[tname] != undefined) && (this.$refs[tname].length != 0) ? this.$refs[tname].quill.getHTML() : ''
		// 	if (valueHtml.indexOf('=') != -1) {
		// 		separator = (this.$refs[tname] != undefined) && (this.$refs[tname].length != 0) ? this.$refs[tname].quill.getText() : ''
		// 		separator = separator.replace(/\n/g, ' ')
		// 		separator = separator.substring(0, separator.length - 1)
		// 		separator = separator + ' '
		// 		separator = separator.split('= ')
		// 		separator.splice(-1, 1)
		// 		separator.forEach((val) => {
		// 			var calcval = val.split(' ')[val.split(' ').length - 1]
		// 			if (calcval.search(/[a-zA-z=]/gim) == -1) {
		// 				if (calcval.search(/[-+*)(/]/gim) > -1) {
		// 					if (calcval.search(/[0-9]/gim) > -1) {
		// 						if (/[\d)]/.test(calcval[calcval.length - 1])) {
		// 							var rcalcval = calcval.split(',').join('.')
		// 							try {
		// 								result = this.$options.filters.thousandSeparator(safeEval(rcalcval))
		// 							}
		// 							catch (e) {
		// 								result = '(not valid formula)'
		// 							}
		// 							sval = rcalcval + '=' + result + ' '
		// 							this.$refs[tname].quill.clipboard.dangerouslyPasteHTML(
		// 								valueHtml = valueHtml.replace(calcval + '=', sval)
		// 							)
		// 						}
		// 					}
		// 				}
		// 			}
		// 		})
		// 	}
		// 	this.updateProject('other', valueHtml)
		// },
		selectedDocs(event) {
			this.$emit('selectedDocs', event)
		},
		addPdf() {
			this.$emit('addPdf')
		},
		printPdf() {
			this.$emit('printPdf')
		},
		preview() {
			this.$emit('preview')
		},
		printOffer() {
			this.$emit('printOffer')
		},
		worker() {
			this.$emit('worker')
		},
		hideWindowPrint() {
			this.$emit('hideWindowPrint')
		},
		openWindowPrint() {
			this.$emit('openWindowPrint')
		},
		// getTablesInItem(id) {
		// 	axios.get('/get_tables', {
		// 		params: {
		// 			id: id
		// 		}
		// 	}).then(response => {
		// 		var tables = response.data.filter((v, i) => {
		// 			if (i < (response.data.length - 1)) {
		// 				return v
		// 			}
		// 		});
		// 		this.tax = response.data[(response.data.length - 1)].taxs.tax;
		// 		this.taxDub = response.data[(response.data.length - 1)].taxs.taxDub;
		// 		this.taxP = response.data[(response.data.length - 1)].taxs.taxP;
		// 		this.taxPDub = response.data[(response.data.length - 1)].taxs.taxPDub;
		// 		this.disc = response.data[(response.data.length - 1)].taxs.disc;
		// 		this.discP = response.data[(response.data.length - 1)].taxs.discP;
		// 		this.butDiscPerc = response.data[(response.data.length - 1)].taxs.butDiscPerc;
		// 		this.addtaxColapse = (response.data[(response.data.length - 1)].taxs.addtaxColapse == 'false') ? false : true;
    //     this.partx = tables
		// 		// this.$emit('tabletopartx', tables)
		// 	})
		// },
		// saveCol() {
		// 	this.addtaxColapse = this.addtaxColapse ? false : true
		// 	this.taxPDub = 0,
		// 		this.taxDub = 0,
		// 		this.discOfPercent(),
		// 		this.updateProjectTaxs()
		// },
		// updateProjectTaxs() {
		// 	if (this.tmp.id != null) {
		// 		axios.get('/updateProjectTaxs', {
		// 			params: {
		// 				id: this.tmp.id,
		// 				butDiscPerc: this.butDiscPerc,
		// 				tax: this.tax ? this.tax : '0',
		// 				taxDub: this.taxDub ? this.taxDub : '0',
		// 				taxP: this.taxP ? this.taxP : '0',
		// 				taxPDub: this.taxPDub ? this.taxPDub : '0',
		// 				disc: this.disc ? this.disc : '0',
		// 				discP: this.discP ? this.discP : '0',
		// 				addtaxColapse: (this.addtaxColapse == true) ? 'true' : 'false'
		// 			}
		// 		})
		// 	}
		// },
		// discOfPercent() {
		// 	this.tax = (this.tax == 'NaN,00') ? 0 : this.tax,
		// 		this.taxDub = (this.taxDub == 'NaN,00') ? 0 : this.taxDub
		// 	this.butDiscPerc = (this.butDiscPerc == undefined) ? '%' : this.butDiscPerc
		// 	var tmpDisc, tmpNetto, tmpTax, tmpTax2
		// 	var summa = 0
		// 	this.partx.forEach(function (val) {
		// 		val.parts.part_content.forEach(function (val1) {
		// 			if (val1.status == 'yes') {
		// 				summa += val1.count * val1.price
		// 			}
		// 		})
		// 	})
		// 	if (this.butDiscPerc == '%') {
		// 		var add = 0
		// 		var add2 = 0
		// 		this.partx.forEach((val) => {
		// 			val.parts.part_content.forEach((sval) => {
		// 				if (sval.without == true) {
		// 					if (sval.alttax == true) add2 = add2 + ((sval.count * sval.price / 100) * this.discP)
		// 					if (sval.alttax != true) add = add + ((sval.count * sval.price / 100) * this.discP)
		// 				}
		// 			})
		// 		})
		// 		this.disc = this.$options.filters.thousandSeparator((summa / 100) * this.discP - (add + add2))
		// 		tmpDisc = (summa / 100) * this.discP - (add + add2)
		// 	}
		// 	else {
		// 		this.disc = this.$options.filters.thousandSeparator(this.discP)
		// 		tmpDisc = this.discP
		// 	}
		// 	this.netto = this.$options.filters.thousandSeparator(summa - tmpDisc)
		// 	tmpNetto = summa - tmpDisc
		// 	var addt = 0
		// 	var addt2 = 0
		// 	this.partx.forEach((val) => {
		// 		val.parts.part_content.forEach((sval, index) => {
		// 			if (sval.status == 'yes') {
		// 				if (sval.alttax != true) {
		// 					addt = addt + (sval.count * sval.price)
		// 				}
		// 				else {
		// 					addt2 = addt2 + (sval.count * sval.price)
		// 				}
		// 			}
		// 		})
		// 	})
		// 	if (this.butDiscPerc == '%') {
		// 		addt = (addt - ((addt / 100) * (this.discP))) + add //плюс потери с without
		// 		addt2 = (addt2 - ((addt2 / 100) * (this.discP))) + add2
		// 	}
		// 	if (this.butDiscPerc == 'P') {
		// 		addt = addt - (addt / 100) * (this.discP * 100 / summa)
		// 		addt2 = addt2 - (addt2 / 100) * (this.discP * 100 / summa)
		// 	}
		// 	this.tax = this.$options.filters.thousandSeparator(addt * (this.taxP / 100))
		// 	tmpTax = (addt * (this.taxP / 100))
		// 	this.taxDub = this.$options.filters.thousandSeparator(addt2 * (this.taxPDub / 100))
		// 	tmpTax2 = (addt2 * (this.taxPDub / 100))
		// 	this.brutto = this.$options.filters.thousandSeparator(tmpNetto + tmpTax + tmpTax2)
		// },
		// getPerson() {
		// 	this.$emit('getPerson')
		// },
		// getCustomer() {
		// 	this.$emit('getCustomer')
		// },
		// getCustomerAdress() {
		// 	this.$emit('getCustomerAdress')
		// },
		// getCustomerAdressOne() {
		// 	this.$emit('getCustomerAdressOne')
		// },
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
		// changeDisable(type_operation, fild, id) {
		// 	this.stopDis = (type_operation == 'f')
		// 	axios.get('/changeDisableTable', {
		// 		params: {
		// 			type_operation: type_operation,
		// 			fild: fild,
		// 			id: id,
		// 			'user': this.$security.account['first_name'] + '_' + this.$security.account['second_name']
		// 		}
		// 	})
		// 	if (type_operation == 'f') {
		// 		setTimeout(() => {}, 15000);
		// 	}
		// },
		// updateProject(fild, newData) {
		// 	axios.post('/updateProject', {
		// 		id: this.id,
		// 		date: newData,
		// 		fild: fild
		// 	}).then(response => {
		// 		if (fild == 'other') {
		// 			axios.post('/updateProject', {
		// 				id: this.id,
		// 				date: this.$security.table.account.first_name + '_' + this.$security.table.account.second_name,
		// 				fild: 'user'
		// 			}).then(response => {
		// 				this.cloudLoad = false;
		// 			});
		// 			axios.post('/updateProject', {
		// 				id: this.id,
		// 				date: moment().format("DD.MM HH:mm"),
		// 				fild: 'datacomment'
		// 			});
		// 		}
		// 	})
		// },
	// 	disablefild(fild, id) {
	// 		var result = false
	// 		this.looks.forEach((val) => {
	// 			if (val.rows_id == id) {
	// 				if (val.fild == fild) {
	// 					result = true
	// 				}
	// 			}
	// 		})
	// 		if (this.stopDis == true) result = false
	// 		return result
	// 	},
	// 	disablefildUser(fild, id) {
	// 		var result
	// 		this.looks.forEach((val) => {
	// 			if (val.rows_id == id) {
	// 				if (val.fild == fild) {
	// 					result = val.user
	// 				}
	// 			}
	// 		})
	// 		return result
	// 	},
	// },
  // mounted() {
    // setTimeout(() => {
      // console.log(this.tmp.id)
      // this.getTablesInItem(this.tmp.id)
    // }, 1000);
	// },
	// watch: {
	// 	partx: {
	// 		handler: function (newValue, oldValue) {
	// 			var arr2 = 0
	// 			newValue.forEach((v) => {
	// 				for (var obj in v.parts.checkbox_list.selected) {
	// 					arr2 = arr2 + v.parts.checkbox_list.selected[obj].length
	// 				}
	// 			})
	// 			if (this.selectedLenght != arr2) {
	// 				this.discOfPercent()
	// 			}
	// 			this.selectedLenght = 0
	// 			oldValue.forEach((v) => {
	// 				for (var obj in v.parts.checkbox_list.selected) {
	// 					this.selectedLenght = this.selectedLenght + v.parts.checkbox_list.selected[obj].length
	// 				}
	// 			})
	// 		},
	// 		deep: true,
	// 	},

	},
}
</script>
