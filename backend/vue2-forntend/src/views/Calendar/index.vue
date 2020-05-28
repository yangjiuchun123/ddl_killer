<template>
  <div id="Calendar" class="app-container">
    <v-app>
      <v-row class="fill-height">
        <v-col>
          <v-sheet height="64">
            <v-toolbar flat color="white">
              <v-btn outlined class="mr-4" color="grey darken-2" @click="setToday">
                Today
              </v-btn>
              <v-btn fab text small color="grey darken-2" @click="prev">
                <v-icon small>mdi-chevron-left</v-icon>
              </v-btn>
              <v-btn fab text small color="grey darken-2" @click="next">
                <v-icon small>mdi-chevron-right</v-icon>
              </v-btn>
              <v-toolbar-title>{{ title }}</v-toolbar-title>
              <v-spacer></v-spacer>
              <v-select
                v-model="type"
                :items="types"
                dense
                outlined
                hide-details
                label="type"
                class="mr-10"
              ></v-select>
              <!-- 创建新事项弹窗-->
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
            </v-toolbar>
          </v-sheet>
          <v-sheet height="600">
            <v-calendar
              ref="calendar"
              v-model="focus"
              color="primary"
              :events="events"
              :event-color="getEventColor"
              :now="today"
              :type="type"
              :first-interval=1
              @click:event="showEvent"
              @click:more="viewDay"
              @click:date="viewDay"
              @change="updateRange"
            ></v-calendar>
            <!--事项详情页-->
            <v-dialog
              v-model="selectedOpen"
              :close-on-content-click="false"
              :activator="selectedElement"
              max-width="500px"
            >
              <v-card
                color="grey lighten-4"
                min-width="350px"
                flat
              >
                <v-toolbar
                  :color="selectedEvent.color"
                  dark
                >
                  <v-icon>mdi-pencil</v-icon>

                  <v-toolbar-title class="pl-2" v-html="selectedEvent.name"></v-toolbar-title>
                  <v-spacer></v-spacer>
                  <v-btn icon>
                    <v-icon
                      small
                      @click="deleteItem(selectedEvent)"
                    >
                      mdi-delete
                    </v-icon>
                  </v-btn>
                </v-toolbar>
                <v-card-text >
                  <el-form ref="detailForm" :model="detailForm" label-width="100px" size="mini">
                    <el-form-item label="" style="margin-top:10px">
                        <span></span>
                      </el-form-item>
                    
                    <el-form-item label="发布时间">
                      <span v-text="detailForm.create_time"></span>
                    </el-form-item>
                    
                    <el-form-item label="截止时间" >
                    <el-date-picker
                          v-if="detailForm.isAdmin"
                          v-model="detailForm.ddl_time"
                          placeholder="选择日期时间"
                          value-format="yyyy-MM-dd HH:mm:ss"
                          format="yyyy-MM-dd HH:mm:ss"
                          type="datetime"
                          id="date1"
                          unlink-panels="true"
                      >
                      </el-date-picker> 
                      <span v-else v-text="detailForm.ddl_time"></span> 
                      <!-- <span>{{defaultForm.isAdmin}}</span>
                      <span>{{typeof(defaultForm.isAdmin)}}</span> -->
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
                            unlink-panels="true"
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
                  <v-btn color="blue darken-1" text @click="modifyTaskSave(selectedEvent)">保存修改</v-btn>
                  <v-btn color="blue darken-1" text @click="selectedOpen = false">取消</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-sheet>
        </v-col>
      </v-row>
    </v-app>
  </div>
</template>

<script>
import { getAllTasks, createOneTask, modifyOneTask,deleteOneTask } from "@/api/user_task"

export default {
  name:'Calendar',
  data: () => ({
    focus: '',
    type: 'month',
    types: ['month', 'week', 'day', '4day'],
    start: null,
    end: null,
    selectedEvent: {},
    selectedElement: null,
    selectedOpen: false, //事项详情窗口的开关状态
    createOpen: false, //创建日程窗口的开关状态
    events: [],
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
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
        isAdmin: false,
        is_finished: false,
        repeat:'',
    },
    defaultForm:{ //默认创建页
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
       isAdmin: false,
       notification_alert:false,
       participant: [],
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
        isAdmin: false,
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
    }

  }),
  computed: {
    title() {
      const { start, end } = this
      if (!start || !end) {
        return ''
      }
      const startMonth = this.monthFormatter(start)
      const endMonth = this.monthFormatter(end)
      const suffixMonth = startMonth === endMonth ? '' : endMonth
      const startYear = start.year
      const endYear = end.year
      const suffixYear = startYear === endYear ? '' : endYear
      const startDay = start.day + this.nth(start.day)
      const endDay = end.day + this.nth(end.day)
      switch (this.type) {
        case 'month':
          return `${startMonth} ${startYear}`
        case 'week':
        case '4day':
          return `${startMonth} ${startDay} ${startYear} - ${suffixMonth} ${endDay} ${suffixYear}`
        case 'day':
          return `${startMonth} ${startDay} ${startYear}`
      }
      return ''
    },
    monthFormatter() {
      return this.$refs.calendar.getFormatter({
        timeZone: 'UTC', month: 'long',
      })
    }
  },
  mounted() {
    this.$refs.calendar.checkChange()
  },
  created () {
   this.initialize()
  },
  methods: {
    viewDay({ date }) {
      this.focus = date
      this.type = 'day'
    },
    getEventColor(event) {
      return event.color
    },
    setToday() {
      this.focus = this.today
    },
    prev() {
      this.$refs.calendar.prev()
    },
    next() {
      this.$refs.calendar.next()
    },
    showEvent({ nativeEvent, event }) { //显示详情页
      const open = () => {
        console.log("event.detail.isAdmin:",event.detail.isAdmin)
        this.selectedEvent = event
        this.selectedElement = nativeEvent.target
        this.detailForm = Object.assign({}, event.detail)
            
        setTimeout(() => this.selectedOpen = true, 10)

        //console.log(event.detail)

        //改变event.detail的值，前面的event.detail都将更改 但是detailForm不受影响
        /*
        console.log(this.detailForm)
        event.detail.tid=-1
        console.log(this.detailForm)
        */
      }

      if (this.selectedOpen) {
        this.selectedOpen = false
        setTimeout(open, 10)
      } else {
        open()
      }
      nativeEvent.stopPropagation()
    },
    setColor(type,is_finished){
        if(is_finished===true)
            return 'grey darken-1'
        if(type ==='homework')
            return 'orange'
        else if(type ==='exam')
            return 'red'
        else if(type ==='meeting')
            return 'green'
        else if(type ==='personal')
            return 'blue'
        else
            return 'blue'
    },
    updateRange({ start, end }) {
      this.start = start
      this.end = end
      //this.intialize()
    },
    initialize() { //从后端获取全部的task 赋值给events
      getAllTasks(this.$store.getters.uid).then(res => {
          // console.log(res)
          var events = []
          var fetched_data=res.data
          // console.log(fetched_data)
          var rdata = fetched_data
          for (let i = 0; i < rdata.length; i++){
              var ie = rdata[i]
              // console.log('------initialize-------')
              // console.log(typeof(ie.isAdmin))
              //ie.isAdmin = false
              if(ie.ddl_time===''){//若无ddl，则日历不渲染该事项
                continue
                }
              events.push({
                name: ie.title,
                start: ie.ddl_time,
                // start: ie.create_time,
                // end: ie.ddl_time,
                color: this.setColor(ie.category,ie.is_finished),
                detail: ie     //保存此task的全部信息
              })
            }
          this.events = events
          // console.log(this.events)
      })
    },

    deleteItem(event) {
      const index = this.events.indexOf(event)      
      console.log(event)
      var tid1 =event.detail.tid    
      //confirm('Are you sure you want to delete this item?') && this.events.splice(index, 1)
      if(confirm('Are you sure you want to delete this item?')){
        this.events.splice(index, 1)
        //与后端交互 删除task
        deleteOneTask(this.$store.getters.uid,tid1).then(res => {
          console.log(res.data)
        })
        this.selectedOpen = false
      }else{
        console.log("cancel")
      } 
    },
    
    createTask(formName){
      this.$refs[formName].validate((valid) => {
                if (valid) {
                    var temp = this.newForm; //temp为引用 newForm 改变时 temp也会改变;temp改变时，newForm也会改变
                    const ddl_date_time = temp.ddlDay+' '+temp.ddlTime;
                    const alert_date_time = temp.alertDay+' '+temp.alertTime;
                    const create_time = this.formatDate(new Date(),true)
                    var detail = Object.assign({},temp) //temp的拷贝
                    detail.ddl_time = ddl_date_time;
                    detail.notification_time = alert_date_time
                    if(alert_date_time===' ')
                        detail.notification_time=ddl_date_time
                    detail.create_time = create_time
                    delete detail.ddlDay
                    delete detail.ddlTime
                    delete detail.alertDay 
                    delete detail.alertTime
                    //@ 与后端交互 创建新task
                    var postObj1 =  eval('(' + JSON.stringify(detail) + ')')
                    createOneTask(this.$store.getters.uid, postObj1).then(res =>{
                      console.log(res.data)
                      //为新建的task赋值后端分配的tid
                      detail['tid']=res.data.tid
                      detail['course_name']=null
                      detail['is_finished']=false
                      detail['isAdmin'] =true
                      var newEvent={
                      name:temp.title,
                      start:ddl_date_time,
                      color:this.setColor(temp.category,temp.is_finished),
                      detail:detail
                      }
                      this.events.push(newEvent);
                      //
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
      //重置表单
      //this.newForm = Object.assign({},this.defaultForm)
      this.$refs[formName].resetFields();
      this.createOpen = false
    },
    modifyTaskSave(event){
      //与后端交互  修改task
      event.start=this.detailForm.ddl_time
      event.detail=Object.assign({}, this.detailForm)
      event.color=this.setColor(this.detailForm.category,this.detailForm.is_finished)
      console.log(this.detailForm)
      //传回此时修改的event.detail的JSON字符串 为不受后面影响
      var postObj2 =  eval('(' + JSON.stringify(event.detail) + ')')
      modifyOneTask(this.$store.getters.uid, postObj2).then(res =>{
        console.log(res.data)
      })
      this.selectedOpen=false
    },

    nth(d) {
      return d > 3 && d < 21
        ? 'th'
        : ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th'][d % 10]
    },
    /*
    rnd(a, b) {
      return Math.floor((b - a + 1) * Math.random()) + a
    },
    */
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
  }
}
</script>
