#!/bin/bash

echo $#  '根据训练数据生成中文数据集'
#if [ $# -ne 2 ]
#then
 #   echo "Usage: $0 '../../sample_data/test.txt'  'val_rate(0.2)' "
  #  exit
#fi

startTime=`date +%Y%m%d-%H:%M`
startTime_s=`date +%s`

SAVE_DIR="./data_cn/"

if [ ! -d ${SAVE_DIR} ];then
mkdir ${SAVE_DIR}
fi

export PYTHONPATH=../../


if [ ! -d ${SAVE_DIR}"tfrecords" ]
then
    mkdir ${SAVE_DIR}"tfrecords"
fi


echo "start --------- generate  tfrecord "

python ../data_provider/write_tfrecord.py \
--dataset_dir='../../sample_data/images' \
--char_dict_path=${SAVE_DIR}'char_map.json' \
--anno_file_path='../../sample_data/label.txt' \
--save_dir=${SAVE_DIR}'tfrecords/'


endTime=`date +%Y%m%d-%H:%M`
endTime_s=`date +%s`
echo "$startTime ---> $endTime"