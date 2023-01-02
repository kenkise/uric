<template>
  <div class="show_center">
    <h1>展示中心页面</h1>
    <a-button type="danger">
      Danger
    </a-button>

    <div class="calendar">
      <div :style="{ width: '300px', border: '1px solid #d9d9d9', borderRadius: '4px' }">
        <a-calendar :fullscreen="false" @panelChange="onPanelChange"/>
      </div>
    </div>
    <div class="echarts">
      <div ref="main" style="height: 500px;width: 400px;"></div>
    </div>


  </div>

</template>

<script>
export default {
  name: "ShowCenter",
  created() {
    // console.log("host:::", this.$settings.host);
    // this.$axios.get("http://wthrcdn.etouch.cn/weather_mini?city=北京",).then(response => {
    //   console.log(response.data.data.forecast);
    // })
  },
  mounted() {
    this.show_echarts();
  },
  methods: {
    onPanelChange(value, mode) {
      console.log(value, mode);
    },
    show_echarts() {
      var myChart = this.$echarts.init(this.$refs.main);
      // 绘制图表
      myChart.setOption({
        title: {
          text: 'ECharts 入门示例'
        },
        tooltip: {},
        xAxis: {
          data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }]
      });
    }
  },
}
</script>

<style scoped>
.show_center .echarts, .calendar {
  display: inline-block;
  float: left;
  margin-left: 40px;

}
</style>