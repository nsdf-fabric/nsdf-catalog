<template>
  <q-layout view="hHh lpR ffr">

    <q-header bordered class="bg-white text-grey-8">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title>
            <img src="~/assets/nsdf/logo.png" style="height: 1em; position: relative; top: 3px;">
            NSDF Data Catalog
        </q-toolbar-title>

        <q-btn dense flat round icon="menu" @click="toggleRightDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <!-- drawer content -->
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

    <q-drawer v-model="rightDrawerOpen" side="right" overlay elevated>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-grey-8 text-white">
        <q-toolbar class="items-center" style="background-color: black;">
            <img src="~assets/nsf/NSF_4-Color_bitmap_Logo.png" style="height: 2em; margin-right: 1em;" />
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
    const rightDrawerOpen = ref(false)

    return {
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },

      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  }
});
</script>
