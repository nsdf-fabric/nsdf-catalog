<style lang="sass">

</style>

<template>
	<q-page class="row" style="padding: 1em;">

    <q-table
      :rows="rows"
      row-key="id"

      :columns="columns"
      :filter="filter"
      v-model:pagination="pagination"
      :loading="loading"
      :grid="grid"

      flat
      style="width: 100%;"

      @request="updateSearchResults"
    >

      <template v-slot:body-cell-origin_id="props">
        <q-td :props="props">
          <div>
            <q-badge :label="props.value" />
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-name="props">
        <q-td :props="props">
          <div>
              <strong><a :href="'#/entry/' + props.row.id" style="color: black;">{{props.value}}</a></strong>
          </div>
        </q-td>
      </template>


      <template v-slot:body-cell-tags="props">
        <q-td :props="props">
          <div>
              <template v-for="tag in props.value" :key="tag">
                  <q-badge color="grey" style="margin-right: 0.25em;">{{ tag }}</q-badge>
              </template>
          </div>
        </q-td>
      </template>


      <template v-slot:top-left>
            <q-form
                style="position: relative; left: -0.9em;"
                class="q-gutter-md"
                action="#/search"
                method="get"
                >
                <q-input name="query" v-model="filter" filled type="search" hint="Search" style="width: 500px;">
                    <template v-slot:append>
                        <q-icon name="search" />
                    </template>
                </q-input>

            </q-form>
      </template>


      <template v-slot:top-right>
      <q-toggle
        v-model="grid"
        checked-icon="check"
        label="Grid View"
        unchecked-icon="clear"
      />
      </template>

      <template v-slot:item="props">
          <div class="q-pa-xs col-xs-12 col-sm-6 col-md-4">
              <q-card flat style="background: #ebebeb">
                  <q-card-section class="text-left">
                      <a :href="'#/entry/' + props.row.id" style="color: black; text-decoration: none; display: block;">
                          <strong style="text-decoration: underline;">{{props.row.name}}</strong><br/>
                          <span style="font-size: 0.8em; font-family: monospace;">{{ props.row.id }}</span>
                      </a>
                  </q-card-section>

                      <q-separator />

                      <q-card-section>
                          Origin: <q-badge>{{ props.row.origin_id }}</q-badge><br/>
                          Size: <b>{{ props.row.size }} MiB</b><br/>
                      </q-card-section>
                      <q-separator />

                      <q-card-section class="flex flex-left">
                          Tags: &nbsp;<br/>
                          <div>
                          <template v-for="tag in props.row.tags" :key="tag">
                              <q-badge color="grey" style="margin-right: 0.25em;">{{ tag }}</q-badge>
                          </template>
                          </div>
                      </q-card-section>

              </q-card>
          </div>
      </template>
    </q-table>



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

import { api } from 'boot/axios';


// https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/21152762#21152762
function getQueryParams() {
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    return location.search ? location.search.substr(1).split('&').reduce((qd, item) => {let [k,v] = item.split('='); v = v && decodeURIComponent(v); (qd[k] = qd[k] || []).push(v); return qd}, {}) : {}
}


export default defineComponent({
    setup () {
        const $q = useQuasar()
        const router = useRouter()
        const route = useRoute()

        // data
        const filter = ref('')
        const rows = ref([])

        // display options
        const columns = [                   // some configuration on how to render each column (also see template)
            { name: 'name', label: 'Name', field: 'name' , align: 'left', sortable: true},
            { name: 'tags', label: 'Tags', field: 'tags', align: 'left'},
            { name: 'origin_id', label: 'Origin', field: 'origin_id', align: 'left', sortable: true},
            { name: 'size', label: 'Size (MiB)', field: 'size', sortable: true},
        ];
        const loading = ref(false)          // is the laoding indicator active?
        const pagination = ref({            // state of the pagination
            page: 1,
            sortBy: 'id',
            descending: false,
            rowsPerPage: 10,
            rowsNumber: 1000
        })


        // helper functions
        function updateSearchResults(props: any) {

            console.log(props)

            // gather params
            let params = {
            }
            Object.assign(params, props.pagination)
            if (props.filter != '') {   
                Object.assign(params, {filter: props.filter})
            }

            console.log(params)

            api.get('/search', {params: params})
                .then((response) => {
                    rows.value = response.data

                    pagination.value.sortBy = props.pagination.sortBy
                    pagination.value.descending = props.pagination.descending
                    pagination.value.rowsPerPage = props.pagination.rowsPerPage
                    pagination.value.page = props.pagination.page

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



        // vue lifecycle hooks
        onMounted(() => {

            let query = getQueryParams();

            // eslint-disable-next-line @typescript-eslint/ban-ts-comment
            // @ts-ignore
            filter.value = query.query[0];

            let props = {
                pagination: pagination.value,
                filter: filter.value
            }
            updateSearchResults(props)
        })


        // data exposed to public and templates
        return {
            // data
            rows,

            // display options
            columns,
            filter,
            pagination,
            loading,
            grid: ref(true),

            // helper functions
            updateSearchResults,
        }
    }
});
</script>
