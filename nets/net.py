# -------------------------------------------------
# @Time    : 2020/7/2 0:39
# @Author  : RunRun
# @File    : net
# @Software: PyCharm
#
# -------------------------------------------------
# 功能
#
#  查看整个网络的架构
#
#
# 结果
#
#
#
#
#
from nets.yolo3 import yolo_body
from keras.layers import  Input

Inputs = Input([416,416,3])
model = yolo_body(Inputs,3,10)
model.summary()