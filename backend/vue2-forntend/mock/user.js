
const tokens = {
  admin: {
    // token: 'admin-token'
    token: '1234567'
  },
  editor: {
    token: 'editor-token'
  }
}

const users = {
  '1234567': {
    roles: ['admin'],
    introduction: 'I am a super administrator',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Super Admin'
  },
  'editor-token': {
    roles: ['editor'],
    introduction: 'I am an editor',
    avatar: 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
    name: 'Normal Editor'
  }
}

const user_info = {
    "uid": 1,
    "student_id": "17373001",
    "name": "北小航",
    "email": "0000001@qq.com",
    "created_at": "2020-03-15 16:22:37"
}

export default [
  // user login
  {
    url: '/vue-admin-template/user/login',
    type: 'post',
    response: config => {
      // const { username } = config.body
      // const token = tokens[username]
      // console.log(username)
      console.log(config.body)
      const token = tokens['admin']
      
      var success = false;
      // mock error
      if (success) {
        return {
          code: 200,
          msg: 'Success.'
        }
      }
      else {
        return {
          code: 404,
          msg: 'Fail'
        }
      }
      
    }
  },
  {
    url: '/vue-admin-template/user/register',
    type: 'post',
    response: config => {
      // const { username } = config.body
      // const token = tokens[username]

      console.log(config.body)
      
      var success = true

      if (success) {
        return {
          code: 200
        }
      }
      else {
        return {
          code: 401,
          msg: 'register failed'
        }
      }
      
    }
  },

  // get user info
  {
    url: '/vue-admin-template/user/info\.*',
    type: 'get',
    response: config => {
      const { token } = config.query
      // const info = users[token]
      console.log(token)
      const info = users['1234567']

      console.log(config.query)
      // mock error
      if (!info) {
        return {
          code: 50008,
          message: 'Login failed, unable to get user details.'
        }
      }

      return {
        code: 200,
        data: info
      }
    }
  },

  // get user info detail
  {
    url: '/vue-admin-template/api/user/info',
    type: 'get',
    response: config => {
      const { uid } = config.query
      var hasInfo = true

      console.log(config.query)

      if (hasInfo) {
        return {
          code: 200,
          data: {
            'success': true,
            'message': "Success.",
            'user': user_info,
          }
        }
      }
      else {
        return {
          code: 200,
          data: {
            'success': false,
            'message': 'User not exists.'
          }
        }
      }
      
    }
  },

  // user logout
  {
    url: '/vue-admin-template/user/logout',
    type: 'post',
    response: _ => {
      return {
        code: 200,
        data: 'success'
      }
    }
  }
]
