# lingoBridge

一款面向 Windows 的桌面翻译与语音助手。支持双击 `Ctrl + C` 划词翻译、截图 OCR、AI 与 Google 双路翻译，以及 Edge TTS、Piper 和小米 MiMo TTS 朗读。

## 功能特性

- **划词翻译**：选中文本后连续按两次 `Ctrl + C`，翻译窗口会在光标附近弹出。
- **截图翻译**：按 `Alt + E` 框选屏幕区域，通过本地 RapidOCR 识别文字后自动翻译。
- **双路翻译**：Google 翻译快速返回结果；配置兼容 OpenAI 协议的模型后，可同时获得流式 AI 翻译。
- **智能中英互译**：根据输入内容自动选择中文或英文作为目标语言。
- **文本朗读**：默认支持 Edge TTS；也可配置小米 MiMo TTS，或使用 Piper 进行本地短文本朗读。
- **桌面体验**：系统托盘运行、全局快捷键、浅色/深色主题，并支持自定义唤起与截图快捷键。
- **开机启动**：可在“通用与外观”中选择登录 Windows 后自动在托盘启动。

## 运行环境

- Windows 10/11
- Python 3.10 或更高版本
- 网络连接（Google 翻译、AI 翻译和云端 TTS 需要）

## 快速开始

```powershell
git clone <repository-url>
cd lingoBridge

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

开发环境下直接执行 `python main.py` 不会强制申请管理员权限。如需以管理员权限运行，可使用：

```powershell
python main.py --admin
```

程序启动后会常驻系统托盘。

## 快捷键

| 操作 | 默认快捷键 | 说明 |
| --- | --- | --- |
| 划词翻译 | 连续两次 `Ctrl + C` | 先选中文本，再在 0.6 秒内连续复制两次 |
| 显示或隐藏主窗口 | `Alt + Q` | 可在设置中修改 |
| 截图翻译 | `Alt + E` | 框选区域后自动 OCR 并翻译，可在设置中修改 |
| 退出程序 | 托盘菜单 | 右键单击托盘图标并选择退出 |

如果快捷键被其他软件占用，请在设置中更换组合键。

## 翻译配置

不配置 API Key 时，程序仍可使用 Google 翻译。若要启用 AI 翻译，请打开托盘菜单中的“设置”，填写：

- `API Key`
- `API Base URL`
- 模型名称或模型接入点

翻译客户端使用 OpenAI 兼容接口，可连接支持该协议的模型服务。实际可用的模型、鉴权方式和费用以服务提供商说明为准。

## 语音朗读

默认使用 Edge TTS，无需额外下载模型。设置页还提供以下选项：

- **Piper 本地 TTS**：适合短文本，需要自行准备 Piper 程序和语音模型。
- **小米 MiMo TTS**：需要配置相应的 API Key、接口地址、模型与音色。
- **pygame / mpv 播放器**：默认使用 pygame；安装 mpv 后可在设置中切换。

启用本地 Piper 或 mpv 时，在项目根目录创建 `mpv` 文件夹：

```text
lingoBridge/
├─ main.py
└─ mpv/
   ├─ mpv.exe
   ├─ piper.exe
   ├─ zh_CN-huayan-medium.onnx
   └─ en_US-lessac-medium.onnx
```

也可以通过环境变量 `LINGOBRIDGE_TOOL_DIR` 指定上述工具所在目录。

> `mpv` 目录、可执行文件和模型文件默认不会提交到 Git，请根据各项目的许可协议从官方渠道获取。

## 配置与日志

应用会将用户配置和日志保存在：

```text
%APPDATA%\lingoBridge\
├─ config.json
└─ lingobridge_error.log
```

仓库中的 `config.example.json` 仅用于展示配置结构。请不要把真实 API Key、`.env`、日志或个人配置提交到仓库。

## 打包 Windows 程序

项目提供了 PyInstaller 构建脚本：

```powershell
python build_exe.py
```

构建结果位于：

```text
dist\lingoBridge\lingoBridge.exe
```

如需在构建完成后复制到指定发布目录：

```powershell
python build_exe.py --deploy-dir D:\Release\lingoBridge
```

注意：指定的目标目录如果已经存在，构建脚本会先清空该目录再复制新版本，请确认路径无误。

## 项目结构

```text
lingoBridge/
├─ core/              # 翻译、OCR、TTS 与配置
├─ ui/                # 主窗口、设置、托盘与截图界面
├─ utils/             # Windows API 工具
├─ docs/              # 维护文档
├─ main.py            # 程序入口
├─ build_exe.py       # PyInstaller 构建脚本
└─ requirements.txt   # Python 依赖
```

## 注意事项

- 截图 OCR 在本地执行；Google 翻译、AI 翻译及云端 TTS 会把相应文本发送给第三方服务。
- 打包版本可能申请管理员权限，以提高全局快捷键和剪贴板监听的可靠性。
- 若 AI 翻译不可用，请优先检查 API Key、Base URL、模型名称和网络连接。
- 若截图功能不可用，请确认 `rapidocr-onnxruntime` 与 `onnxruntime` 已正确安装。

## License

MIT License Jinser Zhao
