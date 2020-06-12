<template>
  <div id ="Eventlist">
  <v-app>
    <v-row class="fill-height">
        <v-col>
          <v-sheet>

            <v-data-table
              :headers="headers"
              :items="tasks"
              :sort-by="['is_finished', 'ddl_time']"
              :sort-desc="[false, false]"
              multi-sort
              class="elevation-2 mx-5 my-8"
              :search="search"
            >
              <template v-slot:top>
                <v-toolbar flat color="white">
                  <v-toolbar-title>DDL列表</v-toolbar-title>
                  <v-divider
                    class="mx-4"
                    inset
                    vertical
                  ></v-divider>
                  <v-spacer></v-spacer>
                  <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                    class="mr-12"
                  ></v-text-field>
                  <v-dialog v-model="createOpen" max-width="500px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="primary" dark class="mb-2" v-on="on">创建新日程</v-btn>
                    </template>
                    <v-card>
                      <v-toolbar color="primary" dark>
                        <v-toolbar-title>创建新日程</v-toolbar-title>
                      </v-toolbar>
                      <v-card-text>
                        <p></p>
                        <el-form ref="newForm" :model="newForm" :rules="createRule" label-width="110px">
                          <el-form-item label="事项名称" prop="title">
                            <el-input v-model="newForm.title"></el-input>
                          </el-form-item>
                          <el-form-item label="事项类型" >
                            <el-select v-model="newForm.category" placeholder="请选择类型">
                              <el-option label="个人" value="personal"></el-option>
                              <el-option label="会议" value="meeting"></el-option>
                            </el-select>
                          </el-form-item>
                          <el-form-item label="相关平台" prop="platform">
                            <el-input v-model="newForm.platform"></el-input>
                          </el-form-item>
                          <el-form-item label="相关链接" prop="urls">
                            <el-input v-model="newForm.urls"></el-input>
                          </el-form-item>
                          <el-form-item label="截止时间" required>
                            <el-col :span="11">
                              <el-form-item prop="ddlDay">
                                <el-date-picker  value-format="yyyy-MM-dd" format="yyyy-MM-dd" placeholder="选择日期"  v-model="newForm.ddlDay" style="width: 100%;"></el-date-picker>
                              </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                              <el-form-item prop="ddlTime">
                                <el-time-picker value-format="HH:mm:ss" format="HH:mm:ss" placeholder="选择时间" v-model="newForm.ddlTime" style="width: 100%;"></el-time-picker>
                              </el-form-item>
                            </el-col>
                          </el-form-item>
                          <el-form-item label="任务描述" prop="content">
                            <el-input type="textarea" v-model="newForm.content"></el-input>
                          </el-form-item>
                          <el-form-item label="开启提醒" prop="notification_alert">
                            <el-switch v-model="newForm.notification_alert"></el-switch>
                          </el-form-item>
                          <el-form-item label="提醒时间" v-if="newForm.notification_alert==true">
                            <el-col :span="11">
                              <el-form-item prop="alertDay">
                                <el-date-picker  value-format="yyyy-MM-dd" format="yyyy-MM-dd" placeholder="选择日期" v-model="newForm.alertDay" style="width: 100%;"></el-date-picker>
                              </el-form-item>
                            </el-col>
                            <el-col class="line" :span="2">-</el-col>
                            <el-col :span="11">
                              <el-form-item prop="alertTime">
                                <el-time-picker value-format="HH:mm:ss" format="HH:mm:ss" placeholder="选择时间" v-model="newForm.alertTime" style="width: 100%;"></el-time-picker>
                              </el-form-item>
                            </el-col>
                          </el-form-item>
                          <el-form-item label="重复提醒" v-if="newForm.notification_alert==true" >
                            <el-select v-model="newForm.repeat" placeholder="请选择是否重复">
                              <el-option label="否" value=""></el-option>
                              <el-option label="每日" value="daily"></el-option>
                              <el-option label="每周" value="weekly"></el-option>
                              <el-option label="每月" value="monthly"></el-option>
                            </el-select>
                          </el-form-item>
                          <el-form-item  label="其他参与成员" prop="participant">
                            <el-select
                                v-model="newForm.participant"
                                multiple
                                filterable
                                allow-create
                                default-first-option
                                placeholder="请输入学号">
                              </el-select>
                          </el-form-item>
                        </el-form>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="createTask('newForm')">立即创建</v-btn>
                        <v-btn color="blue darken-1" text @click="createCancel('newForm')">取消</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>

                  <!-- edit对话框 -->
                  <v-dialog v-model="editOpen" max-width="500px">
                  <v-card>
                    <v-card-title>
                      <span class="headline" v-text="detailForm.title"></span>
                    </v-card-title>
                    <v-card-text>
                      <p></p>
                        <el-form ref="detailForm" :model="detailForm" label-width="100px" size="mini">
                            <el-form-item label="" style="margin-top:10px">
                                <span></span>
                              </el-form-item>
                          <el-form-item label="发布时间">
                            <span v-text="detailForm.create_time"></span>
                          </el-form-item>
                          
                          <el-form-item label="截止时间" >
                            <el-date-picker
                                v-if='detailForm.isAdmin'
                                v-model="detailForm.ddl_time"
                                placeholder="选择日期时间"
                                value-format="yyyy-MM-dd HH:mm:ss"
                                format="yyyy-MM-dd HH:mm:ss"
                                type="datetime"
                                id="date1"
                            >
                            </el-date-picker> 
                            <span v-else v-text="detailForm.ddl_time"></span>
                            </el-form-item>
                            
                          <el-form-item label="事项分类">
                            <span v-text="detailForm.category"></span>
                          </el-form-item>
                          <el-form-item label="关联课程" v-show="detailForm.course_name!=null" >
                            <span v-text="detailForm.course_name"></span>
                          </el-form-item>
                          <el-form-item  label="相关平台" v-show="detailForm.platform!=null">
                            <span v-text="detailForm.platform"></span>
                          </el-form-item>
                          <el-form-item label="相关链接" v-show="detailForm.urls!=null">
                              <a :href="detailForm.urls" target="_Blank"> {{ detailForm.urls }} </a>
                          </el-form-item>
                          <el-form-item label="任务描述">
                              <el-input type="textarea" v-model="detailForm.content" :disabled="detailForm.isAdmin==false"></el-input>
                            </el-form-item>
                            <el-form-item label="完成状态">
                                <el-switch v-model="detailForm.is_finished" active-color="#13ce66"></el-switch>
                            </el-form-item>
                          <el-form-item label="开启提醒">
                            <el-switch v-model="detailForm.notification_alert"></el-switch>
                          </el-form-item>
                          
                          <el-tooltip class="item" effect="light" content="Top Center 提示文字" placement="top">
                            <div slot="content" ><p style="color: #E6A23C">提醒时间只能精确到分钟</p></div>
                            <el-form-item label="提醒时间" v-show="detailForm.notification_alert==true">
                              <el-date-picker
                                  v-model="detailForm.notification_time"
                                  placeholder="选择日期时间"
                                  value-format="yyyy-MM-dd HH:mm:ss"
                                  format="yyyy-MM-dd HH:mm:ss"
                                  type="datetime"
                                  id="date2"
                                >
                              </el-date-picker>
                            </el-form-item>
                          </el-tooltip>
                          <el-form-item label="重复提醒" v-show="detailForm.notification_alert==true" >
                            <el-select v-model="detailForm.repeat" placeholder="请选择是否重复">
                              <el-option label="否" value=""></el-option>
                              <el-option label="每日" value="daily"></el-option>
                              <el-option label="每周" value="weekly"></el-option>
                              <el-option label="每月" value="monthly"></el-option>
                            </el-select>
                          </el-form-item>
                        </el-form>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="modifyTaskSave(item)">保存修改</v-btn>
                        <v-btn color="blue darken-1" text @click="close">取消</v-btn>
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-toolbar>
              </template>
              <!--完成状态复选框-->
              <!-- <template v-slot:item.is_finished="{ item }">
                  <v-simple-checkbox :change="finish(item)" v-model="item.is_finished"></v-simple-checkbox>
              </template> -->

              
              <template v-slot:item.alter="{ item }">
                <v-icon class="mr-2" 
                  @click="changeTaskState(item.tid)"
                >
                  {{ item.is_finished ?  'mdi-checkbox-marked' : ' mdi-checkbox-blank-outline'}}
                </v-icon>
              </template>

              <template v-slot:item.actions="{ item }">
                <a v-bind:href="item.urls" target='_BLANK'><v-icon small class="mr-2" > mdi-share-variant </v-icon></a>
                <v-icon small class="mr-2"  @click="editItem(item)"> mdi-pencil </v-icon>        
                <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
              </template>

              <template v-slot:no-data>
                <!-- <v-btn color="primary" @click="initialize">Reset</v-btn> -->
                <updateBtn color='primary' class=''></updateBtn> 
                <!--<table>这在这干嘛的啊，报错给注释了-->
              </template>
            </v-data-table>
          </v-sheet>
          <v-sheet>
          <!-- -----------------快速创建 -->
          
          <v-divider class='mx-5'></v-divider>
          <br/>
          <v-sheet height="64" class='mx-5'>
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
              </v-sheet>
          </v-sheet>
        </v-col>
    </v-row>
  </v-app>
 </div>
</template>

<script>
import { getAllTasks, createOneTask, modifyOneTask,deleteOneTask } from "@/api/user_task"
import { alterTaskState } from '@/api/tasks';
import updateBtn from '@/views/UpdateButton'

export default {
    inject: ['reload'],
    components: {
        updateBtn
    },
    data: () => ({
      editOpen: false,//详情页
      createOpen:false,//创建界面
      search: '',
      headers: [
        {
          text: '事项名称',
          align: 'start',
          value: 'title',
          sortable: false,
        },
        { text: '关联课程', value: 'course_name' },
        { text: '截止日期', value: 'ddl_time' },
        { text: '事项类型', value: 'category' },
        // { text: '完成状态', value: 'is_finished' },
        { text: '完成状态', value: 'alter', sortable: false },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      tasks: [],
      editedIndex: -1,

      detailForm:{  //详情页
          tid:-1,
          title:'',
          category:'',
          course_name:'',
          content: '',
          platform:'',
          urls:'',
          create_time: '',
          ddl_time:'',
          notification_alert:false,
          notification_time: '',
          isAdmin:false,
          is_finished: false,
          repeat:''
      },
      defaultForm:{  //详情页
          tid:-1,
          title:'',
          category:'',
          course_name:'',
          content: '',
          platform:'',
          urls:'',
          create_time: '',
          ddl_time:'',
          notification_alert:false,
          notification_time: '',
          isAdmin:false,
          is_finished: false,
          repeat:''
      },
      newForm:{//创建日程界面
          tid: -1,
          title: '',
          category: 'personal',
          content: '',
          platform: '',
          urls:'',
          ddlDay:'',
          ddlTime:'',
          alertDay:'',
          alertTime:'',
          notification_alert:false,
          participant: [],
          repeat:''
      },
    
      createRule:{
        title:[
           { required: true, message: '请输入事项名称', trigger: 'blur' },
        ],
        ddlDay:[
          { required: true, message: '请选择日期', trigger: 'change' }
        ],
        ddlTime:[
          {  required: true, message: '请选择时间', trigger: 'change' },
        ],
        alertDay:[
          {  required: true, message: '请选择日期', trigger: 'change' }
        ],
        alertTime:[
          {  required: true, message: '请选择时间', trigger: 'change' },
        ],
        content:[
          {  required: true, message: '请输入任务内容', trigger: 'change' },
        ],
        paticipant: [
          { type: 'array', trigger: 'change' }
        ],
      },



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
    /*
    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },
    */
    /*
    watch: {
      dialog (val) {
        val || this.close()
      },
    },
    */
    created () {
      this.initialize()
    },
    methods: {
      initialize() {
        //@
        getAllTasks(this.$store.getters.uid).then(res => {  // fetch data
            // return response
            console.log(res)
            var fetched_data=res.data
            /*
            const temp = []
            var rdata = fetched_data.data

            for (let i = 0; i < rdata.length; i++){
              var ie = rdata[i]
              temp.push(ie)
            }
            */
            this.tasks = fetched_data;
        })
      },
      async editItem(item) {
        this.editedIndex = this.tasks.indexOf(item)
        // console.log(this.editedIndex)
        // console.log(item.isAdmin)
        this.detailForm =  Object.assign({}, item)
        // console.log(item)
        // console.log(this.detailForm)
        // console.log(this.detailForm.isAdmin)
        // console.log(typeof(this.detailForm.isAdmin))
        // console.log(this.detailForm.title)
        //this.editedItem.detail=Object.assign({},item.detail)
        this.editOpen = true
      },
      modifyTaskSave(item){
        Object.assign(this.tasks[this.editedIndex], this.detailForm)
        //@后端传值
        var postObj1 =  eval('(' + JSON.stringify(this.detailForm) + ')')
        modifyOneTask(this.$store.getters.uid, postObj1).then(res =>{
          console.log(res.data)
        })
        this.close()
      },
      //加了个close
      close () {
        this.editOpen = false
        // setTimeout(() => {
        //   this.detailForm = Object.assign({}, this.defaultForm)
        //   this.editedIndex = -1
        // }, 300)
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },
    
      deleteItem(item) {
        const index = this.tasks.indexOf(item)
        var tid1=item.tid
        console.log(tid1)
        if(confirm('Are you sure you want to delete this item?')){
          this.tasks.splice(index, 1)
          //与后端交互 删除task          
          deleteOneTask(this.$store.getters.uid,tid1).then(res => {
            console.log(res.data)
          })
          this.close()
        }
        //confirm('Are you sure you want to delete this item?') && this.tasks.splice(index, 1)
        
      },

      createTask(formName){
        this.$refs[formName].validate((valid) => {
                  if (valid) {
                      var temp = this.newForm //temp为引用 newForm 改变时 temp也会改变;temp改变时，newForm也会改变
                      const ddl_date_time = temp.ddlDay+' '+temp.ddlTime
                      const alert_date_time = temp.alertDay+' '+temp.alertTime
                      const create_time = this.formatDate(new Date(),true)
                      var detail = Object.assign({},temp) //temp的拷贝
                      detail['ddl_time'] = ddl_date_time
                      detail['notification_time'] = alert_date_time
                      if(alert_date_time===' ')
                        detail.notification_time=ddl_date_time
                      detail['create_time'] = create_time
                      delete detail.ddlDay
                      delete detail.ddlTime
                      delete detail.alertDay
                      delete detail.alertTime
                      
                      //@ 与后端交互 创建新task
                      var postObj2 =  eval('(' + JSON.stringify(detail) + ')')
                      createOneTask(this.$store.getters.uid, postObj2).then(res =>{
                        console.log(res.data)
                        //为新建的task赋值后端分配的tid
                        detail['tid']=res.data.tid                       
                        console.log(detail.tid)
                        //回调函数的异步机制  要按顺序执行需将以下代码放入回调函数中
                        detail['course_name']=null
                        detail['is_finished']= false
                        detail['isAdmin'] = true
                        var newTask= Object.assign({},detail)                        
                        this.tasks.push(newTask);
                        //重置表单
                        this.$refs[formName].resetFields();
                        this.createOpen = false;
                      })
                     
                      
                  } else {
                    console.log('error submit!!');
                    return false;
                  }
                });
      },
      createCancel(formName){
        this.$refs[formName].resetFields();
        this.createOpen = false
      },
      formatDate(a, withTime) {
        var myN = a.getFullYear();
        var myY = a.getMonth()+1;
        var myR = a.getDate();
        var myh = a.getHours();
        var mym = a.getMinutes();
        var mys = a.getSeconds();
        if (myY < 10) {
            myY = '0' + myY
        }
        if (myh < 10) {
            myh = '0' + myh; //补齐
        }
        if (mym < 10) {
            mym = '0' + mym; //补齐
        }
        if (mys < 10) {
            mys = '0' + mys; //补齐
        }
        if (myR < 10) {
            myR = '0' + myR; //补齐
        }
        var fullDateTime = myN + '-' + myY + '-' + myR + ' ' + myh + ':' + mym + ':' + mys;
        var fullDate =  myN + '-' + myY + '-' + myR
        return withTime
            ? fullDateTime
            : fullDate

        //return withTime
        //    ? `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()} ${a.getHours()}:${a.getMinutes()}:${a.getSeconds()}`
        //    : `${a.getFullYear()}-${a.getMonth() + 1}-${a.getDate()}`
        },

      changeTaskState(tid) {
        console.log(tid)
        alterTaskState(this.$store.getters.uid, tid).then(res=>{
          console.log(res.data)
          this.reload()
          //this.$message('加油！')
        })
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
          is_finished: false,
          repeat: ""
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
            this.$message("创建成功 ✔")
            var newTask = Object.assign({},new_task)
            this.tasks.push(newTask)
            this.initDialog()
            
            //重置表单
            this.$refs[formName].resetFields()
          })
        }
      },

      onEnterSubmit() {
        console.log(this.task_content)
        if (this.task_content.trim().length ==0) {
          return
        }
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
          ddl_time: new Date().toISOString().substr(0, 10) + ' 23:30:00',
          notification_alert:false,
          notification_time: '',
          isAdmin:true,
          is_finished: false,
          repeat: ""
        }
        console.log(new_task)
        createOneTask(this.$store.getters.uid, new_task).then(res =>{
          console.log(res.data)
          //为新建的task赋值后端分配的tid
          new_task['tid']=res.data.tid                       
          console.log(new_task.tid)
          this.task_content = ''
          this.$message("创建成功 ✔")
          var newTask = Object.assign({},new_task)
          this.tasks.push(newTask)
          this.initDialog()
          
          //重置表单
          this.$refs[formName].resetFields()
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
