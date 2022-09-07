<template>
<div>
                               <b-row >
                                    <b-col cols="6">
                                      <b-form-group horizontal label-cols="7" label="Images group by:">
                                          <b-select class="customButton" :value="selectedDamageImages" :options="labelForFieldsImages()" @change="chvalueimages($event);resetFilds()"  />
                                      </b-form-group>
                                    </b-col>
                                    <b-col cols="6" v-show="((detselrow()==false)&&selectedDamageImages=='Image')">
                                      <b-button @click="allselrow()" class="customButton"> Select All </b-button>
                                    </b-col>
                                   <b-col cols="6" v-show="detselrow()">
                                      <b-form-group horizontal label-cols="7" label="To change table:">
                                          <b-select class="customButton" @change="selectimagesarr($event)" :options="optImages" text-field="value" value-field="id" />
                                      </b-form-group>
                                    </b-col>
                                  </b-row>
                                    <br/>

                                     <b-table v-viewer  :items="domageImages" :fields="fieldsImages" stacked="lg" hover
                                     @row-clicked="image_in_table_selected" class="tableProject outgroup" small v-if="selectedDamageImages=='Image'">
                                      <template slot="id" slot-scope="row">
                                        <b-col cols="12" class="text-center">
                                          <img :src="row.item.id" class="image" style="max-height:70px;max-width:70px" @click.stop="showx('outgroup', row.index)">
                                        </b-col>
                                      </template>
                                      <template slot="file_name" slot-scope="row">
                                           <b-form-input :state="null" type="text" @change="updatefilename($event, 'name', row.item.id.split('=')[1])" :title="row.item.file_name"
                                           :value="row.item.file_name" class="cForm-input" @focus.native="changeDisable('f', 'nameoffile', row.item.id.split('=')[1])"
                                           @blur.native="changeDisable('b', 'nameoffile', row.item.id.split('=')[1])" :id="'nameoffile'+row.item.id.split('=')[1]" style="width:95%" /> 
                                      </template>
                                      <template slot="delete" slot-scope="it">
                                                <b-col>
                                                <b-link @click.stop="filedel(it.item.id.split('=')[1])" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                                </b-col>
                                        </template>
                                      <template slot="group" slot-scope="row">
                                          <b-select class="customButton" :value="row.item.group" :options="optImages"
                                          style="width:95%" text-field="value" value-field="id" 
                                          @change="updatefilename($event, 'group', row.item.id.split('=')[1])" />
                                      </template>
                                        <template slot="date" slot-scope="data">
                                           {{data.item.date | dateInverse}}
                                        </template>
                                    </b-table>
                                    <div v-else  v-for="(item, i) in groupByFild(selectedDamageImages)">
                                    <b-link v-b-toggle="item.id+'-'+i" class="butMore">
                                      <span class="when-opened">- {{item.name}} <b-button @click.stop="allselrowin(item.table)" class="customButton when-opened" v-show="detselrowin(item.table)"> Select All </b-button></span>
                                      <span class="when-closed">+ {{item.name}}</span>
                                    </b-link> 
                                    <b-collapse :id="item.id+'-'+i">
                                      <b-table  v-viewer :items="item.table" :fields="fieldsImages" stacked="lg" hover  @row-clicked="image_in_table_selected" 
                                      :class="'tableProject '+'im'+item.id+'-'+i" small >
                                        <template slot="id" slot-scope="row">
                                        <b-col cols="12" class="text-center">
                                          <img :src="row.item.id" class="image" style="max-height:100px;max-width:100px" @click.stop="showx('im'+item.id+'-'+i, row.index)">
                                        </b-col>
                                        </template>
                                      <template slot="file_name" slot-scope="row">
                                           <b-form-input :state="null" type="text" @change="updatefilename($event, 'name', row.item.id.split('=')[1])" :title="row.item.file_name"
                                           :value="row.item.file_name" class="cForm-input" @focus.native="changeDisable('f', 'nameoffile', row.item.id.split('=')[1])" 
                                           @blur.native="changeDisable('b', 'nameoffile', row.item.id.split('=')[1])" :id="'nameoffile'+row.item.id.split('=')[1]" style="width:95%" /> 
                                      </template>
                                      <template slot="group" slot-scope="row">
                                          <b-select class="customButton" :value="row.item.group" :options="optImages"
                                          style="width:95%" text-field="value" value-field="id" 
                                          @change="updatefilename($event, 'group', row.item.id.split('=')[1])" />
                                      </template>
                                      <template slot="delete" slot-scope="it">
                                                <b-col>
                                                <b-link @click.stop="filedel(it.item.id.split('=')[1])" class="fas fa-trash fa-w-16" style="padding-top:7px;" />
                                                </b-col>
                                        </template>
                                        <template slot="date" slot-scope="data">
                                           {{data.item.date | dateInverse}}
                                        </template>
                                      </b-table>
                                    </b-collapse>
                                    </div>
</div>
</template>
<script type="text/javascript">


export default {
  components: {
    
  },
  props: ['domageImages', 'fieldsImages', 'selectedDamageImages', 'optImages'],
  data(){
      return{
       
            }
    },
  
    methods: {
    changeDisable(type_operation, fild, id){
      this.$emit('changeDisable', type_operation, fild, id)
        },
    filedel(val) {
            this.$emit('filedel', val)
        },
    chvalueimages(val){
        this.$emit('chvalueimages', val)
      },
 
    image_in_table_selected(item){
        this.$emit('imageInTableSelected', item)
       },
    showx(classId, index){
        this.$emit('showx', classId, index)
       },
    updatefilename(val, type, id){
       this.$emit('updatefilename', val, type, id)
    },
    resetFilds(){
       this.$emit('resetFilds')
    },
    

      labelForFieldsImages(){
        var labelsArr = [];
        this.fieldsImages.forEach((v)=>{
          if(v.key=='id'){
            labelsArr.push('Image')
          }else{
            if(v.key!='delete'){
              labelsArr.push(v.key)
            }
          }

        })
        return labelsArr
      },

// labelForFieldsImages(){
// this.$emit('labelForFieldsImages')
// },


allselrow(){
this.$emit('allselrow')
},
allselrowin(table){
this.$emit('allselrowin', table)
},
selectimagesarr(group){
this.$emit('selectimagesarr', group)
},


    detselrow(){
      var countdetect = 0
      this.domageImages.forEach((v)=>{
             if(v._rowVariant=='secondary'){
              countdetect = countdetect + 1
             }
        })
      if (countdetect > 0) return true
        else{
          return false
        }
    },

    detselrowin(table){

      var countdetect = 0
      table.forEach((v)=>{
             if(v._rowVariant=='secondary'){
              countdetect = countdetect + 1
             }
        })

        return ((countdetect==0) && (table.length > 1))
   
    },
    groupByFild(fild){
        var tables = []
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == fild)].thClass='d-none'
        this.fieldsImages[this.fieldsImages.findIndex(x => x.key == fild)].tdClass='d-none'

        this.domageImages.forEach((v)=>{
            var date = v.date
            var user = v.user
            var file_name = v.file_name
            var id = v.id
            var group = v.group


          if (fild == 'date'){
            var nameOfDate = v.date.split(' ')[0]
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'group':group, 'file_name':file_name, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'file_name'){
            var nameOfDate = v.file_name
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'user':user, 'group':group, 'date':date, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'user'){
            var nameOfDate = v.user
            if (tables.findIndex(x => x.name == nameOfDate) == -1){
              tables.push({'name':nameOfDate, 'table':[{'id':id, 'group':group, 'file_name':file_name, 'date':date, '_rowVariant':''}]})
            }else{
              tables[tables.findIndex(x => x.name == nameOfDate)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
            }
          }
          if (fild == 'group'){
            var nameOfDate = v.group
            if (this.optImages[this.optImages.findIndex(y => y.id == group)]){
              if (tables.findIndex(x => x.name == this.optImages[this.optImages.findIndex(y => y.id == group)].value) == -1){
                tables.push({'name':this.optImages[this.optImages.findIndex(y => y.id == group)].value, 'table':[{'id':id, 'user':user, 'file_name':file_name, 'date':date, '_rowVariant':''}]})
              }else{
                tables[tables.findIndex(x => x.name == this.optImages[this.optImages.findIndex(y => y.id == group)].value)].table.push({'id':id, 'user':user, 'file_name':file_name, 'group':group, 'date':date, '_rowVariant':''})
              }
            }
          }




        })
        return tables
      },


    },
    mounted(){

    }
  }

</script>