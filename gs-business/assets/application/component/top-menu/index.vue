<template>
  <b-navbar toggleable="lg" type="dark" variant="primary">

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
                    <b-nav-item-dropdown style="white-space: nowrap;" text="General">
                        <b-dropdown-item style="white-space: nowrap;" to="/project" href="#">{{project.content}}</b-dropdown-item>
<!--                    <b-dropdown-item to="#" href="#">Deals</b-dropdown-item>
                        <b-dropdown-item href="#">Assignments</b-dropdown-item>
                        <b-dropdown-item href="#">Bills</b-dropdown-item> -->
                        <b-dropdown-item style="white-space: nowrap;" to="/balance" href="#">Bills</b-dropdown-item>
                    </b-nav-item-dropdown>
<!-- 
                    <b-nav-item-dropdown text="Order Overview">
                        <b-dropdown-item href="#">T-Course</b-dropdown-item>
                        <b-dropdown-item href="#">Damage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Leakage Reports</b-dropdown-item>
                        <b-dropdown-item href="#">Device List</b-dropdown-item>
                        <b-dropdown-item href="#">Equipment Storage</b-dropdown-item>
                    </b-nav-item-dropdown> -->
                    <b-nav-item-dropdown style="white-space: nowrap;" text="Sub Сontractor">
                        <b-dropdown-item style="white-space: nowrap;" to="/sub" href="#">SUB-Data</b-dropdown-item>
                        <!-- <b-dropdown-item to="/subData" href="#">SUB-Data</b-dropdown-item> -->
                        <!-- <b-dropdown-item href="#">E-Invoices</b-dropdown-item> -->
                    </b-nav-item-dropdown>
                    <b-nav-item-dropdown style="white-space: nowrap;" text="Base Data">
                        <b-dropdown-item style="white-space: nowrap;" to="/customer" href="#">Customer Data</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/personals" href="#">Company Data</b-dropdown-item>
         <!--           <b-dropdown-item href="#">Insurance</b-dropdown-item>
                        <b-dropdown-item href="#">Expert</b-dropdown-item> -->
                        <b-dropdown-item style="white-space: nowrap;" to="/prices" href="#">Price List</b-dropdown-item>
                        <b-dropdown-item style="white-space: nowrap;" to="/devices" href="#">Devices List</b-dropdown-item>
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
      <b-navbar-nav class="w-100">
        <b-nav-form class="w-100">
  <!--         <slot></slot> -->
        </b-nav-form>


        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template #button-content>
            <em>{{company}} {{username}} ({{leftTime}})</em>
          </template>
          <b-dropdown-item href="#">Profile</b-dropdown-item>
          <b-dropdown-item href="#" @click="exit">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
    <b-navbar-brand href="#" style="white-space: nowrap;">{{company}}</b-navbar-brand>
  </b-navbar>
</template>


<script type="text/javascript">
import axios from 'axios';
import moment from 'moment';
export default {
    data() {
        return {
          project:{content:'Project'},
          username:'',
          company:'',
          time:'',
          leftTime:'',
          is_focus: 1
      }},

    methods: {
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
     // console.log(this.$security)
   // this.company = this.$security.company['name']
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