#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import json
import requests
from datetime import datetime
from os import getenv

# variables

headers = {
    'Content-Type': 'application/json'
}


# var_args = Variable.get("url_var", deserialize_json=True)

class Parks_ETL:

    def __init__(self):

        self.par_api_url_base = getenv('PAR_API_URL', 'https://a100.gov.bc.ca/pub/parws')
        self.bcgn_api_url_base = getenv('BCGN_API_URL', 'https://apps.gov.bc.ca/pub/bcgnws')
        self.strapi_base = getenv('x', 'https://dev-cms.bcparks.ca')
        self.bcwfs_api_url_base = getenv('BCWFS_API_URL',
                                         ('https://services6.arcgis.com/ubm4tcTYICKBpist/arcgis/rest/'
                                          'services/British_Columbia_Bans_and_Prohibition_Areas/FeatureServer/0/query'))
        self.token = getenv("STRAPI_API_TOKEN")

    ### Import PAR functions
    def _get_data_from_par(self):
        '''
         retrieve protected area information from PAR via an API

        :return: the results of the api call to PAR
        '''

        api_url = f"{self.par_api_url_base}/protectedLands?protectedLandName=%25&protectedLandTypeCodes=CS,ER,PA,PK,RA"

        result = None

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                # convert json to Python object
                data = response.json()

                if 'data' in data:
                    result = data["data"]
                else:
                    print('data does not conform to expectations!')

            return result
        except Exception as e:
            print('Error invoking webservice', e)
            raise

    def _dump_par_data(self, data):
        '''

        :param data:
        :return:
        '''

        api_url = f'{self.strapi_base}/protected-areas?token={self.token}'

        for pro_land in data:
            try:
                # check object relationships
                # sites
                index_count = 0
                for site in pro_land["sites"]:
                    pro_land["sites"][index_count] = self.create_or_update_site(site)
                    index_count = index_count + 1

                # managementAreas
                index_count = 0
                for mArea in pro_land["managementAreas"]:
                    pro_land["managementAreas"][index_count] = self.create_or_update_mgmt_area(mArea)
                    index_count = index_count + 1

                pro_area = self.get_protected_area_from_strapi(pro_land["orcs"])

                #protected areas
                if pro_area is None:
                    api_url = f'{self.strapi_base}/protected-areas?token={self.token}'
                    # rectified_payload = python_to_proper_json_string(pro_land)
                    response = requests.post(api_url, json=pro_land, headers=headers)

                    if response.status_code == 200:
                        data = response.json()

                        print(
                            f'Protected Area with id: {data["id"]} and ORCS:{pro_land["orcs"]}  successfully created!')
                    else:
                        print(f'dump par data: Unplanned status code returned - {response.status_code}')
                else:
                    print(f'Protected area ORCS:{pro_land["orcs"]} already exist in strapi')
                    api_url = f'{self.strapi_base}/protected-areas/{pro_area["id"]}?token={self.token}'
                    # rectified_payload = python_to_proper_json_string(pro_land)
                    # del pro_land["sites"]
                    # del pro_land["managementAreas"]
                    response = requests.put(api_url, json=pro_land, headers=headers)

                    if response.status_code == 200:
                        data = response.json()

                        print(
                            f'Protected Area with id: {data["id"]} and ORCS:{pro_land["orcs"]}  successfully updated!')
                    else:
                        print(f'dump par data: Unplanned status code returned - {response.status_code}')

            except Exception as e:
                print('dump par data: Error invoking webservice', e)
                raise

    def create_or_update_site(self, site):
        '''
        Given the Site info passed in, if the site exists in Strapi it will update Strapi's information.
        If it does not exist in strapi, it will be created there

        :param site: a dict with SIte information to add to strapi
        :return: strapi id of the Site
        '''

        newSite = self.get_site_from_strapi(site["orcsSiteNumber"])

        if newSite is None:
            # create new site
            newSite = self.create_site_in_strapi(site)
        else:
            print(f'Site with orcsSiteNumber: {site["orcsSiteNumber"]} already exists')
            newSite = self.update_site_in_strapi(newSite["id"], site)

        return newSite

    def create_or_update_mgmt_area(self, mArea):
        '''
        Given the Management Area info passed in, if the site exists in Strapi it will update Strapi's information.
        If it does not exist in strapi, it will be created there


        :param mArea: a dict containing information for the Management Area
        :return: the strapi id for the Management Area
        '''

        newMArea = self.get_mgmt_area_from_strapi(mArea["managementAreaNumber"])

        if newMArea is None:
            # create new mgmt area
            newMArea = self.create_mgmt_area_in_strapi(mArea)
        else:
            print(f'Management Area with managementAreaNumber: {mArea["managementAreaNumber"]} already exists')
            newSite = self.update_mgmt_area_in_strapi(newMArea["id"], mArea)

        return newMArea

    def get_or_create_section(self, section):
        '''
        Given the Section info passed in, if the site exists in Strapi it will update Strapi's information.
        If it does not exist in strapi, it will be created there

        :param section: a dict with Section information to add to strapi
        :return: strapi id of the Section
        '''
        newSection = self.get_section_from_strapi(section["sectionNumber"])

        if newSection is None:
            # create new section
            newSection = self.create_section_in_strapi(section)
            print(f'Section with sectionNumber: {section["sectionNumber"]} successfully created!')
        else:
            print(f'Section with sectionNumber: {section["sectionNumber"]} already exists')

        return newSection

    def get_or_create_region(self, region):
        '''
        Given the Resion info passed in, if the site exists in Strapi it will update Strapi's information.
        If it does not exist in strapi, it will be created there

        :param region: a dict with SIte information to add to strapi
        :return: strapi id of the Region
        '''
        newRegion = self.get_region_from_strapi(region["regionNumber"])

        if newRegion is None:
            # create new region
            newRegion = self.create_region_in_strapi(region)
            print(f'Section with regionNumber: {region["regionNumber"]} successfully created!')
        else:
            print(f'Section with regionNumber: {region["regionNumber"]} already exists')

        return newRegion

    def _get_data_from_bcgn(self, data):
        '''
         retrieve protected area information from BC Geographical Names Information System (BCGN) via an API

        :return: the results of the api call to BCGN
        '''
        result = []
        try:
            indx = 0
            for pro_land in data:
                featureId = pro_land["featureId"]

                api_url = f"{self.bcgn_api_url_base}/names/{featureId}.json"
                response = requests.get(api_url, headers=headers)

                if response.status_code == 200:
                    # convert json to Python object
                    data = response.json()
                    data["orcs"] = pro_land["orcNumber"]
                    result.append(data)

            return result
        except Exception as e:
            print('Error invoking webservice', e)
            raise

    def _dump_bcgn_data(self, data):
        '''

        :param data:
        :return:
        '''
        park_type_legal_id = self.get_park_type_legal_from_strapi()

        for park_name in data:
            try:

                existing_park_name = self.get_park_names_legal_from_strapi(park_name["protectedArea"],
                                                                           park_type_legal_id)

                if existing_park_name is None:
                    api_url = f'{self.strapi_base}/park-names?token={self.token}'
                    # rectified_payload = python_to_proper_json_string(pro_land)
                    response = requests.post(api_url, json=park_name, headers=headers)

                    if response.status_code == 200:
                        data = response.json()
                        print(f'Park Name for ORCS:{park_name["orcs"]}  successfully created!')
                    else:
                        print(
                            f'_dump_bcgn_data: dump par data: Unplanned status code returned - {response.status_code}  {park_name}')
                else:
                    print(f'Park Name for ORCS:{park_name["orcs"]} already exist in strapi')
                    api_url = f'{self.strapi_base}/park-names/{existing_park_name["id"]}?token={self.token}'
                    response = requests.put(api_url, json=park_name, headers=headers)

                    if response.status_code == 200:
                        result = response.json()
                        print(
                            f'Protected Area with id: {result["id"]} and ORCS:{park_name["orcs"]}  successfully updated!')
                    else:
                        print(f'_dump_bcgn_data: Unplanned status code returned - {response.status_code}')

            except Exception as e:
                print('_dump_bcgn_data: Error invoking webservice', e)
                raise

    def _get_data_from_bcwfs(self):
        '''
         retrieve Fire Ban Prohibition information via an API

        :return: the results of the api call
        '''

        api_url = f"{self.bcwfs_api_url_base}?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=OBJECTID%20ASC&resultOffset=0&resultRecordCount=50&cacheHint=true&quantizationParameters=%7B%22mode%22%3A%22edit%22%7D"

        result = None

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                # convert json to Python object
                result = response.json()

            return result
        except Exception as e:
            print('Error invoking webservice', e)
            raise

    def _dump_bcwfs_data(self, data):
        '''

        :param data:
        :return:
        '''
        api_url = f'{self.strapi_base}/Fire-Ban-Prohibitions?token={self.token}'
        print(f'dump data {data} ')
        self.delete_fireban_prohibitions_from_strapi()
        try:
            for feature in data:
                # persist object
                print(f'dump data: data - {feature}')
                response = requests.post(api_url, json=feature, headers=headers)

                if response.status_code == 200:
                    result = response.json()
                    print(f'Record with id: {result["id"]} successfully created!')
                else:
                    print(f'_dump_bcwfs_data: Unplanned status code returned - {response.status_code}')

        except Exception as e:
            print('_dump_bcwfs_data: Error invoking webservice', e)
            raise

    ### Transform

    def _transform_data_par(self, data):
        '''

        :param data:
        :return:
        '''

        json = []

        for pro_land in data:
            json.append(self.transform_par_to_proct_land(pro_land))

        return json

    def transform_par_to_proct_land(self, pro_land):
        '''

        :param pro_land:
        :return:
        '''
        json = {
            "orcs": pro_land["orcNumber"],
            "protectedAreaName": pro_land["protectedLandName"],
            "totalArea": pro_land["totalArea"],
            "uplandArea": pro_land["uplandArea"],
            "marineArea": pro_land["marineArea"],
            "marineProtectedArea": pro_land["marineProtectedAreaInd"],
            "type": pro_land["protectedLandTypeDescription"],
            "typeCode": pro_land["protectedLandTypeCode"],
            "class": pro_land["protectedLandClassCode"],
            "status": pro_land["protectedLandStatusCode"],
            "establishedDate": pro_land["establishedDate"],
            "repealedDate": None,
            "url": "",
            "latitude": None,
            "longitude": None,
            "mapZoom": None,
            "sites": self.transform_par_sites(pro_land["orcNumber"], pro_land["sites"]),
            "managementAreas": self.transform_par_mgmtAreas(pro_land["managementAreas"])
        }

        return json

    def transform_par_sites(self, orcsNumber, sites):
        '''

        :param orcsNumber:
        :param sites:
        :return:
        '''
        json = []

        for site in sites:
            result = self.transform_par_site(orcsNumber, site)
            json.append(result)

        return json

    def transform_par_site(self, orcsNumber, site):
        '''

        :param orcsNumber:
        :param site:
        :return:
        '''
        orcsSiteNumber = "{}-{}".format(orcsNumber, site["protectedLandSiteNumber"])

        json = {
            "orcsSiteNumber": orcsSiteNumber,
            "siteNumber": site["protectedLandSiteNumber"],
            "siteName": site["protectedLandSiteName"],
            "status": site["protectedLandSiteStatusCode"],
            "establishedDate": site["protectedLandSiteEstablishedDate"],
            "repealedDate": site["protectedLandSiteCanceledDate"],
            "url": "",
            "latitude": None,
            "longitude": None,
            "mapZoom": None
        }

        return json

    def transform_data_bcgn(self, data):
        '''

        :param data:
        :return:
        '''
        json = []
        park_type_legal_id = self.get_park_type_legal_from_strapi()

        for item in data:
            json.append(self.transform_bcgn_data_to_park_names(item, park_type_legal_id))
        print(f'_transform_data_bcgn : End Dump {json}')
        return json

    def transform_par_mgmtAreas(self, areas):
        '''

        :param areas:
        :return:
        '''
        json = []

        for area in areas:
            result = self.transform_par_mgmtArea(area)
            json.append(result)

        return json

    def transform_par_mgmtArea(self, area):
        '''

        :param area:
        :return:
        '''
        return {
            "managementAreaNumber": int(area["protectedLandManagementAreaNumber"]),
            "managementAreaName": area["protectedLandManagementAreaName"],
            "section": self.transform_par_section(int(area["protectedLandSectionNumber"]), \
                                                  area["protectedLandSectionName"]),
            "region": self.transform_par_region(int(area["protectedLandRegionNumber"]), \
                                                area["protectedLandRegionName"])
        }

    def transform_par_section(self, number, name):
        '''
        Create a dict appropriate for strapi consumption from a section name and number

        :param number: Section Number
        :param name: Section Name
        :return: a dict with name and number indexed appropriately
        '''
        return {
            "sectionNumber": number,
            "sectionName": name
        }

    def transform_par_region(self, number, name):
        '''
        Create a dict appropriate for strapi consumption from a region name and number

        :param number: Region Number
        :param name: Region Name
        :return: a dict with name and number indexed appropriately
        '''
        return {
            "regionNumber": number,
            "regionName": name
        }

    def transform_bcwfs_feature(self, feature):
        '''

        :param feature:
        :return:
        '''

        attribute = feature["attributes"]
        eff_date = str(datetime.fromtimestamp(int(attribute["ACCESS_STATUS_EFFECTIVE_DATE"]) / 1000))
        fire_zone_id = self.get_firezone_from_strapi(attribute["FIRE_ZONE_NAME"])
        fire_centre_id = self.get_firecentre_from_strapi(attribute["FIRE_CENTRE_NAME"])

        json = {
            "type": attribute["TYPE"],
            "prohibitionDescription": attribute["ACCESS_PROHIBITION_DESCRIPTION"],
            "effectiveDate": eff_date,
            "fireCentre": fire_centre_id,
            "fireZone": fire_zone_id,
            "bulletinURL": attribute["BULLETIN_URL"],
            "area": attribute["FEATURE_AREA_SQM"],
            "length": attribute["FEATURE_LENGTH_M"]
        }
        return json

    def transform_bcgn_data_to_park_names(self, data, park_type_legal_id):
        '''
        takes a dict populated with data from BCGN, and performs a set of actions on the data to make
        a dict suitable for adding to the strapi collection

        :param data: the BCGN data to transform to be be suitable for a strapi collections
        :param park_type_legal_id: the parknametype to be update
        :return: the transformed record
        '''

        pro_area = self.get_protected_area_from_strapi(data["orcs"])

        json = {
            "orcs": data["orcs"],
            "parkName": data["feature"]["properties"]["name"],
            "source": "BCGWNS",
            "protectedArea": pro_area["id"]
        }
        if data["feature"]["properties"]["isOfficial"] == 1:
            json["parkNameType"] = park_type_legal_id

        return json

    def _transform_data_bcwfs(self, data):
        '''
        Return a list of features from the provided BC Wildfire Services data

        :param data: BC Wildfire Services ESRI data
        :return: a list of transformed features
        '''

        json = []

        for feature in data['features']:
            json.append(self.transform_bcwfs_feature(feature))

        return json

    ### Create/Update content in Strapi

    def create_site_in_strapi(self, site):
        '''
        Create a site in Strapi
        :param site: a dict containing the infrmation/attribues defined in strapi for a site
        :return: the strapi id of the site
        '''

        api_url = f"{self.strapi_base}/sites?token={self.token}"
        result = None

        try:
            response = requests.post(api_url, json=site, headers=headers)

            if response.status_code == 200:
                result = response.json()
                print(f'Site with orcsSiteNumber: {site["orcsSiteNumber"]} successfully created!')
            else:
                print(f'create site: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('create site:Error invoking webservice')
            raise

    def update_site_in_strapi(self, id, site):
        '''

        :param id:
        :param site:
        :return:
        '''

        api_url = f"{self.strapi_base}/sites/{id}?token={self.token}"
        result = None

        try:
            response = requests.put(api_url, json=site, headers=headers)

            if response.status_code == 200:
                result = response.json()
                print(f'Site with orcsSiteNumber: {site["orcsSiteNumber"]} updated')
            else:
                print(f'update site: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('update site:Error invoking webservice')
            raise

    def create_region_in_strapi(self, region):
        '''
        Create a region in Strapi
        :param region: a dict containing the infrmation/attribues defined in strapi for a region
        :return: the strapi id of the region
        '''

        api_url = f"{self.strapi_base}/sites?token={self.token}"
        result = None

        try:
            response = requests.post(api_url, json=region, headers=headers)

            if response.status_code == 200:
                result = response.json()

                print(f'Record with id: {result["id"]} successfully created!')
            else:
                print(f'create region: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('Error invoking webservice')
            raise

    def create_section_in_strapi(self, section):
        '''
        Create a section in Strapi
        :param section: a dict containing the infrmation/attribues defined in strapi for a section
        :return: the strapi id of the section
        '''

        api_url = f"{self.strapi_base}/sites?token={self.token}"
        result = None

        try:
            response = requests.post(api_url, json=section, headers=headers)

            if response.status_code == 200:
                result = response.json()

                print(f'Record with id: {result["id"]} successfully created!')
            else:
                print(f'create section: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('Error invoking webservice')
            raise

    def create_mgmt_area_in_strapi(self, mArea):
        '''
        Create Management Area in Strapi
        Ensures the corresponding Region/Section exists, creating if need before

        :param mArea: a dict containing the infrmation/attribues defined in strapi for a Management Area
        :return: the strapi id of the Management Area
        '''

        api_url = f"{self.strapi_base}/management-areas?token={self.token}"
        result = None

        try:
            # handle depencies - region, sections
            if 'region' in mArea:
                mArea["region"] = self.get_or_create_region(mArea["region"])

            if 'section' in mArea:
                mArea["section"] = self.get_or_create_section(mArea["section"])

            response = requests.post(api_url, json=mArea, headers=headers)

            if response.status_code == 200:
                result = response.json()

                print(
                    f'Management Area with managementAreaNumber: {mArea["managementAreaNumber"]} successfully created!')
            else:
                print(f'create mgmt: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('Error invoking webservice')
            raise

    def update_mgmt_area_in_strapi(self, id, mArea):
        '''

        :param id: the id in strapi for a particular mamagement area
        :param mArea:
        :return:
        '''

        api_url = f"{self.strapi_base}/management-areas/{id}?token={self.token}"
        result = None

        try:
            del mArea["region"]
            del mArea["section"]

            response = requests.put(api_url, json=mArea, headers=headers)

            if response.status_code == 200:
                result = response.json()
                print(f'Management Area with managementAreaNumber: {mArea["managementAreaNumber"]} updated')
            else:
                print(f'update Management Area: Unplanned status code returned - {response.status_code}')

            return result

        except:
            print('update Management Area:Error invoking webservice')
            raise

    ### Get content from Strapi

    def get_protected_area_from_strapi(self, orcs):
        '''

        :param orcs:
        :return:
        '''

        api_url = f"{self.strapi_base}/protected-areas?orcs={orcs}"

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                result = None
                if len(data) > 0:
                    result = data[0]

                return result
            else:
                print(f'Unable to get protected area with code {response.status_code}')
        except:
            print(f'Error invoking webservice - {api_url}')
            raise

    def get_site_from_strapi(self, orcsSiteNumber):
        '''

        :param orcsSiteNumber:
        :return:
        '''

        api_url = f"{self.strapi_base}/sites?orcsSiteNumber={orcsSiteNumber}"

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data[0]
            else:
                print(f'Unable to get site with code {response.status_code}')
        except:
            print(f'Error invoking webservice - {api_url}')
            raise

    def get_mgmt_area_from_strapi(self, mAreaNumber):
        '''

        :param mAreaNumber:
        :return:
        '''

        api_url = f"{self.strapi_base}/management-areas?managementAreaNumber={mAreaNumber}"

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data[0]
            else:
                print(f'Unable to get mgmt area with code {response.status_code}')
        except:
            print(f'Error invoking webservice - {api_url}')
            raise

    def get_region_from_strapi(self, regionNumber):
        '''

        :param regionNumber:
        :return:
        '''

        api_url = f"{self.strapi_base}/regions?regionNumber={regionNumber}"

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data[0]
            else:
                print(f'Unable to region with code {response.status_code}')
        except:
            print(f'Error invoking webservice - {api_url}')
            raise

    def get_section_from_strapi(self, sectionNumber):
        '''

        :param sectionNumber:
        :return:
        '''

        api_url = f"{self.strapi_base}/sections?sectionNumber={sectionNumber}"

        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data
            else:
                print(f'Unable to get section with code {response.status_code}')
        except:
            print(f'Error invoking webservice - {api_url}')
            raise

    def get_park_names_legal_from_strapi(self, protectedAreaId, parkNameLegalId):
        '''
        query Strapi for a list of legal names of parks for a particular park type in a particular protected are
        If any are found, it returns the first park meeting the criteria

        :param protectedAreaId: the id of a protetced area
        :param parkNameLegalId:  the id of a park's type
        :return: a Strapi Park record
        '''


        api_url = f"{self.strapi_base}/park-names?protectedArea={protectedAreaId}&parkNameType={parkNameLegalId}"
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data[0]
            else:
                print(f'get_park_names_legal_from_strapi: Unable to get park names with code {response.status_code}')
        except:
            print(f'get_park_names_legal_from_strapi: Error invoking webservice - {api_url}')
            raise

    def get_park_type_legal_from_strapi(self):
        '''

        :return:
        '''

        api_url = f"{self.strapi_base}/park-name-types?nameType=Legal"
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return None
                else:
                    return data[0]["id"]
            else:
                print(
                    f'get_park_type_legal_from_strapi: Unable to get park name legal type with code {response.status_code}')
        except:
            print(f'get_park_type_legal_from_strapi: Error invoking webservice - {api_url}')
            raise

    def get_firezone_from_strapi(self, fireZoneName):
        '''

        :param fireZoneName:
        :return:
        '''

        api_url = f"{self.strapi_base}/Fire-Zones?fireZoneName_contains={fireZoneName}"
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return 0
                else:
                    return data[0]["id"]
            else:
                print(f'get_firezone_from_strapi: Unable to get fire zone with code {response.status_code}')
        except:
            print(f'get_firezone_from_strapi: Error invoking webservice - {api_url}')
            raise

    def get_firecentre_from_strapi(self, fireCentreName):
        '''
        retrieve all firecentres from strapi whose names contains the string passed in
        :param fireCentreName:a Fire Centre name, or part thereof
        :return:
        '''

        api_url = f"{self.strapi_base}/Fire-Centres?fireCentreName_contains={fireCentreName}"
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if len(data) == 0:
                    return 0
                else:
                    return data[0]["id"]
            else:
                print(f'get_firezone_from_strapi: Unable to get fire zone with code {response.status_code}')
        except:
            print(f'get_firezone_from_strapi: Error invoking webservice - {api_url}')
            raise

    def delete_fireban_prohibitions_from_strapi(self):
        '''
        Deletes all fireban prohibitions from strapi
        :return: None
        '''

        api_url = f"{self.strapi_base}/Fire-Ban-Prohibitions"
        try:
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                for fireban in data:
                    response = requests.delete(f'{api_url}/{fireban["id"]}?token={self.token}', headers=headers)

                print(f'delete_fireban_prohibitions_from_strapi: Deleted all Fire Ban Prohibitions')
            else:
                print(
                    f'delete_fireban_prohibitions_from_strapi: Unable to get fire zone with code {response.status_code}')
        except:
            print(f'delete_fireban_prohibitions_from_strapi: Error invoking webservice - {api_url}')
            raise

    ### misc
    def clean_data(self):
        '''
        Purpose is Unknown
        :return:
        '''

        pass

    def validate_data(self):
        '''
        Purpose is Unknown
        :return:
        '''

        pass

