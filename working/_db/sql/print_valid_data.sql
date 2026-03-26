SELECT video_date, play_type, player_id, play_round, camera_view, COUNT(*) AS count 
    FROM point_table 
    WHERE action = '站定準備' 
    GROUP BY video_date, play_type, player_id, play_round, camera_view
    ORDER BY video_date, player_id, play_round;