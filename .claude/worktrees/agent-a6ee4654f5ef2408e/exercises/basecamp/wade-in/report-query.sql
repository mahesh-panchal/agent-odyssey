-- "What a model sent back" for: samples received per project, and open milestones.
SELECT p.name,
       COUNT(s.id) AS samples_received,
       COUNT(m.id) AS open_milestones
FROM projects p
JOIN samples s ON s.project_id = p.id
JOIN milestones m ON m.project_id = p.id
WHERE m.done = 0
GROUP BY p.name
ORDER BY p.name;
