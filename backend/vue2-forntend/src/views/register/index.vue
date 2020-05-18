<template>
  <div class="login-container">
    <!-- <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="login-form" auto-complete="on"
      label-position="left"> -->
    <el-row type="flex" justify="center" style="margin-top: 40px">
      <el-col :span="10">
      <!--el-card style="background-color: #3f5c6d2c;"-->
      <el-form ref="ruleForm" :model="ruleForm" :rules="rules" class="login-form" auto-complete="on" label-position="left">

        <div class="title-container">
          <h2 class="title">Register</h2>
        </div>

        <el-form-item prop="uid">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="uid"
            v-model="ruleForm.uid"
            placeholder="学号"
            name="uid"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <el-form-item prop="username">
          <span class="svg-container">
            <svg-icon icon-class="user" />
          </span>
          <el-input
            ref="name"
            v-model="ruleForm.name"
            placeholder="用户名"
            name="name"
            type="text"
            tabindex="1"
            auto-complete="on"
          />
        </el-form-item>

        <el-tooltip class="item" effect="dark" content="Top Left 提示文字" placement="top-start">
          <div slot="content">注册时只允许根据学号自适应的北航邮箱验证，<br/>以防止学号盗用，之后可在个人信息中修改接<br/>收提醒的邮箱</div>
          <el-form-item prop="email">
            <span class="svg-container">
              <i class="el-icon-message"></i>
            </span>
            <el-input placeholder="邮箱" v-model="ruleForm.email" :readonly="true"></el-input>
          </el-form-item>
        </el-tooltip>

        <el-form-item prop="password">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="ruleForm.password"
            :type="passwordType"
            placeholder="密码"
            name="password"
            tabindex="2"
            auto-complete="on"
            @keyup.enter.native="submitForm('ruleForm')"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

        <el-form-item prop="checkPass">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input type="password" placeholder="确认密码" v-model="ruleForm.checkPass" @keyup.enter.native="submitForm('ruleForm')" autocomplete="off"/>
        </el-form-item>
        
        <el-form-item>
          <!-- <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button> -->
          <el-button type="primary" style="width:100%;"
            @click.native.prevent="submitForm('ruleForm')">注册</el-button>
        </el-form-item>

        <div class="tips" align="right">
          <span style="margin-right:20px;"><el-link type="white" @click="login">已有账号？点击登录</el-link></span>
        </div>

      </el-form>
      <!--/el-card-->
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { register } from '@/api/user'
import { JSEncrypt } from 'jsencrypt'

  export default {
    data() {
      const validateUid = (rule, value, callback) => {
        var reg = /^\d{8}$/
        if (value == '') {
          callback(new Error('请输入学号'))
        } 
        else if (!reg.test(value)){
          callback(new Error('请输入8位数学号'))
        }
        else {
          callback()
        }
      }
      const validateUsername = (rule, value, callback) => {
        if (value == '') {
          callback(new Error('请输入用户名'))
        } else {
          callback()
        }
      }
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (this.ruleForm.checkPass !== '') {
            this.$refs.ruleForm.validateField('checkPass');
          }
          callback();
        }
      };
      var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'));
        } else if (value !== this.ruleForm.password) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
      return {
        ruleForm: {
          uid: '',
          name: '',
          email: '',
          password: '',
          checkPass: '',
        },
        rules: {
          uid: [
            {require: true, validator: validateUid, trigger: 'blur'}
          ],
          username: [
            { require: true, validator: validateUsername, trigger: 'blur'}
          ],
          password: [
            { require: true, validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱地址', trigger: 'blur' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
          ]
        },
        passwordType: 'password',
        pub_key: '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt1/hVqW9pxTAp6vbJu5+5myvA\nF8wvsEqM7FdIAKe5hhD1paQhPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhV\nUEw/rQ8AATFxLTitXWhjFPC2quAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1If\ni/+q/qgZMCAGKY1EAwIDAQAB\n-----END PUBLIC KEY-----'
      };
    },
    watch: {
      "ruleForm.uid": {
        handler(newVal){
          console.log("change")
          this.ruleForm.email = newVal + '@buaa.edu.cn'
        },
        deep: true
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
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            var submitForm = {
              uid: this.ruleForm.uid,
              name: this.ruleForm.name,
              email: this.ruleForm.email,
              password: this.encrypt(this.ruleForm.password),
            }
            console.log(submitForm.password)
            register(submitForm).then(res => {
              // this.$router.push({ path: '/login' })
              alert('点击跳转至北航邮箱进行验证');
              // this.window.open({ path: 'https://mail.buaa.edu.cn/coremail/index.jsp?nodetect=true' })
              window.open('https://mail.buaa.edu.cn/coremail/index.jsp?nodetect=true', "_self");
            }).catch(error => {
              console.log(error)
            })
          } else {
            console.log('error form!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      login() {
        this.$router.push({ path: '/login' })
      },
      encrypt(password) {
        let encrypt = new JSEncrypt()
        encrypt.setPublicKey(this.pub_key)
        // var encPassword = encrypt.encrypt(this.password)
        // console.log(this.username)
        // console.log(encPassword)
        return encrypt.encrypt(password)
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
