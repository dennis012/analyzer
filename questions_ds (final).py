
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


dataset = pd.read_csv('custom_dataset3.csv', sep = ',', engine='python') #,sep='delimiter')
y = dataset['category']


# In[3]:


dataset.head()


# In[4]:


from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
dataset['category'] = le.fit_transform(dataset.category)


# In[5]:


dataset.shape


# In[6]:


# #import re
# import nltk
# nltk.download('stopwords')


# In[7]:


# from nltk.stem.porter import PorterStemmer
# ps = PorterStemmer()
# from nltk.corpus import stopwords


# In[8]:


# stemmed_dataset= []
# for i in range(0,100):
#     stemmed_array = dataset['question'][i].split()
#     stemmed = [ps.stem(word) for word in stemmed_array if not word in set(stopwords.words('english')) ]
#     stemmed = ' '.join(stemmed)
#     stemmed_dataset.append(stemmed)
    
# print (stemmed_dataset[0:5])


# In[9]:


# print(len(stemmed_dataset))


# In[10]:


from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
X = cv.fit_transform(dataset['question'])


# In[11]:


from sklearn.naive_bayes import MultinomialNB


# In[12]:


X.shape


# In[13]:


y.shape


# In[14]:


mnb = MultinomialNB().fit(X.toarray(),y)


# In[15]:


Y = cv.transform(["polymorphism"])
prediction = mnb.predict(Y)
print(prediction)


# In[16]:


from sklearn.externals import joblib


# In[17]:


joblib.dump(mnb,'model_joblib')


# In[18]:


mj = joblib.load('model_joblib')


# In[19]:


Y = cv.transform(["What is an interface "])
mj.predict(Y)

