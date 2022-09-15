<template>
    <container class="container-fluid">
        <container-header>
            <top-menu></top-menu>
        </container-header>
        <container-body>
            <b-card :header="project.content" class="gs-container">
                <container>
                    <container-header>
                        <!-- <b-input-group style="margin-bottom: 5px"> -->
                            <b-input-group><b-input placeholder="[search]" v-model="keyword" />
                            <template #append>
<b-dropdown text="options" variant="outline-secondary">

<b-form-checkbox-group
  button-variant="outline-secondary"
   v-model="selected"
  stacked
  :options="types_for_tables_opt"
  @change="keywordChange($event)"
  buttons />


    </b-dropdown>
  </template>
                           </b-input-group>
                           <!-- </b-input-group> -->

                       
                    </container-header>
                    <container-body>
           <!-- <v-infinite-scroll :loading="loading" @bottom="nextPage" :offset='20' style="max-height: 80vh; overflow-y: scroll;"> -->
                        <b-table stacked="lg" hover :items="items_search" :fields="fields" @row-clicked="inItemClick"  class="tableProject" small busy.sync="isBusy">
                               <template slot="id" slot-scope="data">
                                  {{rpeNumber(data.item.id)}}-{{data.item.project_number_year}}
                                </template>
                                <template slot="status_set" slot-scope="data">
                                   <b-form inline v-on:click.stop.prevent>
                                      <b-form-select class="w-100" v-model="data.item.status_set" @change="updateWork($event, data.item.id)">
                                           <option v-for="opt in options" >{{opt.text}}</option>
                                       </b-form-select>
                                   </b-form>
                                </template>
                                <template slot="other" slot-scope="data">
                                  <div class="text-container">
                                <span  class="text-content" v-html="firstRos(data.item.other, '', '', 'h')" :title="firstRos(data.item.other, data.item.user?'['+data.item.user+' ':'', data.item.datacomment?data.item.datacomment+']':'', 't')" />
                              </div>
                             <!--    <vue-editor class="modEdit"
                                     :value="firstRos(data.item.other)" 
                                     >
                                  </vue-editor> -->
                              </template>
                             <template slot="street1" slot-scope="data">
                                  <div class="text-container">
                                <span  class="text-content"> {{data.item.street1}}</span>
                              </div>
                              </template>
                             <template slot="city1" slot-scope="data">
                                  <div class="text-container">
                                <span  class="text-content"> {{data.item.city1}}</span>
                              </div>
                              </template>
                              <template slot="date" slot-scope="data">
                                {{data.item.date | dateInverse}}
                              </template>
                                <template slot="invoice" slot-scope="data" >
                                  <b-button size="sm" @click.stop="getOffer(data.item.id)" v-b-modal.invoice variant="outline-secondary" class="mr-1 fas fa-dollar-sign" />
                                </template>

                        <!--         <template slot="offer" slot-scope="data">
                                    <b-button size="sm" @click.stop="data.toggleDetails" variant="outline-secondary"  class="mr-1 fas fa-info" />
                                </template> -->


                            <template slot="row-details" slot-scope="data">
                                <b-row>
                                    <b-col v-html="data.item.other" class="pWOutMargin"></b-col>
                                </b-row>
                            </template>

     </b-table>
       <!-- </v-infinite-scroll> -->
                    </container-body>
                </container>
                <b-card-footer>
                  <b-button @click="addProject" variant="outline-secondary">Add Project</b-button>
                  <!-- <b-button @click="addProject">Add Project</b-button> -->
                </b-card-footer>
            </b-card>
        </container-body>
  <b-modal id="invoice" size="lg" title="List" ok-only  centered>
    <div v-for="name in types_for_tables">
                                   {{name.type}}   
                                    <b-table class="tableProject" striped hover :items="getItems(name.type)" :fields="fieldsTable">
                                        <template slot="number" slot-scope="it">
                                             <b-link @click.stop="findRow(it.item.number, name.type)"
                                             v-if="it.item.number.split(' ')[1]">{{ it.item.number.split(' ')[0] }}</b-link>
                                             <div v-else>{{ it.item.number.split(' ')[0] }}</div>
                                        </template>

                                        <template slot="delete" slot-scope="it">
                                            <b-col align-self="center">
                                                <b-link @click="offerDel(it.item.id)" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                            </b-col>
                                        </template>

                                      <template slot="status_set" slot-scope="it" >
                                          <line-chart :datas="dataCharts(it.item)" v-if="name.type=='Invoices'"
                                          :width="150"  :height="20" style="margin-left: -15px;">
                                          </line-chart>
                                          <b-form inline v-else>
                                                <b-form-select v-model="it.item.status_set" @change="updateItem($event, name.type, it.item.id)"
                                                class="w-100" :style="computeStyleOfferM(it.item.status_set)">
                                                  <option v-for="opt in options" :style="computeStyleOfferM(opt.text)">
                                                  {{opt.text}}
                                                  </option>
                                                </b-form-select>
                                            </b-form>
                                      </template>
                                    </b-table>
                                  </div>
          </b-modal>

                                                <b-modal id="addProjectWithDate" ref="addProjectWithDate"  size="md" title="Data Of Project" centered>
                                                  <b-form-group horizontal :label-cols="4" label="Country:" >
                                                     <b-select  selected="Germany" value-field="code" text-field="name" v-model="selectedCornty"  :options="countries" />
                                                </b-form-group>
                                                <br>
                                                <b-form-group horizontal :label-cols="4" label="Zip code:" >
                                                    <b-form-input  :state="null" type="text" v-model="zip" @input="searchZip($event)" placeholder="Enter zip code"   />
                                                </b-form-group>
                                                 <br>
                                                 <b-form-group horizontal :label-cols="4" label="Area:" >
                                                    <b-form-input  :state="null" type="text" v-model="area"  placeholder="Enter Area"/>
                                                </b-form-group>

                                                
                                           
                                                <br>
                                          
                                                <b-form-group horizontal :label-cols="4" label="City:" >
                                                    <b-form-input  :state="null" type="text"  v-model="city" placeholder="Enter city"   />
                                                </b-form-group>
                                             <br>

                                                   <b-form-group horizontal :label-cols="4"  label="Street:">
                                                    <b-input-group>
                                                        <b-form-input :state="null" v-model="street" type="text" placeholder="Enter street" />
                                                        <b-button v-b-modal.map variant="outline-secondary"  size="sm">
                                                          <i class="fa fa-map-marker" aria-hidden="true"></i>
                                                        </b-button>
                                                    </b-input-group>
                                                   
                                                </b-form-group>
                                            
<template slot="modal-footer">
                    <b-button type="submit" variant="outline-primary" @click="createProject">
                        OK
                    </b-button>
                </template>
          </b-modal>
           <b-modal size="lg" centered ok-only id="map" title="Track">
            <b-embed type="iframe" aspect="16by9" :src="'https://www.google.com/maps/embed/v1/directions?key=AIzaSyBFTr5-GCSd0rT-euE1Uarf64eF6mZVK9k&'+
            'origin=In+den+Leppsteinswiesen+8,+64380+Roßdorf&'+
            'destination='+selectedCornty.name+' '+area+' '+street">
            </b-embed>
                    <template slot="modal-footer">
                    <b-button type="submit" variant="primary" v-b-modal.addProjectWithDate>
                        OK
                    </b-button>
                </template>
        </b-modal>
    </container>
</template>
<script>
import {VueEditor, Quill} from 'vue2-editor';
import axios from 'axios';
export default {
    components: {
        VueEditor
    },
    data() {
        return {
          project:{contetn:'Projcet'},
          old_done: '01',
          area: null,
          selectedCornty: 'DE',
            countries:[ 
  {name: 'Afghanistan', code: 'AF'}, 
  {name: 'Åland Islands', code: 'AX'}, 
  {name: 'Albania', code: 'AL'}, 
  {name: 'Algeria', code: 'DZ'}, 
  {name: 'American Samoa', code: 'AS'}, 
  {name: 'AndorrA', code: 'AD'}, 
  {name: 'Angola', code: 'AO'}, 
  {name: 'Anguilla', code: 'AI'}, 
  {name: 'Antarctica', code: 'AQ'}, 
  {name: 'Antigua and Barbuda', code: 'AG'}, 
  {name: 'Argentina', code: 'AR'}, 
  {name: 'Armenia', code: 'AM'}, 
  {name: 'Aruba', code: 'AW'}, 
  {name: 'Australia', code: 'AU'}, 
  {name: 'Austria', code: 'AT'}, 
  {name: 'Azerbaijan', code: 'AZ'}, 
  {name: 'Bahamas', code: 'BS'}, 
  {name: 'Bahrain', code: 'BH'}, 
  {name: 'Bangladesh', code: 'BD'}, 
  {name: 'Barbados', code: 'BB'}, 
  {name: 'Belarus', code: 'BY'}, 
  {name: 'Belgium', code: 'BE'}, 
  {name: 'Belize', code: 'BZ'}, 
  {name: 'Benin', code: 'BJ'}, 
  {name: 'Bermuda', code: 'BM'}, 
  {name: 'Bhutan', code: 'BT'}, 
  {name: 'Bolivia', code: 'BO'}, 
  {name: 'Bosnia and Herzegovina', code: 'BA'}, 
  {name: 'Botswana', code: 'BW'}, 
  {name: 'Bouvet Island', code: 'BV'}, 
  {name: 'Brazil', code: 'BR'}, 
  {name: 'British Indian Ocean Territory', code: 'IO'}, 
  {name: 'Brunei Darussalam', code: 'BN'}, 
  {name: 'Bulgaria', code: 'BG'}, 
  {name: 'Burkina Faso', code: 'BF'}, 
  {name: 'Burundi', code: 'BI'}, 
  {name: 'Cambodia', code: 'KH'}, 
  {name: 'Cameroon', code: 'CM'}, 
  {name: 'Canada', code: 'CA'}, 
  {name: 'Cape Verde', code: 'CV'}, 
  {name: 'Cayman Islands', code: 'KY'}, 
  {name: 'Central African Republic', code: 'CF'}, 
  {name: 'Chad', code: 'TD'}, 
  {name: 'Chile', code: 'CL'}, 
  {name: 'China', code: 'CN'}, 
  {name: 'Christmas Island', code: 'CX'}, 
  {name: 'Cocos (Keeling) Islands', code: 'CC'}, 
  {name: 'Colombia', code: 'CO'}, 
  {name: 'Comoros', code: 'KM'}, 
  {name: 'Congo', code: 'CG'}, 
  {name: 'Congo, The Democratic Republic of the', code: 'CD'}, 
  {name: 'Cook Islands', code: 'CK'}, 
  {name: 'Costa Rica', code: 'CR'}, 
  {name: 'Cote D\'Ivoire', code: 'CI'}, 
  {name: 'Croatia', code: 'HR'}, 
  {name: 'Cuba', code: 'CU'}, 
  {name: 'Cyprus', code: 'CY'}, 
  {name: 'Czech Republic', code: 'CZ'}, 
  {name: 'Denmark', code: 'DK'}, 
  {name: 'Djibouti', code: 'DJ'}, 
  {name: 'Dominica', code: 'DM'}, 
  {name: 'Dominican Republic', code: 'DO'}, 
  {name: 'Ecuador', code: 'EC'}, 
  {name: 'Egypt', code: 'EG'}, 
  {name: 'El Salvador', code: 'SV'}, 
  {name: 'Equatorial Guinea', code: 'GQ'}, 
  {name: 'Eritrea', code: 'ER'}, 
  {name: 'Estonia', code: 'EE'}, 
  {name: 'Ethiopia', code: 'ET'}, 
  {name: 'Falkland Islands (Malvinas)', code: 'FK'}, 
  {name: 'Faroe Islands', code: 'FO'}, 
  {name: 'Fiji', code: 'FJ'}, 
  {name: 'Finland', code: 'FI'}, 
  {name: 'France', code: 'FR'}, 
  {name: 'French Guiana', code: 'GF'}, 
  {name: 'French Polynesia', code: 'PF'}, 
  {name: 'French Southern Territories', code: 'TF'}, 
  {name: 'Gabon', code: 'GA'}, 
  {name: 'Gambia', code: 'GM'}, 
  {name: 'Georgia', code: 'GE'}, 
  {name: 'Germany', code: 'DE'}, 
  {name: 'Ghana', code: 'GH'}, 
  {name: 'Gibraltar', code: 'GI'}, 
  {name: 'Greece', code: 'GR'}, 
  {name: 'Greenland', code: 'GL'}, 
  {name: 'Grenada', code: 'GD'}, 
  {name: 'Guadeloupe', code: 'GP'}, 
  {name: 'Guam', code: 'GU'}, 
  {name: 'Guatemala', code: 'GT'}, 
  {name: 'Guernsey', code: 'GG'}, 
  {name: 'Guinea', code: 'GN'}, 
  {name: 'Guinea-Bissau', code: 'GW'}, 
  {name: 'Guyana', code: 'GY'}, 
  {name: 'Haiti', code: 'HT'}, 
  {name: 'Heard Island and Mcdonald Islands', code: 'HM'}, 
  {name: 'Holy See (Vatican City State)', code: 'VA'}, 
  {name: 'Honduras', code: 'HN'}, 
  {name: 'Hong Kong', code: 'HK'}, 
  {name: 'Hungary', code: 'HU'}, 
  {name: 'Iceland', code: 'IS'}, 
  {name: 'India', code: 'IN'}, 
  {name: 'Indonesia', code: 'ID'}, 
  {name: 'Iran, Islamic Republic Of', code: 'IR'}, 
  {name: 'Iraq', code: 'IQ'}, 
  {name: 'Ireland', code: 'IE'}, 
  {name: 'Isle of Man', code: 'IM'}, 
  {name: 'Israel', code: 'IL'}, 
  {name: 'Italy', code: 'IT'}, 
  {name: 'Jamaica', code: 'JM'}, 
  {name: 'Japan', code: 'JP'}, 
  {name: 'Jersey', code: 'JE'}, 
  {name: 'Jordan', code: 'JO'}, 
  {name: 'Kazakhstan', code: 'KZ'}, 
  {name: 'Kenya', code: 'KE'}, 
  {name: 'Kiribati', code: 'KI'}, 
  {name: 'Korea, Democratic People\'S Republic of', code: 'KP'}, 
  {name: 'Korea, Republic of', code: 'KR'}, 
  {name: 'Kuwait', code: 'KW'}, 
  {name: 'Kyrgyzstan', code: 'KG'}, 
  {name: 'Lao People\'S Democratic Republic', code: 'LA'}, 
  {name: 'Latvia', code: 'LV'}, 
  {name: 'Lebanon', code: 'LB'}, 
  {name: 'Lesotho', code: 'LS'}, 
  {name: 'Liberia', code: 'LR'}, 
  {name: 'Libyan Arab Jamahiriya', code: 'LY'}, 
  {name: 'Liechtenstein', code: 'LI'}, 
  {name: 'Lithuania', code: 'LT'}, 
  {name: 'Luxembourg', code: 'LU'}, 
  {name: 'Macao', code: 'MO'}, 
  {name: 'Macedonia, The Former Yugoslav Republic of', code: 'MK'}, 
  {name: 'Madagascar', code: 'MG'}, 
  {name: 'Malawi', code: 'MW'}, 
  {name: 'Malaysia', code: 'MY'}, 
  {name: 'Maldives', code: 'MV'}, 
  {name: 'Mali', code: 'ML'}, 
  {name: 'Malta', code: 'MT'}, 
  {name: 'Marshall Islands', code: 'MH'}, 
  {name: 'Martinique', code: 'MQ'}, 
  {name: 'Mauritania', code: 'MR'}, 
  {name: 'Mauritius', code: 'MU'}, 
  {name: 'Mayotte', code: 'YT'}, 
  {name: 'Mexico', code: 'MX'}, 
  {name: 'Micronesia, Federated States of', code: 'FM'}, 
  {name: 'Moldova, Republic of', code: 'MD'}, 
  {name: 'Monaco', code: 'MC'}, 
  {name: 'Mongolia', code: 'MN'}, 
  {name: 'Montserrat', code: 'MS'}, 
  {name: 'Morocco', code: 'MA'}, 
  {name: 'Mozambique', code: 'MZ'}, 
  {name: 'Myanmar', code: 'MM'}, 
  {name: 'Namibia', code: 'NA'}, 
  {name: 'Nauru', code: 'NR'}, 
  {name: 'Nepal', code: 'NP'}, 
  {name: 'Netherlands', code: 'NL'}, 
  {name: 'Netherlands Antilles', code: 'AN'}, 
  {name: 'New Caledonia', code: 'NC'}, 
  {name: 'New Zealand', code: 'NZ'}, 
  {name: 'Nicaragua', code: 'NI'}, 
  {name: 'Niger', code: 'NE'}, 
  {name: 'Nigeria', code: 'NG'}, 
  {name: 'Niue', code: 'NU'}, 
  {name: 'Norfolk Island', code: 'NF'}, 
  {name: 'Northern Mariana Islands', code: 'MP'}, 
  {name: 'Norway', code: 'NO'}, 
  {name: 'Oman', code: 'OM'}, 
  {name: 'Pakistan', code: 'PK'}, 
  {name: 'Palau', code: 'PW'}, 
  {name: 'Palestinian Territory, Occupied', code: 'PS'}, 
  {name: 'Panama', code: 'PA'}, 
  {name: 'Papua New Guinea', code: 'PG'}, 
  {name: 'Paraguay', code: 'PY'}, 
  {name: 'Peru', code: 'PE'}, 
  {name: 'Philippines', code: 'PH'}, 
  {name: 'Pitcairn', code: 'PN'}, 
  {name: 'Poland', code: 'PL'}, 
  {name: 'Portugal', code: 'PT'}, 
  {name: 'Puerto Rico', code: 'PR'}, 
  {name: 'Qatar', code: 'QA'}, 
  {name: 'Reunion', code: 'RE'}, 
  {name: 'Romania', code: 'RO'}, 
  {name: 'Russian Federation', code: 'RU'}, 
  {name: 'RWANDA', code: 'RW'}, 
  {name: 'Saint Helena', code: 'SH'}, 
  {name: 'Saint Kitts and Nevis', code: 'KN'}, 
  {name: 'Saint Lucia', code: 'LC'}, 
  {name: 'Saint Pierre and Miquelon', code: 'PM'}, 
  {name: 'Saint Vincent and the Grenadines', code: 'VC'}, 
  {name: 'Samoa', code: 'WS'}, 
  {name: 'San Marino', code: 'SM'}, 
  {name: 'Sao Tome and Principe', code: 'ST'}, 
  {name: 'Saudi Arabia', code: 'SA'}, 
  {name: 'Senegal', code: 'SN'}, 
  {name: 'Serbia and Montenegro', code: 'CS'}, 
  {name: 'Seychelles', code: 'SC'}, 
  {name: 'Sierra Leone', code: 'SL'}, 
  {name: 'Singapore', code: 'SG'}, 
  {name: 'Slovakia', code: 'SK'}, 
  {name: 'Slovenia', code: 'SI'}, 
  {name: 'Solomon Islands', code: 'SB'}, 
  {name: 'Somalia', code: 'SO'}, 
  {name: 'South Africa', code: 'ZA'}, 
  {name: 'South Georgia and the South Sandwich Islands', code: 'GS'}, 
  {name: 'Spain', code: 'ES'}, 
  {name: 'Sri Lanka', code: 'LK'}, 
  {name: 'Sudan', code: 'SD'}, 
  {name: 'Suriname', code: 'SR'}, 
  {name: 'Svalbard and Jan Mayen', code: 'SJ'}, 
  {name: 'Swaziland', code: 'SZ'}, 
  {name: 'Sweden', code: 'SE'}, 
  {name: 'Switzerland', code: 'CH'}, 
  {name: 'Syrian Arab Republic', code: 'SY'}, 
  {name: 'Taiwan, Province of China', code: 'TW'}, 
  {name: 'Tajikistan', code: 'TJ'}, 
  {name: 'Tanzania, United Republic of', code: 'TZ'}, 
  {name: 'Thailand', code: 'TH'}, 
  {name: 'Timor-Leste', code: 'TL'}, 
  {name: 'Togo', code: 'TG'}, 
  {name: 'Tokelau', code: 'TK'}, 
  {name: 'Tonga', code: 'TO'}, 
  {name: 'Trinidad and Tobago', code: 'TT'}, 
  {name: 'Tunisia', code: 'TN'}, 
  {name: 'Turkey', code: 'TR'}, 
  {name: 'Turkmenistan', code: 'TM'}, 
  {name: 'Turks and Caicos Islands', code: 'TC'}, 
  {name: 'Tuvalu', code: 'TV'}, 
  {name: 'Uganda', code: 'UG'}, 
  {name: 'Ukraine', code: 'UA'}, 
  {name: 'United Arab Emirates', code: 'AE'}, 
  {name: 'United Kingdom', code: 'GB'}, 
  {name: 'United States', code: 'US'}, 
  {name: 'United States Minor Outlying Islands', code: 'UM'}, 
  {name: 'Uruguay', code: 'UY'}, 
  {name: 'Uzbekistan', code: 'UZ'}, 
  {name: 'Vanuatu', code: 'VU'}, 
  {name: 'Venezuela', code: 'VE'}, 
  {name: 'Viet Nam', code: 'VN'}, 
  {name: 'Virgin Islands, British', code: 'VG'}, 
  {name: 'Virgin Islands, U.S.', code: 'VI'}, 
  {name: 'Wallis and Futuna', code: 'WF'}, 
  {name: 'Western Sahara', code: 'EH'}, 
  {name: 'Yemen', code: 'YE'}, 
  {name: 'Zambia', code: 'ZM'}, 
  {name: 'Zimbabwe', code: 'ZW'} 
],
           selected: ['Not Done'], // Must be an array reference!
        options: [
          { text: 'Orange', value: 'orange' },
          { text: 'Apple', value: 'apple' },
          { text: 'Pineapple', value: 'pineapple' },
          { text: 'Grape', value: 'grape' }
        ],
            keywordOld: null,
            keyword: '',
            page: 1,
            // // items: [],
            loading: false,
            additem:[],
            types_for_tables:[],
            types_for_tables_opt:[],
            items_table:[],

            fields: {
                id: {
                  label: 'Project',
                  sortable: true,
                  variant:'',
                  class: 'pn'
                },
                date: {
                  label: 'Start',
                  sortable: true,
                  variant:'',
                  class: 'st'
                },
                street1: {
                  label: 'Street',
                  sortable: true,
                  variant:'',
                  class: 'str'
                },
                zip1: {
                  label: 'ZIP',
                  sortable: true,
                  variant:'',
                  class: 'zip'
                },
                city1: {
                  label: 'City',
                  sortable: true,
                  variant:'',
                  class: 'cit'
                },
                other: {
                  label: 'Other',
                  sortable: true,
                  variant:''
                },
                // offer: {
                // label: 'Offer',
                // variant:''
                // // class: 'number'
                // },
                invoice: {
                label: 'List',
                class: 'list',
                variant:''
                },
                status_set: {
                label: 'Status',
                sortable: true,
                class: 'status',
                variant:''
                }
                },
            fieldsOffer: {
                offer_number: {
                label: 'Offer',
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
                label: 'Invoice',
                sortable: true,
                class: 'number'
                },
                other: {
                label: 'Other',
                sortable: true
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
            invoices: null,
            city: null,
            street: null,
            area: null,
            zip: null,

            fieldsTable: {
                number: {
                    label: 'Number',
                    sortable: true
                },
                date: {
                    label: 'Date',
                    sortable: true
                },
                place: {
                    label: 'Place',
                    sortable: true
                },
                insurance_number: {
                    label: 'Insurance',
                    sortable: true
                },

                other: {
                    label: 'Other',
                    sortable: true
                },
               

                netto: {
                    label: 'Netto',
                    sortable: true
                },

                brutto: {
                    label: 'Brutto',
                    sortable: true
                },

                 status_set: {
                    label: 'Status',
                    sortable: true,
                    class: 'status'
                },

                delete: {
                    label: "&#128465;",
                    class: 'text-center'
                }
            }
        }


    },
computed:{
items_search() {
      this.fields.id.variant =
            this.fields.date.variant =
            this.fields.street1.variant =
            this.fields.zip1.variant =
            this.fields.other.variant =
            this.fields.status_set.variant =
            this.fields.invoice.variant =
            this.fields.city1.variant = ''
      if (this.keyword){
         return this.items.filter(item =>{

          if ((this.rpeNumber(item.id)+'-'+item.project_number_year).includes(this.keyword)) {
            this.fields.id.variant = 'info'
            return true
          }
          if (item.date.includes(this.keyword)){
            this.fields.date.variant = 'info'
            return true
          }
          if (item.street1.includes(this.keyword)){
            this.fields.street1.variant = 'info'
            return true
          }
          if (item.city1.includes(this.keyword)){
            this.fields.city1.variant = 'info'
            return true
          }
          if (item.zip1.includes(this.keyword)){
            this.fields.zip1.variant = 'info'
            return true
          } 
          if (item.other?item.other.includes(this.keyword):''){
            this.fields.other.variant = 'info'
            return true
          }
          if (item.status_set?item.status_set.includes(this.keyword):''){
            this.fields.status_set.variant = 'info'
            return true
          } 
            this.getOfferRet(item.id, item)

            if(this.additem.length>0){
              var retid = this.additem.filter((v)=>{
                if (item.id==v) return true
              })
              if(retid.length>0){
              this.fields.invoice.variant = 'info'
                this.additem = []
                return true
              }
            }


          })
         
        }else{
            return this.items
        }
}
    
    },

    methods: {
      searchZip(val){
        axios.get('https://maps.google.com/maps/api/geocode/json', {
          params: {
            components: "country:"+this.selectedCornty+"|postal_code:"+val,
            sensor: "false",
            language: "en",
            key: "AIzaSyDKWZ-Jrk9KMoHYakuQfD6xQ4qUZ2XkGpo"
          }
        }).then(response => {
                  if (JSON.parse(response.request.response).results[0]!=undefined){
                  var results = JSON.parse(response.request.response).results[0]
                    for (var i=0; i<results.address_components.length; i++)
                      {
                        if (results.address_components[i].types[0] == "locality") {
                        //this is the object you are looking for City
                          var  city = results.address_components[i];
                        }
                        if (results.address_components[i].types[0]=="postal_town"){
                          //this is the object you are looking for City for GB
                          var  city = results.address_components[i];
                        }
                        if (results.address_components[i].types[0] == "administrative_area_level_1") {
                        //this is the object you are looking for State
                          var  region = results.address_components[i];
                        }
                      }
                      this.city = city?city.long_name:''
                      this.area = region?region.long_name:''
                  }
                })
      
                },

    keywordChange(e){

      var done = '0'
      var notdone = '0'
      e.forEach((v)=>{
        if(v=='Done'){
         done='1'
        }
        if(v=='Not Done'){
         notdone='1'
        }
      })

      if ((done+notdone)!=this.old_done){
        this.getProjects(done+notdone)
        this.old_done = done+notdone
      }
      
      this.keyword = this.keyword+' '
      this.keyword = this.keyword.slice(0,-1)

    },
 getOfferRet(project_id, item){
if (this.keywordOld!=this.keyword){ 
axios.get('/project_detail_new', {
  params: {
    id: project_id
  }
}).then(response => {
  var newresp = response.data.filter((v)=>{
    var result = 0
    this.selected.forEach((s)=>{
      if (s == v.type){
        result=result+1
      }
    })
    if (result>0){
      return v
    }
    
  })


     if(JSON.stringify(newresp).includes(this.keyword)){
          if (this.additem.indexOf(item.id)==-1){
            this.additem.push(item.id)
          }
          
      }
      this.keywordOld=this.keyword 
})


  
}
        },

// prevPage () {
//        if (this.page == 1) return
//        --this.page
//        this.api()
//      },
//      nextPage () {
//        ++this.page
//        this.api()
//      },
//      api () {
//        this.loading = true
//        axios.get('/projects', {
//             params: {
//               // page: this.page
//               done: 0
//             }
//   }).then((response) => {
//          this.items = response.data
//          this.loading = false
//        })
//      },


updateWork(val, id){
        axios.get('/updateProject', {params: {
                id: id,
                date: val,
                fild: 'status_set'
        }})
},
findRow(id, name){
var intId=parseInt(id.split(' ')[1])
var rows = this.getItems('Contracts').filter((v)=>{
    if(v.id==intId){
     return v
    }
})

   this.inItemGetData(rows[0], 0)

},
getItems(type){
  return this.items_table.filter((v)=>{
    if (v.type == type){
      return v
    }
  })
}, 
dataCharts(val){

    var pay = this.summFromRow(val, val.brutto)*100/val.brutto
    var withOut =100-(this.summFromRow(val, val.brutto)*100/val.brutto)
    // var days = ((-this.difdate(val.date)*34/14)<=0)?0:-this.difdate(val.date)*34/14


    // if (pay >= withOut){
    // pay = pay + (34 - days)
    // } else{
    // withOut = withOut + (34 - days)
    // }
    
    // pay = pay.toFixed(0)
    // withOut = withOut.toFixed(0)
    // days = days.toFixed(0)

    // console.log(pay, withOut, days, pay+withOut+days)
    return [pay, withOut]
    },
    updateItem(val, type, id){
      axios.get('/update_item_from_project', {
            params: {
                 val: val,
                 id: id
               }
      })
    },
            computeStyleOfferM(value) {
            switch (value) {
                case 'Open':
                    return {
                        'background-color': '#FFFFFF'
                    };
                case 'Done':
                    return {
                        'background-color': '#00f25A'
                    };
            }
        },
    summFromRow(row, brutto){
    // console.log(brutto)
    var result = 0
    row.op.forEach((v)=>{
         result = parseInt(result) + parseInt(v.value)
    })
    if (result>brutto){
        result = brutto
    }
    if (result<(-brutto)){
        result = -brutto
    }
    return result
    },
        offerDel(del_id) {
            if (confirm("Are you sure?")) {
                axios.get('/del_item', {
                    params: {
                        id: del_id
                    }
                }).then(response => {
                    this.offers = response.data
                })
            };
},
        firstRos(val, user, datacomment, t){

            if (val!=null){
              if (t=='h'){
                    val = val.split('</p>').join(" &crarr; ")
                    val = val.split('<br>').join(" &crarr; ")
                    val = val.split('<p>').join('')
                    // val = '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '
                    // var val1 = val
                    // // alert(window.innerWidth)
                    // var w = (window.innerWidth/100)*(window.innerWidth/100)
                    // // var w = (1*((window.innerWidth/898)*100)/100)
                    // // var w = (window.innerWidth/100)*3
                    // val = val.slice(0,w)
                    // if (val!=val1){
                    //   val = val+'...'
                    // }
              }     
              if (t=='t'){
                    val = val.split('</p>').join('\n')
                    val = val.split('<br>').join('\n')
                    val = val.replace(/(<([^>]+)>)/ig, "")
                    }       
                    val = val + '\n' +user+datacomment
                    // val = val.replace(/(<([^>]+)>)/ig, "")
                    // var firsrtRow1 = firstRow[0].split('<p>')
                    // firsrtRow1[1] = firsrtRow1[1].replace(/(<([^>]+)>)/ig, "");
                    return val
            } 
           
        },
        rpeNumber(num){
            var nuls=3-num.toString().length
            for (var i = 0; i <= nuls; i++) {
                num='0'+num
            }

            return num
            
        },
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


axios.get('/get_types_for_tables', {
}).then(response => {
  this.types_for_tables = response.data;
})
axios.get('/project_detail_new', {
  params: {
    id: project_id
  }
}).then(response => {
  this.items_table = response.data;
})




        },


    getInvoice(project_id){
        axios.get('/invoice', {params: {id: project_id}}).then(response => {
               this.invoices = response.data
         })
        },
    addProject(){
      this.$refs.addProjectWithDate.show()
      this.area = ""
      this.city = ""
      this.street = ""
      this.zip = ""
        },
      createProject(){
      this.$refs.addProjectWithDate.hide()

        axios.get('/add_project', {
            params: {
               city: this.city,
               street: this.street,
               zip: this.zip,
               area: this.area,
               contry: this.selectedCornty,
               user: this.$security.account.id
            }
        }).then(response => {
               this.items = response.data
             this.$router.push({
                 path: '/project/detail/'+this.items[this.items.length-1].id
             })
         })
      },
getProjects(done){
  axios.get('/projects', {
    params: {
    done: done
  }
}).then(response => {
    this.items = response.data
    this.loading = false
});
  axios.get('/get_types_for_tables', {
}).then(response => {
  this.types_for_tables_opt = []
  this.types_for_tables_opt.push('Done')
  this.types_for_tables_opt.push('Not Done')
  response.data.forEach((v)=>{
    this.types_for_tables_opt.push(v.type)
    this.selected.push(v.type)
  })

});

        },
        computeStyle(value) {
             switch (value) {
                    case 'Open':
                    return {
                        'background-color': '#FFFFFF'
                    };
                case 'Done':
                    return {
                        'background-color': '#00f25A'
                    };
                case 'Invoice':
                    return {
                        'background-color': 'yellow'
                    };
                case 'Desiccation':
                    return {
                        'background-color': 'grey'
                    };
                case 'Leakage Detection':
                    return {
                        'background-color': 'red'
                    };
                case 'Restoration':
                    return {
                        'background-color': 'blue'
                    };
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
        setTimeout(() => {
        axios.get('/variables').then(response => {
        this.project=response.data[0]
        this.fields.id.label=this.project.content
        })
            this.$socket.send('getProjects')
            this.$options.sockets.onmessage = (data) => (data.data=='getProjects') ? this.getProjects('01'): ''
        },1000);
        }
    }
</script>
<style type="text/css">
    .pWOutMargin p{
        margin-bottom:0px; 
    }
  @media screen and (min-width: 992px)  {
    .status{
      width: 200px;
    }

    .list{
      width: 40px;
    }
    .pn{
      width:115px;
    }
    .st{
      width:70px;    
    }
    .str{
      width:150px; 
    }
    .zip{
      width: 50px;      
    }
    .cit{
      width:150px;     
    }
    .other{
      max-width: 100%;
    }
}
.text-container {
    position: relative;
    display: block;
    width: 100%;
    height: calc(2em + -5px);
    overflow: hidden;
    white-space: normal;
}

.text-content {
  word-break: break-all;
  position: relative;
  display: block;
  max-height: 3em;
}



</style>