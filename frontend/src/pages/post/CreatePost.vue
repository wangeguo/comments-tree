<template lang="html">
  <div class="post-create">
    <header>
      <h1>New Post</h1>
    </header>

    <InvalidMessage :errors="errors" :invalid="invalid" :message="message"/>

    <form @submit.prevent="create">
      <label for="content">Content</label>
      <textarea id="content" v-model="content" name="content"></textarea>
      <div class="actions">
        <input type="submit" value="Save">
        <span class="limiter">{{ 200 - content.length }} characters remaining</span>
      </div>
    </form>
  </div>
</template>

<script>
import PostService from '@/services/post'
import InvalidMessage from '@/components/InvalidMessage'

export default {
  name: 'CreatePost',
  components: {InvalidMessage},
  data () {
    return {
      invalid: false,
      message: '',
      errors: [],
      content: ''
    }
  },

  methods: {
    create () {
      PostService.create({
        content: this.content
      })
        .then(response => {
          this.$router.push({name: 'Home'})
        })
        .catch(e => {
          this.invalid = true
          this.message = e.response.data.message
          this.errors = e.response.data.errors
        })
    }
  },
  computed: {
    charactersLeft () {
      var char = this.content.length
      var limit = 200
      return (limit - char) + ' / ' + limit + 'characters remaining'
    }
  }
}
</script>

<style lang="css" scoped>
.actions {
  display: flex;
  flex-direction: row;
}

.actions .limiter {
  flex: auto;
  text-align: right;
}
</style>
