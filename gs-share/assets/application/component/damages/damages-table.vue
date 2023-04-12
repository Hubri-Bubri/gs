<template>
 <div>
    <slot name="tableHead" :tableId="tableId" ></slot>
    <br>
     <b-collapse visible :id="'dev'+tableId">
      <!-- {{value}} -->
      <draggable v-model="value.parts.damage_content" :element="'div'" :options="{handle:'.handle', group:'a', animation:150}"
                  :no-transition-on-drag="true" @end="checkMove($event, value.parts.checkbox_list)" @choose="move()"> 
<!-- {{value.parts.damage_content}} -->
        <b-container v-for="(content, subIndex) in value.parts.damage_content" :key="content.id" >
         <b-row>
            <b-col cols="1" class="handle">{{(subIndex+1)}}</b-col>
            <b-col cols="5" v-if="(index!=0)+(subIndex!=0)">         
                <b-input :value="content.name"  @change="updateDamage($event, 'name', content.id)" />
                <textarea :value="content.desc" style="width:100%;height:90%;" @change="updateDamage($event.target.value, 'desc', content.id)" class="form-control"  />
            </b-col>
            <b-col cols="5" v-else  align-self="center" style="text-align:center;">
              This is title image
            </b-col>
             <b-col cols="6" style="text-align:center;">
              <img style="max-width:300px;max-height:300px;cursor:pointer" :src="'/image_damage?id='+content.imgId+'&nocache='+random()" @click.stop="edit(content)" />
 <!--               <svg v-html="content.rotate"></svg> -->
<!-- <canvas id="canvas1" width="400" height="400"></canvas>

<button @click="can">1</button> -->
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
      }
    },
  methods: {
    random(){
    return Math.random()*100;
    },

  move(){
    this.oldarray =  JSON.parse(JSON.stringify(this.value.parts.damage_content))
  },
      checkMove(event, model){
           console.log()
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