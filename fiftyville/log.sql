-- Find the crime scene report
SELECT * FROM crime_scene_reports
WHERE year = 2025 AND month = 7 AND day = 28
AND street = 'Humphrey Street';

-- Find interviews from the day of the theft
SELECT * FROM interviews
WHERE year = 2025 AND month = 7 AND day = 28;

-- Find the thief
SELECT * FROM people
WHERE name = 'Bruce';

-- Find the escape city
SELECT * FROM airports
WHERE city = 'New York City';

-- Find the accomplice
SELECT * FROM people
WHERE name = 'Robin';
