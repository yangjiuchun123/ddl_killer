<template>
    <v-app  class="aboutUs-container">
      <v-container>
        <v-row>
          <v-col cols="12">
            <v-card
              class="mx-auto"
              dark
              raised
              img="../../assets/bgd2.jpg"
            >
              <v-card-title>
		        <p>
                我们是北航2020软件工程团队—— 软软软 团队。DDLKiller项目是我们团队首次开发的项目，我们希望在我们的不断改进下，它能成为一个方便的、好用的项目。
                反馈Bug和问题请点击<a color='#ffffff' href="https://www.cnblogs.com/UltraSoft/p/12813150.html"><font color='#ffffff'>「Bug反馈」</font></a>。
		        </p>
              </v-card-title>
            </v-card>
          </v-col>


          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#48789e"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「“曲奇为团队尽心尽力，这届我选曲奇做话事人！”」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                认真负责的组长，团队的PM，同时也担任部分的后端开发工作。负责协调团队进度、协助组员Debug，是团队的主心骨。
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sf.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">CookieLau</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                     <v-btn icon @click="show1 = !show1">
                        <v-icon class="mr-1">{{ show1 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                     </v-btn>

                     <v-btn icon target="_blank"  href="https://www.cnblogs.com/CookieLau/">
                        <v-icon class="mr-1" > mdi-comment-account</v-icon>
                     </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#2e5a88"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「“哎fmh，这块怎么做？”」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                看名字这么长就知道是大佬了！我们的项目就是基于他的fmh.js开发的（误）！团队的前端负责人，在自己开发的同时也会帮助前端组员解决问题，捉虫无数。
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sh.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">宇宙第一无敌最强前端大神fmh</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show2 = !show2">
                       <v-icon class="mr-1">{{ show2 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>

                    <v-btn icon  target="_blank" href="https://www.cnblogs.com/kingkongk/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#1d4576"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「“唔，不要把BUG都放在我的锅里，都看饿了……”」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                fmh的哥哥，负责我的课程、个人中心、关于我们和主页界面的开发。同时也是组内的美工担当，UI设计都要经过他的审核！
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sg.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">王 FUJI</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show3 = !show3">
                       <v-icon class="mr-1">{{ show3 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>

                    <v-btn icon  target="_blank" href="https://www.cnblogs.com/FUJI-Mount/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#986b8d"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「“我这日历怎么又有玄学BUG了”」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                前端开发成员之一，负责我的日历和我的DDL界面的开发，专业理清日历视图的一团乱麻，组内唯一的小姐姐，人美技术强！
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sj.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">LZH</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show4 = !show4">
                       <v-icon class="mr-1">{{ show4 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>

                    <v-btn icon  target="_blank" href="https://www.cnblogs.com/lzh-blod/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>

          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#0f2645"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「“啊？数据库又要大改？？”」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                后端开发成员之一，负责后端数据库的建立和API的编写。与前端配合完成了数据的传输，大佬一枚。
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74si.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">DZ</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show5 = !show5">
                       <v-icon class="mr-1">{{ show5 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>

                    <v-btn icon target="_blank"  href="https://www.cnblogs.com/Miracle-dz/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card
              class="mx-auto"
              color="#040a1a"
              dark
              max-width="400"
            >
              <v-card-title>
                <span class="title font-weight-bold">「让高考语文只考了90多分的人来负责文案是否搞错了什么」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                后端开发成员之一，负责URL和部分较难后端需求。关于我们这部分就是我写的文案哦～
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sk.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">Monster</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show6 = !show6">
                       <v-icon class="mr-1">{{ show6 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>
                    <v-btn icon target="_blank" href="https://www.cnblogs.com/yangjiuchun/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>

          <v-spacer></v-spacer>
          <v-col cols="4">
            <v-card class="mx-auto" color="#a1c3dd" dark max-width="400">
              <v-card-title> 
                <span class="title font-weight-bold">「HDL」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                带蓝子的简介
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://gitee.com/FujiW/FigureBed/raw/master/img/20200608170955.png"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">带蓝子</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show7 = !show7">
                       <v-icon class="mr-1">{{ show7 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>
                    <v-btn icon target="_blank" href="https://www.cnblogs.com/MisTariano/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>


          <v-spacer></v-spacer>
          <v-col cols="4" v-show="false">
            <v-card class="mx-auto" color="#040a1a" dark max-width="400">
              <v-card-title> 
                <span class="title font-weight-bold">「新成员1」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                新成员1的简介
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sk.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">新成员1</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show8 = !show8">
                       <v-icon class="mr-1">{{ show8 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>
                    <v-btn icon target="_blank" href="https://www.cnblogs.com/yangjiuchun/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-spacer></v-spacer>
          <v-col cols="4" v-show="false">
            <v-card class="mx-auto" color="#040a1a" dark max-width="400">
              <v-card-title> 
                <span class="title font-weight-bold">「新成员2」</span>
              </v-card-title>
              <v-card-text class="headline font-weight-bold">
                新成员2的简介
              </v-card-text>
              <v-card-actions>
                <v-list-item class="grow">
                  <v-list-item-avatar color="grey darken-3">
                    <v-img
                      class="elevation-6"
                      src="https://i.niupic.com/images/2020/03/21/74sk.jpg"
                    ></v-img>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title class="font-weight-bold">新成员2</v-list-item-title>
                  </v-list-item-content>
                  <v-row align="center" justify="end" >
                    <v-btn icon @click="show9 = !show9">
                       <v-icon class="mr-1">{{ show9 ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                    </v-btn>
                    <v-btn icon target="_blank" href="https://www.cnblogs.com/yangjiuchun/">
                       <v-icon class="mr-1" > mdi-comment-account</v-icon>
                    </v-btn>
                  </v-row>
                </v-list-item>
              </v-card-actions>
            </v-card>
          </v-col>


        </v-row>
      </v-container>
    </v-app>

</template>


<script>
  export default {
    data: () => ({
      show1: true,
      show2: true,
      show3: true,
      show4: true,
      show5: true,
      show6: true,
      show7: true,
      show8: true,
      show9: true,
    }),

    methods:{

    }
  }
</script>


<style lang="scss" scoped>
  $bg:#2d3a4b;
  // $dark_gray:#889aa4;
  // $light_gray:#eee;
  $white: #ffffff;

  .aboutUs-container {
    min-height: 100%;
    width: 100%;

    background-image: url('../../assets/bgd2.jpg');
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
</style>


