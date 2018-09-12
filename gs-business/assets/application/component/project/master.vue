<template>
    <container class="container-fluid">
        <container-header>
            <top-menu></top-menu>
        </container-header>
        <container-body>
            <b-card header="Project" footer="Card Footer" class="gs-container">
                <container>
                    <container-header>
                        <b-form style="margin-bottom: 5px">
                            <b-input placeholder="[search]" />
                        </b-form>
                    </container-header>
                    <container-body>
                        <b-table stacked="lg" hover :items="items" :fields="fields" @row-clicked="inItemClick"  class="tableProject" small >
                            <template slot="status_set" slot-scope="data">
                               <b-form inline v-on:click.stop.prevent class="status">
                                    <b-form-select v-model="data.item.status_set" :options="options"/>
                                    <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyle(data.item.status_set)"></i>
                                </b-form>
                            </template>
                            <template slot="invoice" slot-scope="data">
                                    <b-button size="sm" @click.stop="getInvoice(data.item.id)" v-b-modal.invoice variant="outline-secondary" class="mr-1 fas fa-dollar-sign" />
                            </template>
                            <template slot="offer" slot-scope="data">
                                <b-button size="sm" @click.stop="getOffer(data.item.id)" v-b-modal.offer  variant="outline-secondary" class="mr-1 fas fa-hand-holding-usd" />
                            </template>
                        </b-table>
                    </container-body>
                </container>
            </b-card>
        </container-body>
          <b-modal id="offer"  size="lg" title="Offer List" ok-only  centered>

             <b-table hover stacked="sm" :items="offers" :fields="fieldsOffer" @row-clicked="inOfferClick"  class="tableProject" small >
                    <template slot="status_set" slot-scope="offer">
                        <b-row>
                            <b-col cols="6">  {{ offer.item.status_set }}  </b-col>   <b-col cols="1"><i class="fas fa-circle fa-w-16 fa-2x " :style="computeStyleOffer(offer.item.status_set)"></i></b-col>
                   </b-row>
                    </template>
            </b-table>
           </b-modal>
         <b-modal id="invoice" size="lg" title="Invoice List" ok-only  centered>
            <b-table hover  stacked="sm" :items="invoices" :fields="fieldsInvoice" @row-clicked="inItemClick"  class="tableProject" small >
                    <template slot="status_set" slot-scope="invoice">
                        <b-row>
                            <b-col cols="6">  {{ invoice.item.status_set }}  </b-col>   <b-col cols="1"><i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyleInvoice(invoice.item.status_set)"></i></b-col>
                   </b-row>
                    </template>
            </b-table>
          </b-modal>
    </container>
</template>
<script>
import axios from 'axios';
export default {
    data() {
        return {
            fields: {
                project_number: {
                label: 'Project No.',
                sortable: true,
                class: 'number'
                },
                date: {
                label: 'Start',
                sortable: true,
                class: 'number'
                },
                street: {
                label: 'Street',
                sortable: true,
                class: 'number'
                },
                zip: {
                label: 'ZIP',
                sortable: true,
                class: 'number'
                },
                city: {
                label: 'City',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                class: 'other'
                },
                offer: {
                label: 'Offer',
                class: 'number'
                },
                invoice: {
                label: 'Invoice',
                class: 'number'
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'number'
                }
                },
            fieldsOffer: {
                offer_number: {
                label: 'Offer No.',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                class: 'other'
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status'
                }
                },
            fieldsInvoice: {
                invoice_number: {
                label: 'Invoice No.',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true,
                class: 'other'
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status'
                }
                },
               options: [
                         { value: 'Open', text: 'Open' },
                         { value: 'Done', text: 'Done'},
                         { value: 'Invoice', text:'Invoice' },
                         { value: 'Desiccation', text:'Desiccation' },
                         { value: 'Leakage_Detection', text:'Leakage Detection' },
                         { value: 'Restoration', text:'Restoration'}
               ],
            items: [],
            ddd: 0,
            idSpan: 0,
            offers: null,
            invoices: null
        }
    },
    methods: {
        inItemClick(item, index, event) {
            this.$router.push({
                path: `/project/detail/${item.id}`
            })
        },
        inOfferClick(item, index, event) {
            this.$router.push({
                path: `/project/detail/${item.id}/offer/${offer.id}`
            })
        },
    getOffer(project_id){
        axios.get('/offer', {params: {id: project_id}}).then(response => {
               this.offers = response.data
           })
        },
    getInvoice(project_id){
        axios.get('/invoice', {params: {id: project_id}}).then(response => {
               this.invoices = response.data
         })
        },
        computeStyle(value) {
            switch (value) {
                case 'Open': return {'color': '#F5DEB3'};
                case 'Done': return {'color': 'green'};
                case 'Invoice': return {'color':'orange'};
                case 'Desiccation': return {'color':'grey'};
                case 'Leakage_Detection': return {'color':'red'};
                case 'Restoration': return {'color':'blue'};
            }
        },
        computeStyleOffer(value) {
            switch (value) {
                case 'Not Finished': return {'color': 'grey'};
                case 'Sent': return {'color': 'orange'};
                case 'Denied': return {'color':'red'};
                case 'Agreement': return {'color':'green'};
            }
        },
        computeStyleInvoice(value) {
            switch (value) {
                case 'Paid': return {'color': 'green'};
                case 'Not Paid': return {'color': 'gray'};
                case 'Overdue': return {'color':'red'};
                case 'Partially Paid': return {'color':'orange'};
            }
        }
},
      mounted(){
        axios.get('/projects').then(response => {
               this.items = response.data
         })
        }
    }
</script>