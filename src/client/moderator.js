import React from 'react'
import {connect} from 'react-redux'

export default connect(
  storeState => {
    return {
      store: storeState
    }
  }
)(
  class extends React.Component {
    render() {
      console.log(this.props.store)
      return <div>
        WOO!
      </div>
    }
  }
);
