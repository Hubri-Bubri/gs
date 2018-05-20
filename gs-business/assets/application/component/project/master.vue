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
                        <b-table striped hover :items="items" @row-clicked="inItemClick"></b-table>
                     </container-body>
                </container>
            </b-card>
        </container-body>
    </container>
</template>


<script>
//const sel ='<select></select>';
const items = [
    { 'Project number': '777-2018', 'type': 'L','Street': 'In den Leppsteinswiesen 8',
    'ZIP': 'D-64293', 'City': 'Berlin', 'Calculation':'25.02.2018 send post',
    'Release of costs':'no', 'Others':'Wir waren Vorort und haben nichts festgestellen können',
    'Status':'open' },
     { 'Project number': '777-2018', 'type': 'L','Street': 'In den Leppsteinswiesen 8',
    'ZIP': 'D-64293', 'City': 'Berlin', 'Calculation':'25.02.2018 send post',
    'Release of costs':'no', 'Others':'Wir waren Vorort und haben nichts festgestellen können',
    'Status':'open' },
     { 'Project number': '777-2018', 'type': 'L','Street': 'In den Leppsteinswiesen 8',
    'ZIP': 'D-64293', 'City': 'Berlin', 'Calculation':'25.02.2018 send post',
    'Release of costs':'no', 'Others':'Wir waren Vorort und haben nichts festgestellen können',
    'Status':'open' },
     { 'Project number': '777-2018', 'type': 'L','Street': 'In den Leppsteinswiesen 8',
    'ZIP': 'D-64293', 'City': 'Berlin', 'Calculation':'25.02.2018 send post',
    'Release of costs':'no', 'Others':'Wir waren Vorort und haben nichts festgestellen können',
    'Status':'open' },
     { 'Project number': '777-2018', 'type': 'L','Street': 'In den Leppsteinswiesen 8',
    'ZIP': 'D-64293', 'City': 'Berlin', 'Calculation':'25.02.2018 send post',
    'Release of costs':'no', 'Others':'Wir waren Vorort und haben nichts festgestellen können',
    'Status':'open' },
]

export default {
    
    data () {
        return {
            items: items
        }
    },

    methods: {
        inItemClick(item, index, event) {
            this.$router.push({
                path: `/project/detail/${item.age}`
            });
        }
    }
}
</script>