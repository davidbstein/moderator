import React from 'react'
import {connect} from 'react-redux'

export default class CommentInput extends React.Component {
  render() {
    const comments = this.props.comments;
    return <div className="comment-input">
      <div> Add a (non-anonymous) comment: </div>
      <textarea />
      <div className="buttons">
        <button onclick={(e) => {console.log(e);}}> comment </button>
      </div>
    </div>
  }
}
