# 資料夾架構
```
./ -- 工作根目錄  
├── _db/ -- 資料庫目錄  
│   ├── lib/ -- 資料儲存目錄  
│   ├── sql/ -- SQL指令存放目錄  
│   ├── count_valid_data.py  -- 計數目前的有效總球數(站定準備)
│   ├── import.py            -- 將資料原始檔匯入資料庫  
│   ├── print_data_status.py -- 查詢指定成員資料進度  
│   ├── setup_db.py          -- 建立空白資料庫(用於初始化)  
│   └── show_data_table.py   -- 顯示當前所有動作缺陷數量  
│  
├── 0327/ -- 每次取得的原始資料 請依實際日期做命名
|   ├── 04.csv
|   └── ...
└── newest/ -- 資料原始檔目錄  
    ├── 01.csv  
    ├── 02.csv  
    ├── 03.csv  
    ├── ...  
    ├── 14.csv  
    └── README.md -- 說明各原始資料完成狀態與資料日期等資訊  
```

## 操作基本說明
如工作目錄與上述表格不同，執行各程式前請務必檢查 ``VARIABLE`` 區塊宣告之路徑是否正確。  
- import.py
  - 匯入資料前，會將原先資料庫目標資料**先清除再匯入**，請留意。
  - 預設資料來源為 ``newest/*.csv``
- show_data_table.py
  - 如果需要輸出Excel資料，大約 80 行左右，將註解取消即可。 (如報錯請自行補齊套件)

## 開發日誌
- v1.0: 基本功能上線並推上Github
- v1.1: 追加fps 和 version 欄位資訊
- v1.2: 重新修正v1.1資料判定
  - create_db 已修改
  - import.py 已修改
  - print_data_status 未修改，需追加版本功能
  - show_data_table 未修改，需追加版本功能
  - count_valid_data 未修改，需追加版本功能
- v1.3:
  - import.py 更動核心寫入邏輯以及將檔名替換成標準格式
  - print_data_status 已修改，可以如期閱讀資料
  - show_data_table 未更新 但勉強不影響核心功能