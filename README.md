# tenguins
Project repository for Data-X, Fall 2018

API keys are stored in `config.yaml`, which is withheld from the git repository via [.gitignore](./.gitignore). To reproduce notebooks, create a `config.yaml` in the root project directory and store API keys as the notebook structure suggests. A guide to using `pyyaml` with API keys can be found  [here](notebooks/0-setup).


## Notebooks


- RCP_Scraping.ipynb :
	- Scrapes real clear politics and internet archives to create a comprehensive .csv of every poll on that site from mid year 2010 to just before the 2018 midterm elections

- Practice_with_Polls.ipynb :
	- Separates scraped polls into sections based on type of the poll e.g. race poll, presidential approval, congressional approval, etc.

- finding_winners_governor.ipynb :
	- scrapes wikipedia and internet archives to create comprehensive governor winners .csv from 2010 to just before the 2018 midterm elections

- finding_winners_house_senate.ipynb :
	- scrapes wikipedia and internet archives to create comprehensive house and senate winners .csv from 2010 to just before the 2018 midterm elections

- PredictIt Analysis.ipynb :
	- (Jerry's) failed attempt at working with data from PredictIt

- PollOnlyModel.ipynb :
	- ignore this

- 538_grade_to_score.ipynb:
    	- To run this code, you should have two supplemental file, 'pollster.csv' and 'gradetoscore.csv', and all 'RCP_XXX_final.csv' files (they are in /data/cleaned). 
    	- This code would first transform the of 'Spread' into a usable form (notice, if the result is binary, ie. 'Democrats and Repblicans', 'Approval and Disapproval', the 'Spread' might be negative, which means, Rep > Dem or Disapp > App). 
    	- Secondly, this code would assign the grade (score) to each of the polling data according to the information given by 538 website (from 0 to 13, 1 is equivalent to F and 13 is equivalent to A+, notice, score of 0 means unknown)

- agg_poll_market.R:
	- Ignore this
	- Attempt to aggregate poll data and market data but failed

- poll_grade.R:
	- Ignore this. Same as second part of '538_grade_to_score.ipynb'. Can be used to verify the correctness of it.
	
- result_transformation.R:
	- Ignore this. Same as first part of '538_grade_to_score.ipynb'. Can be used to verify the correctness of it.
#Data

## Cleaned Data


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

- RCP_c_approval_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_Direction_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_Generic_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_house_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_governor_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- RCP_senate_Final.csv :
	- one of the outputs of Practice_with_Polls.ipynb

- DailyMarketData_Fixed.csv :
	- data from PredictIt. It doesn't seem too helpful considering the small number of markets, but it might be worth keeping just in case.
