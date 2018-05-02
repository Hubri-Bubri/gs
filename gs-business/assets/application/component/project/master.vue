<template>
    <container class="container-fluid">
        <container-header>
            <top-menu></top-menu>
        </container-header>
        <container-body>
            <b-card header="Project" class="gs-container">
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
const items = [
    { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
    { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
    { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
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