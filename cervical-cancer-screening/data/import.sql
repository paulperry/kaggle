PRAGMA cache_size = 400000;
PRAGMA synchronous = OFF;
PRAGMA journal_mode = OFF;
PRAGMA locking_mode = EXCLUSIVE;
PRAGMA count_changes = OFF;
PRAGMA temp_store = MEMORY;
PRAGMA auto_vacuum = NONE;

.mode csv
.separator ","
-- in rough order of size , big ones first
.import input2/diagnosis_head_stripped.csv diagnosis
.import input2/patient_activity_head_stripped.csv patient_activity
.import input2/prescription_head_stripped.csv prescription
.import input2/procedure_head_stripped.csv procedure
.import input2/surgical_head_stripped.csv surgical
.import input2/physicians_stripped.csv physician
.import input2/drugs_stripped.csv drug
.import input2/patients_test_stripped.csv patients_test
.import input2/patients_train_stripped.csv patients_train
.import input2/diagnosis_code_stripped.csv diagnosis_code
.import input2/procedure_code_stripped.csv procedure_code
.import input2/surgical_code_stripped.csv surgical_code

CREATE TABLE train_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);
CREATE TABLE test_patients_to_exclude
(
  patient_id integer  PRIMARY KEY
);

.import input2/train_patients_to_exclude.csv train_patients_to_exclude
.import input2/test_patients_to_exclude.csv test_patients_to_exclude

-- .import sample_submission.csv sample_submission

delete from patients_train where patient_id in (select * from train_patients_to_exclude );
delete from patients_test where patient_id in (select * from test_patients_to_exclude );

