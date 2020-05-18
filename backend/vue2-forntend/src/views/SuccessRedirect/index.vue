<template>
  <v-app>
    <v-row justify="center" align="center">

      <v-card height="300px" width="1000px" loading="primary">
        <v-card-title>
          <h1>Congratulations!🎉</h1>
        </v-card-title>
        <v-row align="center" justify="center">
          <span style="font-size: 20px">
            还有{{ count }}秒跳转至登录界面，或点击
            <el-link type="primary" style="font-size: 20px" @click="jump">
              链接
            </el-link>
            直接跳转
          </span>   
        </v-row>
      </v-card>
    </v-row>
    
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import { test } from '@/api/user'
import updateBtn from '@/views/UpdateButton'

export default {
  data(){
    return {
      count:"",//倒计时
    }
  },
 
  created() {
    this.threeGo()
  },
  
  methods: {
    //3秒后进入跳转页面
    threeGo(){
      const TIME_COUNT = 3;
      if(!this.timer){
        this.count = TIME_COUNT;
        this.timer = setInterval(()=>{
          if(this.count > 0 && this.count <= TIME_COUNT){
            this.count--;
          }else{
            clearInterval(this.timer);
            this.timer = null;
            //跳转的页面写在此处
            this.jump()
          }
        },1000)
      }
    },
    jump() {
      this.$router.push({path: '/login'});
    }
  }
}
</script>