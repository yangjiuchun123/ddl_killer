<template>
<div class="app-container">
  <v-app>
    <v-row class="fill-height">
      <v-tabs vertical>
        <v-tab>
          <v-icon left>mdi-settings</v-icon>基础设置
        </v-tab>
        <v-tab>
          <v-icon left>mdi-account</v-icon>个人信息
        </v-tab>

        
        <v-tab-item>
          <v-list shaped>
            <v-subheader>Email通知</v-subheader>
            <v-list-item-group
              v-model="settings"
              multiple
            >
              <template v-for="(item, i) in emailSets">
                <v-divider
                  v-if="!item"
                  :key="`divider-${i}`"
                ></v-divider>

                <v-list-item
                  v-else
                  :key="`item-${i}`"
                  :value="item"
                  active-class="blue--text text--accent-4"
                  @click="isInit = true"
                >
                  <template v-slot:default="{ active, toggle}">
                    <v-list-item-action disabled>
                      <v-checkbox
                        :input-value="active"
                        :true-value="item"
                        color="blue accent-4"
                        @click="toggle"
                      ></v-checkbox>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title v-text="item"></v-list-item-title>
                    </v-list-item-content>
                  </template>
                </v-list-item>
              </template>
            </v-list-item-group>
            <v-list-item>
              <v-list-item-title>更多功能正在探索中💭 敬请期待👍</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-tab-item>

        <v-tab-item>
          <v-form ref="userForm" class="pa-4 pt-6">
            <v-text-field
              v-model="userForm.name"
              label="用户名"
              outlined
              shaped
              :rules="[rules.required]"
              :readonly="!isChangeName"
              :append-icon="!isChangeName ? 'mdi-border-color' : 'mdi-check'"
              @click:append="isChangeName = !isChangeName"
            ></v-text-field>
            <el-tooltip class="item" effect="light" content="Top Center 提示文字" placement="top">
                <div slot="content" ><p style="color: #E6A23C">学号是验证你的唯一信息，不允许修改哦😀</p></div>
                <v-text-field
                v-model="userForm.uid"
                label="学号"
                outlined
                shaped
                readonly
                ></v-text-field>
            </el-tooltip>
            <el-tooltip class="item" effect="light" content="Top Center 提示文字" placement="top">
                <div slot="content" ><p style="color: #E6A23C">如果收信箱内找不到邮件的话，可能被处理到垃圾箱🗑️了呢</p></div>
            <v-text-field
              v-model="userForm.email"
              label="提醒邮箱"
              outlined
              shaped
              :rules="[rules.email, rules.required]"              
              :readonly="!isChangeEmail"
              :append-icon="!isChangeEmail ? 'mdi-border-color' : 'mdi-check'"
              @click:append="isChangeEmail = !isChangeEmail"
            ></v-text-field>
            </el-tooltip>
            
            <el-tooltip class="item" effect="light" content="Top Center 提示文字" placement="top">
                <div slot="content" ><p style="color: #E6A23C">没有确认密码，所以看清楚再改哦🤣</p></div>
            <v-text-field
              v-model="userForm.password"
              :label="!isChangePassword ? '修改密码' : '修改密码为'"
              outlined
              shaped
              :type="isShow? 'text' : 'password'"
              :readonly="!isChangePassword"
              :append-outer-icon="!isChangePassword ? 'mdi-border-color' : 'mdi-check'"
              :append-icon="!isShow ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-outer="isChangePassword = !isChangePassword"
              @click:append="isShow = !isShow"
            ></v-text-field>
            </el-tooltip>
          </v-form>

          <v-divider></v-divider>

          <v-card-actions>
            <v-btn text @click="OnUserInfoClear">清空信息</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              class="white--text"
              color="blue accent-4"
              depressed
              :disabled="isChangeEmail||isChangeName||isChangePassword"
              @click="OnUserInfoSubmit"
            >保存修改</v-btn>
          </v-card-actions>
        </v-tab-item>

      </v-tabs>
    </v-row>
  </v-app>
</div>
</template>

<script>
  import {getUserInfo, modifyUserInfo, getUserSetting, modifyUserSetting} from '@/api/user';

  export default {
    data: () => ({
      isChangeName : false,
      isChangeEmail: false,
      isChangePassword: false,
      isShow: false,

      rules: {
        required: value => !!value || 'Required.',
        counter: value => value.length <= 20 || 'Max 20 characters',
        email: value => {
          const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
          return pattern.test(value) || 'Invalid e-mail.'
        },
      },

      userForm: {
        uid: '',
        name: '',
        email: '',
        password: '',
      },

      emailSets: [
        'DDL提醒',
        '团体日程提醒',
        //'',
        '共享资源更新提醒',
      ],
      settings: [],

      isInit: false,
    }),

    created () {
      this.initialize()
    },

    watch: {
      "settings": {
        handler(newVal){
          // console.log("change")
          // console.log(newVal)
          var t_setting = {
            ddl_alert: false,
            participate_alert: false,
            resource_alert: false
          }
          for (let i=0;i<newVal.length;i=i+1) {
            if (newVal[i]=="DDL提醒") t_setting.ddl_alert = true
            if (newVal[i]=="团体日程提醒") t_setting.participate_alert = true
            if (newVal[i]=="共享资源更新提醒") t_setting.resource_alert = true
          }
          console.log(t_setting)
          if(this.isInit) {
            modifyUserSetting(this.$store.getters.uid, t_setting).then(res => {
              // this.$message('修改成功!')
              // console.log("succeed")
              // console.log(res)
              }).catch(error => {
              console.log(error)
            })
          }

        },
      }
    },

    methods:{
      initialize () {
        getUserInfo(this.$store.getters.uid).then(res => {
          this.userForm.uid = res.uid
          this.userForm.name = res.name
          this.userForm.email = res.email
          // console.log(res)
        })
        this.settings = []
        getUserSetting(this.$store.getters.uid).then(res => {
          
          // console.log(res.data[0].ddl_alert)
          // console.log(res.data[0].participate_alert)
          // console.log(res.data[0].resource_alert)
          if (res.data[0].ddl_alert) this.settings.push("DDL提醒")
          if (res.data[0].participate_alert) this.settings.push("团体日程提醒")
          if (res.data[0].resource_alert) this.settings.push("共享资源更新提醒")
          // console.log('---------------------------')
          // console.log(res)
          // console.log(this.settings)
        })
      },

      OnUserInfoSubmit() {//传输数据到后台
        var valid = this.$refs.userForm.validate()
        if(valid) {
          //向后端传数据
          modifyUserInfo(this.$store.getters.uid, this.userForm).then(res => {
            this.$message('修改成功!请查收邮件以更新账户!');
            // logout()
            // alert('即将跳转至北航邮箱')
            // window.open('https://mail.buaa.edu.cn/coremail/index.jsp?nodetect=true', "_self");
            logout()  
            this.$router.push({ path: '/login' })
            }).catch(error => {
            // alert(error)
            console.log(error)
          })
        }
        else {
          this.$message('error submit!')
        }
      },
      OnUserInfoClear() {
        //重置表单
        // this.$refs.userForm.reset()
        this.userForm.name = ''
        this.userForm.email = ''
        this.userForm.password = ''
      },
      logout() {
        this.$store.dispatch('user/logout')
        this.$router.push('/login?redirect=${this.$route.fullPath}')
      },
      printItem(item) {
          console.log(item)
      }
    },

    

  }
</script>
