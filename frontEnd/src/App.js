import React, { Component } from "react";
import { Route, Redirect, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import PredictForm from "./components/predictForm";
import NotFound from "./components/notFound";
import NavBar from "./components/navBar";

import "react-toastify/dist/ReactToastify.css";
import "./App.css";

class App extends Component {
  state = {};

  render() {
    return (
      <React.Fragment>
        <ToastContainer />
        <main className="container-fluid px-0 m-0">
          <Switch>
            <Route path="/predict/new" component={PredictForm} />
            <Route path="/not-found" component={NotFound} />
            <Redirect from="/" exact to="/predict/new" />
            <Redirect to="/not-found" />
          </Switch>
        </main>
      </React.Fragment>
    );
  }
}

export default App;
