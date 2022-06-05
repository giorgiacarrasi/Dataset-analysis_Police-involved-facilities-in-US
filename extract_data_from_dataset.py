import pandas as pd 
from pandas import DataFrame

class ExtractData: 
    df: DataFrame

    def __init__(self, df): 
        self.df = df 

    def groupByArmedAndRaceDF(self): 
        dfByArmedAndRace = self.df.groupby(['Armed', 'Race'], dropna=True)\
                    .size()\
                    .sort_values(ascending=True)\
                    .reset_index(name='size')

        dfByArmedAndRace = dfByArmedAndRace[dfByArmedAndRace['size'] > 70]

        dfByArmedAndRace = self.df.groupby(['Race', 'Armed'], dropna=True,  observed=True) \
                            .filter(lambda g: len(g) > 10)
        dfByArmedAndRace.Armed = dfByArmedAndRace.Armed.cat.remove_unused_categories()
        dfByArmedAndRace = dfByArmedAndRace.groupby(['Race', 'Armed'], dropna=True) \
                                            .size() \
                                    .unstack('Race')

        return dfByArmedAndRace

    def groupByMannerOfDeathAndRaceDF(self):
        dfByMannerOfDeathAndRace = self.df.groupby(['Race', 'Manner_of_death'], dropna=True) \
                                .size() \
                                .unstack('Race')
        return dfByMannerOfDeathAndRace
    
    def groupByVictimsByStateAndRaceDF(self):
        firstTenState = self.df.groupby(['State', 'Race'], dropna=True) \
                        .size() \
                        .sort_values(ascending=False) \
                        .reset_index(name='size')['State'] \
                        .unique()[:10]

        dfByStateAndRace = self.df[self.df['State'].isin(firstTenState)]
        dfByStateAndRace = dfByStateAndRace.assign(State=dfByStateAndRace.State.cat.remove_unused_categories()) \
                    .groupby(['State', 'Race'], dropna=True) \
                    .size() \
                    .unstack('Race')
        return dfByStateAndRace

    def groupByVictimsByCityAndRaceDF(self):
        firstTenCity = self.df.groupby(['City', 'Race'], dropna=True) \
                        .size() \
                        .sort_values(ascending=False) \
                        .reset_index(name='size')['City'] \
                        .unique()[:10]

        dfByCityAndRace = self.df[self.df['City'].isin(firstTenCity)] \
                        .groupby(['City', 'Race'], dropna=True) \
                        .size() \
                        .unstack('Race')
        return dfByCityAndRace
    
    def victimsByYearAndRaceDF(self): 
        dfByRaceAndDate = self.df[['Race', 'Date']].copy()
        dfByRaceAndDate['date_year'] = dfByRaceAndDate['Date'].dt.year

        dfByRaceAndDate = dfByRaceAndDate.groupby(['Race', 'date_year'], dropna=True) \
                        .size() \
                        .reset_index(name='count') 
        dfByRaceAndDate.set_index('date_year', inplace=True)

        return dfByRaceAndDate

    def onlyFemaleVictimsByRaceDF(self):
        dfOnlyFemaleByRace = self.df.copy()

        dfOnlyFemaleByRace = dfOnlyFemaleByRace[dfOnlyFemaleByRace['Gender']== 'Female'] 
        dfOnlyFemaleByRace = dfOnlyFemaleByRace.groupby(['Race'], dropna=True) \
                        .size() \
                        .sort_values(ascending=False) 
        return dfOnlyFemaleByRace

    def mentalIllnessPresenceByRaceDF(self):
        dfMentalIllnessByRace = self.df.copy()

        dfMentalIllnessByRace = dfMentalIllnessByRace.groupby(['Race', 'Mental_illness'], dropna=True) \
                        .size() \
                        .unstack(1) \
                        .sort_values( by=0, ascending=True) 
        return dfMentalIllnessByRace

