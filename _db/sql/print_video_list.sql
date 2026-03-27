SELECT video_date, play_type, player_id, play_round, 
       MIN(camera_view) AS representative_view, -- 抓字母序最前面的鏡頭 (例如 LF)
       COUNT(*) AS frames_count                 -- 該鏡頭下的動作筆數
FROM point_table 
WHERE action = '站定準備' 
GROUP BY video_date, play_type, player_id, play_round -- 不再依照鏡頭分組
ORDER BY video_date, player_id, play_round;