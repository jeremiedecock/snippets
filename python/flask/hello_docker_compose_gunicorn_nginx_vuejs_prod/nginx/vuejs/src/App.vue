<script>
export default {
  data() {
    return {
      message: 'Push the button just below to print a message from the REST API...'
    }
  },
  methods: {
    printMessage() {
      if(window.fetch) {
        fetch('http://127.0.0.1:8000/')
          .then(response => response.json())
          .then(data => {
              this.message = data.message
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
  <h1>{{ message }}</h1>
  <button @click="printMessage">Print current date time</button>
</template>


<style>
button {
  display: block;
  margin-bottom: 1em;
}
</style>