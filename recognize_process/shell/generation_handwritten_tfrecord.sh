#!/bin/bash

echo $#  '生成中文手写数据集'
if [ $# -ne 2 ]
then
    echo "Usage: $0 './label.txt'  'val_rate(0.2)' "
    exit
fi

startTime=`date +%Y%m%d-%H:%M`
startTime_s=`date +%s`

BASE_DIR="./data_cn/"

export PYTHONPATH=../../
echo 'input file line count: '
TOTAL_COUNT=$(awk '{print NR}' $1 | tail -n1)

echo "start --------- generate  image --"
echo 'val_rate: ' $2 ' total count ' ${TOTAL_COUNT}

val_count=`echo "scale=0; ${TOTAL_COUNT} * $2" | bc`
val_count=`echo $val_count | awk -F. '{print $1}'`

train_count=$[TOTAL_COUNT - val_count]

echo 'total  count: '  ${TOTAL_COUNT}
echo 'test   count: '  ${val_count}
echo 'train  count: '  ${train_count}

head -n ${train_count} $1  > ${BASE_DIR}'train.txt'
tail -n ${val_count}   $1  > ${BASE_DIR}'valid.txt'


if [ ! -d ${BASE_DIR}"tfrecords" ]
then
    mkdir ${BASE_DIR}"tfrecords"
fi

#head -n 20 ${BASE_DIR}"valid_labels.txt"  > ${BASE_DIR}'test_labels.txt'
 
echo "start --------- generate  tfrecord "

python ../data_provider/write_tfrecord.py \
--dataset_dir=${BASE_DIR}'images' \
--char_dict_path=${BASE_DIR}'char_map.json' \
--anno_file_path=${BASE_DIR}'train.txt' \
--save_dir=${BASE_DIR}'tfrecords/train/'

python ../data_provider/write_tfrecord.py \
--dataset_dir=${BASE_DIR}'images/' \
--char_dict_path=${BASE_DIR}'char_map.json' \
--anno_file_path=${BASE_DIR}'valid.txt' \
--save_dir=${BASE_DIR}'tfrecords/valid/'


endTime=`date +%Y%m%d-%H:%M`
endTime_s=`date +%s`
echo "$startTime ---> $endTime"