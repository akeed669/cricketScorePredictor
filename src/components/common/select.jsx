import React from "react";

const Select = ({ name, label, options, error, ...rest }) => {
  return (
    <div className="form-group form-inline row">
      <div className="form-group col-lg-4">
        <label htmlFor={name}>{label}</label>
      </div>
      <div className="form-group col-lg-2">
        <select name={name} id={name} {...rest} className="form-control">
          <option value="" />
          {options.map((option) => (
            <option key={option._id} value={option._id}>
              {option.name}
            </option>
          ))}
        </select>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
    </div>
  );
};

export default Select;
