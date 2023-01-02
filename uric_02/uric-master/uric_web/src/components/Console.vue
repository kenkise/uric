<template>
  <div class="console">
    <div class="console_header">
      <div class="info">
        {{host_info.name}} | {{host_info.username}}@{{host_info.ip_addr}}:{{host_info.port}}
      </div>
      <div class="file_part">
        <button type="button" class="ant-btn ant-btn-primary" @click="showDrawer">
          <a-icon type="folder-open"/>
          文件管理器
        </button>
      </div>
    </div>

    <div class="file_show">

      <div>

        <a-drawer
          title="文件管理器"
          :width="900"
          :visible="visible"
          :body-style="{ paddingBottom: '80px' }"
          @close="onClose"
        >
          <div class="file_nav">
            <div>
              <a-breadcrumb>
                <a-breadcrumb-item>
                  <a-icon @click="back_folder('/',1)" type="home"/>
                </a-breadcrumb-item>

                <a-breadcrumb-item v-for="(folder_path,f_index) in path" :key="f_index" v-show="folder_path!=='/'">
                  <span style="cursor: pointer;" @click="back_folder(folder_path,f_index)">{{folder_path}}</span>
                </a-breadcrumb-item>
              </a-breadcrumb>
            </div>
            <div style="display: flex; align-items: center;">
              <span>显示隐藏文件：</span>
              <a-switch @change="switch_on_off" checked-children="开" un-checked-children="关"/>
              <div style="margin-left: 10px">
                <a-upload
                  name="file"
                  :multiple="true"
                  :action="visit_url+'?folder_path=' + folder_path_str"
                  :headers="headers"
                  @change="handleChange"
                >
                  <a-button type="primary">
                    <a-icon type="upload"/>
                    上传文件
                  </a-button>
                </a-upload>
              </div>

            </div>


          </div>
          <div>
            <a-table
              :columns="columns"
              :data-source="data"
              :pagination="false"
              :scroll="{ y: 400 }"
            >

              <a slot="name" slot-scope="text,record"> <!-- record表示该条记录，是个字典 -->
                <span @click="join_folder(text)" v-if="record.file_attr.substr(0,1)==='d'">
                  <a-icon type="folder"/>
                {{ text }}
                </span>
                <span v-else>
                  <a-popconfirm placement="top" ok-text="下载" cancel-text="取消" @confirm="confirm(text)">
                    <template slot="title">
                      <p>确认下载该文件吗？</p>
                      <p>{{ text }}</p>
                    </template>

                      <a-icon type="file"/>
                      {{ text }}

                  </a-popconfirm>
                </span>
              </a>
            </a-table>
          </div>
        </a-drawer>
      </div>
    </div>


    <div id="terminal"></div>
  </div>
</template>

<script>
import { Terminal } from 'xterm'


  const columns = [

    {
      title: '名称',
      dataIndex: 'file_name',
      width: 300,
      scopedSlots: {customRender: 'name'},
    },
    {
      title: '大小',
      dataIndex: 'file_size',

    },
    {
      title: '修改时间',
      dataIndex: 'file_modify_time',
      width: 200,
    },
    {
      title: '属性',
      dataIndex: 'file_attr',
      width: 150,
      scopedSlots: {customRender: 'file_attr'},
    },
    {
      title: '操作',
      dataIndex: 'action',
    },
  ];


export default {
  name: "Console",
  data(){
    return {
      visible: false, // 控制抽屉的显示隐藏
      host_info: {
        id: 0,
      },
      headers: {
        authorization: 'authorization-text',
      },
      data: [],
      columns,
      path: ['/',], // 默认是根路径，获取根路径下所有的文件和文件夹 ls-l /
      ls_cmd: "\\ls -l -h --time-style '+%Y/%m/%d %H:%M:%S'",
      folder_path_str: '/',
      visit_url:'',
    }
  },
  mounted() {
    this.show_terminal()
  },
  methods:{
    // 拼接访问的目录路径
    join_folder(text) {
      this.file_folder_list = [];
      if (text === '/') {
        this.path = ['/',]
      } else {
        this.path.push(text);
      }

      let folder_path = this.path.join('/');
      // folder_path = '/'
      if (this.path.length > 1) {
        folder_path = folder_path.slice(1);
      }

      this.folder_path_str = folder_path;

      this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);

    },

    // 发送ls指令
    send_show_folder_cmd(folder_path, cmd) {
        this.$axios.get(this.visit_url, {
          params: {
            cmd: `${cmd} ${folder_path}`,
          }
        }).then((response) => {
          console.log('>>>>>>',this.folder_path_str);
          console.log('>>>>>>',response);
          this.data = [];
          let data = response.data;
          // console.log(data);
          let data_l = data[1].split('\n').slice(1);

          // console.log('///',data_l);
          data_l.forEach((file_info, file_index) => {
            // console.log(v);
            if (file_info) {
              // console.log(file_info,file_index);
              //["drwxr-xr-x", "2", "root", "root", "4096", "2020/09/14", "17:34:06", "bin"]
              let files_list = file_info.trim().split(/\s+/);
              // console.log(files_list);
              let a_list = files_list.slice(5, 7);
              let timer = a_list.join(' ');

              this.data.push({
                key: `${files_list[7] + 1}`,
                file_name: files_list[7],  //[-1]， 不支持负数索引
                file_size: files_list[4],
                file_modify_time: timer,
                file_attr: files_list[0],
              })
            }
          })
          // this.file_folder_list = this.file_folder_list.concat(data_l_2);
        }).catch((error) => {
          console.log('报错啦！！！');
        })
      },

      // 显示隐藏文件和隐藏显示文件
      switch_on_off(e) {
        // console.log('>>>',e);  // true\false
        if (e) {
          // 开启显示隐藏文件
          this.ls_cmd = `\\ls -l -h -a --time-style '+%Y/%m/%d %H:%M:%S'`
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);
        } else {
          // 关闭显示隐藏文件
          this.ls_cmd = `\\ls -l -h --time-style '+%Y/%m/%d %H:%M:%S'`
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);
        }
      },
    back_folder(text, f_index){
      // 返回上级目录
      // this.path = this.path.slice(0,f_index+1);
      this.path = this.path.slice(0, f_index);
      this.join_folder(text);
    },
    showDrawer(){
       // 显示文件管理器的抽屉
      this.visible = true;
      this.visit_url = `${this.$settings.host}/host/file/${this.$route.params.id}/`;
      this.join_folder('/');
    },
    onClose() {
      // 关闭抽屉
      this.visible = false;
    },

    handleChange(info) {
        if (info.file.status !== 'uploading') {
          // console.log(info.file, info.fileList);

        }
        if (info.file.status === 'done') {
          this.send_show_folder_cmd(this.folder_path_str, this.ls_cmd);
          this.$message.success(`${info.file.name} file uploaded successfully`);
        } else if (info.file.status === 'error') {
          this.$message.error(`${info.file.name} file upload failed.${info.file.response.error}`);
        }
    },
    show_terminal(){
      // 获取当前本次操作的远程主机信息
      let pk = this.$route.params.id;
      let token = sessionStorage.token || localStorage.token;
      this.$axios.get(`/host/list/${pk}/`,{
        headers:{
          Authorization: `jwt ${token}`,
        }
      }).then((response) => {
        this.host_info = response.data;
        console.log(this.host_info)
      })

      // 初始化terminal窗口
       var term = new Terminal({
           rendererType: "canvas", //渲染类型
           rows: 40, //行数
           convertEol: true, // 启用时，光标将设置为下一行的开头
           scrollback: 100,   // 终端中的回滚量
           disableStdin: false, //是否应禁用输入。
           cursorStyle: 'underline', //光标样式
           cursorBlink: true, //光标闪烁
           theme: {
             foreground: '#ffffff', //字体
             background: '#060101', //背景色
             cursor: 'help',//设置光标
           }
       });
       // 建立websocket
       let ws = new WebSocket(`ws://api.uric.cn:8000/ws/ssh/${this.$route.params.id}/`);
       var keyWord = '';  // 拼接用户输入的内容
       let msg = ""
      // 监听接收来自服务端响应的数据
       ws.onmessage = function (event) {
        if (!keyWord){
          //所要执行的操作
          term.write(event.data);
        }else {
          keyWord=''
          // 对响应回来的数据进行一些加工处理，筛选出结果内容部分
          let a = event.data.replace(event.data.split('\r\n',1)[0],'');
          let b = a.split('\r\n',-1).slice(0,-1).join('\r\n');
          term.write('\r\n'+b)
        }
      }

      term.prompt = () => {
        term.write('\r\n');
        // term.write('\r\n$ ')
        msg = '';
      }

      term.onKey(e => {
        console.log(e)
        const ev = e.domEvent
        const printable = !ev.altKey && !ev.altGraphKey && !ev.ctrlKey && !ev.metaKey

        console.log('>>>>',ev.keyCode);
        if (ev.keyCode === 13) {
          // console.log(keyWord);
          // 按下回车键进行指令的发送
          ws.send(keyWord);

        } else if (ev.keyCode === 8) {
          // Do not delete the prompt
          if (term._core.buffer.x > 2) {
            term.write('\b \b')
          }
        } else if (printable) {
          term.write(e.key);
          keyWord += e.key
        }
      })

       term.open(document.getElementById('terminal'));

    }
  }
}
</script>

<style scoped>
.console_header{
  height: 60px;
  line-height: 60px;
}
.info{
  float: left;
}
.file_part{
  float: right;
  margin-right: 18px;
}
</style>