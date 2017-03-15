import React from 'react'
import {connect} from 'react-redux'

// TODO: the syling here is SO BAD. like, so bad. really bad.

export default class Vote extends React.Component {
  render() {
    return <div className="vote">
      <div className="upvote" onClick={this.props.upvote}>
        <div className="upvote-arrow" />
      </div>
      <div className="vote-score"> {this.props.score} </div>
      {this.props.downvote && 
        <div className="downvote" onClick={this.props.downvote}>
          <div className="downvote-arrow" />
        </div>
      }
    </div>
  }
}
