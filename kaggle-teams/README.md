Kaggle Teams
============

This is a start at a quantitative and social network study of Kaggle
Teams.

There is a lot to learn from the top data science practitioners.  They
have dedicated a lot of time to develop their workflows, have great
intuition of what methods are likely to work, and are efficient in
their use of time.

The central question is: who do they choose to team with and how does
the team organize their work?

Data for this analysis comes from the Kaggle Leaderboard as of
February 17, 2016. The data was extracted by web-scraping Kaggle’s
leaderboard web pages. Source code for web-scraping and data
pre-processing can be found at
[Jim Thompson's](https://github.com/jimthompson5802)
[github repository](https://github.com/jimthompson5802/kaggle-RScript). This
analysis builds on previous analysis of Kaggle teams
[by country](https://www.kaggle.com/jimthompson/introducing-kaggle-scripts/kaggle-competition-medal-count-analysis),
[by team structure](https://www.kaggle.com/jimthompson/introducing-kaggle-scripts/visualizing-kaggle-team-structures),
[by profile](http://notesofdabbler.github.io/201412_exploreKaggle/exploreKaggleUsers.html),
and
[over time](https://www.kaggle.com/jeffhebert/d/kaggle/meta-kaggle/kaggle-competitions-over-time).
This analysis does not take advantage of the
[Meta-Kaggle](https://www.kaggle.com/kaggle/meta-kaggle) dataset yet.
As of February 17, 2016 there were 200 completed competitions. In this
study I focus this analysis on the 133 competitions with a cash prize
that had teams.

The questions I investigate are in the [kaggle_teams](https://github.com/paulperry/kaggle/tree/master/kaggle-teams/kaggle_teams.ipynb) notebook are:

1. How many kagglers joined teams?
1. What is the distribution of team sizes?
1. How many distict team names were there?
1. Which competitions had the most teams?
1. Which team name won the most competitions
1. Which team members won the most when on a team?
1. Which are the largest teams?
1. Who has teamed up the most?
1. What does the social graph look like?
1. What are the skills of the top players?
1. Do teams cluster based on skills?
1. Do teams form based on language or country?
1. Does participating on a team correlate with Kaggle rank?
1. Do members team differently on structured vs unstructured data competitions?

<p align="center"><b>The Kaggle social graph of top players</b><br>
<img src='kaggle_teams.png'>
</p>

I've only teamed up 3 times, and on one occasion found we had made a
number of small but expensive mistakes.  So I decided I would
interview the top team players to learn some best practices. I
followed up with some specific questions:

1 .How do you select who you want to team with?
1. How do you communicate? Email, chat, video chat?
1. How do you share code?
1. How do you share data (or features)?
1. Do you share code frameworks?
1. How do you decide to divide the work?
1. How do you avoid duplicative work? Or repeated work?
1. How do you avoid team members finding the same stuff?
1. How do you keep track of model performance?
1. How do you decide who gets to submit what on each day?
1. Who picks and and how do you pick the final submissions?
1. If you wanted to learn what worked on other Kaggle teams, which
  teams would you want to learn from, and what questions would you
  ask?

I was lucky to communicate with <a
href='https://www.kaggle.com/leustagos'>Leustagos</a> (Lucas Eustaquio
Gomes da Silva) before he passed away, and this is what I learned:

"There is no easy way, winning is the result of much study, experience
and hard work. Learning from mistakes, reading winners forums, etc.

Success in teaming up consists in picking a good team. Most of the
time I team up with the same people. I like brainstorming ideas and
discussing some feature engineering. Its important to undestand each
other and to have somewhat distinct approachs. Other than that teaming
up wont be much more than averaging models. Until you find a good team
its a bit of trial and error. But try picking people that are around
you rank level and build up from there. Its easier to understand each
other."

1. *How do you communicate?* __chat__
1. *How do you share code?* __usually we dont, but when we do, its on dropbox__
1. *How do you share data (or features)?* __csv on dropbox__
1. *Do you share code frameworks?* __people dont like to mess much with someone else's code__
1. *How do you decide to divide the work?* __chat, but we usually have
  some slightly different approaches. its rare but we can suggest each
  other based on availability which ideas we can pursue
  first. Ususally telling what i will do will prevent others from doing the
  same__
1. *How do you avoid duplicative work?* __we dont avoid, but its not a
big issue. I don't team up from the start so we can have distinct
approachs when merging teams__
1. *How do you avoid team members finding the same stuff?* __we dont__
1. *How do you keep track of model performance?* __each one is
responsible for keeping its versioning. I use git, some just duplicate
and enumerate files. on each subission we describe which models we
used to generate it__
1. *How do you decide who gets to submit what on each day?* __commom
sense. we divide equally the number of submissions, but if someones
need more he asks__
1. *Who picks and and how do you pick the final submissions?* __the
leader picks it. Its a consensus. I never had any trouble to do
it. With the right reasons its very easy to choose. Of course some
times I dont agree and we just go with the majority. Just dont be very
picky and it will go smoothly.  It's very rare for me to not pick my
best submission. Except on some competitions that are too random.__

My conclusion was that at the time (2016, and before
[Kaggle Kernels](https://www.kaggle.com/kernels)), teams would at best
ensemble their models. Little time was devoted to joint data
exploration, feature reuse, and understanding other people's
models.  

References:

Leskovec, Jure, and Julian J. Mcauley. <a
href='http://papers.nips.cc/paper/4532-learning-to-discover-social-circles-in-ego-networks'>
"Learning to discover social circles in ego networks."</a> Advances in
neural information processing systems. 2012.
