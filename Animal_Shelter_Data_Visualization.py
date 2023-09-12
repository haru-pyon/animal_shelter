#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# In[28]:


# Using Data provided by City of Long Beach
"""
https://data.longbeach.gov/explore/dataset/animal-shelter-intakes-and-outcomes/information/?disjunctive.animal_type&disjunctive.primary_color&disjunctive.sex&disjunctive.intake_cond&disjunctive.intake_type&disjunctive.reason&disjunctive.outcome_type&disjunctive.outcome_subtype&disjunctive.intake_is_dead&disjunctive.outcome_is_dead
"""
df = pd.read_csv("animal.csv")


# In[5]:


# Deleting a row that showed cat age is -7
df = df[df["Animal ID"] != "A656513"]
# Creating age groups (bins)
bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 26]
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21-26']
df['Age Group'] = pd.cut(df['Age'], bins=bins, labels=labels)
df['Is Adopted'] = df["Outcome Type"] == 'ADOPTION'
df["Is Euthanized"] = df["Outcome Type"] == 'EUTHANASIA'


# # Adoption and Euthanization Rate by Age for Dogs

# In[6]:


# Set the font style for Seaborn
sns.set(style="darkgrid", font_scale=1.2, rc={"font.family": "Georgia"},
       palette="Set2")


# In[7]:


# Filter the DataFrame to include only "DOG" entries
df_dogs = df[df["Animal Type"] == "DOG"]

# Melt the DataFrame to combine "Is Euthanized" and "Is Adopted" into one variable
df_dogs_melted = pd.melt(df_dogs, id_vars=["Age Group"], value_vars=["Is Euthanized", "Is Adopted"], var_name="Status")

# Create the grouped bar plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_dogs_melted, x="Age Group", y="value", hue="Status", 
            errorbar = None, palette="Set2", linewidth=2)

plt.title('Adoption and Euthanization Rate by Age for Dog', fontsize=25)
plt.xlabel("Age", fontsize = 20)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel('Rate', fontsize=20)
plt.ylim(0, 0.3)  # Set the y-axis limits to show proportions
plt.legend(title='Outcome', loc='upper right', fontsize=20)
plt.show()


# # Outcome Rates for Dogs by Age

# In[9]:


selected_outcome = ['RESCUE', 'EUTHANASIA', 'ADOPTION', 'RETURN TO OWNER',
                   "TRANSFER", "DIED"]
filtered_df = df[(df['Animal Type'] == 'DOG') & (df['Outcome Type'].isin(selected_outcome))]

# Group by 'Age Group' and 'Outcome Type', and calculate counts
grouped = filtered_df.groupby(['Age Group', 'Outcome Type']).size().unstack(fill_value=0)

# Calculate the total number of dogs in each age group
total_dogs = grouped.sum(axis=1)

# Calculate the outcome rate (percentage) for each age group and outcome type
outcome_rates = grouped.div(total_dogs, axis=0) * 100

# Create a stacked bar plot to visualize outcome rates
plt.figure(figsize=(20, 10))
outcome_rates.plot(kind='bar', stacked=True, cmap='Set2', edgecolor='k')
plt.title('Outcome Rates for Dogs by Age', fontsize=25)
plt.xlabel('Age')
plt.ylabel('Outcome Rate (%)')

# Set the legend outside and to the right
plt.legend(title='Outcome Type', bbox_to_anchor=(1, 1), loc='upper left')
plt.xticks(rotation=45)

plt.show()


# # Oucome Rates for Dogs by Age

# In[10]:


good_outcome = ['RESCUE', 'ADOPTION', 'RETURN TO OWNER','HOMEFIRST', 'SHELTER, NEUTER, RETURN',
                   "FOSTER TO ADOPT", "RETURN TO RESCUE", "FOSTER", "COMMUNITY CAT"]
bad_outcome = ["EUTHANASIA", "DIED", "DISPOSAL"]
unknown_outcome = ["TRANSFER", "TRANSPORT", "MISSING"]


# In[11]:


# Create a function to categorize outcome types
def categorize_outcome(outcome):
    if outcome in good_outcome:
        return 'Desired'
    elif outcome in bad_outcome:
        return 'Undesirable'
    elif outcome in unknown_outcome:
        return 'Unknown'
    else:
        return 'Others'

# Apply the categorization function to create a new column 'Outcome Category'
df['Outcome Category'] = df['Outcome Type'].apply(categorize_outcome)


# In[12]:


# Group by 'Age Group' and 'Outcome Type', and calculate counts
grouped = df.groupby(['Age Group', 'Outcome Category']).size().unstack(fill_value=0)

# Calculate the total number of dogs in each age group
total_dogs = grouped.sum(axis=1)

# Calculate the outcome rate (percentage) for each age group and outcome type
outcome_rates = grouped.div(total_dogs, axis=0) * 100

# Create a stacked bar plot to visualize outcome rates
plt.figure(figsize=(20, 10))
outcome_rates.plot(kind='bar', stacked=True, cmap='Set2', edgecolor='k')
plt.title('Outcome Rates for Dogs by Age', fontsize =25)
plt.xlabel('Age')
plt.ylabel('Outcome Rate (%)')

# Set the legend outside and to the right
plt.legend(title='Outcome Category', bbox_to_anchor=(1, 1), loc='upper left')

plt.xticks(rotation=45)
plt.show()


# # Compare Dogs and Cats

# In[13]:


# Filter the DataFrame to include only "DOG" entries
df_dogs = df[df["Animal Type"] == "DOG"]
df_cats = df[df["Animal Type"] == "CAT"]

# Melt the DataFrame to combine "Is Euthanized" and "Is Adopted" into one variable
df_dogs_melted = pd.melt(df_dogs, id_vars=["Age Group"], value_vars=["Is Euthanized", "Is Adopted"], var_name="DOG")
df_cats_melted = pd.melt(df_cats, id_vars=["Age Group"], value_vars=["Is Euthanized", "Is Adopted"], var_name="CAT")

# Create two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot lines for dogs on the first subplot
sns.lineplot(data=df_dogs_melted, x="Age Group", y="value", hue="DOG",
             errorbar=None,  ax=axes[0], linewidth=3)
axes[0].set_title('Dogs', fontsize=20)
axes[0].set_xlabel("Age")
axes[0].set_ylabel('Rate')
axes[0].set_ylim(0, 0.5)  
axes[0].tick_params(axis='x', rotation=45,
                   labelsize=15)  
axes[0].legend(title='Legend', loc='upper right')

# Plot lines for cats on the second subplot
sns.lineplot(data=df_cats_melted, x="Age Group", y="value", hue="CAT",
             errorbar=None,  ax=axes[1], linewidth=3)
axes[1].set_title('Cats', fontsize=20)
axes[1].set_xlabel('Age')
axes[1].set_ylabel('Rate')
axes[1].set_ylim(0, 0.5) 
axes[1].tick_params(axis='x', rotation=45,
                   labelsize=15)  
axes[1].legend(title='Outcome', loc='upper left')

# Add a shared title across both subplots
plt.suptitle('Adoption and Euthanization Rate', fontsize=25)

# Adjust spacing between subplots
plt.tight_layout()

plt.show()


# # Outcome Rates for Cats by Age

# In[14]:


selected_outcome = ['RESCUE', 'EUTHANASIA', 'ADOPTION', 'RETURN TO OWNER',
                   "TRANSFER", "COMMUNITY CAT"]
filtered_df = df[(df['Animal Type'] == 'CAT') & (df['Outcome Type'].isin(selected_outcome))]

# Group by 'Age Group' and 'Outcome Type', and calculate counts
grouped = filtered_df.groupby(['Age Group', 'Outcome Type']).size().unstack(fill_value=0)

# Calculate the total number of cats in each age group
total_cats = grouped.sum(axis=1)

# Calculate the outcome rate (percentage) for each age group and outcome type
outcome_rates = grouped.div(total_cats, axis=0) * 100

# Create a stacked bar plot to visualize outcome rates
plt.figure(figsize=(20, 10))
outcome_rates.plot(kind='bar', stacked=True, cmap='Set2', edgecolor='k')
plt.title('Outcome Rates for Cats by Age', fontsize = 25)
plt.xlabel('Age')
plt.ylabel('Outcome Rate (%)')

# Set the legend outside and to the right
plt.legend(title='Outcome Type', bbox_to_anchor=(1, 1), loc='upper left')

plt.xticks(rotation=45)
plt.show()


# # Color

# In[16]:


# Specify the specific value to use for NaNs (e.g., a specific day)
specific_day = "2023-09-08"  # Replace with your desired specific day

# Replace NaN values in the "Difference" column wicth the specific day
df["Outcome Date"].fillna(pd.Timestamp(specific_day), inplace=True)

dp_df = pd.DataFrame({
    "Intake": df["Intake Date"].tolist(),
    "Outcome": df["Outcome Date"].tolist(),
})

# Convert the "Intake" and "Outcome" columns to datetime objects
dp_df["Intake"] = pd.to_datetime(dp_df["Intake"])
dp_df["Outcome"] = pd.to_datetime(dp_df["Outcome"])

# Calculate the difference between the two data points and create a new column
df["Time spent at Shelter"] = dp_df["Outcome"] - dp_df["Intake"]

# Find the value from the specific row that does not show the time properly
# df.loc[df["Time spent at Shelter"].isna(), "Time spent at Shelter"]
replacement_value = df.loc[39515, "Time spent at Shelter"]

# Replace NaT values with the replacement value
df["Time spent at Shelter"].fillna(replacement_value, inplace=True)


# In[17]:


def categorize_dog_color(color_name):
    white_colors = ['WHITE']
    brown_chocolate_colors = ['BROWN', 'CHOCOLATE', 'BR BRINDLE', 'TAN', 
                              "FAWN", 'BUFF', 'BLONDE', 'WHEAT', 'APRICOT', 'PEACH',
                             "BRN TABBY"]
    black_colors = ['BLACK', 'BLK TABBY', 'BLK SMOKE', 'BLK TIGER']
    yellow_golden_colors = ['YELLOW', 'GOLD', 'Y BRINDLE', "CREAM",
                           "CRM TIGER"]
    gray_colors = ['GRAY', 'GRAY TABBY', 'SILVER', 'GRAY TIGER', 'SLVR TABBY',
                  "GREEN"]
    red_colors = ['RED', 'RED MERLE', 'ORG TIGER','BRN MERLE', 'SEAL', 'SABLE', 
                  'DAPPLE', 'RUDDY', 'BRN TIGER', 'CR LYNX PT', 'LC LYNX PT', 
                  'TORBI', 'L-C PT', 'C-T PT', 'S-T PT', 'ST LYNX PT', 'LILAC PT',
                  'B-C PT', "PINK", "LIVER", "LIVER TICK"]
    blue_colors = ['BLUE', 'BLUE PT', 'BLUE MERLE', 'BLUE BRIND', 'BLUE TABBY', 'BLUE CREAM', 'BLUE FAWN',
                  "PURPLE", "BL BRINDLE", "BLUE TICK"]
    orange_colors = ['ORANGE', 'ORG TABBY', 'CREAM TABBY', 'CREAM PT']
    multi_colors = ["TORTIE", "TRICOLOR", "CALICO"]
    
    if color_name in white_colors:
        return 'WHITE'
    elif color_name in brown_chocolate_colors:
        return 'BROWN/CHOCOLATE'
    elif color_name in black_colors:
        return 'BLACK'
    elif color_name in yellow_golden_colors:
        return 'YELLOW/GOLDEN'
    elif color_name in gray_colors:
        return 'GRAY'
    elif color_name in red_colors:
        return 'RED'
    elif color_name in blue_colors:
        return 'BLUE'
    elif color_name in orange_colors:
        return 'ORANGE'
    elif color_name in multi_colors:
        return 'MULTI COLORS'
    else:
        return 'UNKNOWN' 


# In[18]:


df['Color Category'] = df['Primary Color'].apply(categorize_dog_color)


# In[19]:


# Filter the DataFrame for "DOG"
filtered_df = df[(df["Animal Type"] == "DOG") &(df['Color Category'] != "UNKNOWN")&
                (df["Time spent at Shelter"].dt.days <= 365) &
                (df["Outcome Type"].isin(["ADOPTION", "FOSTER TO ADOPT"]))]

# Define the desired order of categories
desired_order = ["WHITE", "BLUE", "YELLOW/GOLDEN", "RED", "BROWN/CHOCOLATE", "GRAY", "BLACK"]

# Define RGB colors for typical dog-related colors
custom_palette = [(255, 255, 255),   # White (common in many breeds)
                  (128, 144, 170),   # muted grayish-blue
                  (218, 165, 32),    # Golden Retriever-like (yellow/gold)
                  (139, 0, 0),       # Red (e.g., Irish Setter)
                  (139, 69, 19),     # Brown
                  (169, 169, 169),   # Gray 
                  (0, 0, 0)]         # Black (common in many breeds)

# Convert RGB tuples to hexadecimal strings manually
custom_palette = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in custom_palette]

# Create a violin plot
plt.figure(figsize=(20, 10))
sns.violinplot(x="Color Category", y=filtered_df["Time spent at Shelter"].dt.days,
               order=desired_order, data=filtered_df, split=False,
               palette=custom_palette, width=1)

# Add individual data points (dots) with a swarmplot
sns.stripplot(x="Color Category", y=filtered_df["Time spent at Shelter"].dt.days, 
              data=filtered_df, jitter=True, color="limegreen", alpha=0.5,
             edgecolor='black')

# Add labels and a title
plt.xlabel("Color", fontsize=20)
plt.ylabel("Duration in Shelter", fontsize=20)
plt.title("Shelter Stay Duration by Color for Dogs", fontsize=30)

plt.ylim(-40, 180)
plt.show()


# In[20]:


# Filter the DataFrame for "CAT"
filtered_df = df[(df["Animal Type"] == "CAT") &(df['Color Category'] != "UNKNOWN")&
                (df["Time spent at Shelter"].dt.days <= 365) &
                (df["Outcome Type"].isin(["ADOPTION", "FOSTER TO ADOPT",
                                         "COMUNITY CAT"]))]

# Define the desired order of categories
desired_order = ["WHITE", "BLUE", "YELLOW/GOLDEN", "ORANGE", "RED", "BROWN/CHOCOLATE", "GRAY", "BLACK"]

custom_palette = [(255, 255, 255),   # White (common in many breeds)
                  (112, 128, 144),   # Russian Blues
                  (255, 215, 0),    # Siamese cats
                  (255, 165, 0),   # orange
                  (255, 0, 0),       # Red Maine Coons
                  (139, 69, 19),     # Brown Burmese cats
                  (128, 128, 128),   # Gray ( British Shorthairs )
                  (0, 0, 0)]         # Black (common in many breeds)

# Convert RGB tuples to hexadecimal strings manually
custom_palette = ['#%02x%02x%02x' % (r, g, b) for (r, g, b) in custom_palette]

# Create a violin plot
plt.figure(figsize=(20, 10))
sns.violinplot(x="Color Category", y=filtered_df["Time spent at Shelter"].dt.days,
               data=filtered_df, split=False,
               order = desired_order,
               palette=custom_palette, width=1)

# Add individual data points (cats) with a swarmplot
sns.stripplot(x="Color Category", y=filtered_df["Time spent at Shelter"].dt.days, 
              data=filtered_df, jitter=True, color="limegreen", alpha=0.5,
             edgecolor='black')

# Add labels and a title
plt.xlabel("Color", fontsize=20)
plt.ylabel("Duration in Shelter", fontsize=20)
plt.title("Shelter Stay Duration by Color for Cats", fontsize=30)

plt.ylim(-40, 180)

plt.show()


# # Initial Condition and outcome

# In[21]:


normal = ["NORMAL"]
moderate = ["UNDER AGE/WEIGHT", "INJURED  MODERATE", "ILL MODERATETE", 
           "BEHAVIOR  MODERATE"]
mild = ["ILL MILD","INJURED  MILD","BEHAVIOR  MILD"]
severe = ["INJURED  SEVERE", "ILL SEVERE", "BEHAVIOR  SEVERE"]


# In[22]:


# Create a function to categorize outcome types
def categorize_intake(intake):
    if intake in normal:
        return "NORMAL"
    elif intake in moderate:
        return "MODERATE"
    elif intake in mild:
        return "MILD"
    elif intake in severe:
        return "SEVERE"
    else:
        return "OTHERS (aged,etc.)"

# Apply the categorization function to create a new column 'Intake Category'
df['Intake Category'] = df['Intake Condition'].apply(categorize_intake)


# In[23]:


from matplotlib.path import Path

# Define the custom dog paw marker
paw_marker = Path([
    (0.0, 0.5),  # Start point
    (0.1, 0.7),  # Toe 1
    (0.2, 0.6),  # Pad 1
    (0.4, 0.6),  # Pad 2
    (0.5, 0.7),  # Toe 3
    (0.6, 0.5),  # End point
])
df = df.copy()
df['Intake Date'] = pd.to_datetime(df['Intake Date'])

# Filter the DataFrame for "DOG"
filtered_df = df[(df["Animal Type"] == "DOG") &
                (df["Time spent at Shelter"].dt.days <= 365) &
                (df["Outcome Type"]=="ADOPTION") &
                (df['Intake Date'].dt.year >= 2020)]

desired_order = ["NORMAL", "MILD", "MODERATE", "SEVERE"]
custom_palette = ["skyblue", "green", "gold", "red"]

# Create a copy of the DataFrame to avoid the warning
filtered_df = filtered_df.copy()

# Sort the DataFrame based on the desired order using .loc
filtered_df['Intake Category'] = pd.Categorical(filtered_df['Intake Category'], categories=desired_order, ordered=True)
filtered_df.sort_values(by='Intake Category', inplace=True)

# Create a scatter plot
plt.figure(figsize=(16, 10))
sns.scatterplot(data=filtered_df, x = "Age", y=filtered_df["Time spent at Shelter"].dt.days, 
                hue='Intake Category', palette=custom_palette, marker=paw_marker, s=4000,
               edgecolor='black', linewidth=0.5, alpha=0.8)

# Set plot labels and title
plt.xlabel('Age', fontsize=20)
plt.ylabel('Time spent at Shelter', fontsize=20)
plt.title('Duration at Shelter until Adoption by Intake Category of Dogs',
         fontsize=30)

plt.xlim(-1, 20)
plt.ylim(0, 200)
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.legend(fontsize=20) 

plt.show()


# In[25]:


# Create a copy of the DataFrame to avoid the warning
filtered_df = filtered_df.copy()

# Sort the DataFrame based on the desired order using .loc
filtered_df['Intake Category'] = pd.Categorical(filtered_df['Intake Category'], categories=desired_order, ordered=True)
filtered_df.sort_values(by='Intake Category', inplace=True)

# Create a KDE plot
plt.figure(figsize=(10, 5))
sns.kdeplot(data=filtered_df, x="Age", y=filtered_df["Time spent at Shelter"].dt.days, hue='Intake Category', palette="deep")

# Set plot labels and title
plt.xlabel('Age', fontsize=15)
plt.ylabel('Time spent at Shelter', fontsize=15)
plt.title('Duration at Shelter until Adoption by Intake Condition and Age of Dogs', fontsize=20)

plt.xlim(0, 26)
plt.ylim(-10, 200)
plt.show()


# In[26]:


# Filter the DataFrame for "DOG" and intake year >= 2020
filtered_df = df[(df["Animal Type"] == "DOG") &
                 (df['Intake Date'].dt.year >= 2020) &
                 df["Outcome Type"].isin(bad_outcome + good_outcome)]

filtered_cat_df = df[(df["Animal Type"] == "CAT") &
                     (df['Intake Date'].dt.year >= 2020) &
                     df["Outcome Type"].isin(bad_outcome + good_outcome)]

desired_hue_order = ["RETURN TO OWNER", "ADOPTION", "RESCUE", "FOSTER TO ADOPT",
                     "HOMEFIRST", "EUTHANASIA", "DIED"]

# Create a count plot to visualize the relationship between intake category and outcome type
# Create two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
# Add a shared title across both subplots
plt.suptitle('Intake Condition and Outcome', fontsize=25)
plt.subplots_adjust(wspace=0.3)

sns.countplot(data=filtered_df, y="Intake Category", hue="Outcome Type",
              order=["NORMAL", "MILD", "MODERATE", "SEVERE"], palette="Set2",
              hue_order=desired_hue_order, ax=axes[0])

# Set plot labels and title for the first subplot
axes[0].set_xlabel('Outcome Numbers')
axes[0].set_ylabel('Intake Condition')
axes[0].set_title('Dogs', fontsize=20)
axes[0].legend(title='Outcome', loc='lower right')

sns.countplot(data=filtered_cat_df, y="Intake Category", hue="Outcome Type",
              order=["NORMAL", "MILD", "MODERATE", "SEVERE"], palette="Set2",
              hue_order=desired_hue_order, ax=axes[1])

# Set plot labels and title for the second subplot
axes[1].set_xlabel('Outcome Numbers')
axes[1].set_ylabel('')
axes[1].set_title('Cats', fontsize=20)
axes[1].get_legend().remove()

plt.show()


# In[27]:


filtered_df = df[(df["Animal Type"].isin(["DOG", "CAT"]))]

desired_order = ["NORMAL", "MILD", "MODERATE", "SEVERE"]
# Calculate the probability of euthanasia for each intake category
euthanasia_probabilities = (filtered_df[filtered_df['Outcome Type'].isin(bad_outcome)]
                            .groupby(['Intake Category', 'Animal Type'])
                            .size() / (filtered_df.groupby(['Intake Category', 'Animal Type']).size())*
                           100)

# Reset the index to make 'Intake Category' a column
euthanasia_probabilities = euthanasia_probabilities.reset_index(name='Euthanasia Probability')

# Sort the DataFrame based on the desired order using .loc
euthanasia_probabilities['Intake Category'] = pd.Categorical(euthanasia_probabilities['Intake Category'], categories=desired_order, ordered=True)
euthanasia_probabilities.sort_values(by='Intake Category', inplace=True)

# Round the euthanasia probability to two decimal places
euthanasia_probabilities['Euthanasia Probability'] = euthanasia_probabilities['Euthanasia Probability']

# Create a scatter plot
plt.figure(figsize=(8, 8))
sns.scatterplot(data=euthanasia_probabilities, y="Euthanasia Probability", 
                x="Intake Category", hue = "Animal Type", marker=paw_marker, s=10000,
                palette = "bone", edgecolor='black', linewidth=1)

# Add numbers (text labels) to the data points
for index, row in euthanasia_probabilities.iterrows():
    plt.annotate(f"{row['Euthanasia Probability']:.2f}",
                 (row['Intake Category'], row['Euthanasia Probability']),
                 textcoords="offset points",
                 xytext=(0,20),  # Adjust the offset here
                 ha='right', va='baseline', fontsize=13, color='black', alpha=1)
    
# Set plot labels and title
plt.xlabel('Intake Condition', fontsize=15)
plt.ylabel('Death Probability (%)', fontsize = 15)
plt.title("Probability of Euthanasia and Death", fontsize=25)

plt.xlim(-0.5, 3.5)
plt.ylim(0, 100)

plt.legend(loc="upper left")

plt.show()


# In[ ]:




