import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageSequence
from ai_core import AIPetCore
import sys

class DesktopPet:
    def __init__(self):
        self.window = tk.Tk()
        self.window.overrideredirect(True)
        # 不设置置顶，避免遮挡其他应用
        # self.window.attributes('-topmost', True)
        self.window.attributes('-transparentcolor', 'white')
        
        self.pet_width = 200
        self.pet_height = 200
        self.window.geometry(f"{self.pet_width}x{self.pet_height}+100+100")
        
        # 动图路径（请修改为你的实际路径）
        self.pet_image_path = r"C:\Users\17947\Desktop\MyAIPet\pet.gif"
        
        self.original_frames = []
        self.resized_frames = []
        self.frame_index = 0
        self.animation_id = None
        
        self.load_animated_gif()
        
        self.pet_label = tk.Label(self.window, bg='white')
        self.pet_label.pack(fill=tk.BOTH, expand=True)
        self.start_animation()
        
        self.ai = AIPetCore(
            model_name="qwen2.5:7b",   # 改为你的模型名
            system_prompt="你是一只可爱的电子小猫桌宠，名字叫“哈基米南北绿豆”。你总是用简短、温暖、可爱的语气说话，每句话结尾可以加上“喵~”。你非常喜欢和主人聊天。"
        )
        
        self.chat_window = None
        self.chat_display = None
        self.input_entry = None
        
        # 拖拽绑定
        self.pet_label.bind('<Button-1>', self.start_move)
        self.pet_label.bind('<B1-Motion>', self.on_move)
        # 双击打开聊天
        self.pet_label.bind('<Double-Button-1>', self.toggle_chat)
        # 滚轮缩放
        self.pet_label.bind('<MouseWheel>', self.on_mousewheel)
        
        # 创建红叉关闭按钮
        self.create_close_button()
        
        self.window.mainloop()
    
    # ---------- 红叉关闭按钮 ----------
    def create_close_button(self):
        size = 28
        self.close_canvas = tk.Canvas(
            self.window,
            width=size,
            height=size,
            bg='white',
            highlightthickness=0,
            bd=0
        )
        self.circle = self.close_canvas.create_oval(
            4, 4, size-4, size-4,
            fill='#E53935',
            outline=''
        )
        self.text = self.close_canvas.create_text(
            size//2, size//2,
            text="✕",
            font=("Segoe UI", 14, "bold"),
            fill='white'
        )
        self.close_canvas.tag_bind(self.circle, "<Enter>", self.close_hover)
        self.close_canvas.tag_bind(self.text, "<Enter>", self.close_hover)
        self.close_canvas.tag_bind(self.circle, "<Leave>", self.close_leave)
        self.close_canvas.tag_bind(self.text, "<Leave>", self.close_leave)
        self.close_canvas.tag_bind(self.circle, "<Button-1>", self.quit_program)
        self.close_canvas.tag_bind(self.text, "<Button-1>", self.quit_program)
        self.close_canvas.place(relx=1.0, rely=0, anchor='ne', x=-12, y=8)
    
    def close_hover(self, event):
        self.close_canvas.itemconfig(self.circle, fill='#B71C1C')
    
    def close_leave(self, event):
        self.close_canvas.itemconfig(self.circle, fill='#E53935')
    
    def quit_program(self, event=None):
        self.window.quit()
        self.window.destroy()
        sys.exit(0)
    
    # ---------- 动图加载 ----------
    def load_animated_gif(self):
        try:
            im = Image.open(self.pet_image_path)
            self.original_frames = []
            for frame in ImageSequence.Iterator(im):
                frame_rgba = frame.convert("RGBA")
                self.original_frames.append(frame_rgba)
            if not self.original_frames:
                raise ValueError("GIF 没有帧")
            self._resize_all_frames()
        except Exception as e:
            print(f"动图加载失败: {e}，使用粉色占位")
            placeholder = Image.new('RGBA', (self.pet_width, self.pet_height), (255,192,203,255))
            self.original_frames = [placeholder]
            self._resize_all_frames()
    
    def _resize_all_frames(self):
        self.resized_frames = []
        for frame in self.original_frames:
            resized = frame.resize((self.pet_width, self.pet_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(resized)
            self.resized_frames.append(photo)
    
    def start_animation(self):
        if self.resized_frames:
            self.pet_label.config(image=self.resized_frames[0])
            self.animate()
    
    def animate(self):
        if not self.resized_frames:
            return
        self.frame_index = (self.frame_index + 1) % len(self.resized_frames)
        self.pet_label.config(image=self.resized_frames[self.frame_index])
        self.animation_id = self.window.after(100, self.animate)
    
    def stop_animation(self):
        if self.animation_id:
            self.window.after_cancel(self.animation_id)
            self.animation_id = None
    
    def update_pet_image(self):
        self.stop_animation()
        self._resize_all_frames()
        self.frame_index = 0
        self.start_animation()
    
    # ---------- 拖拽移动 ----------
    def start_move(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
    
    def on_move(self, event):
        x = self.window.winfo_x() + (event.x - self.drag_start_x)
        y = self.window.winfo_y() + (event.y - self.drag_start_y)
        self.window.geometry(f"+{x}+{y}")
        # 聊天窗口跟随移动
        if self.chat_window and self.chat_window.winfo_exists():
            chat_x = x + self.pet_width + 10
            chat_y = y
            screen_width = self.window.winfo_screenwidth()
            screen_height = self.window.winfo_screenheight()
            width = self.chat_window.winfo_width()
            height = self.chat_window.winfo_height()
            if chat_x + width > screen_width:
                chat_x = screen_width - width - 10
            if chat_y + height > screen_height:
                chat_y = screen_height - height - 10
            if chat_x < 0: chat_x = 10
            if chat_y < 0: chat_y = 10
            self.chat_window.geometry(f"+{chat_x}+{chat_y}")
    
    # ---------- 滚轮缩放 ----------
    def on_mousewheel(self, event):
        delta = 1 if event.delta > 0 else -1
        new_w = self.pet_width + delta * 10
        new_h = self.pet_height + delta * 10
        if new_w < 50:
            new_w = 50
            new_h = 50
        if new_w != self.pet_width:
            self.pet_width = new_w
            self.pet_height = new_h
            self.window.geometry(f"{self.pet_width}x{self.pet_height}")
            self.update_pet_image()
            if self.chat_window and self.chat_window.winfo_exists():
                self.resize_chat_window()
    
    # ---------- 聊天窗口 ----------
    def toggle_chat(self, event=None):
        if self.chat_window and self.chat_window.winfo_exists():
            self.chat_window.destroy()
            self.chat_window = None
        else:
            self.create_chat_window()
    
    def resize_chat_window(self):
        scale = self.pet_width / 200
        new_width = max(200, int(280 * scale))
        new_height = max(250, int(380 * scale))
        self.chat_window.geometry(f"{new_width}x{new_height}")
        font_size = max(10, min(16, int(11 + (scale - 1) * 4)))
        if self.chat_display:
            self.chat_display.config(font=("微软雅黑", font_size))
            self.chat_display.tag_config("user", font=("微软雅黑", font_size, "bold"))
            self.chat_display.tag_config("pet", font=("微软雅黑", font_size))
            self.chat_display.tag_config("system", font=("微软雅黑", font_size-1, "italic"))
        if self.input_entry:
            self.input_entry.config(font=("微软雅黑", font_size))
        x = self.window.winfo_x() + self.pet_width + 10
        y = self.window.winfo_y()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        if x + new_width > screen_width:
            x = screen_width - new_width - 10
        if y + new_height > screen_height:
            y = screen_height - new_height - 10
        if x < 0: x = 10
        if y < 0: y = 10
        self.chat_window.geometry(f"+{x}+{y}")
    
    def create_chat_window(self):
        scale = self.pet_width / 200
        width = max(200, int(280 * scale))
        height = max(250, int(380 * scale))
        font_size = max(10, min(16, int(11 + (scale - 1) * 4)))
        x = self.window.winfo_x() + self.pet_width + 10
        y = self.window.winfo_y()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        if x + width > screen_width:
            x = screen_width - width - 10
        if y + height > screen_height:
            y = screen_height - height - 10
        if x < 0: x = 10
        if y < 0: y = 10
        
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("🐱 哈基米南北绿豆")
        self.chat_window.geometry(f"{width}x{height}+{x}+{y}")
        self.chat_window.attributes('-topmost', True)  # 聊天框可以置顶，便于输入
        self.chat_window.configure(bg='#2b2b2b')
        self.chat_window.resizable(True, True)
        
        main_frame = tk.Frame(self.chat_window, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)
        
        self.chat_display = scrolledtext.ScrolledText(
            main_frame, wrap=tk.WORD, state=tk.DISABLED,
            font=("微软雅黑", font_size), bg='#1e1e1e', fg='#eeeeee',
            insertbackground='white', relief='flat', borderwidth=0,
            padx=5, pady=5
        )
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=3, pady=3)
        self.chat_display.tag_config("user", foreground="#4FC3F7", font=("微软雅黑", font_size, "bold"))
        self.chat_display.tag_config("pet", foreground="#FFB74D", font=("微软雅黑", font_size))
        self.chat_display.tag_config("system", foreground="#aaaaaa", font=("微软雅黑", font_size-1, "italic"))
        
        input_frame = tk.Frame(main_frame, bg='#2b2b2b')
        input_frame.grid(row=1, column=0, sticky="ew", padx=3, pady=3)
        input_frame.grid_columnconfigure(0, weight=1)
        
        self.input_entry = tk.Entry(
            input_frame, font=("微软雅黑", font_size),
            bg='#f0f0f0', fg='black', insertbackground='black',
            relief='solid', borderwidth=1
        )
        self.input_entry.grid(row=0, column=0, sticky="ew", padx=(0,4), ipady=2)
        self.input_entry.bind("<Return>", self.send_message)
        
        send_btn = tk.Button(
            input_frame, text="发", command=self.send_message,
            bg='#4CAF50', fg='white', activebackground='#45a049',
            relief='flat', font=("微软雅黑", font_size), width=3, cursor="hand2"
        )
        send_btn.grid(row=0, column=1)
        
        btn_frame = tk.Frame(self.chat_window, bg='#2b2b2b')
        btn_frame.pack(fill=tk.X, pady=(0,3))
        clear_btn = tk.Button(
            btn_frame, text="清空", command=self.clear_memory,
            bg='#444444', fg='white', activebackground='#555555',
            relief='flat', font=("微软雅黑", font_size), padx=5, pady=1, cursor="hand2"
        )
        clear_btn.pack(side=tk.RIGHT, padx=5)
        
        self.append_message("✨ 系统", "双击桌宠开关聊天 | 红叉退出")
        self.input_entry.focus_set()
    
    def append_message(self, sender, message):
        if not self.chat_display:
            return
        self.chat_display.config(state=tk.NORMAL)
        if sender == "你":
            tag = "user"
        elif sender == "哈基米南北绿豆":
            tag = "pet"
        else:
            tag = "system"
        self.chat_display.insert(tk.END, f"{sender}: ", tag)
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self, event=None):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return
        self.input_entry.delete(0, tk.END)
        self.append_message("你", user_input)
        self.append_message("哈基米南北绿豆", "…")
        try:
            reply = self.ai.talk(user_input)
            self.chat_display.config(state=tk.NORMAL)
            last_line_start = self.chat_display.index("end-2c linestart")
            self.chat_display.delete(last_line_start, "end-1c")
            self.chat_display.config(state=tk.DISABLED)
            self.append_message("哈基米南北绿豆", reply)
        except Exception as e:
            self.chat_display.config(state=tk.NORMAL)
            last_line_start = self.chat_display.index("end-2c linestart")
            self.chat_display.delete(last_line_start, "end-1c")
            self.chat_display.config(state=tk.DISABLED)
            self.append_message("错误", str(e))
    
    def clear_memory(self):
        self.ai.clear_history()
        self.append_message("✨ 系统", "记忆已清空")

if __name__ == "__main__":
    pet = DesktopPet()