<template>
	<q-page class="column items-center justify-evenly">


		<div>
            
            <img src="~/assets/nsdf/header.background.gif" width="500px" />

			<div style="text-align: center; margin-bottom: 3em;">
				<img src="~/assets/nsdf/logo.png" /><br/>
				<span>Data Catalog Search</span>
			</div>

			<q-input v-model="search" filled type="search" hint="Search" style="width: 500px;">
				<template v-slot:append>
					<q-icon name="search" />
				</template>
			</q-input>

			<div style="text-align: right;">
				<a href="/#/advanced">Advanced Search</a>
			</div>
		</div>

		<div>Example Searches:</div>

	</q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';

export default defineComponent({
	name: 'IndexPage',
	setup() {

		return { 
			search: ref(''),
		};
	}
});
</script>
