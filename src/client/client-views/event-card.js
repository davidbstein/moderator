import React from 'react'
import {connect} from 'react-redux'

export default class EventCard extends React.Component {
  render() {
    const e = this.props.event;
    return <div className="event-card card">
      <div className="event-info-container">
        <div className="event-title">{this.props.event.title}</div>
      </div>
      <div className="event-card-actions">
        <button
          onClick={
            ()=>{
              window.location=`/post_question/${e.lookup_id}`;
            }
          }
          className="event-card-button">
          Submit a question
        </button>
        <button
          onClick={
            ()=>{
              window.location=`/e/${encodeURIComponent(e.title.replace('-','_'))}-${e.lookup_id}`;
            }
          }
          className="event-card-button">
          View, vote, and comment on questions
        </button>
      </div>
    </div>
  }
}
