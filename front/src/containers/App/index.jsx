import React from "react"
import { Routes, Route } from "react-router-dom"

import Grid from "@mui/material/Grid"
import Paper from "@mui/material/Paper"

import Menu from "./components/Menu"
import Actors from "@/sections/Actors"
import Movies from "@/sections/Movies"

import styles from "./App.module.css"


const App = () => {
  return (
    <Grid container>
      <Grid item xs={12} className={ styles.AppHeader }>
        Take Home
      </Grid>
      <Grid item xs={12}>
        <Grid container>
          <Grid item xs={1}>
            <Menu />
          </Grid>
          <Grid item xs={2}>
            <Paper className={ styles.AppContent }>
              <Routes>
                <Route path="actors" element={<Actors />} />
                <Route path="movies" element={<Movies />} />
              </Routes>
            </Paper>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  )
}

export default App
