#!/usr/bin/env python
# coding: utf-8

# In[3]:


#data directory
datadir = "D:/Intern Project/Raw data/CollegeScorecard_Raw_Data"


# In[4]:


import warnings 
warnings.filterwarnings('ignore')


# In[5]:


#list of files in directory
#ls "D:/Intern Project/Raw data/CollegeScorecard_Raw_Data"


# In[6]:


#read in the 2009 data
COL = pd.read_csv(datadir + '/MERGED2009_10_PP.csv')


# In[7]:


COL.info()


# In[8]:


# Which columns have no NAs
col_dna = COL.dropna(axis=1)
col_dna.info()


# In[9]:


col_dtypes = dict(col_dna.dtypes.replace(np.dtype('int64'),np.dtype('float64'))) # make the dtypes floats
col_dtypes['UNITID'] = np.dtype('int64') # convert the UNITID back to int
vars_interest = ['ADM_RATE','UGDS','TUITIONFEE_IN','TUITIONFEE_OUT','MN_EARN_WNE_P10'] # Include these vars
col_dtypes.update({a: np.dtype('float64') for a in vars_interest}) # make them floats


# In[10]:


col_try_again = pd.read_csv(datadir + '/MERGED2009_10_PP.csv',na_values='PrivacySuppressed',
                            dtype=col_dtypes,usecols=col_dtypes.keys())
col_try_again.info()


# In[11]:


col_try_again['Year'] = pd.Period('2010',freq='Y')


# In[12]:


def read_cs_data(year,col_dtypes,datadir):
    """read a CollegeScorecard dataframe"""
    nextyr = str(int(year) + 1)[-2:]
    filename = datadir + '/MERGED{}_{}_PP.csv'.format(year,nextyr)
    col = pd.read_csv(filename,na_values='PrivacySuppressed',
                      dtype=col_dtypes,usecols=col_dtypes.keys())
    col['Year'] = pd.Period(str(int(year) + 1),freq='Y')
    return col


# In[13]:


col = pd.concat((read_cs_data(str(y),col_dtypes,datadir) for y in range(1999,2018)))
col = col.set_index(['UNITID','Year'])


# In[14]:


col.head()


# In[15]:


col.UGDS.sum()


# In[16]:


x = col.groupby('Year').sum()['UGDS']
x = pd.DataFrame(x)
x


# In[17]:


x = x.drop(x.index[1])
x


# # Undergraduates enrollment from 2000 to 2018

# In[57]:


ax = x.plot(y='UGDS', linestyle = '-', marker = 'o', figsize=(15,8))
ax.set_title('undergraduate Enrollment')
ax.set_ylabel('UG Enrollment')
plt.xticks(fontsize=12)
plt.show()


# In[48]:


plt.figure(figsize=(20, 20))
ax = x.plot(y='UGDS',linestyle = '-', marker = 'o')
ax.set_title('undergraduate pop.')
ax.set_ylabel('UG Enrollment')
plt.show()


# In[ ]:


y = col.groupby('STABBR').sum()['UGDS']
y = pd.DataFrame(y)
y = y.rename(columns=lambda x:x.strip())
y.head()


# In[ ]:


y['STABBR'] = y.index
y.head()


# In[ ]:


plt.figure(figsize=(10,6))
ax = y.plot(y='UGDS')
ax.set_title('undergraduate pop.')
ax.set_ylabel('UG Enrollment')
plt.legend()


# In[ ]:


sns.set_style('dark')
plt.figure(figsize = (16, 16))
ax = sns.barplot(y.STABBR.value_counts().values, list(y.STABBR.value_counts().index), 
           palette = sns.color_palette('bright', len(y.STABBR.value_counts())))
for p in ax.patches:
    width = p.get_width()
    plt.text(20+p.get_width(), p.get_y()+0.55*p.get_height(),
             '{:1.0f}'.format(width),
             ha='center', va='center', fontsize = 12)
plt.title('Number of undergraduate enrollments per state', fontsize = 15)
plt.xlabel('Number of under graduates', fontsize = 13)
plt.ylabel('State Code', fontsize = 13)
plt.xticks([], [])
plt.yticks(fontsize = 12)

plt.tight_layout();


# In[ ]:


plt.figure(figsize = (7, 4))
sdvzs = sns.barplot(data = y , x = 'UGDS' , y = 'STABBR', color = sns.color_palette()[0])
for p in sdvzs.patches:
    width = p.get_width()
    plt.text(20+p.get_width()/0.9555, p.get_y()+0.55*p.get_height(),
             '{:1.0f}'.format(width),
             ha='center', va='center',fontsize = 12)


# In[ ]:




