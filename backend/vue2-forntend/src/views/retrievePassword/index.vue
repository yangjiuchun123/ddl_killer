<template>  
  <div id="rtPWD" class="forget-container">   
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
                  height="230px"             
                >
                <v-card-text>
                <el-form ref="form1" :model="form1" :rules="rules1"  auto-complete="on" label-position="left">
                  <el-form-item prop="uid">
                    <span class="svg-container">
                      <svg-icon icon-class="user" />
                    </span>
                    <el-input
                      ref="uid"
                      v-model="form1.uid"
                      placeholder="学号"
                      name="uid"
                      type="text"
                      tabindex="1"
                      auto-complete="on"                    
                    />
                  </el-form-item>                  
               
                  <el-form-item prop="verify_code">
                    <span class="svg-container">
                      <i class="el-icon-message"></i>
                    </span>
                    <el-input placeholder="北航邮箱验证码" v-model="form1.verify_code" type="text" ></el-input>
                    <span>                    
                    <el-button plain :disabled="flag" @click="getAuthCode">{{ msg }}</el-button>
                    </span>
                  </el-form-item>
                </el-form>
                </v-card-text>
                <v-card-action >
                  <div  class="text-center">
                    <v-btn color="primary" @click="nextStep1('form1')" >下一步</v-btn>
                    <v-btn text @click="resetForm('form1')">重置</v-btn> 
                  </div>
                </v-card-action>
                </v-card>                
              </v-stepper-content>

              <v-stepper-content step="2">
                <v-card
                  class="mb-12"                
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
                      placeholder="重置密码"
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
                  <v-btn color="primary" @click="nextStep2('form2')" >下一步</v-btn>
                  <v-btn text @click="resetForm('form2')">重置</v-btn>
                  </div>               
                </v-card-action>         
                </v-card>                
              </v-stepper-content>

              <v-stepper-content step="3">
                <v-card
                  class="mb-12"                  
                  height="230px"
                >
                <v-card-text>
                  <p></p>
                  <p class="text-center">-^0^- 新登录密码重置成功，请重新登录!</p>
                  <p></P>
                </v-card-text>
                <v-card-action >     
                  <div  class="text-center">        
                    <v-btn color="primary" @click="login"  >重新登录</v-btn>
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
import { sendAuthCode,verifyAuthCode,resetPWD } from '@/api/user'
import { JSEncrypt } from 'jsencrypt'
//import { encrypt } from '@/utils/encrypt'

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
      };
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
        flag:false,
        key_id:'',
        pub_key:'',
        uid:'',
        msg:'获取邮箱验证码',        
        form1:{
          uid:'',          
          verify_code:'',//验证码
        },
        rules1:{
           uid: [
            {require: true, validator: validateUid, trigger: 'blur'}
          ],          
          verify_code:[
            {required:true,message: '请输入验证码', trigger:'blur'}
          ]
        },
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
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      /*
       encrypt(password) {
        let encrypt = new JSEncrypt()
        encrypt.setPublicKey(this.pub_key)
        // var encPassword = encrypt.encrypt(this.password)
        // console.log(this.username)
        // console.log(encPassword)
        return encrypt.encrypt(password)
      },
      */
      getAuthCode(){
        this.$refs.form1.validateField('uid', (errMsg) => {
               if (errMsg) {
                   console.log('学号校验未通过')
               }else {
                //@后端先判断该学号是否存在，再给北航邮箱发送验证码
                var postData={
                  uid:this.form1.uid
                }
                sendAuthCode(postData).then(res => {                         
                  const _this =this;
                  this.flag = true; 
                  var time = 150;//定义时间变量 150s
                  var timer = null;//定义定时器
                  timer = setInterval(function(){
                    if(time==0){
                      _this.msg="重新获取验证码";                          
                      _this.flag=false;            
                      clearInterval(timer);//清除定时器
                    }else{
                      _this.msg=time+"秒后重新获取";                     
                      time--;
                    }                    
                  },1000)  
                  }).catch(error => {
                    console.log(error)
                  })  
               }
           })
      },

      nextStep1(formName){
        console.log(formName);
        this.$refs[formName].validate((valid) => {
          if (valid) {
            var submitForm = {
              uid: this.form1.uid,
              verify_code:this.form1.verify_code,
            }
            console.log(submitForm)
            //@与后端交互
            
            verifyAuthCode(submitForm).then(res => {              
              this.e1=2;
              this.uid=res.data.uid;
              //用于之后的密码加密
              this.key_id=res.data.key_id;
              this.pub_key=res.data.pub_key;              
            }).catch(error => {
              console.log(error)
            })
          } else {            
            return false;
          }                
          })
      },
      
      encryptPWD(password){
        let enc = new JSEncrypt()
        // res : {'pub_key': pub_key, 'key_id': key.id}
        // console.log("res.key_id: ", res.key_id)
        // console.log("pub_key: ", res.pub_key)
        enc.setPublicKey(this.pub_key)
        var encPass = "kid:" + this.key_id + "|" + enc.encrypt(password)
        return encPass
      },

      nextStep2(formName){
        console.log(formName);
        this.$refs[formName].validate((valid) => {
          if (valid) {
            var submitForm = {
              uid:this.uid,
              password: this.encryptPWD(this.form2.password),            
            }
            console.log(submitForm)
            //@与后端交互
            
            resetPWD(submitForm).then(res => {        
              this.e1=3;
              
            }).catch(error => {
              console.log(error)
            })
          } else {
            
            return false;
          }                
          })    

      },
     
    }
  }
</script>

<style lang="scss" >
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg:#283443;
$light_gray:#fff;
$cursor: #fff;


@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .forget-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.forget-container {
  .labelterm {
    font-size: 18px;
    color: #fff;
    margin-top: 10px;
    margin-bottom: 10px;
  }

  .el-input {
    display: inline-block;
    height: 47px;
    width: 180px;

    input {
      background: transparent;
      //background-color:#454545;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color:#454545;
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
    width:370px;
    margin-left: auto;
    margin-right:auto;
  }
}
</style>

<style lang="scss" scoped>
$bg:#2d3a4b;
$dark_gray:#889aa4;
// $light_gray:#eee;
$white: #ffffff;

.cardColor {
  background-color: #9a9c9c2c;
}

.forget-container {
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
  //background-color: #fff;
  background-repeat: no-repeat;
  background-size: cover;
  -webkit-background-size: cover;
  -o-background-size: cover;
  background-position: center 0;
  overflow: hidden;

  .login-form {
    position: relative;    
    width: 700px;
    height: 430px;
    max-width: 100%;
    min-width:630px;
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
    color: $dark_gray;
    //color: $white;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
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
    color: $dark_gray;   
    cursor: pointer;
    user-select: none;
  }
}
</style>
