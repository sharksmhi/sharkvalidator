# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2021-04-14 13:42

@author: johannes
"""
from pathlib import Path
from sharkvalidator import App
from sharkvalidator.utils import generate_filepaths
from sharkvalidator.validators.validator import ValidatorLog


if __name__ == '__main__':

    path_to_zips = r'..\sharkweb\SHARKdata_datasets'
    app = App()

    dtypes = (
        'Bacterioplankton', 'Chlorophyll', 'Epibenthos',
        'HarbourSeal', 'GreySeal',
        'HarbourPorpoise',
        # 'PhysicalChemical',
        'Profile', 'Phytoplankton',
        'Picoplankton', 'PlanktonBarcoding',
        'PrimaryProduction', 'RingedSeal', 'SealPathology', 'Sedimentation',
        'SLV', 'Zoobenthos', 'Zooplankton',
    )
    semicolon_set = set()
    for dtype in dtypes:
        print(f'Datatype: {dtype}')
        generator = generate_filepaths(path_to_zips, pattern=f'SHARK_{dtype}')
        for zip_id in generator:
            # if not '2020_SVF_DEEP' in zip_id:
            #     continue
            # print(zip_id)
            zip_id = Path(zip_id)
            app.read(
                zip_id,
                reader='sharkzip',
                delivery_name=zip_id.name,
            )

            app.validate(zip_id.name, validator_list=['formats_freetext'],
                         disapproved_only=True)

            df = app.deliveries[zip_id.name]['data']
            if not (df == df.replace({';': ','}, regex=True)).all().all():
                semicolon_set.add(zip_id.name)

            app.deliveries.drop_delivery(name=zip_id.name)

        # app.write(
        #     writer='log',
        #     file_name=f'validation_log_{dtype}.yaml',
        # )
        # app.write(
        #     writer='xlsx',
        #     file_name=f'validation_log_20211119_{dtype}.xlsx',
        # )

        ValidatorLog.update_info(reset_log=True)
    from pprint import pprint

    pprint(semicolon_set)
