const r_courses = // 成功查询返回
{
    "success": true,
    "message": "Success.",
    "user": {
        "uid": 1,
        "student_id": "17373001",
        "name": "北小航",
        "email": "0000001@qq.com"
    },
    "data": [ //这里的data是学生选课course的集合
        {
            "cid": "BH000001",
            "course_name": "软件工程",
            "accessibility": "r"
        },
        {
            "cid": "BH000002",
            "course_name": "工科数学分析",
            "accessibility": "wr" // w表示可写，课程负责人
        },
        {
            "cid": "BH000003",
            "course_name": "高级算法分析",
            "accessibility": "r"
        }
    ]
}

const r_singleCourse = 
{
    "success": true,
    "message": "Success.",
    "course": {
        "cid": "BH000001",
        "course_name": "软件工程"
    },
    "data": [ //这里的data是tasks的集合
        {
            "tid": 10,
            "title": "个人博客——热身", 
            "category": "homework", 
            "content": "这是一篇个人博客", 
            "useful_urls": [
                    "www.edu.cnblogs.com/xxxxxx"
            ],
            "cid": "BH000001",
            "ddl": {
                "ddl_id": 1,
                "ddl_time": {
                    "date": "2020-04-01",
                    "time": "23:55"
                },
                "notification_time": {
                    "date": "2020-03-31",
                    "time": "12:00",
                    "repeat": null
                },
                "notification_content": "交作业啦"
            }
        },
        {
            "tid": 27,
            "title": "团队博客——功能规格",
            "category": "homework",
            "content": "这是一篇团队博客",
            "useful_urls": [
                "www.edu.cnblogs.com/xxxxx",
                "www.github.com/BuaaRedSun/docs"
            ],
            "cid": "BH000001",
            "ddl": {
                "ddl_id": 13,
                "ddl_time": {
                    "date": "2020-04-10",
                    "time": "23:55"
                },
                "notification_time": {
                    "date": "2020-04-09",
                    "time": "23:55",
                    "repeat": null
                },
                "notification_content": "交作业啦"                
            }
        }
    ] 
}


export default [
  {
    url: '/vue-admin-template/api/user/courses',
    type: 'get',
    response: config => {
      const {uid} = config.query

      console.log(config.query)

      return {
        code: 200,
        data: {
          'success': true,
          'courses': r_courses,
          'message': "Success",
        }
      }
    }
  },

  {

  }
]
