CREATE TABLE "er_job" (
  "unique_id" varchar PRIMARY KEY,
  "data_role" varchar,
  "company_id" integer,
  "salary" varchar,
  "job_description" varchar,
  "job_types" TEXT[],
  "degree" TEXT[],
  "majors" TEXT[],
  "experience" varchar,
  "tools" TEXT[],
  "others" varchar,
  "url" varchar,
  "crawl_date" timestamp
);

CREATE TABLE "er_company" (
  "company_id" integer PRIMARY KEY,
  "company_name" varchar
);

CREATE TABLE "er_company_location" (
  "company_id" integer,
  "company_name" varchar,
  "county_id" integer,
  "district_id" integer
);

CREATE TABLE "er_county" (
  "county_id" integer PRIMARY KEY,
  "county_name_ch" varchar,
  "county_name_eng" varchar
);

CREATE TABLE "er_district" (
  "district_id" integer PRIMARY KEY,
  "district_name_ch" varchar,
  "district_name_eng" varchar,
  "county" integer
);

CREATE TABLE "er_tools" (
  "tool_id" integer PRIMARY KEY,
  "tool" varchar
);

CREATE TABLE "er_major" (
  "major_id" integer PRIMARY KEY,
  "major" varchar
);

CREATE TABLE "er_job_type" (
  "job_type_id" integer PRIMARY KEY,
  "job_type" varchar
);

CREATE TABLE "er_degree" (
  "degree_id" integer PRIMARY KEY,
  "degree" varchar
);

COMMENT ON COLUMN "er_job"."job_types" IS 'array of job types';

COMMENT ON COLUMN "er_job"."degree" IS 'array of degrees';

COMMENT ON COLUMN "er_job"."majors" IS 'arrary of majors';

COMMENT ON COLUMN "er_job"."tools" IS 'arrary of tools';

ALTER TABLE "er_job" ADD FOREIGN KEY ("company_id") REFERENCES "er_company" ("company_id");

CREATE TABLE "er_job_type_er_job" (
  "er_job_type_job_type_id" integer,
  "er_job_job_types" TEXT[],
  PRIMARY KEY ("er_job_type_job_type_id", "er_job_job_types")
);

ALTER TABLE "er_job_type_er_job" ADD FOREIGN KEY ("er_job_type_job_type_id") REFERENCES "er_job_type" ("job_type_id");

ALTER TABLE "er_job_type_er_job" ADD FOREIGN KEY ("er_job_job_types") REFERENCES "er_job" ("job_types");


CREATE TABLE "er_degree_er_job" (
  "er_degree_degree_id" integer,
  "er_job_degree" TEXT[],
  PRIMARY KEY ("er_degree_degree_id", "er_job_degree")
);

ALTER TABLE "er_degree_er_job" ADD FOREIGN KEY ("er_degree_degree_id") REFERENCES "er_degree" ("degree_id");

ALTER TABLE "er_degree_er_job" ADD FOREIGN KEY ("er_job_degree") REFERENCES "er_job" ("degree");


CREATE TABLE "er_major_er_job" (
  "er_major_major_id" integer,
  "er_job_majors" TEXT[],
  PRIMARY KEY ("er_major_major_id", "er_job_majors")
);

ALTER TABLE "er_major_er_job" ADD FOREIGN KEY ("er_major_major_id") REFERENCES "er_major" ("major_id");

ALTER TABLE "er_major_er_job" ADD FOREIGN KEY ("er_job_majors") REFERENCES "er_job" ("majors");


CREATE TABLE "er_tools_er_job" (
  "er_tools_tool_id" integer,
  "er_job_tools" TEXT[],
  PRIMARY KEY ("er_tools_tool_id", "er_job_tools")
);

ALTER TABLE "er_tools_er_job" ADD FOREIGN KEY ("er_tools_tool_id") REFERENCES "er_tools" ("tool_id");

ALTER TABLE "er_tools_er_job" ADD FOREIGN KEY ("er_job_tools") REFERENCES "er_job" ("tools");


ALTER TABLE "er_company_location" ADD FOREIGN KEY ("company_id") REFERENCES "er_company" ("company_id");

ALTER TABLE "er_company_location" ADD FOREIGN KEY ("county_id") REFERENCES "er_county" ("county_id");

ALTER TABLE "er_company_location" ADD FOREIGN KEY ("district_id") REFERENCES "er_district" ("district_id");

ALTER TABLE "er_district" ADD FOREIGN KEY ("county") REFERENCES "er_county" ("county_id");
