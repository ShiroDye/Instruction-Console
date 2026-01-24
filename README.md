
[![Discord](https://img.shields.io/discord/1305535111697141790?label=Discord&logo=discord&color=7289DA)](https://discord.gg/fBRMhdnhSW)

## 📄 License / 许可证

This project is licensed under the **MIT License**.  
本项目采用 **MIT 许可证** 开源。

> **Summary**: You can use, copy, and modify this software for any purpose, but the author is not responsible for any consequences.  
> **简述**：您可以出于任何目的使用、复制或修改本软件，但作者不承担任何使用后果。

# Instruction Console (指令序列控制台) 

[English Version](#english-version) | [简体中文说明](#简体中文说明) [繁体中文说明](#繁体中文说明)

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
3. **Run**: Click **START EXECUTION**; a 3-second buffer is provided for window switching.
4. **Emergency Stop**: Terminate execution immediately by clicking the red **STOP** button.

### 🛠️ Environment & Build
- **Requirement**: Python 3.8 or higher with the `pynput` library installed.
- **Dependency Installation**: `pip install pynput`
- **Build Command**: 
  ```bash
  pyinstaller -F -w -n "InstructionConsole_Vx.x" main_xxxEN.py

---

<a name="简体中文说明"></a>
## 简中说明
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
3. **缓冲执行**：点击「开始执行」后，程序会预留 3 秒缓冲时间，可在此期间切换至目标操作窗口。
4. **紧急终止**：点击红色「停止执行」按钮或直接关闭程序，即可立即终止自动化任务。

### 🛠️ 环境依赖与打包
- **运行环境**：Python 3.8 及以上版本，需安装 pynput 第三方库。
- **安装依赖命令**：pip install pynput
- **打包指令**：pyinstaller -F -w -n "InstructionConsole_Vx.x" main.xxxCN.py

---

<a name="繁体中文说明"></a>
## 繁中说明
### 項目定位
指令序列控制台是一款輕量級、高精度的自動化工具，旨在簡化重複性的鍵盤操作。

### ✨ 核心特性
- **智能組合鍵解析**：支持 `{}` 模擬多鍵同時按下（組合鍵）、`[]` 模擬單鍵按下，解析邏輯精準。
- **物理延遲優化**：內置 0.05s 按鍵按下延遲 + 0.1s 按鍵保持時間，確保 WIN+R 等系統級快捷鍵 100% 觸發成功。
- **穩健分詞邏輯**：基於正規表示式分詞（Regex-based Tokenizing）的解析引擎，徹底解決字符漏打、指令錯位問題。
- **即時手動錄製**：系統級按鍵攔截能力，可即時捕捉鍵盤操作並自動轉化為標準化指令標籤。
- **靈活循環控制**：支持自定義循環次數，輸入 `inf` 可開啟無限循環模式。

### 🚀 操作步驟
1. **編寫指令**：在主輸入區編寫指令序列，例如 `{[WIN][R]}` 可觸發系統「執行」視窗。
2. **配置循環**：在下方輸入框設置重複執行次數，也可通過選單調節執行速度。
3. **緩衝執行**：點擊「開始執行」後，程式會預留 3 秒緩衝時間，可在此期間切換至目標操作視窗。
4. **緊急終止**：點擊紅色「停止執行」按鈕或直接關閉程式，即可立即終止自動化任務。

### 🛠️ 環境依賴與打包
- **執行環境**：Python 3.8 及以上版本，需安裝 pynput 第三方函式庫。
- **安裝依賴指令**：pip install pynput
- **打包指令**：pyinstaller -F -w -n "InstructionConsole_Vx.x" main_xxxTC.py
