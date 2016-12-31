import React from "react"
import ReactDOM from 'react-dom'

class Moderator extends React.Component {
  render() {
    return <div>
      this is the page
    </div>
  }
}

const target = document.getElementById("target")
ReactDOM.render(<Moderator/>, target)
