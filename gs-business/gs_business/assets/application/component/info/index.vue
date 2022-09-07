<template>
    <div class="gs-business_info">
            <form>
                <input v-on:change="loadInfo"/>
            </form>
          <b-table striped hover :items="items"></b-table>
    </div>
</template>


<script type="text/javascript">
import axios from 'axios';


    export default {
         data () {
            return {
              items: [
              { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
              { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
              { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
              { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
            ]
            }
          },
          methods: {
            loadInfo() {
                this.items = [];
            }
          },

          mounted() {

            axios.get('/info').then(response => {
                this.items = respnose.data
            })
          }
    }
</script>