import ReactDOM from 'react-dom'
import React from "react"
import {createStore, combineReducers, applyMiddleware, compose} from 'redux'
import {Provider} from 'react-redux'

import Moderator from './moderator'
import reducer from './client-model/reducer'
import API from './client-model/API'

const render = () => {
  ReactDOM.render(
    <Provider store={store}>
      <div>
        <Moderator />
      </div>
    </Provider>,
    document.getElementById("target")
  )
};

// dev tools
const store = (
    window.devToolsExtension && window._DEV_MODE ?
    window.devToolsExtension()(createStore) :
    createStore
  )(reducer);

const api = new API(store)

render();
