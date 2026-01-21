# vscode-keyboard-extension
## VS Code 拡張機能 パッケージ化ツール (VS Code Extension Builder)

このツールは、VS Code拡張機能（キー配列カスタマイズ等）の `.vsix` パッケージ作成を、コマンド操作なしで簡単に行うためのPython製GUIアプリです。

## ✨ 特徴
* **ワンクリック作成**: ボタン一つで `vsce package` コマンドを実行し、`.vsix` ファイルを生成します。
* **JSON切り替え機能**: 複数の配列設定ファイル（`.json`）を読み込み、即座に適用してビルドできます。
* **ログ表示**: エラーや成功のステータスを画面上で確認できます。

## 🛠 動作環境
* **Windows**
* **Python 3.x** (標準ライブラリ `tkinter` を使用)
* **Node.js** (`npx` コマンドが使える状態であること)

## 📦 インストールと配置
このスクリプト (`build_tool.py`) は、拡張機能のプロジェクトルート（`package.json` がある場所）に置いて使用します。

### フォルダ構成例
```text
my-extension/
├── main.py      <-- このツール
├── package.json       <-- 必須
├── jis_layout.json    <-- 現在適用中の配列データ
├── layouts/           <-- (任意) 保存用配列データ置き場
│   ├── qwerty.json
│   └── dvorak_custom.json
└── ...
