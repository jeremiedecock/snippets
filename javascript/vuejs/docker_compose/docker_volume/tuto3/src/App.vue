<script>
export default {
  created() {
    // Simple GET request using fetch
    fetch("https://api.npms.io/v2/search?q=vue")
      .then(response => response.json())
      .then(data => (this.totalVuePackages = data.total));
  }
}
</script>

<template>
  <h1>VueJS + Fetch example</h1>
  Total number of views for VueJS on NPM: {{ totalVuePackages }}
</template>