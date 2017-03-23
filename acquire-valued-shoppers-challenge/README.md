acquire-valued-shoppers-challenge
=========================

As best I recall this competition, I must have downloaded [the data](https://www.kaggle.com/c/acquire-valued-shoppers-challenge/data), [put it in SQL DB](https://github.com/paulperry/kaggle/blob/master/acquire-valued-shoppers-challenge/shoppers.sql), performed some [basic EDA](https://github.com/paulperry/kaggle/blob/master/acquire-valued-shoppers-challenge/shoppers.out) on it with SQL,  [ipynb](http://nbviewer.ipython.org/github/paulperry/kaggle/blob/master/acquire-valued-shoppers-challenge/Shoppers%20Challenge.ipynb), and python scripts. I then used [vw](https://github.com/JohnLangford/vowpal_wabbit) with the following [command line arguments](https://github.com/paulperry/kaggle/blob/master/acquire-valued-shoppers-challenge/vw_command_line.txt) and built a model for final predictions.

I referenced the following literature and sites:

- Agrawal, Rakesh, et al. <a href='http://www.cs.helsinki.fi/hannu.toivonen/pubs/advances.pdf'>"Fast Discovery of Association Rules."</a> Advances in knowledge discovery and data mining 12.1 (1996): 307-328.
- Hahsler, Michael, et al. <a href='http://www.jmlr.org/papers/v12/hahsler11a.html'>"The arules R-package ecosystem: analyzing interesting patterns from large transaction data sets."</a> Journal of Machine Learning Research 12.Jun (2011): 2021-2025.
- Kanagal, Bhargav, et al. <a href='http://dl.acm.org/citation.cfm?id=2336669'>"Supercharging recommender systems using taxonomies for learning user purchase behavior."</a> Proceedings of the VLDB Endowment 5.10 (2012): 956-967.
- Leonard, Michael, and Brenda Wolfe. <a href='http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.88.8081&rep=rep1&type=pdf'>"Mining transactional and time series data."</a> abstract, presentation and paper, SUGI (2005): 10-13. (and Paper 080-30) 
- Pascale, G. <a href='stats.idre.ucla.edu/wp-content/uploads/2016/02/p007.pdf'>"Calculating marginal probabilities in PROC PROBIT."</a> Online http://www.ats.ucla.edu/stat/sas (1998).
- Qualls, Bill <a href='https://firstanalytics.files.wordpress.com/2015/07/mwsug-2013-aa07.pdf'>Introduction to Market Basket Analysis</a>, First Analytics, Raleigh, NC.
- Radcliffe, Nicholas J., and Patrick D. Surry. <a href='http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.441.5361&rep=rep1&type=pdf'>"Real-world uplift modelling with significance-based uplift trees."</a> White Paper TR-2011-1, Stochastic Solutions (2011).
- Rendle, Steffen, et al. <a href='http://dl.acm.org/citation.cfm?id=1795167'>"BPR: Bayesian personalized ranking from implicit feedback."</a> Proceedings of the twenty-fifth conference on uncertainty in artificial intelligence. AUAI Press, 2009.
- Shashanka, Madhu, and Michael Giering. <a href='http://link.springer.com/chapter/10.1007/978-1-4419-0221-4_41'>"Mining Retail Transaction Data for Targeting Customers with Headroom-A Case Study."</a> IFIP International Conference on Artificial Intelligence Applications and Innovations. Springer US, 2009.
- So, Ying. <a href='http://www.sascommunity.org/sugi/SUGI93/Sugi-93-217%20So.pdf'>"A tutorial on logistic regression."</a> Cary, NC: SAS White Papers (1995).(and <a href='https://support.sas.com/rnd/app/stat/papers/logistic.pdf'>here</a>)
- Stokes, Maura E. <a href='http://statistics.ats.ucla.edu/stat/sas/library/categorical.pdf'>"Recent advances in categorical data analysis."</a> 24th annual meeting of the SAS Users Group International Conference, Miami Beach. Retrieved February. Vol. 1. 1999.
- Tan, Pang-Ning, Michael Steinbach, and Vipin Kumar. <a href='https://www-users.cs.umn.edu/~kumar/dmbook/ch6.pdf'>"Association analysis: basic concepts and algorithms."</a> Introduction to data mining (2005): 327-414.
- Tobias, Randall D. <a href='http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.460.1258&rep=rep1&type=pdf'>"An introduction to partial least squares regression."</a> Proceedings of the twentieth annual SAS users group international conference. SAS Institute Cary, NC, 1995.
- Wissuwa, Stefan ; CLEVE, Jürgen ; LÄMMEL, Uwe: Data Mining to support Customer Relationship Management. In: BATOG, Jacek (Hrsg.): Proceedings der Konferenz Baltic Business Development University of Szczecin, 2006, S. 377-389
- Woo, Jongwook, and Yuhang Xu. <a href='http://cerc.wvu.edu/download/WORLDCOMP'11/2011%20CD%20papers/PDP4494.pdf'>"Market basket analysis algorithm with Map/Reduce of cloud computing."</a> The 2011 International Conference on Parallel and Distributed Processing Techniques and Applications (PDPTA 2011), Las Vegas. 2011.
- Xiong, Liang, et al. <a href='http://epubs.siam.org/doi/abs/10.1137/1.9781611972801.19'>"Temporal collaborative filtering with bayesian probabilistic tensor factorization."</a> Proceedings of the 2010 SIAM International Conference on Data Mining. Society for Industrial and Applied Mathematics, 2010.

Sites:
- <a href='https://github.com/MLWave/kaggle_acquire-valued-shoppers-challenge'>MLWave GitHub repo</a>
- <a href='http://machinelearningmastery.com/market-basket-analysis-with-association-rule-learning/'>Market Basket Analysis with Association Rule Learning</a> by Jason Brownlee on March 17, 2014.
- <a href='http://snowplowanalytics.com/guides/recipes/catalog-analytics/market-basket-analysis-identifying-products-that-sell-well-together.html'>Market basket analysis: identifying products and content that go well together</a>
- <a href='https://en.wikipedia.org/wiki/Quantile_regression'>Quantile Regression</a>
- <a href='https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0ahUKEwj70JeRmevSAhWK7IMKHeL5BLoQFggnMAE&url=https%3A%2F%2Fwww.researchgate.net%2Ffile.PostFileLoader.html%3Fid%3D57563157eeae39aa52279f64%26assetKey%3DAS%253A370168766189570%25401465266519195&usg=AFQjCNFHr3hcxh753druh3n1y6ETWAl0hg&sig2=TKbdWt-1ysj9gmKH1ZEWUQ'>Tobit Models</a>


