import ActionTypes from "../actionTypes"

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
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
      const response = JSON.parse(xmlHttp.responseText);
      for (callback in Object.values(callbacks))
        callback(response);
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
  process_response(response_action_type, callback, data){
    this.dispatch({
      type: response_action_type,
      data: data,
    })
    if (callback) callback(data);
  }
  post(uri, data, submit_action_type, response_action_type, callback) {
    this.dispatch({type: submit_action_type, data: data})
    JSONpost(
      uri,
      data,
      this.process_response.bind(this, response_action_type, callback)
    )
  }
}

export default class {
  constructor(dispatch){
    this.caller = new Caller(dispatch);
  }
  new_comment_vote(question_id, comment_id, vote){
    this.caller.post(
      "api/new_comment_vote",
      params,
      ActionTypes.COMMENT.VOTE,
      ActionTypes.COMMENT.VOTE_ACK,
    );
  }
  new_question_vote(question_id, vote){
    this.caller.post(
      "api/new_question_vote",
      params,
      ActionTypes.QUESTION.VOTE,
      ActionTypes.QUESTION.VOTE_ACK,
    );
  }
  new_comment(question_id, content){
    this.caller.post(
      "api/new_comment",
      params,
      ActionTypes.COMMENT.SUBMIT,
      ActionTypes.COMMENT.SUBMIT_ACK,
    );
  }
  new_question(event_id, content){
    this.caller.post(
      "api/new_question",
      params,
      ActionTypes.QUESTION.SUBMIT,
      ActionTypes.QUESTION.SUBMIT_ACK,
    );
  }
  new_event(org_id, params){
    this.caller.post(
      "api/new_event",
      params,
      ActionTypes.EVENT.SUBMIT,
      ActionTypes.EVENT.SUBMIT_ACK,
    );
  }
  get_question(question_id){
    this.caller.post(
      "api/get_question",
      {question_id},
      ActionTypes.QUESTION.REQUEST,
      ActionTypes.QUESTION.RECIEVE,
    );
  }
  get_event(event_id){
    this.caller.post(
      "api/get_event",
      {event_id},
      ActionTypes.EVENT.REQUEST,
      ActionTypes.EVENT.RECIEVE,
    );
  }
}
