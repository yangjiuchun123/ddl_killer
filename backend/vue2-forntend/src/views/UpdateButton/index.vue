<template>
<div>
  <v-row>
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on }">
        <!-- <v-btn color="primary" dark v-on="on">同步</v-btn> -->
        <v-btn outlined class="font-weight-bold" v-on="on" >更新课程</v-btn>

      </template>
      <v-card>
        <v-card-title>
          <span class="headline">同步课程中心</span>
        </v-card-title>
        <v-card-text>
            
            <v-container>
            <p class="warning--text">输入您的统一认证账号以同步课程中心数据；<br>P.S. 本站点不会存储统一认证账号密码，且采用加密传输密码保证安全。<br>P.P.S 建议在 <strong>课程中心->用户偏好</strong> 中将<strong><font color='red'>非本学期</font></strong>课程移至 <strong><u>归档站点</u></strong>，以获得更快的同步速度。</p>
            <v-row>
                <v-text-field v-model="username" label="统一认证账号" @keyup.enter="submit" required></v-text-field>
            </v-row>
            <v-row>
                <v-text-field v-model="password" label="统一认证密码" type="password" @keyup.enter="submit" required></v-text-field>
            </v-row>
            </v-container>

            <v-card
                color="primary"
                dark
                v-if="loading"
            >
                <v-card-text>
                请稍等，根据您的课程中心的设置可能需要1~3分钟的时间
                <v-progress-linear
                    indeterminate
                    color="white"
                    class="mb-0"
                ></v-progress-linear>
                </v-card-text>
            </v-card>

        </v-card-text>
        <v-card-actions>-
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">关闭</v-btn>
          <v-btn color="blue darken-1" text @click="submit">提交</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>

import { updateFromCourse } from '@/api/user_task'
// import JSEncrypt from '@/utils/jsencrypt/bin/jsencrypt'
import { JSEncrypt } from 'jsencrypt'

export default {
  name: 'updateBtn',
  data: () => ({
    dialog: false,
    loading : false,
    username: '',
    password: '',
    pub_key: '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCt1/hVqW9pxTAp6vbJu5+5myvA\nF8wvsEqM7FdIAKe5hhD1paQhPcG/RkPFzQG1u0jeQcwNJIddhmk/jqAK0v2GbHhV\nUEw/rQ8AATFxLTitXWhjFPC2quAlGRzRby4LALxlWBziGNzKU6BERsI1nawJb1If\ni/+q/qgZMCAGKY1EAwIDAQAB\n-----END PUBLIC KEY-----'

  }),
  methods: {
      submit() {
          this.loading = true
          
          let encrypt = new JSEncrypt()
          encrypt.setPublicKey(this.pub_key)
          var encPassword = encrypt.encrypt(this.password)
          console.log(this.username)
          console.log(encPassword)

          updateFromCourse(this.$store.getters.uid, { username: this.username, password: encPassword }).then(res => {
            this.$emit('updEvent')
            this.loading = false
            this.dialog = false
            this.$message({
              showClose: true,
              message: '课程中心同步成功！快去查看自己的ddl吧！',
              type: 'success',
              duration: 0
            });
          }).catch(error => {
            this.loading = false
          })
      }
  }
}
</script>
