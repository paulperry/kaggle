# Two Sigma Financial Modeling Challenge

- https://www.kaggle.com/c/two-sigma-financial-modeling

<a href='https://www.twosigma.com/'>Two Sigma</a> hosted a challenge to predict what appear to be daily stock market prices. As they describe it:

> This dataset contains anonymized features pertaining to a time-varying
> value for a financial instrument. Each instrument has an id. Time is
> represented by the 'timestamp' feature and the variable to predict is
> 'y'. No further information will be provided on the meaning of the
> features, the transformations that were applied to them, the
> timescale, or the type of instruments that are included in the data.

It was an interesting competition, primarily because if I were to
tackle ML on market data, I would would want to structure the data
exactly as they provided in the training set.  The addition of <a
href='https://github.com/Giqles/kagglegym'>kagglegym</a> also helped
produce an environment less susceptible to leaks or lookahead bias.
The downside is we don't know the meaning of the anonymized
transformed data, making it harder to bring domain knowledge to the
problem; and in turn complicating the decision of which features to
build.

Here I :
- [Perform a basic Exploratory Data Analysis (EDA)](https://github.com/paulperry/kaggle/blob/master/two-sigma-financial-modeling/models/2Sigma_EDA.ipynb)
- [Inspect some basic Benchmarks](https://github.com/paulperry/kaggle/blob/master/two-sigma-financial-modeling/models/2Sigma_Benchmarks.ipynb)
- Perform some feature egineering
- Develop an XGB Model
- [and compare some top models in the competition](https://github.com/paulperry/kaggle/blob/master/two-sigma-financial-modeling/models/other_models.ipynb)

I joined this competition very late and submitted only two models.




