<script>
export default {
  data() {
    return {
      foo: 'bonjour'
    }
  }
}
</script>


<template>
  <select v-model="foo">
    <option value="bonjour">Bonjour</option>
    <option value="hello">Hello</option>
  </select>

  <p>{{ foo }}</p>
</template>


<style>
</style>