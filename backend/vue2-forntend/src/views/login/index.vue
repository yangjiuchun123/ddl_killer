<template>
  <div class="login-container">
    <el-row type="flex" justify="center" style="margin-top: 180px">
      <el-col :span="10">
        <!--el-card style="background-color: #3f5c6d2c;"-->
          <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">

            <div class="title-container">
              <h2 class="title">Welcome to DDL Killer</h2>
            </div>

            <el-form-item prop="uid">
              <span class="svg-container">
                <svg-icon icon-class="user" />
              </span>
              <el-input
                ref="uid"
                v-model="loginForm.uid"
                placeholder="Student ID"
                name="uid"
                type="text"
                tabindex="1"
                auto-complete="on"
              />
            </el-form-item>

            <el-form-item prop="password">
              <span class="svg-container">
                <svg-icon icon-class="password" />
              </span>
              <el-input
                :key="passwordType"
                ref="password"
                v-model="loginForm.password"
                :type="passwordType"
                placeholder="Password"
                name="password"
                tabindex="2"
                auto-complete="on"
                @keyup.enter.native="submit"
              />
              <span class="show-pwd" @click="showPwd">
                <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
              </span>
            </el-form-item>

            <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;" @click.native.prevent="submit">登录</el-button>
            <div class="tips"  style="float:left;">              
              <el-link type="white" @click="retrievePWD">忘记密码</el-link>
            </div>
            <div class="tips"  style="float:right;">         
              <el-link type="white" @click="regis">还没有账号？点击注册</el-link>              
            </div>            
          </el-form>
        <!--/el-card-->
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { validUid } from '@/utils/validate'
import { encrypt } from '@/utils/encrypt'

export default {
  name: 'Login',
  data() {
    const validateUid = (rule, value, callback) => {
        if (value == '') {
          callback(new Error('请输入学号'))
        } else {
          callback()
        }
      }
    const validatePassword = (rule, value, callback) => {
      if (value == '') {
        callback(new Error('请输入密码'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        uid: '',
        password: ''
      },
      loginRules: {
        uid: [{ required: true, trigger: 'blur', validator: validateUid }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined,
      pub_key: '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt1/hVqW9pxTAp6vbJu5+5myvA\nF8wvsEqM7FdIAKe5hhD1paQhPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhV\nUEw/rQ8AATFxLTitXWhjFPC2quAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1If\ni/+q/qgZMCAGKY1EAwIDAQAB\n-----END PUBLIC KEY-----'
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
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
    submit() {
      console.log("submit!")
      this.$refs.loginForm.validate(async valid => { // 箭头函数可以直接访问到最外面的this
        if (valid) {
          this.loading = true
          let encPassword = await encrypt(this.loginForm.password)
          this.$store.dispatch('user/login', {uid: this.loginForm.uid, password: encPassword}).then(res => { // dispatch: 把这个请求分发到user/login处理
            console.log(res)
            this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch(error => {
            console.log(error)
            this.loading = false
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    regis() {
      this.$router.push({ path: '/register' })
    },
    //@add Password
    retrievePWD(){
      this.$router.push({ path: '/retrievePassword' })
    }
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
    width: 520px;
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
      margin: 0px auto 40px auto;
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
