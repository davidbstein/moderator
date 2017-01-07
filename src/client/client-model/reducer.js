import actionTypes from "../actionTypes"

const test_state = {
  events: {
    1: {
      "event": {
        "domain": "appboy.com",
        "description": "my test event",
        "title": "my test event",
        "owner_email": "david.stein@appboy.com",
        "moderators": [
          "david.stein@appboy.com"
        ],
        "lookup_id": "626094d76b8726212ae04111f9220f2",
        "id": 1
      },
      "questions": {
        2: {
          "question": {
              "flag_note": [],
            "e_id": 1,
            "flagged": false,
            "content": "this is my second one",
            "comment_count": 0,
            "score": 230,
            "id": 2
          },
          "comments": [],
        },
        1: {
          "question": {
            "flag_note": [],
            "e_id": 1,
            "id": 1,
            "content": "this is my first question",
            "comment_count": 0,
            "score": -80,
            "flagged": false
          },
          "comments": [
            {
              "flag_note": null,
              "q_id": 1,
              "owner_email": "david.stein@appboy.com",
              "id": 1,
              "content": "this is comment one",
              "score": 0,
              "flagged": null
            },
            {
              "flag_note": null,
              "q_id": 1,
              "owner_email": "david@appboy.com",
              "id": 2,
              "content": "this is comment two",
              "score": 1,
              "flagged": null
            }
          ]
        }
      }
    }
  }
}

const initial_state = {
  events: {
  },
}

export default function(state=test_state, action) {
  switch (action) {
    case actionTypes.PLACEHOLDER:
      return action.message
    default:
      return state
  }
}
