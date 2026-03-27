-- 建立標點紀錄表
CREATE TABLE point_table
(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  video_date TEXT, 
  video_name TEXT, 
  play_type TEXT, 
  player_id TEXT, 
  play_round TEXT, 
  camera_view TEXT, 
  fps TEXT, 
  version TEXT, 
  action TEXT, 
  frame INTEGER, 
  time_sec REAL, 
  faults TEXT
);
