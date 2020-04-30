#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 20:48:26 2020

@author: hamishgibbs
@updates_by: ulfaslak
"""

import sys, os, json
import pandas as pd
from utils.utils import download_data, move_most_recent_files, get_earliest_date
from utils.mobility import get_file_dates, get_urls

def main(_args):
    '''
    download colocation data
    
    Parameters
    ----------
    _args : listx
        Arg list secret_key, username and pass dir, csv file specifying download countries and ids, outdir.

    Returns
    -------
    None.

    '''
    
    with open(_args[1]) as fp:
        keys = json.load(fp)

    #read target datasets
    data_target = pd.read_csv(_args[2])

    for _, row in data_target.iterrows():
        print("Downloading:", row.type)

        base_url = f'https://www.facebook.com/geoinsights-portal/{row.addr}/?id={row.id}&ds='

        earliest_date = get_earliest_date(row, _args[3])  # <-- added by ulfaslak
        data_dates = get_file_dates(earliest_date)
        urls = get_urls(base_url, data_dates)

        print(f"    {len(urls)} up to files to collect:", end=" ")

        download_data(urls, keys)

        move_most_recent_files(_args[3] + "/" + row.country + "/" + row.type, urls)
    
    print('Success.')

if __name__ == "__main__":
    
    _args = sys.argv

    main(_args)