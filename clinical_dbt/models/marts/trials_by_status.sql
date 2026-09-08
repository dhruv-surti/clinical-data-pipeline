SELECT status, COUNT(*) AS trial_count 
FROM {{ ref('stg_trials')}}
GROUP BY status
