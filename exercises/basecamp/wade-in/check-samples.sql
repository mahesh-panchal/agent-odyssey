-- Your own check: samples per project, counted on their own.
SELECT p.name, COUNT(*) AS samples_received
FROM samples s JOIN projects p ON p.id = s.project_id
GROUP BY p.name ORDER BY p.name;
