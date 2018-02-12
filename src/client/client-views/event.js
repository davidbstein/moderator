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
      props.API.get_event(props.lookup_id);
    }
    reload_question(question_id){
      this.props.API.get_question(question_id,
        () => this.setState({question_pending: false})
      );
    }
    question_vote(question_id, vote){
      this.props.API.new_question_vote(
        question_id,
        vote,
        this.reload_question.bind(this, question_id)
      );
    }
    render() {
      const e = this.props.state.event_lookup[this.props.lookup_id];

      const o = this.props.state.org;
      if (!e || !e.event){
        return <div className="loader event-loader" />
      }
      return <div className="event">
        <div className="page-header">
          <div className="page-header-container">
            <div className="event-title page-title">
              <span className="org-title">
                <a href="/"> {o.domain} moderator </a>
              </span>
            {" > "}
            {e.event.title}
            </div>
            <div className="logout-button"><a href="/logout">logout</a></div>
          </div>
        </div>
        <div className="underheader" />
        <div classsName="unique-link-container">
          Add new questions using {' '}
          <a href={`/post_question/${e.event.lookup_id}`}>this link</a>.
          You do not need to be signed in to post a question.
        </div>
        <div className="event-question-list">
          <QuestionList
            questions={e.questions}
            vote={this.question_vote.bind(this)}
          />
          <a className="card new-question-card" href={`/post_question/${e.event.lookup_id}`}>
            Submit a new question
          </a>
        </div>
      </div>
    }
  }
);
