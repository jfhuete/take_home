import React, { Component } from "react"

import MUIDataTable from "mui-datatables"

import { api_url } from "@/constants"


class Actors extends Component {

  constructor(props) {
    super(props)

    this.state = {
      actors: []
    }
  }

  async componentDidMount() {
    try {
      const response = await fetch(api_url)
      const body = await response.json()

      this.setState({ actors: body })

    } catch (err) {
      throw new Error(
        `Can't GET ${api_url}. Error ${err}`)
    }

  }

  render() {
    return (
      <MUIDataTable
        title="Actors List"
        data={ this.state.actors }
      />
      // <div>
      //   Actors
      // </div>
    )
  }
}

export default Actors

