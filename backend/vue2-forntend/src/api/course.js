import request from '@/utils/request'

export function getUserCourses(uid) {
  return request({
    url: `/api/user/${uid}/courses`,
    method: 'get',
    uid
  })
}

export function getCourseTaskByCid(uid, cid) {
  return request({
    url: `/api/user/${uid}/course/${cid}/tasks`,
    method: 'get',
    uid,
    cid
  })
}

export function getResourceByCid(uid, cid) {
  return request({
    url: `/api/user/${uid}/course/${cid}/resources`,
    method: 'get',
    uid,
    cid
  })
}

export function getNoticesByCid(uid, cid) {
  return request({
    url: `/api/user/${uid}/course/${cid}/notifications`,
    method: 'get',
    uid,
    cid
  })
}


export function addResource(data, uid, cid) {
  console.log(data)
  return request({
    url: `/api/user/${uid}/course/${cid}/resources/new`,
    method: 'post',
    data
  })
}