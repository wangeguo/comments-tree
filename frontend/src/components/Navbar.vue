<template lang="html">
  <nav>
    <h1><a href="/">Comments Tree</a></h1>
    <ul v-if="$store.state.isUserLoggedIn">
      <li><span>{{ $store.state.user.username }}</span></li>
      <li><a class="action" @click="logout()">Logout</a></li>
    </ul>
    <ul v-else-if="!$store.state.isUserLoggedIn">
      <li><router-link :to="{name: 'Register'}">Register</router-link></li>
      <li><router-link :to="{name: 'Login'}">Login</router-link></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    logout () {
      this.$store.dispatch('setToken', null)
      this.$store.dispatch('setUser', null)
      this.$router.push({name: 'Home'})
    }
  }
}
</script>

<style lang="css" scoped>
nav {
  background: lightgray;
  display: flex;
  align-items: center;
  padding: 0 0.5rem;
}

nav h1 {
  flex: auto;
  margin: 0;
}

nav h1 a {
  text-decoration: none;
  padding: 0.25rem 0.5rem;
}

nav ul  {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
}

nav ul li a, nav ul li span, header .action {
  display: block;
  padding: 0.5rem;
}

nav ul li a {
  cursor: pointer;
}
</style>
