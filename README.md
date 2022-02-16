# Predictions
As a passionate of football, statistics and programing I created this console application, that based on the games that took place in this season can predict the outcome of any match.
Program calculates strengths of teams in defence, attack, at home and in away matches, based on them calculates the expected goals for each team.
Probabilities are values of Poissant distribution density function, where EX = exppected goals of the team.
User can also see the chances and computed expected odds for popular events offered by every bookmaker:
- both teams to score
- 1X2
- double chance
- over 2.5 goals and under 2.5 goals
- correct score

## Scraping data
Web scraping is the significant part of this project. All necessary tasks are automatized. Data is upadated from Flashscore, SkySport and TheGuardian.
Real odds are scraped from well-known bookmaker Betclic, the user can easily compare expected odds with these offered by the market and find opportunities 
or check the suggested bets.

## GUI
The output is written to console, but GUI build in tkinter helps user navigate through the application and get the desired data
 
## Data
Data used to calculations is stored in csv files, but you can check excel files if you want a clearer visualisation

## Analysis
While updating data, program saves the prediction and real result to further analysis. 

## Check for yourself!
