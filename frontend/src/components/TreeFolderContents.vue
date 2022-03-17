<template>
  <div class="tree-folder-contents">
    <div v-for="child in children" :key="child.id">
      <TreeFolder v-if="child.children" :folder="child"/>
      <Post v-else :post="child"/>

    </div>
  </div>
</template>

<script>
import Post from '@/components/Post'
import TreeFolder from '@/components/TreeFolder'

export default {
  name: 'TreeFolderContents',
  props: {
    children: []
  },
  components: {Post, TreeFolder}
}
</script>

<style lang="css">
.tree-folder-contents {
  padding-left: 20px;
  border-left: 1px solid #cccccc;
}
</style>
