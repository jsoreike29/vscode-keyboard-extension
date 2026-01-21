import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
import subprocess
import threading
import os
import sys
import shutil

class VsceBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VS Code Extension Builder")
        self.root.geometry("500x550")

        # タイトルラベル
        label = tk.Label(root, text="拡張機能 パッケージ化ツール", font=("Meiryo", 14, "bold"))
        label.pack(pady=10)

        # 説明
        desc = tk.Label(root, text="JSONを切り替えてパッケージ化を実行できます")
        desc.pack()

        # --- JSONファイル選択エリア ---
        json_frame = tk.LabelFrame(root, text="キー配列データ (JSON)", font=("Meiryo", 10), padx=10, pady=5)
        json_frame.pack(fill="x", padx=20, pady=10)

        # 現在の状態表示
        self.json_status_label = tk.Label(json_frame, text="現在のファイル: jis_layout.json (既存)", fg="#333")
        self.json_status_label.pack(anchor="w")

        # 読み込みボタン
        load_btn = tk.Button(json_frame, text="別のJSONファイルを読み込む...", command=self.load_json_file)
        load_btn.pack(anchor="e", pady=5)
        # -----------------------------

        # 実行ボタン
        self.build_btn = tk.Button(root, text="パッケージ作成開始", command=self.start_build, 
                                   bg="#007acc", fg="white", font=("Meiryo", 12), width=20)
        self.build_btn.pack(pady=10)

        # ログ表示エリア
        tk.Label(root, text="実行ログ:").pack(anchor="w", padx=10)
        self.log_area = scrolledtext.ScrolledText(root, height=10, state='disabled')
        self.log_area.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def log(self, message):
        """ログエリアに文字を出力する"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def load_json_file(self):
        """ファイルダイアログを開いてJSONを選択し、jis_layout.jsonに上書きコピーする"""
        file_path = filedialog.askopenfilename(
            title="適用したい配列定義JSONを選択してください",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                target_path = "jis_layout.json"
                filename = os.path.basename(file_path)

                # 【修正】同じファイルを選んだ場合のエラー回避
                # 絶対パスに変換して比較し、同じならコピー処理をスキップ
                if os.path.abspath(file_path) == os.path.abspath(target_path):
                    self.log(f">>> 選択されたファイルは既に現在の設定ファイルです: {filename}")
                    self.json_status_label.config(text=f"セット中: {filename} (変更なし)", fg="green", font=("Meiryo", 9, "bold"))
                    return

                # 選択されたファイルを jis_layout.json としてコピー（上書き）
                shutil.copy(file_path, target_path)
                
                # 表示更新
                self.json_status_label.config(text=f"セット中: {filename}", fg="blue", font=("Meiryo", 9, "bold"))
                
                self.log(f">>> レイアウトファイルを更新しました: {filename}")
                self.log(f"    (jis_layout.json の内容が {filename} で上書きされました)")
                
            except Exception as e:
                self.log(f">>> ファイル読み込みエラー: {e}")
                messagebox.showerror("エラー", f"ファイルの読み込みに失敗しました:\n{e}")

    def start_build(self):
        self.build_btn.config(state='disabled', text="実行中...")
        self.log_area.config(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.config(state='disabled')
        
        thread = threading.Thread(target=self.run_vsce)
        thread.start()

    def run_vsce(self):
        self.log(f">>> 作業ディレクトリ: {os.getcwd()}")
        self.log(">>> 処理を開始しました...")
        
        cmd = "npx @vscode/vsce package"

        try:
            process = subprocess.Popen(
                cmd, 
                shell=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                encoding='cp932', 
                errors='replace'
            )

            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.log(output.strip())

            stderr = process.stderr.read()
            if stderr:
                self.log("--- エラー出力 ---")
                self.log(stderr.strip())

            return_code = process.poll()

            if return_code == 0:
                self.log("\n>>> 成功！ .vsixファイルが作成されました。")
                messagebox.showinfo("完了", "パッケージ化に成功しました！")
            else:
                self.log("\n>>> 失敗しました。ログを確認してください。")
                messagebox.showerror("エラー", "パッケージ化に失敗しました。")

        except Exception as e:
            self.log(f"\n>>> 例外が発生しました: {e}")
            messagebox.showerror("例外", str(e))
        
        finally:
            self.build_btn.config(state='normal', text="パッケージ作成開始")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
    
    os.chdir(script_dir)

    root = tk.Tk()
    app = VsceBuilderApp(root)
    root.mainloop()