#!/bin/bash

echo $#  '下载中文签名数据集'

startTime=`date +%Y%m%d-%H:%M`
startTime_s=`date +%s`

#copy from s3
#TODO: public the data access
aws s3 cp s3://csdc-ocr-ml-dev/chinese-ocr./手写签名.zip  .
#unzip
unzip -P chineseocr 手写签名.zip

#make output dir
BASE_DIR="./data_cn/"

if [ ! -d ${BASE_DIR} ];then
mkdir ${BASE_DIR}
fi

#move all png files into one folder



#generate one single label txt

endTime=`date +%Y%m%d-%H:%M`
endTime_s=`date +%s`
echo "$startTime ---> $endTime"