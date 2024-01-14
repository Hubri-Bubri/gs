<template>
  <div>
    <slot name="tableHead" :tableId="tableId" ></slot>
    <br>
    <div :id="'damage'+value.parts.id">
      <draggable v-model="value.parts.damage_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
      :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)" @choose="move()"> 
        <b-container v-for="(content, subIndex) in value.parts.damage_content" :key="content.id" >
          <b-row>
            <b-col cols="1" class="handle">{{(subIndex+1)}}</b-col>
            <b-col cols="5" v-if="(index!=0)+(subIndex!=0)">         
              <b-input :value="content.name"  @change="updateDamage($event, 'name', content.id)" />
                <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
                contenteditable="true" @click.prevent.self v-html="content.desc"
                @blur="updateDamage($event.target.innerHTML, 'desc', content.id)" />
            </b-col>
            <b-col cols="5" v-else  align-self="center" style="text-align:left;">
              <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
              contenteditable="true" @click.prevent.self v-html="content.desc"
              @blur="updateDamage($event.target.innerHTML, 'desc', content.id)" />
            </b-col>
            <b-col cols="6" style="text-align:center;">
              <img style="max-width:300px;max-height:300px;cursor:pointer" :src="'/image_damage?id='+content.imgId+'&nocache='+random()" @click.stop="edit(content)" />
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
  props: ['value', 'tableId', 'workers', 'index'],
    data() {
      return {
        oldarray: [],
      }
    },
  methods: {
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
    move(){
      this.oldarray =  JSON.parse(JSON.stringify(this.value.parts.damage_content))
    },
    checkMove(event, model){
      console.log('checkMove')
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