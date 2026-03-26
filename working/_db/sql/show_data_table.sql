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