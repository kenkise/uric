<template>

  <div class="release_apply">
    <!--    <h1>发布申请</h1>-->
    <div class="release_apply_category" style="display: flex;justify-content: space-between;">
      <a-radio-group :value="apply_category" @change="handleCategoryChange">
        <a-radio-button value="0">
          全部({{release_apply_data.length}})
        </a-radio-button>
        <a-radio-button :value="status_value[0]" v-for="(status_value,status_index) in release_apply_status_data" :key="status_index">
          {{status_value[1]}} ({{classify_release_apply_data[status_value[0]].length}})
        </a-radio-button>

      </a-radio-group>
      <a-button type="primary" icon="plus" @click="new_release_apply">
        新建发布申请
      </a-button>

    </div>

    <div class="choose_app">

      <a-modal v-model="choose_app_visible" title="选择应用" width="800px">
        <a-row>
          <a-col :span="6">
            <div>
              <a-menu
                :default-selected-keys="['1']"
                mode="inline"
                :inline-collapsed="collapsed"
                @select="envs_menu_change"
              >
                <a-menu-item :key="envs_value.id" v-for="(envs_value,envs_index) in envs_data" @click="change_env_event(envs_value.id)">
                  <a-icon type="pie-chart"/>
                  <span>{{envs_value.name}}</span>
                </a-menu-item>


              </a-menu>
            </div>
          </a-col>
          <a-col :span="18">
            <a-row type="flex" justify="space-around" align="middle">
              <a-col :span="8" :key="app_index" v-for="(app_value,app_index) in app_data">
                <p style="height: 80px;line-height: 80px;text-align: center">

                  <a-button @click="show_new_release_apply(app_value.release_app__id)" type="primary" style="height: 50px;width: 150px;">
                    {{app_value.release_app__name}}
                  </a-button>

                </p>
              </a-col>

            </a-row>
          </a-col>
        </a-row>


      </a-modal>
    </div>

    <div class="new_release_apply_modal">

      <a-modal v-model="new_release_visible" title="新建发布申请" width="800px" >
        <template slot="footer">
          <a-button key="back" @click="resetCreateApplyForm">
            取消
          </a-button>
          <a-button key="submit" type="primary" @click="onCreateApplySubmit">
            提交
          </a-button>
        </template>

        <div class="new_release_model_from">
          <a-form-model
            ref="ruleForm"
            :model="new_release_form_data.form"
            :rules="new_release_form_data.rules"
            :label-col="new_release_form_data.labelCol"
            :wrapper-col="new_release_form_data.wrapperCol"
          >
            <a-form-model-item ref="name" label="申请标题" prop="name">
              <a-input
                v-model="new_release_form_data.form.name"
                @blur="
          () => {
            $refs.name.onFieldBlur();
          }
        "
              />
            </a-form-model-item>
            <a-form-model-item label="选择分支/标签版本" prop="version">
              <a-input-group compact>

                <a-select style="width: 30%" v-model="new_release_form_data.form.git_release_branch_or_tag" default-value="1">

                  <a-select-option value="1">
                    branch
                  </a-select-option>
                  <a-select-option value="2">
                    Tag
                  </a-select-option>
                </a-select>
                <a-select style="width: 70%" v-model="new_release_form_data.form.git_release_version" default-value="1">
                  <a-select-option :value="branch_value" v-for="(branch_value, branch_index) in git_branchs" :key="branch_index">
                    {{branch_value}}
                  </a-select-option>

                </a-select>
              </a-input-group>
            </a-form-model-item>
            <a-form-model-item label="选择Commit ID" required prop="git_release_commit_id" v-if="new_release_form_data.form.git_release_branch_or_tag==='1'">
              <a-select v-model="new_release_form_data.form.git_release_commit_id" default-value="1">
                  <a-select-option :value="commit_info_index" v-for="(commit_info_value, commit_info_index) in git_branchs_commit_info" :key="commit_info_index">
                    {{commit_info_value}}>>>>{{commit_info_index}}
                  </a-select-option>

                </a-select>

            </a-form-model-item>


            <a-form-model-item label="备注信息" prop="description">
              <a-input v-model="new_release_form_data.form.description" type="textarea"/>
            </a-form-model-item>

          </a-form-model>
        </div>

      </a-modal>
    </div>
    <div class="release_apply_list" style="margin-top: 20px;">
      <a-table :columns="columns" :data-source="different_status_release_apply" rowKey="id">
        <a slot="action" slot-scope="text, record" v-if="record.release_status===1">
          <a-button size="small" @click="review_info(record.id)" type="link">审核</a-button> |
          <a-button size="small"  type="link">编辑</a-button> |
          <a-button size="small"  type="link">删除</a-button>
        </a>
         <a slot="action" slot-scope="text, record" v-else-if="record.release_status===2">
          <router-link :to="`/uric/release_result/${record.id}`">发布</router-link> |
          <a-button size="small"  type="link">查看</a-button>
        </a>
        <a slot="action" slot-scope="text, record" v-else-if="record.release_status===3">
          <a-button size="small" type="link">查看</a-button> |
          <a-button size="small"  type="link">回滚</a-button>
        </a>

        <a slot="action" slot-scope="text, record" v-else-if="record.release_status===4">
          <a-button size="small" type="link" style="color:Red;">快查看吧</a-button>

        </a>
        <a slot="action" slot-scope="text, record" v-else>
          <a-button size="small"  type="link">查看</a-button>
        </a>
      </a-table>
    </div>
    <!-- 审核发布代码记录的弹窗 -->
    <div class="review_modal">
      <a-modal v-model="review_visible" title="审核发布申请" @ok="handleReviewOk">
        <a-form-model ref="reviewForm" :model="review_data.form" :label-col="review_data.labelCol" :wrapper-col="review_data.wrapperCol">
          <a-form-model-item label="审核结果">
            <a-switch v-model="review_data.review_status"/>
          </a-form-model-item>

          <a-form-model-item label="审核意见">
            <a-input v-model="review_data.form.review_desc" type="textarea"/>
          </a-form-model-item>
        </a-form-model>
      </a-modal>
    </div>


  </div>


</template>

<script>
  const columns = [
    {title: '申请标题', width: 50, dataIndex: 'name', key: 'name',},
    {title: '应用', width: 50, dataIndex: 'app_name', key: 'app_name',},
    {title: '发布环境', dataIndex: 'envs_name', key: 'envs_name', width: 80},
    {title: '版本', dataIndex: 'git_release_commit_id', key: 'git_release_commit_id', width: 50},
    {title: '状态', dataIndex: 'get_release_status_display', key: 'get_release_status_display', width: 50},
    {title: '申请人', dataIndex: 'username', key: 'username', width: 50},
    {title: '申请时间', dataIndex: 'created_time', key: 'created_time', width: 100},

    {
      title: '操作',
      key: 'operation',
      width: 100,
      scopedSlots: {customRender: 'action'},
    },
  ];
  // const data = [];
  // for (let i = 0; i < 100; i++) {
  //   data.push({
  //     id: i,
  //     name: `Edrward ${i}`,
  //     age: 32,
  //     address: `London ${i}`,
  //   });
  // }
  export default {
    name: "ReleaseApply",
    data() {
      return {
        envs_data:[],  // 环境数据
        envs_id:1, // 所选环境的id值
        app_data:[],  // 应用数据
        release_apply_data:[],  // 发布申请数据
        classify_release_apply_data:{},  // 所有分类归纳的发布申请数据
        different_status_release_apply:[], // 点击不同分类时的 发布申请数据
        app_id:1, // 用户新建发布申请时选择的应用id
        release_apply_status_data:[],  // 发布申请状态数据

        // 根据分类划分出5个数据
        release_apply_data_1 : [], // 待审核数据
        release_apply_data_2 : [], // 待发布数据
        release_apply_data_3 : [], // 发布成功数据
        release_apply_data_4 : [], // 发布异常数据
        release_apply_data_5 : [], // 其他类型数据

        git_branchs:[], // 不同应用的新建发布对应的git仓库的分支信息
        git_branchs_commit_info:[], // 不同分支的commit版本信息，默认先获得master分支的，业务级别就定好有master分支


        columns,
        // data,
        apply_category: '0',  // 发布申请分类，默认为全部
        choose_app_visible: false,
        new_release_visible: false,

        collapsed: false, // 环境分类菜单栏数据属性

        new_release_form_data: {
          labelCol: {span: 4},
          wrapperCol: {span: 14},
          other: '',
          form: {
            name: '', // 申请标题
            git_release_branch_or_tag:'1',  // 申请选择的是git分支还是标签
            git_release_version:'master', // 分支/标签 的版本, 也就是我们选择哪个分支
            git_release_commit_id: '', // git的commit id 数据
            release_record:0,
            description: '',  // 备注信息
          },
          rules: {
            name: [
              {required: true, message: '请输入申请标题', trigger: 'blur'},
              {min: 1, max: 10, message: 'Length should be 1 to 10', trigger: 'blur'},
            ],
            git_release_branch_or_tag: [{required: true, message: '请选择分支还是标签', trigger: 'change'}],
            git_release_version: [{required: true, message: '请选择版本', trigger: 'change'}],

            git_release_commit_id: [{required: true, message: '请选择commit ID', trigger: 'change'}],

          },

        },

        review_visible: false, // 审核弹框显示或者隐藏
        review_data:{
          labelCol: { span: 4 },
          wrapperCol: { span: 14 },
          release_id:0,// 点击审核的申请记录id
          review_status: false, // 审核状态，
          form: {
            release_status: 1, // 审核状态为true时，它的值为2，表示待发布
            review_user:1,  // 审核用户的id
            review_desc: '',// 审核意见
          },
        },
      }
    },
    created() {
      this.get_envs_data();
      // this.get_app_data();
      this.change_env_event(); // 获取不同环境的应用，默认是测试环境，页面加载时触发一次，环境菜单切换时也触发
      this.get_release_apply_data();
      this.get_release_apply_status_data();
    },

    watch:{
      'new_release_form_data.form.git_release_version':function (val) {
        // this.get_branch_commit_history()
        // console.log('val', val);

        this.show_new_release_apply(); // 执行获取不同分支的版本数据

      }
    },

    methods: {

      // 切换环境时，展示对应的环境的应用
      change_env_event(){
        let token = sessionStorage.token || localStorage.token;
        this.$axios.get(`${this.$settings.host}/release/envs/apps`,{
          params:{
            envs_id:this.envs_id,
          }
        }, {
          headers:{
            Authorization: "jwt "+ token
          }
        }).then((res)=>{
          this.app_data = res.data.envs_apps_data;


        }).catch((error)=>{

        })


      },


      // 根据发布申请的状态，将发布申请数据进行分类,请求数据回来之后，就执行该方法
       classify_release_data_by_status(){
        this.release_apply_data_1 = []
        this.release_apply_data_2 = []
        this.release_apply_data_3 = []
        this.release_apply_data_4 = []
        this.release_apply_data_5 = []

        this.release_apply_data.forEach((k,v)=>{
           if (k.release_status === 1){
             this.release_apply_data_1.push(k);
           }
           else if (k.release_status === 2){
             this.release_apply_data_2.push(k);
           }
           else if (k.release_status === 3){
             this.release_apply_data_3.push(k);
           }
           else if (k.release_status === 4){
             this.release_apply_data_4.push(k);
           }
           else {
             this.release_apply_data_5.push(k);
           }

         });
        this.classify_release_apply_data['0'] = this.release_apply_data
        this.classify_release_apply_data['1'] = this.release_apply_data_1
        this.classify_release_apply_data['2'] = this.release_apply_data_2
        this.classify_release_apply_data['3'] = this.release_apply_data_3
        this.classify_release_apply_data['4'] = this.release_apply_data_4
        this.classify_release_apply_data['5'] = this.release_apply_data_5

       },

      // 点击新建发布的弹框中的确认按钮的效果，提交发布申请的数据
      onCreateApplySubmit() {
        this.$refs.ruleForm.validate(valid => {
          if (valid) {
            let token = sessionStorage.token || localStorage.token;
            this.$axios.post(`${this.$settings.host}/release/apply`,this.new_release_form_data.form,{
              headers:{
                Authorization: "jwt " + token
              }
            })
              .then((res)=>{
                this.release_apply_data.push(res.data);
                this.classify_release_data_by_status();
                this.different_status_release_apply = this.release_apply_data;
                this.resetCreateApplyForm();
              }).catch((error)=>{

            })

          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      // 点击新建发布的弹框中的取消按钮的效果
      resetCreateApplyForm() {
        this.$refs.ruleForm.resetFields();
        this.new_release_visible = false;
      },


      // 点击新建发布按钮的弹框效果
      new_release_apply() {
        this.choose_app_visible = true;
      },
      // 点击应用，弹出新建发布申请的弹框,获取该应用新建的最新发布对应的git仓库的分支信息和版本信息，默认先展示的是master分支相关信息
      show_new_release_apply(app_id=null) {
         console.log('app_id>> ',app_id);
         // 发送请求，获取分支数据以及不同分支的commits版本数据
        if (app_id){
          this.app_id = app_id;
        }

        this.$axios.get(`${this.$settings.host}/release/git/branch`,{
          params:{
            app_id: this.app_id,
            branchs:this.new_release_form_data.form.git_release_version,
          }
        }).then((res)=>{
          // res.data.branch_list -- ["dev" ,"master"]

          this.git_branchs = res.data.branch_list;
          this.git_branchs_commit_info = res.data.commits;
          this.new_release_form_data.form.release_record = res.data.release_record_id;
        }).catch((error)=>{

        })
        this.choose_app_visible = false;
        this.new_release_visible = true;
      },




      // // 点击新建发布的确认按钮效果
      // handle_new_release_apply(e) {
      //   console.log(e);
      //   this.new_release_visible = false;
      // },
      // 新建发布弹框中，选择不同环境的切换效果,antd官网中就有这个select事件如何使用
      envs_menu_change({item, key, selectedKeys}) {
        // console.log(item, key, selectedKeys);  key是环境id
        this.envs_id = key;
        this.change_env_event();


      },

      // 发布类型按钮点击切换效果
      handleCategoryChange(e) {

        this.apply_category = e.target.value;
        this.different_status_release_apply = this.classify_release_apply_data[this.apply_category]
        // console.log(0)
        console.log(this.apply_category, typeof this.apply_category);
      },

      // 获取所有环境数据
      get_envs_data(){
          let token = sessionStorage.token || localStorage.token;
        this.$axios.get(`${this.$settings.host}/conf_center/environment`, {
          headers:{
            Authorization: "jwt "+ token
          }
        })
        .then((res)=>{
          this.envs_data = res.data;
        }).catch((error)=>{

        })
      },


      // // 获取所有应用数据
      // get_app_data(){
      //   let token = sessionStorage.token || localStorage.token;
      //   this.$axios.get(`${this.$settings.host}/release/app`, {
      //     headers:{
      //       Authorization: "jwt "+ token
      //     }
      //   })
      //   .then((res)=>{
      //     this.app_data = res.data;
      //   }).catch((error)=>{
      //
      //   })
      // },
      // 获取所有发布申请数据

      get_release_apply_data(){
          let token = sessionStorage.token || localStorage.token;
        this.$axios.get(`${this.$settings.host}/release/apply`, {
          headers:{
            Authorization: "jwt "+ token
          }
        })
        .then((res)=>{
          this.release_apply_data = res.data;
          this.classify_release_data_by_status();
          this.different_status_release_apply = this.release_apply_data;
        }).catch((error)=>{

        })
      },

      // 获取所有发布申请的状态数据
      get_release_apply_status_data(){
          let token = sessionStorage.token || localStorage.token;
        this.$axios.get(`${this.$settings.host}/release/apply/status`, {
          headers:{
            Authorization: "jwt "+ token
          }
        })
        .then((res)=>{
          this.release_apply_status_data = res.data.status_data;
        }).catch((error)=>{

        })
      },

      // 点击审核,记录id值并弹出审核对话框
      review_info(release_id) {
        console.log('release_id>>>', release_id);
        // this.$axios.put()
        this.review_data.release_id = release_id;
        this.review_visible = true;
      },
      // 审核弹框中点击提交，发送请求，修改申请记录的状态为待发布
      handleReviewOk() {
        let release_status = 1
        if( this.review_data.review_status ){
          this.review_data.form.release_status = 2;
        }else{
          this.review_data.form.release_status = 5;
        }
        let token = sessionStorage.token || localStorage.token;
        this.$axios.patch(`${this.$settings.host}/release/release_ap/${this.review_data.release_id}/`, this.review_data.form,{
          headers:{
            Authorization: "jwt " + token,
          }
        })
        .then((res)=>{
          for(let data of this.release_apply_data){
            if(data.id === res.data.id){
              data.release_status = res.data.release_status
              data.review_desc    = res.data.review_desc
              data.review_user    = res.data.review_user
            }
          }
          this.classify_release_data_by_status();
          this.different_status_release_apply = this.release_apply_data;
          this.resetReviewApplyForm();
        }).catch((error)=>{

        })

      },

      resetReviewApplyForm() {
        this.review_data.review_status = false,
        this.review_data.form = {
            release_status: 1, // 审核状态为true时，它的值为2，表示待发布
            review_user:1,     // 审核用户的id
            review_desc: '',   // 审核意见
        }
        this.apply_category = '0';
        this.review_visible = false;
      },
    },
  }
</script>

<style scoped>

</style>