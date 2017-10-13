import React from 'react'
import {connect} from 'react-redux'
import Vote from './vote'

export default class Comment extends React.Component {
  upvote() {
    this.props.vote(1);
  }
  downvote () {
    this.props.vote(-1);
  }
  render() {
    const c = this.props.comment;
    return <div className="comment">
      <Vote
        upvote={this.upvote.bind(this)}
        downvote={this.props.allow_downvotes ? this.downvote.bind(this) : null}
        score={c.score}
      />
      <div className="comment-content">
        <div className="comment-author">
          {c.owner_email}
        </div>
        <div className="comment-text">
          {c.content}
        </div>
      </div>
    </div>
  }
}
