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
    #     r'..validator_test\sharkdata\pp\SHARK_Phytoplankton_2019_SMHI_version_2020-10-27.zip',
    #     reader='phytop_sharkzip',
    #     delivery_name='phyto_zip',
    # )

    # app.read(
    #     r'..\FysKem\NATIONELLA_Data\2022\IBTS\arbetsmapp\dataexporter\2022-04-13 0742-2022-LANDSKOD 77-FARTYGSKOD 10',
    #     reader='phyche_lims',
    #     delivery_name='phyche_delivery',
    # )

    wd = r'..\FysKem\NATIONELLA_Data\2021\BAS_EXT_SYK_SMHI\helår'
    for direc in os.listdir(wd):
        app.read(
            '/'.join((wd, direc)),
            reader='phyche_lims',
            delivery_name=direc,
        )

    # app.read(
    #     'C:/Temp/DV/validator_test/Format_Skärgårdsprover 2020 vpl_SMHI.xlsx',
    #     reader='phytop_xlsx',
    #     delivery_name='svab_phyto',
    # )

    # app.validate('svab_phyto', disapproved_only=True)
    # app.validate('phyche', disapproved_only=True)
    # app.validate('phyche_delivery', disapproved_only=True)
    app.validate(*os.listdir(wd), disapproved_only=True)
    # app.validate('phyto_sw', disapproved_only=True)
    # app.validate('phyto_zip', validator_list=['formats'], disapproved_only=True)

    app.write(writer='xlsx')
