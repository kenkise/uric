<template>
  <div class="release">
    <div class="search">
      <a-row>
        <a-col :span="8">
          <a-form-item
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
            label="应用名称："
          >
            <a-input
              placeholder="请输入"
            />
          </a-form-item>
        </a-col>
        <a-col :span="8">
          <a-form-item
            :label-col="formItemLayout.labelCol"
            :wrapper-col="formItemLayout.wrapperCol"
            label="描述信息："
          >
            <a-input
              v-decorator="[
          'nickname',
          { rules: [{ required: true, message: 'Please input your nickname' }] },
        ]"
              placeholder="请输入"
            />
          </a-form-item>
        </a-col>
        <a-col :span="8">
          <router-link to="/release">
            <a-button type="primary" icon="sync" style="margin-top: 3px;">
              刷新
            </a-button>
          </router-link>
        </a-col>
      </a-row>
    </div>
    <div class="add_app">
      <a-button @click="showaddModal" icon="plus">新建应用</a-button>
      <a-modal v-model="addmodelvisible" title="新建应用" @ok="handleaddappOk">
        <a-form-model ref="addappruleForm" :model="app_form" :rules="add_app_rules" :label-col="labelCol" :wrapper-col="wrapperCol">
          <a-form-model-item ref="app_name" label="应用名称" prop="app_name">
            <a-input v-model="app_form.app_name" @blur=" () => { $refs.app_name.onFieldBlur(); }"/>
          </a-form-model-item>
          <a-form-model-item ref="tag" label="唯一标识符" prop="tag"><a-input v-model="app_form.tag" @blur=" () => { $refs.tag.onFieldBlur(); }"/>
          </a-form-model-item>
          <a-form-model-item label="备注信息" prop="app_desc">
            <a-input v-model="app_form.desc" type="textarea"/>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
    </div>
    <div class="app_list">
      <a-table :columns="columns" :data-source="app_data" :rowKey="record => record.id">
        <span class="release_btn" slot="action" slot-scope="record">
          <span @click="showModal(record)">新建发布</span>
          <span style="color: lightgray"> | </span>
          <span>克隆发布</span>
          <span style="color: lightgray"> | </span>
          <span>编辑</span>
          <span style="color: lightgray"> | </span>
          <span>删除</span>
        </span>
        <p slot="expandedRowRender" slot-scope="record, index, indent, expanded" style="margin: 0">
          {{ record.name }} {{expanded}}
        </p>
      </a-table>
    </div>
    <div class="create_new_release">

      <a-modal width="800px" v-model="visible" title="选择发布方式" @ok="handleOk" :footer="null">
        <div style="background-color: #ececec; padding: 20px;">
          <a-row :gutter="10">
            <a-col :span="10" :offset="1" @click="showModal1">
              <a-card :bordered="false" style="cursor: pointer;">
                <div style="display: flex;">
                  <div style="margin-right: 16px;">
                    <a-icon type="ordered-list" style="font-size: 36px; color: rgb(24, 144, 255);"/>
                  </div>
                  <div>
                    <div style="margin-bottom: 12px;font-weight: 500;font-size: 16px; color: rgba(0,0,0,.85);"><span>常规发布</span></div>
                    <div>由 uric 来控制发布的主流程，你可以通过添加钩子脚本来执行额外的自定义操作。</div>
                  </div>
                </div>
              </a-card>
            </a-col>
            <a-col :span="10" :offset="1">
              <a-card :bordered="false" style="cursor: pointer;">
                <div style="display: flex;">
                  <div style="margin-right: 16px;">
                    <a-icon type="build" style="font-size: 36px; color: rgb(24, 144, 255);"/>
                  </div>
                  <div>
                    <div style="margin-bottom: 12px;font-weight: 500;font-size: 16px; color: rgba(0,0,0,.85);"><span>自定义发布</span></div>
                    <div>你可以完全自己定义发布的所有流程和操作，uric 负责按顺序依次执行你记录的动作。</div>
                  </div>
                </div>
              </a-card>
            </a-col>
          </a-row>
        </div>
      </a-modal>
    </div>


    <!--    发布流程对话框 -->
    <div>
      <a-modal width="900px" v-model="visible1" :title="`新建常规发布 - ${release_app_name}`" @ok="handleOk" :footer="null">
        <div>
          <a-steps :current="current">
            <a-step v-for="item in steps" :key="item.title" :title="item.title"/>
          </a-steps>
          <div class="steps-content" style="margin-top: 20px;">
            <a-form-model ref="ruleForm" :model="form" :rules="rules" :label-col="labelCol" :wrapper-col="wrapperCol">
              <div class="basic_config" v-show="current===0">
                <a-form-model-item label="发布环境" prop="envrionment">
                  <a-select v-model="form.envrionment" placeholder="请选择发布环境">
                    <a-select-option :value="env_value.id" v-for="(env_value,env_index) in env_datas" :key="env_index">
                      {{env_value.name}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
                <a-form-model-item ref="git_addr" label="Git仓库地址" prop="git_addr">
                  <a-input v-model="form.git_addr" @blur=" () => { $refs.git_addr.onFieldBlur(); }"/>
                </a-form-model-item>
                <a-form-model-item label="发布审核" prop="delivery">
                  <a-switch @change="msg_notice" checked-children="开" un-checked-children="关"/>
                </a-form-model-item>
                <a-form-model-item label="发布审核" prop="delivery">
                  <a-input-group compact>
                    <a-select v-model="form.msg_type" :disabled="!msg_notice_status">
                      <a-select-option value="0">关闭</a-select-option>
                      <a-select-option value="1">钉钉</a-select-option>
                      <a-select-option value="2">短信</a-select-option>
                      <a-select-option value="3">邮件</a-select-option>
                    </a-select>
                    <a-auto-complete :disabled="!msg_notice_status" style="width: auto" @change="handleChange"/>
                  </a-input-group>
                  <span>应用审核及发布成功或失败结果通知</span>
                </a-form-model-item>
              </div>
              <div class="pub_host" v-show="current===1">
                <a-form-model-item ref="target_host_pub_path" label="目标主机部署路径:" prop="target_host_pub_path">
                  <a-input v-model="form.target_host_pub_path" @blur=" () => { $refs.target_host_pub_path.onFieldBlur(); }"/>
                  <span style="color:darkgrey">目标主机的应用根目录，例如：/var/www/html</span>
                </a-form-model-item>
                <a-form-model-item ref="target_host_repository_path" label="目标主机仓库路径" prop="target_host_repository_path">
                  <a-input v-model="form.target_host_repository_path" @blur=" () => { $refs.target_host_repository_path.onFieldBlur(); }"/>
                  <span style="color:darkgrey">此目录用于存储应用的历史版本，例如：/data/uric/repos</span>
                </a-form-model-item>
                <a-form-model-item ref="keep_history_count" label="保留历史版本数量" prop="keep_history_count">
                  <a-input v-model="form.keep_history_count" @blur=" () => { $refs.keep_history_count.onFieldBlur(); }"/>
                  <span style="color:darkgrey">早于指定数量的历史版本会被删除，以释放空间</span>
                </a-form-model-item>
                <a-form-model-item label="发布目标主机选择" prop="pub_target_host_choose">
                  <a-select @change="handleselectChange" mode="multiple" v-model="form.pub_target_host_choose" placeholder="please select your zone">
                    <a-select-option :value="host_value.id" v-for="(host_value,host_index) in hosts_data" :key="host_index">
                      {{host_value.name}}:{{host_value.ip_addr}}
                    </a-select-option>
                  </a-select>
                </a-form-model-item>
              </div>
              <div class="task_config" v-show="current===2">
                <a-row>
                  <a-col :span="11">
                    <div class="file_filter" style="margin-bottom: 20px;">
                      <div class="file_filter_head">
                        <span>文件过滤：</span>
                        <span>
                          <a-radio-group v-model="filefilterway" @change="filterfilteronChange">
                          <a-radio :value="1">
                            包含
                            <a-tooltip>
                              <template slot="title">仅将匹配文件放到目标主机</template>
                              <a-icon type="info-circle"/>
                            </a-tooltip>
                          </a-radio>
                          <a-radio :value="2">
                            排除
                            <a-tooltip>
                              <template slot="title">匹配文件将不会放到目标主机</template>
                              <a-icon type="info-circle"/>
                            </a-tooltip>
                          </a-radio>
                        </a-radio-group>
                        </span>
                      </div>
                      <div>
                        <editor v-model="file_filter_cmd_content" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                    <div class="before_code_check_out" style="margin-bottom: 20px;">
                      <div class="before_code_check_out_head">
                        <span>代码检出前执行：</span>
                        <span>
                          <a-tooltip>
                              <template slot="title">在部署了uric项目的服务器上执行，拉去代码之前可以执行任意指令</template>
                              <a-icon type="info-circle"/>
                            </a-tooltip>
                        </span>
                      </div>
                      <div>
                        <editor v-model="before_code_check_out_value" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                    <div class="before_release" style="margin-bottom: 20px;">
                      <div class="before_release_head">
                        <span>应用发布前执行：</span>
                        <span>
                          <a-tooltip>
                            <template slot="title">在发布的目标主机上运行，当前目录为目标主机上待发布的源代码目录，可执行任意自定义命令。</template>
                            <a-icon type="info-circle"/>
                          </a-tooltip>
                        </span>
                      </div>
                      <div>
                        <editor v-model="before_release_content" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                  </a-col>
                  <a-col :span="2">
                    <div style="margin-top: 37px;vertical-align: center;text-align: center;height: 100px;">
                      <a-icon style="font-size: 32px" type="setting"/><br><span>基础设置</span>
                    </div>
                    <div style="margin-top: 37px;vertical-align: center;text-align: center;height: 100px;">
                      <a-icon style="font-size: 32px" type="gitlab"/><br><span>代码检出</span>
                    </div>
                    <div style="margin-top: 37px;vertical-align: center;text-align: center;height: 100px;">
                      <a-icon style="font-size: 32px" type="swap"/><br><span>版本切换</span>
                    </div>
                  </a-col>
                  <a-col :span="11">
                    <div class="custom_global_variable" style="margin-bottom: 20px;">
                      <div class="custom_global_variable_head">
                        <span>自定义全局变量:</span>
                        <span>
                          <a-tooltip>
                              <template slot="title">uric 内置了一些全局变量，这些变量可以直接使用，请参考官方文档：<a href="#">全局变量</a></template>
                              <a-icon type="info-circle"/>
                            </a-tooltip>
                        </span>
                      </div>
                      <div>
                        <editor v-model="custom_global_variable" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                    <div class="after_code_check_out" style="margin-bottom: 20px;">
                      <div class="after_code_check_out_head">
                        <span>代码检出后执行:</span>
                        <span>
                          <a-tooltip>
                            <template slot="title">在部署 Uric 的服务器上运行，当前目录为检出后待发布的源代码目录，可执行任意自定义命令。</template>
                            <a-icon type="info-circle"/>
                          </a-tooltip>
                        </span>
                      </div>
                      <div>
                        <editor v-model="after_code_check_out_value" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                    <div class="after_release" style="margin-bottom: 20px;">
                      <div class="after_release_head">
                        <span>应用发布后执行：</span>
                        <span>
                          <a-tooltip>
                            <template slot="title">在发布的目标主机上运行，当前目录为已发布的应用目录，可执行任意自定义命令。</template>
                            <a-icon type="info-circle"/>
                          </a-tooltip>
                        </span>
                      </div>
                      <div>
                        <editor v-model="after_release_value" @init="editorInit" lang="html" theme="chrome" width="100%" height="100"></editor>
                      </div>
                    </div>
                  </a-col>
                </a-row>
              </div>
              <div class="steps-action">
                <a-button :disabled="next_status_control()" v-if="current < steps.length - 1" type="primary" @click="next">下一步</a-button>
                <a-button v-if="current == steps.length - 1" type="primary" @click="onSubmit">提交</a-button>
                <a-button v-if="current > 0" style="margin-left: 8px" @click="prev">上一步</a-button>
              </div>
            </a-form-model>
          </div>
        </div>
      </a-modal>
    </div>
  </div>
</template>

<script>
const columns = [
  {title: '应用名称', dataIndex: 'name', key: 'name'},
  {title: '标识符', dataIndex: 'tag', key: 'tag'},
  {title: '描述信息', dataIndex: 'description', key: 'description'},
  {title: '操作', dataIndex: '', key: 'x', scopedSlots: {customRender: 'action'}},
];
const formItemLayout = {
  labelCol: {span: 8},
  wrapperCol: {span: 12},
};
export default {
  name: "Release",
  data(){
    return {
      columns,
      formItemLayout,
      labelCol: {span: 6},
      wrapperCol: {span: 16},
      app_data:[],      // 应用列表
      env_datas:[],     // 发布环境数据
      addmodelvisible: false,   // 是否显示新建发布应用的弹窗
      app_form: {               // 新建发布应用的表单数据
        app_name: '',
        tag: '',
        app_desc: '',
      },
      add_app_rules: {  // 添加发布应用的表单数据验证规则
        app_name: [
          {required: true, message: '请输入应用名称', trigger: 'blur'},
          {min: 1, max: 30, message: '应用名称的长度必须在1~30个字符之间', trigger: 'blur'},
        ],
        tag: [
          {required: true, message: '请输入应用唯一标识符', trigger: 'blur'},
          {min: 1, max: 50, message: '应用名称的长度必须在1~50个字符之间', trigger: 'blur'},
        ],
      },
      release_app_id: 0,    // 新建发布时从属的应用id
      release_app_name: "", // 新建发布时从属的应用名称
      hosts_data:[],      // 主机数据
      msg_notice_status: false,
      filefilterway: 1,
      file_filter_cmd_content: '',
      before_code_check_out_value: '',
      before_release_content: '',
      custom_global_variable: '',
      after_code_check_out_value: '',
      after_release_value: '',
      visible: false,  // 显示新建发布弹窗
      visible1: false, // 显示发布流程配置弹窗
      current: 0,      // 当前发布流程配置的步骤下标
      steps: [         // 发布流程步骤提示
          {
            title: '基本配置',
            content: '基本配置',
          },
          {
            title: '发布主机',
            content: '发布主机',
          },
          {
            title: '任务配置',
            content: '任务配置',
          },
      ],
      form: { // 新建发布流程的表单数据
          git_addr: '',
          envrionment: undefined,
          msg_type: '0',
          msg_content: '',
          target_host_pub_path: '',
          target_host_repository_path: '',
          keep_history_count: '',
          // pub_target_host_choose:[],
          pub_target_host_choose: undefined,

      },
      rules: {  // 新建发布流程的表单验证规则
          git_addr: [
            {required: true, message: '请输入git地址', trigger: 'blur'},
            {min: 1, max: 64, message: 'Length should be 1 to 64', trigger: 'blur'},
          ],
          target_host_pub_path: [
            {required: true, message: 'Please input Activity name', trigger: 'blur'},
            {min: 3, max: 32, message: 'Length should be 3 to 5', trigger: 'blur'},
          ],
          target_host_repository_path: [
            {required: true, message: 'Please input Activity name', trigger: 'blur'},
            {min: 3, max: 32, message: 'Length should be 3 to 5', trigger: 'blur'},
          ],
          keep_history_count: [
            {required: true, message: 'Please input Activity name', trigger: 'blur'},
            {min: 1, max: 5, message: 'Length should be 3 to 5', trigger: 'blur'},
          ],
          envrionment: [{required: true, message: '请选择环境', trigger: 'change'}],
          pub_target_host_choose: [{required: true, message: '请选择主机', trigger: 'change'}],
        },
    }
  },
  created(){
    this.get_envrionments_data()
    this.get_release_app_data();
  },
  watch:{
    // 切换环境时，触发主机数据的筛选
    'form.envrionment': function(){
      this.get_host_list(this.form.envrionment);
    }
  },
  methods:{
    get_host_list(env) {
      // 获取所选环境对应的主机列表
      let token = sessionStorage.token || localStorage.token;
      this.$axios.get(`${this.$settings.host}/host/list`,{
        params: {
          env: env,
        },
        headers: {
          Authorization: "jwt " + token,
        }
      }).then((res) => {
          this.hosts_data = res.data;
        })

    },
    // 获取所有环境数据
    get_envrionments_data(){
      let token = sessionStorage.token || localStorage.token;
      this.$axios.get(`${this.$settings.host}/conf_center/environment`,{
        headers: {
          Authorization: "jwt " + token,
        }
      })
      .then((res)=>{
        this.env_datas = res.data;
      }).catch((error)=>{

      })
    },
    get_release_app_data(){
      let token = sessionStorage.token || localStorage.token;
      this.$axios.get(`${this.$settings.host}/release/app`,{
        headers: {
          Authorization: "jwt " + token,
        }
      })
      .then(response=>{
        this.app_data = response.data;
      }).catch((error)=>{
        console.log(error.response.data)
      })
    },
    // 添加应用
    showaddModal() {
      this.addmodelvisible = true;
    },
    handleaddappOk(e) {
      this.$refs.addappruleForm.validate(valid => {
        if (valid) {
          let data = {
            name:this.app_form.app_name,
            tag:this.app_form.tag,
            description:this.app_form.desc,
          }
          let token = sessionStorage.token || localStorage.token;
          this.$axios.post(`${this.$settings.host}/release/app`,data,{
            headers: {
              Authorization: "jwt " + token,
            }
          })
          .then((res)=>{
            this.app_data.push(res.data);
            this.$message.success('添加成功');
            this.addmodelvisible = false;
          }).catch((error)=>{

          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    showModal(record){
      this.release_app_id = record.id;      // 记录本次发布的应用ID
      this.release_app_name = record.name;  // 记录本次发布的应用名称
      this.visible = true;
    },
    handleOk(e) {
      console.log(e);
      this.visible = false;
    },
    showModal1() {
      this.visible = false;
      this.visible1 = true;
    },
    // 消息通知开启和关闭切换
    msg_notice(value) {
      console.log('>>>>>', value);
      this.msg_notice_status = value;
    },
    // 控制下一步按钮的状态
    next_status_control() {
      if (this.current === 0 && (this.form.git_addr === '' || this.form.envrionment === undefined)) {
        return true
      } else if (this.current === 1 && (this.form.target_host_pub_path === '' || this.form.target_host_repository_path === '' || this.form.keep_history_count === '' || this.form.pub_target_host_choose === undefined)) {
        return true
      }
    },
    handleChange(value) {
      if (!value && this.msg_type !== 0) {
        this.$message.error('不能为空')
      } else {
        this.form.msg_content = value;
      }
    },
    onSubmit() {
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          let data = {
            release_app_id:this.release_app_id,
            // 基础配置
            envs_id: this.form.envrionment,
            code_git_addr: this.form.git_addr,
            msg_notice_status: this.msg_notice_status,
            msg_type: parseInt(this.form.msg_type),
            msg_content: this.form.msg_content,

            // 发布主机
            target_host_pub_path: this.form.target_host_pub_path,
            target_host_repository_path: this.form.target_host_repository_path,
            keep_history_count: this.form.keep_history_count,
            pub_target_host_choose: this.form.pub_target_host_choose,

            // 任务配置
            filefilterway:this.filefilterway, // 文件过滤方式 1表示包含 2表示过滤
            file_filter_cmd_content: this.file_filter_cmd_content,
            before_code_check_out_value: this.before_code_check_out_value,
            before_release_content: this.before_release_content,
            custom_global_variable: this.custom_global_variable,
            after_code_check_out_value: this.after_code_check_out_value,
            after_release_value: this.after_release_value,

          }
          console.log(data);
          this.$axios.post(`${this.$settings.host}/release/new`,data).then((res)=>{
            this.visible1 = false;
            this.$message.success('新建发布成功！');
          }).catch((error)=>{
            this.$message.error(`新建发布失败！原因：${error.response.data}`);
          })
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    editorInit: function () {
      require('brace/ext/language_tools') //language extension prerequsite...
      require('brace/mode/html')
      require('brace/mode/javascript')    //language
      require('brace/mode/less')
      require('brace/theme/chrome')
      require('brace/snippets/javascript') //snippet
    },
    filterfilteronChange(e) {
      console.log('radio checked', e.target.value);
    },

    handleselectChange(pub_target_host_choose) {
      this.pub_target_host_choose = pub_target_host_choose;
    },
    next() {
      this.current++;
    },
    prev() {
      this.current--;
    },

  },
  components: {
    editor: require('vue2-ace-editor')
  },
}
</script>

<style scoped>
.release_btn span{
  color: #1890ff;
  cursor: pointer;
}
</style>