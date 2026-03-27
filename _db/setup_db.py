"""
PROJECT : Create DataBase
AUTHOR  : PIN CHEN TSAI
VERSION : v0.5
UPDATE  : 2026-03-27
DETALES :
- 建立 SQL 資料庫
- 從外部載入 SQL 建立指令.txt
- 創建資料庫時，會自動新增必要資料夾

STATUS_CODE:

"""

#--- IMPORT---------------------------------------------------+
import sqlite3
import os

#--- VARIABLE-------------------------------------------------+

# 當前工作目錄
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# SQL 檔案路徑
DB_SQL = os.path.join(CURRENT_DIR, 'sql/create_db.sql')

# 資料庫路徑
DB_PATH = os.path.join(CURRENT_DIR, 'lib/point.db')

#--- FUNCTIONS------------------------------------------------+

# 讀取檔案文本
def readfile(file_path):
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"[CDB] ⚠️無法讀取檔案 {file_path}：{e}")

#--- MAIN-----------------------------------------------------+
def create_db(sql_statements, db_path):
    try:

        # 自動新增必要目錄
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"[CDB] 📂 已建立必要的目錄: {db_dir}")

        db_name = os.path.basename(db_path)

        # 連結資料庫 (若不存在會自動建立)
        conn = sqlite3.connect(db_path)

        print(f"[CDB] 正在建立資料庫: {db_path}")

        # 批量執行指令
        conn.executescript(sql_statements)

        # 提交更改並關閉連線
        conn.commit()
        print("[CDB] ✅ 資料表已成功建立！")

    except sqlite3.Error as e:
        print(f"[CDB] ❌ 建立資料庫時發生錯誤: {e}")

    finally:
        if conn:
            conn.close()

#--- ENTRY----------------------------------------------------+
if __name__ == "__main__":
    db_cmd = readfile(DB_SQL)
    #print(db_cmd)
    create_db(db_cmd, DB_PATH)

#--- END------------------------------------------------------+
