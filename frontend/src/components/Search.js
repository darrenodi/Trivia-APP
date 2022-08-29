import React, { Component } from "react";

class Search extends Component {
  state = {
    search: "",
  };

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.search);
  };

  handleInputChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <input
          placeholder="Search questions..."
          name="search"
          onChange={this.handleInputChange}
        />
        <input type="submit" value="Submit" className="button" />
      </form>
    );
  }
}

export default Search;
