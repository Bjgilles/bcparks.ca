import React, { useState } from "react"
import PropTypes from "prop-types"
import {
  TextField,
  Fab,
  Dialog,
  DialogActions,
  DialogContent,
  Button,
  Link,
  Checkbox,
  FormGroup,
  FormControlLabel,
  Divider,
  Chip,
  InputAdornment
} from "@material-ui/core"
import Select from "react-select"
import "../../styles/search.scss"
import HighlightOffOutlinedIcon from "@material-ui/icons/HighlightOffOutlined"
import { navigate } from "gatsby"

const MainSearch = ({ data: { activities, facilities, protectedAreas } }) => {
  const [openFilter, setOpenFilter] = useState(false)
  const [quickSearch, setQuickSearch] = useState({
    camping: false,
    petFriendly: false,
    wheelchair: false,
    marine: false,
    ecoReserve: false,
    electricalHookup: false,
  })
  const [selectedActivities, setSelectedActivities] = useState([])
  const [selectedFacilities, setSelectedFacilities] = useState([])
  const [searchText, setSearchText] = useState("")

  const {
    camping,
    petFriendly,
    wheelchair,
    marine,
    ecoReserve,
    electricalHookup,
  } = quickSearch

  const activityItems = activities.map(a => ({
    label: a.activityName,
    value: a.activityNumber,
  }))

  const facilityItems = facilities.map(f => ({
    label: f.facilityName,
    value: f.facilityNumber,
  }))

  const handleClickOpenFilter = () => {
    setOpenFilter(true)
  }

  const handleCloseFilter = () => {
    setOpenFilter(false)
  }

  const handleQuickSearchChange = event => {
    setQuickSearch({
      ...quickSearch,
      [event.target.name]: event.target.checked,
    })
  }

  const handleActivityDelete = chipToDelete => () => {
    setSelectedActivities(chips =>
      chips.filter(chip => chip.value !== chipToDelete.value)
    )
  }

  const handleFacilityDelete = chipToDelete => () => {
    setSelectedFacilities(chips =>
      chips.filter(chip => chip.value !== chipToDelete.value)
    )
  }

  const searchParkFilter = () => {
    navigate("/park-search", {
      state: {
        quickSearch,
        selectedActivities,
        selectedFacilities,
        searchText,
      },
    })
  }

  const renderDesktop = () => {
    return (
      <div className="park-search-container-inner row align-items-center w-100 no-gutters">
        <div className="col-12">
          <div className="row no-gutters">
            <div className="col-12 park-search-intro text-center text-sm-left">
              <h2 className="heading-white-space">Welcome to BC Parks</h2>
              <p className="pt-sm-3">
                Plan your next adventure by searching for campsites and day-use
                areas around B.C.
              </p>
              <TextField
                id="park-search-text"
                variant="outlined"
                placeholder="Search by park name, location, activity..."
                className="park-search-text-box pr-2"
                value={searchText}
                onChange={event => {
                  setSearchText(event.target.value)
                }}
                onKeyPress={ev => {
                  if (ev.key === "Enter") {
                    searchParkFilter()
                    ev.preventDefault()
                  }
                }}
              />
              <Button
                  variant="contained"
                  onClick={() => {
                    handleCloseFilter()
                    searchParkFilter()
                  }}
                  className="bcgov-normal-gold mobile-search-element-height"
              >
                Search
              </Button>
            </div>
          </div>
          <div className="row no-gutters"></div>
          <div className="col-12 pl-sm-0 pt-sm-3">
            <Link
              component="button"
              className="park-search-filter"
              onClick={handleClickOpenFilter}
            >
              Filters
            </Link>
          </div>
        </div>
      </div>
    )
  }

  const renderMobile = () => {
    return (
      <div className="row align-items-center w-100 no-gutters park-search-group">
        <div className="col-12">
          <div className="row no-gutters px-3">
            <div className="col-12 text-center">
              <h2 className="heading-white-space">Plan your next adventure</h2>
            </div>
          </div>
          <div className="row no-gutters pb-2 px-3">
            <div className="col-9 pr-1">
              <TextField
                  id="park-search-text"
                  variant="outlined"
                  placeholder="Search by park name, location, activity..."
                  className="park-search-text-box mobile-search-element-height"
                  InputProps={{
                    startAdornment: (
                      <InputAdornment position="start">
                        <i className="fas fa-search"></i>
                      </InputAdornment>
                    )
                  }}
                  value={searchText}
                  onChange={event => {
                    setSearchText(event.target.value)
                  }}
                  onKeyPress={ev => {
                    if (ev.key === "Enter") {
                      searchParkFilter()
                      ev.preventDefault()
                    }
                  }}
                />
            </div>
            <div className="col-3">
              <Button
                  variant="outlined"
                  onClick={handleClickOpenFilter}
                  className="bg-transparent rounded text-light mobile-filter mobile-search-element-height"
              >
                Filters
              </Button>
            </div>
          </div>
          <div className="row no-gutters pb-2 px-3">
            <div className="col-12">
              <Button
                  variant="contained"
                  fullWidth
                  onClick={() => {
                    handleCloseFilter()
                    searchParkFilter()
                  }}
                  className="bcgov-normal-blue mobile-search-element-height"
              >
                Search
              </Button>
            </div>
          </div>
          <div className="row no-gutters px-3">
            <div className="col-12">
              <Button
                  variant="contained"
                  href="https://www.discovercamping.ca/"
                  target="_blank"
                  rel="norefferer"
                  fullWidth
                  onClick={() => {
                    handleCloseFilter()
                    searchParkFilter()
                  }}
                  className="bcgov-normal-gold mobile-search-element-height"
              >
                Book a campsite
              </Button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="park-search-container park-search-text-container">
      <div className="d-none d-lg-block v-align-abs">
        {renderDesktop()}
      </div>
      <div className="d-block d-lg-none v-align-abs">
        {renderMobile()}
      </div>
      <Dialog
        open={openFilter}
        onClose={handleCloseFilter}
        aria-labelledby="park-filter-dialog"
        className="park-filter-dialog"
      >
        <DialogContent className="park-filter-dialog-content">
          <div className="container">
            <div className="row">
              <div className="col-12">
                <TextField
                  margin="dense"
                  id="park-filter-text"
                  className="park-filter-text"
                  placeholder="Search by park name, location"
                  fullWidth
                  variant="outlined"
                  value={searchText}
                  onChange={event => {
                    setSearchText(event.target.value)
                  }}
                  onKeyPress={ev => {
                    if (ev.key === "Enter") {
                      handleCloseFilter()
                      searchParkFilter()
                      ev.preventDefault()
                    }
                  }}
                />
              </div>
            </div>
            <div className="row p20t">
              <div className="col-lg-6 col-md-6 col-sm-12">
                <FormGroup className="p30l">
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={camping}
                        onChange={handleQuickSearchChange}
                        name="camping"
                      />
                    }
                    label="Camping"
                    className="no-wrap"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={petFriendly}
                        onChange={handleQuickSearchChange}
                        name="petFriendly"
                      />
                    }
                    label="Dog friendly"
                    className="no-wrap"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={wheelchair}
                        onChange={handleQuickSearchChange}
                        name="wheelchair"
                      />
                    }
                    label="Wheelchair accessible"
                    className="no-wrap"
                  />
                </FormGroup>
              </div>
              <div className="col-lg-6 col-md-6 col-sm-12">
                <FormGroup className="p30l">
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={marine}
                        onChange={handleQuickSearchChange}
                        name="marine"
                      />
                    }
                    label="Marine park"
                    className="no-wrap"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={ecoReserve}
                        onChange={handleQuickSearchChange}
                        name="ecoReserve"
                      />
                    }
                    label="Ecological reserve"
                    className="no-wrap"
                  />
                  <FormControlLabel
                    control={
                      <Checkbox
                        checked={electricalHookup}
                        onChange={handleQuickSearchChange}
                        name="electricalHookup"
                      />
                    }
                    label="Electrical hookups"
                    className="no-wrap"
                  />
                </FormGroup>
              </div>
            </div>
            <Divider className="m20t" />
            <div className="row p20t">
              <div className="col-12">
                <div className="p20l park-select-label">Activities</div>
                <Select
                  id="activities-select"
                  options={activityItems}
                  value={selectedActivities}
                  controlShouldRenderValue={false}
                  isClearable={false}
                  isMulti
                  onChange={e => {
                    setSelectedActivities(e)
                  }}
                  className="park-filter-select"
                  variant="outlined"
                  placeholder="Add an activity from this list"
                  styles={{ menuPortal: base => ({ ...base, zIndex: 9999 }) }}
                  menuPosition={"fixed"}
                />
              </div>
            </div>
            <div className="row p20t">
              <div className="col-12">
                {selectedActivities.map(a => (
                  <Chip
                    key={a.value}
                    label={a.label}
                    onDelete={handleActivityDelete(a)}
                    variant="outlined"
                    className="park-filter-chip"
                    deleteIcon={<HighlightOffOutlinedIcon />}
                  />
                ))}
              </div>
            </div>
            <Divider className="m20t" />
            <div className="row p20t">
              <div className="col-12">
                <div className="p20l park-select-label">Facilities</div>
                <Select
                  id="facilities-select"
                  options={facilityItems}
                  value={selectedFacilities}
                  controlShouldRenderValue={false}
                  isClearable={false}
                  isMulti
                  onChange={e => {
                    setSelectedFacilities(e)
                  }}
                  className="park-filter-select"
                  variant="outlined"
                  placeholder="Add a facility from this list"
                  styles={{ menuPortal: base => ({ ...base, zIndex: 9999 }) }}
                  menuPosition={"fixed"}
                />
              </div>
            </div>
            <div className="row p20t">
              <div className="col-12">
                {selectedFacilities.map(f => (
                  <Chip
                    key={f.value}
                    label={f.label}
                    onDelete={handleFacilityDelete(f)}
                    variant="outlined"
                    className="park-filter-chip"
                    deleteIcon={<HighlightOffOutlinedIcon />}
                  />
                ))}
              </div>
            </div>
            <Divider className="m20t" />
          </div>
        </DialogContent>
        <DialogActions>
          <div className="container">
            <div className="row">
              <div className="col-12 p30">
                <Button
                  variant="contained"
                  onClick={() => {
                    handleCloseFilter()
                    searchParkFilter()
                  }}
                  className="bcgov-button bcgov-normal-blue"
                >
                  Search
                </Button>
              </div>
            </div>
          </div>
        </DialogActions>
      </Dialog>
    </div>
  )
}

MainSearch.propTypes = {
  data: PropTypes.shape({
    activities: PropTypes.array.isRequired,
    facilities: PropTypes.array.isRequired,
  }),
}

export default MainSearch
