# -*- coding: utf-8 -*-
# -----
# BeijingAir AQ Data Processor
# useful functions
# -----
# Author: Tian Heng
# Affiliation: Atmos. Chem. & Climate Group @ PKU/SUST
# Events:
# 2020-09-02    first version adapted R script

import os
import pandas as pd
import numpy as np
from user_conf import NON_VALUE
#import datetime as dt

def load_site_info(sitelist_filepath):
    map_table = pd.read_csv('city_id_mapping.csv', encoding='utf8')
    file_ext = os.path.splitext(sitelist_filepath)[-1]
    if file_ext in ['.xls', '.xlsx']:
        sitelist_in = pd.read_excel(sitelist_filepath)
    elif file_ext in ['.csv', '.txt']:
        sitelist_in = pd.read_csv(sitelist_filepath, encoding='utf8')
    else:
        raise Exception("Unknown File Extension")
    out_site_info = sitelist_in.iloc[:, 0:5].copy()
    out_site_info.columns = ['siteid', 'sitename', 'cityname', 'sitelon', 'sitelat']
    # initial CITYID column in output dataframe
    out_site_info['cityid'] = NON_VALUE
    # loop for filling-in known cityid
    for ir, r in out_site_info.iterrows():
        siteid = int(str(r['siteid']).replace('A', ''))
        idx = map_table[map_table["siteid"]==siteid].index.to_list()
        if idx:
            siteidx = idx[0]
            out_site_info.loc[ir, "cityid"] = map_table.loc[siteidx, "cityid"]
        else:
        # make up new sites' cityid using known data
            cityname = str(r["cityname"])
            cityidx = out_site_info[out_site_info["cityname"]==cityname].index.to_list()
            if cityidx:
                out_site_info.loc[ir, "cityid"] = out_site_info.loc[cityidx[0], "cityid"]

    return out_site_info


# parse one input file into multiple output files
def parse_file_china_sites(inputFILEpath, outputDIRpath, site_info_df):
    # settings
    format_list = [' >11.4f', ' >9.4f', ' >9.4f', ' >9.4f', ' >9.4f', ' >9.4f', ' >9.4f', ' >9.4f']
    spc_list = ['PM2.5', 'PM10', 'SO2', 'CO', 'NO2', 'O3']

    file_name = os.path.split(inputFILEpath)[-1]
    file_ext = os.path.splitext(inputFILEpath)[-1]
    if file_ext in ['.csv', '.txt']:
        data_in = pd.read_csv(inputFILEpath, encoding='utf8')
    elif file_ext in ['.xls', '.xlsx']:
        data_in = pd.read_excel(inputFILEpath)
    else:
        raise Exception("Unknown File Extension")
    data_columns = data_in.columns[3:]
    file_datestring = file_name.replace(file_ext, '').split('_')[-1]    # YYYYMMDD
    save_dir = os.path.join(outputDIRpath, file_datestring[0:6])
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    # start time loop
    for ihour in range(24):
        #t1 = dt.datetime.now()
        out_datestring = file_datestring + format(ihour, '0>2d')
        out_name = 'obs.' + out_datestring + '.txt'
        # fetch hourly data
        data_hour = data_in[data_in["hour"] == ihour]
        with open(os.path.join(save_dir, out_name), 'wt', encoding='utf8') as fout:
            for ssite in data_columns:
                if '.' in ssite:
                    # skip repeat site, e.g. 3207A
                    continue
                siteid = int(ssite.replace('A', ''))
                cityid = site_info_df[site_info_df["siteid"] == ssite]["cityid"].to_list()
                if cityid:
                    cityid = int(cityid[0])
                else:
                    cityid = NON_VALUE
                if len(data_hour)==0:
                    value_list = [cityid, siteid] + [NON_VALUE] * len(spc_list)
                else:
                    value_list = [cityid, siteid]
                    for spc in spc_list:
                        spcdata = data_hour[data_hour["type"]==spc][ssite].to_list()
                        if spcdata:
                            spcdata = spcdata[0]
                            if np.isnan(spcdata):
                                spcdata = NON_VALUE
                        else:
                            spcdata = NON_VALUE
                        value_list.append(spcdata)
                outline = "\t".join([format(x, format_list[i]) for i, x in enumerate(value_list)]) + "\n"
                fout.write(outline)
        print(out_name)
        #t2 = dt.datetime.now()
        #print(t2-t1)


if __name__=='__main__':
    pass