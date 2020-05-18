import Cookies from 'js-cookie'

const TokenKey = 'vue_admin_template_token'
const UidKey = 'uid_key'
const NameKey = 'name_key'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

export function setUid(uid) {
  return Cookies.set(UidKey, uid)
}

export function getUid() {
  return Cookies.get(UidKey)
}

export function setName(name) {
  return Cookies.set(NameKey, name)
}

export function getName() {
  return Cookies.get(NameKey)
}