<template>
    <div class="show_center">
      <h1>展示中心页面</h1>
      <a-button type="primary">
        Primary
      </a-button>
      <a-date-picker @change="onChange" />
      <div ref="main" style="height: 500px;width: 500px;"></div>
    </div>
</template>

<script>

export default {
  name: "ShowCenter",
  data(){
    return {
    }
  },
  created(){
    console.log(this.$settings.host)
  },
  mounted() {
    this.show_echarts();
  },
  methods:{
    onChange(date, dateString) {
      console.log(date, dateString);
    },
    show_echarts(){
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
  }
}
</script>

<style scoped>

</style>