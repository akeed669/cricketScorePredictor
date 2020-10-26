import React from "react";

const Input = ({ name, label, error, ...rest }) => {
  return (
    <div className="form-group form-inline row">
      <div className="form-group col-lg-4">
        <label htmlFor={name}>{label}</label>
      </div>
      <div className="form-group col-lg-2">
        <input {...rest} id={name} name={name} className="form-control" />
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
    </div>
  );
};

export default Input;
