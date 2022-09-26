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
        fetch('api/datetime')                       // Call http://localhost/api/datetime
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