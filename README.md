# Instruction Console (指令序列控制台) V3.2

[English Version](#english-version) | [中文说明](#中文说明)

---

## English Version

**Instruction Console** is a lightweight, high-precision automation utility designed to simplify repetitive keyboard tasks.

### ✨ Features
* [cite_start]**Smart Parsing**: Supports `{}` for combinations and `[]` for single keys[cite: 5, 12].
* [cite_start]**Stability**: Optimized internal delays (0.05s - 0.1s) for system-level hotkey reliability.
* [cite_start]**Manual Recording**: Real-time keystroke capture with system-level interception.
* [cite_start]**Infinite Loops**: Supports specific counts or `inf` for endless execution.

### 🚀 Usage Guide
1. [cite_start]**Input**: Type instructions like `{[CTRL][C]}` or `[ENTER]`[cite: 7, 15].
2. [cite_start]**Setup**: Set loop count and select speed from the Debug Menu[cite: 20].
3. **Run**: Click **START EXECUTION**; [cite_start]2-second buffer provided[cite: 3].
4. [cite_start]**Emergency Stop**: Use the red **STOP** button to terminate immediately[cite: 16].

### 🛠️ Build
```bash
pip install pynput
pyinstaller -F -w -n "InstructionConsole_V3.2" spam.pyw


<a name="中文说明"></a>
## 中文说明

> [cite_start]**项目定位**：指令序列控制台是一款轻量级、高精度的自动化工具，旨在简化重复性的键盘操作 [cite: 1]。

### ✨ 核心特性
* [cite_start]**智能组合键解析**：支持 `{}` 模拟多键同时按下（如组合键）以及 `[]` 模拟单键 [cite: 6, 8, 12]。
* [cite_start]**物理延迟优化**：内部优化了 0.05s 的按下延迟和 0.1s 的保持时间，确保系统级快捷键（如 `WIN+R`）100% 成功触发 [cite: 9, 10]。
* [cite_start]**稳健分词逻辑**：基于正则分词（Regex-based Tokenizing）的解析引擎，有效解决字符漏打或指令错位问题 [cite: 5, 6]。
* [cite_start]**实时手动录制**：支持系统级按键拦截，实时捕捉您的键盘操作并自动转化为指令标签 [cite: 17, 18, 19]。
* [cite_start]**灵活循环控制**：支持指定具体循环次数，或输入 `inf` 开启无限循环模式 [cite: 3, 4]。

### 🚀 操作步骤
1. [cite_start]**编写指令**：在主输入区编写指令序列，例如输入 `{[WIN][R]}` 弹出运行窗口 [cite: 3]。
2. [cite_start]**配置循环**：在下方输入框设定重复次数，并可通过菜单调节执行速度 [cite: 3, 20]。
3. [cite_start]**缓冲执行**：点击 **开始执行** 后，程序会有 **2秒** 的缓冲时间，请利用这段时间将焦点切换至目标窗口 [cite: 3]。
4. [cite_start]**紧急终止**：点击红色的 **停止执行** 按钮或直接关闭程序即可立即终止任务 [cite: 16, 17]。

### 🛠️ 环境依赖与打包
* [cite_start]**运行环境**：Python 3.8+，需安装 `pynput` 库 [cite: 1]。
* **打包指令**：
  ```bash
  pyinstaller -F -w -n "InstructionConsole_V3.2" spam.pyw
