import React from 'react'
import {connect} from 'react-redux'
import CommentList from './comment-list'
import Vote from './vote'

export default class Question extends React.Component {
  upvote() {
    console.log("up");
  }
  downvote() {
    console.log("down");
  }
  render() {
    const q = this.props.question.question;
    const comments = this.props.question.comments;
    return <div className="question">
      <div className="question-container">
        <Vote upvote={this.upvote} downvote={this.downvote} score={q.score}/>
        <div className="question-content">{q.content}</div>
      </div>
      <div className="question-comments">
        <CommentList comments={comments} />
      </div>
    </div>
  }
}
