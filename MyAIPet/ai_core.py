import subprocess
import json
import os
import sys

# Windows 下隐藏子进程窗口的标志
if sys.platform == "win32":
    CREATE_NO_WINDOW = 0x08000000
else:
    CREATE_NO_WINDOW = 0

class AIPetCore:
    def __init__(self, model_name="qwen2.5:7b", system_prompt=""):
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.history = []
        self.history_file = "chat_history.json"
        self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                print(f"已加载 {len(self.history)} 条历史记录")
            except:
                self.history = []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def talk(self, user_input):
        if user_input.strip() in ["/end", "结束", "重置", "清空记忆"]:
            self.clear_history()
            return "✨ 记忆已清空，我们重新开始吧～"

        self.history.append({"role": "user", "content": user_input})
        prompt = ""
        if self.system_prompt:
            prompt += self.system_prompt + "\n"
        for msg in self.history:
            if msg["role"] == "user":
                prompt += f"用户: {msg['content']}\n"
            else:
                prompt += f"助手: {msg['content']}\n"
        prompt += "助手: "

        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name, prompt],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8',
                creationflags=CREATE_NO_WINDOW   # 关键：禁止弹窗
            )
            if result.returncode != 0:
                return f"Ollama 错误: {result.stderr}"
            reply = result.stdout.strip()
            self.history.append({"role": "assistant", "content": reply})
            self.save_history()
            return reply
        except subprocess.TimeoutExpired:
            return "AI 响应超时，请稍后再试。"
        except Exception as e:
            return f"调用失败: {str(e)}"

    def clear_history(self):
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        self.save_history()