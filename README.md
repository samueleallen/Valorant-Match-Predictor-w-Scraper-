# Project Overview
## **Project Steps**
- Scrape match data using requests, Beautiful Soup, and Pandas.
- Clean the data and get it ready for machine learning using pandas
- Make predictions about who will win/lose a match using scikit-learn
- Measure error and improve our predictions

## **Setup**

To follow this project, please install the following locally:
- Jupyter lab
- Latest Python version
- Python Packages
  - pandas
  - requests
  - BeautifulSoup
  - sckikit-learn

## **Data**

We'll be scraping [vlr](https://www.vlr.gg/) as they allow web scraping.

## **Tournament Predictions**  

There are three main tournaments to consider predicting results of:
- First Valorant Masters Tournament of the season
- Second Masters Tournament of the season
- Valorant Champions

Variables to consider:
- Throughout each year, the Masters Tournaments change locations and starting date.
- Valorant esports is not static, many changes are made from year-to-year in the standings system
- Qualifications for these tournaments have been convoluted and dynamic over the last couple of years.

Potential Solutions:
1. Create three different machine learning models each with their own unique training/test set.
2. Only aim for the results of the biggest tournament (Champions Tournament)

## **Feature Engineering**
A couple of ways to go about this:
- Intuition:
- - Intuitively estimate what features have the most impact on the results of a game using your expertise level
- [Scikit](https://scikit-learn.org/stable/modules/feature_selection.html)
  - Use the sk.learn_feature_selection module to improve estimators' accuracy scores

Features to consider:
- Jet lag
   - Does the team perform worse when they have to travel to a far place for the tournament?
   - Do they perform better on home turf?
- Weekday Performance
   - Does a team do better on one weekday compared to another?
- Team rivalries
  - Does team A have a history of doing better against Team B?
  - Note: Implementation of Team and vsTeam as features seemed to lower accuracy score of the model...
  - Something to consider is why this might have happened and if the implementation could be better.
- Team Elos:
  - Create our own elo ranking system.

## **Future Considerations**
In the future, we should consider testing different machine learning algorithims and the implementation of different statistical techniques
to optimize the model futher.

### **Random Forest vs XGBoost:**
Currently we use RandomForest but I have heard XGBoost may produce a better model.
Notable Differences:
- RandomForest trains trees in parallel and combines the trees to make a prediction.
  - Uses bootstrap sampling to improve accuracy
- XGBoost trains trees sequentially and improves upon previous trees.
  - Uses gradient descent to minimize errors.

Ultimately, there are many ways for potential improvements of the model and the answer to finding the next potential improvement is through experimentation.

Future Update: XGBoost performed worse by a margin of roughly 2-3%. 
