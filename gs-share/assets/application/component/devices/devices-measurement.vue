<template>
  <b-container fluid>
    <slot name="tableHead" :tableId="tableId" ></slot>
     <b-collapse :id="'mes'+tableId">
      <table class="tableProject table b-table">
        <tr>
          <th class="text-center">#</th>
          <th class="text-center">Initial min surface</th>
          <th class="text-center">Initial max surface</th>
          <th class="text-center">Initial min depth</th>
          <th class="text-center">Initial max depth</th>
          <th class="text-center">Final min surface</th>
          <th class="text-center">Final max surface</th>
          <th class="text-center">Final min depth</th>
          <th class="text-center">Final max depth</th>
          <th class="text-center">Delete</th>
        </tr>
        <tr v-for="(content, subIndex) in value.parts.measure_protocol">
          <td class="text-center">{{subIndex+1}}&nbsp;</td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.sminsurface" @change="updateMeasureProtocol($event, 'sminsurface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.smaxsurface" @change="updateMeasureProtocol($event, 'smaxsurface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.smindepth" @change="updateMeasureProtocol($event, 'smindepth', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.smaxdepth" @change="updateMeasureProtocol($event, 'smaxdepth', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.fminsurface" @change="updateMeasureProtocol($event, 'fminsurface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.fmaxsurface" @change="updateMeasureProtocol($event, 'fmaxsurface', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.fmindepth" @change="updateMeasureProtocol($event, 'fmindepth', content.id)" />
          </td>
          <td class="text-center">
            <b-input class="cForm-input" style="text-align: center" :value="content.fmaxdepth" @change="updateMeasureProtocol($event, 'fmaxdepth', content.id)" />
          </td>
          <td class="text-right" style="">
            <b-link class="fas fa-trash fa-w-16" @click="measureProtocolDel(content.id) "/>&nbsp;&nbsp;&nbsp;
          </td>
        </tr>
        <tr>
          <td class="text-left" colspan="10"><b-link style="text-decoration: none;font-weight: normal;" @click="addMeasureProtocolrow(value.parts.id)">+</b-link></td>
        </tr>
      </table>
    </b-collapse>
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