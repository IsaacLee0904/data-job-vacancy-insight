SELECT crawl_date
FROM {{ref('er_job')}}
WHERE extract('dow' FROM crawl_date) != 1
