<script>
export default {
  data() {
    return {
      message: 'Enter a GitHub project name (e.g. nodejs) then push the button just above to print its properties from the GitHub public REST API...',
      foo: ''
    }
  },
  methods: {
    bar() {
      if(window.fetch) {
        fetch('https://api.github.com/orgs/' + this.foo)
          .then(response => response.json())
          .then(data => {
              this.message = data
          })
          .catch(error => console.error(error))
      } else {
          this.message = "Fetch is not available";
      }
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