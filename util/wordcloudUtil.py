import numpy as np
from PIL import Image
import matplotlib
matplotlib.use('Agg')  # 设置非图形后端，解决线程冲突
from matplotlib import pyplot as plt
from wordcloud import WordCloud


def genWordCloudPic(str, maskImg, outImg):
    """
    生成云图
    :param str: 词云 空格隔开
    :param maskImg: 形状模版图片
    :param outImg: 输出的词云图文件名
    :return:
    """
    img = Image.open('./static/' + maskImg)  # 形状模版图片
    img_arr = np.array(img)  # 转成图片数组对象
    wc = WordCloud(
        width=800,
        height=600,
        background_color='white',
        colormap='Blues',
        font_path='STHUPO.TTF',
        mask=img_arr
    )
    wc.generate_from_text(str)

    # 绘制图片
    plt.imshow(wc)

    # 不显示坐标轴
    plt.axis('off')

    plt.savefig('./static/' + outImg, dpi=500)
