"""
PROJECT : Import Datas
DETALES :
- 建立 SQL 資料庫
- 從外部載入 SQL 建立指令.txt
"""

# -- IMPORT-------------------------------------+
import os
import pandas as pd
import sqlite3

# -- PATH---------------------------------------+

# 資料庫路徑
CONN_PATH = 'lib/point.db'

# 資源目錄
SRC_DIR = '../newest'

# -- FUNCTIONS----------------------------------+

def import_csv(file_path):
    """
    將 CSV 資料匯入資料庫
    資料庫格式要求:
    id (自動生成), video_date, video_name, player_id, play_round, camera_view, action, frame, time_sec, faults
    """

    try:
        # 讀取 CSV
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"[IDs] 讀取檔案失敗: {e}")
        return

    try:
        # 將欄位重新命名以符合資料庫格式
        rename_map = {
            'Date'     : 'video_date',
            'Video'    : 'video_name',
            'View'     : 'camera_view',
            'Action'   : 'action',
            'Frame'    : 'frame',
            'Time_Sec' : 'time_sec',
            'Faults'   : 'faults'
        }
        df = df.rename(columns=rename_map)

        # 先將日期轉為字串
        # 再轉換為標準格式
        # 260121 -> 2026-01-21
        df['video_date'] = df['video_date'].astype(str)
        df['video_date'] = pd.to_datetime(df['video_date'], format='%y%m%d').dt.date

        # 從檔名取得當前球員編號與回合數
        """
        影片日期_項目名稱_球員編號_進行回合_畫面視角_每秒幀數
        260121_發球_01_01_LF_240.mov
        """

        parts = df['video_name'].str.split('_', expand=True)

        df['play_type']  = parts[1] if len(parts) > 1 else "預設"
        df['player_id']  = parts[2] if len(parts) > 2 else "-1"
        df['play_round'] = parts[3] if len(parts) > 3 else "-1"

        # 將空值(NaN) 轉為空字串
        #df = df.fillna('')

        # 篩選指定欄位
        db_columns = ['video_date', 'video_name', 'play_type', 'player_id', 'play_round', 'camera_view', 'action', 'frame', 'time_sec', 'faults']
        df = df[db_columns]

        # 確保 lib 資料夾存在
        os.makedirs(os.path.dirname(CONN_PATH), exist_ok=True)

        # 與資料庫建立連線
        conn = sqlite3.connect(CONN_PATH)

        # 將資料匯入資料庫
        df.to_sql('point_table', conn, if_exists='append', index=False)

        # 與資料庫中斷連線
        conn.close()
        print(f"[IDs] 已成功匯入: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"[IDs] 資料處理或資料庫連線失敗: {e}")
        return

# -- MAIN---------------------------------------+

def main():
    # CSV 資源格式如下
    """
    Video,Date,View,Action,Frame,Time_Sec,Faults
    260121_發球_01_01_LF_240.mov,260121,LF,站定準備,596,19.876654,"nan"
    """

    print("[IDs] 🧹 清除先前資料，重新匯入")
    conn = sqlite3.connect(CONN_PATH)
    try:
        # 僅刪除資料，保留表格結構
        conn.execute("DELETE FROM point_table")
        conn.commit()
    except sqlite3.OperationalError:
        # 如果是第一次執行，表格還不存在會噴錯，直接跳過即可
        pass
    conn.close()

    print("\n[IDs] 開始進行匯入作業..")
    count = 0 # 檔案計數器

    # 遍歷資源目錄中的所有 .csv 檔案
    for root, dirs, files in os.walk(SRC_DIR):
        # 取得子目錄名稱
        folder_name = os.path.basename(root)
        
        # 遍歷所有檔案
        for f in files:
            # 篩選副檔名
            if not f.endswith('.csv'):
                continue

            # 讀取 CSV 資料
            file_path = os.path.join(root, f)
            import_csv(file_path)
            count += 1

    print(f"[IDs] 📦 總計已匯入 {count} 份 CSV 檔案")

# -- ENTRY--------------------------------------+
if __name__ == "__main__":
    main()

# -- END----------------------------------------+
