import React, { Component } from "react";
import _ from "lodash";

class TableBody extends Component {

  render() {
    const { data, columns } = this.props;

    return (
      <tbody>
      {data.map(item => (
        <tr key={item}>
          {columns.map(column => (
            <td key={column.label}>
              {_.get(item, column.path)}
            </td>
          ))}
        </tr>
      ))}



      </tbody>
    );
  }
}

export default TableBody;
