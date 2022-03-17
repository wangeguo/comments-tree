<template lang="html">
  <div v-if="invalid" class="error">
    <h3 class="message">{{ message }}</h3>
    <dl v-for="(value, key) in errors" :key="key">
      <dt>{{key}}</dt>
      <dd v-for="v in value" :key="v">{{v}}</dd>
    </dl>
  </div>
</template>

<script>
export default {
  name: 'InvalidMessage',
  props: {
    invalid: false,
    message: '',
    errors: []
  }
}
</script>

<style lang="css" scoped>
.error {
  background-color: rgba(204, 47, 46, 0.24);
  padding: 10px;
}
.error h3 {
  color: red;
  padding: 0;
  margin: 0;
}
</style>
