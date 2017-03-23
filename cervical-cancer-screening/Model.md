Basic Insight
=============

Our team, consisting of Elena Cuoco, Paul Perry, and Zygmunt Zając, did not discover the leak, so the insights we present are not tainted by using this source. We were able to score > 0.88 with just 100 features.

Some classifiers can report feature importance. One of them is XGBoost, which we used, among others. Here is the feature importance plot from our best XGBoost model:

![](https://github.com/paulperry/cervical-cancer-screening/blob/master/tmp/images/xgboost_best.png)

* _cbsa_y_ is CBSA of primary_practitioner
* _cbsa_x_ is CBSA of the most visited practitioner for diagnosis across all diagnoses
* _num_visits_ is total count of visits from patient_activity
* _date_delta_ is _last_visit_ - _first_visit_ number of months in medical from 2008 to 2014
* _obg_screen_pct_ is screening % of the OBG
* _obg_id_ is _primary_practitioner_id with specialty_code in ('OBG','GYN','REN', 'OBS')
* _obg_patient_count_ is number of patients of the OBG
* _V72_ is diagnosis V72.31 = "ROUTINE GYNECOLOGICAL EXAMINATION"

The most important features come from two groups: demographics and patient activity. Patient activity includes basic statistics (such as the total number of procedures) and more specific features like OBG information.

Demographics
------------

The most important demographics are age and location.

### Age
	In [9]: pd.options.display.float_format = '{:9,.1%}'.format

	In [10]: train.groupby( 'patient_age_group' ).is_screener.mean()
	Out[10]:
	patient_age_group
	24-26       71.9%
	27-29       70.5%
	30-32       67.8%
	33-35       65.7%
	36-38       64.2%
	39-41       62.5%
	42-44       60.3%
	45-47       58.1%
	48-50       55.9%
	51-53       53.7%
	54-56       51.0%
	57-59       49.0%
	60-62       46.0%
	63-65       40.8%
	66-68       34.5%
	69-71       28.5%

	In [11]: train.groupby( 'patient_age_group' ).is_screener.mean().plot( kind = 'bar', color = 'g' )

![](https://github.com/paulperry/cervical-cancer-screening/blob/master/tmp/images/pct_is_screener_by_age_barplot.png)

You can see that _is_screener_ percentage is strictly declining with each age group.

### Location

Location features include a patient's state and CBSA (see below).

![](https://github.com/paulperry/cervical-cancer-screening/blob/master/tmp/images/states_green.png)

CBSA stands for [Core-Based Statistical Areas](http://greatdata.com/cbsa-data). Defined by the US government Office of Management and Budget, these are geographic locations neighboring urban areas of at least 10,000 people and/or  socioeconomically tied to the urban center by commuting.

We matched patient's location with a CBSA code and used that code as a feature. We did the same with primary physician's office location.

![](https://github.com/paulperry/cervical-cancer-screening/blob/master/tmp/images/cbsa_green.png)

Procedures
----------

It appears that if you were to select one table, procedures offer the most predictive information. Just raw procedure counts by patient and by code allowed us to exceed 0.8 AUC. Therefore, it might be interesting which procedure codes are important for a classifier. We performed a L1 (Lasso) feature selection using Vowpal Wabbit:

	In [37]: vi[['procedure_code', 'procedure_description', 'RelScore']].head( 10 )
	Out[37]:
	  procedure_code                             procedure_description RelScore
	0          57454   COLPOSCOPY CERVIX BX CERVIX & ENDOCRV CURRETAGE  100.00%
	1          81252             GJB2 GENE ANALYSIS FULL GENE SEQUENCE   96.93%
	2          57456          COLPOSCOPY CERVIX ENDOCERVICAL CURETTAGE   95.00%
	3          57455  COLPOSCOPY CERVIX UPPR/ADJCNT VAGINA W/CERVIX BX   91.42%
	4          S4020  IN VITRO FERTILIZATION PROCEDURE CANCELLED BEFOR   85.76%
	5          S0605          DIGITAL RECTAL EXAMINATION, MALE, ANNUAL   83.64%
	6          G0143  SCREENING CYTOPATHOLOGY, CERVICAL OR VAGINAL (AN   78.39%
	7          90696         DTAP-IPV VACCINE CHILD 4-6 YRS FOR IM USE   76.98%
	8          S4023            DONOR EGG CYCLE, INCOMPLETE, CASE RATE   76.67%
	9          69710   IMPLTJ/RPLCMT EMGNT BONE CNDJ DEV TEMPORAL BONE   72.06%
	
The procedures above are positively correlated of a patient being a screener. Here are the codes that indicate otherwise:

	In [42]: vi[['procedure_code', 'procedure_description', 'RelScore']].tail( 10 )
	Out[42]:
		  procedure_code                             procedure_description RelScore
	14337          K0735  SKIN PROTECTION WHEELCHAIR SEAT CUSHION, ADJUSTA  -62.48%
	14338          34805  EVASC RPR AAA AORTO-UNIILIAC/AORTO-UNIFEM PROSTH  -64.68%
	14339          L5975  ALL LOWER EXTREMITY PROSTHESIS, COMBINATION SING  -65.39%
	14340          89321      SEMEN ANALYSIS SPERM PRESENCE&/MOTILITY SPRM  -65.51%
	14341          S9145  INSULIN PUMP INITIATION, INSTRUCTION IN INITIAL   -69.96%
	14342          00632     ANESTHESIA LUMBAR REGION LUMBAR SYMPATHECTOMY  -77.13%
	14343          27756       PRQ SKELETAL FIXATION TIBIAL SHAFT FRACTURE  -78.61%
	14344          3303F      AJCC CANCER STAGE IA, DOCUMENTED (ONC), (ML)  -82.77%
	14345          23675  CLTX SHOULDER DISLC W/SURG/ANTMCL NECK FX W/MANJ  -83.14%
	14346          Q4111                 GAMMAGRAFT, PER SQUARE CENTIMETER  -85.49%

_Complete data and code are available on request._
