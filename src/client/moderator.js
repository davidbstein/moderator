import React from 'react'
import {connect} from 'react-redux'
import Event from './client-views/event'

export default connect(
  storeState => storeState
)(
  class Moderator extends React.Component {
    render() {
      switch (this.props.viewState.page) {
        case "event":
          return <Event />
        default:
          return <div> error :( </div>
      }
    }
  }
);
