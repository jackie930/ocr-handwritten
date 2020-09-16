import argparse
import os
import errno
import sys
import random
import json
import time


def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(
        description="生成用户字符串识别的切分字符串"
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        nargs="?",
        help="The output directory",
        default="output/"
    )
    parser.add_argument(
        "-i",
        "--input_file",
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

def main():
    time_start = time.time()
    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    try:
        os.makedirs(args.output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    assert os.path.exists(args.input_file), \
        "Input file[{}] is not exists.".format(args.input_file)


    print('Input file: {}'.format(args.input_file))

    print('Output dir: {} '.format(args.output_dir))

    with open(args.input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    generate_char_map(lines, args.output_dir)

    time_elapsed = time.time() - time_start
    print('The code run {:.0f}m {:.0f}s'.format(time_elapsed // 60, time_elapsed % 60))


if __name__ == "__main__":
    main()




