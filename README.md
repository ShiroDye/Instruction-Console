## 📄 License / 许可证

This project is licensed under the **MIT License**.  
本项目采用 **MIT 许可证** 开源。

> **Summary**: You can use, copy, and modify this software for any purpose, but the author is not responsible for any consequences.  
> **简述**：您可以出于任何目的使用、复制或修改本软件，但作者不承担任何使用后果。

# Instruction Console (指令序列控制台) V3.2

[English Version](#english-version) | [中文说明](#中文说明)

---

## English Version
**Instruction Console** is a lightweight, high-precision automation utility designed to simplify repetitive keyboard tasks.

### ✨ Features
- **Smart Parsing**: Supports `{}` for key combinations and `[]` for single key operations.
- **Stability**: Optimized internal delays (0.05s - 0.1s) to ensure reliable triggering of system-level hotkeys.
- **Manual Recording**: Real-time keystroke capture via system-level interception.
- **Infinite Loops**: Supports setting specific execution counts or using `inf` for endless execution.

### 🚀 Usage Guide
1. **Input**: Enter instruction sequences (e.g., `{[CTRL][C]}` for copy, `[ENTER]` for enter key).
2. **Setup**: Set the loop count and select execution speed from the Debug Menu.
3. **Run**: Click **START EXECUTION**; a 2-second buffer is provided for window switching.
4. **Emergency Stop**: Terminate execution immediately by clicking the red **STOP** button.

### 🛠️ Environment & Build
- **Requirement**: Python 3.8 or higher with the `pynput` library installed.
- **Dependency Installation**: `pip install pynput`
- **Build Command**: 
  ```bash
  pyinstaller -F -w -n "InstructionConsole_V3.2" spam.pyw

---

<a name="中文说明"></a>
## 中文说明
### 项目定位
指令序列控制台是一款轻量级、高精度的自动化工具，旨在简化重复性的键盘操作。

### ✨ 核心特性
- **智能组合键解析**：支持 `{}` 模拟多键同时按下（组合键）、`[]` 模拟单键按下，解析逻辑精准。
- **物理延迟优化**：内置 0.05s 按键按下延迟 + 0.1s 按键保持时间，确保 WIN+R 等系统级快捷键 100% 触发成功。
- **稳健分词逻辑**：基于正则分词（Regex-based Tokenizing）的解析引擎，彻底解决字符漏打、指令错位问题。
- **实时手动录制**：系统级按键拦截能力，可实时捕捉键盘操作并自动转化为标准化指令标签。
- **灵活循环控制**：支持自定义循环次数，输入 `inf` 可开启无限循环模式。

### 🚀 操作步骤
1. **编写指令**：在主输入区编写指令序列，例如 `{[WIN][R]}` 可触发系统“运行”窗口。
2. **配置循环**：在下方输入框设置重复执行次数，也可通过菜单调节执行速度。
3. **缓冲执行**：点击「开始执行」后，程序会预留 2 秒缓冲时间，可在此期间切换至目标操作窗口。
4. **紧急终止**：点击红色「停止执行」按钮或直接关闭程序，即可立即终止自动化任务。

### 🛠️ 环境依赖与打包
- **运行环境**：Python 3.8 及以上版本，需安装 pynput 第三方库。
- **安装依赖命令**：pip install pynput
- **打包指令**：pyinstaller -F -w -n "InstructionConsole_V3.2" spam.pyw
