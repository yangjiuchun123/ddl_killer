<template>
  <v-app>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-card color="#647d91" dark>

            <v-card-title class="headline font-weight-bold">{{ timeInfo }}，{{ this.$store.getters.name }}</v-card-title>
            <!--v-card-subtitle>
              Listen to your favorite artists and albums whenever and wherever, online and offline.
            </v-card-subtitle-->
            <v-card-actions>
              <v-btn text @click="show = !show">
                初次见面？点我快速上手
                <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
              </v-btn>
              <v-spacer></v-spacer>
              <!-- <v-btn outlined class="font-weight-bold">更新今日课程</v-btn> -->
              
              <!--fmhfmhfmhfmhfmhfmhfmhfmhfmh-->
              <updateBtn class='pa-5'></updateBtn>
              <!--fmhfmhfmhfmhfmhfmhfmhfmhfmh-->

            </v-card-actions>
            <v-expand-transition>
              <div v-show="show">
                <v-divider></v-divider>
                <v-card-text>
                  -&nbsp; 点击右侧<strong>更新课程</strong>按钮，按照提示同步课程中心ddl数据<br>
                  -&nbsp; 在<strong>我的日历</strong>中可以查看到ddl日期及提交状态，并支持创建新日程<br>
                  -&nbsp; 在<strong>DDL列表</strong>中罗列所有ddl的信息，并支持创建与修改<br>
                  -&nbsp; 在<strong>我的课程</strong>中按照课程中心里所选课程展示ddl及共享资源<br>
                  -&nbsp; 在<strong>个人中心</strong>里个性化修改用户信息
                </v-card-text>
              </div>
            </v-expand-transition>
          </v-card>
        </v-col>

        <v-col cols="6">
          <v-card color="#bfcbd9" dark class="mx-auto" @click="jump_calendar">

            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title>
                  <v-icon large left>  mdi-calendar </v-icon>
                  <span class="title font-weight-bold">我的日历</span>
                </v-card-title>

                <v-card-text class="body-1 font-weight-bold">
                  <br><i class="mdi mdi-calendar"></i>&nbsp;一览无余的ddl日历视图<br>
                      <i class="mdi mdi-pencil"></i>&nbsp;支持个性化创建和修改<br>
                      <i class="mdi mdi-calendar-multiple"></i>&nbsp;月/周/天视图任你选择<br>
                      <i class="mdi mdi-checkbox-marked"></i>&nbsp;任务完成状态肉眼可见
                </v-card-text>
                <!-- <v-card-actions>
                  <v-btn text class="font-weight-bold" @click="jump_calendar">立即体验</v-btn>
                </v-card-actions> -->
              </div>

              <v-avatar class="ma-3" size="250" tile>
                <v-img src="https://gitee.com/FujiW/FigureBed/raw/master/img/20200504120118.png"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-card color="#a0a7b9" dark class="mx-auto" @click="jump_eventlist">

            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title>
                  <v-icon large left>  mdi-clipboard-text </v-icon>
                  <span class="title font-weight-bold">我的DDL</span>
                </v-card-title>

                <v-card-text class="body-1 font-weight-bold">
                  <br><i class="mdi mdi-sort"></i>&nbsp;自定义排序所有ddl<br>
                      <i class="mdi mdi-table"></i>&nbsp;所有ddl事项信息清晰罗列<br>
                      <i class="mdi mdi-email-outline"></i>&nbsp;ddl截止前邮件提醒<br>
                      <i class="mdi mdi-calendar-check"></i>&nbsp;与日历视图实时同步
                </v-card-text>
                <!-- <v-card-actions>
                  <v-btn text class="font-weight-bold" @click="jump_eventlist">立即体验</v-btn>
                </v-card-actions> -->
              </div>

              <v-avatar class="ma-3" size="250" tile>
                <v-img src="https://gitee.com/FujiW/FigureBed/raw/master/img/20200505015355.png"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-card color="#93a7bf" dark class="mx-auto"  @click="jump_course">

            <div class="d-flex flex-no-wrap justify-space-between" >
              <div>
                <v-card-title>
                  <v-icon large left>  mdi-library </v-icon>
                  <span class="title font-weight-bold">我的课程</span>
                </v-card-title>

                <v-card-text class="body-1 font-weight-bold">
                  <br><i class="mdi mdi-book-open"></i>&nbsp;一键同步课程中心资源列表<br>
                      <i class="mdi mdi-checkbox-multiple-marked-outline"></i>&nbsp;同步课程中心提交情况<br>
                      <i class="mdi mdi-view-dashboard"></i>&nbsp;按课程分类整合ddl和资源<br>
                      <i class="mdi mdi-share-variant"></i>&nbsp;老师学生可分享资源链接<br>
                </v-card-text>
                <!-- <v-card-actions>
                  <v-btn text class="font-weight-bold" @click="jump_course">立即体验</v-btn>
                </v-card-actions> -->
              </div>

              <v-avatar class="ma-3" size="250" tile>
                <v-img src="https://gitee.com/FujiW/FigureBed/raw/master/img/20200505013243.png"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>
        <v-col cols="6">
          <v-card color="#d1d1d8" dark class="mx-auto">

            <div class="d-flex flex-no-wrap justify-space-between">
              <div>
                <v-card-title>
                  <v-icon large left>  mdi-cube-outline </v-icon>
                  <span class="title font-weight-bold">特色功能</span>
                </v-card-title>

                <v-card-text class="body-1 font-weight-bold">
                  <br><i class="mdi mdi-fast-forward"></i>&nbsp;课程中心作业一键直达<br>
                      <i class="mdi mdi-email"></i>&nbsp;ddl前邮件提醒功能<br>
                      <i class="mdi mdi-lock"></i>&nbsp;RSA加密保障密码传输安全<br>
                      <i class="mdi mdi-account-multiple"></i>&nbsp;多人任务团队任务提醒
                </v-card-text>
                <!-- <v-card-actions>
                  <v-btn text class="font-weight-bold" >立即体验</v-btn>
                </v-card-actions> -->
              </div>

              <v-avatar class="ma-3" size="250" tile>
                <v-img src="https://gitee.com/FujiW/FigureBed/raw/master/img/20200505015146.png"></v-img>
              </v-avatar>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import updateBtn from '@/views/UpdateButton'
import { Message } from 'element-ui'

  export default {
    name: '我的主页',
    components: {
      updateBtn
    },
    data: () => ({
      show: false,
    }),
    created() {
      const h = this.$createElement;
      this.$notify({
        title: '提醒',
        message: h('p', null, [
          h('span', null, '🎉现在可以通过ddlkiller.top直接访问网站，而不需要添加:8000端口了'),
          //h('br'),
          //h('span', null, '😭邮件服务暂时无法使用，因为我们的邮箱账号被北航邮箱封禁了')
        ]),
        duration: 5 * 1000 // 默认3000ms
      })
    },
    computed: {
      timeInfo: function() {
        var hour = new Date().getHours()
        if (hour > 6 && hour < 12) return '早上好'
        else if (hour >= 12 && hour < 14) return '中午好'
        else if (hour >= 14 && hour < 19) return '下午好'
        else if (hour >= 19 && hour < 24) return '晚上好'
        else return '夜深了'
        return hour
      }
    },
    methods: {
      update() {
        // alert('update!')
        console.log('update')
      },
      jump_calendar() {
        this.$router.push({ path: '/Calendar/index' })
      },
      jump_eventlist() {
        this.$router.push({ path: '/Eventlist/index' })
      },
      jump_course() {
        this.$router.push({ path: '/Course/index' })
      }
    }
  }
</script>



<!--style lang="scss" scoped>
  $bg:#2d3a4b;
  // $dark_gray:#889aa4;
  // $light_gray:#eee;
  $white: #ffffff;

  .dashBoard-container {
    min-height: 100%;
    width: 100%;

    background-image: url('../../assets/mld.png');
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
  }
</style-->
