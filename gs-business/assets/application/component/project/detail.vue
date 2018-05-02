<template>
    <container>
        <container-header class="container-fluid">
            <top-menu></top-menu>
        </container-header>

        <container-body class="container-fluid">
            <b-card-group deck>
                <b-card header="featured"
                        header-tag="header"
                        footer="Card Footer"
                        footer-tag="footer"
                        title="Title"
                        class="gs-container">

                    <p class="card-text">Header and footers using props.</p>
                    
                </b-card>

                <b-card no-body class="gs-container">
                  <b-tabs card>
                    <b-tab title="Tab 1">
                        <container>
                            <container-header>1</container-header>
                            <container-body>
                                <b-table striped hover :items="items"></b-table>
                            </container-body>
                            <container-footer>3</container-footer>
                        </container>
                    </b-tab>
                    <b-tab title="Tab 2">
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                      Tab Contents 2<br/>
                    </b-tab>
                  </b-tabs>
                </b-card>
            </b-card-group>
        </container-body>
    </container>
</template>


<script type="text/javascript">
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
];

export default {
    props: {
        id: String
    },

    data() {
        return {
            items: items
        }
    },

    mounted(){
        console.log(this.id);
    }
}
</script>
