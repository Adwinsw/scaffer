import Cookies from 'js-cookie'

const keytoken = 'usertoken'
const csrftoken = 'csrftoken'
const keysession = 'sessionid'

export function getToken(TokenKey) {
  return Cookies.get(TokenKey)
}

export function setToken(TokenKey, token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  Cookies.remove(csrftoken)
  Cookies.remove(keysession)
  return Cookies.remove(keytoken)
}

export function getCookie(name) {
  var cookieValue = null
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';')
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim()
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        // break;
      }
    }
  }
  return cookieValue
}
