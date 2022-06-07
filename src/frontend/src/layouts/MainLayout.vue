<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar style="background-image: url(~/src/assets/nsdf/header.background.gif)">
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title>
          NSDF Data Catalog
        </q-toolbar-title>

        <div></div>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Additional Resources
        </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

      <q-footer>
        <q-toolbar class="items-center" style="background-color: black;">
            <img src="~assets/nsdf/NSF_4-Color_bitmap_Logo.png" style="height: 2em; margin-right: 1em;" />
	This material is based upon work supported by the National Science Foundation under Grant No. 2138811.
        </q-toolbar>
      </q-footer>

  </q-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';

const linksList = [
  {
    title: 'Documentation',
    caption: '',
    icon: 'school',
    link: 'https://github.com/nsdf-fabric/nsdf-object-catalog'
  },
  {
    title: 'Github',
    caption: 'github.com/nsdf-fabric',
    icon: 'code',
    link: 'https://github.com/quasarframework'
  },
  {
    title: 'National Science Data Fabric',
    caption: 'nationalsciencedatafabric.org',
    icon: 'chat',
    link: 'http://nationalsciencedatafabric.org/'
  },
];

export default defineComponent({
  name: 'MainLayout',

  components: {
    EssentialLink
  },

  setup () {
    const leftDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      }
    }
  }
});
</script>
