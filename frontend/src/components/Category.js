import React, { Component } from "react";
import $ from "jquery";

class Category extends Component {
  constructor() {
    super();
    this.state = {
      category: "",
      visibleButton: false,
    };
  }

  flipVisibility() {
    this.setState({ visibleButton: !this.state.visibleButton });
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  submitQuestion = (event) => {
    this.flipVisibility();
    event.preventDefault();
    $.ajax({
      url: "/categories", //TODO: update request URL
      type: "POST",
      dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({
        category: this.state.category,
      }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert("Unable to add Category. Please try your request again");
        return;
      },
    });
  };

  render() {
    return (
      <div Style="margin-bottom:50px;">
        <div
          className="show-category button"
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleButton ? "Add" : "Add"} Category
        </div>
        <div className="answer-holder">
          <span
            style={{
              visibility: this.state.visibleButton ? "visible" : "hidden",
            }}
          >
            <form
              className="form-view"
              id="add-question-form"
              onSubmit={this.submitQuestion}
            >
              <label>
                Category :
                <input
                  type="text"
                  name="category"
                  onChange={this.handleChange}
                />
              </label>
              <input type="submit" className="button" value="Submit" />
            </form>
          </span>
        </div>
      </div>
    );
  }
}

export default Category;
