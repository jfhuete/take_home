import React from "react"
import { Link } from "react-router-dom"

import Grid from "@mui/material/Grid"

import menuItems from "@/menuItems"

import styles from "./Menu.module.css"


const Menu = () => {

  const renderMenuItems = () =>
    Object.keys(menuItems).map(name => {
      const url = menuItems[name].url
      return (
        <li item key={name} xs={12} className={ styles.menuItems }>
          <Link to={url}>
            { name }
          </Link>
        </li>
      )
    })

  return (
    <Grid container spacing={0} className={ styles.MenuContainer }>
      <ul>
        { renderMenuItems() }
      </ul>
    </Grid>
  )
}

export default Menu
