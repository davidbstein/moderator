import actionTypes from "../actionTypes"

const test_state = {
  page: "event",
  state: {
    lookup_id: 1
  }
}

const initial_state = {
  page: undefined,
  state: {}
}

export default function(state=initial_state, action) {
  switch (action.type) {
    case "@@INIT":
      if (window._INFO.page == undefined){
        return {
          ...state,
          page: 'home',
          state: {
          }
        }
      }
      if (window._INFO.page == 'event'){
        return {
          ...state,
          page: 'event',
          state: {
            lookup_id: window._INFO.lookup_id,
          },
        }
      }
      return state
    case actionTypes.PLACEHOLDER:
      return state
    default:
      return state
  }
}
