<template>
  <div id ="Eventlist">
  <v-app>
    <v-data-table
      :headers="headers"
      :items="tasks"
      :sort-by="['is_finished', 'ddl_time']"
      :sort-desc="[false, false]"
      multi-sort
      class="elevation-1 mx-5"
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
        <v-icon small class="mr-2"  @click="editItem(item)"> mdi-pencil </v-icon>
        <a v-bind:href="item.urls" target='_BLANK'><v-icon small class="mr-2" > mdi-share-variant </v-icon></a>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>

      <template v-slot:no-data>
        <!-- <v-btn color="primary" @click="initialize">Reset</v-btn> -->
        <updateBtn color='primary' class=''></updateBtn> 
        <table>
      </template>
    </v-data-table>
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
        { text: '发布时间', value: 'create_time' },
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
          is_finished: false
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
          is_finished: false
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
          participant: []
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
      }
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
    }
  }
</script>
