SELECT * FROM point_table WHERE player_id = '08' AND video_date = '2026-01-21' AND play_type = '舉球';
SELECT COUNT(*) AS 卡位次數
FROM point_table 
WHERE player_id = '08' 
  AND video_date = '2026-01-21' 
  AND play_type = '舉球'
  AND play_round = '03'
  AND camera_view = 'L'
  AND action = '卡位(完成轉身等待接球)';