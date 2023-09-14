from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB

mypipeline = make_pipeline(
    StandardScaler(), 
    GaussianNB()
)

..
mypipeline.fit(X_train, y_train)
..
mypipeline.predict(X_test)
