import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info/',
    method: 'get'
  })
}

export function logout(token) {
  return request({
    url: '/auth/logout/',
    method: 'post'
  })
}
