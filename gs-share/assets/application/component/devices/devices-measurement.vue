<template>
  <b-container fluid>
    <slot name="tableHead" :tableId="tableId" ></slot>
     <div :id="'mestable'+value.parts.id">
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
        <tr v-for="(content, subIndex) in value.parts.measure_protocol">
          <td class="text-center">{{subIndex+1}}&nbsp;</td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.room" @change="updateMeasureProtocol($event, 'room', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.install_surface" @change="updateMeasureProtocol($event, 'install_surface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.install_deep" @change="updateMeasureProtocol($event, 'install_deep', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.uninstall_surface" @change="updateMeasureProtocol($event, 'uninstall_surface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.uninstall_deep" @change="updateMeasureProtocol($event, 'uninstall_deep', content.id)" />
          </td>

          <td class="text-right" style="">
            <b-icon icon="trash" aria-hidden="true" @click="measureProtocolDel(content.id) "></b-icon>
            <!-- <b-link class="fas fa-trash fa-w-16" @click="measureProtocolDel(content.id) "/>&nbsp;&nbsp;&nbsp; -->
          </td>
        </tr>
        <tr>
          <td class="text-left" colspan="7"><b-link style="text-decoration: none;font-weight: normal;" @click="addMeasureProtocolrow(value.parts.id)">+</b-link></td>
        </tr>


      </b-table-simple>
    </div>
  </b-container>
</template>

<script type="text/javascript">
import axios from 'axios';
export default {
  props: ['value', 'tableId'],
    data() {
      return {
        showRows:[],
      }
    },
  methods: {

  updateMeasureProtocol(newData, fild, id){
    axios.get('/updateMeasureProtocol', {params: {
      newData: newData,
      fild: fild,
      id: id
    }})
  },

  addMeasureProtocolrow(id){
    axios.get('/addMeasureProtocolrow', {
      params: {
        id: id
      }
    })
  },

  measureProtocolDel(id) {
    if (confirm("Are you sure?")) {
        axios.get('/measureProtocolDel', {
          params: {
            id: id
          }
        })
    }
  },

  },
}
</script>