<template lang="html">
  <div class="post-index">
    <header>
      <h1>Posts</h1>
      <router-link v-if="$store.state.isUserLoggedIn" :to="{name: 'CreatePost'}" class="action">New</router-link>
    </header>
    <div class="posts">
      <TreeFolder v-for="post in posts" :key="post.id" :folder="post"/>
    </div>
  </div>
</template>

<script>
import TreeFolder from '@/components/TreeFolder'
import PostService from '@/services/post'

export default {
  name: 'PostList',
  components: {TreeFolder},

  data () {
    return {
      posts: [
        {
          id: 1,
          author: 'test',
          content: 'test',
          created: '2018-01-01 00:00:00'
        }
      ]
    }
  },
  mounted () {
    PostService.index()
      .then(response => {
        this.posts = response.data
      })
  }
}
</script>
