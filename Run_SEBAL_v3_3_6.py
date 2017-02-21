# -*- coding: utf-8 -*-
"""
Created on Tue May 03 13:12:18 2016

@author: tih
"""

import SEBAL_v3_3_6

inputExcel = r"J:\SEBAL_Egypt\InputEXCEL_v3_3_6.xlsx"
# Check if gdalwarp can be found by the command prompt!!! by opening the command prompt and type gdalwarp

for number in range(3,4):
    try:
        SEBAL_v3_3_6.SEBALcode(number,inputExcel)
    except:
        print 'SEBAL did not run line %d fully' % number
        

