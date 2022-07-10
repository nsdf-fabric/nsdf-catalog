<template>
    <q-page class="column">

        <div v-if="msg != ''"
            style="padding: 1em;">
            <h5 style="margin: 0;">{{ msg }}</h5>
            <span style="font-size: 0.6em; font-family: monospace;">{{ entry_id }}</span>
        </div>

        <div v-if="data != null"
            style="padding: 1em;">
            <q-card flat style="background: #ebebeb;">
                <q-card-section class="text-left">
                    <h5 style="margin: 0;">
                        <span style="color: grey; font-size: 0.8em;">Entry Detail:</span><br>
                        <strong>{{ data.name }}</strong><br>
                        <span style="font-size: 0.6em; font-family: monospace;">{{ data.id }}</span>
                    </h5>
                </q-card-section>

                      <q-separator />

                <q-card-section class="text-left">
                    <div>
                        Origin: <q-badge>{{ data.origin_id }}</q-badge><br/>
                        Size: <b>{{ data.size }} MiB</b><br/>
                    </div>
                </q-card-section>

                  <q-separator />

                <q-card-section class="text-left">
                <strong>Tags:</strong><br/>
                <template v-for="tag in data.tags" :key="tag">
                    <q-badge color="grey" style="margin-right: 0.25em;">{{ tag }}</q-badge>
                </template>
                </q-card-section>



                <q-card-section class="text-left">
                <strong>Example Code:</strong><br/>

                <pre style="background: #121212; font-size: 0.8em; color: white; padding: 1em;">from nsdf.catalog import Client

catalog = Client()
data = catalog.entry_from(identifier="{{ entry_id }}")

data.stage(where="closest-entry-node")</pre>
                </q-card-section>

            </q-card>
        </div>

    </q-page>
</template>

<script lang="ts">
import { 
    defineComponent, 
    ref, 
    watch,
    onMounted
} from 'vue';
import { useQuasar } from 'quasar';
import { useRouter, useRoute } from 'vue-router'

import { api } from 'boot/axios';


export default defineComponent({
    name: 'EntryPage',
    setup() {
        const $q = useQuasar()
        const router = useRouter()
        const route = useRoute()

        console.log();

        // data
        const entry_id = ref(route.params.id)
        const msg = ref("")
        const data = ref(null)

        // helper functions
        function loadEntryData(entry_id: string | string[]) {
            msg.value = 'loading';
            data.value = null;

            api.get('/entry/' + entry_id)
                .then((response) => {
                    msg.value = '';
                    data.value = response.data
                })
                .catch(() => {
                    msg.value = 'Entry not found.'
                    console.log('NSDF-Warning: Loading entry data failed.')
                })
            

        }

        // reactive variables
        watch(() => route.params.id,
            async newId => {
                entry_id.value = newId
                loadEntryData(newId)
            }
        )

        // vue lifecycle hooks
        onMounted(() => {
            loadEntryData(entry_id.value)
        })



        // data exposed to public and templates
        return { 
            entry_id,
            msg,
            data,

            loadEntryData
        };
    }
});
</script>
