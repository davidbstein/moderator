import actionTypes from "../actionTypes"

const initial_state = {
  page: undefined,
  state: {}
}

export default function(state=initial_state, action) {
  switch (action.type) {
    case "moderator/INIT":
      switch (window._INFO.page){
        case 'event':
          return {
            ...state,
            page: 'event',
            state: {
              lookup_id: window._INFO.lookup_id,
            },
          }
        case 'org':
          return {
            ...state,
            page: 'org',
            state: {
              org_domain: window._INFO.org_info.domain,
            },
          }
        default:
          return {
            ...state,
            page: 'home',
            state: {},
          }
      }
      return state
    default:
      return state
  }
}
