<template>
   <div>



      <draggable :value="value" @input="onItems" :element="'div'" :options="{handle:'.handleTitle', group:'b', animation:150}"
         :no-transition-on-drag="true" @start="drag=true" @end="drag=false">
         <div v-for="(part, index) in value" :key="part.id">          <br>
            <calc-table-print v-model="value[index]" :addtaxColapse="addtaxColapse" :tableId="index" :comments="comments" :prices="prices"
            :color="color" :selectedWorkers="selectedWorkers" :toggle="value[index].parts.toggle ">
               <h6 class="handleTitle"
                    slot="tableHead">
                        {{value[index].parts.part_name}}
                </h6>

            </calc-table-print>

        </div>
      </draggable>
      <br>
           
   </div>
</template>

<script type="text/javascript">
import draggable from 'vuedraggable';
export default {
    components: {
        draggable,
    },
    props: ['value', 'addtaxColapse', 'workers', 'toggle', 'comments', 'prices', 'commentOfTable', 'alttax'],
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
            searchWorker:'',
        }
    },
computed: {
    workers_list() {
      return this.workers.filter(post => {
        return post.toLowerCase().includes(this.searchWorker.toLowerCase())
      })
    },
    total: function() {
        var vm = this;
            return function(value) {
                var summa = 0
                value.forEach(function(val) {
                    if (val.status == 'yes') {
                        summa += val.count * val.price
                    }
                })
                return summa; //количество разрядов
            };
        },
  },
    methods: {

        toModel(newVal, partName) {
            partName = newVal.target.innerText
        }, 
        onItems($event){
          { this.$emit('input', $event) }
        },
        nameOfPart() {
            var tmpArrValue = []
            this.shpart = true,
            this.$refs.shpart.hide(),
            tmpArrValue.push({
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
            this.$emit('input', tmpArrValue.concat(this.value))
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
            var nowPartx = JSON.parse(JSON.stringify(this.value))
            var tmpArr = this.tmpArr = []
            this.oldColor.push(JSON.parse(JSON.stringify(this.color)))
            this.oldPartx.push(JSON.parse(JSON.stringify(this.value)))
            var tmpArrCp = JSON.parse(JSON.stringify(this.value))
            var newColor = []
            this.color.forEach((clolorRow) => {
                var partIndex = clolorRow.split('-')
                nowPartx.forEach(function(part, index) {
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
                nowPartx.forEach((part)=>{
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
            this.$emit('input', nowPartx)
        },
        partDel(part) {
            // console.log(del_id);
            if (confirm("Are you sure?")){
            var deltable=this.value.filter(function(val){return (val!=part)})
            this.$emit('input', deltable)
            }

        },
        cancelPartx(indexButton) {
            var tmpArrValue = []
            this.color = []
            this.moveToCopy = []
            this.oldPartx[indexButton].forEach((val)=> {
                tmpArrValue.push(val)
            })
            this.$emit('input', tmpArrValue)
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