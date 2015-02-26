# http://askubuntu.com/questions/137424/moving-mysql-datadir
# mysql -u root --local-infile=1 -p
# http://derwiki.tumblr.com/post/24490758395/loading-half-a-billion-rows-into-mysql
# http://www.mysqlperformanceblog.com/2008/07/03/how-to-load-large-files-safely-into-innodb-with-load-data-infile/

create database shoppers;

use shoppers;

create table offers (offer numeric, category numeric, quantity numeric, company bigint, offervalue float, brand numeric);
 
load data local infile 'offers.csv' into table offers fields terminated by ',' lines terminated by '\n';

create table trainHistory (id numeric, chain numeric , offer numeric, market numeric, repeattrips numeric, repeater bool, offerdate date);

load data local infile 'trainHistory.csv' into table trainHistory fields terminated by ',' lines terminated by '\n' ignore 1 lines (id, chain, offer, market, repeattrips, @v_repeater, offerdate) set repeater := @v_repeater = 't' ;

create table testHistory (id numeric, chain numeric, offer numeric, market numeric, offerdate date);

load data local infile 'testHistory.csv' into table testHistory fields terminated by ',' lines terminated by '\n' ignore 1 lines (id, chain, offer, market, offerdate);

create table submission (id numeric, repeatProbability float);

load data local infile 'sampleSubmission.csv' into table submission fields terminated by ',' lines terminated by '\n' ignore 1 lines;

alter table submission add unique index id (id);

create table purchased_offers (id numeric, chain numeric, dept numeric, category numeric, company numeric, brand numeric, date date, productsize float, productmeasure varchar(5), purchasequantity numeric, purchaseamount float, offer numeric);

load data local infile 'purchased_offers.csv' into table purchased_offers fields terminated by ',' lines terminated by '\n' ignore 1 lines (id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount,offer);  # 24.64 sec

create table transactions (id numeric, chain numeric, dept numeric, category numeric, company bigint, brand numeric, date date, productsize float, productmeasure char(5), purchasequantity numeric, purchaseamount float);

/* took hours */
load data local infile 'transactions.csv' into table transactions fields terminated by ',' lines terminated by '\n' ignore 1 lines (id,chain,dept,category,company,brand,date,productsize,productmeasure,purchasequantity,purchaseamount);

alter table trainHistory add unique index id_chain (id, chain);
alter table testHistory add unique index id_chain (id, chain);
alter table trainHistory add unique index id_chain (id, offer);
alter table testHistory add unique index id_offer (id, offer );
alter table purchased_offers add index id_offer (id, offer);
alter table offers add index offer (offer);
alter table offers add index product (category, brand, company);
alter table transactions add index id_chain (id, chain); # (37 min 38.44 sec) !
alter table transactions add index product (category, brand, company);   # (45 min 34.15 sec) !

select h.id as id, case when count(t.id) > 0 then 1 else 0 end as repeatProbability 
from testHistory as h 
inner join offers as o on h.offer=o.offer  
left join transactions as t 
on o.category=t.category 
and o.brand=t.brand 
and o.company=t.company 
and h.id=t.id 
into outfile 'benchmark_submission.csv'
fields terminated by ',' lines terminated by '\n';

select h.id as id, count(t.id) as repeatProbability 
from testHistory as h 
inner join offers as o on h.offer=o.offer  
inner join transactions as t 
on o.category=t.category 
and o.brand=t.brand 
and o.company=t.company 
and h.id=t.id 
group by id
into outfile 'benchmark_submission.csv' 
fields terminated by ',' lines terminated by '\n';

select 'id','repeatProbability' 
union all 
select h.id as id, case when count(t.id) > 0 then 1 else 0 end as repeatProbability 
from testHistory as h 
left join purchased_offers as t 
on h.id=t.id and h.offer = t.offer 
group by h.id, h.offer 
into outfile 'benchmark_submission.csv' 
fields terminated by ',' lines terminated by '\n'; 

create table shopped_offers (id numeric, chain numeric, dept numeric, category numeric, company bigint, brand numeric, date date, productsize float, productmeasure varchar(5), purchasequantity numeric, purchaseamount float, offer numeric, offervalue float);

insert into shopped_offers select r.id, r.chain, r.dept, r.category, r.company, r.brand, r.date, r.productsize, r.productmeasure, r.purchasequantity, r.purchaseamount, o.offer, o.offervalue from reduced as r inner join offers as o on o.category=r.category and o.brand=r.brand and o.company=r.company;

update offers as o set dept=(select case when char_length(category) = 3 then left(category, 1) else left(category, 2) end from (select * from offers) as x where x.offer=o.offer);

create table train like trainHistory ; 
insert train select * from trainHistory;
alter table train add unique index id (id);

alter table train add company numeric;
update train tt set tt.company=(select o.company from trainHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table train add offervalue numeric;
update train tt set tt.offervalue=(select o.offervalue from trainHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table train add bought_co int;
update train tt set tt.bought_co=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table train add company_q float;
update train tt set tt.company_q=(select sum(t.purchasequantity) from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table train add company_a float;
update train tt set tt.company_a=(select sum(t.purchaseamount) from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table train add co_30 float;
update train as tt set tt.co_30=(select case when count(*) > 0 then 1 else 0 end from reduced as t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table train add co_q_30 float;
update train as tt set tt.co_q_30=(select sum(t.purchasequantity) from reduced t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table train add co_a_30 float;
update train tt set tt.co_a_30=(select sum(t.purchaseamount) from reduced t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table train add category numeric;
update train tt set tt.category=(select o.category from trainHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table train add bought_cat int;
update train tt set tt.bought_cat=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.category=tt.category and t.id=tt.id) ;

alter table train add brand numeric;

update train tt set tt.brand=(select o.brand from trainHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table train add bought_brand int;
update train tt set tt.bought_brand=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.id=tt.id) ;

alter table train add bought_prod int;
update train tt set tt.bought_prod=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id) ;

alter table train add bought_prod_30 int;
update train tt set tt.bought_prod_30=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 30 day)) ;

alter table train add bought_prod_60 int;
update train tt set tt.bought_prod_60=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 60 day)) ;

alter table train add bought_prod_90 int;
update train tt set tt.bought_prod_90=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 90 day)) ;

alter table train add bought_prod_180 int;
update train tt set tt.bought_prod_180=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table train add last_shopped numeric;
update train tt set tt.last_shopped=(select abs(datediff(max(t.date), tt.offerdate)) from reduced t where t.id=tt.id );

alter table train add visits numeric;
update train tt set tt.visits=(select count(distinct date) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table train add dept int;
update train tt set tt.dept=(select o.dept from trainHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table train add transactions numeric;
update train tt set tt.transactions=(select count(*) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table train add returns numeric;
update train tt set tt.returns=(select case when count(purchasequantity < 0) > 0 or count(purchaseamount < 0) > 0 then 1 else 0 end from reduced t where t.id=tt.id and tt.category=t.category and tt.company=t.company and t.brand=t.brand and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table train add transactions numeric;
update train tt set tt.transactions=(select count(*) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table train add market_cat varchar(5);
update train tt set tt.market_cat=(select concat('M',market) from trainHistory as t where t.id=tt.id);

alter table train add company_cat varchar(20);
update train tt set tt.company_cat=(select concat('C',company) from trainHistory as t where t.id=tt.id);

alter table train add brand_cat varchar(20);
update train tt set tt.brand_cat=(select concat('B', brand) from trainHistory as t where t.id=tt.id);

alter table train add dept_cat varchar(20);
update train tt set tt.dept_cat=(select concat('D', dept) from trainHistory as t where t.id=tt.id);

(select 
'id','chain','offer','market','repeater','offerdate','company','offervalue','bought_co',
'company_q','company_a','co_30','co_q_30','co_a_30','category','bought_cat','bought_prod',
'brand','bought_brand','bought_prod_30','bought_prod_60','bought_prod_90','bought_prod_180',
'last_shopped','visits','dept','transactions','returns','market_cat','company_cat','brand_cat',
'dept_cat')
union
(select id,
ifnull(chain,''),
ifnull(offer,''),
ifnull(market,''),
ifnull(repeater,''),
ifnull(offerdate,''),
ifnull(company,''),
ifnull(offervalue,''),
ifnull(bought_co,''),ifnull(company_q,''),ifnull(company_a,''),
ifnull(co_30,''),ifnull(co_q_30,''),ifnull(co_a_30,''),
ifnull(category,''),ifnull(bought_cat,''),ifnull(bought_prod,''),ifnull(brand,''),
ifnull(bought_brand,''),
ifnull(bought_prod_30,''),ifnull(bought_prod_60,''),ifnull(bought_prod_90,''),
ifnull(bought_prod_180,''),ifnull(last_shopped,''),
ifnull(visits,''),ifnull(dept,''),ifnull(transactions,''),ifnull(returns,''),
ifnull(market_cat,''),ifnull(company_cat,''),ifnull(brand_cat,''),ifnull(dept_cat,'')
into outfile 'train_mod.csv' fields terminated by ',' lines terminated by '\n' from train);

alter table train add customer_dept int;
update train tt set tt.customer_dept=(select case when count(dept) 

# ----------- TEST -

create table test like testHistory ; 
insert test select * from testHistory;
alter table test add unique index id (id);

alter table test add company numeric;
update test tt set tt.company=(select o.company from testHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table test add offervalue numeric;
update test tt set tt.offervalue=(select o.offervalue from testHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table test add bought_co int;
update test tt set tt.bought_co=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table test add company_q float;
update test tt set tt.company_q=(select sum(t.purchasequantity) from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table test add company_a float;
update test tt set tt.company_a=(select sum(t.purchaseamount) from reduced t where t.company=tt.company and t.id=tt.id) ;

alter table test add co_30 float;
update test as tt set tt.co_30=(select case when count(*) > 0 then 1 else 0 end from reduced as t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table test add co_q_30 float;
update test as tt set tt.co_q_30=(select sum(t.purchasequantity) from reduced t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table test add co_a_30 float;
update test tt set tt.co_a_30=(select sum(t.purchaseamount) from reduced t where t.company=tt.company and t.id=tt.id and t.date > date_sub(tt.offerdate, interval 30 day)) ;

alter table test add category numeric;
update test tt set tt.category=(select o.category from testHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table test add bought_cat int;
update test tt set tt.bought_cat=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.category=tt.category and t.id=tt.id) ;

alter table test add brand numeric;
update test tt set tt.brand=(select o.brand from testHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table test add bought_brand int;
update test tt set tt.bought_brand=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.id=tt.id) ;

alter table test add bought_prod int;
update test tt set tt.bought_prod=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id) ;

alter table test add bought_prod_30 int;
update test tt set tt.bought_prod_30=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 30 day)) ;

alter table test add bought_prod_60 int;
update test tt set tt.bought_prod_60=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 60 day)) ;

alter table test add bought_prod_90 int;
update test tt set tt.bought_prod_90=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 90 day)) ;

alter table test add bought_prod_180 int;
update test tt set tt.bought_prod_180=(select case when count(*) > 0 then 1 else 0 end from reduced t where t.brand=tt.brand and t.category=tt.category and t.company=tt.company and t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table test add last_shopped numeric;
update test tt set tt.last_shopped=(select abs(datediff(max(t.date), tt.offerdate)) from reduced t where t.id=tt.id );

alter table test add visits numeric;
update test tt set tt.visits=(select count(distinct date) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table test add dept int;
update test tt set tt.dept=(select o.dept from testHistory t join offers o on t.offer=o.offer where t.id=tt.id) ;

alter table test add transactions numeric;
update test tt set tt.transactions=(select count(*) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table test add returns numeric;
update test tt set tt.returns=(select case when count(purchasequantity < 0) > 0 or count(purchaseamount < 0) > 0 then 1 else 0 end from reduced t where t.id=tt.id and tt.category=t.category and tt.company=t.company and t.brand=t.brand and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table test add transactions numeric;
update test tt set tt.transactions=(select count(*) from reduced t where t.id=tt.id and t.date >= date_sub(tt.offerdate, interval 180 day)) ;

alter table test add market_cat varchar(5);
update test tt set tt.market_cat=(select concat('M',market) from testHistory as t where t.id=tt.id);

alter table test add company_cat varchar(20);
update test tt set tt.company_cat=(select concat('C',company) from testHistory as t where t.id=tt.id);

alter table test add brand_cat varchar(20);
update test tt set tt.brand_cat=(select concat('B', brand) from testHistory as t where t.id=tt.id);

alter table test add dept_cat varchar(20);
update test tt set tt.dept_cat=(select concat('D', dept) from testHistory as t where t.id=tt.id);

alter table test add repeater int;
update test tt set tt.repeater=(select 0 from testHistory as t where t.id=tt.id);

(select 
'id','chain','offer','market','offerdate','company','offervalue','bought_co',
'company_q','company_a','co_30','co_q_30','co_a_30','category','bought_cat','bought_prod',
'brand','bought_brand','bought_prod_30','bought_prod_60','bought_prod_90','bought_prod_180',
'last_shopped','visits','dept','transactions','returns','market_cat','company_cat','brand_cat',
'dept_cat','repeater')
union
(select id,
ifnull(chain,''),
ifnull(offer,''),
ifnull(market,''),
ifnull(offerdate,''),
ifnull(company,''),
ifnull(offervalue,''),
ifnull(bought_co,''),ifnull(company_q,''),ifnull(company_a,''),
ifnull(co_30,''),ifnull(co_q_30,''),ifnull(co_a_30,''),
ifnull(category,''),ifnull(bought_cat,''),ifnull(bought_prod,''),ifnull(brand,''),
ifnull(bought_brand,''),
ifnull(bought_prod_30,''),ifnull(bought_prod_60,''),ifnull(bought_prod_90,''),
ifnull(bought_prod_180,''),ifnull(last_shopped,''),
ifnull(visits,''),ifnull(dept,''),ifnull(transactions,''),ifnull(returns,''),
ifnull(market_cat,''),ifnull(company_cat,''),ifnull(brand_cat,''),ifnull(dept_cat,''), repeater
into outfile 'test_mod.csv' fields terminated by ',' lines terminated by '\n' from test);

select id from test into outfile 'test_ids.csv' lines terminated by '\n';


# paste -d, test_ids.csv Shoppers2_RuleFit_Classifier_\(11\)_64%_Informative_Features_test_mod.csv > submit.csv
# awk -F',' '{print $1 "," $3}' submit.csv > submit_final.csv 

# ------------

id
chain
offer
market
repeater
offerdate
company
offervalue
bought_co
company_q
company_a
co_30
co_q_30
co_a_30
category
bought_cat
bought_prod
brand
bought_brand
bought_prod_30
bought_prod_60
bought_prod_90
bought_prod_180
last_shopped
visits
dept
transactions
returns
market_cat
company_cat
brand_cat
dept_cat


offer_value
offer_quantity
total_spend
has_bought_company
has_bought_company_q
has_bought_company_a
has_bought_company_30
has_bought_company_q_30
has_bought_company_a_30
has_bought_company_60
has_bought_company_q_60
has_bought_company_a_60
has_bought_company_90
has_bought_company_q_90
has_bought_company_a_90
has_bought_company_180
has_bought_company_q_180
has_bought_company_a_180
has_bought_category
has_bought_category_q
has_bought_category_a
has_bought_category_30
has_bought_category_q_30
has_bought_category_a_30
has_bought_category_60
has_bought_category_q_60
has_bought_category_a_60
has_bought_category_90
has_bought_category_q_90
has_bought_category_a_90
has_bought_category_180
has_bought_category_q_180
has_bought_category_a_180
has_bought_brand
has_bought_brand_q
has_bought_brand_a
has_bought_brand_30
has_bought_brand_q_30
has_bought_brand_a_30
has_bought_brand_60
has_bought_brand_q_60
has_bought_brand_a_60
has_bought_brand_90
has_bought_brand_q_90

