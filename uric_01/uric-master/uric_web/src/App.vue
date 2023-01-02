<template>
  <div id="nav">
    <a-locale-provider :locale="this.$settings.locale">
      <router-view/>
    </a-locale-provider>
  </div>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}


</style>
