# 对数据文件进行SHA512校验以及长度校验，并对校验不通过数据进行剔除

import os
import json
import time
import zipfile
import hashlib
import numpy as np


# 加载sigmf-meta文件，读取core:sha512,core:sample_start,core:sample_count,修改data_file值
def load_json(json_path, data_path):
    """

    :param json_path: sigmf-meta文件路径
    :param data_path: bin文件路径
    :return: sha512, sample_start, sample_count
    """

    allSignals = json.load(open(json_path))
    sha512 = allSignals['_metadata']['global']['core:sha512']
    sample_start = allSignals['_metadata']['captures'][0]['core:sample_start']
    sample_count = allSignals['_metadata']['annotations'][0]['core:sample_count']

    allSignals['data_file'] = data_path

    return sha512, sample_start, sample_count


# 读取二进制bin文件
def PullBinarySample(data_path, sample_start):
    """

    :param data_path: bin文件路径
    :param sample_start: 数据偏移位置
    :return: data with flaot32
    """

    if sample_start < 0:
        sample_start = 0

    with open(data_path, "rb") as f:
        # Seek to startSample
        f.seek(sample_start * 4)
        # Read in as floats
        raw = np.fromfile(f, dtype=np.float32)

        return raw


# 数据校验函数
def dataVerify(data_path, sha512, sample_start, sample_count):
    """

    :param data_path: bin文件路径
    :param sha512: 哈希校验码
    :param sample_start: 数据偏移位置
    :param sample_count: 数据长度
    :return: result. Yes代表数据校验通过
    """

    data = PullBinarySample(data_path, sample_start)

    if len(data) != sample_count:  # 长度校验未通过
        print(data_path + '  数据长度错误。')

        result = 'No'

    else:  # 长度校验通过
        if hashlib.sha512(data).hexdigest() != sha512:  # 哈希校验未通过
            print(data_path + '  哈希校验未通过。')

            result = 'No'

        else:
            result = 'Yes'

    return result


# 数据文件根路径
root_dir = 'E:/Github/DATA_NEU/DAY'
if root_dir[-1] != '/':
    root_dir += '/'


if os.path.isfile('result.txt'):
    os.remove('result.txt')

device = os.listdir(root_dir)

start_time = time.time()

for i in range(len(device)):

    device_dir = os.path.join(root_dir, device[i])
    if device_dir[-1] != '/':
        device_dir += '/'

    files = os.listdir(device_dir)

    if len(files) != 3:  # bin文件未解压
        for k in range(len(files)):
            if files[k].split('.')[1] == 'zip':
                zip_path = os.path.join(device_dir, files[k])

        zip_file = zipfile.ZipFile(zip_path)
        zip_file.extractall(device_dir)
        zip_file.close()

        files = os.listdir(device_dir)

    for k in range(len(files)):
        if files[k].split('.')[1] == 'sigmfdata':
            bin_path = os.path.join(device_dir, files[k])  # bin文件路径
        elif files[k].split('.')[1] == 'sigmf-meta':
            sigmf_path = os.path.join(device_dir, files[k])  # sigmf-meta文件路径

    SHA512, start, count = load_json(sigmf_path, bin_path)

    result = dataVerify(bin_path, SHA512, start, count)

    if result == 'Yes':  # 校验不通过
        txt_file = open('result.txt', mode='a+')
        txt_file.write(device[i] + '\n')
        txt_file.close()

end_time = time.time()

print(end_time - start_time)