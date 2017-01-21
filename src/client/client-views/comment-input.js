import React from 'react'
import {connect} from 'react-redux'

export default class CommentInput extends React.Component {
  submit_content(){
    this.props.submit_content(this.textInput.value);
  }
  render() {
    const comments = this.props.comments;
    return <div className="comment-input">
      <div> Add a (non-anonymous) comment: </div>
      <textarea ref={(elem) => {this.textInput = elem}}/>
      <div className="buttons">
        <button onClick={this.submit_content.bind(this)}> comment </button>
      </div>
    </div>
  }
}
