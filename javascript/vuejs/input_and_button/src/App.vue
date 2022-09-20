<script>
export default {
  data() {
    return {
      message: 'Enter a message then push the button just above',
      foo: ''
    }
  },
  methods: {
    bar() {
      this.message = this.foo
    }
  }
}
</script>


<template>
  <div><input v-model="foo" placeholder="Foo"></div>

  <div class="buttons">
    <button @click="bar">Bar</button>
  </div>

  <h1>{{ message }}</h1>
</template>


<style>
input {
  display: block;
  margin-bottom: 1em;
}

button {
  display: block;
  margin-bottom: 1em;
}
</style>