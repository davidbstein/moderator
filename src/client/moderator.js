import React from 'react'
import {connect} from 'react-redux'
import Question from './client-views/question'
import Event from './client-views/event'
import Org from './client-views/org'

export default connect(
  storeState => storeState
)(
  class Moderator extends React.Component {
    render() {
      switch (this.props.viewState.page) {
        case "org":
          return <Org
            org_domain={this.props.viewState.state.org_domain}
          />
        case "event":
          return <Event
            lookup_id={this.props.viewState.state.lookup_id}
          />
        // case "question":
        //   const question = this.props.viewState.state.question
        //   return <QuestionPage
        //     question={question}
        //   />
        default:
          return <div> error :( </div>
      }
    }
  }
);
