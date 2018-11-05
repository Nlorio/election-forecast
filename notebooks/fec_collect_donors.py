import json
import time
import datetime
import requests
import pandas as pd
import numpy as np
import yaml
from pathlib import Path
import pickle
import boto3
from io import BytesIO

CONFIG_FILE = Path('..')/Path('config.yaml')
with open(CONFIG_FILE, 'r') as f:
    config = yaml.load(f)
api_key = config['fec']['api_key']

df_candidate_id = pd.read_pickle('candidate_ids.pkl')
df_candidate_id.head()

df_committee_id = pd.read_pickle('committee_ids.pkl')
df_committee_id.head()

df_comm = pd.read_pickle('committee_id_formatted_v1.pkl')
df_comm.head()

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
    #print(donor_cand_size.status_code)
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
    donor_comm_state = donor_comm_state.json()['results']
    df_dcomm_state = pd.DataFrame(donor_comm_state)
    return df_dcomm_state

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


# Input: Candidate Name, Election Type, Date-time of election (Use Pandas Date time Format)
# 1. Will incorporate a funcation call to
# 2. to retrieve the fraction of committee donations for that candidate

# by_size/by_candidate
#  -0    $200 and under Level 1
#  -200  $200.01 - $499.99 Level 2
#  -500  $500 - $999.99 Level 3
#  -1000 $1000 - $1999.99 Level 4
#  -2000 $2000 + Level 5

a = cand_donor_state('P80001571', 2016)
states = a.state_full


# Returns rows, 1 row per cycle with all features for one candidate.
def candidate_donor_df(candidate_name, states, df_candidate_id):
    cand_row = df_candidate_id[df_candidate_id.name == candidate_name]
    cand_ids = cand_row.candidate_id.values

    j = 0

    #Initialize dataframe
    cand_info = ['name', 'cand_id', 'state', 'cycle', 'incumbent', 'office_full', 'party', 'committee_id']
    donation_levels = ['Donation Level 1',
               'Donation Level 2',
               'Donation Level 3',
               'Donation Level 4',
               'Donation Level 5']
    levels = [0, 200, 500, 1000, 2000]
    columns = np.append(cand_info, states)
    columns = np.append(columns, donation_levels)

    df = pd.DataFrame(columns=columns)

    for cand_id in cand_ids:
        #print(cand_id)

        cycles = cand_row.cycles.values[0]




        #Iterate through candidates cycles, add all cycles as new rows. Append to each column each

        #print(cycles)
        for cycle in cycles:
            df_size = cand_donor_size(cand_id, cycle)
            df_state = cand_donor_state(cand_id, cycle)
            if df_size.values.size == 0 or df_state.values.size == 0:
                continue

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
                              'cycle': cycle,
                              'incumbent': cand_row.incumbent_challenge_full.values[0],
                              'office_full': cand_row.office_full.values[0],
                              'party': cand_row.party_full.values[0],
                              'committee_id': 0}
            state_dict = merge_two_dicts(cand_info_dict, state_dict)
            state_dict = merge_two_dicts(state_dict, level_dict)
            #return state_dict


            #return state_dict.values()
            df.loc[j] = list(state_dict.values()) # An array of the row information
            j += 1
    return df


#Add df_candidate_id input to the previous function for candidate donor information collection function

def get_committee_candidates(candidate_name, states, df_candidate_id, df_comm):
    cand_row = df_candidate_id[df_candidate_id.name == candidate_name]
    cand_ids = cand_row.candidate_id.values
    j = 0

    #Initialize dataframe
    cand_info = ['name', 'cand_id', 'state', 'cycle', 'incumbent', 'office_full', 'party', 'committee_id']
    donation_levels = ['Donation Level 1',
               'Donation Level 2',
               'Donation Level 3',
               'Donation Level 4',
               'Donation Level 5']
    levels = [0, 200, 500, 1000, 2000]
    columns = np.append(cand_info, states)
    columns = np.append(columns, donation_levels)

    df = pd.DataFrame(columns=columns)
    #print(cand_ids)
    for cand_id in cand_ids:
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
            for cycle in cycles:
                df_size = comm_donor_size(comm_id)
                df_state = comm_donor_state(comm_id)
                if df_size.values.size == 0 or df_state.values.size == 0:
                    continue

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
                                  'committee_id': row.committee_id}
                state_dict = merge_two_dicts(cand_info_dict, state_dict)
                state_dict = merge_two_dicts(state_dict, level_dict)

                #return state_dict


                #return state_dict.values()
                df.loc[j] = list(state_dict.values()) # An array of the row information
                j += 1
    return df


cand_info = ['name', 'cand_id', 'state','cycle', 'incumbent', 'office_full', 'party', 'committee_id']
donation_levels = ['Donation Level 1',
       'Donation Level 2',
       'Donation Level 3',
       'Donation Level 4',
       'Donation Level 5']
columns = np.append(cand_info, states)
columns = np.append(columns, donation_levels)
df = pd.DataFrame(columns=columns)
i = 1
amount = len(df_candidate_id.name)
for name in df_candidate_id.name:
    df_name = candidate_donor_df(name, states, df_candidate_id)
    df = pd.concat([df, df_name], sort=False)

    df_name_comm = get_committee_candidates(name, states, df_candidate_id, df_comm)
    df = pd.concat([df, df_name_comm], sort=False)

    print('{}/{}'.format(i, amount))
    i+=1
    if i == 10:
        break

pickle_buffer = BytesIO()
s3_resource = boto3.resource('s3')

df.to_csv(pickle_buffer, index=False)
s3_resource.Object('tenguins_tmp', 'donor_df.pkl').put(Body=pickle_buffer.getvalue())
