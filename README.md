# Data-Job-Vacancy-Insight
A system that recommends data-centric jobs and provides insights, featuring a personalized job report service delivered through a Telegram bot.

## Authors 
- [@IsaacLee0904](https://github.com/IsaacLee0904)

## Timeline
- **2024-03-25:** Project workflow design
- **2024-03-26:** Set up development environment with Docker
- **2024-03-28 to 2024-03-31:** Development of 104 crawler
- **2024-03-31:** Database design
- **2024-04-01 to 2024-04-02:** Data pipeline - Load raw data into the data warehouse (source_data layer)
- **2024-04-08 to 2024-04-09:** Data pipeline - Transform data in the data warehouse (staging_data layer)
- **2024-04-09 to 2024-04-10:** Set up DBT (Data Build Tool)
- **2024-04-12 to 2024-04-19:** Data pipeline - Transform data into the data warehouse (modeling_data layer) with dbt
    - ER model build up in modeling_data layer with dbt model feature
    - ER model tables data quality check setup with dbt test feature
    - Data warehouse modeling_data layer graph (http://localhost:80)
    - Data warehouse modeling_data layer change data capture(CDC) setup with dbt snapshot feature (non-finished)
- Data pipeline deploy with airflow (to-do)
    - 104 crawler
    - Data pipeline - load raw data
    - Data pipeline - transform data
    - Data pipeline - ER modeling 
    - Data quality check 
    - Change data capture

## Project Overview
The "Data-Job-Vacancy-Insight" project is designed to streamline the job searching process for data professionals. By aggregating and analyzing job listings from multiple sources, it offers personalized job recommendations and valuable market insights directly through a user-friendly Telegram bot interface.

## Features
- **Job Recommendations:** Tailored suggestions based on user's skills and preferences.
- **Market Insights:** Analysis of current job market trends within the data field.
- **User Profiles:** Customizable profiles that enhance job matching accuracy.
- **Automated Reports:** Regular updates and reports delivered through Telegram.

## Repository structure
```
├── Config
│   └── database_config.toml
├── Docker-compose.yml
├── Dockerfile
├── README.md
├── assets
│   ├── dbt_entity_relationship_initialize
│   │   ├── initialize_er_company.sql
│   │   ├── initialize_er_job_type.sql
│   │   ├── initialize_er_major.sql
│   │   └── initialize_er_tools.sql
│   └── entity_relationship_model
│       ├── job_vacancy_insight_datawarehouse_entity_relationship.png
│       └── job_vacancy_insight_datawarehouse_entity_relationship.sql
├── data
│   ├── backup
│   │   ├── jobs_20240401_065532.json
│   │   ├── jobs_20240408_135846.json
│   │   └── jobs_20240415_012649.json
│   ├── database
│   └── raw_data
├── dbt
│   ├── dbt_packages
│   │   └── dbt_utils
│   │       ├── CHANGELOG.md
│   │       ├── CONTRIBUTING.md
│   │       ├── LICENSE
│   │       ├── Makefile
│   │       ├── README.md
│   │       ├── RELEASE.md
│   │       ├── dbt_project.yml
│   │       ├── dev-requirements.txt
│   │       ├── docker-compose.yml
│   │       ├── docs
│   │       │   └── decisions
│   │       │       ├── README.md
│   │       │       ├── adr-0000-documenting-architecture-decisions.md
│   │       │       ├── adr-0001-decision-record-format.md
│   │       │       └── adr-0002-cross-database-utils.md
│   │       ├── etc
│   │       │   └── dbt-logo.png
│   │       ├── integration_tests
│   │       │   ├── README.md
│   │       │   ├── ci
│   │       │   │   └── sample.profiles.yml
│   │       │   ├── data
│   │       │   │   ├── datetime
│   │       │   │   │   └── data_date_spine.csv
│   │       │   │   ├── etc
│   │       │   │   │   └── data_people.csv
│   │       │   │   ├── geo
│   │       │   │   │   ├── data_haversine_km.csv
│   │       │   │   │   └── data_haversine_mi.csv
│   │       │   │   ├── schema_tests
│   │       │   │   │   ├── data_cardinality_equality_a.csv
│   │       │   │   │   ├── data_cardinality_equality_b.csv
│   │       │   │   │   ├── data_not_null_proportion.csv
│   │       │   │   │   ├── data_test_accepted_range.csv
│   │       │   │   │   ├── data_test_at_least_one.csv
│   │       │   │   │   ├── data_test_equal_rowcount.csv
│   │       │   │   │   ├── data_test_expression_is_true.csv
│   │       │   │   │   ├── data_test_fewer_rows_than_table_1.csv
│   │       │   │   │   ├── data_test_fewer_rows_than_table_2.csv
│   │       │   │   │   ├── data_test_mutually_exclusive_ranges_no_gaps.csv
│   │       │   │   │   ├── data_test_mutually_exclusive_ranges_with_gaps.csv
│   │       │   │   │   ├── data_test_mutually_exclusive_ranges_with_gaps_zero_length.csv
│   │       │   │   │   ├── data_test_not_accepted_values.csv
│   │       │   │   │   ├── data_test_not_constant.csv
│   │       │   │   │   ├── data_test_relationships_where_table_1.csv
│   │       │   │   │   ├── data_test_relationships_where_table_2.csv
│   │       │   │   │   ├── data_test_sequential_timestamps.csv
│   │       │   │   │   ├── data_test_sequential_values.csv
│   │       │   │   │   ├── data_unique_combination_of_columns.csv
│   │       │   │   │   └── schema.yml
│   │       │   │   ├── sql
│   │       │   │   │   ├── data_deduplicate.csv
│   │       │   │   │   ├── data_deduplicate_expected.csv
│   │       │   │   │   ├── data_events_20180101.csv
│   │       │   │   │   ├── data_events_20180102.csv
│   │       │   │   │   ├── data_events_20180103.csv
│   │       │   │   │   ├── data_filtered_columns_in_relation.csv
│   │       │   │   │   ├── data_filtered_columns_in_relation_expected.csv
│   │       │   │   │   ├── data_generate_series.csv
│   │       │   │   │   ├── data_generate_surrogate_key.csv
│   │       │   │   │   ├── data_get_column_values.csv
│   │       │   │   │   ├── data_get_column_values_dropped.csv
│   │       │   │   │   ├── data_get_column_values_where.csv
│   │       │   │   │   ├── data_get_column_values_where_expected.csv
│   │       │   │   │   ├── data_get_query_results_as_dict.csv
│   │       │   │   │   ├── data_get_single_value.csv
│   │       │   │   │   ├── data_nullcheck_table.csv
│   │       │   │   │   ├── data_pivot.csv
│   │       │   │   │   ├── data_pivot_expected.csv
│   │       │   │   │   ├── data_pivot_expected_apostrophe.csv
│   │       │   │   │   ├── data_safe_add.csv
│   │       │   │   │   ├── data_safe_divide.csv
│   │       │   │   │   ├── data_safe_divide_denominator_expressions.csv
│   │       │   │   │   ├── data_safe_divide_numerator_expressions.csv
│   │       │   │   │   ├── data_safe_subtract.csv
│   │       │   │   │   ├── data_star.csv
│   │       │   │   │   ├── data_star_aggregate.csv
│   │       │   │   │   ├── data_star_aggregate_expected.csv
│   │       │   │   │   ├── data_star_expected.csv
│   │       │   │   │   ├── data_star_prefix_suffix_expected.csv
│   │       │   │   │   ├── data_star_quote_identifiers.csv
│   │       │   │   │   ├── data_union_events_expected.csv
│   │       │   │   │   ├── data_union_exclude_expected.csv
│   │       │   │   │   ├── data_union_expected.csv
│   │       │   │   │   ├── data_union_table_1.csv
│   │       │   │   │   ├── data_union_table_2.csv
│   │       │   │   │   ├── data_unpivot.csv
│   │       │   │   │   ├── data_unpivot_bool.csv
│   │       │   │   │   ├── data_unpivot_bool_expected.csv
│   │       │   │   │   ├── data_unpivot_expected.csv
│   │       │   │   │   ├── data_unpivot_original_api_expected.csv
│   │       │   │   │   └── data_width_bucket.csv
│   │       │   │   └── web
│   │       │   │       ├── data_url_host.csv
│   │       │   │       ├── data_url_path.csv
│   │       │   │       └── data_urls.csv
│   │       │   ├── dbt_project.yml
│   │       │   ├── macros
│   │       │   │   ├── assert_equal_values.sql
│   │       │   │   ├── limit_zero.sql
│   │       │   │   └── tests.sql
│   │       │   ├── models
│   │       │   │   ├── datetime
│   │       │   │   │   ├── schema.yml
│   │       │   │   │   └── test_date_spine.sql
│   │       │   │   ├── generic_tests
│   │       │   │   │   ├── recency_time_excluded.sql
│   │       │   │   │   ├── recency_time_included.sql
│   │       │   │   │   ├── schema.yml
│   │       │   │   │   ├── test_equal_column_subset.sql
│   │       │   │   │   ├── test_equal_rowcount.sql
│   │       │   │   │   └── test_fewer_rows_than.sql
│   │       │   │   ├── geo
│   │       │   │   │   ├── schema.yml
│   │       │   │   │   ├── test_haversine_distance_km.sql
│   │       │   │   │   └── test_haversine_distance_mi.sql
│   │       │   │   ├── sql
│   │       │   │   │   ├── schema.yml
│   │       │   │   │   ├── test_deduplicate.sql
│   │       │   │   │   ├── test_generate_series.sql
│   │       │   │   │   ├── test_generate_surrogate_key.sql
│   │       │   │   │   ├── test_get_column_values.sql
│   │       │   │   │   ├── test_get_column_values_where.sql
│   │       │   │   │   ├── test_get_filtered_columns_in_relation.sql
│   │       │   │   │   ├── test_get_relations_by_pattern.sql
│   │       │   │   │   ├── test_get_relations_by_prefix_and_union.sql
│   │       │   │   │   ├── test_get_single_value.sql
│   │       │   │   │   ├── test_get_single_value_default.sql
│   │       │   │   │   ├── test_groupby.sql
│   │       │   │   │   ├── test_not_empty_string_failing.sql
│   │       │   │   │   ├── test_not_empty_string_passing.sql
│   │       │   │   │   ├── test_nullcheck_table.sql
│   │       │   │   │   ├── test_pivot.sql
│   │       │   │   │   ├── test_pivot_apostrophe.sql
│   │       │   │   │   ├── test_safe_add.sql
│   │       │   │   │   ├── test_safe_divide.sql
│   │       │   │   │   ├── test_safe_subtract.sql
│   │       │   │   │   ├── test_star.sql
│   │       │   │   │   ├── test_star_aggregate.sql
│   │       │   │   │   ├── test_star_no_columns.sql
│   │       │   │   │   ├── test_star_prefix_suffix.sql
│   │       │   │   │   ├── test_star_quote_identifiers.sql
│   │       │   │   │   ├── test_star_uppercase.sql
│   │       │   │   │   ├── test_union.sql
│   │       │   │   │   ├── test_union_base.sql
│   │       │   │   │   ├── test_union_exclude_base_lowercase.sql
│   │       │   │   │   ├── test_union_exclude_base_uppercase.sql
│   │       │   │   │   ├── test_union_exclude_lowercase.sql
│   │       │   │   │   ├── test_union_exclude_uppercase.sql
│   │       │   │   │   ├── test_union_no_source_column.sql
│   │       │   │   │   ├── test_union_where.sql
│   │       │   │   │   ├── test_union_where_base.sql
│   │       │   │   │   ├── test_unpivot.sql
│   │       │   │   │   ├── test_unpivot_bool.sql
│   │       │   │   │   └── test_width_bucket.sql
│   │       │   │   └── web
│   │       │   │       ├── schema.yml
│   │       │   │       ├── test_url_host.sql
│   │       │   │       ├── test_url_path.sql
│   │       │   │       └── test_urls.sql
│   │       │   ├── packages.yml
│   │       │   └── tests
│   │       │       ├── assert_get_query_results_as_dict_objects_equal.sql
│   │       │       ├── generic
│   │       │       │   └── expect_table_columns_to_match_set.sql
│   │       │       ├── jinja_helpers
│   │       │       │   ├── assert_pretty_output_msg_is_string.sql
│   │       │       │   ├── assert_pretty_time_is_string.sql
│   │       │       │   └── test_slugify.sql
│   │       │       └── sql
│   │       │           ├── test_get_column_values_use_default.sql
│   │       │           └── test_get_single_value_multiple_rows.sql
│   │       ├── macros
│   │       │   ├── generic_tests
│   │       │   │   ├── accepted_range.sql
│   │       │   │   ├── at_least_one.sql
│   │       │   │   ├── cardinality_equality.sql
│   │       │   │   ├── equal_rowcount.sql
│   │       │   │   ├── equality.sql
│   │       │   │   ├── expression_is_true.sql
│   │       │   │   ├── fewer_rows_than.sql
│   │       │   │   ├── mutually_exclusive_ranges.sql
│   │       │   │   ├── not_accepted_values.sql
│   │       │   │   ├── not_constant.sql
│   │       │   │   ├── not_empty_string.sql
│   │       │   │   ├── not_null_proportion.sql
│   │       │   │   ├── recency.sql
│   │       │   │   ├── relationships_where.sql
│   │       │   │   ├── sequential_values.sql
│   │       │   │   └── unique_combination_of_columns.sql
│   │       │   ├── jinja_helpers
│   │       │   │   ├── _is_ephemeral.sql
│   │       │   │   ├── _is_relation.sql
│   │       │   │   ├── log_info.sql
│   │       │   │   ├── pretty_log_format.sql
│   │       │   │   ├── pretty_time.sql
│   │       │   │   └── slugify.sql
│   │       │   ├── sql
│   │       │   │   ├── date_spine.sql
│   │       │   │   ├── deduplicate.sql
│   │       │   │   ├── generate_series.sql
│   │       │   │   ├── generate_surrogate_key.sql
│   │       │   │   ├── get_column_values.sql
│   │       │   │   ├── get_filtered_columns_in_relation.sql
│   │       │   │   ├── get_query_results_as_dict.sql
│   │       │   │   ├── get_relations_by_pattern.sql
│   │       │   │   ├── get_relations_by_prefix.sql
│   │       │   │   ├── get_single_value.sql
│   │       │   │   ├── get_table_types_sql.sql
│   │       │   │   ├── get_tables_by_pattern_sql.sql
│   │       │   │   ├── get_tables_by_prefix_sql.sql
│   │       │   │   ├── groupby.sql
│   │       │   │   ├── haversine_distance.sql
│   │       │   │   ├── nullcheck.sql
│   │       │   │   ├── nullcheck_table.sql
│   │       │   │   ├── pivot.sql
│   │       │   │   ├── safe_add.sql
│   │       │   │   ├── safe_divide.sql
│   │       │   │   ├── safe_subtract.sql
│   │       │   │   ├── star.sql
│   │       │   │   ├── surrogate_key.sql
│   │       │   │   ├── union.sql
│   │       │   │   ├── unpivot.sql
│   │       │   │   └── width_bucket.sql
│   │       │   └── web
│   │       │       ├── get_url_host.sql
│   │       │       ├── get_url_parameter.sql
│   │       │       └── get_url_path.sql
│   │       ├── pytest.ini
│   │       ├── run_functional_test.sh
│   │       ├── run_test.sh
│   │       └── tests
│   │           ├── __init__.py
│   │           └── conftest.py
│   ├── dbt_project.yml
│   ├── logs
│   │   └── dbt.log
│   ├── macros
│   │   └── er_function.sql
│   ├── models
│   │   ├── modeling_data
│   │   │   ├── er_company.sql
│   │   │   ├── er_company_location.sql
│   │   │   ├── er_degree.sql
│   │   │   ├── er_job.sql
│   │   │   ├── er_job_type.sql
│   │   │   ├── er_major.sql
│   │   │   └── er_tools.sql
│   │   ├── source_data
│   │   ├── sources.yml
│   │   └── staging_data
│   ├── packages.yml
│   ├── profiles.yml
│   ├── seeds
│   │   ├── er_county.csv
│   │   └── er_district.csv
│   ├── snapshots
│   ├── target
│   │   ├── catalog.json
│   │   ├── compiled
│   │   │   └── data_job_vacancy_insight
│   │   │       ├── models
│   │   │       │   ├── modeling_data
│   │   │       │   │   ├── company_mapping.sql
│   │   │       │   │   ├── company_renew.sql
│   │   │       │   │   ├── er_company.sql
│   │   │       │   │   ├── er_company_location.sql
│   │   │       │   │   ├── er_degree.sql
│   │   │       │   │   ├── er_job.sql
│   │   │       │   │   ├── er_job_type.sql
│   │   │       │   │   ├── er_major.sql
│   │   │       │   │   └── er_tools.sql
│   │   │       │   └── sources.yml
│   │   │       │       ├── source_accepted_values_modelin_0d99cd7dc5c0a3c9e395ed0e0f55e419.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_county_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_district_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_degree_degree_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_crawl_date.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_data_role.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_degree.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_job_types.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_majors.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_tools.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_type_job_type_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_unique_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_major_major_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_tools_tool_id.sql
│   │   │       │       ├── source_not_null_staging_data_job_listings_104_unique_col.sql
│   │   │       │       ├── source_relationships_modeling__70dd375e6610514bf7a3121aec4d0b6f.sql
│   │   │       │       ├── source_relationships_modeling__8649a20016bf99fa58d90366d3c6f6d3.sql
│   │   │       │       ├── source_relationships_modeling__973b7be24359dc3fca16951906791ded.sql
│   │   │       │       ├── source_relationships_modeling__d37dd2cc26789702258008cb472749f6.sql
│   │   │       │       ├── source_unique_modeling_data_er_company_company_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_degree_degree_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_job_type_job_type_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_job_unique_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_major_major_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_tools_tool_id.sql
│   │   │       │       └── source_unique_staging_data_job_listings_104_unique_col.sql
│   │   │       └── tests
│   │   │           └── er_job_crawl_date.sql
│   │   ├── graph.gpickle
│   │   ├── index.html
│   │   ├── manifest.json
│   │   ├── partial_parse.msgpack
│   │   ├── run
│   │   │   └── data_job_vacancy_insight
│   │   │       ├── models
│   │   │       │   ├── modeling_data
│   │   │       │   │   ├── company_mapping.sql
│   │   │       │   │   ├── company_renew.sql
│   │   │       │   │   ├── er_company.sql
│   │   │       │   │   ├── er_company_location.sql
│   │   │       │   │   ├── er_degree.sql
│   │   │       │   │   ├── er_job.sql
│   │   │       │   │   ├── er_job_type.sql
│   │   │       │   │   ├── er_major.sql
│   │   │       │   │   └── er_tools.sql
│   │   │       │   └── sources.yml
│   │   │       │       ├── source_not_null_modeling_data_er_company_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_county_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_company_location_district_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_degree_degree_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_company_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_crawl_date.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_degree.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_job_types.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_majors.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_tools.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_type_job_type_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_job_unique_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_major_major_id.sql
│   │   │       │       ├── source_not_null_modeling_data_er_tools_tool_id.sql
│   │   │       │       ├── source_not_null_staging_data_job_listings_104_unique_col.sql
│   │   │       │       ├── source_relationships_modeling__70dd375e6610514bf7a3121aec4d0b6f.sql
│   │   │       │       ├── source_relationships_modeling__8649a20016bf99fa58d90366d3c6f6d3.sql
│   │   │       │       ├── source_relationships_modeling__973b7be24359dc3fca16951906791ded.sql
│   │   │       │       ├── source_relationships_modeling__d37dd2cc26789702258008cb472749f6.sql
│   │   │       │       ├── source_unique_modeling_data_er_company_company_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_degree_degree_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_job_type_job_type_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_job_unique_id.sql
│   │   │       │       ├── source_unique_modeling_data_er_major_major_id.sql
│   │   │       │       └── source_unique_modeling_data_er_tools_tool_id.sql
│   │   │       └── seeds
│   │   │           ├── er_county.csv
│   │   │           ├── er_district.csv
│   │   │           └── initial_company.csv
│   │   └── run_results.json
│   └── tests
│       ├── er_job_crawl_date.sql
│       └── seeds_generic_test.yml
├── docs
├── logs
│   ├── 104_crawler.log
│   ├── dbt.log
│   ├── graylog_checker.log
│   ├── load_raw_data.log
│   ├── test.log
│   └── transform_raw_data.log
├── main.py
├── model
├── references
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── buildup_src
│   │   ├── database_connection_checker.py
│   │   ├── graylog_checker.py
│   │   └── package_checker.py
│   ├── crawler_src
│   │   └── 104_crawler.py
│   └── data_processing_src
│       ├── load_raw_data.py
│       └── transform_raw_data.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-38.pyc
    │   ├── crawler_utils.cpython-38.pyc
    │   ├── database_utils.cpython-38.pyc
    │   ├── etl_utils.cpython-38.pyc
    │   └── log_utils.cpython-38.pyc
    ├── crawler_utils.py
    ├── database_utils.py
    ├── etl_utils.py
    └── log_utils.py
```