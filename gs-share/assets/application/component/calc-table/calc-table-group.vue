<template>
   <div>
    <b-modal size="sm" centered id="worker" ref="worker" title="Select Workers" body-class="workerHeight">
            <b-form-input type="text" v-model="searchWorker"  style="margin-bottom: 4px !important;"/>
            <b-form-checkbox-group buttons  button-variant="light" style="width:100%" v-model="selectedWorkers" stacked :options="workers_list"/>
            <template slot="modal-footer">
              <button type="button" left class="btn btn-secondary" @click="selectedWorkers=[]">Clear</button>
           </template>
        </b-modal>
      <b-form @submit="nameOfPart">
         <b-modal size="md" centered id="addPart" ref="shpart" title="Add Part">
            <b-form-group horizontal :label-cols="4" label="Name of part:"
               label-for="nameofpart" style="padding: 5px;">
               <b-form-input v-model="nameofpart" required class="cForm-input" id="nameofpart"
                  :state="null" type="text" placeholder="Enter name of part" />
            </b-form-group>
            <template slot="modal-footer">
               <b-button type="submit" variant="primary" data-toggle="addPart">OK</b-button>
            </template>
         </b-modal>
      </b-form>
      <b-modal size="sm" centered id="move" ref="move" title="Move">
         <b-form-select multiple class="" id="move" @change="moveToCopySelect($event, moveToCopyRadio)" v-model="moveToCopy" :select-size="4">
            <option v-for="part in partx">{{part.parts.part_name}}</option>
         </b-form-select>
         <b-form-radio-group name="moveOrCopy" v-model="moveToCopyRadio" :options="['Move', 'Copy']" />
         <template slot="modal-footer">
            <button type="button" class="btn btn-secondary" :disabled="counter==-1" @click="cancelPartx(counter)"><i class="fas fa-undo"></i> ({{(counter+1)}})</button>
            <button type="button" class="btn btn-primary" @click="okMoveToCopy">OK</button>
         </template>
      </b-modal>
      <b-row>
         <b-col>
            <b-button class="customButton" v-b-modal.addPart>
               Add Part
            </b-button>

            <b-button class="customButton" @click="move">
               Move
            </b-button>
            <b-button class="customButton" @click="worker">
               Workers
            </b-button>
        </b-col>
      </b-row>
      <draggable v-model="partx" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="drag=false">
         <calc-table :part="part" :addtaxColapse="addtaxColapse" :color="color" :selectedWorkers="selectedWorkers" v-for="part in partx" :key="part.id">
            <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(part)" slot="tableDel" />
         </calc-table>
      </draggable>
   </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
export default {
    components: {
        draggable,
    },
    props: ['partx', 'addtaxColapse', 'workers'],
    data() {
        return {
            counter: -1,
            moveToCopyRadio: 'Move',
            moveToCopy: [],
            tmpArr: [],
            color: [],
            oldColor: [],
            nameofpart: null,
            shpart: null,
            oldPartx: [],
            selectedWorkers: [],
            searchWorker:''
        }
    },
computed: {
    workers_list() {
      return this.workers.filter(post => {
        return post.toLowerCase().includes(this.searchWorker.toLowerCase())
      })
    }
  },
    methods: {
        nameOfPart() {
            this.shpart = true;
            this.$refs.shpart.hide(),
                this.partx.unshift({
                    parts: {
                        part_name: nameofpart.value,

                        checkbox_list: {
                            flavours: {},
                            selected: {},
                            allSelected: {},
                            indeterminate: {}
                        },

                        part_content: []
                    }
                })
        },
        okMoveToCopy() {
            this.$refs.move.hide()
        },
        move() {
            if (this.color.length != 0) {
                this.counter = -1
                this.moveToCopy = []
                this.oldPartx = []
                this.$refs.move.show()
            } else {
                alert('no selected rows')
            }
        },
        moveToCopySelect(event, radio) {
            var tmpArr = this.tmpArr = []
            this.oldColor.push(JSON.parse(JSON.stringify(this.color)))
            this.oldPartx.push(JSON.parse(JSON.stringify(this.partx)))
            var tmpArrCp = JSON.parse(JSON.stringify(this.partx))
            var newColor = []
            this.color.forEach((clolorRow) => {
                var partIndex = clolorRow.split('-')
                this.partx.forEach(function(part, index) {
                    var temRow = ''
                    var other = ''
                    if (part.parts.part_name == partIndex[0]) {
                        temRow = part.parts.part_content[partIndex[1]]
                        other = tmpArrCp[index].parts.part_content[partIndex[1]]
                        tmpArr.splice(0, 0, other)
                        if (radio == 'Move') {
                            part.parts.part_content.splice(temRow, 1)
                        }
                    }
                })
            })

            event.forEach((eve)=> {
                this.partx.forEach((part)=>{
                    if (part.parts.part_name == eve) {
                        this.tmpArr.forEach(function(val, index) {
                            newColor.push(part.parts.part_name + '-' + index)
                            part.parts.part_content.unshift(val)
                        })
                    }
                })
            })
            this.color = []
            this.color = newColor.slice()
            this.counter = this.counter + 1
        },
        cancelPartx(indexButton) {
            this.color = []
            this.moveToCopy = []
            this.partx.splice(0, this.partx.length)
            this.oldPartx[indexButton].forEach((val)=> {
                this.partx.push(val)
            })
            this.color = JSON.parse(JSON.stringify(this.oldColor[indexButton]))
            this.counter = this.counter - 1
        },
        okMoveToCopy() {
            this.$refs.move.hide()
        },
          worker() {
          this.$refs.worker.show()
        },
        okWorker() {
            this.$refs.worker.hide()
        }

    }
}
</script>
<style>
    #modalWorker .v-select.searchable .dropdown-toggle{
        height: 500px !important;
    }
    .workerHeight{
       /* height: 80%;*/
    }
</style>