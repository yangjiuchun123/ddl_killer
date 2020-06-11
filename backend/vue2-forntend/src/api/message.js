import request from '@/utils/request'

export function getMessage(uid, type) {
    return request({
      url: `/api/user/${uid}/message`,
      method: 'get',
      uid,
      params: { type }
    })
  }

  export function readMessage(uid, mid) {
    return request({
      url: `/api/user/${uid}/message/${mid}/read`,
      method: 'post',
      uid,
      mid
    })
  }

  export function broadcastMessage(uid, data) {
    return request({
      url: `/api/user/${uid}/broadcast`,
      method: 'post',
      uid,
      data
    })
  }