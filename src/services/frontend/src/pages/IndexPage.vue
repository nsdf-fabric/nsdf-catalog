<template>
	<q-page class="column items-center justify-evenly"
	   :style="{ backgroundImage: 'url(' + require('../assets/nsdf/header.background.gif') + ')', background}">

           
		<div> 

			<div style="text-align: center; margin-bottom: 3em;">
				<img src="~/assets/nsdf/logo.png" /><br/>
				<span>Data Catalog Search</span>
			</div>

            <q-form
                class="q-gutter-md"
                action="#/search"
                method="get"
                >
                <q-input name="query" v-model="search" filled type="search" hint="Search" style="width: 500px;">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>

            </q-form>

			<div style="text-align: right;">
				<a href="/#/advanced">Advanced Search</a>
			</div>
		</div>

		<div>Example Searches:</div>

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
		};
	}
});
</script>
