# -*- coding: utf-8 -*-
# @Time    : 9/16/20 9:15 PM
# @Author  : Jackie
# @File    : sub_move.py
# @Software: PyCharm

import os
import json
import errno

def generate_char_map(lines, output_dir):
    """
    :param lines:
    :param output_dir:
    :return:
    """
    char_map_json_file = os.path.join(output_dir, 'char_map.json')
    char_set = set(''.join(lines))

    single_char_map = {}
    index = 0
    for char in char_set:
        single_char_map[char] = index
        index += 1

    json_string = json.dumps(single_char_map, ensure_ascii=False, indent=1)
    with open(char_map_json_file, 'w', encoding='utf-8') as f:
        f.write(json_string)
    print('【输出】生成 Char map 文件  输出路径{}, 文件行数 {}.'.format(char_map_json_file, len(single_char_map)))


    char_map = {}
    ord_map = {}
    index = 0
    for char in char_set:
        ord_map['{}_index'.format(index)] = str(ord(char))
        ord_map['{}_ord'.format(ord(char))] = str(index)

        char_map['{}_ord'.format(ord(char))] = char
        index += 1

    char_map_json_file = os.path.join(output_dir, 'char_dict.json')
    ord_map_json_file = os.path.join(output_dir, 'ord_map.json')

    json_string = json.dumps(char_map, ensure_ascii=False, indent=1)
    with open(char_map_json_file, 'w', encoding='utf-8') as f:
        f.write(json_string)

    json_string = json.dumps(ord_map, ensure_ascii=False, indent=1)
    with open(ord_map_json_file, 'w', encoding='utf-8') as f:
        f.write(json_string)


    print('【输出】生成 Char dict 文件  输出路径{}, 文件行数 {}.'.format(char_map_json_file, len(char_map)))
    print('【输出】生成 Ord  map  文件  输出路径{}, 文件行数 {}.'.format(ord_map_json_file, len(ord_map)))


def gci(ori_path):
    #get full filename list
    res = []
    for fpathe,dirs,fs in os.walk(orig_path):
        for f in fs:
            res.append(os.path.join(fpathe,f))

    print ("<<<<<",res)
    #split to label list and image list
    label_ls = [i for i in res if os.path.splitext(i)[1]=='.txt']
    img_ls = [i for i in res if os.path.splitext(i)[1]=='.png']
    print ("label list<<<<<",label_ls)
    print ("image list<<<<<",img_ls)
    return label_ls, img_ls

def generate_single_lable(label_ls,output_dir):
    'move all labels to one single file'
    res = []
    line_ls = []
    for i in label_ls:
        with open(i,'r',encoding='utf8') as fin:
            for line in fin.readlines():
                line = line.strip('\n')
                line_ls.append(line)
        res.append(i.split('/')[-1].replace('.txt','.png')+' '+line)

    generate_char_map(line_ls,output_dir)
    print ("<<<< generate char map success")

    with open("label.txt","w") as f:
        for i in res:
            f.writelines(i+'\n')

    print ("<<<< Convert label txt success")


##TODO: move all pngs
def move_all_pngs(img_ls,output_dir):
    return None

def main(ori_path,output_dir):
    # Create the directory if it does not exist.
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    img_dir = os.path.join(output_dir,'images')

    try:
        os.makedirs(img_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    label_ls, img_ls =gci(ori_path)
    generate_single_lable(label_ls,output_dir)

if __name__ == "__main__":
    orig_path = '../test'
    output_dir='./'
    main(orig_path, output_dir)
