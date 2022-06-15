# EasyBill <!-- omit in toc -->
**Table of Contents**
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Config](#config)

### Background
经常需要给要报销的文件如pdf和图片文件进行有固定格式的命名如 日期-名字-金额.pdf，每次又要一个个点开查看及其麻烦。这个脚本实现了从文件提取金额和日期的数据，其中图片识别是采用 [PearOCR](https://pearocr.com/) 网站的识别功能，识别能力还是准确的，但是它并没有开放API,所以目前是利用selenium来套壳使用。该脚本目前支持滴滴发票和滴滴行程单，饿了么和美团图片。

### Install
|环境|
|--|
|WIN 10|
|python 3.10|
|chrome|

创建一个虚拟环境(建议)  
`python -m venv ./env`  
激活虚拟环境  
`.\env\Scripts\activate`  
`pip install -r .\requirements.txt`  

或者直接安装依赖  
`pip install -r .\requirements.txt`  

### Usage
`cd src`  
`py main.py`  

### Config

|参数名|描述|参数类型|
|----|----|-----|
|`source`|待处理的文件夹路径|string|
|`userName`|用户名|string|
|`outPath`|输出路径|string|
|`debug`|是否启用debug模式，true开启后在进行图像识别时会显示浏览器|boolean|
|`orderDate`|文件中识别出的订单日期|string|
|`money`|文件中识别出的订单金额|string|
|`fileName`|源文件名|string|
|`target`|目标任务|array|
|`target.name`|任务名|string|
|`target.disable`|是否开启该任务|boolean|
|`target.type`|任务类型 pdf,imgae|string|
|`target.outPath`|任务输出路径|string|
|`target.outFileName`|任务输出文件名格式|string|
|`target.outExcel`|任务输出outExcel的字段|array|
