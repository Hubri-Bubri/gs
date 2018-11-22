<template>
<draggable v-model="partx">
<div style="width:100%" v-for="(part, index) in partx" :key="part.id">

 <b-form-checkbox  style="width:100%" plain name="partx" class="withoutbox handleTitle" :class="{ 'table-dark': toggle.indexOf(part.parts.part_name +index ) >= 0 }"
                                            :value="part.parts.part_name+index"  @change="toggleItem(part.parts.part_name+index)">



            <b-link v-b-toggle="'partx' + index" class="butMore" style="width:100%">
               <span class="when-opened">-</span>
               <span class="when-closed">+ {{ part.parts.part_content }} €</span>
            </b-link>
  <i class="fas fa-dot-circle" style="font-size:12px"></i> 
     <span contenteditable="true" @input="toModel($event, index)" @click.prevent.self>{{part.parts.part_name}}</span>
    <b-link class="fas fa-trash  butMore" style="padding-left: 0px; font-size:12px;" @click="partDel(part.parts.part_name+index);discOfPercent()"/>
    

   </b-form-checkbox>
</div>
</draggable>
</template>


<script type="text/javascript">
import draggable from 'vuedraggable';
import {  VueEditor, Quill  } from 'vue2-editor';
    export default {
        props: ['partx'],
        components: {
        draggable,
        VueEditor
        },
        data(){
            return {
toggle: [],
  methods: {        toggleItem: function (key) {
        var i = this.toggle.indexOf(key)
        if (i < 0) {
        this.toggle.push(key)
      } else {
        this.toggle.splice(i, 1)
      }
    },
}
            }
        }
    }
</script>
