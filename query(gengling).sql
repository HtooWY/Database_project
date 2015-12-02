-- Rate review (player 1 rates review 1 for -1 point)
INSERT INTO rate_review (reviewid, playerid, rating)
VALUES (1, 1, -1); 

-- Change Rate Review (Change player 1's rating on review 1 to 1 point)
UPDATE rate_review
SET rating = 1
WHERE (playerid = 1 AND reviewid = 1);

-- Delete Rate Review
DELETE 
FROM rate_review
WHERE (playerid = 1 AND reviewid = 1);

-- Cannot rate your own review AND update review score
CREATE TRIGGER rate_self 
AFTER INSERT ON rate_review
For Each Row
Begin
	IF (New.playerid)=(SELECT playerid FROM reviews WHERE reviewid=New.reviewid)
	THEN DELETE FROM rate_review WHERE (playerid=New.playerid AND reviewid=New.reviewid);
	ELSE UPDATE reviews SET rating = rating + New.rating WHERE reviewid = New.reviewid;
	END IF;
End;

-- Issue a challenge (player 1 challenges player 2 on gameid 1 for challengeid 1)
INSERT INTO challenges (challengerid, accepterid, gameid, challengeid, cha_time, outcome)
VALUES (1, 2, 1, 1, NOW(), 'Pending');

-- Resolve a challenge (Challenger Wins)
UPDATE challenges
SET outcome = 'Win'
WHERE challengeid = 1;

-- Update all scores
CREATE TRIGGER challenge_end
AFTER UPDATE ON challenges
For Each Row
Begin
    DECLARE num_wins integer;
    DECLARE num_tot integer;
	SET num_wins = SELECT COUNT(*) FROM challenges 
				WHERE (challengerid=New.challengerid AND outcome='Win') 
				OR (accepterid=New.challengerid AND outcome='Lose')；
	SET num_tot = SELECT COUNT(*) FROM challenges 
				WHERE (challengerid=New.challengerid) 
				OR (accepterid=New.challengerid)；
	UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.challgerid;
	SET num_wins = SELECT COUNT(*) FROM challenges 
				WHERE (challengerid=New.accepterid AND outcome='Win') 
				OR (accepterid=New.accepterid AND outcome='Lose')；
	SET num_tot = SELECT COUNT(*) FROM challenges 
				WHERE (challengerid=New.accepterid) 
				OR (accepterid=New.accepterid)；
	UPDATE player SET score=num_win/num_tot*10.0 WHERE playerid=New.accepterid;	
End;

-- Comment on a player page (player 1 comments on player 2)
INSERT INTO comments (commenterid, receiverid, comment_content, comment_time)
VALUES (1, 2, 'You are awsome!', NOW())

-- Change Comments
UPDATE comments
SET comment_content = 'YOU SUCKS!'
WHERE (commenterid=1 AND receiverid=2);

-- DELETE COMMENTS
DELETE
FROM comments
WHERE (commenterid=1 AND receiverid=2);

-- Player search for game HearthStone
SELECT * FROM game WHERE title='HearthStone'

