<template>
 <div>
    <slot name="tableHead" :tableId="tableId" ></slot>
    <br>
     <b-collapse visible :id="'dev'+tableId">
      <draggable v-model="value.parts.damage_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
                  :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)" @choose="move()"> 
        <b-container v-for="(content, subIndex) in value.parts.damage_content" :key="content.id" class="handle">
         <b-row>
            <b-col cols="1" >{{(subIndex+1)}}</b-col>
            <b-col cols="5" v-if="(index!=0)+(subIndex!=0)">         
                <b-input :value="content.name"  @change="updateDamage($event, 'name', content.id)" />
                <textarea :value="content.desc" style="width:100%;height:90%;" @change="updateDamage($event.target.value, 'desc', content.id)" class="form-control"  />
            </b-col>
            <b-col cols="5" v-else  align-self="center" style="text-align:center;">
              This is title image
            </b-col>
             <b-col cols="6" style="text-align:center;">
                     
                <b-col><img :src="'/image_damage?id='+content.imgId" :style="'max-width:300px;max-height:300px;transform: rotate('+content.rotate+'deg);'" /></b-col>
                
                <b-col>
                <button class="btn btn-secondary viewer-reset h22" @click.stop="updateDamage(0, 'rotate', content.id)"  />
                <button class="btn btn-secondary viewer-rotate-left h22" @click.stop="updateDamage(rotateImage('left', content.rotate), 'rotate', content.id)" />
                <button class="btn btn-secondary viewer-rotate-right h22" @click.stop="updateDamage(rotateImage('right', content.rotate), 'rotate', content.id)" />
                </b-col>
              </b-col>
    </b-row>
        <b-row>
     
        <b-col cols="12" align-self="end" style="text-align:right;">
          <b-link  @click.stop="subPartDel(content.id, subIndex);" class="fas fa-trash fa-w-16" />
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="12">
          <hr />
          <br/>
        </b-col>
     </b-row>
        </b-container>
      </draggable> 
    </b-collapse>
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
        showRows:[],
      }
    },
  methods: {
  move(){
    this.oldarray =  JSON.parse(JSON.stringify(this.value.parts.damage_content))
  },
      checkMove(event, model){
           console.log()
      },
  updateDamage(newData, fild, id){
    axios.get('/updateDamage', {params: {
      newData: newData,
      fild: fild,
      id: id
    }})
  },
  rotateImage(direct, val){
    var x = parseFloat((val=='')?0:val)
    // if (direct == 'horizont'){
    //   if (val.indexOf('scaleX(-1)')==-1){
    //     return  val + ' scaleX(-1) '
    //   } else{ 
    //     return val.replace(' scaleX(-1) ', '')
    //   }
    // }
    // if (direct == 'vertical'){
    //   if (val.indexOf('scaleY(-1)')==-1){
    //     return val + ' scaleY(-1) '
    //   } else{ 
    //     return val.replace(' scaleY(-1) ', '')
    //   }
    // }
    if (direct == 'left'){
      if (x==0) {x=-90} else{
        x=x+-90
      }
     return x
    }
    if (direct == 'right'){
      if (x==0) {x=90} else{
        x=x+90
      }
     return x
    }
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
  },
}
</script>
<style type="text/css">
  .h22{
    height: 22px !important;
    padding: 1px;
  }
</style>