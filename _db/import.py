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
    id (自動生成), video_date, video_name, player_id, play_round, camera_view, action, fps, version, frame, time_sec, faults
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

        # 將檔名修改成指定格式內容 (處理例外名稱)
        r"""
        Regex 符號語法:
        ^  代表字串開頭
        $  代表字串結尾
        \d 代表任何數字
        .  代表任何字元
        \. 代表'.'字元
        *  代表重複0次以上
        """

        # 檢查日期資訊前是否有雜訊 (ex. "10_追加/260113" 的 "10_追加/")
        is_extra_path = ~df['video_name'].str.match(r'^\d{6}_')

        # 清洗檔名 (移除多餘路徑與底線)
        df['video_name'] = df['video_name'].str.extract(r'(\d{6}_.*)')[0]
        df['video_name'] = df['video_name'].str.replace(r'_(?=\.)', '', regex=True)

        # 拆解檔名取得各欄位資訊
        """
        影片日期_項目名稱_球員編號_進行回合_畫面視角_每秒幀數
        260121_發球_01_01_LF_240.mov
        """
        parts = df['video_name'].str.split('_', expand=True)

        v_date    = df['video_date']
        v_type    = parts[1] if parts.shape[1] > 1 else "預設"
        v_id      = parts[2] if parts.shape[1] > 2 else "-1"
        v_round   = parts[3] if parts.shape[1] > 3 else "-1"
        v_view    = df['camera_view']
        v_fps_ext = parts[5] if parts.shape[1] > 5 else "0"
        v_ext     = df['video_name'].str.split('.').str[-1]

        # 清除 FPS 的雜訊 (.mov .mp4)
        v_fps = v_fps_ext.str.split('.', expand=True)[0]

        # 獨立判斷資料版本
        # 如果檔名有第 7 段 (Index 6)，取其數字
        # 否則根據是否為追加路徑給予 2 或 1
        if parts.shape[1] > 6:
            # 移除附檔名干擾並轉為字串
            v_version = parts[6].str.split('.', expand=True)[0]
            v_version = v_version.replace("", "1").fillna("1")
        # 根據「是否有前置路徑」決定 2 還是 1
        v_version = is_extra_path.map({True: "2", False: "1"})

        # 確保各部件為字串，以便合併成檔名
        s_date    = v_date.astype(str)
        s_type    = v_type.astype(str)
        s_id      = v_id.astype(str)
        s_round   = v_round.astype(str)
        s_view    = v_view.astype(str)
        s_fps     = v_fps.astype(str)
        s_version = v_version.astype(str)
        s_ext     = v_ext.astype(str)

        # 重新組合檔名: 日期_項目_編號_回合_視角_FPS_版本.副檔名
        df['video_name'] = (
        s_date + '_' + s_type + '_' + s_id + '_' + s_round + '_' + s_view + '_' + s_fps + '_' + s_version + '.' + s_ext
        )

        # 將其餘資料寫入資料庫欄位
        df['play_type']  = v_type
        df['player_id']  = v_id
        df['play_round'] = v_round
        df['fps']        = v_fps.astype(int)
        df['version']    = v_version.astype(int)

        # 先將日期轉為字串
        # 再轉換為標準格式
        # 260121 -> 2026-01-21
        df['video_date'] = df['video_date'].astype(str)
        df['video_date'] = pd.to_datetime(df['video_date'], format='%y%m%d').dt.date

        # 將空值(NaN) 轉為空字串
        #df = df.fillna('')

        # 篩選指定欄位
        db_columns = ['video_date', 'video_name', 'play_type', 'player_id', 'play_round', 'camera_view', 'fps', 'version', 'action', 'frame', 'time_sec', 'faults']
        df = df[db_columns]

        # 確保 lib 資料夾存在
        os.makedirs(os.path.dirname(CONN_PATH), exist_ok=True)

        # 與資料庫建立連線
        conn = sqlite3.connect(CONN_PATH)

        # 將資料匯入資料庫
        df.to_sql('point_table', conn, if_exists='append', index=False)

        # 與資料庫中斷連線
        conn.close()
        print(f"[IDs] ✅ 已處理並匯入: {os.path.basename(file_path)}")

    except Exception as e:
        print(f"[IDs] ❌ 資料處理或資料庫連線失敗: {e}")
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
