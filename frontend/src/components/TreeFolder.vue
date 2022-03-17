<template>
  <div class="node-folder">
    <Post :post="folder"/>
    <TreeFolderContents :children="folder.children"/>
  </div>
</template>

<script>
import Post from '@/components/Post'

export default {
  name: 'TreeFolder',
  props: {
    folder: {}
  },
  components: {
    Post,
    TreeFolderContents: () => import('@/components/TreeFolderContents')}
}
</script>
