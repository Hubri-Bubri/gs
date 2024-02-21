<template>
  <container class="container-fluid">
    <container-header>
      <top-menu></top-menu>
    </container-header>
    <container-body>
      <b-card class="gs-container">
        <template #header>
          <b-row align-v="end">
            <b-col col xl="2" lg="2" md="12" sm="12" xs="12">
              <b-button variant="primary" class="text-nowrap" @click="addCustomer">{{$t('subs.addSub')}}</b-button>
            </b-col>
            <b-col col xl="2" lg="2" md="12"  sm="12" xs="12">
              <b-form-input
              class="w-100"
              v-model="filter"
              type="search"
              :placeholder="$t('projects.search')">
              </b-form-input>
            </b-col>
            <b-col col xl="6" lg="6" md="8"  sm="8" xs="8"> 
              <b-dropdown  variant="primary" dropright>
                 <template #button-content>
                    <b-icon icon="list-check" aria-hidden="true"></b-icon> 
                  </template>
                    <b-form-checkbox-group
                    class="m-2"
                    switches
                    v-model="filterOn">
                    <b-form-checkbox v-for="fild in filterFilds(fields)" :key="fild.key" :value="fild.key">
                      {{fild.label}}
                    </b-form-checkbox>
                    </b-form-checkbox-group>
                  </b-dropdown>
            </b-col>
            <b-col col xl="2" lg="2" md="4"  sm="4" xs="4">
              <b-form-checkbox-group
              class="text-sm-left text-md-left text-lg-right "
              switches
              :options="[$t('fields.showOld')]"
              @change="itemsFilter((show!='Show')?1:0);show=(show!='Show')?'Show':'Hide'"/>
            </b-col>
          </b-row>
        </template>
        <container>
          <container-body>
            <div class="sticky-header-lg b-table-sticky-header m-0 p-0">
            <b-table stacked="lg" :items="items" :fields="getFields()" @row-clicked="inItemClick"   hover :filter="filter" :filter-included-fields="filterOn"
            show-empty :busy="isBusy" @filtered="onFiltered"  no-border-collapse >
              <!-- :busy="(items.length==0)" -->
              <template #cell(in)="data">
                <div class="text-center w-100">
                  {{ data.index + 1 }}
                </div>
              </template>
              <template #cell(old)="data">
                <b-form inline @click.stop.pervent>
                  <b-form-checkbox @change="changeOld(data.item.id, $event);(data.item.old=data.item.old?0:1);(show=='Show')?itemsFilter(1):'';" 
                  plain :checked="data.item.old=(data.item.old==0)?false:true"  style="margin: 0px;" class="withoutPad"></b-form-checkbox>
                </b-form>
              </template>
              <template #empty>
                <div class="text-center">{{$t('projects.empty')}}</div>
              </template>
              <template #table-busy>
                <div class="text-center text-info">
                  <b-spinner class="align-middle"></b-spinner>
                  <strong>{{$t('projects.loading')}}...</strong>
                </div>
              </template>
            </b-table>
          </div>
          </container-body>
        </container>
      </b-card>
    </container-body>
  </container>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
      isBusy: true,
      additem:[],
      countNamePerson:[''],
      countMailPerson:[''],
      countPhonePerson:[''],
      countFaxPerson:[''],
      countOtherPerson:null,
      addFirm:null,
      addAppeal:null,
      addDep:null,
      addPos:null,
      show:"Show",
      items: [],
      items1:[],
      totalRows: 1,
      filter: null,
      filterOn: []
    }
  },
  computed: {
    fields() {
      return [{
        key: 'in',
        label: this.$t('fields.number'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'name',
        label: this.$t('customerDetail.name'), 
        sortable: true,
        variant: 'default'
      },
      {
        key: 'data',
        label: this.$t('customerDetail.date'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'zip',
        label: this.$t('fields.zip'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'city',
        label: this.$t('fields.city'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'street',
        label: this.$t('fields.street'),
        sortable: true,
        variant: 'default'
      },
      {
        key: 'old',
        label: this.$t('customerDetail.old'),
        sortable: true,
        variant: 'default'
      }]
    }
  },
  methods: {
    onFiltered(filteredItems) {
      this.totalRows = filteredItems.length
    },
    getFields(){
      return this.fields.filter((v)=>{
        v.variant = "default"
        this.filterOn.forEach((v1)=>{
          if(v.key==v1){
              v.variant="info"
          }
        });
        return v
      });
    },
    filterFilds(val){
      return  val.filter((v)=>{
        if ((v.key != 'in')&(v.key != 'old')) {
          return v;
        }
      })
    },
    itemsFilter(val){
      if(val==1){
        var arr = this.items.filter(function(val){
          if (val.old==false){
            return val
          }
        })
        this.items=arr
      } else {
        this.items=this.items1
      }
    },
    inItemClick(item, index, event) {
      this.$router.push({
        path: `/sub/detail/${item.id}`
      })
    },
    addCustomer(){
      axios.get('/add_customer_sub_list').then(response => {
        this.items = response.data;
        this.$router.push({
          path: '/sub/detail/'+this.items[this.items.length-1].id
        })
      })
    },
    getCustomers(){
      axios.get('/customer_sub').then(response => {
        // v.date = this.$options.filters.dateInverse(v.date)
        this.items= this.items1 = response.data.filter((v)=>{
          v.name = v.name.split('_').join(' ')
          return v
        });
        this.isBusy = false;
        this.itemsFilter((this.show!='Show')?0:1);
      })
    },
    changeOld(id, eve){
      axios.get('/customer_old', {
        params: {
          id: id,
          event: eve?1:0
        }
      })
    },
  },
  mounted(){
    this.totalRows = this.items.length
    setTimeout(() => {
      this.$socket.send('getCustomers')
      this.$options.sockets.onmessage = (data) => (data.data=='getCustomers') ? this.getCustomers(): ''
    },1000);
  }
}
</script>