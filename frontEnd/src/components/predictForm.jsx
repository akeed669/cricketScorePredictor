
import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
import ResultsTable from './resultsTable';
import { getSelectValues, predictScore } from "../services/selectService";


class PredictForm extends Form {
  initialState = {
    data: {
      venue: "",
      batTeam: "",
      bowlTeam: "",
      matchYear: "",
      runs: 0,
      wickets: 0,
      strikerRuns: 0,
      nonStrikerRuns: 0,
      balls: 0,
    },
    venues: [],
    bowlTeams: [],
    batTeams: [],
    prediction: 0,
    ballsPred:0,
    predictions:[],
    errors: {},
  };

  state=this.initialState;

  schema = {
    venue: Joi.string().required().label("Match venue"),

    batTeam: Joi.string().required().label("Batting team"),

    bowlTeam: Joi.string().required().label("Bowling team"),

    matchYear: Joi.number().required().label("Year of Match"),

    runs: Joi.number().required().min(0).max(350).label("Runs scored"),

    wickets: Joi.number().required().min(0).max(10).label("Wickets fallen"),

    strikerRuns: Joi.number()
      .required()
      .min(0)
      .max(200)
      .label("Runs scored by striker"),

    nonStrikerRuns: Joi.number()
      .required()
      .min(0)
      .max(200)
      .label("Runs scored by non-striker"),

    balls: Joi.number().required().min(0).max(300).label("Balls bowled"),
  };

  async populateLists() {
    const { data: names } = await getSelectValues();

    this.setState({
      venues: names.venues,
      bowlTeams: names.bowlTeams,
      batTeams: names.batTeams,
    });
  }

  async componentDidMount() {
    await this.populateLists();
  }

  doSubmit = async () => {
    const { data: prediction } = await predictScore(this.state.data);
    const deliveries = this.state.data.balls
    this.setState({ ballsPred:deliveries, prediction, predictions:[...this.state.predictions,{prediction:prediction, deliveries:deliveries}] });
  };

  render() {
    return (

      <div className="container-fluid">

        <div className="row navbar navbar-expand-lg navbar-light bg-light">


          <h2 className="col navbar-brand">
            Cricket Score Predictor
          </h2>


          {this.state.prediction > 0 && (
            <h2 className="col navbar-brand text-primary">
              The predicted score after {this.state.ballsPred} balls is {this.state.prediction}
            </h2>
          )}

          {this.state.prediction == 0 &&(<h2 className="col navbar-brand">Prediction Form</h2>)}

          <div className="col">
            <button onClick={this.handleAlternate} className="btn btn-primary pull-right">
              Reset Form
            </button>
          </div>


        </div>

        <div className="container h-100 text-dark">

          <div className="row h-100 mb-5">

            <div className="col-3 mr-5">

              {this.state.prediction > 0 && (
              <div className="border h2 text-center mb-4 text-primary bg-light">
                <p> {this.state.data.batTeam} </p>
                <p> VS </p>
                <p> {this.state.data.bowlTeam} </p>
              </div>
              )}

              <div>
                <ResultsTable prediction={this.state.predictions}></ResultsTable>
              </div>

            </div>

            <div className="col-7">

              <form onSubmit={this.handleSubmit}>
                {this.renderSelect("matchYear", "Match Year", ["2018","2019","2020"])}
                {this.renderSelect("venue", "Match Venue", this.state.venues)}
                {this.renderSelect(
                  "batTeam",
                  "Batting Team",
                  this.state.batTeams
                )}
                {this.renderSelect(
                  "bowlTeam",
                  "Bowling Team",
                  this.state.bowlTeams
                )}
                {this.renderInput("runs", "Runs")}
                {this.renderInput("wickets", "Wickets")}
                {this.renderInput("strikerRuns", "Striker Runs")}
                {this.renderInput("nonStrikerRuns", "Non Striker Runs")}
                {this.renderInput("balls", "Balls")}

                <div className="row justify-content-center">
                  <button type="submit" disabled={this.validate()} className="btn btn-primary mt-3">
                    Predict Score!
                  </button>
                </div>

              </form>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default PredictForm;
