# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-04-14 13:42
@author: johannes
"""
from pathlib import Path
from sharkvalidator import App
from sharkvalidator.utils import generate_filepaths
from sharkvalidator.validators.validator import ValidatorLog

"""

"""


if __name__ == '__main__':

    path_to_zips = 'PATH_TO_zipfiles'

    app = App()

    dtypes = (
        # 'Bacterioplankton', 'Chlorophyll', 'Epibenthos',
        'HarbourSeal', 'GreySeal', 'HarbourPorpoise',
        # 'PhysicalChemical', 'Profile', 'Phytoplankton',
        'Picoplankton', 'PlanktonBarcoding',
        'PrimaryProduction', 'RingedSeal', 'SealPathology', 'Sedimentation',
        'SLV', 'Zoobenthos', 'Zooplankton',
    )

    for dtype in dtypes:
        print(f'Datatype: {dtype}')
        generator = generate_filepaths(path_to_zips, pattern=f'SHARK_{dtype}')
        for zip_id in generator:
            # print(zip_id)
            zip_id = Path(zip_id)
            app.read(
                zip_id,
                reader='sharkzip',
                delivery_name=zip_id.name,
            )

            app.validate(zip_id.name, validator_list=['formats'], disapproved_only=True)

            app.deliveries.drop_delivery(name=zip_id.name)

        app.write(
            writer='log',
            file_name=f'validation_log_{dtype}.yaml',
        )

        ValidatorLog.update_info(reset_log=True)
