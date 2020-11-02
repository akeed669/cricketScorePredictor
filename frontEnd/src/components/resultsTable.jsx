import React, { Component } from "react";
import Table from "./common/table";

class ResultsTable extends Component {

  // columns for populating orders table
  columns = [
    {path:"prediction", label: "Predictions" },
    {path:"deliveries",label: "Balls" },
  ];

  render() {

    // all predictions received as a prop
    let {prediction} = this.props;

    return (
      <Table
        columns={this.columns}
        data={prediction}
      />
    );
  }
}

export default ResultsTable;
