# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## コマンド

```bash
# 仮想環境の有効化（Windows）
venv\Scripts\activate

# アプリの起動
streamlit run app.py

# 依存パッケージのインストール
pip install -r requirements.txt
```

テストスイートおよびリンターは未設定。

## モデル設定

使用モデルは `gemini_client.py` の `MODEL_NAME` 定数で一元管理している。

```python
MODEL_NAME = "gemini-2.5-flash"
```

モデルを変更する場合はここを書き換えるだけで全ツールに反映される。`gemini-2.0-flash` は2026年6月1日に廃止済みのため使用不可。

## アーキテクチャ

Streamlit + Google Gemini API（`gemini-2.5-flash`）で構築した個人用AIライティングツール。

**各ツールのデータフロー:**
1. `app.py` が `st.navigation` で全ページを登録 → サイドバーを自動描画
2. `pages/` 内の各ページがユーザー入力を受け取り、`prompts/` のテンプレートでプロンプトを組み立て、`gemini_client.generate()` を呼び出す
3. `gemini_client.py` が唯一の共有APIクライアント — `.env` を読み込み、SDKを初期化し、`generate(prompt, temperature)` を提供する

**`pages/` と `prompts/` の対応** — 各ページファイルには1対1で対応するプロンプトファイルがある:

| ページ | プロンプト定数 | temperature |
|---|---|---|
| `blog_writer.py` | `BLOG_PROMPT` | 0.8 |
| `email_reply.py` | `EMAIL_PROMPT` | 0.6 |
| `summarizer.py` | `SUMMARY_PROMPT` | 0.3 |
| `tone_rewriter.py` | `TONE_PROMPT` | 0.7 |
| `social_media.py` | `SOCIAL_PROMPT` | 0.85 |
| `grammar_checker.py` | `GRAMMAR_PROMPT` | 0.2 |

**構造化出力のパース** — 2つのページでモデルの出力を区切り文字で分割する:
- `grammar_checker.py`: `"CHANGES:"` で分割し、`CORRECTED:` と `CHANGES:` を2カラムに表示
- `blog_writer.py`: `"Meta:"` で分割し、メタディスクリプションを別表示

**SNS投稿生成のみAPI呼び出しが複数回発生する** — プラットフォームごとに `generate()` を個別に呼び出しているため、3プラットフォーム選択時は3回APIリクエストが走る。フォーマットの混同を防ぐための意図的な設計。

**新しいツールを追加する場合:** `prompts/my_tool.py`（文字列定数）を作成 → `pages/my_tool.py`（StreamlitのUI + `generate()` 呼び出し）を作成 → `app.py` に `st.Page(...)` エントリを追加。

**temperatureの選び方の目安:**
- 創作・SNS系（ブログ・SNS投稿）: 0.8〜0.85
- 一般的な変換・書き換え: 0.6〜0.7
- 事実を扱う要約・校正: 0.2〜0.3

## 環境設定

プロジェクトルートに `.env` ファイルが必要:
```
GEMINI_API_KEY=your_key_here
```

`gemini_client.py` はキーが存在しない場合、インポート時に `st.stop()` を呼び出すため、エラーはPythonのトレースバックではなくUI上に表示される。そのため、このモジュールはStreamlitのページ実行コンテキスト内でのみインポートすること。

各ページファイル冒頭の `sys.path.insert(0, ...)` は、Streamlitがページファイルを独自のスコープで実行するため、兄弟ディレクトリのインポートを解決するために必要。

## プロンプト編集時の注意

`prompts/` 内のテンプレートは `str.format()` で変数を展開している。プロンプト内に `{` `}` を含めたい場合（JSONの例示など）は `{{` `}}` とエスケープすること。各プロンプト末尾の「〜のみを出力してください」という指示は、モデルが前置きや注釈を付けるのを防ぐための重要なガードレールのため削除しないこと。
