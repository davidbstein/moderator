import actionTypes from "../actionTypes"

const initial_state = {
  org: {},
  events: {},
}

export default function(state=initial_state, action) {
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
