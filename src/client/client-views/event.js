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
          <div> Question list </div>
        </div>
        <div className="event-question-list">
          <QuestionList questions={e.questions} />
        </div>
      </div>
    }
  }
);
