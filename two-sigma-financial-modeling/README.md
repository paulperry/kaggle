# Two Sigma Financial Modeling Challenge

- https://www.kaggle.com/c/two-sigma-financial-modeling

<a href='https://www.twosigma.com/'>Two Sigma</a> hosted a challenge to predict what appear to be daily stock market prices. As they describe it:

	This dataset contains anonymized features pertaining to a time-varying
	value for a financial instrument. Each instrument has an id. Time is
	represented by the 'timestamp' feature and the variable to predict is
	'y'. No further information will be provided on the meaning of the
	features, the transformations that were applied to them, the
	timescale, or the type of instruments that are included in the data.

It was an interesting competition, primarily because if I were to
tackle ML on market data, I would would want to structure the data
exactly as they provided in the training set.  The addition of <a
href='https://github.com/Giqles/kagglegym'>kagglegym</a> also helped
produce an environment with no leaks or lookahead bias.

Here I :
- Perform a basic Exploratory Data Analysis (EDA)
- Inspect some basic Benchmarks
- Develop an XGB Model
- review some top models in the competition.


