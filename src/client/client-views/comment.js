import React from 'react'
import {connect} from 'react-redux'
import Vote from './vote'

export default class Comment extends React.Component {
  upvote() {
    console.log("upvote comment")
  }
  downvote () {
    console.log("downvote comment")
  }
  render() {
    const c = this.props.comment;
    return <div className="comment">
      <Vote upvote={this.upvote} downvote={this.downvote} score={c.score}/>
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
