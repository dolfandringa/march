import React, { Component } from "react";
import { Menu } from "semantic-ui-react";
import { NavLink } from "react-router-dom";

export default class NavBar extends Component {
  render() {
    return (
      <Menu>
        <Menu.Item
          onClick={this.handleItemClick}
          as={NavLink}
          to="/"
          name="home"
        >
          Home
        </Menu.Item>
        <Menu.Item
          onClick={this.handleItemClick}
          as={NavLink}
          to="/about"
          name="about"
        >
          About
        </Menu.Item>
      </Menu>
    );
  }
}
