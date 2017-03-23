CREATE TABLE patients_train
(
  patient_id integer PRIMARY KEY,
  patient_age_group character varying(5),
  patient_gender character varying(1),
  patient_state character varying(2),
  ethinicity character varying(20),
  household_income character varying(14),
  education_level character varying(30),
  is_screener integer
);
CREATE TABLE patients_test
(
  patient_id integer PRIMARY KEY,
  patient_age_group character varying(5),
  patient_gender character varying(1),
  patient_state character varying(2),
  ethinicity character varying(20),
  household_income character varying(14),
  education_level character varying(30)
);
CREATE TABLE diagnosis
(
  patient_id integer, --
  claim_id character varying(22),
  claim_type character varying(4),
  diagnosis_date character varying(6),
  diagnosis_code character varying(22),
  primary_practitioner_id integer,
  primary_physician_role character varying(4),
  CONSTRAINT "d.patient_id" FOREIGN KEY (patient_id)
      REFERENCES patients (patient_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
CREATE TABLE diagnosis_code
(
  diagnosis_code character varying(30) NOT NULL,
  diagnosis_description character varying(255),
  CONSTRAINT pk_diag_code PRIMARY KEY (diagnosis_code)
);

CREATE TABLE drug
(
  drug_id character varying(13) NOT NULL,
  "NDC11" character varying(11),
  drug_name character varying(60),
  "BGI" character varying(1),
  "BB_USC_code" character varying(5),
  "BB_USC_name" character varying(60),
  drug_generic_name character varying(60),
  drug_strength character varying(10),
  drug_form character varying(40),
  package_size numeric,
  package_description character varying(50),
  manufacturer character varying(15),
  "NDC_start_date" date,
  CONSTRAINT drug_pkey PRIMARY KEY (drug_id)
);

CREATE TABLE patient_activity
(
  patient_id integer,
  activity_type character varying(1),
  activity_year character varying(4),
  activity_month character varying(2)
);
CREATE TABLE physician
(
  physician_id integer,
  practitioner_id integer NOT NULL,
  state character varying(2),
  specialty_code character varying(3),
  specialty_description character varying(75),
  "CBSA" character varying(30),
  CONSTRAINT pk PRIMARY KEY (practitioner_id)
);
CREATE TABLE prescription
(
  claim_id character varying(22),
  patient_id integer,
  drug_id character varying(13),
  practitioner_id integer,
  refill_code character varying(2),
  days_supply integer,
  rx_fill_date date,
  rx_number character varying(32),
  payment_type character varying(60)
);
CREATE TABLE procedure
(
  patient_id integer,
  claim_id bigint,
  claim_line_item integer,
  claim_type character(2),
  procedure_code character(6),
  procedure_date character(6),
  place_of_service character(60),
  plan_type character(16),
  primary_practitioner_id integer,
  units_administered bigint,
  charge_amount numeric,
  primary_physician_role character varying(10),
  attending_practitioner_id integer,
  referring_practitioner_id integer,
  rendering_practitioner_id integer,
  ordering_practitioner_id integer,
  operating_practitioner_id integer
);
CREATE TABLE procedure_code
(
  procedure_code character varying(48) NOT NULL,
  procedure_description character varying(100),
  CONSTRAINT pc_pk PRIMARY KEY (procedure_code)
);

CREATE TABLE surgical
(
  patient_id integer,
  claim_id character varying(22),
  procedure_type_code character varying(4),
  claim_type character varying(4),
  surgical_code character varying(48),
  surgical_procedure_date character varying(6),
  place_of_service character varying(60),
  plan_type character varying(16),
  practitioner_id integer,
  primary_physician_role character(5)
);
CREATE TABLE surgical_code
(
  surgical_code character varying(48) NOT NULL,
  surgical_description character varying(100),
  CONSTRAINT surgical_code_pkey PRIMARY KEY (surgical_code)
);

CREATE INDEX patient_id_indx
  ON diagnosis (patient_id);
CREATE INDEX prescription_idx
  ON prescription (patient_id);
  
CREATE TABLE train_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);
CREATE TABLE test_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);
