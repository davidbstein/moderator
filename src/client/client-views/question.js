import React from 'react'
import {connect} from 'react-redux'
import CommentList from './comment-list'
import Vote from './vote'

export default class Question extends React.Component {
  render() {
    const q = this.props.question.question;
    const comments = this.props.question.comments;
    return <div className="question">
      <div className="question-container">
        <Vote
          upvote={this.props.upvote}
          downvote={this.props.downvote}
          score={q.score}
          upvotes={q.upvotes}
          downvotes={q.downvotes}
        />
        <div className="question-content">{q.content}</div>
      </div>
      <div className="question-comments">
        <CommentList comments={comments} question_id={q.id} />
      </div>
    </div>
  }
}
