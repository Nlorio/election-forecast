import json
import time
from datetime import datetime
import requests 
import pandas as pd
import numpy as np
import yaml
from pathlib import Path
import pickle 
import os
import re
from nltk import metrics, stem, tokenize
import math
import boto3
from io import BytesIO


api_key = 'IlbRy4iSNXBdEQhTyhQLXl68EVS3U2XttiNvLtpW'

df_candidate_id = pd.read_pickle('candidate_ids.pkl')
df_candidate_id.head()
df_candidate_id.name = np.array([x.lower().replace(",", "") if isinstance(x, str) else x for x in df_candidate_id.name.values])
df_candidate_id.head()

#Reformat df_candidate_id based on cycles
len_reform_df = sum(df_candidate_id['cycles'].apply(lambda row: len(row)))
print('Length of new datframe {}:'.format(len_reform_df))



# def reformat_by_cycle(df):
#     df_temp = df.copy()
    
#     # Create the DataFrame with 54446 rows and columns -- all NaNs
#     cols = df_temp.columns
#     df_cand = pd.DataFrame(np.full((len_reform_df, len(cols)), np.nan), columns=cols)
#     df_cand['cycles'] = df_cand['cycles'].astype(list)
#     df_cand['election_years'] = df_cand['election_years'].astype(list)
    
#     i = 0
#     j= 0
#     for list_cycles in df_temp.cycles:
#         for cycle in list_cycles:
#             df_cand.iloc[j,:] = df_temp.iloc[i,:] 
#             df_cand.iloc[j, 6] = cycle
#             j+=1
    
#         i+=1
#     return df_cand

df_cand = pd.read_pickle('df_cand.pkl')

house_winners = pd.read_pickle(Path('.')/'..'/'data'/'cleaned'/'HousePollwithWinner_Final.pkl')
senate_winners = pd.read_pickle(Path('.')/'..'/'data'/'cleaned'/'SenatePollwithWinner_Final.pkl')
gov_winners = pd.read_pickle(Path('.')/'..'/'data'/'cleaned'/'GovernorPollwithWinner_Final.pkl')


house_winners.head()
senate_winners.head()
gov_winners.head()

df_races = house_winners.append(senate_winners)
df_races = df_races.append(gov_winners)
print(len(df_races.race_name))
df_races.head()

df_race_candidates = df_races[df_races.winner != '<BLANK>']

# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process

# cols = np.append(df_cand.columns.values, np.array(['race_candidates', 'date_of_poll', 'election_result']))
# dimension_length = 2*len(df_race_candidates.race_type) + 20 # To account for potential extra rows 
# df_selected_candidates = pd.DataFrame(np.full((dimension_length, len(cols)), np.nan), columns=cols)
# df_selected_candidates['election_years'] = df_selected_candidates['election_years'].astype(list)

# j = 0
# for index, race_row in df_race_candidates.iterrows():
    
#     race_type = race_row.race_type
#     race_date = race_row.date
#     race_candidates = race_row.top_candidates
#     race_state = race_row.state
    
#     for index, row in df_cand.iterrows():
        
#         last_name = row[0].split()[0]
#         year = row.cycles
#         race = row.office_full.lower()
#         state = row.state

#         for race_candidate in race_candidates:
#             score = fuzz.token_sort_ratio(last_name, race_candidate)
#             if (score >= 100) & (race == race_type) & (year == race_date.year) & (state == race_state):
#                 temp_row = df_cand.iloc[index, :]
#                 temp_row['race_candidates'] = race_candidates
#                 temp_row['date_of_poll'] = race_row.date
#                 temp_row['election_result'] = race_row.winner
#                 df_selected_candidates.iloc[j,:] = temp_row
#                 print(j)
#                 j += 1
            
# df_selected_candidates 
        
            
# df_selected_candidates = df_selected_candidates.dropna()

# df_selected_candidates.to_pickle('df_selected_cand.pkl')

df_selected_candidates = pd.read_pickle('df_selected_cand.pkl')
        
df_committee_id = pd.read_pickle('committee_ids.pkl')

df_comm = pd.read_pickle('committee_id_formatted_v1.pkl')

# Use by_state/by_candidate, by_size/by_candidate
# QUESTION, Does this by_candidate search include donations made to committee's? 

# Use /schedules/schedule_a/by_size/by_candidate/
# Use /schedules/schedule_a/by_state/by_candidate/


# by_size/by_candidate
#  -0    $200 and under
#  -200  $200.01 - $499.99
#  -500  $500 - $999.99
#  -1000 $1000 - $1999.99
#  -2000 $2000 +

def cand_donor_size(candidate_id, cycle): 
    # Returns aggregated totals of contribution amounts that fit within defined groupings

    url_size = 'https://api.open.fec.gov/v1/schedules/schedule_a/\
by_size/by_candidate/\
?per_page=100\
&page=1\
&sort_null_only=false\
&election_full=false\
&cycle={}\
&sort_hide_null=false\
&api_key={}\
&candidate_id={}'.format(cycle, api_key, candidate_id)

    donor_cand_size = requests.get(url_size)
#     print(donor_cand_size.status_code)
    if donor_cand_size.status_code != 200:
        return pd.DataFrame(['time_out'])
    donor_size_result = donor_cand_size.json()['results']
    df_dcand_size = pd.DataFrame(donor_size_result)
    return df_dcand_size

    
    
# Schedule A individual receipts aggregated by contributor state.
# This is an aggregate of only individual contributions. 
def cand_donor_state(candidate_id, cycle): 
    # Returns aggregated totals of contribution amounts that fit within defined groupings
    url_state = 'https://api.open.fec.gov/v1/schedules/schedule_a/\
by_state/by_candidate/\
?per_page=100\
&page=1\
&sort_null_only=false\
&election_full=false\
&cycle={}\
&sort_hide_null=false\
&api_key={}\
&candidate_id={}'.format(cycle, api_key, candidate_id)
    
    donor_cand_state = requests.get(url_state)
    #print(donor_cand_state.status_code)
    if donor_cand_state.status_code != 200:
        return pd.DataFrame(['time_out'])
    donor_state_result = donor_cand_state.json()['results']
    df_dcand_state = pd.DataFrame(donor_state_result)
    return df_dcand_state


# Use /committee/{committee_id}/schedules/schedule_a/by_size/
# Use /committee/{committee_id}/schedules/schedule_a/by_state/
# Extract candidate_ids supported by each committee, use DataFrame B

def comm_donor_size(committee_id):
    url = 'https://api.open.fec.gov/v1/committee/\
{}/schedules/schedule_a/\
by_size/?sort_hide_null=false\
&per_page=100\
&page=1\
&api_key={}\
&sort_null_only=false'.format(committee_id, api_key)
    
    donor_comm_size = requests.get(url)
    #print(donor_comm_size.status_code)
    if donor_comm_size.status_code != 200:
        return pd.DataFrame(['time_out'])
    donor_comm_size = donor_comm_size.json()['results']
    df_dcomm_size = pd.DataFrame(donor_comm_size)
    return df_dcomm_size

def comm_donor_state(committee_id):
    url = 'https://api.open.fec.gov/v1/committee/\
{}/schedules/schedule_a/\
by_state/?sort_hide_null=false\
&per_page=100\
&page=1\
&api_key={}\
&sort_null_only=false'.format(committee_id, api_key)
    
    donor_comm_state = requests.get(url)
    #print(donor_comm_state.status_code)
    if donor_comm_state.status_code != 200:
        return pd.DataFrame(['time_out'])
    donor_comm_state = donor_comm_state.json()['results']
    df_dcomm_state = pd.DataFrame(donor_comm_state)
    return df_dcomm_state


def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

a = cand_donor_state('P80001571', 2016)
states = a.state_full

import time
# Input: Candidate Name, Election Type, Date-time of election (Use Pandas Date time Format)
# 1. Will incorporate a funcation call to 
# 2. to retrieve the fraction of committee donations for that candidate

# by_size/by_candidate
#  -0    $200 and under Level 1 
#  -200  $200.01 - $499.99 Level 2 
#  -500  $500 - $999.99 Level 3 
#  -1000 $1000 - $1999.99 Level 4
#  -2000 $2000 + Level 5

# Election Result: 
#     0 Lose
#     1 Win
#     3 No Data




# Returns rows, 1 row per cycle with all features for one candidate. 
def candidate_donor_df(candidate_name, states, df_candidate_id):
    cand_row = df_candidate_id[df_candidate_id.name == candidate_name]
    cand_ids = cand_row.candidate_id.values
    
    j = 0
    
    #Initialize dataframe
    cand_info = ['name', 'cand_id', 'state', 'cycle', 'incumbent', 'office_full',
                 'party', 'committee_id', 'committee_name','race_candidates', 'election_result']
    donation_levels = ['Donation Level 1',
               'Donation Level 2', 
               'Donation Level 3',
               'Donation Level 4',
               'Donation Level 5']
    levels = [0, 200, 500, 1000, 2000]
    cols = np.append(cand_info, states)
    cols = np.append(cols, donation_levels)

    df = pd.DataFrame(np.full((1000, len(cols)), np.nan), columns=cols)
    cand_id = cand_ids[0]
#     for cand_id in cand_ids:
    #print(cand_id)

    cycles = int(cand_row.cycles.values[0])




    #Iterate through candidates cycles, add all cycles as new rows. Append to each column each

    #print(cycles)
#         for cycle in cycles:
    df_size = cand_donor_size(cand_id, cycles)
    df_state = cand_donor_state(cand_id, cycles)

    if len(df_size) > 0 or len(df_state) > 0:
        
        if df_size.values.size == 0 or df_state.values.size == 0:
                return df.dropna()
                
        if df_size.iloc[0,0] == 'time_out' or df_state.iloc[0,0] == 'time_out':
            print('API Time Out, Sleep for 1 hour')
            time.sleep(3610)
            df_size = cand_donor_size(cand_id, cycles)
            df_state = cand_donor_state(cand_id, cycles)

    if df_size.values.size == 0 or df_state.values.size == 0:
        return df.dropna()
    donor_states = df_state.state_full

    #Build row of information (donor_states)

    # Idea
    # Create dictionary with states as keys and initialized with 0s as values. 
    initialize_array = np.zeros(len(states))
    state_dict = dict(zip(states, initialize_array))

    for ds in donor_states:            
        # Overwrite select values with information from df_state
        state_dict[ds] = df_state[df_state.state_full == ds].total.values[0]


    # Add size features to state_dict 


    level_array = np.zeros(5)
    level_dict = dict(zip(donation_levels, level_array))

    for level in df_size['size']:
        if level == 0:
            donation_level = 'Donation Level 1'
        if level == 200:
            donation_level = 'Donation Level 2'
        if level == 500:
            donation_level = 'Donation Level 3'
        if level == 1000:
            donation_level = 'Donation Level 4'
        if level == 2000:
            donation_level = 'Donation Level 5'
        level_dict[donation_level] = df_size[df_size['size'] == level].total.values[0]


    cand_info_dict = {'name': candidate_name, 
                      'cand_id': cand_id, 
                      'state': cand_row.state.values[0],
                      'cycle': cycles,
                      'incumbent': cand_row.incumbent_challenge_full.values[0],
                      'office_full': cand_row.office_full.values[0],
                      'party': cand_row.party_full.values[0],
                      'committee_id': 0, 
                      'committee_name': 0,
                      'race_candidates': cand_row.race_candidates.values[0],
                      'election_result': cand_row.election_result.values[0]}
    state_dict = merge_two_dicts(cand_info_dict, state_dict)
    state_dict = merge_two_dicts(state_dict, level_dict)
    #return state_dict
    #df.iloc[j]
    #print(np.array(list(state_dict.values())))
    temp = list(state_dict.values())
    df.iloc[j] = np.array(temp, dtype=object) # An array of the row information
    j += 1
    return df.dropna()

                         
import time
#Add df_candidate_id input to the previous function for candidate donor information collection function 

def get_committee_candidates(candidate_name, states, df_candidate_id, df_comm):
    cand_row = df_candidate_id[df_candidate_id.name == candidate_name]
    cand_ids = cand_row.candidate_id.values
    j = 0
    
    #Initialize dataframe
    cand_info = ['name', 'cand_id', 'state', 'cycle', 'incumbent', 'office_full', 'party', 
                 'committee_id', 'committee_name', 'race_candidates', 'election_result']
    donation_levels = ['Donation Level 1',
               'Donation Level 2', 
               'Donation Level 3',
               'Donation Level 4',
               'Donation Level 5']
    levels = [0, 200, 500, 1000, 2000]
    cols = np.append(cand_info, states)
    cols = np.append(cols, donation_levels)

    df = pd.DataFrame(np.full((1000, len(cols)), np.nan), columns=cols)
    cand_id = cand_ids[0]
#     for cand_id in cand_ids:
    comm_rows = df_comm[df_comm.candidate_ids == cand_id]
    #return comm_rows

    #for row in comm_rows: 
    for index, row in comm_rows.iterrows(): #Iterate through each row of the dataframe comm_row
        #print('iter')
        candidate_donor_weight = row.candidate_donor_weight
        cycles = row.cycles
        comm_id = row.committee_id
        #Iterate through candidates cycles, add all cycles as new rows. Append to each column each
        #print(cycles)
#         cycle = cycles[0]
        for cycle in cycles:
            df_size = comm_donor_size(comm_id)
            df_state = comm_donor_state(comm_id)

            
            if len(df_size) > 0 or len(df_state) > 0:
                
                if df_size.values.size == 0 or df_state.values.size == 0:
                    break
                
                if df_size.iloc[0,0] == 'time_out' or df_state.iloc[0,0] == 'time_out':
                    print('API Time Out, Sleep for 1 hour')
                    time.sleep(3610)
                    df_size = comm_donor_size(comm_id)
                    df_state = comm_donor_state(comm_id)

            if df_size.values.size == 0 or df_state.values.size == 0:
                break
            donor_states = df_state.state_full

            #Build row of information (donor_states)

            # Idea
            # Create dictionary with states as keys and initialized with 0s as values. 
            initialize_array = np.zeros(len(states))
            state_dict = dict(zip(states, initialize_array))

            for ds in donor_states:            
                # Overwrite select values with information from df_state
                state_row = df_state[df_state.state_full == ds]
                state_dict[ds] = state_row.total.values[0] * candidate_donor_weight


            # Add size features to state_dict 


            level_array = np.zeros(5)
            level_dict = dict(zip(donation_levels, level_array))

            for level in df_size['size']:
                if level == 0:
                    donation_level = 'Donation Level 1'
                if level == 200:
                    donation_level = 'Donation Level 2'
                if level == 500:
                    donation_level = 'Donation Level 3'
                if level == 1000:
                    donation_level = 'Donation Level 4'
                if level == 2000:
                    donation_level = 'Donation Level 5'
                size_row = df_size[df_size['size'] == level]
                level_dict[donation_level] = size_row.total.values[0] * candidate_donor_weight


            cand_info_dict = {'name': candidate_name, 
                              'cand_id': cand_id, 
                              'state': row.state,
                              'cycle': cycle,
                              'incumbent': 0,
                              'office_full': 0,
                              'party': 0,
                              'committee_id': row.committee_id,
                              'committee_name': row[11],
                              'race_candidates': 0,
                              'election_result': 0}
            state_dict = merge_two_dicts(cand_info_dict, state_dict)
            state_dict = merge_two_dicts(state_dict, level_dict)

            #return state_dict


            #return state_dict.values()
            df.iloc[j] = np.array(list(state_dict.values()), dtype = object) # An array of the row information
            j += 1
            break
    return df.dropna()
    
 #Time to Run 
time = (len(df_selected_candidates.name) / 10 ) * 22 / 60 /60
print('Hours to run, not counting sleep time: {}'.format(time))                    
        
# 120 calls per minute allowed through API 
# 4 calls made per candidate

import time
cand_info = ['name', 'cand_id', 'state','cycle', 'incumbent', 'office_full', 
             'party', 'committee_id', 'committee_name', 'race_candidates', 'election_result']
donation_levels = ['Donation Level 1',
       'Donation Level 2', 
       'Donation Level 3',
       'Donation Level 4',
       'Donation Level 5']
columns = np.append(cand_info, states)
columns = np.append(columns, donation_levels)
df = pd.DataFrame(np.full((100000, len(columns)), np.nan), columns=columns)

i = 1
j = 0 
amount = len(df_selected_candidates.name) 
print(datetime.now())

for name in df_selected_candidates.name:
    df_name = candidate_donor_df(name, states, df_selected_candidates)
    for index, row in df_name.iterrows():
        df.iloc[j] = row 
        j += 1
#     df = pd.concat([df, df_name], sort=False)
    
    df_name_comm = get_committee_candidates(name, states, df_selected_candidates, df_comm)
    if len(df_name_comm.name) != 0:
        for index, row in df_name_comm.iterrows():
            df.iloc[j] = row
            j+= 1
        
   
    #df = pd.concat([df, df_name_comm], sort=False)
    print('{}/{}'.format(i, amount))
    i+=1
    if i == 10:
        print('API Calls per Minute Time Out, Sleep for 60 seconds')
        time.sleep(60)
print(datetime.now())
df


df = df.dropna()

df.to_pickle('donor_df.pkl')

s3 = boto3.resource('s3')
s3.Object('tenguins-tmp', 'donor_df.pkl').put(Body=pickle.dump(df))
