import React from "react";
import Joi from "joi-browser";
import Form from "./common/form";
import { getMovie, saveMovie } from "../services/movieService";
import { getBattingTeams } from "../services/selectService";

class PredictForm extends Form {
  state = {
    data: { title: "", genreId: "", numberInStock: "", dailyRentalRate: "" },
    genres: [],
    errors: {},
  };

  schema = {
    _id: Joi.string(),
    title: Joi.string().required().label("Title"),
    genreId: Joi.string().required().label("Genre"),

    runs: Joi.number().required().min(0).max(350).label("Runs scored"),

    wickets: Joi.number().required().min(0).max(10).label("Wickets fallen"),

    balls: Joi.number().required().min(0).max(300).label("Balls bowled"),

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
  };

  async populateGenres() {
    const theResult = await getBattingTeams();
    console.log(theResult);
    this.setState({ genres: theResult });
  }

  async populateMovie() {
    try {
      const movieId = this.props.match.params.id;
      if (movieId === "new") return;

      const { data: movie } = await getMovie(movieId);
      this.setState({ data: this.mapToViewModel(movie) });
    } catch (ex) {
      if (ex.response && ex.response.status === 404)
        this.props.history.replace("/not-found");
    }
  }

  async componentDidMount() {
    await this.populateGenres();
    await this.populateMovie();
  }

  mapToViewModel(movie) {
    return {
      _id: movie._id,
      title: movie.title,
      genreId: movie.genre._id,
      numberInStock: movie.numberInStock,
      dailyRentalRate: movie.dailyRentalRate,
    };
  }

  doSubmit = async () => {
    await saveMovie(this.state.data);
    this.props.history.push("/movies");
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
              {this.renderInput("date", "Match Date", "date")}
              {this.renderSelect("venueID", "Match Venue", this.state.genres)}
              {this.renderSelect(
                "batTeamID",
                "Batting Team",
                this.state.genres
              )}
              {this.renderSelect(
                "bowlTeamID",
                "Bowling Team",
                this.state.genres
              )}
              {this.renderInput("runs", "Runs")}
              {this.renderInput("balls", "Balls")}
              {this.renderInput("wickets", "Wickets")}
              {this.renderInput("strikerRuns", "Striker Runs")}
              {this.renderInput("nonStrikerRuns", "Non Striker Runs")}
              <div className="row justify-content-center mt-4 mb-4">
                {this.renderButton("PREDICT SCORE!")}
              </div>
            </form>
          </div>
        </div>
      </div>
    );
  }
}

export default PredictForm;
