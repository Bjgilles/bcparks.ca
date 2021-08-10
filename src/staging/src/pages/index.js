// TODO: Mobile - Fix mobile hamburger bottom menu item stutter on expand
// TODO: Mobile - Fix mobile hamburger menu expand being cut off by static alert
// TODO: Mobile - Add search bar to mobile hamburger menu(last item) - CKEditor is preventing the appropriate element structure, could take some time
// TODO: Mobile - Fix text font-weight issue caused by opacity on card body
// TODO: Mobile - Fix footer search icon positioning on all mobile breakpoints(does not scale with current implementation)

import React from "react"
import { graphql } from "gatsby"
import Header from "../components/header"
import Footer from "../components/footer"
import Zone from "../components/zone"
import MainSearch from "../components/mainSearch"
import "../styles/home.scss"

export const query = graphql`
  query {
    strapiWebsites(Name: { eq: "BCParks.ca" }) {
      Footer
      Header
      Name
      Navigation
      id
      homepage {
        id
        Template
        Content {
          id
          strapi_component
          HTML
        }
      }
    }
    allStrapiPages {
      totalCount
      nodes {
        id
        Slug
        Template
        Content
      }
    }
    allStrapiActivityTypes(sort: { fields: activityName }) {
      totalCount
      nodes {
        activityName
        activityNumber
      }
    }
    allStrapiFacilityTypes(sort: { fields: facilityName }) {
      totalCount
      nodes {
        facilityName
        facilityNumber
      }
    }
    allStrapiProtectedArea(sort: { fields: protectedAreaName }) {
      nodes {
        parkActivities {
          activityType
          isActive
          isActivityOpen
          name
        }
        parkFacilities {
          facilityType
          isActive
          isFacilityOpen
          name
        }
        id
        orcs
        latitude
        longitude
        protectedAreaName
        parkNames {
          parkName
          id
          parkNameType
        }
        status
        typeCode
        marineProtectedArea
      }
    }
  }
`
const cmsUrl =  process.env.REACT_APP_CMS_BASE_URL
export default function Home({ data }) {
  const zonesContent = data?.strapiWebsites?.homepage?.Content || []

  return (
    <div>
      <Header>
        {data.strapiWebsites.Header}
      </Header>
      {/* <Menu>
        {data.strapiWebsites.Navigation}
      </Menu> */}
      <div className="alert alert-warning alert-dismissable rounded-0" role="alert" id="home-alert">
        <button type="button" className="close" data-dismiss="alert">×</button>
        <div className="row">
          <div className="col-1 pl-0"><img className="alert-exclamation" src={`${cmsUrl}/uploads/alert_32px_520c5ebbca.png`} alt="exclamation" className="d-inline-flex" /></div>
          <div className="col-11"><span className="text-center">Some parks are currently affected by wildfire activity. <a href="#" className="alert-link d-inline-flex">See all advisories</a>.</span></div>
        </div>
      </div>
      <div class="park-search">
      <MainSearch
            data={{
              activities: data.allStrapiActivityTypes.nodes,
              facilities: data.allStrapiFacilityTypes.nodes,
              protectedAreas: data.allStrapiProtectedArea.nodes,
            }}
      />
      </div>
      <div id="main">
        {zonesContent.map(content => {
          return (
            <Zone key={content.id} zoneID={`Zone${content.id}`} Content={content} />  
          )
        })}
      </div>
      <Footer>
        {data.strapiWebsites.Footer}
      </Footer>
    </div>
  )
}
