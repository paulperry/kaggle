Titanic: Machine Learning from Disaster
----

What works in this competition is domain knowledge: identify the women and children as they are saved first, and know the organization of the cabins on the boat (which deck theya are on).  I achieve a score of 0.78469 for a ranking of 859 / 2,560 at the time; below the 25% mark, but above the 35% mark.  I use [Datarobot](www.datarobot.com) as tool to make the prediction, but handle all the pre and post processing in this [notebook](https://github.com/paulperry/kaggle/blob/master/titanic/Titanic-Derived.ipynb) .

A note about the rankings: scores below 0.84 are reasonable as suggested by this [post](https://www.kaggle.com/c/titanic-gettingStarted/forums/t/4894/what-accuracy-should-i-be-aiming-for/26197), but anything above that is most certainly 'cheating'; which is not hard to do as the dataset is public and the list of names of the deceased is easly found.  This is also evident from the Titanic Leaderboard score disitribution, where most scores are on a long low sloping plateau, but the top of the board quickly rises in score.

![Image of Kaggle Titanic Leaderboard score distribution](https://raw.githubusercontent.com/paulperry/kaggle/master/titanic/titanic_kaggle_score_distribution.png)
Plenty of others have documented their efforts on this dataset, including the list below and their scores:

score | Language | site 
------|----------|------
0.813 | R | [kaggle - R](http://www.kaggle.com/c/titanic-gettingStarted/forums/t/6821/titanic-getting-started-with-r-full-guide-to-0-81340) 
0.81340 | Python | [Elena Cuoco](http://elenacuoco.altervista.org/blog/archives/1195)
0.799 | Python | [kaggle - Pyhton](https://www.kaggle.com/c/titanic-gettingStarted/forums/t/10156/getting-0-799-with-random-forests-and-gradient-boosting/52661) [github](https://github.com/savarin/titanic) 
0.794 | Python | [kaggle - forum]( https://www.kaggle.com/c/titanic-gettingStarted/forums/t/6708/python-code-to-score-0-79426/36826)
0.794 | R | [kaggle - forum](http://www.kaggle.com/c/titanic-gettingStarted/forums/t/5232/r-code-to-score-0-79426)
0.794 | R | [philippeadjiman](http://www.philippeadjiman.com/blog/2013/09/12/a-data-science-exploration-from-the-titanic-in-r/) 
| Python | [](http://elenacuoco.altervista.org/blog/archives/1195)
| | [Who Survived the Titanic? A Logistic Regression Analysis](http://works.bepress.com/lonniekstevans/5/)
| | [agconti](https://github.com/agconti/kaggle-titanic)
| | [mwaskom](http://nbviewer.ipython.org/gist/mwaskom/8224591)



