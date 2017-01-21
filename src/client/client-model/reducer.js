import actionTypes from "../actionTypes"

const initial_state = {
  org: {},
  event_lookup: {},
  e_id2lookup: {},
  questions: {},
}

export default function(state=initial_state, action) {
  const next_state = {...state};
  let event, event_lookup_id;
  switch (action.type) {
    case actionTypes.EVENT.REQUEST:
      event = next_state.event_lookup[action.data.lookup_id] || {}
      next_state.event_lookup[action.data.lookup_id] = {
        ...event,
        loading: false
      }
      return next_state;
    case actionTypes.EVENT.RECIEVE:
      event = action.data.event;
      next_state.event_lookup[event.lookup_id] = action.data;
      next_state.questions = {
        ...next_state.questions,
        ...next_state.event_lookup[event.lookup_id].questions,
      }
      next_state.e_id2lookup[event.id] = event.lookup_id
      return next_state;
    case actionTypes.QUESTION.REQUEST:
      return next_state;
    case actionTypes.QUESTION.RECIEVE:
      event_lookup_id = next_state.e_id2lookup[action.data.question.e_id]
      event = next_state.event_lookup[event_lookup_id]
      let question_id = action.data.question.id
      next_state.event_lookup[event_lookup_id].questions[question_id] = {
        ...action.data
      }
      return next_state
    case actionTypes.QUESTION.VOTE:
      return next_state
    case actionTypes.QUESTION.VOTE_ACK:
      return next_state
    case actionTypes.COMMENT.VOTE:
      return next_state
    case actionTypes.COMMENT.VOTE_ACK:
      return next_state
    case actionTypes.COMMENT.SUBMIT:
      return next_state
    case actionTypes.COMMENT.SUBMIT_ACK:
      return next_state
    default:
      return state
  }
}
