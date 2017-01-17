import actionTypes from "../actionTypes"

const test_state = {
  page: "event",
  state: {
    event_id: 1
  }
}

const initial_state = {
  page: undefined,
  state: {}
}

export default function(state=test_state, action) {
  switch (action.type) {
    case actionTypes.PLACEHOLDER:
      return action.message
    default:
      return state
  }
}
