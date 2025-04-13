# 日本語テキスト・音声処理ツール (Japanese Text and Speech Processor)

日本語のテキストと音声を総合的に処理するツールで、テキスト分析、テキスト読み上げ変換、PowerPointのビデオ変換など、様々な機能をサポートしています。

## 主な機能

- **テキスト処理**：日本語テキストファイルの読み込みと分析
- **Markdown解析**：日本語Markdownファイル構造の解析
- **音声合成**：日本語テキストを音声に変換（Google TTSを使用）
- **テキスト変換**：日本語テキストをひらがな、カタカナ、ローマ字に変換
- **Markdownから音声へ**：Markdownドキュメントを直接音声に変換
- **PPTからビデオへ**：PowerPointプレゼンテーションを日本語ナレーション付きビデオに変換

## インストールガイド

### 基本インストール

```bash
# プロジェクトのクローン
git clone https://github.com/yourusername/japanese_text_speech_processor.git
cd japanese_text_speech_processor

# 依存関係のインストール
pip install -r requirements.txt
```

### 特定機能のためのインストール

必要な機能に応じて、特定の依存パッケージをインストールします：

```bash
# 音声合成機能
pip install gtts

# テキスト変換機能
pip install janome pykakasi

# PPTからビデオへの変換機能
pip install python-pptx Pillow moviepy
```

## 使用ガイド

### テキスト処理

```bash
# 日本語テキストファイルの読み込み
python main.py text --read sample_japanese.txt

# Markdownファイルの分析
python main.py text --read-markdown sample_japanese.md

# 日本語テキスト変換
python main.py text --convert "日本語の自然言語処理" --to-hiragana
python main.py text --convert "日本語の自然言語処理" --to-romaji
python main.py text --convert "日本語の自然言語処理" --to-katakana
```

### 音声合成

```bash
# テキストを直接音声に変換
python main.py speech --text-to-speech "こんにちは、世界！" --output hello.mp3

# テキストファイルを音声に変換
python main.py speech --text-to-speech sample_japanese.txt --output sample.mp3
```

### Markdownから音声への変換

```bash
# Markdownドキュメントを音声に変換
python markdown_to_speech.py sample_japanese.md --output japanese_audio.mp3

# 処理された純テキストも保存
python markdown_to_speech.py sample_japanese.md --output japanese_audio.mp3 --clean
```

### PowerPointからビデオへの変換

```bash
# PPTを日本語ナレーション付きビデオに変換
python ppt_to_narrated_video.py presentation.pptx --output narrated_video.mp4

# 各スライドの最小表示時間（秒）を設定
python ppt_to_narrated_video.py presentation.pptx --output narrated_video.mp4 --min-duration 5.0

# 一時ファイルを保持（デバッグ用）
python ppt_to_narrated_video.py presentation.pptx --output narrated_video.mp4 --keep-temp
```

### デモスクリプト

```bash
# Google TTSデモの実行
python demo_gtts.py

# 音声処理デモの実行
python main.py demo --speech

# テキスト処理デモの実行
python main.py demo --text
```

## 機能詳細

### テキスト処理機能

- **テキスト読み込み**：UTF-8エンコードの日本語テキストファイルをサポート
- **Markdown解析**：見出し、リスト、コードブロックなどのMarkdown要素を識別
- **テキスト変換**：
  - 漢字→ひらがな
  - 漢字→カタカナ
  - 日本語→ローマ字（romaji）
- **テキスト分析**：日本語NLPツールを使用した品詞分析

### 音声合成機能

- **Google TTS**：Googleのオンラインサービスを使用した高品質な日本語音声合成
- **MP3生成**：MP3形式の音声ファイルの作成
- **音声分析**：生成された音声ファイル属性の分析

### Markdownから音声への機能

- **Markdown解析**：Markdown形式要素のインテリジェントな処理
- **フォーマットクリーニング**：音声読み上げに適さない形式要素の削除
- **バッチ変換**：Markdownドキュメント全体を流暢な音声ナレーションに変換

### PPTからビデオへの機能

- **テキスト抽出**：PPTスライドからテキストコンテンツを抽出
- **音声生成**：各スライドに対応する音声解説を作成
- **スライドエクスポート**：PPTスライドを高品質画像としてエクスポート
- **ビデオ合成**：スライド画像と音声を完全なビデオに合成
- **LibreOffice統合**：LibreOffice（利用可能な場合）を使用して高品質スライド画像をエクスポート

## プロジェクト構造

```
japanese_text_speech_processor/
│
├── data/                # データディレクトリ
│   ├── audio/           # 音声ファイル
│   ├── text/            # テキストファイル
│   ├── processed/       # 処理済みデータ
│   └── demo/            # デモファイル
│
├── src/                 # ソースコード
│   ├── text_processor.py        # テキスト処理モジュール
│   ├── speech_processor_gtts.py # 音声処理モジュール
│   └── japanese_phonetics.py    # 日本語音韻変換モジュール
│
├── examples/            # サンプルスクリプト
├── tests/               # テストファイル
│
├── main.py                  # メインプログラム
├── markdown_to_speech.py    # Markdownから音声への変換スクリプト
├── ppt_to_narrated_video.py # PPTからビデオへの変換スクリプト
├── demo_gtts.py             # Google TTSデモ
│
├── requirements.txt     # 依存パッケージリスト
└── README.md            # プロジェクト説明ドキュメント
```

## 使用例

### 音声合成の例

```bash
# 挨拶音声の生成
python main.py speech --text-to-speech "おはようございます。今日もいい天気ですね。" --output greeting.mp3

# 技術紹介音声の生成
python main.py speech --text-to-speech "人工知能と自然言語処理の技術について説明します。" --output tech_intro.mp3
```

### PPTからビデオへの変換例

```bash
# 日本語講座PPTの変換
python ppt_to_narrated_video.py japanese_lesson.pptx --output lesson_video.mp4

# ビジネスプレゼンテーションPPTの変換（最小時間を設定）
python ppt_to_narrated_video.py business_presentation.pptx --output business_video.mp4 --min-duration 6.0
```

### テキスト変換の例

```bash
# 文章をひらがなに変換
python main.py text --convert "日本語は面白いです。" --to-hiragana
# 出力: にほんごはおもしろいです。

# 文章をローマ字に変換
python main.py text --convert "日本語は面白いです。" --to-romaji
# 出力: nihongo wa omoshiroi desu.
```

## 注意事項

1. **ネットワーク要件**：Google TTS機能はインターネット接続が必要です。

2. **ファイル形式**：
   - 音声生成はデフォルトでMP3形式
   - PPTは.pptおよび.pptx形式をサポート
   - テキストファイルはUTF-8エンコーディングを使用する必要があります

3. **依存関係**：
   - 異なる機能には異なる依存パッケージが必要
   - requirements.txtに従って必要な依存関係をすべてインストールしてください

4. **LibreOffice**：
   - PPTからビデオへの変換機能では、高品質スライドをエクスポートするためにLibreOfficeを使用可能
   - インストールされていない場合、代替方法で簡易画像を生成します

5. **処理制限**：
   - Google TTSは1回のリクエストで処理できるテキストの長さに制限があります
   - 大きなPPTファイルの処理には時間がかかることがあります

## トラブルシューティング

**問題**：音声生成で「gTTSError」エラーが発生
- **原因**：ネットワーク接続の問題またはGoogleサービスが一時的に利用できない
- **解決方法**：ネットワーク接続を確認し、後で再試行してください

**問題**：テキスト変換機能が動作しない
- **原因**：janomeまたはpykakasiがインストールされていない
- **解決方法**：`pip install janome pykakasi`を実行してください

**問題**：PPTからビデオへの変換でスライド画像の品質が悪い
- **原因**：LibreOfficeがインストールされていない
- **解決方法**：LibreOfficeをインストールするか、PPT形式を調整してください

**問題**：ビデオ生成プロセス中に「No module named 'moviepy'」と表示される
- **原因**：moviepyがインストールされていない
- **解決方法**：`pip install moviepy`を実行してください

**問題**：大きなファイルを処理する際にメモリエラーが発生
- **原因**：システムメモリ不足
- **解決方法**：他のアプリケーションを閉じるか、システムメモリを増やしてください

## 今後の計画

- Webインターフェースの追加（ブラウザでの使用が容易に）
- より多くの音声合成エンジンのサポート
- 複数ファイルを処理するバッチ処理機能の追加
- より多くのビデオ形式と品質オプションの提供
- PPTアニメーション効果のサポート追加

## ライセンス

MIT

## 作者
jacky wang
作成: 2025年3月

---

*このツールは教育および個人利用のみを目的としています。Google TTSサービスを使用する際は、関連するサービス規約に従ってください。*
