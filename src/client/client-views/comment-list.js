import React from 'react'
import {connect} from 'react-redux'
import Comment from './comment'
import CommentInput from './comment-input'
import API from '../client-model/API'

const COMMENT_MAX_HEIGHT = 95;

export default connect(
  storeState => ({}),
  dispatch => ({API: new API(dispatch)})
)(
  class CommentList extends React.Component {
    constructor(props) {
      super(props);
      this.state = {
        slider: false,
        question_pending: false,
      };
    }
    componentWillMount() {
      this.props.API.get_question(this.props.question_id);
    }
    toggleSlider() {
      this.props.API.get_question(this.props.question_id);
      this.setState({slider: !this.state.slider});
    }
    comment_vote(comment_id, vote){
      this.props.API.new_comment_vote(
        this.props.question_id,
        comment_id,
        vote,
        this.reload_comments.bind(this)
      );
    }
    reload_comments(){
      this.props.API.get_question(this.props.question_id,
        () => this.setState({question_pending: false})
      );
    }
    comment_create(content){
      if (content == ''){
        return
      }
      this.setState({question_pending: true})
      this.props.API.new_comment(
        this.props.question_id,
        content,
        this.reload_comments.bind(this)
      );
    }
    render() {
      let comment_divs = <div className="comment-loader loader"></div>
      let comment_count = 0;
      if (this.props.comments != null){
        const comments = Object.values(this.props.comments);
        comment_divs = comments.map((comment, _k)=>{
          return <Comment
            comment={comment}
            vote={this.comment_vote.bind(this, comment.id)}
            key={_k}
          />
        });
        comment_count = comments.length;
      }
      let input_div = <div className="comment-loader loader"></div>
      let anonymous_link_div = <div></div>
      if (!this.state.question_pending)
        anonymous_link_div = <div className="anonymous-comment-link"> Add an anonymous comment using <a href={`/post_comment/${this.props.question_id}`}>this link</a>.</div>
        input_div = <CommentInput
          submit_content={this.comment_create.bind(this)}
        />
      return <div className="comment-list">
        <div
          className={`slider slider-${this.state.slider}`}
          style={{maxHeight: (3+comment_count) * COMMENT_MAX_HEIGHT}}
        >
          {comment_divs}
          {anonymous_link_div}
          {input_div}
        </div>
        <div className="slider-toggle" onClick={this.toggleSlider.bind(this)}>
          {this.state.slider ? `hide comments` : `${comment_count} comments`}
        </div>
      </div>
    }
  }
)
