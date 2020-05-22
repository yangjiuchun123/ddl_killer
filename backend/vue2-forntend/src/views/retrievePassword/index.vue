<template>  
  <div class="login-container">   
    <el-row type="flex" justify="center" style="margin-top: 130px">
      <el-col :span="10">      
      <div class="title-container">
          <h2 class="title">Retrieve Password</h2>
      </div>
      <div  class="login-form" >
        <v-app>
          <v-stepper v-model="e1">
            <v-stepper-header>
              <v-stepper-step :complete="e1 > 1" step="1">身份验证</v-stepper-step>
              <v-divider></v-divider>
              <v-stepper-step :complete="e1 > 2" step="2">密码重置</v-stepper-step>
              <v-divider></v-divider>
              <v-stepper-step step="3">重置完成</v-stepper-step>
            </v-stepper-header>

            <v-stepper-items>
              <v-stepper-content step="1">
                <v-card
                  class="mb-12"
                  color="grey lighten-1"
                  height="230px"
                >
                <v-card-acation >
                  <div  class="text-center">
                    <v-btn color="primary" @click="e1 = 2" >Continue</v-btn>
                    <v-btn text>Cancel</v-btn>  
                  </div>
                </v-card-action>
                </v-card>

                
              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card
                  class="mb-12"
                  color="grey lighten-1"
                  height="230px"
                >
                <v-card-text>
                <el-form  ref="form2" :model="form2" :rules="rules2"  auto-complete="on" label-position="left">
                  <el-form-item prop="password">
                    <span class="svg-container">
                      <svg-icon icon-class="password" />
                    </span>
                    <el-input
                      :key="passwordType"
                      ref="password"
                      v-model="form2.password"
                      :type="passwordType"
                      placeholder="密码"
                      name="password"
                      tabindex="2"
                      auto-complete="on"
                    />
                    <span class="show-pwd" @click="showPwd">
                      <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
                    </span>
                  </el-form-item>

                  <el-form-item prop="checkPass">
                    <span class="svg-container">
                      <svg-icon icon-class="password" />
                    </span>
                    <el-input type="password" placeholder="确认密码" v-model="form2.checkPass" autocomplete="off"/>
                  </el-form-item>
                </el-form>
                </v-card-text>  
                <v-card-action >
                  <div  class="text-center">
                  <v-btn color="primary" @click="e1 = 3" >Continue</v-btn>
                  <v-btn text>Cancel</v-btn>
                  </div>               
                </v-card-action>         
                </v-card>                
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                  class="mb-12"
                  color="grey lighten-1"
                  height="230px"
                >
                <v-card-text>
                  -^0^- 新登录密码重置成功，请重新登录!
                </v-card-text>
                <v-card-action >     
                  <div  class="text-center">        
                    <v-btn color="primary" @click="login" class="mx-auto" >重新登录</v-btn>
                  </div>
                </v-card-action>
                </v-card>
                
                
              </v-stepper-content>
            </v-stepper-items>
          </v-stepper>       
        </v-app>
      </div>
 
      </el-col>
    </el-row>
  </div>

</template>

<script>

  export default {
    data() {
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.form2.checkPass !== '') {
            this.$refs.form2.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.form2.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
     return {
        e1: 1,
        form2:{
          password: '',
          checkPass: '',
        },
        rules2:{
          password: [
            { require: true, validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
        },
        passwordType: 'password',
      }
    },
    watch: {
      
    },
    methods: {
      showPwd() {
        if (this.passwordType === 'password') {
          this.passwordType = ''
        } else {
          this.passwordType = 'password'
        }
        this.$nextTick(() => {
          this.$refs.password.focus()
        })
      },
      login() {
        this.$router.push({ path: '/login' })
      },

     
    }
  }
</script>

<style lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .labelterm {
    font-size: 18px;
    color: #fff;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
// $dark_gray:#889aa4;
// $light_gray:#eee;
$white: #ffffff;

.cardColor {
  background-color: #9a9c9c2c;;
}

.login-container {
  min-height: 100%;
  width: 100%;

  background-image: url('../../assets/bgd.png');
  top: 0;
  left: 0;
  width:100%;
  height:100%;
  min-width: 1000px;
  z-index:-10;
  zoom: 1;
  background-color: #fff;
  background-repeat: no-repeat;
  background-size: cover;
  -webkit-background-size: cover;
  -o-background-size: cover;
  background-position: center 0;
  // background-color: $bg;
  overflow: hidden;

  .login-form {
    position: relative;
    width: 800px;
    height: 430px;
    max-width: 100%;
    padding: 50px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }

  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    // color: $dark_gray;
    color: $white;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      // color: $light_gray;
      color: $white;
      margin: 0px auto 10px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    // color: $dark_gray;
    color: $white;
    cursor: pointer;
    user-select: none;
  }
}
</style>
