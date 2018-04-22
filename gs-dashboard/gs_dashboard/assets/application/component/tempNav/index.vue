<template>
    <div>

        <login-form></login-form>




    <b-row align-h="around">
            <b-card-group v-for="application in applications">
                    <b-card :title="application.name"
                            :img-src="application.image"
                            img-fluid
                            img-top>
                        <p class="card-text">
                            {{application.description}}
                        </p>
                         <p class="card-text">
                            {{application.userName}}
                            {{application.id}}
                            {{application.access}}
                        </p>
                        <b-button variant="primary" :to="application.link">{{application.label}}</b-button>
                    </b-card>
            </b-card-group>
    </b-row>
 



    </div>
</template>


<script type="text/javascript">
export default {
    props: {
        applications: Array
    }
}
</script>
