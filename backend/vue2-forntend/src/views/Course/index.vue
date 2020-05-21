<template>
  <div class="app-container">
    <v-app>
      <!--v-toolbar flat-->
      <v-card color="basil">
          <v-card-title class="justify-center py-6">
            <v-chip-group
              column
              active-class="primary--text"
            >
              <v-chip v-for="tag in tags" :key="tag.cid" @click="chooseOne(tag)"
                class="ma-2" color="#1565C0" outlined label
              >
                {{ tag.course_name }}
              </v-chip>
            </v-chip-group>
          </v-card-title>
          <v-tabs  v-model="tab_now">
            <v-tab>DDL列表</v-tab>
            <v-tab>共享资源</v-tab>
            <v-tab>课程通知</v-tab>
            <v-spacer></v-spacer>
            <v-text-field
              v-model="searchs[tab_now]"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
              class="mr-12"
              height="28px"
            ></v-text-field>
            
            <!--DDL列表 开始-->
            <v-tab-item>
              <!--Eventlist></Eventlist-->
              <v-data-table
                :headers="headers"
                :items="ddls"
                class="elevation-1"
                show-expand
                single-expand=true
                :expanded.sync="expanded"
                item-key="tid"
                height="500px"
                no-data-text="本课程暂无DDL"
                fixed-header
                :search="searchs[0]"
                :sort-by="['is_finished', 'ddl_time']"
                :sort-desc="[false, false]"
                multi-sort
              >
                <!--template v-slot:item.remains="{ item }">
                  <v-chip :color="getColor(item.remains)" dark>{{ item.remains }}</v-chip>
                </template-->

                <template v-slot:item.title="{ item }">
                  <a v-bind:href="item.urls" target='_BLANK'> {{item.title}}</a >
                </template>

                <!--template v-slot:item.is_finished="{ item }">
                  <v-simple-checkbox v-model="item.is_finished"></v-simple-checkbox>
                </template-->

                <template v-slot:item.actions="{ item }">
                  <v-icon class="mr-2" 
                    @click="changeTaskState(item.tid)"
                  >
                    {{ item.is_finished ?  'mdi-checkbox-marked' : ' mdi-checkbox-blank-outline'}}
                  </v-icon>
                </template>

                <template v-slot:expanded-item="{ headers, item }">
                  <td :colspan="headers.length"><br/>{{ item.content }}<br/><br/></td>
                </template>

              </v-data-table>

            </v-tab-item>
            <!--DDL列表 结束-->

            <v-tab-item>
              <v-data-table
                :headers="Rheaders"
                :items="srcs"
                class="elevation-1"
                :search="searchs[1]"
                height="400px"
                no-data-text="本课程暂无资源"
              >
                <template v-slot:item.title="{ item }">
                  <a v-bind:href="item.url" target='_BLANK'> {{item.title}}</a>
                </template>
              </v-data-table>

              <v-divider></v-divider>
              <v-form ref="fileSubmit">
                <v-container fluid>
                  <v-row
                    align="start"
                    justify="center"
                    class="lighten-5"
                  >
                    <v-col cols="12" sm="3">
                      <v-text-field
                        v-model="fileSubmit.title"
                        label="文件名"
                        solo
                        clearable
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="3">
                      <v-text-field
                        v-model="fileSubmit.url"
                        label="分享链接"
                        :rules="[rules.url]"
                        solo
                        clearable
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="2">
                      <v-text-field
                        v-model="fileSubmit.code"
                        label="提取码"
                        solo
                        clearable
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="2">
                      <v-btn
                        style="top: -5px"
                        offset-y
                        color="cyan"
                        large
                        class="ma-2 white--text"
                        :disabled="!(fileSubmit.url&&fileSubmit.title)"
                        @click="onFileSubmit"
                      >
                        <v-icon left dark>mdi-cloud-upload</v-icon>
                        分享
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
              </v-form>

            </v-tab-item>

            <v-tab-item>
              <v-data-table
                :headers="Nheaders"
                :items="notices"
                class="elevation-1"
                :search="searchs[2]"
                height="500px"
                no-data-text="本课程暂无通知"
              >
                <template v-slot:item.title="{ item }">
                  <a v-bind:href="item.url" target='_BLANK'> {{item.title}}</a>
                </template>
              </v-data-table>
            </v-tab-item>


          </v-tabs>
      </v-card>
      <!--/v-toolbar-->
    </v-app>
  </div>
</template>

<script>
  import { getUserCourses, getCourseTaskByCid,  getResourceByCid, getNoticesByCid, addResource} from '@/api/course';
  import { alterTaskState } from '@/api/tasks';

  import Eventlist from '../Eventlist/index.vue'

  export default {
    components: {
      Eventlist,
    },

    data: () => ({
      search: '',      
      Rsearch: '',
      searchs: ['','',''],
      tab_now: null,
      ////////////////////////////////////DDL列表 开始
      headers: [
        {
          text: '事项名称',
          align: 'start',
          sortable: false,
          value: 'title',
        },
        { text: '发布时间', value: 'create_time' },
        { text: '截止时间', value: 'ddl_time' },
        //{ text: '剩余时间', value: 'remains' },
        //{ text: '完成状态', value: 'is_finished' },
        { text: '完成状态', value: 'actions', sortable: false },
        //{ text: '已完成人数', value: 'dalaos' },
        { text: '更多', value: 'data-table-expand' },

      ],

      tags: [],
      ddls: [],
      expends: [],
      ////////////////////////////////////DDL列表 结束
      
      ////////////////////////////////////共享资源 开始
      Rheaders: [
        {
          text: '资源名称',
          align: 'start',
          sortable: true,
          value: 'title',
        },
        {
          text: '提取码',
          value: 'code',
        },
        {
          text: '分享人',
          value: 'sharer'
        },
      ],


      srcs: [],
      fileSubmit: {
        title: '',
        url: '',
        code: '',
        sharer: '',
      },
      cid_now: '',

      rules: {
        required: value => !!value || 'Required.',
        url: value => {
          const pattern = /http[s]?:\/\/[^\s]*$/
          return pattern.test(value) || '不合法的链接格式'
        }
      },
      ////////////////////////////////////共享资源 结束

      ////////////////////////////////////课程通知 开始
      Nheaders: [
        {
          text: '标题',
          align: 'start',
          sortable: true,
          value: 'title',
        },
        {
          text: '发布时间',
          value: 'time',
        },
        {
          text: '内容详情',
          value: 'content'
        },
      ],

      notices: [],
      ////////////////////////////////////课程通知 结束

    }),

    created () {
      this.initialize()
    },

    methods: {
      initialize () {
        getUserCourses(this.$store.getters.uid).then(res => {
          console.log(res)
          var r_courses = res.data;
          for (let i = 0; i < r_courses.length; i++) {
            this.tags.push(r_courses[i]);
          }
        })
      },
      chooseOne(item) {
        // alert("choose" + item.course_name);
        this.updatePage(item.cid);
      },
      updatePage (cid) {
        this.cid_now = cid
        this.ddls = []
        getCourseTaskByCid(this.$store.getters.uid, cid).then(res => {
          console.log(res)
          var r_tasks = res.data;
          for (let i = 0; i < r_tasks.length; i++) {
            this.ddls.push(r_tasks[i]);
          }
        })

        this.srcs = []
        getResourceByCid(this.$store.getters.uid, cid).then(res => {
          // console.log(res)
          var r_resources = res.data;
          for (let i = 0; i < r_resources.length; i++) {
            this.srcs.push(r_resources[i]);
          }
        })

        this.notices = []
        getNoticesByCid(this.$store.getters.uid, cid).then(res => {
          // console.log(res)
          var r_notices = res.data;
          for (let i = 0; i < r_notices.length; i++) {
            this.notices.push(r_notices[i]);
          }
        })



        for (let i=0;i<this.ddls.length;i++) {
          this.courses[i] = this.ddls[i].title
          console.log(this.courses)
        }

        //DDL列表 开始
        //DDL列表 结束

      },

      changeTaskState(tid) {
        console.log(tid)
        alterTaskState(this.$store.getters.uid, tid).then(res=>{
          console.log(res.data)
          this.updatePage(this.cid_now)
          //this.$message('加油！')
        })
      },

      getColor (remains) {
        if (remains < 20) return 'red'
        else if (remains < 100) return 'orange'
        else return 'green'
      },

      onFileSubmit() {        
        var valid = this.$refs.fileSubmit.validate()
        this.fileSubmit.sharer = this.uid
        if(valid) {
          addResource(this.fileSubmit, this.$store.getters.uid, this.cid_now).then(res=>{
            console.log(res.data)
            this.$message('分享成功')
            this.updatePage(this.cid_now)
          })
        }
        else {
          this.$message('error submit!')
        }
      }
    }
  }
</script>
