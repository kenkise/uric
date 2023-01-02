import zhCN from 'ant-design-vue/lib/locale-provider/zh_CN';
export default {  // 注意，对象要抛出后，其他文件中才能引入使用
  host:'http://api.uric.cn:8000', // 我们的后台项目将来就通过这个域名和端口来启动
  ws_host: "ws://api.uric.cn:8000", //weboscket服务端
  locale: zhCN, // 语言
}