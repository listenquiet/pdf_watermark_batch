import tkinter as tk
from tkinter import filedialog, colorchooser, ttk, messagebox
import os
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import platform
import threading
from queue import Queue

# 注册中文字体
def setup_chinese_font():
    """设置中文字体支持"""
    system = platform.system().lower()
    
    # 常见中文字体路径
    font_paths = [
        # Windows系统黑体
        "C:/Windows/Fonts/simhei.ttf",
        # 微软雅黑
        "C:/Windows/Fonts/msyh.ttf",
        # 备用路径
        "./simhei.ttf",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                # 注册黑体字体
                pdfmetrics.registerFont(TTFont('SimHei', font_path))
                print(f"✅ 成功加载中文字体: {font_path}")
                return True
            except Exception as e:
                print(f"❌ 加载字体失败 {font_path}: {e}")
                continue
    
    print("⚠️ 未找到可用的中文字体，中文可能显示异常")
    return False

class PDFWatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ PDF批量水印工具 ✨")
        self.root.geometry("700x650")  # 增加窗口高度以容纳新控件
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        # 设置中文字体
        self.chinese_font_available = setup_chinese_font()
        
        # 变量初始化
        self.input_pdf_paths = []  # 改为列表，支持多个文件
        self.output_dir = tk.StringVar()
        self.watermark_text = tk.StringVar(value="机密文件")
        self.font_size = tk.IntVar(value=36)
        self.rotation = tk.IntVar(value=45)
        self.opacity = tk.DoubleVar(value=0.3)
        self.color_code = tk.StringVar(value="#808080")
        self.density = tk.IntVar(value=5)
        
        # 进度相关
        self.progress_var = tk.DoubleVar()
        self.progress_queue = Queue()
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # ==== 文件选择区域 ====
        file_frame = ttk.LabelFrame(main_frame, text="📂 文件选择", padding="10")
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 输入文件选择（支持多文件）
        ttk.Label(file_frame, text="输入PDF文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_files_label = ttk.Label(file_frame, text="未选择文件", foreground="gray")
        self.input_files_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(file_frame, text="选择文件...", command=self.browse_input_files).grid(row=0, column=2, padx=5, pady=5)
        
        # 输出目录选择
        ttk.Label(file_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.output_dir, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        # ==== 水印设置区域 ====
        watermark_frame = ttk.LabelFrame(main_frame, text="🔧 水印设置", padding="10")
        watermark_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 水印文本
        ttk.Label(watermark_frame, text="水印文本:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(watermark_frame, textvariable=self.watermark_text, width=30).grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        
        # 字体大小
        ttk.Label(watermark_frame, text="字体大小:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Scale(watermark_frame, from_=8, to=70, variable=self.font_size, orient=tk.HORIZONTAL, length=200,
                  command=lambda v: self.update_label(self.font_size_label, int(float(v)))).grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        self.font_size_label = ttk.Label(watermark_frame, text=str(self.font_size.get()))
        self.font_size_label.grid(row=1, column=2, sticky=tk.W, padx=5)
        
        # 旋转角度
        ttk.Label(watermark_frame, text="旋转角度:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Scale(watermark_frame, from_=0, to=360, variable=self.rotation, orient=tk.HORIZONTAL, length=200,
                  command=lambda v: self.update_label(self.rotation_label, int(float(v)))).grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        self.rotation_label = ttk.Label(watermark_frame, text=str(self.rotation.get()))
        self.rotation_label.grid(row=2, column=2, sticky=tk.W, padx=5)
        
        # 透明度
        ttk.Label(watermark_frame, text="透明度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Scale(watermark_frame, from_=0.1, to=1.0, variable=self.opacity, orient=tk.HORIZONTAL, length=200,
                  command=lambda v: self.update_label(self.opacity_label, round(float(v), 1))).grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        self.opacity_label = ttk.Label(watermark_frame, text=str(self.opacity.get()))
        self.opacity_label.grid(row=3, column=2, sticky=tk.W, padx=5)
        
        # 水印密度
        ttk.Label(watermark_frame, text="水印密度:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Scale(watermark_frame, from_=1, to=10, variable=self.density, orient=tk.HORIZONTAL, length=200,
                  command=lambda v: self.update_label(self.density_label, int(float(v)))).grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        self.density_label = ttk.Label(watermark_frame, text=str(self.density.get()))
        self.density_label.grid(row=4, column=2, sticky=tk.W, padx=5)
        
        # 颜色选择
        ttk.Label(watermark_frame, text="字体颜色:").grid(row=5, column=0, sticky=tk.W, pady=5)
        color_frame = ttk.Frame(watermark_frame, width=30, height=30)
        color_frame.grid(row=5, column=1, padx=5, pady=5, sticky=tk.W)
        self.color_canvas = tk.Canvas(color_frame, width=30, height=30, bg=self.color_code.get())
        self.color_canvas.pack()
        ttk.Button(watermark_frame, text="选择颜色", command=self.choose_color).grid(row=5, column=2, sticky=tk.W, padx=5)
        
        # ==== 进度显示区域 ====
        progress_frame = ttk.LabelFrame(main_frame, text="📊 处理进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=600)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="就绪，请选择PDF文件并设置水印参数")
        self.status_label.pack(fill=tk.X, pady=5)
        
        # ==== 操作按钮 ====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.process_button = ttk.Button(button_frame, text="🚀 批量添加水印", command=self.start_batch_processing)
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.quit_button = ttk.Button(button_frame, text="退出", command=root.quit)
        self.quit_button.pack(side=tk.RIGHT, padx=5)
    
    def update_label(self, label, value):
        label.config(text=str(value))
    
    def browse_input_files(self):
        """选择多个PDF文件"""
        filenames = filedialog.askopenfilenames(
            title="选择PDF文件（可多选）",
            filetypes=[("PDF文件", "*.pdf"), ("所有文件", "*.*")]
        )
        if filenames:
            self.input_pdf_paths = list(filenames)
            if len(self.input_pdf_paths) == 1:
                self.input_files_label.config(text=os.path.basename(self.input_pdf_paths[0]))
            else:
                self.input_files_label.config(text=f"已选择 {len(self.input_pdf_paths)} 个文件")
            
            # 自动设置输出目录为第一个文件的目录
            if not self.output_dir.get():
                first_dir = os.path.dirname(self.input_pdf_paths[0])
                self.output_dir.set(first_dir)
    
    def browse_output_dir(self):
        """选择输出目录"""
        dirname = filedialog.askdirectory(title="选择输出目录")
        if dirname:
            self.output_dir.set(dirname)
    
    def choose_color(self):
        color = colorchooser.askcolor(title="选择水印颜色", initialcolor=self.color_code.get())
        if color[1]:
            self.color_code.set(color[1])
            self.color_canvas.config(bg=color[1])
    
    def start_batch_processing(self):
        """开始批量处理"""
        if not self.input_pdf_paths:
            messagebox.showerror("错误", "请选择要处理的PDF文件！")
            return
        
        if not self.output_dir.get():
            messagebox.showerror("错误", "请选择输出目录！")
            return
        
        # 禁用按钮防止重复点击
        self.process_button.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_label.config(text="正在处理，请稍候...")
        
        # 在新线程中处理，避免界面卡死
        threading.Thread(target=self.batch_process_files, daemon=True).start()
        
        # 启动进度更新
        self.root.after(100, self.update_progress)
    
    def batch_process_files(self):
        """批量处理文件的核心逻辑"""
        total_files = len(self.input_pdf_paths)
        success_count = 0
        error_files = []
        
        for i, input_path in enumerate(self.input_pdf_paths):
            try:
                # 更新进度
                progress = (i / total_files) * 100
                self.progress_queue.put(("progress", progress))
                self.progress_queue.put(("status", f"正在处理: {os.path.basename(input_path)} ({i+1}/{total_files})"))
                
                # 处理单个文件
                output_path = self.get_output_path(input_path)
                if self.add_watermark_to_file(input_path, output_path):
                    success_count += 1
                else:
                    error_files.append(os.path.basename(input_path))
                
            except Exception as e:
                error_files.append(os.path.basename(input_path))
                print(f"处理文件 {input_path} 时出错: {e}")
        
        # 完成处理
        self.progress_queue.put(("progress", 100))
        self.progress_queue.put(("done", success_count, total_files, error_files))
    
    def get_output_path(self, input_path):
        """生成输出文件路径"""
        basename = os.path.basename(input_path)
        name, ext = os.path.splitext(basename)
        output_name = f"{name}_带水印{ext}"
        return os.path.join(self.output_dir.get(), output_name)
    
    def add_watermark_to_file(self, input_path, output_path):
        """为单个文件添加水印"""
        try:
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            r, g, b = self.hex_to_rgb(self.color_code.get())
            can.setFillColorRGB(r, g, b, alpha=self.opacity.get())
            
            # 设置字体
            if self.chinese_font_available:
                can.setFont("SimHei", self.font_size.get())
            else:
                can.setFont("Helvetica-Bold", self.font_size.get())
            
            page_width = 612
            page_height = 792
            
            text = self.watermark_text.get()
            can.saveState()
            can.translate(page_width / 2, page_height / 2)
            can.rotate(self.rotation.get())
            
            # 计算文本宽度
            if self.chinese_font_available:
                text_width = can.stringWidth(text, "SimHei", self.font_size.get())
            else:
                text_width = can.stringWidth(text, "Helvetica-Bold", self.font_size.get())
            
            # 根据密度计算间距
            density_factor = self.density.get() / 5
            base_spacing = text_width * 2
            spacing = base_spacing / density_factor
            
            # 绘制多行水印
            for y in range(-page_height, page_height * 2, int(spacing * 0.8)):
                for x in range(-page_width, page_width * 2, int(spacing)):
                    if self.chinese_font_available:
                        can.setFont("SimHei", self.font_size.get())
                    else:
                        can.setFont("Helvetica-Bold", self.font_size.get())
                    can.drawString(x, y, text)
            
            can.restoreState()
            can.save()
            
            packet.seek(0)
            
            with open(input_path, 'rb') as input_file:
                pdf_reader = PyPDF2.PdfReader(input_file)
                pdf_writer = PyPDF2.PdfWriter()
                
                watermark_pdf = PyPDF2.PdfReader(packet)
                watermark_page = watermark_pdf.pages[0]
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page.merge_page(watermark_page)
                    pdf_writer.add_page(page)
                
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"处理文件 {input_path} 时出错: {e}")
            return False
    
    def update_progress(self):
        """更新进度条和状态"""
        try:
            while not self.progress_queue.empty():
                msg_type, *args = self.progress_queue.get_nowait()
                
                if msg_type == "progress":
                    self.progress_var.set(args[0])
                elif msg_type == "status":
                    self.status_label.config(text=args[0])
                elif msg_type == "done":
                    success_count, total_files, error_files = args
                    self.process_button.config(state=tk.NORMAL)
                    
                    if error_files:
                        error_msg = "\n".join(error_files[:5])  # 只显示前5个错误文件
                        if len(error_files) > 5:
                            error_msg += f"\n... 还有 {len(error_files) - 5} 个文件"
                        messagebox.showwarning(
                            "处理完成", 
                            f"批量处理完成！\n成功: {success_count}/{total_files}\n失败文件:\n{error_msg}"
                        )
                    else:
                        messagebox.showinfo(
                            "处理完成", 
                            f"批量处理完成！\n成功: {success_count}/{total_files} 个文件"
                        )
                    
                    self.status_label.config(text="处理完成")
                    return
        except:
            pass
        
        # 继续检查更新
        self.root.after(100, self.update_progress)
    
    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return r, g, b

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFWatermarkApp(root)
    root.mainloop()
