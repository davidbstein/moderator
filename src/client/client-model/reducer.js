import actionTypes from "../actionTypes"

const initial_state = {
  org: {},
  event_lookup: {},
  e_id2lookup: {},
  questions: {},
}


function init_state(mutable_state, action){
  const preload_info = window._INFO;
  switch (preload_info.page){
    case 'event':
      mutable_state.org = preload_info.org_info;
      return mutable_state;
    case 'org':
      mutable_state.org = preload_info.org_info;
      preload_info.events.forEach(
        (event) => {
          mutable_state.event_lookup[event.lookup_id] = event;
          mutable_state.e_id2lookup[event.id] = event.lookup_id;
        }
      );
      return mutable_state;
    default:
      return mutable_state;
  }
}

const merge_questions = (new_questions, original_questions) => {
  const merged_questions = {...original_questions}
  for (var question_id in new_questions){
    if (!merged_questions[question_id]){
      merged_questions[question_id] = new_questions[question_id];
    } else {
      merged_questions[question_id].score = new_questions[question_id].score;
      merged_questions[question_id].upvotes = new_questions[question_id].upvotes;
      merged_questions[question_id].downvotes = new_questions[question_id].downvotes;
    }
  }
  return merged_questions;
}

export default function(state=initial_state, action) {
  const next_state = {...state};
  let event, event_lookup_id;
  switch (action.type) {
    case "moderator/INIT":
      init_state(next_state, action)
      return next_state
    case actionTypes.EVENT.REQUEST:
      event = next_state.event_lookup[action.data.lookup_id] || {}
      next_state.event_lookup[action.data.lookup_id] = {
        ...event,
        loading: false
      }
      return next_state;
    case actionTypes.EVENT.RECIEVE:
      event = action.data.event;
      next_state.event_lookup[event.lookup_id] = {
        event: event,
        questions: merge_questions(
            action.data.questions,
            next_state.event_lookup[event.lookup_id].questions
          ),
      };
      next_state.questions = {
        ...next_state.event_lookup[event.lookup_id].questions,
        ...next_state.questions,
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
