BEGIN;
CREATE TABLE "tastyapi_groupextra" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL UNIQUE REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    "group_type" varchar(10) NOT NULL,
    "owner_id" integer REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "tastyapi_groupaccess" (
    "id" serial NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED,
    "read_access" boolean NOT NULL,
    "write_access" boolean NOT NULL,
    "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
    "object_id" integer CHECK ("object_id" >= 0) NOT NULL,
    UNIQUE ("group_id", "content_type_id", "object_id")
)
;
CREATE TABLE "users" (
    "user_id" integer NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "name" varchar(100) NOT NULL,
    "email" varchar(255) NOT NULL UNIQUE,
    "password" text NOT NULL,
    "address" varchar(200) NOT NULL,
    "city" varchar(50) NOT NULL,
    "province" varchar(100) NOT NULL,
    "country" varchar(100) NOT NULL,
    "postal_code" varchar(15) NOT NULL,
    "institution" varchar(300) NOT NULL,
    "reference_email" varchar(255) NOT NULL,
    "confirmation_code" varchar(32) NOT NULL,
    "enabled" varchar(1) NOT NULL,
    "role_id" smallint,
    "contributor_code" varchar(32) NOT NULL,
    "contributor_enabled" varchar(1) NOT NULL,
    "professional_url" varchar(255) NOT NULL,
    "research_interests" varchar(1024) NOT NULL,
    "request_contributor" varchar(1) NOT NULL,
    "django_user_id" integer UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "users_roles" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "role_id" smallint NOT NULL
)
;
CREATE TABLE "image_type" (
    "image_type_id" smallint NOT NULL PRIMARY KEY,
    "image_type" varchar(100) NOT NULL UNIQUE,
    "abbreviation" varchar(10) NOT NULL UNIQUE,
    "comments" varchar(250) NOT NULL
)
;
CREATE TABLE "georeference" (
    "georef_id" bigint NOT NULL PRIMARY KEY,
    "title" text NOT NULL,
    "first_author" text NOT NULL,
    "second_authors" text NOT NULL,
    "journal_name" text NOT NULL,
    "full_text" text NOT NULL,
    "reference_number" text NOT NULL,
    "reference_id" bigint,
    "journal_name_2" text NOT NULL,
    "doi" text NOT NULL,
    "publication_year" text NOT NULL
)
;
CREATE TABLE "image_format" (
    "image_format_id" smallint NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "metamorphic_grades" (
    "metamorphic_grade_id" smallint NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "metamorphic_regions" (
    "metamorphic_region_id" bigint NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL UNIQUE,
    "description" text NOT NULL
)
;
CREATE TABLE "mineral_types" (
    "mineral_type_id" smallint NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL
)
;
CREATE TABLE "minerals" (
    "mineral_id" smallint NOT NULL PRIMARY KEY,
    "real_mineral_id" smallint NOT NULL,
    "name" varchar(100) NOT NULL UNIQUE
)
;
ALTER TABLE "minerals" ADD CONSTRAINT "real_mineral_id_refs_mineral_id_f080b59b" FOREIGN KEY ("real_mineral_id") REFERENCES "minerals" ("mineral_id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "reference" (
    "reference_id" bigint NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "regions" (
    "region_id" smallint NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "rock_type" (
    "rock_type_id" smallint NOT NULL PRIMARY KEY,
    "rock_type" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "roles" (
    "role_id" smallint NOT NULL PRIMARY KEY,
    "role_name" varchar(50) NOT NULL,
    "rank" smallint
)
;
CREATE TABLE "spatial_ref_sys" (
    "srid" integer NOT NULL PRIMARY KEY,
    "auth_name" varchar(256) NOT NULL,
    "auth_srid" integer,
    "srtext" varchar(2048) NOT NULL,
    "proj4text" varchar(2048) NOT NULL
)
;
CREATE TABLE "subsample_type" (
    "subsample_type_id" smallint NOT NULL PRIMARY KEY,
    "subsample_type" varchar(100) NOT NULL UNIQUE
)
;
CREATE TABLE "admin_users" (
    "admin_id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "elements" (
    "element_id" smallint NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL UNIQUE,
    "alternate_name" varchar(100) NOT NULL,
    "symbol" varchar(4) NOT NULL UNIQUE,
    "atomic_number" integer NOT NULL,
    "weight" double precision,
    "order_id" integer
)
;
CREATE TABLE "element_mineral_types" (
    "element_id" smallint NOT NULL REFERENCES "elements" ("element_id") DEFERRABLE INITIALLY DEFERRED,
    "mineral_type_id" smallint NOT NULL REFERENCES "mineral_types" ("mineral_type_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "image_reference" (
    "image_id" bigint NOT NULL,
    "reference_id" bigint NOT NULL REFERENCES "reference" ("reference_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "oxides" (
    "oxide_id" smallint NOT NULL PRIMARY KEY,
    "element_id" smallint NOT NULL REFERENCES "elements" ("element_id") DEFERRABLE INITIALLY DEFERRED,
    "oxidation_state" smallint,
    "species" varchar(20) NOT NULL UNIQUE,
    "weight" double precision,
    "cations_per_oxide" smallint,
    "conversion_factor" double precision NOT NULL,
    "order_id" integer
)
;
CREATE TABLE "oxide_mineral_types" (
    "oxide_id" smallint NOT NULL REFERENCES "oxides" ("oxide_id") DEFERRABLE INITIALLY DEFERRED,
    "mineral_type_id" smallint NOT NULL REFERENCES "mineral_types" ("mineral_type_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "projects" (
    "project_id" integer NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL,
    "description" varchar(300) NOT NULL,
    "isactive" varchar(1) NOT NULL
)
;
CREATE TABLE "samples" (
    "sample_id" bigint NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "sesar_number" varchar(9) NOT NULL,
    "public_data" varchar(1) NOT NULL,
    "collection_date" timestamp with time zone,
    "date_precision" smallint,
    "number" varchar(35) NOT NULL,
    "rock_type_id" smallint NOT NULL REFERENCES "rock_type" ("rock_type_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "location_error" double precision,
    "country" varchar(100) NOT NULL,
    "description" text NOT NULL,
    "location_text" varchar(50) NOT NULL
)
;
CREATE TABLE "sample_metamorphic_grades" (
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "metamorphic_grade_id" smallint NOT NULL REFERENCES "metamorphic_grades" ("metamorphic_grade_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY,
    UNIQUE ("sample_id", "metamorphic_grade_id")
)
;
CREATE TABLE "sample_metamorphic_regions" (
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "metamorphic_region_id" bigint NOT NULL REFERENCES "metamorphic_regions" ("metamorphic_region_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY,
    UNIQUE ("sample_id", "metamorphic_region_id")
)
;
CREATE TABLE "sample_minerals" (
    "mineral_id" smallint NOT NULL REFERENCES "minerals" ("mineral_id") DEFERRABLE INITIALLY DEFERRED,
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "amount" varchar(30) NOT NULL,
    "id" integer NOT NULL PRIMARY KEY,
    UNIQUE ("mineral_id", "sample_id")
)
;
CREATE TABLE "sample_reference" (
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "reference_id" bigint NOT NULL REFERENCES "reference" ("reference_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY,
    UNIQUE ("sample_id", "reference_id")
)
;
CREATE TABLE "sample_regions" (
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "region_id" smallint NOT NULL REFERENCES "regions" ("region_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY,
    UNIQUE ("sample_id", "region_id")
)
;
CREATE TABLE "sample_aliases" (
    "sample_alias_id" bigint NOT NULL PRIMARY KEY,
    "sample_id" bigint REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "alias" varchar(35) NOT NULL,
    UNIQUE ("sample_id", "alias")
)
;
CREATE TABLE "subsamples" (
    "subsample_id" bigint NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "public_data" varchar(1) NOT NULL,
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "grid_id" bigint,
    "name" varchar(100) NOT NULL,
    "subsample_type_id" smallint NOT NULL REFERENCES "subsample_type" ("subsample_type_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "grids" (
    "grid_id" bigint NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "subsample_id" bigint NOT NULL REFERENCES "subsamples" ("subsample_id") DEFERRABLE INITIALLY DEFERRED,
    "width" smallint NOT NULL,
    "height" smallint NOT NULL,
    "public_data" varchar(1) NOT NULL
)
;
CREATE TABLE "chemical_analyses" (
    "chemical_analysis_id" bigint NOT NULL PRIMARY KEY,
    "version" integer NOT NULL,
    "subsample_id" bigint NOT NULL REFERENCES "subsamples" ("subsample_id") DEFERRABLE INITIALLY DEFERRED,
    "public_data" varchar(1) NOT NULL,
    "reference_x" double precision,
    "reference_y" double precision,
    "stage_x" double precision,
    "stage_y" double precision,
    "image_id" bigint,
    "analysis_method" varchar(50) NOT NULL,
    "where_done" varchar(50) NOT NULL,
    "analyst" varchar(50) NOT NULL,
    "analysis_date" timestamp with time zone,
    "date_precision" smallint,
    "reference_id" bigint REFERENCES "reference" ("reference_id") DEFERRABLE INITIALLY DEFERRED,
    "description" varchar(1024) NOT NULL,
    "mineral_id" smallint REFERENCES "minerals" ("mineral_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "large_rock" varchar(1) NOT NULL,
    "total" double precision,
    "spot_id" bigint NOT NULL
)
;
CREATE TABLE "chemical_analysis_elements" (
    "chemical_analysis_id" bigint NOT NULL REFERENCES "chemical_analyses" ("chemical_analysis_id") DEFERRABLE INITIALLY DEFERRED,
    "element_id" smallint NOT NULL REFERENCES "elements" ("element_id") DEFERRABLE INITIALLY DEFERRED,
    "amount" double precision NOT NULL,
    "precision" double precision,
    "precision_type" varchar(3) NOT NULL,
    "measurement_unit" varchar(4) NOT NULL,
    "min_amount" double precision,
    "max_amount" double precision,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "chemical_analysis_oxides" (
    "chemical_analysis_id" bigint NOT NULL REFERENCES "chemical_analyses" ("chemical_analysis_id") DEFERRABLE INITIALLY DEFERRED,
    "oxide_id" smallint NOT NULL REFERENCES "oxides" ("oxide_id") DEFERRABLE INITIALLY DEFERRED,
    "amount" double precision NOT NULL,
    "precision" double precision,
    "precision_type" varchar(3) NOT NULL,
    "measurement_unit" varchar(4) NOT NULL,
    "min_amount" double precision,
    "max_amount" double precision,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "images" (
    "image_id" bigint NOT NULL PRIMARY KEY,
    "checksum" varchar(50) NOT NULL,
    "version" integer NOT NULL,
    "sample_id" bigint REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "subsample_id" bigint REFERENCES "subsamples" ("subsample_id") DEFERRABLE INITIALLY DEFERRED,
    "image_format_id" smallint REFERENCES "image_format" ("image_format_id") DEFERRABLE INITIALLY DEFERRED,
    "image_type_id" smallint NOT NULL REFERENCES "image_type" ("image_type_id") DEFERRABLE INITIALLY DEFERRED,
    "width" smallint NOT NULL,
    "height" smallint NOT NULL,
    "collector" varchar(50) NOT NULL,
    "description" varchar(1024) NOT NULL,
    "scale" smallint,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "public_data" varchar(1) NOT NULL,
    "checksum_64x64" varchar(50) NOT NULL,
    "checksum_half" varchar(50) NOT NULL,
    "filename" varchar(256) NOT NULL,
    "checksum_mobile" varchar(50) NOT NULL
)
;
ALTER TABLE "image_reference" ADD CONSTRAINT "image_id_refs_image_id_c68ced23" FOREIGN KEY ("image_id") REFERENCES "images" ("image_id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "chemical_analyses" ADD CONSTRAINT "image_id_refs_image_id_ab7c019f" FOREIGN KEY ("image_id") REFERENCES "images" ("image_id") DEFERRABLE INITIALLY DEFERRED;
CREATE TABLE "image_comments" (
    "comment_id" bigint NOT NULL PRIMARY KEY,
    "image_id" bigint NOT NULL REFERENCES "images" ("image_id") DEFERRABLE INITIALLY DEFERRED,
    "comment_text" text NOT NULL,
    "version" integer NOT NULL
)
;
CREATE TABLE "image_on_grid" (
    "image_on_grid_id" bigint NOT NULL PRIMARY KEY,
    "grid_id" bigint NOT NULL REFERENCES "grids" ("grid_id") DEFERRABLE INITIALLY DEFERRED,
    "image_id" bigint NOT NULL REFERENCES "images" ("image_id") DEFERRABLE INITIALLY DEFERRED,
    "top_left_x" double precision NOT NULL,
    "top_left_y" double precision NOT NULL,
    "z_order" smallint NOT NULL,
    "opacity" smallint NOT NULL,
    "resize_ratio" double precision NOT NULL,
    "width" smallint NOT NULL,
    "height" smallint NOT NULL,
    "checksum" varchar(50) NOT NULL,
    "checksum_64x64" varchar(50) NOT NULL,
    "checksum_half" varchar(50) NOT NULL,
    "locked" varchar(1) NOT NULL,
    "angle" double precision
)
;
CREATE TABLE "project_invites" (
    "invite_id" integer NOT NULL PRIMARY KEY,
    "project_id" integer NOT NULL REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "action_timestamp" timestamp with time zone NOT NULL,
    "status" varchar(32) NOT NULL
)
;
CREATE TABLE "project_members" (
    "project_id" integer NOT NULL REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "project_samples" (
    "project_id" integer NOT NULL REFERENCES "projects" ("project_id") DEFERRABLE INITIALLY DEFERRED,
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "id" integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE "sample_comments" (
    "comment_id" bigint NOT NULL PRIMARY KEY,
    "sample_id" bigint NOT NULL REFERENCES "samples" ("sample_id") DEFERRABLE INITIALLY DEFERRED,
    "user_id" integer NOT NULL REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED,
    "comment_text" text NOT NULL,
    "date_added" timestamp with time zone
)
;
CREATE TABLE "uploaded_files" (
    "uploaded_file_id" bigint NOT NULL PRIMARY KEY,
    "hash" varchar(50) NOT NULL,
    "filename" varchar(255) NOT NULL,
    "time" timestamp with time zone NOT NULL,
    "user_id" integer REFERENCES "users" ("user_id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "xray_image" (
    "image_id" bigint NOT NULL PRIMARY KEY REFERENCES "images" ("image_id") DEFERRABLE INITIALLY DEFERRED,
    "element" varchar(256) NOT NULL,
    "dwelltime" smallint,
    "current" smallint,
    "voltage" smallint
)
;
CREATE INDEX "tastyapi_groupextra_owner_id" ON "tastyapi_groupextra" ("owner_id");
CREATE INDEX "tastyapi_groupaccess_group_id" ON "tastyapi_groupaccess" ("group_id");
CREATE INDEX "tastyapi_groupaccess_content_type_id" ON "tastyapi_groupaccess" ("content_type_id");
SELECT AddGeometryColumn('metamorphic_regions', 'shape', 4326, 'POLYGON', 2);
CREATE INDEX "metamorphic_regions_shape_id" ON "metamorphic_regions" USING GIST ( "shape" );
SELECT AddGeometryColumn('metamorphic_regions', 'label_location', 4326, 'POINT', 2);
CREATE INDEX "metamorphic_regions_label_location_id" ON "metamorphic_regions" USING GIST ( "label_location" );
CREATE INDEX "minerals_real_mineral_id" ON "minerals" ("real_mineral_id");
CREATE INDEX "admin_users_user_id" ON "admin_users" ("user_id");
CREATE INDEX "element_mineral_types_element_id" ON "element_mineral_types" ("element_id");
CREATE INDEX "element_mineral_types_mineral_type_id" ON "element_mineral_types" ("mineral_type_id");
CREATE INDEX "image_reference_image_id" ON "image_reference" ("image_id");
CREATE INDEX "image_reference_reference_id" ON "image_reference" ("reference_id");
CREATE INDEX "oxides_element_id" ON "oxides" ("element_id");
CREATE INDEX "oxide_mineral_types_oxide_id" ON "oxide_mineral_types" ("oxide_id");
CREATE INDEX "oxide_mineral_types_mineral_type_id" ON "oxide_mineral_types" ("mineral_type_id");
CREATE INDEX "projects_user_id" ON "projects" ("user_id");
CREATE INDEX "samples_rock_type_id" ON "samples" ("rock_type_id");
CREATE INDEX "samples_user_id" ON "samples" ("user_id");
SELECT AddGeometryColumn('samples', 'location', 4326, 'POINT', 2);
ALTER TABLE "samples" ALTER "location" SET NOT NULL;
CREATE INDEX "samples_location_id" ON "samples" USING GIST ( "location" );
CREATE INDEX "sample_metamorphic_grades_sample_id" ON "sample_metamorphic_grades" ("sample_id");
CREATE INDEX "sample_metamorphic_grades_metamorphic_grade_id" ON "sample_metamorphic_grades" ("metamorphic_grade_id");
CREATE INDEX "sample_metamorphic_regions_sample_id" ON "sample_metamorphic_regions" ("sample_id");
CREATE INDEX "sample_metamorphic_regions_metamorphic_region_id" ON "sample_metamorphic_regions" ("metamorphic_region_id");
CREATE INDEX "sample_minerals_mineral_id" ON "sample_minerals" ("mineral_id");
CREATE INDEX "sample_minerals_sample_id" ON "sample_minerals" ("sample_id");
CREATE INDEX "sample_reference_sample_id" ON "sample_reference" ("sample_id");
CREATE INDEX "sample_reference_reference_id" ON "sample_reference" ("reference_id");
CREATE INDEX "sample_regions_sample_id" ON "sample_regions" ("sample_id");
CREATE INDEX "sample_regions_region_id" ON "sample_regions" ("region_id");
CREATE INDEX "sample_aliases_sample_id" ON "sample_aliases" ("sample_id");
CREATE INDEX "subsamples_sample_id" ON "subsamples" ("sample_id");
CREATE INDEX "subsamples_user_id" ON "subsamples" ("user_id");
CREATE INDEX "subsamples_subsample_type_id" ON "subsamples" ("subsample_type_id");
CREATE INDEX "grids_subsample_id" ON "grids" ("subsample_id");
CREATE INDEX "chemical_analyses_subsample_id" ON "chemical_analyses" ("subsample_id");
CREATE INDEX "chemical_analyses_image_id" ON "chemical_analyses" ("image_id");
CREATE INDEX "chemical_analyses_reference_id" ON "chemical_analyses" ("reference_id");
CREATE INDEX "chemical_analyses_mineral_id" ON "chemical_analyses" ("mineral_id");
CREATE INDEX "chemical_analyses_user_id" ON "chemical_analyses" ("user_id");
CREATE INDEX "chemical_analysis_elements_chemical_analysis_id" ON "chemical_analysis_elements" ("chemical_analysis_id");
CREATE INDEX "chemical_analysis_elements_element_id" ON "chemical_analysis_elements" ("element_id");
CREATE INDEX "chemical_analysis_oxides_chemical_analysis_id" ON "chemical_analysis_oxides" ("chemical_analysis_id");
CREATE INDEX "chemical_analysis_oxides_oxide_id" ON "chemical_analysis_oxides" ("oxide_id");
CREATE INDEX "images_sample_id" ON "images" ("sample_id");
CREATE INDEX "images_subsample_id" ON "images" ("subsample_id");
CREATE INDEX "images_image_format_id" ON "images" ("image_format_id");
CREATE INDEX "images_image_type_id" ON "images" ("image_type_id");
CREATE INDEX "images_user_id" ON "images" ("user_id");
CREATE INDEX "image_comments_image_id" ON "image_comments" ("image_id");
CREATE INDEX "image_on_grid_grid_id" ON "image_on_grid" ("grid_id");
CREATE INDEX "image_on_grid_image_id" ON "image_on_grid" ("image_id");
CREATE INDEX "project_invites_project_id" ON "project_invites" ("project_id");
CREATE INDEX "project_invites_user_id" ON "project_invites" ("user_id");
CREATE INDEX "project_members_project_id" ON "project_members" ("project_id");
CREATE INDEX "project_members_user_id" ON "project_members" ("user_id");
CREATE INDEX "project_samples_project_id" ON "project_samples" ("project_id");
CREATE INDEX "project_samples_sample_id" ON "project_samples" ("sample_id");
CREATE INDEX "sample_comments_sample_id" ON "sample_comments" ("sample_id");
CREATE INDEX "sample_comments_user_id" ON "sample_comments" ("user_id");
CREATE INDEX "uploaded_files_user_id" ON "uploaded_files" ("user_id");
COMMIT;
