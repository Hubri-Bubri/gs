<template>
<div style="width:100%;padding-left:10px;vertical-align:middle;height:18px;">
    <div style="width:100%; background-color:yellow; ">
        &nbsp;
    </div>

    <div :style="'width:'+datas[0]+'%; background-color:#'+((datas[2]=='s')?'007bff':'00f25A')+';position:relative;top:-18px;' ">
        &nbsp;
    </div>
    <div style="position:relative;top:-36px;">
       <center>{{ Math.round(datas[0]) }}%</center>
    </div>
</div>

</template>
<script type="text/javascript">
import axios from 'axios';
export default {
  props: ['datas']
}
</script>