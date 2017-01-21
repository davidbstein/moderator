import React from 'react'
import {connect} from 'react-redux'
import API from '../client-model/API'
import EventCard from './event-card'

export default connect(
  storeState => storeState,
  dispatch => ({API: new API(dispatch)})
)(
  class Org extends React.Component {
    constructor(props) {
      super(props);
    }
    render() {
      const o = this.props.state.org;
      return <div className="org">
        <div className="page-header">
          <div className="page-header-container">
            <div className="org-title page-title">
              <a href="/"> {o.domain} moderator </a>
            </div>
            <div className="logout-button"><a href="/logout">logout</a></div>
          </div>
        </div>
        <div className="underheader" />
        <div className="new-event-link-container">
          To create a new event, please contact your
          team's <a href="mailto:david.stein@appboy.com">
          moderator admin</a>.
        </div>
        <div className="org-event-list">
        {
          Object.values(this.props.state.event_lookup).sort(
            (a, b) => a.id - b.id
          ).map(
            (e) => {
              console.log(e);
              return <EventCard key={e.id} event={e} />
            }
          )
        }
        </div>
      </div>
    }
  }
);
