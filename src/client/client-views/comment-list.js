import React from 'react'
import {connect} from 'react-redux'
import Comment from './comment'
import CommentInput from './comment-input'

export default class CommentList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {slider: true};
  }
  toggleSlider() {
    console.log('hi');
    this.setState({slider: !this.state.slider});
  }
  render() {
    const comments = Object.values(this.props.comments);
    return <div className="comment-list">
      <div
        className={`slider slider-${this.state.slider}`}
        style={{maxHeight: (3+comments.length) * 256}}
      >
        {
          comments.map((comment, _k)=>{
            return <Comment comment={comment} key={_k} />
          })
        }
        <CommentInput />
      </div>
      <div className="slider-toggle" onClick={this.toggleSlider.bind(this)}>
        {this.state.slider ? `hide comments` : `${comments.length} comments`}
      </div>
    </div>
  }
}
