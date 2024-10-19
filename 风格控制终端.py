from muko import *


class 全局配置:
    # 》》风格控制终端》》：
    原文路径 = '原文.txt'
    背景音乐 = './背景音乐/Feder.mp3'
    # 你的视频类型是横屏还是竖屏？   '横屏'  '竖屏'
    视频类型 = '横屏'
    # 角色提示词和主题（写下你给AI的提示）:
    # 类型： 人物 动物（都是拟人状态，就是动物也可能是动物精灵（人形）） 》》其他自定义！自由度高
    类型 = '人物'
    主题 = '阳光,温馨,轻松'
    人物提示词风格 = '以男女和年纪开头，比如：“男, 年轻, 修长身材”'

    # 画图（入门设置）：
    场景 = '文生图'
    #模型 = '通用写实'
    #模型 = 'Q版'
    #模型 = '【2.5D】revAnimated_v11.civitai (1)'
    模型 = '推文古代'
    # 模型 = '推文悬疑'
    # hunhe 出图效果灰淡
    # kl 出图效果明亮
    # 编码器 = 'hunhe'
    编码器 = 'sdxl'
    #编码器 = 'hunhe'
    #编码器 = 'kl'
    #采样器 = 'UniPC'
    采样器 = 'DDIM'
    微调 = ''
    # 微调 = None
    尺寸 = '1024*1024'

    # 朗读：
    音色 = '脉云希'
    朗读音量 = 110
    语速 = 1.1
    音调 = 0.7
    情感 = '温暖亲切'
    # 复制到浏览器打开《高阶音色表》
    # https://doc.weixin.qq.com/sheet/e3_ATUAKwYqAE4rXojO6DqQMOE0mP1hr?scode=AOAAkwfUACgZdM2Rb9
    # 复制到浏览器打开《超高阶音色表》
    # https://doc.weixin.qq.com/sheet/e3_AYwAtAZqAF0xoDCTRmuRdyZgLApu2?scode=AOAAkwfUACgd25qp01

    # 视频尺寸（建议两个一样，一致）
    横屏背景尺寸 = (1440, 1080)
    竖屏背景尺寸 = (1080, 1920)
    # 推荐尺寸 (1920, 1080) (1600, 900) (1366, 768) (1280, 720) (1024, 768) (1080, 810)(960, 720)......
    # 推荐尺寸 (1080, 1920)
    # 竖屏背景尺寸的推荐尺寸：横屏没有
    # 此参数在V1.4版本不建议更改

    # 音量：
    音频音量 = 150
    背景音乐音量 = 4
    音频速率 = 1

    # 字幕：   竖屏推荐 字体大小 35    横屏推荐 字体大小 55
    字幕颜色 = (255, 255, 0)
    描边颜色 = (0, 0, 0)
    描边宽度 = 2.5
    字体大小 = 75
    字体 = 'wujie'
    描边透明度 = 0.9
    字幕透明度 = None
    字幕位置 = ('无', 960)
    背景尺寸比例 = None
    背景颜色 = None
    背景透明度 = None
    字体间距 = None

    特效素材文件夹列表 = 列表(
        '精选',
    )

    输出(f"基本信息：\n《小说推文{视频类型}视频》\n主题：{主题}\n尺寸：{尺寸}\n音色：{音色}\n情感：{情感}")

