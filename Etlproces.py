#!/usr/bin/env python
# coding: utf-8

# In[48]:


#foldera te ndryshem me json files bashkohen ne nje csv te vetem 
import os
import pandas as pd
dfs = []
data_dir="jsonFiles";

#Bashkimi i disa json data files ne nje file csv te vetem 
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            df = pd.read_json(file_path)
            dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

print(f"Total rows combined: {combined_df.shape[0]}")


# In[49]:


# Percaktojme  file path-in e outputit
output_file_path = 'just_join_CSVfile.csv'

# Ruajme DataFramin ne nje CSV file
combined_df.to_csv(output_file_path, index=False)

print(f"Converted to CSV data in  {output_file_path}")


# In[49]:


# Fshirja e kollonave qe nuk na nevoiten per studim 
columns_to_remove = ['street', 'country_code', 'address_text', 'company_url', 'company_logo_url','latitude','longitude']
combined_df = combined_df.drop(columns=columns_to_remove)


# In[64]:


combined_df.head()


# In[65]:


# Check for NaN or null values in the DataFrame
null_values =combined_df.isnull().sum()

# Display the count of null values for each column
print(null_values)


# In[66]:


#Konvertojeme ne nje csv file 
df = pd.DataFrame(combined_df)


# In[67]:


# Normalize skills
skills_df = df.explode('skills')[['id', 'skills']].reset_index(drop=True)
skills_df = pd.concat([skills_df.drop(['skills'], axis=1), skills_df['skills'].apply(pd.Series)], axis=1)
skills_df = skills_df.rename(columns={"name": "skill_name", "level": "skill_level"})

# Normalize employment_types
employment_df = df.explode('employment_types')[['id', 'employment_types']].reset_index(drop=True)
employment_df = pd.concat([employment_df.drop(['employment_types'], axis=1), employment_df['employment_types'].apply(pd.Series)], axis=1)


# In[68]:


# Remove the original lists from the main DataFrame
df = df.drop(columns=['skills', 'employment_types'])


# In[69]:


# Display the normalized tables
print("Main Data Frame:")
print(df)


# In[70]:


print("\nSkills DataFrame:")
print(skills_df)


# In[71]:


print("\nEmployment Types DataFrame:")
print(employment_df)


# In[72]:


#Unifilikmi i te dhenave 


# In[73]:


#Fillimisht shohim tipin e te dhenave 


# In[74]:


print(df.dtypes)


# In[75]:


# Convert columns to appropriate data types
df['title'] = df['title'].astype(str)
df['city'] = df['city'].astype(str)
df['marker_icon'] = df['marker_icon'].astype(str)
df['workplace_type'] = df['workplace_type'].astype(str)
df['company_name'] = df['company_name'].astype(str)
df['company_size'] = df['company_size'].astype(str)
df['experience_level'] = df['experience_level'].astype(str)
df['published_at'] = pd.to_datetime(df['published_at'])
df['remote_interview'] = df['remote_interview'].astype(bool)
df['id'] = df['id'].astype(str)
df['remote'] = df['remote'].astype(bool)


# In[77]:


df.fillna('', inplace=True) 


# In[81]:


# Check for duplicate rows based on all columns
duplicates_all_columns = df[df.duplicated()]
print("Duplicate Rows Based on All Columns:")
print(duplicates_all_columns)


# In[82]:


# Fshirja e te dhenave to dublikuara
df = df.drop_duplicates()
print("\nDataFrame with Duplicates Removed (based on all columns):")
print(df)


# In[71]:


# Drop duplicates in skills_df
#skills_df = skills_df.drop_duplicates(subset=['id', 'skill_name', 'skill_level'])


# In[72]:


# Drop duplicates in employment_df
#employment_df = employment_df.drop_duplicates(subset=['id', 'type', 'salary'])


# In[29]:


df.head(10)


# In[74]:


df.to_csv('output.csv', index=False)


# In[76]:


skills_df.to_csv('output_skills.csv', index=False)


# In[77]:


employment_df.to_csv('output_employment.csv', index=False) 


# In[ ]:




