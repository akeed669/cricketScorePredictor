import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
//import { getMovie, saveMovie } from "../services/movieService";
import { getSelectValues, predictScore } from "../services/selectService";

class PredictForm extends Form {
  state = {
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
    matchYears:[],
    bowlTeams: [],
    batTeams: [],
    prediction: 0,
    errors: {},
  };

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
      matchYears:names.matchYears,
      venues: names.venues,
      bowlTeams: names.bowlTeams,
      batTeams: names.batTeams,
    });
  }

  async componentDidMount() {
    await this.populateLists();
    //await this.populateMovie();
  }

  doSubmit = async () => {
    const { data: prediction } = await predictScore(this.state.data);
    console.log(typeof prediction);
    this.setState({ prediction });
    //this.props.history.push("/movies");
  };

  render() {
    return (
      <div className="container-fluid h-100 bg-light text-dark">
        <div className="row justify-content-center">
          <h1 className="display-3">Prediction Form</h1>
        </div>
        <div className="row justify-content-center align-items-center h-100 mt-5 mb-5">
          <div className="col col-xl-5">
            <form onSubmit={this.handleSubmit}>
              {this.renderSelect("matchYear", "Match Year", this.state.matchYears)}
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
              <div className="row justify-content-center mt-4 mb-4">
                {this.renderButton("PREDICT SCORE!")}
              </div>
              {this.state.prediction > 0 && (
                <div>
                  <p>The predicted score is {this.state.prediction} </p>
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default PredictForm;
