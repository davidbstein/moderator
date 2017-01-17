/*
Constants builder - outputs an object that maps to string key constants.

eg -
  actionTypes.DISPLAY.QUESTION_OPENED == "DISPLAY.QUESTION_OPENED"
*/

const actions = {
  DISPLAY: [
    "QUESTION_OPENED",
    "QUESTION_CLOSED",
  ],
  EVENT: [
    "SUBMIT",
    "SUBMIT_ACK",
    "REQUEST",
    "RECIEVE",
  ],
  QUESTION: [
    "SUBMIT",
    "SUBMIT_ACK",
    "REQUEST",
    "RECIEVE",
    "VOTE",
    "VOTE_ACK",
  ],
  COMMENT: [
    "SUBMIT",
    "SUBMIT_ACK",
    "VOTE",
    "VOTE_ACK",
  ]
};

export default ((actions) => {
  let to_export = {};
  for (let k of Object.keys(actions)){
    to_export[k] = {}
    for (let v of actions[k])
      to_export[k][v] = k + "." + v;
  }
  return to_export;
})(actions);
