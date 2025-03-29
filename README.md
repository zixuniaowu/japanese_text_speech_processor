# Japanese Text and Speech Processor

本项目是一个日语文本和语音处理工具，支持日语文本处理、文本到语音转换等功能。

## 功能特点

- 日语文本文件的读取和处理
- Markdown 格式的日语文本结构解析
- 使用 Google Text-to-Speech 进行文本到语音转换
- 日语文本的平假名、片假名和罗马字转换
- 音频文件的基本分析
- **Markdown 文件直接转换为语音**

## 安装

### 基本安装

```bash
# 克隆项目（如已下载则跳过此步骤）
git clone <repository-url>
cd japanese_text_speech_processor

# 安装基本依赖
pip install -r requirements.txt

# 安装语音处理所需的依赖
pip install gtts
```

### 文本处理功能（可选）

如果需要使用日语文本转换功能（如转换为平假名、罗马字等）：

```bash
pip install janome pykakasi
```

## 使用方法

### 文本处理

读取日语文本文件：

```bash
python main.py text --read sample_japanese.txt
```

分析日语 Markdown 文件结构：

```bash
python main.py text --read-markdown sample_japanese.md
```

文本转换（需要安装 janome 和 pykakasi）：

```bash
# 将文本转换为平假名
python main.py text --convert "日本語の処理" --to-hiragana

# 将文本转换为罗马字
python main.py text --convert "日本語の処理" --to-romaji

# 将文本转换为片假名
python main.py text --convert "日本語の処理" --to-katakana

# 分词分析
python main.py text --convert "日本語の処理技術は面白いです。" --tokenize
```

### 语音处理

将文本转换为语音（需要互联网连接）：

```bash
# 直接转换文本
python main.py speech --text-to-speech "こんにちは、世界！" --output hello.mp3

# 从文件转换
python main.py speech --text-to-speech sample_japanese.txt --output sample.mp3
```

分析音频文件：

```bash
python main.py speech --analyze-audio data/audio/hello.mp3
```

### Markdown转语音

将Markdown格式的日语文本直接转换为语音：

```bash
# 基本用法 - 将Markdown文件转换为MP3
python markdown_to_speech.py sample_japanese.md --output japanese_sample.mp3

# 同时保存处理后的纯文本
python markdown_to_speech.py sample_japanese.md --output japanese_sample.mp3 --clean

# 指定不同的输出文件名
python markdown_to_speech.py data/text/sample_japanese.md --output data/audio/markdown_speech.mp3
```

这个脚本会：
1. 读取指定的Markdown文件
2. 清理Markdown格式标记以获取纯文本
3. 使用Google TTS引擎将文本转换为语音
4. 保存为MP3文件（如使用`--clean`选项，还会保存处理后的纯文本）

### 演示

运行完整的 gTTS 演示（需要互联网连接）：

```bash
python demo_gtts.py
```

使用主程序运行语音演示：

```bash
python main.py demo --speech
```

运行文本处理演示：

```bash
python main.py demo --text
```

## 项目结构

```
japanese_text_speech_processor/
│
├── data/                # 数据目录
│   ├── audio/           # 生成的音频文件
│   ├── demo/            # 演示生成的文件
│   │   └── gtts/        # gTTS演示文件
│   ├── processed/       # 处理后的数据
│   └── text/            # 文本文件
│
├── src/                 # 源代码
│   ├── text_processor.py          # 文本处理模块
│   ├── speech_processor_gtts.py   # 使用gTTS的语音处理模块
│   └── japanese_phonetics.py      # 日语音韵转换模块
│
├── examples/            # 示例脚本
├── tests/               # 测试文件
├── main.py              # 主程序
├── demo_gtts.py         # gTTS演示脚本
├── markdown_to_speech.py # Markdown转语音脚本
├── requirements.txt     # 依赖列表
└── README.md            # 本文件
```

## 注意事项

1. 语音合成功能需要互联网连接，因为它使用 Google 的在线服务。

2. gTTS 只能生成 MP3 格式的文件，不能直接生成 WAV 文件。如果指定了 .wav 扩展名，程序会创建一个提示文件，并将实际音频保存为 MP3。

3. 为获得最佳效果，请确保安装了所有推荐的依赖包：
   - 基本文本处理：pathlib, typing
   - 日语文本分析：janome, pykakasi
   - 语音合成：gtts

4. 所有生成的音频文件旁会创建同名的 .txt 文件，包含原始文本内容，便于参考。

5. Markdown转语音过程中，脚本会尝试智能处理Markdown格式（如移除代码块、转换列表项为句子等），以提供更自然的语音效果。

## 示例

### 文本到语音转换示例

```bash
# 将问候语转换为语音
python main.py speech --text-to-speech "おはようございます。今日の天気はいいですね。" --output greeting.mp3

# 将诗歌转换为语音
python main.py speech --text-to-speech "桜の花が春風に舞い散る様子は、とても美しいです。" --output poem.mp3
```

### Markdown到语音转换示例

```bash
# 将文档标题页转换为语音
python markdown_to_speech.py README.md --output readme_intro.mp3

# 将日语教程转换为语音
python markdown_to_speech.py data/text/japanese_tutorial.md --output japanese_lesson.mp3 --clean
```

### 文本分析示例

```bash
# 将日文句子转换为不同形式
python main.py text --convert "日本語の自然言語処理は興味深いです。" --to-hiragana --to-romaji
```

## 排障指南

问题：运行时出现 "gtts.tts.gTTSError" 错误
- 原因：没有互联网连接或 Google TTS 服务不可用
- 解决方法：检查网络连接，稍后重试

问题：日语文本转换功能不可用
- 原因：未安装 janome 或 pykakasi
- 解决方法：执行 `pip install janome pykakasi`

问题：Markdown转语音时出现格式问题
- 原因：特殊的Markdown格式可能未被正确处理
- 解决方法：尝试先使用`--clean`选项查看处理后的文本，然后根据需要修改源Markdown文件

## 许可

MIT

## 作者

Created: March 29, 2025
