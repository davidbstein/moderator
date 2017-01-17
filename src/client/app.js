import ReactDOM from 'react-dom'
import React from "react"
import {createStore, combineReducers, applyMiddleware, compose} from 'redux'
import {Provider} from 'react-redux'

import Moderator from './moderator'
import reducer from './client-model/reducer'
import viewReducer from './client-model/viewReducer'

const render = (store) => {
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
  )(combineReducers({
    state: reducer,
    viewState: viewReducer,
  }));

render(store);
