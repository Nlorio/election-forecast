# tenguins
Project repository for Data-X, Fall 2018

## Virtual environment setup

We have included a [requirements.txt](./requirements.txt), which can be used to create a Python3 virtual environment using the following commands executed in the root directory of the repository:

```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

## API Keys

API keys are stored in `config.yaml`, which is withheld from the git repository via [.gitignore](./.gitignore). To reproduce notebooks, create a `config.yaml` in the root project directory and store API keys as the notebook structure suggests. A guide to using `pyyaml` with API keys can be found  [here](notebooks/0-setup).


## Notebooks

- RCP_Scraping.ipynb :
	- Scrapes real clear politics and internet archives to create a comprehensive .csv of every poll on that site from mid year 2010 to just before the 2018 midterm elections

- Practice_with_Polls.ipynb :
	- Separates scraped polls into sections based on type of the poll e.g. race poll, presidential approval, congressional approval, etc.

- Race_Winner_Matcher.ipynb :
	- takes polls edited by Junseo and adds winners for each race. Also adds district 0 for governor and senator

- PredictIt Analysis.ipynb :
	- (Jerry's) failed attempt at working with data from PredictIt

- PollOnlyModel.ipynb :
	- ignore this

- 538_grade_to_score.ipynb:
    	- To run this code, you should have two supplemental file, 'pollster.csv' and 'gradetoscore.csv', and all 'RCP_XXX_final.csv' files.
    	- This code would first transform the of 'Spread' into a usable form (if binary, might be negative.
    	- Secondly, this code would assign the grade (score) to each of the polling data according to 538 website (from 0 to 13, 1 is equivalent to F and 13 is equivalent to A+, score of 0 means unknown)

- agg_poll_market.R:
	- Ignore this
	- Attempt to aggregate poll data and market data but failed

- poll_grade.R:
	- Ignore this. Same as second part of '538_grade_to_score.ipynb'. Can be used to verify the correctness of it.

- result_transformation.R:
	- Ignore this. Same as first part of '538_grade_to_score.ipynb'. Can be used to verify the correctness of it.

- DemocratRepublican_Classification.ipynb
	- Assigns party affiliation to the current leader of a race (formatted as a time series)G
	- For Gubernatorial, Senatorial, and House races

- Polls_Agg.ipynb
	- Attempt to aggregate polls data with PredictIt markets
	- Failed -- finding common grounds between the datasets is very difficult without an enormous amount of repetitiveness

- data_visualization.ipynb
	- Data visualization for predictit data and RCP data
	- this notebook requires the .csv with nfile name 'xxx_538.csv'

- notebooks/0-setup
	- [reading-api-keys.ipynb](notebooks/0-setup/reading-api-keys.ipynb)
		- Information on how to hide an API key in a git repository

- notebooks/1-preprocessing
	- [old_finding_winners_house_senate.ipynb](notebooks/1-preprocessing/old_finding_winners_house_senate.ipynb)
		- Old scraper that scrapes Wikipedia and internet archives to create comprehensive house and senate winners .csv from 2010 to just before the 2018 midterm elections
	- [old_finding_winners_governor.ipynb](notebooks/1-preprocessing/old_finding_winners_governor.ipynb)
		- Old scraper that scrapes Wikipedia and internet archives to create comprehensive governor winners .csv from 2010 to just before the 2018 midterm elections
	- [new_scrape_house.ipynb](notebooks/1-preprocessing/new_scrape_house.ipynb)
		- New Wikipedia scraper for House races
	- [new_scrape_governor.ipynb](notebooks/1-preprocessing/new_scrape_governor.ipynb)
		- New Wikipedia scraper for gubernatorial races
	- [new_scrape_senate.ipynb](notebooks/1-preprocessing/new_scrape_senate.ipynb)
		- New Wikipedia scraper for Senate races



## Cleaned Data

- candidate_parties_house.csv :
	- Names + parties of all House candidates. Output of new_scrape_house.ipynb.
- candidate_parties_senate.csv :
	- Names + parties of all Senate candidates. Output of new_scrape_senate.ipynb.
- candidate_parties_governor.csv :
	- Names + parties of all gubernatorial candidates. Output of new_scrape_governor.ipynb.


- Clean_Governor_Winners.csv :
	- output of finding_winners_governor.ipynb

- Clean_House_Winners.csv :
	- one of the outputs of finding_winners_house_senate.ipynb

- Clean_Senate_Winners.csv :
	- one of the outputs of finding_winners_house_senate.ipynb

- Final_Polls_Nov_5.csv :
	- output of RCP_Scraping.ipynb

- RCP_p_approval_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb
- RCP_p_approval_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- RCP_c_approval_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_c_approval_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- RCP_Direction_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_Direction_Final_538.csv :
	- one of the outputs of '538_grade_to_score.ipynb'

- RCP_Generic_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_Generic_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- RCP_house_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_house_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- RCP_governor_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_governor_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- RCP_senate_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_senate_Final_538.csv :
	- one of the putpus of '538_grade_to_score.ipynb'

- DailyMarketData_Fixed.csv :
	- data from PredictIt. It doesn't seem too helpful considering the small number of markets, but it might be worth keeping just in case.

- gov_races_classified.pkl :
	- Gubernatorial races classified by party affiliation (output of DemocratRepublican_Classification.ipynb)

- sen_races_classified.pkl :
	- Senatorial races classified by party affiliation (output of DemocratRepublican_Classification.ipynb)

- house_races_classified.pkl :
	- House races classified by party affiliation (output of DemocratRepublican_Classification.ipynb)
