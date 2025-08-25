### 一、说明

工作场景需要批量给pdf添加水印，但网上找了一圈都没找到免费的，都是要会员的，正好这两天在玩AiPy Pro，就想着让AI写个工具

<img src="file:///C:/Users/zhang/Pictures/marktext/2025-08-25-14-41-44-image.png" title="" alt="" width="556">

### 二、文件目录

最终文件组成很简单，就一个py文件。但在用AiPy Pro制作过程中产生领取了其他临时文件，包括AI自我排错、自我编译打包的临时文件

<img src="file:///C:/Users/zhang/Pictures/marktext/2025-08-25-14-43-15-image.png" title="" alt="" width="402">



### 三、自己编译

如果不想用release编译好的，就自己用pyinstaller编译exe

1. **创建虚拟环境**：
   
   ```
   python -m venv watermark_env
   ```

2. **激活虚拟环境**：
   
   ```
   watermark_env\Scripts\activate
   ```

3. **安装所有依赖**：
   
   ```
   pip install pyinstaller PyPDF2 reportlab Pillow
   ```

4. **执行打包**：
   
   ```
   pyinstaller --onefile --windowed --name "PDF水印工具" pdf_watermark_batch.py
   ```

编译好的在当前dist目录里

![](C:\Users\zhang\Pictures\marktext\2025-08-25-14-37-59-image.png)

### 四、关于AiPy Pro和trustoken

AiPy Pro是知道创宇旗下的类似于manus的AI+自动化任务辅助工具，官方网址 [爱派（AiPy），本地Manus，你的工作牛马！](https://www.aipyaipy.com/)

调用的是trustoken[Trustoken - AI大模型Token管理和分发平台](https://www.trustoken.cn/)我的trustoken邀请码：**5kvk**。每个用户注册了默认都有14元额度，用完可以免费领取

![](C:\Users\zhang\Pictures\marktext\2025-08-25-14-46-13-image.png)

感兴趣的可以自己去官网看。我分享下让工具干活的几个截图

![](C:\Users\zhang\Pictures\marktext\2025-08-25-14-40-35-image.png)

![](C:\Users\zhang\Pictures\marktext\2025-08-25-14-40-54-image.png)

![](C:\Users\zhang\Pictures\marktext\2025-08-25-14-41-16-image.png)


