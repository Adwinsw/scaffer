import request from '@/utils/request'

export function getList(controller, model, params) {
  return request({
    url: '/' + controller + '/' + model + '_member/',
    method: 'get',
    data: params
  })
}

export function post(controller, model, params) {
  return request({
    url: '/' + controller + '/' + model + '_member/',
    method: 'post',
    data: params
  })
}

export function update(controller, model, params, id) {
  return request({
    url: '/' + controller + '/' + model + '_member/' + id + '/',
    method: 'patch',
    data: params
  })
}

export function destroy(controller, model, pk) {
  return request({
    url: '/' + controller + '/' + model + '_member/' + pk,
    method: 'delete'
  })
}
