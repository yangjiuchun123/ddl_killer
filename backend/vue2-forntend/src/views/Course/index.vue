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

              <v-divider></v-divider>

              <!-- -----------------快速创建 -->
              <v-row>
                  <v-col cols="12" sm="1"></v-col>
                  <v-col cols="12" sm="10">
                    <v-text-field
                      background-color="blue lighten-5"
                      v-model="task_content"
                      @keyup.enter="onEnterSubmit"
                      hint="✅输入日程内容, 回车快速创建！！也可以点击右侧➕号进行详细设置！"
                      solo
                    >
                        <template v-slot:append>
                          <v-dialog v-model="TaskDialog" persistent max-width="600px">
                            <template v-slot:activator="{ on }">
                              <v-btn color="primary" dark v-on="on" icon large @click="naive_initDialog"><v-icon>mdi-plus</v-icon></v-btn>
                              <!-- <v-btn color="primary" dark class="mr-2" v-on="on" icon large><v-icon>mdi-plus-circle</v-icon></v-btn> -->
                            </template>
                            <v-card ref="form">
                              <v-card-title></v-card-title>
                              <v-card-text>
                                <v-container>
                                  <v-row>
                                    <v-col cols="12">
                                      <v-text-field ref="title" label="事项名称" v-model="task_title" :rules="[rules.required]" required outlined clearable></v-text-field>
                                    </v-col>

                                    <v-col cols="12">
                                      <v-textarea label="详细描述" v-model="task_content" auto-growed no-resize outlined clearable></v-textarea>
                                    </v-col>

                                    <v-col cols="12" sm="6">
                                      <v-select :items="task_types" v-model="task_type" label="事项类型" required outlined></v-select>
                                    </v-col>

                                    <v-col cols="12" sm="3">
                                      <v-select
                                        label="截止日期"
                                        :items="task_ddls"
                                        v-model="task_ddl"
                                        v-show="!isPicker"
                                        required outlined
                                      >
                                        <template v-slot:append-item>
                                          <v-divider class="mb-2"></v-divider>
                                          <v-list-item
                                            ripple
                                            @click="isPicker=true"
                                          >选择其他日期</v-list-item>
                                        </template>
                                      </v-select>

                                      <v-menu
                                        v-model="menu2"
                                        :close-on-content-click="false"
                                        :nudge-right="40"
                                        transition="scale-transition" offset-y min-width="290px"
                                      >
                                        <template v-slot:activator="{ on }">
                                          <v-text-field
                                            ref="date"
                                            label="点击选择日期"
                                            v-model="task_date"
                                            v-show="isPicker"
                                            v-on="on"
                                            :rules="[rules.required]"
                                            readonly outlined
                                          ></v-text-field>
                                        </template>
                                        <v-date-picker v-model="task_date" @input="menu2 = false"></v-date-picker>
                                      </v-menu>
                                    </v-col>

                                    <v-col cols="12" sm="3">
                                      <v-menu
                                        ref="menu"
                                        v-model="menu4"
                                        :close-on-content-click="false"
                                        :nudge-right="40"
                                        :return-value.sync="task_time"
                                        transition="scale-transition"
                                        offset-y
                                        max-width="290px"
                                        min-width="290px"
                                      >
                                        <template v-slot:activator="{ on }">
                                          <v-text-field
                                            v-model="task_time"
                                            label="截止时间"
                                            outlined
                                            readonly
                                            v-on="on"
                                          ></v-text-field>
                                        </template>
                                        <v-time-picker
                                          v-if="menu4"
                                          v-model="task_time"
                                          full-width
                                          ampm-in-title
                                          @click:minute="$refs.menu.save(task_time)"
                                        ></v-time-picker>
                                      </v-menu>
                                    </v-col>

                                    <v-col cols="12" v-show="task_type=='团队任务'">
                                      <v-combobox
                                        v-model="task_participant"
                                        :items="participant_items"
                                        :search-input.sync="participant_search"
                                        hide-selected
                                        hint="请输入需要通知到的相关成员的学号"
                                        label="相关成员"
                                        multiple
                                        persistent-hint
                                        small-chips
                                        outlined
                                      >
                                        <template v-slot:no-data>
                                          <v-list-item>
                                            <v-list-item-content>
                                              <v-list-item-title>
                                                No results matching "<strong>{{ participant_search }}</strong>". Press <kbd>enter</kbd> to create a new one
                                              </v-list-item-title>
                                            </v-list-item-content>
                                          </v-list-item>
                                        </template>
                                      </v-combobox>
                                    </v-col>
                                  </v-row>
                                  <v-card-actions>
                                    <v-row>
                                        <v-btn block depressed  small tile color="primary" @click="saveDialog"> Save </v-btn>
                                        <v-btn block depressed  small tile @click="initDialog();TaskDialog=false;"> Close </v-btn>
                                    </v-row>
                                    </v-card-actions>
                                </v-container>
                              </v-card-text>
                            </v-card>
                          </v-dialog>

                        </template>
                      </v-text-field>
                  </v-col>
                  <v-col cols="12" sm="1"></v-col>
                </v-row>

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
  import { getAllTasks, createOneTask, modifyOneTask,deleteOneTask } from "@/api/user_task"
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


      //------------------快速创建
      isPicker: false,
      task_title: '',
      task_content: '',
      task_types: [],
      task_type: '',
      task_ddls: [],
      task_ddl: '',
      task_date: '',
      task_time: '',
      task_participant: [],
      TaskDialog: false,
      menu2: false,
      menu3: false,
      menu4: false,

      isTitleChange: false,

      rules: {
        required: value => !!value || '本项内容必须填写哦~',
        counter: value => value.length <= 20 || 'Max 20 characters',
      },
      name: null,
      date: null,
      formHasErrors: false,

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
      },

      //------------------快速创建
      initDialog() {
        var week = new Array("周日", "周一", "周二", "周三", "周四", "周五", "周六")
        var today = new Date()
        var ddl1 = '今天 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)
        today.setDate(today.getDate() + 1)
        var ddl2 = '明天 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)
        today.setDate(today.getDate() + 6)
        var ddl3 = '下周 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)

        this.isPicker = false
        this.task_title = '',
        this.task_content = '',
        this.task_types =  ['个人日程', '团队任务']
        this.task_type = '个人日程'
        this.task_ddls = [ddl1, ddl2, ddl3]
        this.task_ddl = ddl1
        this.task_date = ''
        this.task_time = '24:00'
        this.task_participant = []

        this.isTitleChange = false
        this.formHasErrors = false

        Object.keys(this.form).forEach(f => {
          this.$refs[f].reset()
        })

      },

      naive_initDialog() {
        var week = new Array("周日", "周一", "周二", "周三", "周四", "周五", "周六")
        var today = new Date()
        var ddl1 = '今天 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)
        today.setDate(today.getDate() + 1)
        var ddl2 = '明天 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)
        today.setDate(today.getDate() + 6)
        var ddl3 = '下周 '+week[today.getDay()]+' '+today.toISOString().substr(0, 10)
        this.isPicker = false
        this.task_types =  ['个人日程', '团队任务']
        this.task_type = '个人日程'
        this.task_ddls = [ddl1, ddl2, ddl3]
        this.task_ddl = ddl1
        this.task_date = ''
        this.task_time = '24:00'
        this.task_participant = []

        this.isTitleChange = false
        this.formHasErrors = false
      },

      saveDialog() {
        console.log(this.isPicker)
        console.log(this.task_title)
        console.log(this.task_content)
        console.log(this.task_type)
        console.log(this.task_ddl)
        console.log(this.task_date)
        console.log(this.task_time)

        var t_time = this.isPicker?this.task_date:this.task_ddl.substr(6,12)

        var new_task = {
          tid:-1,
          title: this.task_title,
          category: (this.task_type=="个人日程")?'person':'meeting',
          content: this.task_content,
          participant:this.task_participant,
          platform: '',
          urls:'',
          create_time: new Date().toISOString().substr(0, 10) + 
            ' ' + new Date().getHours() + ':' + + new Date().getMinutes() + ':'+ new Date().getSeconds(),
          ddl_time: t_time+' '+this.task_time+':00',
          notification_alert:false,
          notification_time: '',
          isAdmin:true,
          is_finished: false
        }

        console.log(new_task)

        this.formHasErrors = false
        Object.keys(this.form).forEach(f => {
          if (!this.form[f])
            if (f!='date' || this.isPicker) this.formHasErrors = true
          this.$refs[f].validate(true)
        })

        console.log(this.formHasErrors)

        if (!this.formHasErrors){
          this.TaskDialog = false

          createOneTask(this.$store.getters.uid, new_task).then(res =>{
            console.log(res.data)
            //为新建的task赋值后端分配的tid
            new_task['tid']=res.data.tid                       
            console.log(new_task.tid)
            this.initDialog()
          })
        }
      },

      onEnterSubmit() {
        console.log(this.task_content)
        var new_task = {
          tid:-1,
          title: this.task_content.substr(0,20),
          category: 'person',
          content: this.task_content,
          participant:this.task_participant,
          platform: '',
          urls:'',
          create_time: new Date().toISOString().substr(0, 10) + 
            ' ' + new Date().getHours() + ':' + + new Date().getMinutes() + ':'+ new Date().getSeconds(),
          ddl_time: new Date().toISOString().substr(0, 10) + ' 24:00:00',
          notification_alert:false,
          notification_time: '',
          isAdmin:true,
          is_finished: false
        }
        console.log(new_task)
        createOneTask(this.$store.getters.uid, new_task).then(res =>{
          console.log(res.data)
          //为新建的task赋值后端分配的tid
          new_task['tid']=res.data.tid                       
          console.log(new_task.tid)
          this.task_content = ''
          this.initDialog()
        })
      },

    },

    computed: {
      form () {
        return {
          title: this.task_title,
          date: this.task_date,
        }
      },
    },

    watch: {
      "task_content": {
        handler(newVal){
          console.log("change")
          if (!this.form['title']){
            this.task_title = newVal.substr(0, 20)
          }
        },
      }
    },
  }
</script>
