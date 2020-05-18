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
