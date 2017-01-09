import React from 'react'
import {connect} from 'react-redux'
import QuestionList from './question-list'

export default connect(
  storeState => storeState
)(
  class Event extends React.Component {
    render() {
      const e = this.props.state.events[this.props.viewState.state.event_id];
      return <div className="event">
        <div className="page-header">
          <div className="event-title page-title">{e.event.title}</div>
        </div>
        <div className="underheader" />
        <div className="unique-link-container">
          Add new questions using {' '}
          <a href={`/post_question/${e.event.lookup_id}`}>this link</a>.
          You do not need to be signed in to use this link.
        </div>
        <div className="event-question-list">
          <QuestionList questions={e.questions} />
        </div>
      </div>
    }
  }
);
