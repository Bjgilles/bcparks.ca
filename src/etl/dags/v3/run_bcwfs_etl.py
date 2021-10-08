#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(0,0,0,0,0),
    'email': ['Robert.Fiddler@gov.bc.ca'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}
'''
ETL_PROC_NAME = "bcparks_bcwfs_etl"

import utils

etl = utils.Parks_ETL()
attempts = 0
done = False
e = None
while attempts < 2 and not done:
    try:
        bcwfs_data = etl._get_data_from_bcwfs()
        bcwfs_trans = etl._transform_data_bcwfs(bcwfs_data)
        etl._dump_bcwfs_data(bcwfs_trans)

    except Exception as e:
        attempts += 1

if e is not None:
    print("Error loading Parks data")
    raise e
