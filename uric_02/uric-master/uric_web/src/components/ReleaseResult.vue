<template>
  <div class="release_result">
    <h1>发布结果: </h1>
    <ul>
      <li :key="result_index" v-for="(result_value,result_index) in result_list">
        {{ result_value }}
      </li>

    </ul>
  </div>
</template>
<script>
export default {
  name: "ReleaseResult",
  data() {
    return {
      release_apply_id: 0,
      result_list: []
    }
  },
  created() {
    let ths = this;
    this.release_apply_id = this.$route.params.id
    let ws = new WebSocket(`${this.$settings.ws_host}/ws/release/${this.release_apply_id}/`);
    ws.onmessage = function (event) {
      console.log(':::', event.data);
      ths.result_list.push(event.data)
    }
  }

}
</script>

<style scoped>

</style>
