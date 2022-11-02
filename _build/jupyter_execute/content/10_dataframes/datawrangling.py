#!/usr/bin/env python
# coding: utf-8

# # Wrangling behavorial data generated by OpenSesame
# 

# ## Introduction
# You build the experiment and ran your first participant. Now, it is time to take a look at the data you have collected.
# 
# OpenSesame outputs a *comma-separated values (csv)* file. This is a very widely used format, and you can painlessly import this file type in Python using the datafile package **pandas**. Let's import a datafile from two participants and merge those in one file:
# 
# 

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt

subj1 = pd.read_csv("data/subject-1.csv", sep=",")
subj2 = pd.read_csv("data/subject-2.csv", sep=",")

df = pd.concat([subj1, subj2], ignore_index=True)
df


# That's a lot of columns. In your "logger" file in OpenSesame, the recommended thing to do is to check the box of "Log all variables". This is the safest option, because it's easy to remove columns and you would rather not have that you missed an essential variable after doing your experiment. Let's pick the columns that we need:
# 

# In[2]:


include_columns = ['subject_nr', 'block', 'congruency_transition_type', 'congruency_type',
                   'correct', 'response_time', 'task_transition_type', 'task_type']

df_trim = df[include_columns]
df_trim


# Alright, it's getting a bit more uncluttered now. The task-design is so that the last two blocks are different kind of blocks. We don't have to go in details now, but for further analysis we will have to create a dataframe without block 11 and 12. There are [many ways to conditional selection of rows](https://www.geeksforgeeks.org/selecting-rows-in-pandas-dataframe-based-on-conditions/), but here we opt to use the information that we need all blocks with a value smaller than 11.

# In[3]:


# Here the last blocks should be 12
print(df_trim.tail(5))

# Conditionally select rows based on if the value in the "block" column is lower than 11
df_trim_blocks = df_trim[df_trim['block'] < 11]

# Check to see if the last block is now 10 instead of 12
print(df_trim_blocks.tail(5))


# In[4]:


#check counts
pd.pivot_table(
    df_trim,
    values="correct",
    index=["subject_nr"],
    columns=["congruency_type"],
    aggfunc=len,
)

df_trim['task_type'].value_counts()
df_trim['congruency_type'].value_counts()
df_trim['congruency_transition_type'].value_counts()


#  Let's get a feel wat we are dealing with.

# In[5]:


#dataframe syntax
plt.figure(figsize=(8,6));
plt.hist(df_trim_blocks.query("task_transition_type == 'task-switch'").response_time, bins=100, alpha=0.5, label="Task switches");
plt.hist(df_trim_blocks.query("task_transition_type == 'task-repetition'").response_time, bins=100, alpha=0.5, label="Task repetitions");


# In[6]:


#df.head()

#df['acc']
#df.acc

#df.iloc[1]

#print(df['congruency'])

#df.shape

#dfg = df.groupby('subject_nr')
#dfg.mean()

#df.groupby('subject_nr').agg([np.sum, np.mean, np.std])


df_trim_blocks['rt_zscore'] = df.groupby(['subject_nr','task_transition_type'])['response_time'].transform(lambda x: (x-x.mean())/x.std())

print(df_trim_blocks)


# In[7]:


plt.figure(figsize=(8,6));
plt.hist(df.query("congruency == 'inc' & rt_zscore <= 3").response_time, bins=100, alpha=0.5, label="data1");
plt.hist(df.query("congruency == 'inc' & rt_zscore > 3").response_time, bins=100, alpha=0.5, label="data2");


# In[8]:


import seaborn as sns

df['is_outlier'] = df['rt_zscore'] > 3

sns.set_theme(style="darkgrid")
sns.displot(
    df.query("subject_nr != 0"), x="response_time", col="congruency", row="subject_nr",
    binwidth=10, height=3, facet_kws=dict(margin_titles=True), hue = "is_outlier",
)


# In[9]:


df


# In[10]:


df_sum = df.query("rt_zscore <= 3").groupby(['subject_nr','congruency'])['response_time'].mean()


# In[11]:


df_sum


# In[ ]:




