SELECT video_date, play_type, player_id, play_round, 
	COUNT(faults) AS f_count 
    FROM point_table 
    WHERE player_id = '10'
    GROUP BY video_date, play_type, player_id, play_round, camera_view
    ORDER BY video_date, player_id, play_round;