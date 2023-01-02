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
          <span @click="showModal(record.id)">新建发布</span>
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
    }
  },
  created(){
    this.get_release_app_data();
  },
  methods:{
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
    showModal(record_id){
      console.log(record_id)
    }
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