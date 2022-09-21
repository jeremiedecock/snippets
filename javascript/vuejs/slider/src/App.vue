<script>
export default {
  data() {
    return {
      foo: 100
    }
  }
}
</script>


<template>
  <!-- controls -->
  <div>
    <input type="range" v-model="foo" min="0" max="100">
    <span>{{foo}}</span>
  </div>
</template>


<style>
input {
  display: block;
  margin-bottom: 1em;
}
</style>