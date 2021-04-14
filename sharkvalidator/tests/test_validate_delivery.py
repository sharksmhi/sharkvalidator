# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-12-16 15:26

@author: johannes

"""
from sharkvalidator import App


if __name__ == '__main__':

    app = App()

    # app.read(
    #     r'C:\Temp\DV\validator_test\sharkweb\phytop_test.txt',
    #     reader='phytop_sharkweb',
    #     delivery_name='phyto_sw',
    # )

    app.read(
        r'C:\Temp\DV\validator_test\sharkdata\pp\SHARK_Phytoplankton_2019_SMHI_version_2020-10-27.zip',
        reader='phytop_sharkzip',
        delivery_name='phyto_zip',
    )

    # app.read(
    #     'C:/Temp/DV/validator_test/Format Physical and chemical Kalmar kust 2020.xlsx',
    #     reader='phyche_xlsx',
    #     delivery_name='phyche_delivery',
    # )

    # app.read(
    #     'C:/Temp/DV/validator_test/2021-04-09 1244-2020-LANDSKOD 77-FARTYGSKOD 10',
    #     reader='phyche_lims',
    #     delivery_name='lims',
    # )

    # app.read(
    #     'C:/Temp/DV/validator_test/PP_DEEP_Phytoplankton_data_2019_2020-05-07.xlsx',
    #     reader='phytop_xlsx',
    #     delivery_name='deep_phyto',
    # )

    # app.validate('lims', disapproved_only=True)
    # app.validate('hal_phyche', disapproved_only=True)
    # app.validate('him', disapproved_only=True)
    # app.validate('phyto_sw', disapproved_only=True)
    app.validate('phyto_zip', validator_list=['formats'], disapproved_only=True)

    app.write(writer='log')
