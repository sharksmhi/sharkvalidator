# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 15:26

@author: johannes
"""
import os
from sharkvalidator import App


if __name__ == '__main__':

    app = App()

    # app.read(
    #     r'C:\Temp\DV\validator_test\sharkweb\phytop_test.txt',
    #     reader='phytop_sharkweb',
    #     delivery_name='phyto_sw',
    # )

    # app.read(
    #     r'..\SHARK_Phytoplankton_2019_SMHI_version_2020-10-27.zip',
    #     reader='phytop_sharkzip',
    #     delivery_name='phyto_zip',
    # )

    app.read(
        r'..\9-Sep\data_exporter\2022-09-28 1409-2022-LANDSKOD 77-FARTYGSKOD 10',
        reader='phyche_lims',
        delivery_name='phyche_delivery',
    )

    # wd = r'..2022\BAS_EXT_SYK_SMHI\7-Jul\data_exporter'
    # for direc in os.listdir(wd):
    #     app.read(
    #         '/'.join((wd, direc)),
    #         reader='phyche_lims',
    #         delivery_name=direc,
    #     )

    # app.read(
    #     'C:/Temp/DV/validator_test/Format_Skärgårdsprover 2020 vpl_SMHI.xlsx',
    #     reader='phytop_xlsx',
    #     delivery_name='svab_phyto',
    # )

    # app.validate('svab_phyto', disapproved_only=True)
    # app.validate('phyche', disapproved_only=True)
    app.validate('phyche_delivery', disapproved_only=True)
    # app.validate(*os.listdir(wd), disapproved_only=True)
    # app.validate('phyto_sw', disapproved_only=True)
    # app.validate('phyto_zip',
    #              validator_list=['formats'],
    #              disapproved_only=True)

    app.write(writer='xlsx')
