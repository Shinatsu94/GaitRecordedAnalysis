"""
PROJECT : Show Data Table
DETALES :
- 以指定表格形式輸出資料庫資料
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

# 匯出excel 路徑
E_PATH = os.path.join(CURRENT_DIR, 'lib/失誤統計報表.xlsx')

# -- FUNCTIONS----------------------------------+

# -- MAIN---------------------------------------+

def main():

    # 檢查資料庫是否存在
    if not os.path.exists(CONN_PATH):
        print(f"[PVD] 找不到資料庫檔案: {CONN_PATH}")
        return

    # 連接資料庫
    conn = sqlite3.connect(CONN_PATH)

    print("-" * 50)

    # 取得資料 (使用參數化進行查詢)
    query  = """
    SELECT video_date, player_id, play_type, play_round,
        MAX(c_faults) AS f_count
    FROM (
        SELECT video_date, play_type, player_id, play_round, camera_view,
            COUNT(faults) AS c_faults
        FROM point_table
        GROUP BY video_date, play_type, player_id, play_round, camera_view
    ) AS sub
    GROUP BY video_date, play_type, player_id, play_round
    ORDER BY video_date, player_id, play_type, play_round;
    """

    # 執行查詢
    df = pd.read_sql_query(query, conn)

    # 中斷資料庫
    conn.close()

    # 印出結果
    if df.empty:
        print("[SDT] 於資料庫中查無指定資料。")
        return
    else:
        # 建立 "資料名稱"
        df['資料名稱'] = df['player_id'] + "_" + df['play_type']

        # 進行資料轉置
        pivot_df = df.pivot_table(
            index=['video_date', '資料名稱'],
            columns='play_round',
            values='f_count',
            fill_value=0, # 將空值補0
        ).reset_index()

        # 將數值轉為整數(int)
        cols = pivot_df.columns.drop(['video_date', '資料名稱'])
        pivot_df[cols] = pivot_df[cols].astype(int)

        # 輸出結果
        print(pivot_df.to_string(index=False))
        print("-" * 50)
        print(f"動作缺陷總數(已排除重複): {pivot_df[cols].sum().sum()}")

        # 匯出成 Excel
        #pivot_df.to_excel(E_PATH, index=False)
        #print(f"[SDT] 已匯出檔案: {E_PATH}")


# -- ENTRY--------------------------------------+
if __name__ == "__main__":
    main()

# -- END----------------------------------------+
