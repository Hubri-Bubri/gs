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
                        <b-table striped hover :items="items" :fields="fields" @row-clicked="inItemClick" class="tableProject">
                            <template slot="status" slot-scope="data">
                                <b-form inline v-on:click.stop.prevent>
                                    <b-form-select v-model="data.item.status_set" :options="options"/>
                                    <i class="fas fa-circle fa-w-16 fa-2x" :style="computeStyle(data.item.status_set)"></i>
                                </b-form>
                            </template>
                        </b-table>
                    </container-body>
                </container>
            </b-card>
        </container-body>
    </container>
</template>
<script>

const items = [{
        'project_number': '0001-2016', 
        'type': 'L',
        'street': 'In den Leppsteinswiesen 8',
        'zip': 'D-64293',
        'city': 'Berlin',
        'start': '25.02.2018',
        'others': 'Wir waren Vorort und haben nichts festgestellen können',
        'status_set': 'Open',
        'id': '1'
    },
    {
        'project_number': '777-2018',
        'type': 'L',
        'street': 'In den Leppsteinswiesen 8',
        'zip': 'D-64293',
        'city': 'Berlin',
        'start': '25.02.2018',
        'others': 'Wir waren Vorort und haben nichts festgestellen können',
        'status_set': 'Done',
        'id': '2'
    },
    {
        'project_number': '777-2018',
        'type': 'L',
        'street': 'In den Leppsteinswiesen 8',
        'zip': 'D-64293',
        'city': 'Berlin',
        'start': '25.02.2018',
        'others': 'Wir waren Vorort und haben nichts festgestellen können',
        'status_set': 'Invoice',
        'id': '3'
    },
    {
        'project_number': '777-2018',
        'type': 'L',
        'street': 'In den Leppsteinswiesen 8',
        'zip': 'D-64293',
        'city': 'Berlin',
        'start': '25.02.2018',
        'others': 'Wir waren Vorort und haben nichts festgestellen können',
        'status_set': 'Desiccation',
        'id': '4'
    },
    {
        'project_number': '777-2018',
        'type': 'L',
        'street': 'In den Leppsteinswiesen 8',
        'zip': 'D-64293',
        'city': 'Berlin',
        'start': '25.02.2018',
        'others': 'Wir waren Vorort und haben nichts festgestellen können',
        'status_set': 'Leakage_Detection',
        'id': '5'
    },
]

export default {

    data() {
        return {
            fields: {
                project_number: {
                label: 'Project Number',
                sortable: true
                },
                start: {
                label: 'Start',
                sortable: true
                },
                type: {
                label: 'Type',
                sortable: true
                },
                street: {
                label: 'Street',
                sortable: true
                },
                zip: {
                label: 'ZIP',
                sortable: true
                },
                city: {
                label: 'City',
                sortable: true
                },
                others: {
                label: 'Others',
                sortable: true
                },
                status: {
                label: 'Status',
                sortable: true
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
            items: items,
            idSpan: 0
        }
    },

    methods: {
        inItemClick(item, index, event) {
            this.$router.push({
                path: `/project/detail/${item.id}`
            });
        },

        computeStyle(value) {
            switch (value) {
                case 'Open': return {'color': 'black'};
                case 'Done': return {'color': 'green'};
                case 'Invoice': return {'color':'orange'};
                case 'Desiccation': return {'color':'grey'};
                case 'Leakage_Detection': return {'color':'red'};
                case 'Restoration': return {'color':'blue'};
            }
        },

        mounted() { 
            console.log('121');
            changeSelect('Done', '1');
    //        axiox.get('/projects', ).then(function(response) {

      //      }), 
            

        }
    }
}
</script>
