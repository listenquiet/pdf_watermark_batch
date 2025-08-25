### 一、说明

工作场景需要批量给pdf添加水印，但网上找了一圈都没找到免费的，都是要会员的，正好这两天在玩AiPy Pro，就想着让AI写个工具，工具截图如下

<img width="877" height="852" alt="image" src="https://github.com/user-attachments/assets/53f09493-1226-41f7-a07a-8ce389418b12" />


### 二、文件目录

最终文件组成很简单，就一个py文件。但在用AiPy Pro制作过程中产生领取了其他临时文件，包括AI自我排错、自我编译打包的临时文件

<img width="520" height="899" alt="image" src="https://github.com/user-attachments/assets/fb531c25-bb56-4c19-a8d9-e889315ebe7a" />


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

<img width="773" height="114" alt="image" src="https://github.com/user-attachments/assets/43895a6d-853c-46fe-86e7-493069fd4d6e" />


### 四、感谢AiPy Pro和trustoken

AiPy Pro是知道创宇旗下的类似于manus的AI+自动化任务辅助工具，官方网址 [爱派（AiPy），本地Manus，你的工作牛马！](https://www.aipyaipy.com/)

调用的是trustoken[Trustoken - AI大模型Token管理和分发平台](https://www.trustoken.cn/)每个用户注册了默认都有14元额度，用完可以免费领取,我的trustoken邀请码：**5kvk** 如果觉得工具有用可以填写我的邀请码支持下。

<img width="1074" height="781" alt="image" src="https://github.com/user-attachments/assets/57712f08-e5a6-47df-b078-cf32816d6964" />


感兴趣的可以自己去官网看。我分享下让工具干活的几个截图

<img width="1605" height="1110" alt="image" src="https://github.com/user-attachments/assets/6353070b-99fa-41fa-a9c0-d433a66c54fb" />

<img width="1119" height="887" alt="image" src="https://github.com/user-attachments/assets/2ff63937-752a-4257-8f2e-9b84219694a8" />

<img width="1075" height="961" alt="image" src="https://github.com/user-attachments/assets/7bb33aab-9e21-426c-b6b5-45b5691b250c" />


