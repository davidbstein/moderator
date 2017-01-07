import React from 'react'
import {connect} from 'react-redux'
import Question from './question'

export default class QuestionList extends React.Component {
  render() {
    return <div>
      {
        Object.values(this.props.questions).sort((question) => {
          return "sort-key";
        }).map((question, _k) => {
          return <Question question={question} key={_k}/>
        })
      }
    </div>
  }
}
