<template>
  <Form />
  <Search />
</template>

<script>
import Form from "./components/form.vue";
import Search from "./components/search.vue";

export default {
  name: "App",
  components: { Form, Search },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
