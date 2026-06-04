🐱 哈基米南北绿豆 · AI 桌宠
一只会聊天、会动、能拖拽、能缩放、带记忆的桌面宠物。
基于 Ollama 本地大模型 + Python Tkinter 实现，完全本地运行，无需联网。

✨ 功能亮点
🖼️ 透明窗口动画：支持 GIF 动图，宠物可任意拖拽、滚轮缩放
💬 AI 对话：通过 Ollama 调用本地 Qwen2.5 / 通义千问等模型，离线聊天
🧠 上下文记忆：自动保存对话历史，下次启动继续聊（输入 /end 清空）
🪟 聊天窗口：深色主题 + 彩色气泡，可缩放、跟随桌宠移动
🔴 一键退出：右上角红叉按钮，优雅关闭程序
🔝 单击置前：被其他窗口遮挡时，单击桌宠即可临时置顶（0.5秒后自动恢复）
🔧 纯本地运行：无需网络，数据隐私安全

🛠️ 技术栈
Python 3.8+
Tkinter – GUI 框架
Pillow – 图像处理与 GIF 播放
Ollama – 本地大模型推理
subprocess – 调用 Ollama 命令行

📦 安装与运行
1. 安装 Ollama 并下载模型
# 安装 Ollama（官网：ollama.com）
ollama pull qwen2.5:7b   # 或 wen2.5:7b，根据你下载的模型名
2. 克隆项目
git clone https://github.com/yourname/ai-desktop-pet.git
cd ai-desktop-pet
3. 安装 Python 依赖
pip install pillow
4. 准备宠物动图
将你喜欢的 GIF 动图命名为 pet.gif 放在项目根目录。

5. 修改模型名称
编辑 desktop_pet.py，将第 44 行中的 model_name 改为你实际的模型名（通过 ollama list 查看）。

6. 运行桌宠
bash
python desktop_pet.py
无黑框运行：使用 pythonw.exe desktop_pet.py 或打包成 exe。

🎮 交互说明
操作	效果
双击桌宠	打开/关闭聊天窗口
单击桌宠	临时将窗口置前（不挡住工作）
拖拽桌宠	移动位置
滚轮	缩放桌宠大小
拖拽聊天框边缘	手动缩放聊天框
单击红叉	退出程序
🗣️ 聊天功能
输入文字，按回车发送

AI 会用“喵～”的语气回复（可自定义 system prompt）

输入 /end 或点击“清空记忆”即可重置对话

🧩 自定义你的桌宠
更换形象：替换 pet.gif 即可（支持透明背景 PNG/GIF）

修改性格：编辑 desktop_pet.py 中的 system_prompt 变量

调整窗口大小：代码中 pet_width / pet_height 变量

隐藏控制台：将 desktop_pet.py 重命名为 desktop_pet.pyw 并双击

📄 文件结构
text
ai-desktop-pet/
├── desktop_pet.py      # 主程序
├── ai_core.py           # AI 调用与历史记忆模块
├── pet.gif              # 宠物动图（自行准备）
├── restore.png          # 隐藏恢复按钮（可选）
└── chat_history.json    # 自动生成的对话历史文件
🧪 常见问题
Q: 启动后显示粉色方块
A: 没有找到 pet.gif，请检查路径是否正确。

Q: 发送消息无回复
A: 确保 Ollama 服务正在后台运行（任务栏有图标）。

Q: 子进程弹出黑色窗口
A: 已默认使用 CREATE_NO_WINDOW 标志，Windows 下不会弹窗。

📌 待优化
通过任务栏托盘图标恢复隐藏

支持更多模型（如 GPT4All、llama.cpp）

增加喂食/抚摸动画

🐾 最后
这是从零开始，一步步搭建的 AI 桌宠项目。
如果你也想要一只会聊天的电子小猫，欢迎 ⭐ 收藏和 fork ～

注：本项目仅用于个人学习与娱乐，使用本地模型不涉及任何云端数据。
灵感来源于深夜写代码的寂寞与对电子宠物的热爱 🐱💻
