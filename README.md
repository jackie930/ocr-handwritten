# ocr-handwritten

This repo is be used for ocr-handwritten recognition via CRNN

# Data


we have two ways to generate input data
* from open source
* use trdggenerate 

sample input data generated by trdg

![input](./doc/input.png)

sample input data from open source

![input2](./doc/input2.png)

handwritten sample

![input](./doc/image.png)

# Quick start

## build environment

```shell script
conda create -n  ocr-cn python=3.6 pip scipy numpy ##运用conda 创建python环境
source activate ocr-cn
pip install -r requirements.txt -i https://mirrors.163.com/pypi/simple/
```

## prepare data

```shell script
# download handwritten data
cd ./recognize_process/shell
sh download_handwritten_data.sh

#generate tfrecord
sh generation_handwritten_tfrecord.sh ./label.txt 0.2
```

## training 

```shell script
sh train-cn.sh
```

training sreenshot

![train](./doc/train.png)

![loss](./doc/loss.png)

![loss](./doc/train4.png)

### test

```shell script
sh test-cn.sh
```
test result after 30 min training

![test](./doc/train3.png)
![test](./doc/train2.png)

## train on AWS SageMaker

todo