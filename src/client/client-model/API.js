
function JSONget(uri, callback)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(JSON.parse(xmlHttp.responseText));
    else
      throw(xmlHttp)
  }
  xmlHttp.open("GET", uri, true);
  xmlHttp.send(null);
}

function JSONpost(uri, postData, callback)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
      callback(JSON.parse(xmlHttp.responseText));
    else
      throw(xmlHttp)
  }
  xmlHttp.open("POST", uri, true);
  xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xmlHttp.send(JSON.stringify(postData));
}

export default class {
  constructor(store){
    this.store = store;
  }
  new_comment_vote(params){
    JSONpost(
      "api/new_comment_vote",
      params,
      (data) => {
        console.log("resp to new_comment_vote:", data);
      })
  }
  new_question_vote(params){
    JSONpost(
      "api/new_question_vote",
      params,
      (data) => {
        console.log("resp to new_question_vote:", data);
      })
  }
  new_comment(params){
    JSONpost(
      "api/new_comment",
      params,
      (data) => {
        console.log("resp to new_comment:", data);
      })
  }
  new_question(params){
    JSONpost(
      "api/new_question",
      params,
      (data) => {
        console.log("resp to new_question:", data);
      })
  }
  new_event(params){
    JSONpost(
      "api/new_event",
      params,
      (data) => {
        console.log("resp to new_event:", data);
      })
  }
  get_question(question_id){
    JSONpost(
      "api/get_question",
      {},
      (data) => {
        console.log("resp to get_question: ", data)
      })
  }
  get_event(event_id){
    JSONpost(
      "api/get_event",
      {},
      (data) => {
        console.log("resp to get_event: ", data)
      })
  }
}
