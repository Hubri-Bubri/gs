<template>
  <b-navbar toggleable="lg" type="dark" variant="primary">
    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
     <b-navbar-brand  style="white-space: nowrap;">{{company}}</b-navbar-brand>
    <b-collapse id="nav-collapse" is-nav>


      <b-navbar-nav>
                    <b-nav-item-dropdown style="white-space: nowrap;" :text="$t('topMenu.general')">
                        <b-dropdown-item style="white-space: nowrap;" to="/project" >{{project.content}}</b-dropdown-item>
<!--                    <b-dropdown-item to="#" href="#">Deals</b-dropdown-item>
                        <b-dropdown-item href="#">Assignments</b-dropdown-item>
                        <b-dropdown-item href="#">Bills</b-dropdown-item> -->
                        <b-dropdown-item style="white-space: nowrap;" to="/offers" >{{$t('topMenu.offers')}}</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/contracts" >{{$t('topMenu.contracts')}}</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/balance" >{{$t('topMenu.bills')}}</b-dropdown-item>
                    </b-nav-item-dropdown>
<!-- 
                    <b-nav-item-dropdown text="Order Overview">
                        <b-dropdown-item href="#">T-Course</b-dropdown-item>
                        <b-dropdown-item href="#">Damage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Leakage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Device List</b-dropdown-item>
                        <b-dropdown-item href="#">Equipment Storage</b-dropdown-item>
                    </b-nav-item-dropdown> -->
                    <b-nav-item-dropdown style="white-space: nowrap;" :text="$t('topMenu.subContractor')">
                        <b-dropdown-item style="white-space: nowrap;" to="/sub" >{{$t('topMenu.subData')}}</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/subcontracts" >{{$t('topMenu.subcontracts')}}</b-dropdown-item>
                        <!-- <b-dropdown-item to="/subData" href="#">SUB-Data</b-dropdown-item> -->
                        <!-- <b-dropdown-item href="#">E-Invoices</b-dropdown-item> -->
                    </b-nav-item-dropdown>
                    <b-nav-item-dropdown style="white-space: nowrap;" :text="$t('topMenu.baseData')">
                        <b-dropdown-item style="white-space: nowrap;" to="/customer" >{{$t('topMenu.customerData')}}</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/personals" >{{$t('topMenu.companyData')}}</b-dropdown-item>
         <!--           <b-dropdown-item href="#">Insurance</b-dropdown-item>
                        <b-dropdown-item href="#">Expert</b-dropdown-item> -->
                        <b-dropdown-item style="white-space: nowrap;" to="/prices">{{$t('topMenu.priceList')}}</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/devices" >{{$t('topMenu.devicesList')}}</b-dropdown-item>
                    </b-nav-item-dropdown>
<!-- 
                    <b-nav-item-dropdown text="Statistics">
                        <b-dropdown-item href="#">Monthly Sales</b-dropdown-item>
                        <b-dropdown-item href="#">Customer Sales</b-dropdown-item>
                        <b-dropdown-item href="#">Partner Sales</b-dropdown-item>
                    </b-nav-item-dropdown> -->
<!-- 
                    <b-nav-item-dropdown text="Settings" right v-has-permission.project@master@table-project.read>
                        <b-dropdown-item href="#">Employee</b-dropdown-item>
                        <b-dropdown-item href="#">Settings</b-dropdown-item>
                        <b-dropdown-item href="#">Units</b-dropdown-item>
                        <b-dropdown-item href="#" v-has-permission.project@master@table-project.write>Fleet</b-dropdown-item>
                    </b-nav-item-dropdown> -->
                </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <!-- <b-nav-form> -->
  <!--         <slot></slot> -->
        <!-- </b-nav-form> -->
        <country-flag :country="detect($i18n.locale)" class="d-none d-lg-block"></country-flag>
        <b-nav-item-dropdown>
          <template #button-content>
             {{detectLang($i18n.locale)}}
          </template>
            <b-dropdown-item v-for="(lang, i) in langs" :key="`Lang${i}`" @click.stop="$i18n.locale=lang">
              <country-flag :country="lang" /> {{detectLang(lang)}}
            </b-dropdown-item>
        </b-nav-item-dropdown>


        <b-nav-item-dropdown :text="username+' ('+leftTime+')'">
          <b-dropdown-item v-for="companyOpt in companyAvailable" :key="companyOpt.id"  style="white-space: nowrap;" :href="companyOpt.link" >
            {{companyOpt.name}}
          </b-dropdown-item>
          <!-- <b-dropdown-item>{{$t('topMenu.profile')}}</b-dropdown-item> -->
          <b-dropdown-item @click="exit">{{$t('topMenu.singOut')}}</b-dropdown-item>
        </b-nav-item-dropdown>


        
      </b-navbar-nav>
    </b-collapse>
   
  </b-navbar>
</template>


<script type="text/javascript">
import axios from 'axios';
import moment from 'moment';
import CountryFlag from 'vue-country-flag';
export default {
    components: {
        CountryFlag
    },
    data() {
        return {
          langs: ['gb', 'de', 'ru'],
          project:{content:'Project'},
          username:'',
          company:'',
          companyAvailable:'',
          time:'',
          leftTime:'',
          is_focus: 1
      }},

    methods: {
      detectLang(val){
        if (val == 'gb'){
          return 'English'
        }
        if (val == 'de'){
          return 'Deutsche'
        }
        if (val == 'ru'){
          return 'Русский'
        }
      },
      detect(browserLanguage){
        var returnLanguage = 'gb'
        this.langs.filter((lang)=>{
          if (lang == browserLanguage){
            returnLanguage = lang
          }
        })
        return returnLanguage
      },
      displaytime() {
          var self = this
          var diffrent = moment(this.time,"YYYY-MM-DD HH:mm:ss")
          .diff(moment().format("YYYY-MM-DD HH:mm:ss"), "seconds")

          var sec = diffrent;
          var h = sec/3600 ^ 0;
          var m = (sec-h*3600)/60 ^ 0;
          var s = sec-h*3600-m*60;

          this.leftTime =  ((m<10?"0"+m:m)+":"+(s<10?"0"+s:s)) // (h<10?"0"+h:h)+":"+

          if(diffrent <=0){ // '00:00:00'
              // this.exit()
          }
          setTimeout(self.displaytime, 1000)
      },
      exit(){
        console.log('exit')
        axios.get('/logout').then(response => {window.location.href = '//in.awe.do'});
      },
      variables(){
      axios.get('/variables').then(response => {
        this.project=response.data[0]
        })
    },
  },

    mounted(){

   // setTimeout(() => {
   this.username = this.$security.account['first_name']+' '+this.$security.account['second_name'],
     console.log(this.$security)
   this.company = this.$security.table['selected-company']['name']
   this.companyAvailable = this.$security.table['available-companies']
   this.variables();
        // },1);





      var self = this
      var time = 15 //add minutes
      this.time =  moment().add(time, 'minutes').format("YYYY-MM-DD HH:mm:ss");
      this.displaytime();
      document.onmousemove = ()=> {
      this.time =  moment().add(time, 'minutes').format("YYYY-MM-DD HH:mm:ss");
        };
      document.onkeypress = ()=> {
      this.time =  moment().add(time, 'minutes').format("YYYY-MM-DD HH:mm:ss");
      };
      document.onclick= ()=> {
      this.time =  moment().add(time, 'minutes').format("YYYY-MM-DD HH:mm:ss");
      };

    }
}
</script>