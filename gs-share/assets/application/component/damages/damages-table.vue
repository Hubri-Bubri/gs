<template>
  <div>
    <slot name="tableHead" :tableId="tableId" ></slot>
    <br>
    <div :id="'damage'+value.parts.id">
      <draggable  v-model="value.parts.damage_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
      :no-transition-on-drag="true" @start="drag=true" @end="checkMove($event)" @choose="move()"> 

      <b-container v-for="(content, subIndex) in value.parts.damage_content" :key="content.id" >
          <b-row>
            <b-col cols="1" class="handle">{{(subIndex+1)}}</b-col>
            <b-col cols="5" v-if="(index!=0)+(subIndex!=0)">         
              <b-input :value="content.name"  @change="updateDamage($event, 'name', content.id)" />
                <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
                contenteditable="plaintext-only" @click.prevent.self v-html="content.desc"
                @blur="updateDamage($event.target.innerHTML, 'desc', content.id)" />
            </b-col>
            <b-col cols="5" v-else  align-self="center" style="text-align:left;">
              <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
              contenteditable="plaintext-only" @click.prevent.self v-html="content.desc"
              @blur="updateDamage($event.target.innerHTML, 'desc', content.id)" />
            </b-col>
            <b-col cols="6" style="text-align:center;">
              <img :style="'max-width:300px;max-height:'+size+'px;cursor:pointer'" :src="'/image_damage?id='+content.imgId+'&q='+quality+'&nocache='+random()" @click.stop="edit(content)" />
            </b-col> 
          </b-row>
          <b-row>
            <b-col cols="12" align-self="end" style="text-align:right;">
              <b-icon icon="trash" aria-hidden="true" @click.stop="subPartDel(content.id, subIndex);"></b-icon>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12">
              <hr />
              <br />
            </b-col>
          </b-row>
        </b-container>
      </draggable> 
    </div>
  </div>
</template>
<script type="text/javascript">
import draggable from 'vuedraggable';
import axios from 'axios';
export default {
  components: {
    draggable
  },
  props: ['value', 'tableId', 'workers', 'index', 'quality', "size", "nowTableId"],
    data() {
      return {
        oldarray: [],
      }
    },



  methods: {
    move(){
      this.oldarray =  JSON.parse(JSON.stringify(this.value.parts.damage_content))
      },
      checkMove(event){
         this.nowTableId.forEach((v)=>{
            if(v.parts.id!=this.value.parts.id){
                v.parts.damage_content.forEach((v1)=>{
                 if(v1.id == this.oldarray[event.oldIndex].id){
                    axios.get('/update_id_damage', {
                      params: {
                        newIndex: event.newIndex,
                        oldPart: this.value.parts.id,
                        oldIndex: event.oldIndex,
                        newPart: v.parts.id
                      }
                  })
                 }
              })
            }
            if(v.parts.id==this.value.parts.id){
              if(v.parts.damage_content.length==this.oldarray.length){
                axios.get('/update_id_in_one_damage', {
                      params: {
                        newIndex: event.newIndex,
                        oldIndex: event.oldIndex,
                        newPart: v.parts.id
                      }
                   })
               }
            }
         })
      },

    updateDamage(newData, fild, id){
      axios.get('/updateDamage', { params: {
        newData: newData,
        fild: fild,
        id: id
      }})
    },
    random(){
      return Math.random()*100;
    },

    subPartDel(subDel_id, subIndex) {
      if (confirm("Are you sure?")) {
        axios.get('/del_row_from_damage', {
          params: {
            id: subDel_id
          }
        })
      }
    },
    edit(content){
      this.$emit('edit', content)
    }
  },
}
</script>