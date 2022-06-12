<template>
	<q-page class="row">

    <q-btn label="AXIOS test" @click="loadData" />
    <div>{{ data }}</div>

    <q-table
      style="width: 100%;"
      :grid="grid"
      :rows="rows"
      :columns="columns"
      row-key="name"
      :filter="filter"
      hide-header
    >

     <template v-slot:top-right>
        <q-toggle v-model="grid" label="Grid" class="q-mb-md" />
     </template>

      <template v-slot:top-left>
        <img src="~/assets/nsdf/logo.png" style="height: 3.5em; margin-right: 1em; float: left;" />
        <q-input filled debounce="300" v-model="filter" placeholder="Search">
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </template>
    </q-table>


  </q-page>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const columns = [
  {
    name: 'desc',
    required: true,
    align: 'left',
    field: (row: any) => row.name,
    format: (val: any) => `${val}`,
    sortable: true
  },
  { name: 'calories', align: 'center', label: 'Calories', field: 'calories', sortable: true },
  { name: 'fat', label: 'Fat (g)', field: 'fat', sortable: true },
  { name: 'carbs', label: 'Carbs (g)', field: 'carbs' }
]

const rows = [
  { name: 'Frozen Yogurt', calories: 159, fat: 6.0, carbs: 24 },
  {     name: 'Ice cream sandwich',     calories: 237,     fat: 9.0,     carbs: 37   },
  {     name: 'Eclair',     calories: 262,     fat: 16.0,     carbs: 23   },   
  {     name: 'KitKat',     calories: 518,     fat: 26.0,     carbs: 65   },
  { name: 'Frozen Yogurt', calories: 159, fat: 6.0, carbs: 24 },
  {     name: 'Ice cream sandwich',     calories: 237,     fat: 9.0,     carbs: 37   },
  {     name: 'Eclair',     calories: 262,     fat: 16.0,     carbs: 23   },   
  {     name: 'Donut',     calories: 452,     fat: 25.0,     carbs: 51   },  
  { name: 'Frozen Yogurt', calories: 159, fat: 6.0, carbs: 24 },
  {     name: 'KitKat',     calories: 518,     fat: 26.0,     carbs: 65   },
  {     name: 'Ice cream sandwich',     calories: 237,     fat: 9.0,     carbs: 37   },
  {     name: 'Donut',     calories: 452,     fat: 25.0,     carbs: 51   },  
  {     name: 'Eclair',     calories: 262,     fat: 16.0,     carbs: 23   },   
  {     name: 'KitKat',     calories: 518,     fat: 26.0,     carbs: 65   },
  {     name: 'Donut',     calories: 452,     fat: 25.0,     carbs: 51   },  
]


export default defineComponent({
    setup () {
        const $q = useQuasar()
        const data = ref(null)

        function loadData () {
            api.get('/')
                .then((response) => {
                    data.value = response.data
                })
                .catch(() => {
                    $q.notify({
                        color: 'negative',
                        position: 'top',
                        message: 'Loading failed',
                        icon: 'report_problem'
                    })
                })
        }


        return {
            data,
            loadData,

            grid: ref(true),
            filter: ref(''),
            columns,
            rows
        }
    }
});
</script>
