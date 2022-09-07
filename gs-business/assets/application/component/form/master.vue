<template>
  <b-container>
      <input type="file" id="file" ref="file" @change="handleFileUpload()"/>
      <button @click="submitFile">Submit</button>
  </b-container>
</template>

<script>
  import axios from 'axios';

  export default {
    data(){
      return {
        file: ''
      }
    },

    methods: {
      submitFile(){
            let formData = new FormData();
            formData.append('file', this.file);
            axios.post( '/loadFiles',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            )
      },

      handleFileUpload(){
        this.file = this.$refs.file.files[0];
      }
    }
  }
</script>