import requests
import re
import os
import sys
import json
import pdb
import numpy as np
import time


# B站API详情 https://github.com/Vespa314/bilibili-api/blob/master/api.md

# 视频AV号列表
aid_list = []

# 评论用户及其信息
info_list = []

def create_folders(directory):
    # Create a folder if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_target_txt(input_path):
        # Read in target txt into a string list
        if not input_path.endswith('.txt'):
            assert(1==0), file+" extension is not txt"
        with open(input_path, "r") as txtfile:
            data = txtfile.readlines()
        tmp_string = [string.rstrip('\n') for string in data]
        res = []
        for cur_string in tmp_string:
            split_res = cur_string.split(":")
            res.append([split_res[0], split_res[1]])
        # Turn to numpy array...
        res = np.asarray(res)
        return res

def file_lists_read(file_name):
    # read data from file
    res = []
    with open(file_name, "r") as file:
        for line in file:
            data = eval(line)
            res.append(data)
    return res

def print_output_to_file(file_name, data):
    # write data into files
    with open(file_name, "a") as file:
        for single_data in data:
            file.write(str(single_data) + '\n')

# 获取指定UP的所有视频的AV号 mid:用户编号 size:单次拉取数目 page:页数
def getAllAVList(mid, size, page):
    # The following part of this program is from:
    # 作者：肥肥杨
    # 链接：https://www.zhihu.com/question/56924570/answer/236892766
    # 来源：知乎
    # 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
    # 获取UP主视频列表
    aid_list = []
    for n in range(1,page+1):
        url = "http://space.bilibili.com/ajax/member/getSubmitVideos?mid=" + \
            str(mid) + "&pagesize=" + str(size) + "&page=" + str(n)
        r = requests.get(url)
        text = r.text
        json_text = json.loads(text)
        # 遍历JSON格式信息，获取视频aid
        for item in json_text["data"]["vlist"]:
            aid_list.append(item["aid"])
    if len(aid_list) == 0:
        pdb.set_trace()
    else:
        return aid_list
    # print(aid_list)

def get_all_av_list():
    # Fetch all the vtuber av numbers listed in vtuber.txt
    MID_list_pair = read_target_txt("vtuber.txt")
    MID_list = MID_list_pair[:,1]
    Whole_av_list = []
    for mid in MID_list:
        start_time = time.time()
        new_list = getAllAVList(int(mid), 100, 15)
        if len(new_list) == 0:
            continue
        Whole_av_list.append(new_list)
        print("vtuber with id: {} processed within {}, {} data obtained".format(mid, "--- %s seconds ---" % (time.time() - start_time), len(new_list)))
    print_output_to_file("av_data_list.txt", Whole_av_list)
    return MID_list, Whole_av_list

if __name__ == '__main__':
    print("Begin the av list fetch process...")
    # MID_list, Whole_list = get_all_av_list()
    MID_list_pair = read_target_txt("vtuber.txt")
    MID_list = MID_list_pair[:,1]
    Whole_list = file_lists_read("av_data_list.txt")
    assert len(MID_list) == len(Whole_list)
    for mid, av_list in zip(MID_list, Whole_list):
        mid = int(mid)
        output_trunk = "danmaku_dataset/{}".format(mid)
        create_folders(output_trunk)
        for single_av in av_list:
            start_time = time.time()
            av_number = "av{}".format(single_av)
            output_path = "{}/{}.csv".format(output_trunk, single_av)
            os.system("python danmuku.py -i {} -o {}".format(av_number, output_path))
            print("{} processed within {}, saved to {}".format(av_number, "--- %s seconds ---" % (time.time() - start_time), output_path))

