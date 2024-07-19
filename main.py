
import plotly.express as px
import streamlit as st
import pandas as pd

@st.cache
def load_data():
    return pd.read_csv('C:/Users/User/Downloads/output.csv')

df = load_data()


st.title('Job Listings Dashboard')


st.sidebar.header('Filters')
city_filter = st.sidebar.multiselect('City', options=df['city'].unique(), default=df['city'].unique())
experience_level_filter = st.sidebar.multiselect('Experience Level', options=df['experience_level'].unique(), default=df['experience_level'].unique())
workplace_type_filter = st.sidebar.multiselect('Workplace Type', options=df['workplace_type'].unique(), default=df['workplace_type'].unique())
remote_filter = st.sidebar.selectbox('Remote', options=[True, False, 'All'], index=2)


filtered_df = df[(df['city'].isin(city_filter)) &
                 (df['experience_level'].isin(experience_level_filter)) &
                 (df['workplace_type'].isin(workplace_type_filter))]

if remote_filter != 'All':
    filtered_df = filtered_df[filtered_df['remote'] == remote_filter]


st.write('### Filtered Job Listings')
st.write(filtered_df)


st.write('### Data Summary')
st.write(filtered_df.describe(include='all'))


st.write('### Visualizations')


st.write('#### Number of Jobs by City')
city_count = filtered_df['city'].value_counts()
st.bar_chart(city_count)


st.write('#### Number of Jobs by Experience Level')
exp_count = filtered_df['experience_level'].value_counts()
st.bar_chart(exp_count)

st.write('#### Number of Jobs by Company')
company_count = filtered_df['company_name'].value_counts()
st.bar_chart(company_count)

if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(df)


#Visualise skills

skills_df =pd.read_csv('C:/Users/User/Downloads/output_skills.csv')

# Display the original data
st.subheader('Skills Data')
st.write(skills_df)


# Analyze the skill levels
st.subheader('Skill Level Analysis')

# Most common skill levels
skill_level_counts = skills_df['skill_level'].value_counts().reset_index()
skill_level_counts.columns = ['skill_level', 'count']

st.write(skill_level_counts)

# Plot the skill level distribution
fig = px.bar(skill_level_counts, x='skill_level', y='count', title='Skill Level Distribution')
st.plotly_chart(fig)

# Skill level distribution per skill
skill_level_per_skill = skills_df.groupby(['skill_name', 'skill_level']).size().reset_index(name='count')

fig_skill_level = px.bar(skill_level_per_skill, x='skill_name', y='count', color='skill_level', barmode='group',
                         title='Skill Level Distribution per Skill')
st.plotly_chart(fig_skill_level)

# Save the deduplicated data to a new CSV file
skills_df.to_csv('skills_df.csv', index=False)

# Provide a download link for the deduplicated CSV file
st.subheader('Download this Data')
st.download_button(
    label="Download CSV",
    data=skills_df.to_csv(index=False),
    file_name='skills_dfd.csv.csv',
    mime='text/csv'
)


#Visualise salary
import streamlit as st
import pandas as pd
import plotly.express as px

employment_df = pd.read_csv('C:/Users/User/Downloads/output_employment.csv')
st.subheader('Salary Analysis')

# Display the original data
st.subheader('Original Data')
st.write(employment_df)

# Parse the 'salary' column
def parse_salary(salary):
    try:
        return eval(salary.replace('pln', "'pln'"))
    except:
        return None

employment_df['salary'] = employment_df['salary'].apply(parse_salary)

# Average salary by type
def calculate_avg_salary(salary):
    if salary is not None:
        return (salary['from'] + salary['to']) / 2
    return None

employment_df['avg_salary'] = employment_df['salary'].apply(calculate_avg_salary)

avg_salary_by_type = employment_df.dropna(subset=['avg_salary']).groupby('type')['avg_salary'].mean().reset_index()
avg_salary_by_type.columns = ['type', 'avg_salary']

st.write(avg_salary_by_type)

# Plot average salary by type
fig_avg_salary = px.bar(avg_salary_by_type, x='type', y='avg_salary', title='Average Salary by Type')
st.plotly_chart(fig_avg_salary)

# Salary distribution by type
salary_dist_by_type = employment_df.dropna(subset=['avg_salary']).groupby(['type', 'avg_salary']).size().reset_index(name='count')

fig_salary_dist = px.histogram(salary_dist_by_type, x='avg_salary', color='type', barmode='overlay', title='Salary Distribution by Type')
st.plotly_chart(fig_salary_dist)

# Comparison of B2B vs. permanent salaries
b2b_salaries = employment_df[employment_df['type'] == 'b2b'].dropna(subset=['avg_salary'])['avg_salary']
permanent_salaries = employment_df[employment_df['type'] == 'permanent'].dropna(subset=['avg_salary'])['avg_salary']

comparison_df = pd.DataFrame({
    'b2b': b2b_salaries,
    'permanent': permanent_salaries
})

st.subheader('B2B vs. Permanent Salary Comparison')
st.write(comparison_df.describe())

employment_df.to_csv('emp_data.csv', index=False)
st.write('Download  Data')
st.download_button(
    label="Download CSV",
    data=employment_df.to_csv(index=False),
    file_name='emp_data.csv',
    mime='text/csv'
)
