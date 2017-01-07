import React from 'react'
import {connect} from 'react-redux'
import Vote from './vote'

export default class Comment extends React.Component {
  render() {
    const c = this.props.comment;
    return <div className="comment">
      <Vote upvote={1} downvote={1} score={c.score}/>
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
