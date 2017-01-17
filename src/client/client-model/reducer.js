import actionTypes from "../actionTypes"

const test_state = {
  events: {
    1: {
      "event": {
        "domain": "appboy.com",
        "description": "static placholder",
        "title": "static placholder",
        "owner_email": "david.stein@appboy.com",
        "moderators": [
          "david.stein@appboy.com"
        ],
        "lookup_id": "626094d76b8726212ae04111f9220f2",
        "id": 1
      },
      "questions": {}
    }
  }
}

const initial_state = {
  org: {},
  events: {},
}

export default function(state=test_state, action) {
  const next_state = {...state};
  switch (action.type) {
    case actionTypes.EVENT.REQUEST:
      event = next_state.events[action.data.event_id] || {}
      next_state.events[action.data.event_id] = {
        ...event,
        loading: false
      }
      return next_state;
    case actionTypes.EVENT.RECIEVE:
      next_state.events[action.data.event.id] = action.data;
      return next_state;
    case actionTypes.QUESTION.REQUEST:
      return next_state;
    case actionTypes.QUESTION.RECIEVE:
      event = next_state.events[action.data.question.e_id]
      let question_id = action.data.question.id
      next_state.events[event.event.id].questions[question_id] = {
        ...action.data
      }
      return next_state
    default:
      return state
  }
}
