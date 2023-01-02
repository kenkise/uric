<template>

  <div class="release">
    <div class="search">
      <a-row>
        <a-col :span="8">
          <a-form-item :label-col="formItemLayout.labelCol" :wrapper-col="formItemLayout.wrapperCol" label="环境名称：">
            <a-input placeholder="请输入"/>
          </a-form-item>
        </a-col>

        <a-col :span="8">
          <router-link to="/release">
            <a-button type="primary" icon="sync" style="margin-top: 3px;">刷新</a-button>
          </router-link>
        </a-col>
      </a-row>
    </div>
    <div>
      <a-button type="primary" @click="showModal"><a-icon type="plus"/>新建</a-button>
    </div>
    <div class="app_list">
      <a-table :columns="columns" :data-source="data" rowKey="id">
        <a slot="action" slot-scope="text" href="javascript:;">
          <router-link to="/">编辑</router-link>
          <span style="color: lightgray"> | </span>
          <router-link to="/">删除</router-link>
        </a>
      </a-table>
    </div>
    <div>
      <a-modal width="720px" v-model="visible" title="新建环境" @ok="handleOk">
        <a-form :form="form" :label-col="{ span: 5 }" :wrapper-col="{ span: 12 }" @submit="handleSubmit">
          <a-form-item label="环境名称">
            <a-input v-decorator="['name', { rules: [{ required: true, message: '请输入环境名称' }] }]"/>
          </a-form-item>
          <a-form-item label="唯一标识符">
            <a-input v-decorator="['tag', { rules: [{ required: true, message: '请输入唯一标识符' }] }]"/>
          </a-form-item>
          <a-form-item label="备注信息">
            <a-input type="textarea"/>
          </a-form-item>
        </a-form>
      </a-modal>
    </div>
  </div>
</template>
<script>

  const columns = [
    {title: '序号', dataIndex: 'id', key: 'id'},
    {title: '环境名称', dataIndex: 'name', key: 'name'},
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
    data() {
      return {
        name:'',
        tag:'',
        desc:'',
        formLayout: 'horizontal',
        form: this.$form.createForm(this, { name: 'coordinated' }),
        formItemLayout,
        columns,
        data:[],
        visible: false,
        visible1: false,
        current: 0,
        steps: [
          {
            title: 'First',
            content: '基本配置',
          },
          {
            title: 'Second',
            content: '发布主机',
          },
          {
            title: 'Last',
            content: '任务配置',
          },
        ],
      }
    },
    created() {
      this.get_envrionments_data();
    },
    methods: {
      get_envrionments_data(){
        let token = sessionStorage.token || localStorage.token;
        this.$axios.get(`${this.$settings.host}/conf_center/environment`,{
          headers:{
            Authorization: "jwt " + token,
          }
        })
        .then((res)=>{
          this.data = res.data;
        }).catch((error)=>{

        })
      },
      handleSubmit(e) {
        e.preventDefault();
          this.form.validateFields((err, values) => {
            if (!err) {
              let token = sessionStorage.token || localStorage.token;
              console.log('Received values of form: ', values);
              this.$axios.post(`${this.$settings.host}/conf_center/environment`,values,{
                headers:{
                  Authorization: "jwt " + token,
                }
              })
              .then((res)=>{
                this.$message.success('添加成功！')
                // console.log(res.data);
                this.data.push(res.data);
              }).catch((error)=>{

              })
              this.visible = false;

            }
          });
      },

      next() {
        this.current++;
      },

      prev() {
        this.current--;
      },

      showModal() {
        this.visible = true;
      },

      handleOk(e) {
        // console.log(e);
        this.handleSubmit(e);
      },
    },
  }
</script>
<style scoped>
  .xx_title:after {
    border: none;
  }
</style>