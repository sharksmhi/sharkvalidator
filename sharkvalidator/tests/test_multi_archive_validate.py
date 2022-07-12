#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-10-27 08:59

@author: johannes
"""
from pathlib import Path
from sharkvalidator import App
from sharkvalidator.utils import generate_filepaths
from sharkvalidator.validators.validator import ValidatorLog


if __name__ == '__main__':

    path_to_zips = r'..sharkweb\SHARKdata_datasets'
    app = App()

    dtypes = (
        # 'Bacterioplankton', 'Chlorophyll', 'Epibenthos',
        # 'HarbourSeal', 'GreySeal',
        # 'HarbourPorpoise',
        'PhysicalChemical',
        # 'Profile', 'Phytoplankton',
        # 'Picoplankton', 'PlanktonBarcoding',
        # 'PrimaryProduction', 'RingedSeal', 'SealPathology', 'Sedimentation',
        # 'SLV', 'Zoobenthos', 'Zooplankton',
    )

    for dtype in dtypes:
        print(f'Datatype: {dtype}')
        generator = generate_filepaths(path_to_zips, pattern=f'SHARK_{dtype}')
        for fid in generator:
            if not '1928_BAS_XXX' in fid:
                continue
            fid = Path(fid)
            app.read(
                fid,
                reader='sharkzip',
                delivery_name=zip_id.name,
            )

            app.validate(fid.name, validator_list=['formats_TIME'], disapproved_only=True)

            app.deliveries.drop_delivery(name=zip_id.name)

        # app.write(
        #     writer='log',
        #     file_name=f'validation_log_{dtype}.yaml',
        # )
        # app.write(
        #     writer='xlsx',
        #     file_name=f'validation_log_20211026_{dtype}.xlsx',
        # )
        #
        # ValidatorLog.update_info(reset_log=True)
