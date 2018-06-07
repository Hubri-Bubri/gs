<template>
    <container>
        <b-modal size="lg" centered  ok-only id="map" title="Track">
          <b-embed type="iframe" aspect="16by9"
            :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+project.street"></b-embed>
        </b-modal>
        <container-header class="container-fluid">
            <top-menu></top-menu>
        </container-header>
        <container-body class="container-fluid">
          <b-card-group deck>
            <b-card no-body class="gs-container">
              <b-tabs card>
                <b-tab title="Tab 1">
                  <container>
                    <container-body>
                      <b-container fluid>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="project-number">Project Number:</label></b-col>
                          <b-col sm="9">
                            <b-form-input id="project-number" :state="null" disabled type="text"
                            v-model="project.number" placeholder="Enter project number"></b-form-input>
                          </b-col>
                        </b-row>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="date">Date:</label></b-col>
                          <b-col sm="9">
                            <b-form-input id="date" :state="null" type="date"
                            v-model="project.date" placeholder="Enter date"></b-form-input>
                          </b-col>
                        </b-row>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="editor">Editor:</label></b-col>
                          <b-col sm="9">
                            <b-form-input id="editor" :state="null" type="text"
                            v-model="project.editor" placeholder="Enter editor name"></b-form-input>
                          </b-col>
                        </b-row>
                        <hr>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="street">Street:</label></b-col>
                          <b-col sm="9">
                            <b-input-group left="@" class="mb-2 mr-sm-2 mb-sm-0">
                              <b-form-input id="street" :state="null" type="text"
                              v-model="project.street" placeholder="Enter street"></b-form-input>
                              <b-button v-b-modal.map>G</b-button>
                            </b-input-group>
                          </b-col>
                        </b-row>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="city">City:</label></b-col>
                          <b-col sm="9">
                            <b-form-input id="city" :state="null" type="text"
                            v-model="project.city" placeholder="Enter city"></b-form-input>
                          </b-col>
                        </b-row>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="zip-code">Zip code:</label></b-col>
                          <b-col sm="9">
                            <b-form-input id="zip-code" :state="null" type="text"
                            v-model="project.zip" placeholder="Enter zip code"></b-form-input>
                          </b-col>
                        </b-row>
                        <hr>
                        <b-row class="my-1">
                          <b-col sm="3"><label for="customer">Customer:</label></b-col>
                          <b-col sm="9">
                            <v-select taggable label="name" v-model="customer" :options="area"></v-select>
                          </b-col>
                        </b-row>
                        <b-row class="my-1" v-if="availablePersons">
                          <b-col sm="3"><label for="contact-person">Contact person:</label></b-col>
                          <b-col sm="9">
                            <v-select taggable v-model="person" :options="availablePersons"></v-select>
                          </b-col>
                        </b-row>
                        <b-row class="my-1" v-if="person">
                          <b-col sm="3"><label for="mail">E-mail:</label></b-col>
                          <b-col sm="9">
                             <b-button :href="'mailto:'+person.mail">{{person.mail}}</b-button>
                          </b-col>
                        </b-row>
                        <b-row class="my-1" v-if="person">
                          <b-col sm="3"><label for="mail">Phone:</label></b-col>
                          <b-col sm="9">
                            <b-button :href="'cal:'+person.tel">{{person.tel}}</b-button>
                          </b-col>
                        </b-row>
                         <b-row class="my-1" v-if="person">
                          <b-col sm="3"><label for="mail">Fax:</label></b-col>
                          <b-col sm="9">
                            <b-button :href="'cal:'+person.fax">{{person.fax}}</b-button>
                          </b-col>
                        </b-row>
                      </b-container>                      
                    </container-body>
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

            <b-card no-body class="gs-container">
               <b-tabs card>
                  <b-tab title="Tab 3">
                    <container>
                      <container-header>1</container-header>
                      <container-body>
                        <b-table striped hover :items="items"></b-table>
                      </container-body>
                      <container-footer>3</container-footer>
                    </container>
                  </b-tab>
                  <b-tab title="Tab 4">
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
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' },
    { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
];
export default {
    props: {
        id: String
    },

    data() {
        return {
          items: items,
          project: {number: '777-2018', editor: 'Alexander Baer', date: '2018-02-01',
          street: 'Frankfurter Strasse 39_0312', city: 'Darmstadt', zip: 'D-64293'},

          customer: null,
          person: null,

          area: [
            {
              name: 'Bauverein',
              persons: [{ label:'Sven Wolthoff', mail:'Sven@Wolth-off', tel:'+49 (999) 99-99-99', fax:'+49 (999) 99-99-99'},
              {label:'Michael Wernity', mail:'Michael@Wernity', tel:'+49 (888) 88-88-88'},
              {label:'Sven Schulmeier', mail:'Sven@Schulmeier', tel:'+49 (777) 77-77-77'}]
            },
            {
              name: 'ABG',
              persons: ['Sommer', 'Herbst', 'Winter']
            },
            {
              name: 'Entega',
               persons: ['Alexander Ploety', 'Norbert Staedter', 'Johen Bendt']
            },
          ]
        }
      },
      computed: {
        availablePersons() {
        return this.customer ? this.customer.persons : false
        }
      },
      mounted(){
        console.log(this.id);
      }
}
</script>
