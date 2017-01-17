import React from 'react'
import {connect} from 'react-redux'
import QuestionList from './question-list'
import API from '../client-model/API'

export default connect(
  storeState => storeState,
  dispatch => ({API: new API(dispatch)})
)(
  class Event extends React.Component {
    constructor(props) {
      super(props);
      props.API.get_event(1);
    }
    render() {
      const e = this.props.state.events[this.props.event_id];
      return <div className="event">
        <div className="page-header">
          <div className="page-header-container">
            <div className="event-title page-title">{e.event.title}</div>
            <div className="logout-button"><a href="/logout">logout</a></div>
          </div>
        </div>
        <div className="underheader" />
        <div className="unique-link-container">
          Add new questions using {' '}
          <a href={`/post_question/${e.event.lookup_id}`}>this link</a>.
          You do not need to be signed in to post a question.
        </div>
        <div className="event-question-list">
          <QuestionList questions={e.questions} />
        </div>
      </div>
    }
  }
);
