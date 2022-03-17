<template lang="html">
  <div class="auth-login">
    <header>
      <h1>Log In</h1>
    </header>

    <InvalidMessage :errors="errors" :invalid="invalid" :message="message"/>

    <form @submit.prevent="login">
      <label for="username">Username</label>
      <input id="username" v-model="username" name="username" required>
      <label for="password">Password</label>
      <input id="password" v-model="password" name="password" required type="password">
      <input type="submit" value="Log In">
    </form>
  </div>
</template>

<script>
import AuthService from '@/services/auth'
import InvalidMessage from '@/components/InvalidMessage'

export default {
  name: 'Login',
  components: {InvalidMessage},
  data () {
    return {
      invalid: false,
      message: '',
      errors: [],
      username: '',
      password: ''
    }
  },

  methods: {
    login () {
      AuthService.login({
        username: this.username,
        password: this.password
      })
        .then(response => {
          this.$store.dispatch('setToken', response.data.token)
          this.$store.dispatch('setUser', response.data.user)
          this.$router.push({name: 'Home'})
        })
        .catch(e => {
          this.invalid = true
          this.message = e.response.data.message
          this.errors = e.response.data.errors
        })
    }
  }
}
</script>
