import React from 'react'
import {connect} from 'react-redux'
import Comment from './comment'
import CommentInput from './comment-input'
import API from '../client-model/API'

export default connect(
  storeState => ({}),
  dispatch => ({API: new API(dispatch)})
)(
  class CommentList extends React.Component {
    constructor(props) {
      super(props);
      this.state = {slider: false};
    }
    componentWillMount() {
      this.props.API.get_question(this.props.question_id);
    }
    toggleSlider() {
      this.props.API.get_question(this.props.question_id);
      this.setState({slider: !this.state.slider});
    }
    render() {
      let comment_divs = <div className="comment-loader loader"></div>
      let comment_count = "loading";
      if (this.props.comments != null){
        const comments = Object.values(this.props.comments);
        comment_divs = comments.map((comment, _k)=>{
          return <Comment comment={comment} key={_k} />
        });
        comment_count = comments.length;
      }
      return <div className="comment-list">
        <div
          className={`slider slider-${this.state.slider}`}
          style={{maxHeight: (3+comment_count) * 256}}
        >
          {comment_divs}
          <CommentInput />
        </div>
        <div className="slider-toggle" onClick={this.toggleSlider.bind(this)}>
          {this.state.slider ? `hide comments` : `${comment_count} comments`}
        </div>
      </div>
    }
  }
)