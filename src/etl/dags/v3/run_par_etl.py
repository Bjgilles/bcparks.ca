

import utils

etl = utils.Parks_ETL()
attempts = 0
done = False
e = None
while attempts < 2 and not done:
    try:
        par_data = etl._get_data_from_par()
        par_trans = etl._transform_data_par(par_data)
        etl._dump_par_data(par_trans)
        bcgn_data = etl._get_data_from_bcgn(par_trans)
        bcgn_trans = etl._transform_data_bcgn(bcgn_data)
        etl._dump_bcgn_data(bcgn_trans)
        done = True
    except Exception as e:
        attempts += 1

if e is not None:
    print("Error loading Parks data")
    raise e
