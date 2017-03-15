import React from 'react'
import {connect} from 'react-redux'
import Question from './question'

export default class QuestionList extends React.Component {
  constructor(props) {
    super(props);
    const original_scores = {}
    Object.values(this.props.questions).forEach(
      (q) => original_scores[q.question.id] = q.question.score
    )
    this.state = {
      original_scores: original_scores
    }
  }
  componentWillReceiveProps(nextProps) {
    const original_scores = {...this.state.original_scores}
    Object.values(nextProps.questions).forEach(
      (q) => {
        const score = original_scores[q.question.id];
        if (score == undefined)
          original_scores[q.question.id] = q.question.score;
      }
    )
    this.setState({original_scores: original_scores});
  }
  vote(question_id, vote) {
    this.props.vote(question_id, vote);
  }
  render() {
    return <div>
      {
        Object.values(this.props.questions).sort(
          (qa, qb) => {
            return (
              this.state.original_scores[qb.question.id] -
              this.state.original_scores[qa.question.id]
              );
          }
        ).map(
          (question, _k) => {
            return <Question
              question={question}
              key={_k}
              upvote={this.vote.bind(this, question.question.id, 1)}
              downvote={this.props.allow_downvotes ? this.vote.bind(this, question.question.id, -1) : null}
            />
          }
        )
      }
    </div>
  }
}
