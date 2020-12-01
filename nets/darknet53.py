# -------------------------------------------------
# @Time    : 2020/6/23 22:08
# @Author  : RunRun
# @File    : test
# @Software: PyCharm
#
# -------------------------------------------------
# 功能
#
# Darknet53网络框架
#
#

from functools import wraps
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from utils.utils import compose


# --------------------------------------------------#
#   单次卷积
# --------------------------------------------------#
@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    darknet_conv_kwargs = {'kernel_regularizer': l2(5e-4)}   # 进行正则化，提升性能
    darknet_conv_kwargs['padding'] = 'valid' if kwargs.get('strides')==(2,2) else 'same'
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)

#---------------------------------------------------#
#   卷积块
#   DarknetConv2D + BatchNormalization + LeakyReLU
#       结合darknet    标准化    激活函数
#---------------------------------------------------#
def DarknetConv2D_BN_Leaky(*args, **kwargs):
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose( 
        DarknetConv2D(*args, **no_bias_kwargs),
        BatchNormalization(),
        LeakyReLU(alpha=0.1))

#---------------------------------------------------#
#   卷积块   调整输入长宽 进行 残差结构  返回输出的x
#   DarknetConv2D + BatchNormalization + LeakyReLU
#---------------------------------------------------#
def resblock_body(x, num_filters, num_blocks):
    x = ZeroPadding2D(((1,0),(1,0)))(x)
    x = DarknetConv2D_BN_Leaky(num_filters, (3,3), strides=(2,2))(x)   # 特殊卷积块 步长2  长宽变为原来的1/2

    for i in range(num_blocks):
        # 进行两次卷积   1X1 通道压缩1/2    3X3 把通道扩张回来
        y = DarknetConv2D_BN_Leaky(num_filters//2, (1,1))(x)
        y = DarknetConv2D_BN_Leaky(num_filters, (3,3))(y)
        x = Add()([x,y])    # 残差结构 add 把 主干和残差 相加  重复num_blocks 次
    return x

#---------------------------------------------------#
#   darknet53 的主体部分
#---------------------------------------------------#
def darknet_body(x):
    # 经过卷积块 416，416,3
    x = DarknetConv2D_BN_Leaky(32, (3,3))(x)
    # 208,208    输入特征层 输出通道数  重复次数
    x = resblock_body(x, 64, 1)
    #104,104,128
    x = resblock_body(x, 128, 2)

    # 52,52,256  到第一个特征层 传到预测值处理网络 8次
    x = resblock_body(x, 256, 8)
    feat1 = x

    # 26,26，512 提取出特征层   8次   26即划分的网格数
    x = resblock_body(x, 512, 8)
    feat2 = x
    # 13,13,1024  提出特征层   4次
    x = resblock_body(x, 1024, 4)
    feat3 = x

    return feat1,feat2,feat3

