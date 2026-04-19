"""
PROJECT : Count Valid Data
DETALES :
- 從資料庫中計算目前有效的總資料數
"""

# -- IMPORT-------------------------------------+
import os
import pandas as pd
import sqlite3

# -- VARIABLE-----------------------------------+

# 當前工作目錄
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 資料庫路徑
CONN_PATH = os.path.join(CURRENT_DIR, 'lib/point.db')

PLAY_TYPE = ['發球', '舉球']

# -- FUNCTIONS----------------------------------+

# -- MAIN---------------------------------------+

def main():

    # 檢查資料庫是否存在
    if not os.path.exists(CONN_PATH):
        print(f"[CVD] 找不到資料庫檔案: {CONN_PATH}")
        return

    # 連接資料庫
    conn = sqlite3.connect(CONN_PATH)

    # 定義查詢維度
    dates = ["2026-01-13", "2026-01-21"]
    modes = ["發球", "舉球"]
    p_ids = [
        "01", "02", "03", "04", "05",
        "06", "07", "08", "09", "10",
        "11", "12", "13", "14"
    ]
    p_rounds = ["01", "02", "03", "04", "05"]

    print("-" * 50)

    # 取得資料 (使用參數化進行查詢)
    query  = """
    SELECT video_date, play_type, player_id, play_round, camera_view, COUNT(*) AS count 
    FROM point_table 
    WHERE action  = '站定準備' 
    AND play_type = ?
    GROUP BY video_date, play_type, player_id, play_round, camera_view
    ORDER BY video_date, player_id, play_round;
    """

    for i in PLAY_TYPE:
        # 執行查詢
        result = pd.read_sql_query(query, conn, params=(i,))

        # 印出結果
        if result.empty:
            print("[CVD] 於資料庫中查無指定資料。")
        else:
            # 依照回合維度分組
            grouped = result.groupby(['video_date', 'play_type', 'player_id', 'play_round'])

            c_max = grouped['count'].max().sum()
            c_min = grouped['count'].min().sum()

            print(f"{i}有效總球數(排除重複鏡頭):{c_min} ~ {c_max}")

    # 中斷資料庫
    conn.close()

# -- ENTRY--------------------------------------+
if __name__ == "__main__":
    main()

# -- END----------------------------------------+
