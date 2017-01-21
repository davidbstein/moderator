import ActionTypes from "../actionTypes"


const VERBOSE = true;

// currently not used.
function JSONget(uri, callback)
{
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(JSON.parse(xmlHttp.responseText));
    else if (xmlHttp.readyState < 4)
      console.log(xmlHttp.readyState, xmlHttp.status)
    else
      throw(xmlHttp)
  }
  xmlHttp.open("GET", uri, true);
  xmlHttp.send(null);
}

function JSONpost(uri, postData, callbacks=[])
{
  if (VERBOSE) console.log(`requesting ${uri} with ${JSON.stringify(postData)} -- (callbacks: ${callbacks.length})`)
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
      const response = JSON.parse(xmlHttp.responseText);
      for (let callback of callbacks.filter(fn => typeof(fn) == 'function')){
        callback(response);
      }
    }
    else if (xmlHttp.readyState < 4){
      // this is fine.
    }
    else
      throw(xmlHttp)
  }
  xmlHttp.open("POST", uri, true);
  xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlHttp.send(JSON.stringify(postData));
}

class Caller {
  constructor(dispatch){
    this.dispatch=dispatch;
  }
  process_response(response_action_type, data){
    this.dispatch({
      type: response_action_type,
      data: data,
    })
  }
  post(uri, data, submit_action_type, response_action_type, callback) {
    this.dispatch({type: submit_action_type, data: data})
    JSONpost(
      uri,
      data,
      [this.process_response.bind(this, response_action_type), callback]
    )
  }
}

export default class {
  constructor(dispatch){
    this.caller = new Caller(dispatch);
  }
  new_comment_vote(question_id, comment_id, vote, callback){
    this.caller.post(
      "/api/new_comment_vote",
      {question_id, comment_id, vote},
      ActionTypes.COMMENT.VOTE,
      ActionTypes.COMMENT.VOTE_ACK,
      callback,
    );
  }
  new_question_vote(question_id, vote, callback){
    this.caller.post(
      "/api/new_question_vote",
      {question_id, vote},
      ActionTypes.QUESTION.VOTE,
      ActionTypes.QUESTION.VOTE_ACK,
      callback,
    );
  }
  new_comment(question_id, content, callback){
    this.caller.post(
      "/api/new_comment",
      {question_id, content},
      ActionTypes.COMMENT.SUBMIT,
      ActionTypes.COMMENT.SUBMIT_ACK,
      callback,
    );
  }
  new_question(event_lookup, content){
    this.caller.post(
      "/api/new_question",
      params,
      ActionTypes.QUESTION.SUBMIT,
      ActionTypes.QUESTION.SUBMIT_ACK,
    );
  }
  new_event(org_id, params){
    this.caller.post(
      "/api/new_event",
      params,
      ActionTypes.EVENT.SUBMIT,
      ActionTypes.EVENT.SUBMIT_ACK,
    );
  }
  get_question(question_id, callback){
    this.caller.post(
      "/api/get_question",
      {question_id},
      ActionTypes.QUESTION.REQUEST,
      ActionTypes.QUESTION.RECIEVE,
      callback,
    );
  }
  get_event(lookup_id){
    this.caller.post(
      "/api/get_event",
      {lookup_id},
      ActionTypes.EVENT.REQUEST,
      ActionTypes.EVENT.RECIEVE,
    );
  }
}
