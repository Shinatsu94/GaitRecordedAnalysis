"""
PROJECT : Print Data Status
DETALES :
- 列出指定資料庫資料
"""

# -- IMPORT-------------------------------------+
import os
import pandas as pd
import sqlite3

# -- VARIABLE-----------------------------------+

# 資料庫路徑
CONN_PATH = 'lib/point.db'
SEARCH_ID = '09'

# -- FUNCTIONS----------------------------------+

# 列出指定範圍的資料數
def print_data_list(id):

    # 檢查資料庫是否存在
    if not os.path.exists(CONN_PATH):
        print(f"[PDL] 找不到資料庫檔案: {CONN_PATH}")
        return

    # 連接資料庫
    conn = sqlite3.connect(CONN_PATH)

    print("-" * 50)
    print(f"{id} 的有效總資料")
    print("-" * 50)

    # 取得資料 (使用參數化進行查詢)
    query = """
    SELECT video_date, player_id, play_type, play_round, camera_view,
        COUNT(*) AS d_count
    FROM point_table
    WHERE player_id = ?
    GROUP BY video_date, play_type, player_id, play_round, camera_view
    ORDER BY video_date, player_id, play_type, play_round, camera_view;
    """

    # 執行查詢
    result = pd.read_sql_query(query, conn, params=(id,))

    # 中斷資料庫
    conn.close()

    # 印出結果
    if result.empty:
        print("[PDL] 於資料庫中查無指定資料。")
    else:
        grouped = result.groupby(['video_date', 'play_type', 'player_id', 'play_round'])

        for keys, group in grouped:
            # 解構分組鍵值
            d, m, p, r = keys

            # 建立前綴標籤
            prefix = f"{d}_{m}_{p}_{r}"
            print(f"{prefix}   資料小計: | ", end="")

            # 遍歷該組合中的所有鏡頭與數量
            for _, row in group.iterrows():
                # 輸出格式：鏡頭:數量
                print(f"{row['camera_view']}:{row['d_count']} | ", end="")
            print()

# 從資料庫中查詢目前有效的資料數
def print_valid_data(id):

    # 檢查資料庫是否存在
    if not os.path.exists(CONN_PATH):
        print(f"[PVD] 找不到資料庫檔案: {CONN_PATH}")
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
    print(f"{id} 的有效球數")
    print("-" * 50)

    # 取得資料 (使用參數化進行查詢)
    query  = f"""
    SELECT video_date, play_type, player_id, play_round, camera_view, 
    COUNT(*) AS count 
    FROM point_table 
    WHERE action = '站定準備' 
        AND player_id = ?
    GROUP BY video_date, play_type, player_id, play_round, camera_view
    ORDER BY video_date, player_id, play_round;
    """

    # 執行查詢
    result = pd.read_sql_query(query, conn, params=(id,))

    # 印出結果
    if result.empty:
        print("[PVD] 於資料庫中查無指定資料。")
    else:
        grouped = result.groupby(['video_date', 'play_type', 'player_id', 'play_round'])

        for keys, group in grouped:
            # 解構分組鍵值
            d, m, p, r = keys

            # 建立前綴標籤
            prefix = f"{d}_{m}_{p}_{r}"
            print(f"{prefix}   球數小計: | ", end="")

            # 遍歷該組合中的所有鏡頭與數量
            for _, row in group.iterrows():
                # 輸出格式：鏡頭:數量
                print(f"{row['camera_view']}:{row['count']} | ", end="")
            print()

    # 中斷資料庫
    conn.close()

# -- MAIN---------------------------------------+
def main(id):
    print_data_list(id)
    print_valid_data(id)


# -- ENTRY--------------------------------------+
if __name__ == "__main__":
    user_input = input('請輸入球員編號(01 ~ 14): ').strip()

    # 將輸入轉換為補零後的兩位數字串 (ex. "1" -> "01", "12" -> "12")
    formatted_id = user_input.zfill(2) if user_input.isdigit() else user_input

    # 檢查是否於指定範圍內
    valid_ids = [str(i).zfill(2) for i in range(1, 15)] # 產生 ['01', '02', ..., '14']

    if formatted_id in valid_ids:
        final_id = formatted_id
    else:
        final_id = SEARCH_ID


    main(final_id)


# -- END----------------------------------------+
