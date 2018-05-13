
import pyprind
import pandas as pd
import os

xxxhmiac = 'imported done'
print(xxxhmiac)

labels = {'pos': 1, 'neg': 0}
pbar = pyprind.ProgBar(50000)
df = pd.DataFrame()



for s in ('test', 'train'):
 for l in ('pos', 'neg'):
  path = r'C:\Users\Harry Muzart\Documents\aclImdb/%s/%s' % (s, l)
  for file in os.listdir(path):
   with open(os.path.join(path, file), 'r', encoding='utf-8') as infile:
    txt = infile.read()
   df = df.append([[txt, labels[l]]], ignore_index=True)
   pbar.update()
   
df.columns = ['review', 'sentiment']

xxxhmiad = 'appended to dataframe done'
print(xxxhmiad)

# # path = os.path.join(basepath, s, l)


import numpy as np
np.random.seed(0)
df = df.reindex(np.random.permutation(df.index))
df.to_csv(r'C:\Users\Harry Muzart\Documents\SAfiles/movie_data.csv', index=False)

xxxhmiae = 'permutation done'
print(xxxhmiae)

import pandas as pd

xxxhmiaf = 'panda done'
print(xxxhmiaf)

df = pd.read_csv(r'C:\Users\Harry Muzart\Documents\SAfiles/movie_data.csv')
df.head(3)

xxxhmiaf = 'read csv done'
print(xxxhmiaf)

#### sort unicaode error at read csv



# Transforming documents into feature vectors

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer()
docs = np.array([
        'The sun is shining',
        'The weather is sweet',
        'The sun is shining, the weather is sweet, and one and one is two'])
bag = count.fit_transform(docs)

print(count.vocabulary_)

print(bag.toarray())

# Assessing word relevancy via term frequency-inverse document frequency

np.set_printoptions(precision=2)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf = TfidfTransformer(use_idf=True, norm='l2', smooth_idf=True)
print(tfidf.fit_transform(count.fit_transform(docs)).toarray())

tf_is = 3
n_docs = 3
idf_is = np.log((n_docs+1) / (3+1))
tfidf_is = tf_is * (idf_is + 1)
print('tf-idf of term "is" = %.2f' % tfidf_is)

tfidf = TfidfTransformer(use_idf=True, norm=None, smooth_idf=True)
raw_tfidf = tfidf.fit_transform(count.fit_transform(docs)).toarray()[-1]
raw_tfidf

l2_tfidf = raw_tfidf / np.sqrt(np.sum(raw_tfidf**2))
l2_tfidf


# Cleaning text data


df.loc[0, 'review'][-50:]


import re
def preprocessor(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    text = re.sub('[\W]+', ' ', text.lower()) +\
        ' '.join(emoticons).replace('-', '')
    return text
	
preprocessor(df.loc[0, 'review'][-50:])

preprocessor("</a>This :) is :( a test :-)!")

df['review'] = df['review'].apply(preprocessor)


# Processing documents into tokens


from nltk.stem.porter import PorterStemmer
porter = PorterStemmer()

def tokenizer(text):
    return text.split()

tokenizer('runners like running and thus they run')	
	
def tokenizer_porter(text):
    return [porter.stem(word) for word in text.split()]
	
tokenizer_porter('runners like running and thus they run')


import nltk
nltk.download('stopwords')


from nltk.corpus import stopwords

stop = stopwords.words('english')
[w for w in tokenizer_porter('a runner likes running and runs a lot')[-10:]
if w not in stop]


# Training a logistic regression model for document classification

X_train = df.loc[:25000, 'review'].values
y_train = df.loc[:25000, 'sentiment'].values
X_test = df.loc[25000:, 'review'].values
y_test = df.loc[25000:, 'sentiment'].values


from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
if Version(sklearn_version) < '0.18':
    from sklearn.grid_search import GridSearchCV
else:
    from sklearn.model_selection import GridSearchCV

tfidf = TfidfVectorizer(strip_accents=None,
                        lowercase=False,
                        preprocessor=None)

param_grid = [{'vect__ngram_range': [(1, 1)],
               'vect__stop_words': [stop, None],
               'vect__tokenizer': [tokenizer, tokenizer_porter],
               'clf__penalty': ['l1', 'l2'],
               'clf__C': [1.0, 10.0, 100.0]},
              {'vect__ngram_range': [(1, 1)],
               'vect__stop_words': [stop, None],
               'vect__tokenizer': [tokenizer, tokenizer_porter],
               'vect__use_idf':[False],
               'vect__norm':[None],
               'clf__penalty': ['l1', 'l2'],
               'clf__C': [1.0, 10.0, 100.0]},
              ]

lr_tfidf = Pipeline([('vect', tfidf),
                     ('clf', LogisticRegression(random_state=0))])

gs_lr_tfidf = GridSearchCV(lr_tfidf, param_grid,
                           scoring='accuracy',
                           cv=5,
                           verbose=1,
                           n_jobs=-1)
						   
gs_lr_tfidf.fit(X_train, y_train)

print('Best parameter set: %s ' % gs_lr_tfidf.best_params_)
print('CV Accuracy: %.3f' % gs_lr_tfidf.best_score_)

clf = gs_lr_tfidf.best_estimator_
print('Test Accuracy: %.3f' % clf.score(X_test, y_test))

from sklearn.linear_model import LogisticRegression
import numpy as np
if Version(sklearn_version) < '0.18':
    from sklearn.cross_validation import StratifiedKFold
    from sklearn.cross_validation import cross_val_score
else:
    from sklearn.model_selection import StratifiedKFold
    from sklearn.model_selection import cross_val_score

np.random.seed(0)
np.set_printoptions(precision=6)
y = [np.random.randint(3) for i in range(25)]
X = (y + np.random.randn(25)).reshape(-1, 1)

if Version(sklearn_version) < '0.18':
    cv5_idx = list(StratifiedKFold(y, n_folds=5, shuffle=False, random_state=0))

else:
    cv5_idx = list(StratifiedKFold(n_splits=5, shuffle=False, random_state=0).split(X, y))
    
cross_val_score(LogisticRegression(random_state=123), X, y, cv=cv5_idx)


if Version(sklearn_version) < '0.18':
    from sklearn.grid_search import GridSearchCV
else:
    from sklearn.model_selection import GridSearchCV

gs = GridSearchCV(LogisticRegression(), {}, cv=cv5_idx, verbose=3).fit(X, y)

gs.best_score_

cross_val_score(LogisticRegression(), X, y, cv=cv5_idx).mean()


# Working with bigger data - online algorithms and out-of-core learning





# Ch9 - Serializing fitted scikit-learn estimators




