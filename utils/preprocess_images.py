# -*- coding: utf-8 -*-
# @Time    : 9/16/20 9:15 PM
# @Author  : Jackie
# @File    : preprocess_images.py
# @Software: PyCharm

import os
import json
import errno
import shutil
import argparse

def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(
        description="生成charmap，移动图片目录"
    )
    parser.add_argument(
        "-i",
        "--orig_path",
        type=str,
        nargs="?",
        help="The input directory containing source images and txt",
        default="output/",
        required=True
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default="",
        required=True
    )
    parser.add_argument(
        "-oi",
        "--output_images_dir",
        type=str,
        nargs="?",
        help="When set, this argument uses a specified text file as source for the text",
        default="",
        required=True
    )

    return parser.parse_args()

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
    for fpathe,dirs,fs in os.walk(ori_path):
        for f in fs:
            res.append(os.path.join(fpathe,f))

    #print ("<<<<<",res)
    #split to label list and image list
    label_ls = [i for i in res if os.path.splitext(i)[1]=='.txt']
    img_ls = [i for i in res if os.path.splitext(i)[1]=='.jpg']
    print ("length of label list<<<<<",len(label_ls))
    print ("length of image list<<<<<",len(img_ls))
    return label_ls, img_ls

def generate_single_lable(label_ls,output_dir):
    'move all labels to one single file'
    res = []
    line_ls = []
    for i in label_ls:
        try:
            with open(i,'r',encoding='utf8') as fin:
                for line in fin.readlines():
                    line = line.strip('\n')
                    line_ls.append(line)
            res.append(i.split('/')[-1].replace('.txt','.jpg')+' '+line)
        except:
            continue

    generate_char_map(line_ls,output_dir)
    print ("<<<< generate char map success")

    with open("label.txt","w") as f:
        for i in res:
            f.writelines(i+'\n')

    print ("<<<< Convert label txt success")

def move_all_pngs(ori_path,output_images_dir):
    'move all pngs under one output directory'
    # root 所指的是当前正在遍历的这个文件夹的本身的地址
    # dirs 是一个 list，内容是该文件夹中所有的目录的名字(不包括子目录)
    # files 同样是 list, 内容是该文件夹中所有的文件(不包括子目录)
    if not os.path.exists(output_images_dir):
        os.makedirs(output_images_dir)

    if os.path.exists(ori_path):
        for root,dirs,files in os.walk(ori_path):
            for file in files:
                #TODO:add support for all image types
                if os.path.splitext(file)[1]=='.jpg':
                    src_file = os.path.join(root, file)
                    shutil.copy(src_file, output_images_dir)
                    print(src_file)
    print('<<<< Move images Done!')

def main():
    # Create the directory if it does not exist.
    args = parse_arguments()
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    img_dir = os.path.join(args.output_dir,'images')

    try:
        os.makedirs(img_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    label_ls, img_ls =gci(ori_path=args.orig_path)
    generate_single_lable(label_ls,args.output_dir)
    move_all_pngs(args.orig_path,args.output_images_dir)

if __name__ == "__main__":
    main()
