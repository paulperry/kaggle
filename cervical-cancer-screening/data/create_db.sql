-- based on postgres
-- change dir to where the files are
\cd /Users/paulperry/Documents/kaggle-private/input
-- presumes that a database 'ccancer' is created'
-- \c ccancer;
set datestyle to 'dmy';
set client_encoding to latin1;

-- patient demographic information
drop table patient;
create table patient
(
patient_id numeric,
patient_age_group varchar(5), -- patient age in 3 year increments (18-20, 21-23, 24-26, etc.) 
patient_gender varchar(1), -- gender 
patient_state  varchar(2), -- state 
ethnicity      varchar(20), -- patient ethnicity, where available: caucasian, african american, hispanic, all other
household_income varchar(14), -- patient range of household income, where available: less than or equal to $49,999,  $50-99,999 ,  $100k +  and unknown) 
education_level varchar(20) -- patient highest education attained, where available: high school or less, some college,  “associate degree and above” and unknown 
);

drop table patient_activity;
create table patient_activity -- this table indicates the whether there was activity from that patient in a given month
(
patient_id numeric,
activity_type varchar(1),  -- values: a = all claims, r = retail claims only
activity_year varchar(4), -- year of database activity. 
activity_month varchar(2)
);

drop table rx;
create table rx
(
claim_id varchar(22),
patient_id numeric,
drug_id  varchar(13),
practitioner_id numeric,
refill_code varchar(2), -- 0 = new rx, else value = refill number 
days_supply numeric, 
rx_fill_date date,
rx_number varchar(32), -- encrypted rx script number 
payment_type varchar(60) null -- cash,commercial,medicare,medicaid,assistance,unknown
);

drop table drug;
create table drug
(
drug_id varchar(13) primary key, 
ndc11 varchar(11),
drug_name varchar(60),
bgi    varchar(1), -- brand generic indicator 
bb_usc_code varchar(5), -- blue book usc code 
bb_usc_name varchar(60), -- blue book usc name 
drug_generic_name varchar(60), 
drug_strength varchar(10),
drug_form varchar(40),
package_size numeric(11,3),
package_description varchar(20),
manufacturer varchar(15),
ndc_start_date date -- date ndc entered market
);
    
drop table physician;
create table physician
(
physician_id numeric, -- prc_rel_gid 
practitioner_id numeric primary key, -- ds writer gid (primary key) 
state  varchar(2),
specialty_code varchar(3),
specialty_description varchar(75),
cbsa  varchar(30) -- cbsa in which the physician is located 
);

drop table diagnosis;
create table diagnosis
(
patient_id numeric,
claim_id varchar(22),
claim_type varchar(4), 
diagnosis_date varchar(6),
diagnosis_code varchar(30),
primary_practitioner_id numeric, 
primary_physician_role varchar(4)
);

drop table diagnosis_code;
create table diagnosis_code
(
diagnosis_code varchar(30),
diagnosis_description varchar(255)
);
    
drop table procedure;
create table procedure
(
patient_id numeric,
claim_id numeric,
claim_line_item numeric,
claim_type varchar(22), -- claim type: hcfa/ub92 or mx/hx 
procedure_code varchar(248), 
procedure_date varchar(26), 
place_of_service varchar(260),
plan_type  varchar(216),
primary_practitioner_id numeric,
units_administered numeric,
charge_amount  numeric,
primary_physician_role varchar(210),
attending_practitioner_id numeric,
referring_practitioner_id numeric null,
rendering_practitioner_id numeric null,
ordering_practitioner_id numeric null,
operating_practitioner_id numeric 
);

drop table procedure_code;
create table procedure_code
(
procedure_code  varchar(48),
procedure_description varchar(100)
);

drop table surgical;
create table surgical
(
patient_id numeric,
claim_id   varchar(22),
procedure_type_code varchar(4),
claim_type  varchar(4),
surgical_code  varchar(48),
surgical_procedure_date varchar(6),
place_of_service varchar(60),
plan_type   varchar(16),
practitioner_id numeric,
primary_physician_role varchar(10)
);

drop table surgical_code;
create table surgical_code
(
surgical_code  varchar(48),
surgical_description varchar(100)
);

drop table patients_test;
create table patients_test
(
patient_id numeric,
patient_age_group varchar(5),
patient_gender varchar(1),
patient_state  varchar(2),
ethinicity     varchar(20),
household_income varchar(14),
education_level varchar(30)
);

drop table patients_train;
create table patients_train
(
patient_id numeric,
patient_age_group varchar(5),
patient_gender varchar(1),
patient_state  varchar(2),
ethinicity     varchar(20),
household_income varchar(14),
education_level varchar(30),
is_screener numeric
);

\copy diagnosis_code from diagnosis_code.csv null as 'NA' csv header
\copy drug           from drugs.csv null as 'NA' csv header
\copy physician      from physicians.csv null as 'NA' csv header
\copy procedure_code from procedure_code.csv null as 'NA' csv header
\copy surgical_code  from surgical_code.csv null as 'NA' csv header
\copy diagnosis      from diagnosis_head.csv null as 'NA' csv header
\copy patient_activity from patient_activity_head.csv csv header
\copy rx               from prescription_head.csv csv header 
\copy procedure from procedure_head.csv csv header 
\copy surgical from surgical_head.csv csv header
\copy patients_train from patients_train.csv csv header 
\copy patients_test from patients_test.csv csv header 


drop index train_patient_idx;
create unique index train_patient_idx on patients_train (patient_id);
drop index test_patient_idx;
create unique index test_patient_idx on patients_test (patient_id);

create index diag_patient_idx on diagnosis (patient_id);
create index diag_code_idx on diagnosis (diagnosis_code);

create index patient_activity_idx on patient_activity (patient_id);
create index rx_patient_idx on rx (patient_id);
create index proc_patient_idx on procedure (patient_id);
create index patient_surgical_idx on surgical (patient_id);

create table train_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);
create table test_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);


\copy train_patients_to_exclude from 'train_patients_to_exclude.csv' ;
\copy test_patients_to_exclude from 'test_patients_to_exclude.csv' ;

delete from patients_train where patient_id in (select patient_id from train_patients_to_exclude);
delete from patients_test where patient_id in (select patient_id from test_patients_to_exclude);
delete from diagnosis where patient_id in (select patient_id from train_patients_to_exclude);
delete from diagnosis where patient_id in (select patient_id from test_patients_to_exclude);
delete from procedure where patient_id in (select patient_id from train_patients_to_exclude);
delete from procedure where patient_id in (select patient_id from test_patients_to_exclude);
delete from patient_activity where patient_id in (select patient_id from train_patients_to_exclude);
delete from patient_activity where patient_id in (select patient_id from test_patients_to_exclude);
delete from surgical where patient_id in (select patient_id from train_patients_to_exclude);
delete from surgical where patient_id in (select patient_id from test_patients_to_exclude);
delete from rx where patient_id in (select patient_id from train_patients_to_exclude);
delete from rx where patient_id in (select patient_id from test_patients_to_exclude);
vacuum;

select patient_id, procedure_code from procedure where procedure_code
in (select procedure_code from procedure_code where
procedure_description like '%CERVI%');

\copy (select t1.patient_id, t2.primary_practitioner_id, t3.cbsa from patients_train t1 left join diagnosis t2 on (t1.patient_id=t2.patient_id) left join physician t3 on (t2.primary_practitioner_id=t3.practitioner_id)) to 'diagnosis_patient_practitioner.csv' with csv header;

\copy (select distinct(t1.patient_id, t2.primary_practitioner_id, t3.cbsa) from patients_test t1 left join diagnosis t2 on (t1.patient_id=t2.patient_id) left join physician t3 on (t2.primary_practitioner_id=t3.practitioner_id)) to 'diagnosis_patient_practitioner_test.csv' with csv header;

\copy (select distinct(t1.patient_id, t2.primary_practitioner_id, t3.cbsa) from patients_train t1 left join procedure t2 on (t1.patient_id=t2.patient_id) left join physician t3 on (t2.primary_practitioner_id=t3.practitioner_id)) to 'procedure_patient_practitioner.csv' with csv header;
-- COPY 25023093

\copy (select t1.patient_id, t2.procedure_type_code, count(procedure_type_code) as count from patients_train t1, surgical t2 group by t1.patient_id, procedure_type_code) to 'surgical_procedure_type_code.csv' with csv header

\copy (select patient_id, count(patient_id) as num_procedures from procedure group by patient_id) to 'procedure_counts.csv' with csv header

\copy (select t1.patient_id, count(t2.patient_id) as num_procedures from patients_train t1 left join procedure t2 on(t1.patient_id=t2.patient_id) group by t1.patient_id) to 'train_procedure_counts.csv' with csv header
-- COPY 1157817
-- Time: 668356.468 ms
\copy (select t1.patient_id, count(t2.patient_id) as num_procedures from patients_test t1 left join procedure t2 on(t1.patient_id=t2.patient_id) group by t1.patient_id) to 'test_procedure_counts.csv' with csv header
-- COPY 1701813
-- Time: 463628.095 ms

drop table diag_code;
drop table diag_code_p ;

select t1.patient_id, t1.diagnosis_code into diag_code from diagnosis t1 right join patients_train t2 on (t1.patient_id=t2.patient_id) where t1.diagnosis_code in (select diagnosis_code from diagnosis_code limit 1000 offset 000);
-- Time: 368788.134 ms

select * from pivotmytable('diag_code','diag_code_p','patient_id','diagnosis_code','diagnosis_code','count');
-- Time: 361303.918 ms

\copy (select * from diag_code_p) to 'diag_code_000_1000.csv' with csv header
-- Time: 96349.282 ms

-- sed -i '' '2,$s/,0/,/g' diag_code_0_1000.csv

\copy (select t1.patient_id, t1.primary_practitioner_id, specialty_code from diagnosis t1 join physician t2 on (t1.primary_practitioner_id=t2.practitioner_id) join patients_train t3 on (t1.patient_id=t3.patient_id) where t2.specialty_code in ('FPP','PLN','FPG','FM','FP','FSM')) to 'train_physician_specialty_code_family.csv' with csv header

\copy (select t1.patient_id, t1.primary_practitioner_id, specialty_code from diagnosis t1 join physician t2 on (t1.primary_practitioner_id=t2.practitioner_id) join patients_test t3 on (t1.patient_id=t3.patient_id) where t2.specialty_code in ('FPP','PLN','FPG','FM','FP','FSM')) to 'test_physician_specialty_code_family.csv' with csv header
