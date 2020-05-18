import request from '@/utils/request'

export function getAllTasks(uid) {
  return request({
    baseURL: '',
    url: `/api/user/${uid}/tasks`,
    method: 'get',
    uid
  })
}

export function deleteOneTask(data) {
  console.log('delete task:')
  console.log(data)
  return request({
    url: '/api/tasks/delete',
    method: 'post',
    data
  })
}

export function createOneTask(uid, data) {
  console.log('create a new task:')
  console.log(data)
  return request({
    baseURL: '',
    url: `/api/user/${uid}/tasks/new`,
    method: 'post',
    data
  })
}

export function modifyOneTask(uid, data) {
  console.log('modify task:')
  console.log(data)
  return request({
    url: `/api/user/${uid}/tasks/modify`,
    method: 'post',
    data
  })
}

export function alterTaskState(uid, tid) {
    console.log('finish task: '+uid + " " + tid)
    return request({
        url: `/api/user/${uid}/task/${tid}/alterTaskState`,
        method: 'post',
    })
}
