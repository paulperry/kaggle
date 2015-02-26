"""
Kaggle Challenge:
Modded version from 
"http://www.kaggle.com/c/acquire-valued-shoppers-challenge/" 
'Reduce the data and generate features' by Triskelion 

"""

from datetime import datetime, date
from collections import defaultdict

data_dir = "../data/"

loc_offers = data_dir + "offers.csv"
loc_transactions = data_dir + "transactions.csv"
loc_train = data_dir + "trainHistory.csv"
loc_test = data_dir + "testHistory.csv"

# will be created
loc_reduced = data_dir + "reduced.csv" 
loc_out_train = data_dir + "train.vw"
loc_out_test = data_dir + "test.vw"
loc_stats = data_dir + "eda_stats.csv" 
###

def eda_stats(loc_transactions, loc_stats):
  start = datetime.now()
  from collections import Counter
  import math
  
  #get all categories and comps on offer in a dict
  idd = {}
  chain = {}
  dept = {}
  category = {}
  company = {}
  brand = {}
  date = {}
  productsize  = Counter()
  productmeasure = Counter()
  purchasequantity = Counter()
  purchaseamount = Counter()
  cat_co_brand = Counter()
  #open output file
  o =  open(loc_stats, "wb")
  #go through transactions file
  for e, line in enumerate( open(loc_transactions) ):
    if e != 0:
      l = line.split(",")
      idd[l[0]] = 1
      chain[l[1]] = 1
      dept[l[2]] = 1
      category[l[3]] = 1
      company[l[4]] = 1
      brand[l[5]] = 1
      date[l[6]] = 1
      productsize [math.trunc( float(l[7]))] += 1;
      productmeasure[l[8]] += 1;
      purchasequantity[ int(l[9])] += 1
      purchaseamount[math.trunc( float(l[10]))] += 1
      cat_co_brand_val = str(l[3]) +'.'+ str(l[4]) +'.'+ str(l[5])
      cat_co_brand[cat_co_brand_val] += 1 
      #progress
      if e % 5000000 == 0:
        print e, datetime.now() - start

  o.write("unque users: "+ str(len(idd))+'\n')
  o.write("chains: " + str(len(chain))+'\n')
  o.write("dept's: " + str(len(dept))+'\n')
  o.write("categories: "+ str(len(category))+'\n')
  o.write("companies: "+ str(len(company))+'\n')
  o.write("brands: "+ str(len(brand))+'\n')
  o.write("dates: "+ str(len(date))+'\n')
  o.write("product sizes: "+str(len(productsize))+'\n')
  o.write("product measures: "+ str(len(productmeasure))+'\n')
  o.write("purchase quantities: "+ str(len(purchasequantity))+'\n')
  o.write("puchase amounts: "+ str(len(purchaseamount))+'\n')
  o.write("unique products: "+ str(len(cat_co_brand))+'\n')
  o.write("# of transactions: "+ str(e) +'\n')
  o.close()
  o =  open('productsize.json', "wb")
  o.write(str(dict(productsize )))
  o.close()
  o =  open('productmesaure.json', "wb")
  o.write(str(dict(productmeasure)))
  o.close()
  o = open('purchasequantity.json', "wb")
  o.write(str(dict(purchasequantity)))
  o.close()
  o =  open('purchaseamount.json', "wb")
  o.write(str(dict(purchaseamount)))
  o.close()
  o =  open('cat_co_brand.json', "wb")
  o.write(str(dict(cat_co_brand)))
  o.close()

  print e, datetime.now() - start, "done!"

def reduce_data(loc_offers, loc_transactions, loc_reduced):
  start = datetime.now()
  #get all categories and comps on offer in a dict
  offers_cat = {}
  offers_co = {}
  offers_brand = {}
  for e, line in enumerate( open(loc_offers) ):
    offers_cat[ line.split(",")[1] ] = 1
    offers_co[ line.split(",")[3] ] = 1
    offers_brand[ line.split(",")[6] ] = 1
  #open output file
  with open(loc_reduced, "wb") as outfile:
    #go through transactions file and reduce
    reduced = 0
    for e, line in enumerate( open(loc_transactions) ):
      if e != 0:
        #only write when if category in offers dict
        if line.split(",")[3] in offers_cat or line.split(",")[4] in offers_co:
          outfile.write( line )
          reduced += 1
      else:
        outfile.write( line ) #print header
      #progress
      if e % 5000000 == 0:
        print e, reduced, datetime.now() - start
  print e, reduced, datetime.now() - start


def diff_days(s1,s2):
	date_format = "%Y-%m-%d"
	a = datetime.strptime(s1, date_format)
	b = datetime.strptime(s2, date_format)
	delta = b - a
	return delta.days

def generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test):
	#keep a dictionary with the offerdata
	offers = {}
	for e, line in enumerate( open(loc_offers) ):
		row = line.strip().split(",")
		offers[ row[0] ] = row

	#keep two dictionaries with the shopper id's from test and train
	train_ids = {}
	test_ids = {}
	for e, line in enumerate( open(loc_train) ):
		if e > 0:
			row = line.strip().split(",")
			train_ids[row[0]] = row
	for e, line in enumerate( open(loc_test) ):
		if e > 0:
			row = line.strip().split(",")
			test_ids[row[0]] = row
	#open two output files
	with open(loc_out_train, "wb") as out_train, open(loc_out_test, "wb") as out_test:
		#iterate through reduced dataset 
		last_id = 0
		features = defaultdict(float)
		for e, line in enumerate( open(loc_transactions) ):
			if e > 0: #skip header
				#poor man's csv reader
				row = line.strip().split(",")
				#write away the features when we get to a new shopper id
				if last_id != row[0] and e != 1:
					
					#generate negative features
					if "has_bought_company" not in features:
						features['never_bought_company'] = 1
					
					if "has_bought_category" not in features:
						features['never_bought_category'] = 1
						
					if "has_bought_brand" not in features:
						features['never_bought_brand'] = 1
						
					if "has_bought_brand" in features and "has_bought_category" in features and "has_bought_company" in features:
						features['has_bought_brand_company_category'] = 1
					
					if "has_bought_brand" in features and "has_bought_category" in features:
						features['has_bought_brand_category'] = 1
					
					if "has_bought_brand" in features and "has_bought_company" in features:
						features['has_bought_brand_company'] = 1
						
					outline = ""
					test = False
					for k, v in features.items():
						
						if k == "label" and v == 0.5:
							#test
							outline = "1 '" + last_id + " |f" + outline
							test = True
						elif k == "label":
							outline = str(v) + " '" + last_id + " |f" + outline
						else:
							outline += " " + k+":"+str(v) 
					outline += "\n"
					if test:
						out_test.write( outline )
					else:
						out_train.write( outline )
					#print "Writing features or storing them in an array"
					#reset features
					features = defaultdict(float)
				#generate features from transaction record
				#check if we have a test sample or train sample
				if row[0] in train_ids or row[0] in test_ids:
					#generate label and history
					if row[0] in train_ids:
						history = train_ids[row[0]]
						if train_ids[row[0]][5] == "t":
							features['label'] = 1
						else:
							features['label'] = 0
					else:
						history = test_ids[row[0]]
						features['label'] = 0.5
						
					#print "label", label 
					#print "trainhistory", train_ids[row[0]]
					#print "transaction", row
					#print "offers", offers[ train_ids[row[0]][2] ]
					#print
					
					features['offer_value'] = offers[ history[2] ][4]
					features['offer_quantity'] = offers[ history[2] ][2]
					offervalue = offers[ history[2] ][4]
					
					features['total_spend'] += float( row[10] )
					
					if offers[ history[2] ][3] == row[4]:
						features['has_bought_company'] += 1.0
						features['has_bought_company_q'] += float( row[9] )
						features['has_bought_company_a'] += float( row[10] )
						
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_company_30'] += 1.0
							features['has_bought_company_q_30'] += float( row[9] )
							features['has_bought_company_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_company_60'] += 1.0
							features['has_bought_company_q_60'] += float( row[9] )
							features['has_bought_company_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_company_90'] += 1.0
							features['has_bought_company_q_90'] += float( row[9] )
							features['has_bought_company_a_90'] += float( row[10] )
						if date_diff_days < 180:
							features['has_bought_company_180'] += 1.0
							features['has_bought_company_q_180'] += float( row[9] )
							features['has_bought_company_a_180'] += float( row[10] )
					
					if offers[ history[2] ][1] == row[3]:
						
						features['has_bought_category'] += 1.0
						features['has_bought_category_q'] += float( row[9] )
						features['has_bought_category_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_category_30'] += 1.0
							features['has_bought_category_q_30'] += float( row[9] )
							features['has_bought_category_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_category_60'] += 1.0
							features['has_bought_category_q_60'] += float( row[9] )
							features['has_bought_category_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_category_90'] += 1.0
							features['has_bought_category_q_90'] += float( row[9] )
							features['has_bought_category_a_90'] += float( row[10] )						
						if date_diff_days < 180:
							features['has_bought_category_180'] += 1.0
							features['has_bought_category_q_180'] += float( row[9] )
							features['has_bought_category_a_180'] += float( row[10] )				
					if offers[ history[2] ][5] == row[5]:
						features['has_bought_brand'] += 1.0
						features['has_bought_brand_q'] += float( row[9] )
						features['has_bought_brand_a'] += float( row[10] )
						date_diff_days = diff_days(row[6],history[-1])
						if date_diff_days < 30:
							features['has_bought_brand_30'] += 1.0
							features['has_bought_brand_q_30'] += float( row[9] )
							features['has_bought_brand_a_30'] += float( row[10] )
						if date_diff_days < 60:
							features['has_bought_brand_60'] += 1.0
							features['has_bought_brand_q_60'] += float( row[9] )
							features['has_bought_brand_a_60'] += float( row[10] )
						if date_diff_days < 90:
							features['has_bought_brand_90'] += 1.0
							features['has_bought_brand_q_90'] += float( row[9] )
							features['has_bought_brand_a_90'] += float( row[10] )						
						if date_diff_days < 180:
							features['has_bought_brand_180'] += 1.0
							features['has_bought_brand_q_180'] += float( row[9] )
							features['has_bought_brand_a_180'] += float( row[10] )	
				last_id = row[0]
				if e % 100000 == 0:
					print e
					
#generate_features(loc_train, loc_test, loc_transactions, loc_out_train, loc_out_test)


if __name__ == '__main__':
#	reduce_data(loc_offers, loc_transactions, loc_reduced)
#	generate_features(loc_train, loc_test, loc_reduced, loc_out_train, loc_out_test)
    eda_stats(loc_transactions, loc_stats)
	
	
