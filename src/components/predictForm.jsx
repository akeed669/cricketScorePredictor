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
      matchDate: "",
      runs: 0,
      wickets: 0,
      balls: 0,
      strikerRuns: 0,
      nonStrikerRuns: 0,
    },
    venues: [],
    bowlTeams: [],
    batTeams: [],
    prediction: 0,
    errors: {},
  };

  schema = {
    venue: Joi.string().required().label("Match venue"),

    batTeam: Joi.string().required().label("Batting team"),

    bowlTeam: Joi.string().required().label("Bowling team"),

    matchDate: Joi.date().required().label("Date of Match"),

    runs: Joi.number().required().min(0).max(350).label("Runs scored"),

    wickets: Joi.number().required().min(0).max(10).label("Wickets fallen"),

    balls: Joi.number().required().min(0).max(300).label("Balls bowled"),

    strikerRuns: Joi.number()
      .required()
      .min(0)
      .max(200)
      .less(Joi.ref("runs"))
      .label("Runs scored by striker"),

    nonStrikerRuns: Joi.number()
      .required()
      .min(0)
      .max(200)
      .less(Joi.ref("runs"))
      .label("Runs scored by non-striker"),
  };

  async populateVenues() {
    const { data: names } = await getSelectValues();

    this.setState({
      venues: names.venues,
      bowlTeams: names.bowlTeams,
      batTeams: names.batTeams,
    });
  }

  // async populateMovie() {
  //   try {
  //     const movieId = this.props.match.params.id;
  //     if (movieId === "new") return;

  //     const { data: movie } = await getMovie(movieId);
  //     this.setState({ data: this.mapToViewModel(movie) });
  //   } catch (ex) {
  //     if (ex.response && ex.response.status === 404)
  //       this.props.history.replace("/not-found");
  //   }
  // }

  async componentDidMount() {
    await this.populateVenues();
    //await this.populateMovie();
  }

  // mapToViewModel(movie) {
  //   return {
  //     _id: movie._id,
  //     title: movie.title,
  //     genreId: movie.genre._id,
  //     numberInStock: movie.numberInStock,
  //     dailyRentalRate: movie.dailyRentalRate,
  //   };
  // }

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
              {this.renderInput("matchDate", "Match Date", "date")}
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
              {this.renderInput("balls", "Balls")}
              {this.renderInput("wickets", "Wickets")}
              {this.renderInput("strikerRuns", "Striker Runs")}
              {this.renderInput("nonStrikerRuns", "Non Striker Runs")}
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
