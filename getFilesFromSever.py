#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Project   :getDownloadAddress
# @FileName  :getFilesFromSever.py
# @Time      :2021/3/23 9:54
# @IDE       :PyCharm
# @Author    :ZhangTiantian

import pandas as pd
import os
import requests
from clint.textui import progress
import progressbar
import time
# -------------------------------------------------------------------
def analysisFilesURL(csv_path,save_folder):
    df = pd.read_excel(csv_path)
    height, width = df.shape
    url_list = df.values.copy()
    data = df.values
    for row in range(height):
        if data[row][2] == "Zip File":
            temp = data[row][0]
            FileName = temp[0:6]
            FileType = ".bin"
        else:
            temp = data[row][0]
            FileName = temp[0:6]
            FileType = ".sigmf-meta"
        url_list[row, 0] = FileName+FileType
        # url_list[row, 1] = FileType
        url_list[row, 1] = data[row][1]
        url_list[row, 2] = save_folder+"\\"+FileName
    return url_list
def initialFileDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return 0
def downloadFilesAndRenameIt(url_list):
    row,column = url_list.shape
    for index in range(row):
        file_path = url_list[index, 2]
        initialFileDirectory(file_path)
        print(url_list[index, 0]+"  Begaining!!")
        widgets = ['下载: ', progressbar.Percentage(),  # 进度条标题
            ' ', progressbar.Bar(marker='>', left='[', right=']', fill=' '),  # 进度条填充、边缘字符
            ' ', progressbar.Timer(),  # 已用的时间
            ' ', progressbar.ETA(),  # 剩余时间
            ' ', progressbar.FileTransferSpeed(),  # 下载速度
        ]
        res = requests.get(url_list[index, 1], stream=True)
        total_length = int(res.headers.get('content-length'))

        bar = progressbar.ProgressBar(widgets=widgets, max_value=total_length)  # 实例化对象

        with open(file_path+"\\"+url_list[index, 0], "wb") as file:
            loaded = 0
            bar.start()
            for chunk in res.iter_content(chunk_size=4096):
                loaded += len(chunk)
                bar.update(loaded)
                if chunk:
                    file.write(chunk)
        bar.finish()
        time.sleep(1)
        print("File download success!!!")
    return 0


if __name__ == '__main__':
    csv_path = r'C:\Users\ZhangTiantian\Desktop\filedownloadtest\Day1_Equalized.xlsx'  # 解析文件路径
    save_folder = r'C:\Users\ZhangTiantian\Desktop\filedownloadtest\Workspace'
    url_list = analysisFilesURL(csv_path,save_folder)
    downloadFilesAndRenameIt(url_list)  # 下载对应的文件
    print("Over!")










