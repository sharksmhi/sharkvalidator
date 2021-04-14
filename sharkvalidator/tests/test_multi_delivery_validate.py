# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-04-14 13:42
@author: johannes
"""
import os
from pathlib import Path
from sharkvalidator import App
from sharkvalidator.utils import generate_filepaths


if __name__ == '__main__':

    path_to_zips = r'\\winfs\data\prodkap\sharkweb\SHARKdata_datasets'

    generator = generate_filepaths(path_to_zips, pattern='SHARK_Phytoplankton')

    app = App()

    for i, zip_id in enumerate(generator):
        # print(zip_id)
        zip_id = Path(zip_id)
        app.read(
            zip_id,
            reader='phytop_sharkzip',
            delivery_name=zip_id.name,
        )

        app.validate(zip_id.name, validator_list=['formats'], disapproved_only=True)

        app.deliveries.drop_delivery(name=zip_id.name)

    app.write(writer='log')
