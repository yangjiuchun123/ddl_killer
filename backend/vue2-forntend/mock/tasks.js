const data={
    "success": true,
    "message": "Success.",
    "uid": 1,
    "data": [ //这里的data是task集合
        { // homework
            "tid": 27,
            "title": "团队博客——功能规格",
            "category": "homework",
            "content": "这是一篇团队博客",
            "useful_urls": [
                "www.edu.cnblogs.com/xxxxx",
                "www.github.com/BuaaRedSun/docs"
            ],
            "platform": "博客园",
            "cid": "1",
            "course_name": "软件工程",
            "ddl": {
                "ddl_id": 13,
            "ddl_time": "2020-04-10 23:55:00",
                "notification_alert": true,
            "notification_time": "2020-04-09 23:55:00",
            "notification_repeat": null,
            "notification_content": "交作业啦"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
        { // exam
            "tid": 35,
            "title": "工科数学分析期中考试",
            "category": "exam",
            "useful_urls": [], //集合size=1即可，空值有点奇怪
            "platform": "教4-401",
            "cid": "3",
            "course_name": "工科数学分析",
            "ddl": {
                "ddl_id": 30,
                "ddl_time": "2020-04-29 14:30:00",
                "notification_alert": false,
                "notification_time": "2020-04-29 14:30:00",
                "notification_repeat": "day",
                "notification_content": "淑芬考试",
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
        { // personal
            "tid": 42,
            "title": "拿快递",
            "category": "personal",
            "useful_urls": null,
            "platform": null,
            "cid": null,
            "course_name": null,
            "ddl": {
                "ddl_id": 50,
                "ddl_time": "2020-04-20 17:30:00",
                "notification_alert": true,
                "notification_time": "2020-04-11 17:00",
                "notification_repeat": null,
                "notification_content": "东门顺丰快递"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": true
        },
        { // meeting
            "tid": 77,
            "title": "志愿者例会",
            "category": "meeting",
            "useful_urls": [
                "www.bv2008.cn"
            ],
            "platform": "志愿北京",
            "cid": "1",
            "course_name": null,
            "ddl": {
                "ddl_id": 70,
                "ddl_time": "2020-04-23 14:30:00",
                "notification_alert": true,
                "notification_time": "2020-04-01 14:00:00",
                "notification_repeat": "week",
                "notification_content": "汇报周进展"
            },
            "created_at": "2020-03-20 15:33:20",
            "is_finished": false
        },
    ]
}

export default [

    {
      url: '/vue-admin-template/tasks/getAll',
      type: 'get',
      response: config => {
        return {
          code: 200,
          data: data
        }
      }
    },

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
    {
      url: '/vue-admin-template/tasks/createOne',
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
      url: '/vue-admin-template/tasks/modifyOne',
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
