import React from "react"
import MegaMenu from "./MegaMenu"

import { rhythm } from "../utils/typography"

export default function Header({ children, mode = 'external', content = [] }) {
  if (mode === 'internal') {
    return (
      <MegaMenu content={content} />
    )
  }
  return (
    <header id='header' dangerouslySetInnerHTML={{ __html: children}}/>
  )
}