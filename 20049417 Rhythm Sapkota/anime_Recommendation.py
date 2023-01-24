#!/usr/bin/env python
# coding: utf-8

# In[ ]:



import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')



# In[5]:


anime = pd.read_csv(r'C:\Users\Rhythm sapkota\Desktop\AI Coursework\anime.csv')
print(anime)
df = pd.read_csv(r'C:\Users\Rhythm sapkota\Desktop\AI Coursework\rating.csv')
print(df)


# In[6]:


df = pd.merge(df,anime.drop('rating',axis=1),on='anime_id')
df.head()


# In[7]:


df.groupby('name')['rating'].mean().sort_values(ascending=False).head(10)
df.groupby('name')['rating'].count().sort_values(ascending=False).head(10)


# In[8]:


ratings = pd.DataFrame(df.groupby('name')['rating'].mean())
ratings['num of ratings'] = pd.DataFrame(df.groupby('name')['rating'].count())

genre_dict = pd.DataFrame(data=anime[['name','genre']])
genre_dict.set_index('name',inplace=True)
ratings.head()


# In[9]:


plt.figure(figsize=(15,5))
ratings['num of ratings'].hist(bins=300)
plt.xlim(0,3000)


# In[10]:


ratings['rating'].hist(bins=50)


# In[11]:


sns.jointplot(x='rating',y='num of ratings',data=ratings)


# In[12]:


def check_genre(genre_list,string):
    if any(x in string for x in genre_list):
        return True
    else:
        return False
    
def get_recommendation(name):
    #generating list of anime with the same genre with target
    anime_genre = genre_dict.loc[name].values[0].split(', ')
    cols = anime[anime['genre'].apply(
        lambda x: check_genre(anime_genre,str(x)))]['name'].tolist()
    
    #create matrix based on generated list
    animemat = df[df['name'].isin(cols)].pivot_table(
        index='user_id',columns='name',values='rating')
       
    #create correlation table
    anime_user_rating = animemat[name]
    similiar_anime = animemat.corrwith(anime_user_rating)
    corr_anime = pd.DataFrame(similiar_anime,columns=['correlation'])
    corr_anime = corr_anime.join(ratings['num of ratings'])
    corr_anime.dropna(inplace=True)
    corr_anime = corr_anime[corr_anime['num of ratings']>5000].sort_values(
        'correlation',ascending=False)
    
    return corr_anime.head(10)


# In[13]:


get_recommendation('Shingeki no Kyojin')


# In[14]:


get_recommendation('Naruto')


# In[ ]:




