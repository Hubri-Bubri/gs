<template>
       <div>
        <temp-nav :applications="applications"></temp-nav>
       </div>
</template>


<script type="text/javascript">
    export default {
        computed: {
            applications: function() {
                return this.$root.applications;
            }
        }
    }
</script>
