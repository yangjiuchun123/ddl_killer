import request from '@/utils/request'

export function login(data) {
  return request({
    // url: '/vue-admin-template/user/login',
    baseURL: '',
    url: '/api/login',
    method: 'post',
    data
  })
}

export function register(data) {
  return request({
    baseURL: '',
    url: '/api/register',
    // url: '/vue-admin-template/user/register',
    method: 'post',
    data
  })
}


// 首页右上角的info
export function getInfo(token) {
  return request({
    url: '/vue-admin-template/user/info',
    method: 'get',
    params: { token }
  })
} 

// 个人中心的info
export function getUserInfo(uid) {
  return request({
    url: `/api/user/${uid}/info`,
    method: 'get',
    uid
  })
}

// 获取个人中心的设置
export function getUserSetting(uid) {
  return request({
    url: `/api/user/${uid}/settings`,
    method: 'get',
    uid
  })
}
//更改个人中心的设置
export function modifyUserSetting(uid, data) {
  return request({
    baseURL: '',
    url: `/api/user/${uid}/settings`,
    method: 'post',
    data,
    uid
  })
}


export function modifyUserInfo(uid, data) {
  return request({
    baseURL: '',
    url: `/api/modify`,
    method: 'post',
    data,
    uid
  })
}

export function logout() {
  return request({
    baseURL: '',
    url: '/api/logout',
    // url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}

export function getPubKey() {
  return request({
    baseURL: '',
    url: '/api/security/pub-key',
    // url: '/vue-admin-template/user/logout',
    method: 'get'
  })
}

//忘记密码相关
//@ data：{uid：'17370000'}
export function sendAuthCode(data){
  return request({
    url: '/api/user/forget/email',
    method: 'post',
    data
    //后端返回 告诉前端该账号是否存在
  })
}
//data:{uid:'17370000',verify_code:'6666'}
export function verifyAuthCode(data){
  return request({
    url: '/api/user/forget/verify',
    method: 'post',
    data
  })
}

//@ data:{uid:'',password:'hahahaha'}
export function resetPWD(data){
  return request({
    baseURL: '',
    url: `/api/user/forget/reset`,
    method: 'post',
    data
  })   
}

// 用户反馈
export function feedback(uid, data) {
  return request({
    baseURL: '',
    url: `/api/user/${uid}/report`,
    method: 'post',
    data,
  })   
}
