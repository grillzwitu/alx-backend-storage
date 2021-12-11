-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers 
-- that computes and store the average weighted score for all students.

-- Requirements:

-- Procedure ComputeAverageWeightedScoreForUsers is not taking any input.

DELIMITER ||
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN UPDATE users AS user, (
SELECT user.id, SUM(score * weight) / SUM(weight) AS wt_avg
FROM users AS user 
JOIN corrections AS corr ON user.id=corr.user_id
JOIN projects AS proj ON corr.project_id=proj.id 
GROUP BY user.id) AS Wt_All

SET user.average_score = Wt_All.wt_avg
WHERE user.id=Wt_All.id;
END ||
DELIMITER ;
