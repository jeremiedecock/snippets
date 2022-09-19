<script>
export default {
  data() {
    return {
      message: 'Push the button just below to print the current date time from a public REST API...'
    }
  },
  methods: {
    printDateTime() {
      if(window.fetch) {
        fetch('http://worldclockapi.com/api/json/utc/now')
          .then(response => response.json())
          .then(data => {
              this.message = data.currentDateTime
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
  <button @click="printDateTime">Print current date time</button>
</template>


<style>
button, a {
  display: block;
  margin-bottom: 1em;
}
</style>