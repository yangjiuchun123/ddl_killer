var data={
       "data":[
          { // homework
              "tid": 1,
              "title": "团队博客——功能规格",
              "category": "homework",
              "course":"软件工程",
              "content": "这是一篇团队博客",
              "platform": "博客园",
              "urls":"https://www.github.com/BuaaRedSun/docs",
              "create_time": "2020-03-20 15:33:20",
              "ddl_time": "2020-04-10 23:55:00",
              "notification_alert": true,
              "notification_time": "2020-04-09 23:55:00",
              "is_admin":false,
              "is_finished": false
          },
          { // exam
              "tid": 2,
              "title": "工科数学分析期中考试",
              "category": "exam",
              "course": "工科数学分析",
              "content": "祝你考试顺利",
              "platform": "教4-401",
              "urls": "http://www.baidu.com/",
              "create_time": "2020-03-20 15:33:20",
              "ddl_time": "2020-04-29 14:30:00",
              "notification_alert": false,
              "notification_time": "2020-04-29 14:30:00",
              "is_admin":false,
              "is_finished": false
          },
          { // personal
              "tid": 3,
              "title": "拿快递",
              "category": "personal",
              "urls": null,
              "platform": null,
              "course": null,
              "content":"东门顺丰快递",
              "create_time": "2020-04-18 15:33:20",
              "ddl_time": "2020-04-20 17:30:00",
              "notification_alert": true,
              "notification_time": "2020-04-11 17:00",
              "is_admin":true,
              "is_finished": true
          },
          { // meeting
              "tid": 4,
              "title": "志愿者例会",
              "category": "meeting",
              "urls":"https://www.bv2008.cn",
              "platform": "志愿北京",
              "course": null,
              "content":null,
              "create_time": "2020-03-20 15:33:20",
              "ddl_time": "2020-04-23 14:30:00",
              "notification_alert": true,
              "notification_time": "2020-04-01 14:00:00",
              "is_admin":true,
              "is_finished": false
          },
      ]
  }

export default [
    //获取当前用户的所有task
    {
      url: '/api/user/uid/tasks',
      type: 'get',
      response: config => {
        return {
          code: 200,
          data: data
        }
      }
    },
    /*
    {
      url: '/vue-admin-template/tasks/deleteOne',
      type: 'post',
      response:config => {
        console.log(config.body)
        return {
          code: 200,
          data: 'delete success',
        }
      }
    },
    */
    {
      url: '/api/user/uid/tasks/new',
      type: 'post',
      response:config => {
        console.log(config.body)
        return {
          code: 200,
          data: 'create success',
        }
      }
    },
    {
      url: '/api/user/uid/tasks/modify',
      type: 'post',
      response:config => {
        console.log(config.body)
        return {
          code: 200,
          data: 'modify success',
        }
      }
    }
  ]
