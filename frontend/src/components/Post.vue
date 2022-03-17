<template lang="html">
  <article class="post">
    <h1>{{ post.content }}</h1>
    <div class="about">by {{ post.author }} on {{ post.created }}</div>
    <div v-if="$store.state.isUserLoggedIn" class="actions">
      <router-link :to="{name: 'ReplyPost', params: {id: post.id}}" class="action">Reply</router-link>
      <router-link :to="{name: 'UpdatePost', params: {id: post.id}}" class="action">Edit</router-link>
    </div>
  </article>
</template>

<script>
export default {
  name: 'Post',
  props: {
    post: {}
  }
}
</script>

<style lang="css" scoped>
.post h1 {
  font-size: 1.5em;
  margin-bottom: 0;
}

.post .about {
  color: slategray;
  font-style: italic;
}
</style>
