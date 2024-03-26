<template >
  <div v-if="damage_list.length>0">
<b-row>
        <b-link style="text-decoration: none" @click="toog(table.id)">
        <div
          :id="'domageplus'+table.id"
          style="display: none; vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-down" font-scale="1" /> 
        </div>
        <div :id="'domageminus'+table.id" style="vertical-align: middle; padding-right: 10px">
          <b-icon icon="arrow-up" font-scale="1" /> 
        </div>
      </b-link> {{table.name}}&nbsp;&nbsp;&nbsp;<b-icon icon="trash" aria-hidden="true" @click="delImageFromPart()"></b-icon>
    </b-row>
    <br>
    <div :id="'damage'+table.id">
      <b-container v-for="(content, subIndex) in damage_list" :key="content.id" >
          <b-row>
            <b-col cols="1" class="handle">{{(subIndex+1)}}</b-col>
            <b-col cols="5" v-if="(index!=0)+(subIndex!=0)">         
              <b-input :value="content.name"  @change="updateDamage(subIndex, $event, 'name', content.id, content.name)" />
                <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
                contenteditable="plaintext-only" @click.prevent.self v-html="content.desc"
                @blur="updateDamage(subIndex, $event.target.innerHTML, 'desc', content.id, content.desc)" />
            </b-col>
            <b-col cols="5" v-else  align-self="center" style="text-align:left;">
              <div :style="'width:370px;padding-left:4px;border: solid 1px;'"
              contenteditable="plaintext-only" @click.prevent.self v-html="content.desc"
              @blur="updateDamage(subIndex, $event.target.innerHTML, 'desc', content.id, content.desc)" />
            </b-col>
            <b-col cols="6" style="text-align:center;">
              <img :style="'max-width:300px;max-height:'+size+'px;cursor:pointer'" :src="'/image_damage?id='+content.imgId+'&q='+quality+'&nocache='+random()" @click.stop="edit(content)" />
            </b-col> 
          </b-row>
          <b-row>
            <b-col cols="12" align-self="end" style="text-align:right;">
              <b-icon icon="trash" aria-hidden="true" @click.stop="subPartDel(content.id);"></b-icon>
            </b-col>
          </b-row>
          <b-row>
            <b-col cols="12">
              <hr />
              <br />
            </b-col>
          </b-row>
        </b-container>
    </div>
  </div>
</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: ['table',  'index', 'quality', "size", 'id', 'index'],
    data() {
      return {
        damage_list:[],
        oldarray: []
      }
    },
  methods: {
    toog(val){
        document.getElementById('domageminus'+val).style.display = document.getElementById('damage'+val).style.display = (document.getElementById('damage'+val).style.display=='none') ? '' : 'none'
        document.getElementById('domageplus'+val).style.display = (document.getElementById('domageminus'+val).style.display=='none') ? '' : 'none'
      },
    delImageFromPart(){
        if (confirm("Are you sure?")){
          axios.get('/delImageFromPart', {
            params: {
              tableId: this.table.id
            }
          })
        }
      },
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
    updateDamage(index, newData, fild, id, old){
      if (old!=newData){
        axios.get('/updateDamage', { params: {
          tableId:this.table.id,
          index:index,
          newData: newData,
          fild: fild,
          id: id
        }})
      }
    },
    random(){
      return Math.random()*100;
    },
    subPartDel(subDel_id, subIndex) {
      if (confirm("Are you sure?")) {
        axios.get('/del_row_from_damage', {
          params: {
            id: subDel_id,
            tableId:this.table.id
          }
        })
      }
    },
    edit(content){
      this.$emit('edit', content)
    },
    getRowsInDamage(id) {
         axios.get('/get_damage_list', {
            params: {
               id: id
            }
         }).then(response => {
            this.damage_list = response.data
            this.$emit('switchDamagesGroup', response.data.length, this.index)
         })
      },
      getFild(updateFild) {
        this.damage_list[updateFild.index][updateFild.fild] = updateFild.value;
      },
      updateImageDamage(id) {
        this.damage_list.forEach((v)=>{
          if (v.id == id){
            var for_update= v.imgId;
            v.imgId = ''
            v.imgId = for_update
          }
        })
      }
  },
  mounted() {
     this.getRowsInDamage(this.table.id);

    this.$options.sockets.onmessage = (data) => {
      var delimetr = data.data.split(':')

      if (delimetr[0] == 'updateImageDamage') {
        this.updateImageDamage(delimetr[1])
      }
   };
   }
}
</script>