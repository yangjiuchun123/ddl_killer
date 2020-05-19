import request from '@/utils/request'

export function getAllTasks(uid) {
  return request({
    url: `/api/user/${uid}/tasks`,
    method: 'get',
    uid
  })
}

export function deleteOneTask(uid, tid) {
  console.log('delete task:')
  console.log(tid)
  return request({
    url: `/api/user/${uid}/tasks/${tid}/delete`,
    method: 'post',
  })
}

export function createOneTask(uid, data) {
  console.log('create a new task:')
  console.log(data)
  return request({
    url: `/api/user/${uid}/tasks/new`,
    method: 'post',
    data,
  })
}

export function modifyOneTask(uid, data) {
  console.log('modify task:')
  console.log(data)
  return request({
    url: `/api/user/${uid}/tasks/new`,
    method: 'post',
    data
  })
}

export function updateFromCourse(uid, data) {
  console.log('get from course:')
  console.log(data)
  return request({
    url: `/api/user/${uid}/update_course`,
    method: 'post',
    data
  })
}
