import pandas as pd

def explore_data():
    """ Getting to know the dataset (to cleanup and set up models). """
    
    df = pd.read_csv('DisasterDeclarationsSummaries.csv')

    print "-----------------------------------------"
    print "-----------------------------------------"
    print "TOTAL # OBSERVATIONS:", len(df.index) # 48054
    print "\nCOLUMNS NAMES:\n", list(df) 
    # ['disasterNumber', 'ihProgramDeclared', 'iaProgramDeclared', 'paProgramDeclared', 'hmProgramDeclared', 'state', 'declarationDate', 'fyDeclared', 'disasterType', 'incidentType', 'title', 'incidentBeginDate', 'incidentEndDate', 'disasterCloseOutDate', 'declaredCountyArea', 'placeCode', 'hash', 'lastRefresh']
    print "-----------------------------------------"
    print "-----------------------------------------"

    for i, column in enumerate(list(df)):
        
        values = list(df[column].unique())
        data_type = type(values[0])

        print "COLUMN # {} / {}".format(i+1, len(list(df))+1)
        print "COLUMN NAME:", column, data_type
        if len(values)>20:
            print "\nVALUES: (10 of out {}): \n".format(len(values)), values[:20]
        else:
            print "\nVALUES (all {}): \n".format(len(values)), values
        print "MIN and MAX VALUES :", (min(values), max(values))
        print "-----------------------------------------"


def explore_dropped():
    """ Drop duplicates/missingness and explore data. """

    df = pd.read_csv('DisasterDeclarationsSummaries.csv')

    print "-----------------------------------------"
    print "-----------------------------------------"
    # Remove nan / missingness
    df = df.drop_duplicates()
    df = df.dropna(axis=0, how='all')
    df = df.dropna()
    df = df[~df.astype(str).eq('None').any(1)]
    df = df[df.astype(str).ne('None').all(1)]

    print "STATES: {}".format(len(list(df['state'].unique())))
    print list(df['state'].unique())


    # see how it affects sample size
    print "DROPPING DUPLICATES, MISSINGNESS, NaNs"
    print "TOTAL # OBSERVATIONS:", len(df.index) # 2628
    print "-----------------------------------------"
    print "-----------------------------------------"

    for i, column in enumerate(list(df)):
        
        values = list(df[column].unique())
        data_type = type(values[0])

        print "COLUMN # {} / {}".format(i+1, len(list(df))+1)
        print "COLUMN NAME:", column, data_type
        if len(values)>20:
            print "\nVALUES: (10 of out {}): \n".format(len(values)), values[:20]
        else:
            print "\nVALUES (all {}): \n".format(len(values)), values
        print "MIN and MAX VALUES :", (min(values), max(values))
        print "-----------------------------------------"

# explore_data()
explore_dropped()