import React from "react"
import { css } from "@emotion/react"
import { useStaticQuery, Link, graphql } from "gatsby"

import { rhythm } from "../utils/typography"
import HTMLArea from "../components/HTMLArea"
import Media from "../components/media"

export default function Zone(props)
{
  if (props.Content==null) {
    return null;
  }
    return (
    <div>
      <div id={props.zoneID}>
          <HTMLArea isVisible={props.Content.strapi_component=='parks.html-area' ? true:false} >
            {props.Content.HTML}
          </HTMLArea>
          <Media  url={props.Content.strapi_component=='parks.image' ? props.Content.Media.localFile.url: null } 
          isVisible={props.Content.strapi_component=='parks.image' ? true:false} />
        </div>        
    </div>
  )
}