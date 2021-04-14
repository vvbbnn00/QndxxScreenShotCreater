# 青年大学习截图生成器
## 注意
未知原因，导致目前国外服务器无法通过HTTPS协议访问青年大学习。
因此，请避免将服务器架设在国外，否则，将会出现502错误。
由于代码编写于1年多前，且许久未维护，可能出现问题，欢迎联系我，**免费帮忙解决**。

## 特色功能
- 支持多种型号的手机截图，且可以自制截图模板
- 拥有缓存功能，访问速度更快
- 仅需1个160+行的python代码和手机模板文件即可完成服务器部署

## 快速上手
本程序基于Python Flask框架编写，在架设服务器之前，请确认您的服务器已安装Python3.x。

若您不会搭建服务器，也没有关系，您可以通过以下方式体验：
- **快速获取最新一期的截图**：访问[该网址](https://smfms.vvbbnn00.cn/)，点击`最新一期的青年大学习`按钮即可。
- **获取往期大学习截图**：访问[该网址](https://smfms.vvbbnn00.cn/smw/qndxx)。

**文明使用，请勿恶意攻击网站服务器。穷学生买不起网站防御，一打就瘫了，谢谢！**

## 帮助文档

### 目录结构
```
root
├─frame	 手机截图模板存放处，具体配置格式见【模板配置】
├─1.jpg 	手机截图模板，必须为jpg格式
	├─1.json   手机截图模板配置文件
└─qndxx   生成的截图缓存
    ├─aHR0cDovL2g1LmN5b2wuY29tL3NwZWNpYWwvZGF4dWV4aS9oamtsZXJ0eXB4L20uaHRtbA==
		├─ori.jpg
		├─1.jpg
		├─...
	├─...
└─pingfangSS.ttf 字体文件，可以更换，但需要修改代码
└─qndxx_gen.py 脚本运行文件
```

### 模板配置
模板为json格式，每一份模板必须有jpg和json两个文件配套，建议用数字命名。
``` json
{
	"id": 配置文件id,
	"start_x": 代表结束图片的位置的左上角x坐标,
	"start_y": 代表结束图片的位置的左上角y坐标,
	"width": 插入截图的宽度,
	"height": 插入截图的高度,
	"color": 标题文字颜色，请将16进制转成10进制,
	"c_x": 代表标题文字位置的左上角x坐标,
	"c_y": 代表标题文字位置的左上角x坐标,
	"f_size": 代表标题文字的字体大小
}
类型要求：均为整型
```
**示例文件：1.json**
``` json
{
	"id": 1,
	"start_x": 0,
	"start_y": 256,
	"width": 1080,
	"height": 1849,
	"color": 1907997,
	"c_x": 150,
	"c_y": 145,
	"f_size": 55
}
```
**示例图片：1.jpg**
![@1.jpg| center | 0x1024](https://od.vvbbnn00.cn/t/9GaXXT)


