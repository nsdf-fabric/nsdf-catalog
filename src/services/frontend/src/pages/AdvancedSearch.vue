<template>
	<q-page class="column">


        <div style="margin: 1em;">
            <h5>
                <span style="color: grey;">Advanced Search:</span>
            </h5>

            <q-form 
                class="q-gutter-md" 
                action="#/search"
                method="get"
                >

                <q-input name="query" v-model="search" filled type="search" hint="Search">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>

                <q-select
                    name="origin"
                    filled
                    v-model="repo_selection"
                    multiple
                    :options="repo_options"
                    counter
                    max-values="2"
                    hint="Max 2 selections"
                    />

                    <div>
                        <q-btn label="Search" type="submit" color="primary"/>
                        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
                    </div>

            </q-form>

        </div>



    </q-page>
</template>

<script lang="ts">
import { 
    defineComponent, 
    ref, 
    watch,
    onMounted,
    computed
} from 'vue';
import { useQuasar } from 'quasar';
import { useRouter, useRoute } from 'vue-router'

export default defineComponent({
	name: 'IndexPage',
	setup() {
        const $q = useQuasar()
        const router = useRouter()
        const route = useRoute()

        // data exposed to public and templates
		return { 
			search: ref(''),

            repo_selection: ref(null),
            repo_options: ['Materials Commons', 'Digital Rocks']
		};
	}
});
</script>
