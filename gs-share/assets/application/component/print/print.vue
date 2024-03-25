<template>
          <b-modal size="lg" centered ok-only no-close-on-esc no-close-on-backdrop hide-header-close  :visible="printModal">
         <div slot="modal-title" class="w-100">
            <div>{{$t('print.print')}}</div>
         </div>
                   <b-container v-show="printBusy">
                <b-row align-v="center" class="text-center" style="width:100%;height:550px;">
                    <b-col>
                <strong class="text-info">
                <b-spinner class="align-middle"  ></b-spinner>
                    {{$t('projects.loading')}}...
                </strong>
                    </b-col>
                </b-row>
                </b-container> 
                
         <iframe type="iframe" style="width:100%;height:550px;" name="myIframe"  v-show="printBusy==false" :src="(src=='#')?null:src"></iframe>
       
         <div slot="modal-footer" class="w-100">
            <b-row align-v="start">
               <b-col cols="6" align-self="end">
                  <b-form inline  v-if="type!='Devices'">
                     <b-col cols="4">{{$t('print.dateOfPrint')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;"
                           size="sm" type="date" :value="today" @change="today=$event;printBusy=true;makePdf();" />
                     </b-col>
                  </b-form>
                   <b-form inline v-if="type=='SUB' || type=='Invoices'">
                     <b-col cols="4">{{$t('print.startWorks')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           :value="stworks" @change="stworks=$event;printBusy=true;makePdf();" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="type!='Devices' & type!='Damage' & type!='Reports'">
                     <b-col cols="4">{{$t('print.endWorks')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           :value="fworks" @change="fworks=$event;printBusy=true;makePdf();" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="type=='Damage'">
                     <b-col cols="4">{{$t('print.inspectDate')}}</b-col>
                     <b-col cols="8">
                        <b-input style="color:#000; padding-left: 5px !important; font-size: 16px;width:172px;" size="sm" type="date"
                           :value="dateForInspect"  @change="dateForInspect=$event;printBusy=true;makePdf();" />
                     </b-col>
                  </b-form>
                  <b-form inline v-if="type=='Damage'">
                     <b-col cols="4">{{$t('print.inspectBy')}}</b-col>
                     <b-col cols="8">
            <b-dropdown
                size="sm"
                :text="byForInspect?byForInspect:'---'"
                variant="link"
                no-caret
                class="maxHeight outUnderline">
                <b-dropdown-item-button
                  @click="byForInspect='---';printBusy=true;makePdf();"
                  >---</b-dropdown-item-button>
                <b-dropdown-item-button
                  :key="worker"
                  v-for="worker in workers"
                  @click="byForInspect=worker;printBusy=true;makePdf();">
                  {{worker}}
                </b-dropdown-item-button>
            </b-dropdown>


                     </b-col>
                  </b-form>

                  <b-button-group size="sm" style="padding-top: 15px !important;padding-left: 15px !important;">
                    <b-button variant="primary" @click="(printBusy=true);printModal=false;" >
                        {{$t('print.close')}} 
                     </b-button>
                     <b-button variant="primary" @click="printPdf" >
                        {{$t('print.print')}} 
                     </b-button>
                     <b-button variant="primary" @click="addPdf()">
                        {{ addDocument?$t('projectDetail.docInProgress'):$t('projectDetail.add') }}
                     </b-button>
                     <b-button variant="primary" @click="addPdfSep()" v-show="type=='Devices'">
                        {{$t('print.addSeparated')}} 
                     </b-button>                     
                  </b-button-group>
               </b-col>
               <b-col cols="6">
                   <b-form-select buttons text-field="name" value-field="id" button-variant="outline-primary" 
                     :options="typeDocsList" @change="selectedDocs($event)" :value="selectedDocsList"
                     multiple :select-size="(type=='Damage')?7:(type=='Devices')?3:5">
                  </b-form-select>
               </b-col>
            </b-row>
         </div>
      </b-modal>
</template>
<script>
import axios from 'axios';
export default {
    props: [
    'tmp',
    'pid',
    'workers'
    ],
    data() {
        return {
        type:null,
        printModal:false,
        src:'#',
        typeDocsList:[],
        selectedDocsList:[],
        printBusy:true,
        addDocument:false,
        forPreview:null,
      //   addPdfs:false,
        today: (new Date().getFullYear() + '-' +
                    (((new Date().getFullYear() + '-' + (new Date().getMonth() + 1)).length == 6) ? '0' + (new Date().getMonth() + 1) : (new Date().getMonth() + 1))) +
                '-' +
                (((new Date().getFullYear() + '-' + (new Date().getDate())).length == 6) ? '0' + (new Date().getDate()) : (new Date().getDate())),
        stworks: null,
        fworks: null,
            dateForInspect: '',
            byForInspect: '---',
          }
    },
    methods: {
    makePdf(){
      //   this.forPreview = Math.ceil(Math.random()*1000000);
      //   this.printModal=true;
        this.src = '/pdf?addPdf=false&forPreview='+this.forPreview+'&pid='+this.pid+'&itemId='+this.tmp.id+'&type='+this.type+'&today='+this.today+'&stworks='+this.stworks+'&fworks='+this.fworks+
        '&dateForInspect='+this.dateForInspect+'&byForInspect='+this.byForInspect+'&selectedDocsList='+this.selectedDocsList.join();
    },
      // loadFrame(){
      //   if (this.addDocument)
      //     {
      //       // this.printModal=false;
      //       // this.addPdfs=false;
      //       this.addDocument=false;
      //       this.selectedDocsList = [];
      //     }
      // },
        previewPDFForm(type){

            var requestForType = (type=='StandingOrder')?'Orders':type
            this.type = requestForType
            this.forPreview = Math.ceil(Math.random()*1000000)
            this.printModal=true;
            axios.get('/get_type_docs', {
				params: {
					type: requestForType
				}
			}).then(response => {
				this.typeDocsList = response.data
				if (requestForType == 'Offers') {
					this.selectedDocsList = ['31']
				}
				if (requestForType == 'Invoices') {
					this.selectedDocsList = ['14']
				}
				if (requestForType == 'Orders') {
					this.selectedDocsList = ['38']
				}
				if (requestForType == 'SUB') {
					this.selectedDocsList = ['41']
				}
				if (requestForType == 'Devices') {
					this.selectedDocsList = ['45']
				}
				if (requestForType == 'Damage') {
					this.selectedDocsList = ['48']
				}
				if (requestForType == 'Reports') {
					this.selectedDocsList = ['50']
				}

                this.src = '/pdf?addPdf=false&forPreview='+this.forPreview+'&pid='+this.pid+'&itemId='+this.tmp.id+'&type='+this.type+'&today='+this.today+'&stworks='+this.stworks+'&fworks='+this.fworks+
                '&dateForInspect='+this.dateForInspect+'&byForInspect='+this.byForInspect+'&selectedDocsList='+this.selectedDocsList.join();
                
			})
        },
        selectedDocs(event){
          this.printBusy=true;
			this.selectedDocsList = event
            this.makePdf()
        },
		addPdfSep() {
         this.src='#'
			// this.addPdfs = 'separator'
         this.printModal=false
         axios.get('/pdf', {
				params: {
					addPdf:'separator',
               forPreview:this.forPreview,
               pid:this.pid,
               itemId:this.tmp.id,
               type:this.type,
               today:this.today,
               stworks:this.stworks?this.stworks:'null',
               fworks:this.fworks?this.fworks:'null',
               dateForInspect:this.dateForInspect?this.dateForInspect:'',
               byForInspect:this.byForInspect?this.byForInspect:'',
               selectedDocsList:this.selectedDocsList.join()
				}
			})
         // this.addDocument=true;
         // this.makePdf();
		},
		printPdf() {
				window.frames["myIframe"].focus();
				window.frames["myIframe"].print();
		},
      addPdf() {
    
         // this.addDocument=true;
         this.src='#'
         // this.addPdfs=true
         this.printModal=false


         axios.get('/pdf', {
				params: {
					addPdf:'true',
               forPreview:this.forPreview,
               pid:this.pid,
               itemId:this.tmp.id,
               type:this.type,
               today:this.today,
               stworks:this.stworks?this.stworks:'null',
               fworks:this.fworks?this.fworks:'null',
               dateForInspect:this.dateForInspect?this.dateForInspect:'',
               byForInspect:this.byForInspect?this.byForInspect:'',
               selectedDocsList:this.selectedDocsList.join()
				}
			})

     },
   },
    mounted(){
        this.$options.sockets.onmessage = (data) => {
        var delimetr = data.data.split(':')
        if (delimetr[0] == 'preview') {
            if (delimetr[1] == this.forPreview) this.printBusy=false
        }
        if (delimetr[0] == 'print') {
            if (delimetr[1] == this.forPreview) this.$emit('wasmade', delimetr[2], delimetr[3])
        }
    }
}
}
</script>