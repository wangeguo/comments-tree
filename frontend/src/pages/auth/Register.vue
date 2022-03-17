<template>
  <div class="auth-register">
    <header>
      <h1>Register</h1>
    </header>

    <InvalidMessage :errors="errors" :invalid="invalid" :message="message"/>

    <form @submit.prevent="register">
      <label for="username">Username</label>
      <input id="username" v-model="username" name="username" required>
      <label for="email">Email</label>
      <input id="email" v-model="email" name="email" required>
      <label for="password">Password</label>
      <input id="password" v-model="password" name="password" required type="password">
      <input type="submit" value="Register">
    </form>
  </div>
</template>

<script>
import AuthService from '@/services/auth'
import InvalidMessage from '@/components/InvalidMessage'

export default {
  name: 'Register',
  components: {InvalidMessage},
  data () {
    return {
      invalid: false,
      message: '',
      errors: [],
      username: '',
      email: '',
      password: ''
    }
  },

  methods: {
    register () {
      AuthService.register({
        username: this.username,
        email: this.email,
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
