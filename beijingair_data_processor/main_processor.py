# -*- coding: utf-8 -*-
# -----
# BeijingAir AQ Data Processor
# main functions
# -----
# Author: Tian Heng
# Affiliation: Atmos. Chem. & Climate Group @ PKU/SUST
# Events:
# 2020-09-02    first version adapted R script

import os
from utils import load_site_info, parse_file_china_sites
from user_conf import SITELIST_FILENAME, INPUT_DIR, OUTPUT_DIR, INPUT_PREFIX

if __name__=='__main__':
    site_list = load_site_info(os.path.join(INPUT_DIR, SITELIST_FILENAME))
    file_list = [x for x in os.listdir(INPUT_DIR) if INPUT_PREFIX in x]
    print(str(len(file_list)) + " files to process")
    for fn in file_list:
        parse_file_china_sites(os.path.join(INPUT_DIR, fn), OUTPUT_DIR, site_list)