<template>
  <b-container fluid>
    <b-row align-v="center">
      <b-link style="text-decoration: none" @click="toogMeas(table.id)">
        <div
          :id="'measurementProtocolClose'+table.id"
          style="display: none; vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-down" font-scale="1" /> {{$t('measurement.measurementProtocol')}}
        </div>
        <div :id="'measurementProtocolOpen'+table.id" style="vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-up" font-scale="1" /> {{$t('measurement.measurementProtocol')}}
        </div>
      </b-link>
  
      <div :id="'s'+table.id" style="display: none;">
        <span v-show="table.summa!='0,00'" align-self="end" class="text-right">{{$t('projectDetail.total')}} {{table.summa}} €</span>
        <span v-show="table.alt_summa!='0,00'" align-self="end" class="text-right" > {{$t('projectDetail.totalAlternative')}} {{table.alt_summa}} €</span>
        &nbsp;|&nbsp;
      </div>
      <!-- <b-icon
        icon="trash"
        aria-hidden="true"
        @click="$emit('tableDelete', table.id, item_id)"
        style="cursor: pointer" /> -->
    </b-row>
     <div :id="'mestable'+table.id">
      <b-table-simple bordered >
        <b-thead>
          <b-tr>
          <b-th rowspan="2" style="text-align: center;vertical-align: middle;">#</b-th>
          <b-th rowspan="2" style="text-align: center;vertical-align: middle;">{{$t('measurement.room')}}</b-th>
          <b-th colspan="2" style="text-align: center;">{{$t('measurement.mesinstallation')}}</b-th>
          <b-th colspan="2" style="text-align: center;">{{$t('measurement.mesuninstallation')}}</b-th>
          <b-th rowspan="2" style="text-align: center;vertical-align: middle;">X</b-th>
        </b-tr>
        <b-tr>
          <b-th style="text-align: center;">{{$t('measurement.surface')}}</b-th>
          <b-th style="text-align: center;">{{$t('measurement.deep')}}</b-th>
          <b-th style="text-align: center;">{{$t('measurement.surface')}}</b-th>
          <b-th style="text-align: center;">{{$t('measurement.deep')}}</b-th>
        </b-tr>
          </b-thead>
        <tr v-for="(content, subIndex) in measure_protocol">
          <td class="text-center">{{subIndex+1}}&nbsp;</td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.room" @change="updateMeasureProtocol(subIndex, $event, 'room', content.id, content.room)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.install_surface" @change="updateMeasureProtocol(subIndex, $event, 'install_surface', content.id, content.install_surface)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.install_deep" @change="updateMeasureProtocol(subIndex, $event, 'install_deep', content.id, content.install_deep)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.uninstall_surface" @change="updateMeasureProtocol(subIndex, $event, 'uninstall_surface', content.id, content.uninstall_surface)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.uninstall_deep" @change="updateMeasureProtocol(subIndex, $event, 'uninstall_deep', content.id, content.uninstall_deep)" />
          </td>

          <td class="text-right" style="cursor: pointer;">
            <b-icon icon="trash" aria-hidden="true" @click="measureProtocolDel(content.id) "></b-icon>
            <!-- <b-link class="fas fa-trash fa-w-16" @click="measureProtocolDel(content.id) "/>&nbsp;&nbsp;&nbsp; -->
          </td>
        </tr>
        <tr>
          <td class="text-left" colspan="7"><b-link style="text-decoration: none;font-weight: normal;" @click="addMeasureProtocolrow(table.id)">+</b-link></td>
        </tr>


      </b-table-simple>
    </div>
  </b-container>
</template>

<script type="text/javascript">
import axios from 'axios';
export default {
  props: ['table'],
    data() {
      return {
        measure_protocol:[],
        showRows:[],
      }
    },
  methods: {
    toogMeas(val){
      document.getElementById('measurementProtocolOpen'+val).style.display = document.getElementById('mestable'+val).style.display = (document.getElementById('mestable'+val).style.display=='none') ? '' : 'none'
      document.getElementById('measurementProtocolClose'+val).style.display = (document.getElementById('measurementProtocolOpen'+val).style.display=='none') ? '' : 'none'
    },
  updateMeasureProtocol(index, newData, fild, id, old){
    if (old!=newData){
      axios.get('/updateMeasureProtocol', {params: {
        tableId:this.table.id,
        index, index,
        newData: newData,
        fild: fild,
        id: id
      }})
    }
  },

  addMeasureProtocolrow(id){
    axios.get('/addMeasureProtocolrow', {
      params: {
        id: id,
        tableId:this.table.id
      }
    })
  },

  measureProtocolDel(id) {
    if (confirm("Are you sure?")) {
        axios.get('/measureProtocolDel', {
          params: {
            id: id,
            tableId:this.table.id
          }
        })
    }
  },
    getRowsInMeasureProtocol(id) {
         axios.get('/get_MeasureProtocol_list', {
            params: {
               id: id
            }
         }).then(response => {
            this.measure_protocol = response.data;
         })
      },
      getFild(updateFild) {
        this.measure_protocol[updateFild.index][updateFild.fild] = updateFild.value;
      },
  },
  mounted() {
    // unitPercent=((this.table.obj!='')&&(this.table.obj!=null))?this.table.obj.split(','):[];
    this.getRowsInMeasureProtocol(this.table.id);
   }
}
</script>