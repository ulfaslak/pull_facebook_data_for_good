#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 16:41:48 2020

@author: hamishgibbs
"""

import os
import glob
import shutil
from selenium import webdriver
import time
import operator
from datetime import datetime
from datetime import timedelta


def try_mkdir_silent(path):
    '''
    Make the target directory or do nothing if it already exists.
    
    Parameters
    ----------
    path : str
        directory to be made.

    Returns
    -------
    None.

    '''
    
    try:
        os.mkdir(path)
    except:
        pass
    
def get_home_dir():
    '''
    Expand user home directory.

    Returns
    -------
    str.

    '''
    
    return(os.path.expanduser("~"))


def download_data(urls: list, keys: list):
    '''
    navigate the facebook login page and access each url

    Parameters
    ----------
    urls : list
        dataset urls.
    keys : list
        login keys username, password.

    Returns
    -------
    None.

    '''
    
    driver = webdriver.Chrome(executable_path='/Applications/chromedriver')
    
    driver.get(urls[0])
    
    driver.find_element_by_xpath('//*[@id="email"]').send_keys(keys[0])
    
    driver.find_element_by_xpath('//*[@id="pass"]').send_keys(keys[1])
    
    driver.find_element_by_xpath('//*[@id="loginbutton"]').click()
    time.sleep(1)
    
    for i, url in enumerate(urls[1:]):
        driver.get(url)
        print(i, end=" ")
        time.sleep(1)

    print("\n")
        
    driver.quit()

def rename_and_move(old_fn: str, old_dir: str, new_fn: str, new_dir: str):
    '''
    rename files and move them to a new directory

    Parameters
    ----------
    old_fn : str
        old filename.
    old_dir : str
        old directory.
    new_fn : str
        new filemane.
    new_dir : str
        new directory.

    Returns
    -------
    None.

    '''
    
    os.rename(old_dir + '/' + old_fn, old_dir + '/' + new_fn) 

    shutil.move(old_dir + '/' + new_fn, new_dir + '/' + new_fn)
    
def get_new_file_name(file: str):
    '''
    parse default filename to reformat as COUNTRY_DATE.csv

    Parameters
    ----------
    file : str
        filename.

    Returns
    -------
    new filename.

    '''
        
    country = file.split('/')[-1].split(" ")[0]
    
    date = file.split('/')[-1].split("_")[-1].split(".")[0].replace('-', '_').replace(' ', '_')
    
    return(country + '_' + date + '.csv')
    
def move_most_recent_files(outdir: str, urls: list):
    '''
    get the most recent files form the download directory, rename them, and put them in the destination directory

    Parameters
    ----------
    outdir : str
        output directory.
    urls : list
        download urls.

    Returns
    -------
    None.

    '''

    try_mkdir_silent(outdir)

    csv_files = glob.glob(get_home_dir() + '/Downloads/*.csv')
    csv_files = {}

    for f in glob.glob(get_home_dir() + '/Downloads/*.csv'):
        csv_files[f] = os.path.getctime(f)

    sorted_files = [f[0] for f in sorted(csv_files.items(), key=operator.itemgetter(1), reverse=True)[:len(urls)]]
    
    new_fns = [get_new_file_name(file) for file in sorted_files]
    
    for i, sorted_file in enumerate(sorted_files):
        
        rename_and_move(sorted_file.split('/')[-1], get_home_dir() + '/Downloads', new_fns[i], outdir)

def get_earliest_date(row, outdir):
    """Get the earliest date, either the one specified in the input or infered from the most recent downloaded file.

    Added by Ulf Aslak
    """
    year = row.start_date[:4]
    month = row.start_date[5:7]
    day = row.start_date[8:10]

    earliest_date = datetime(int(year), int(month), int(day), 0)

    try:
        downloaded_files = os.listdir(outdir + "/" + row.country + "/" + row.type)
        downloaded_files = [f for f in downloaded_files if f.endswith(".csv")]
    except FileNotFoundError:
        downloaded_files = []

    if len(downloaded_files) > 0:
        newest_file = sorted(downloaded_files)[-1]
        newest_date = datetime(
            int(newest_file[-19:-15]),
            int(newest_file[-14:-12]),
            int(newest_file[-11:-9]),
            int(newest_file[-8:-6])
        ) + timedelta(hours=8)
        earliest_date = max(earliest_date, newest_date)

    return earliest_date