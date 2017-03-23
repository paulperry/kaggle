aws s3 cp s3://cervical-cancer-screening/diagnosis_code.csv.gz .
 aws s3 cp s3://cervical-cancer-screening/diagnosis_head.csv.gz .
aws s3 cp s3://cervical-cancer-screening/drugs.csv.gz .
aws s3 cp s3://cervical-cancer-screening/patient_activity_head.csv.gz .
aws s3 cp s3://cervical-cancer-screening/patients_test.csv.gz .
aws s3 cp s3://cervical-cancer-screening/patients_train.csv.gz .
aws s3 cp s3://cervical-cancer-screening/physicians.csv.gz .
aws s3 cp s3://cervical-cancer-screening/prescription_head.csv.gz .
aws s3 cp s3://cervical-cancer-screening/procedure_code.csv.gz .
aws s3 cp s3://cervical-cancer-screening/procedure_head.csv.gz .
aws s3 cp s3://cervical-cancer-screening/sample_submission.csv .
aws s3 cp s3://cervical-cancer-screening/surgical_code.csv.gz .
 aws s3 cp s3://cervical-cancer-screening/surgical_head.csv.gz .
aws s3 cp s3://cervical-cancer-screening/test_patients_to_exclude.csv .
aws s3 cp s3://cervical-cancer-screening/train_patients_to_exclude.csv .
#
gunzip diagnosis_code.csv.gz 
 gunzip diagnosis_head.csv.gz 
gunzip drugs.csv.gz 
gunzip patient_activity_head.csv.gz 
gunzip patients_test.csv.gz 
gunzip patients_train.csv.gz 
gunzip physicians.csv.gz 
gunzip prescription_head.csv.gz 
gunzip procedure_code.csv.gz 
gunzip procedure_head.csv.gz 
gunzip sample_submission.csv 
gunzip surgical_code.csv.gz 
gunzip surgical_head.csv.gz 
gunzip test_patients_to_exclude.csv 
gunzip train_patients_to_exclude.csv 
