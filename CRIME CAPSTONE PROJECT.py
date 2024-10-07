#!/usr/bin/env python
# coding: utf-8

# <div style="text-align:left;">
#     <img src="Datafied logo.jpg" alt="Datafied Logo" width="120" height="10">
# </div>
# 
# # CRIME CAPSTONE PROJECT
# 
# © Datafied Academy

# ###  Data and Setup

# ____
# **Import numpy and pandas**

# In[1]:


import numpy as np
import pandas as pd


# **Import visualization libraries and set %matplotlib inline.**

# In[2]:


import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# **Read in the excel file and merge as a dataframe called crime**

# In[4]:


# Load the Excel file
#file_path = 'path_to_your_file.xlsx'  # Replace with the actual path to your Excel file
excel_file = pd.ExcelFile('prc-pfa-mar2013-onwards-tables-191023.xlsx')


# In[5]:


# Filter out the sheets with years in their names (2012-13 to 2023-24)
sheets_to_merge = [sheet for sheet in excel_file.sheet_names if any(year in sheet for year in ['2012-13', '2013-14', '2014-15',\
                                                                                               '2015-16', '2016-17','2017-18',\
                                                                                               '2018-19','2019-20','2020-21',\
                                                                                               '2021-22','2022-23', '2023-24'])]

# Initialize an empty DataFrame to hold the merged data
merged_data = pd.DataFrame()

# Loop through the relevant sheets and append their data to the merged DataFrame
for sheet in sheets_to_merge:
    sheet_data = pd.read_excel(excel_file, sheet_name=sheet)
    merged_data = pd.concat([merged_data, sheet_data], ignore_index=True)

# Drop the "offence" column if it exists
if 'offence' in merged_data.columns:
    merged_data = merged_data.drop(columns=['offence'])

# Drop rows where numeric columns have negative or zero values
numeric_columns = merged_data.select_dtypes(include=['number']).columns
merged_data = merged_data[(merged_data[numeric_columns] > 0).all(axis=1)]


# In[6]:


# Save the final merged DataFrame to an Excel file
merged_data.to_excel('merged_output.xlsx', index=False)


# **New Dataset Merged**

# In[3]:


crime = pd.read_excel('merged_output.xlsx')


# ### Data Frame Inspection

# **Checking the column header**

# In[62]:


print(crime.columns)


# **Show concise summary information about the DataFrame**

# In[63]:


crime.info()


# **Show the summary statistics of numeric columns**

# In[64]:


crime.describe()


# **The first 5 rows of the DataFrame**

# In[65]:


crime.head()


# **The last first 5 rows of the DataFrame**

# In[66]:


crime.tail()


# ### Analyzing the crime dataset

# In[ ]:





# In[10]:


offences_per_year = crime.groupby('Financial Year')['Number of Offences'].sum().reset_index()
plt.figure(figsize=(10,6))
plt.bar(offences_per_year['Financial Year'], offences_per_year['Number of Offences'])
plt.title('Total Offences by Year')
plt.xlabel('Financial Year')
plt.ylabel('Number of Offences')
plt.xticks(rotation=89)
plt.show()


# **Offence Breakdown in 2022/23**

# In[6]:


# Filter, group, and plot in a single line
crime[crime['Financial Year'] == '2022/23'] \
    .groupby('Offence Group')['Number of Offences'].sum() \
    .plot(kind='bar', figsize=(10,6), color='skyblue', title='Offence Breakdown in 2022/23')

# Customize labels and grid
plt.ylabel('Number of Offences')
plt.xlabel('Offence Group')
plt.xticks(rotation=89)
plt.grid(True)

# Show the plot
plt.show()


# **Offence Breakdown in 2021/22**

# In[8]:


# Filter, group, and plot in a single line
crime[crime['Financial Year'] == '2021/22'] \
    .groupby('Offence Group')['Number of Offences'].sum() \
    .plot(kind='bar', figsize=(10,6), color='skyblue', title='Offence Breakdown in 2021/22')

# Customize labels and grid
plt.ylabel('Number of Offences')
plt.xlabel('Offence Group')
plt.xticks(rotation=89)
plt.grid(True)

# Show the plot
plt.show()


# In[ ]:





# **Crime trend over time**

# In[68]:


# Convert 'Financial Year' and 'Financial Quarter' into a single datetime column for trend analysis
crime['Year_Quarter'] = crime['Financial Year'] + ' Q' + crime['Financial Quarter'].astype(str)

# Group by the newly created 'Year_Quarter' column to get the total number of offences for each period
crime_trends = crime.groupby('Year_Quarter')['Number of Offences'].sum().reset_index()

# Plot the crime trends
plt.figure(figsize=(12, 6))
plt.plot(crime_trends['Year_Quarter'], crime_trends['Number of Offences'], marker='o')
plt.xticks(rotation=45)
plt.title('Crime Trends Over Time')
plt.xlabel('Year and Quarter')
plt.ylabel('Number of Offences')
plt.grid(True)
plt.show()


# **Offence Description by the total number**

# In[69]:


# Group by 'Offence Description' to get the total number of offences for each type
top_crime_types = crime.groupby('Offence Description')['Number of Offences'].sum().reset_index()

# Sort to get the top 10 crime types
top_crime_types = top_crime_types.sort_values(by='Number of Offences', ascending=False).head(10)

# Plot the top crime types
plt.figure(figsize=(12, 6))
plt.barh(top_crime_types['Offence Description'], top_crime_types['Number of Offences'], color='orange')
plt.title('Top 10 Crime Types')
plt.xlabel('Number of Offences')
plt.ylabel('Offence Description')
plt.show()



# **Top five (5) force with the highest number of offence**

# In[82]:


# Group by 'Force Name' to get the total number of offences for each force, sort and get top 5
crimes_by_force = crime.groupby('Force Name')['Number of Offences'].sum().sort_values(ascending=False).head(5).reset_index()

# Create a donut chart
plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(crimes_by_force['Number of Offences'], labels=crimes_by_force['Force Name'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'], wedgeprops={'edgecolor': 'black'}, textprops=dict(color="black"))

# Create a circle at the center to make it a donut chart
centre_circle = plt.Circle((0,2),0.70,fc='white')
plt.gca().add_artist(centre_circle)

# Change the font size and color of the percentage labels inside the donut
for autotext in autotexts:
    autotext.set_color('black')
    autotext.set_fontsize(12)
plt.title('Top 5 Police Forces by Number of Crimes')
plt.show()


# **Top ten (10) Offence Subgroup by the number of Offences**

# In[58]:


# Group by 'Offence Subgroup' to get the total number of offences for each subgroup, and then sort by 'Number of Offences'
crimes_by_subgroup = crime.groupby('Offence Subgroup')['Number of Offences'].sum().sort_values(ascending=False).head(10).reset_index()

# Plot the crimes by offence subgroup
plt.figure(figsize=(12, 6))
plt.barh(crimes_by_subgroup['Offence Subgroup'], crimes_by_subgroup['Number of Offences'])
plt.title('Top 10 Crimes by Offence Subgroup (Descending Order)')
plt.xlabel('Number of Offences')
plt.ylabel('Offence Subgroup')
plt.xticks(rotation=45)
plt.gca().invert_yaxis()  # Invert the y-axis to display the highest values at the top
plt.show()


# **Financial Quarter and Offence Group for each quater**

# In[52]:


# Group by 'Financial Quarter' and 'Offence Group' to get the total number of offences for each quarter
crimes_by_quarter_group = crime.groupby(['Financial Quarter', 'Offence Group'])['Number of Offences'].sum().unstack().fillna(0)

# Plot the grouped bar chart
crimes_by_quarter_group.plot(kind='bar', figsize=(12, 8), stacked=True)
plt.title('Crimes by Offence Group Across Financial Quarters')
plt.xlabel('Financial Quarter')
plt.ylabel('Number of Offences')
plt.xticks(rotation=0)
plt.show()


# **Crime Reduction by Police Force Over Time**

# In[21]:


# Group by 'Financial Year', 'Force Name', and 'Offence Group' to sum 'Number of Offences'
force_effectiveness = crime.groupby(['Financial Year', 'Force Name', 'Offence Group'])['Number of Offences'].sum().unstack()

# Plot
force_effectiveness.plot(figsize=(12, 6))
plt.title('Crime Reduction by Police Force Over Time')
plt.xlabel('Financial Year')
plt.ylabel('Number of Offences')
plt.xticks(rotation=45)
plt.legend(title='Offence Group', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.show()


# **Number of Offence by Police Force over Financial Years**

# In[53]:


# Group by 'Financial Year' and 'Force Name' to get the total number of offences for each police force over time
offences_by_force_year = crime.groupby(['Financial Year', 'Force Name'])['Number of Offences'].sum().unstack().fillna(0)

# Plot the line chart
offences_by_force_year.plot(figsize=(12, 8))
plt.title('Number of Offences by Police Force Over Financial Years')
plt.xlabel('Financial Year')
plt.ylabel('Number of Offences')
plt.xticks(rotation=45)
plt.legend(title='Police Force', loc='upper left', bbox_to_anchor=(1,1))
plt.grid(True)
plt.show()


# **Total crime by month across each year**

# In[56]:


# Extract the month from the financial quarter
crime['Month'] = crime['Financial Quarter'].apply(lambda x: 'Q' + str(int(x)))

# Group by 'Month' to get the total number of offences across all years
crimes_by_month = crime.groupby('Month')['Number of Offences'].sum().reset_index()

# Plot the line chart
plt.figure(figsize=(12, 6))
sns.lineplot(x='Month', y='Number of Offences', data=crimes_by_month, marker='o')
plt.title('Total Crimes by Month Across Years')
plt.xlabel('Month')
plt.ylabel('Number of Offences')
plt.grid(True)
plt.show()


# **Heatmap for number of crime by Offence Group over Financial year**

# In[48]:


# Group by 'Financial Year' and 'Offence Group' to get the total number of offences
offences_by_year_group = crime.groupby(['Financial Year', 'Offence Group'])['Number of Offences'].sum().unstack().fillna(0)

# Plot the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(offences_by_year_group, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Number of Crimes by Offence Group Over Financial Years')
plt.xlabel('Offence Group')
plt.ylabel('Financial Year')
plt.show()


# **Clustermap of Crime by Offence Group over Financial Year**

# In[49]:


# Plot a clustermap based on the number of offences by offence group over financial years
plt.figure(figsize=(12, 12))
sns.clustermap(offences_by_year_group, cmap='viridis', linewidths=0.5, figsize=(12, 12))
plt.title('Clustermap of Crimes by Offence Group Over Financial Years')
plt.show()


# In[13]:






# # INSIGHT AND RECOMMENDATION

# 
# ### 1. **Target High-Crime Areas**
#    - **Focus**: Direct resources to regions and offence types with the highest crime rates (e.g., theft, assault).
#    - **Action**: Increase patrols and deploy specialized units in hotspots.
# 
# ### 2. **Address Seasonal Crime Spikes**
#    - **Focus**: Prepare for seasonal crime increases during high-crime periods (e.g., summer, holidays).
#    - **Action**: Boost police presence and run awareness campaigns in peak months.
# 
# ### 3. **Monitor Rising Crime Subgroups**
#    - **Focus**: Pay attention to offence types showing rising trends (e.g., violence without injury,Criminaldamage, domestic violence etc).
#    - **Action**: Develop targeted strategies and specialized training for emerging crime types.
# 
# ### 4. **Evaluate Police Force Performance**
#    - **Focus**: Assess the crime-handling effectiveness of different police forces.
#    - **Action**: Allocate resources and support to forces dealing with high crime volumes or areas needing improvement.
# 
# ### 5. **Use Predictive Policing**
#    - **Focus**: Leverage historical data to forecast future crime trends and hotspots.
#    - **Action**: Implement predictive models to anticipate crime and deploy resources proactively.

# ## Thank You
# 
#   **Presented by Ayanfe Isaiah Olabamiji**

# In[ ]:




