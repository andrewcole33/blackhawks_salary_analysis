import pandas as pd

def clean_team_salary_df(df):
    
    
    # Rename the column titles to all lowercase for ease of work in future
    col_titles = ['no.', 'name', 'nationality', 'pos', 'age', 'ht', 'wt', 'hand', 'exp', 'birth_date', 'summary', 'salary', 'draft']
    df.columns = col_titles
    
    # Clean names column to strip player names of unecessary characters
    names = df.name.tolist()
    new_names = []
    for x in names:
        new_names.append(x.split("\\")[0])
    df.name = new_names
    
    # Clean hand column to replace values with single letter handedness (L or R)
    handedness = df.hand.tolist()
    new_hand = []
    for x in handedness:
        new_hand.append(x.split('/')[0])
    df.hand = new_hand
    
    # Clean salary column to replace salaries with integer values that are stripped of commas and dollar signs
    salary = df.salary.tolist()
    new_salary = []  
    for x in salary:
        x = x.replace(",","")
        new_salary.append(x.split("$")[1])
        
    df.salary = new_salary
    df.salary = df.salary.astype('int')
    
    # Replace exp column (experience) to remove "R" values for rookies. Replacing the values for rooking with 0.5 to signify it is not a full         season played yet 
    
    df.exp.replace({'R':'0.5'}, inplace = True)
    
    # Clean nationality column to replace values with three letter country codes for ease of work in future
    country_dict = {'se':'SWE', 'ca':'CAN', 'us':'USA', 'cz':'CZE', 'fi':'FIN','ru':'RUS', 'ge':'GER'}
    df.nationality = df.nationality.replace(country_dict)


    # Convert height attributes to inches
    heights = df.ht.tolist()
    new_heights = []
    for x in heights:
        x = (int(x.split('-')[0])*12) + (int(x.split('-')[1]))
        new_heights.append(x)
    df.ht = new_heights
    
    # Drop unecessary columns
    df.drop(['summary', 'draft', 'birth_date'], axis = 1, inplace = True)
    
    positions = ['F', 'D']
    df = df[df['pos'].isin(positions)]
    
    df.replace('Jonathan Toews (C)', 'Jonathan Toews', inplace = True)
    
    return df



def clean_full_df(df1, df2, situation):
    team_df = df1[(df1.team == 'CHI') & (df1.situation == f"{situation}")]
    full_df = pd.merge(team_df, df2, on = ['name'], how = 'outer')
    full_df = full_df.drop(labels = ['no.', 'pos'], axis = 1)
    
    
    seabrook = {'name': 'Brent Seabrook', 'nationality':'CAN', 'age': 34, 'ht': 75, 'wt': '220', 'hand':'R', 'exp': 15, 'salary': 6875000}
    sikura = {'name': 'Dylan Sikura', 'nationality': 'CAN', 'age':24, 'ht':71, 'wt':166, 'hand': 'L', 'exp': 3 , 'salary': 750000}
    dehaan = {'name':'Calvin de Haan', 'nationality': 'CAN', 'age':28, 'ht':73, 'wt':195, 'hand': 'L', 'exp': 8 , 'salary': 4550000}
    gilbert = {'name':'Dennis Gilbert', 'nationality': 'USA', 'age':23, 'ht':74, 'wt':216, 'hand': 'L', 'exp': 0.5 , 'salary': 925000}
    nylander = {'name':'Alex Nylander', 'nationality': 'SWE', 'age':22, 'ht':73, 'wt':192, 'hand': 'R', 'exp': 4 , 'salary': 863333}
    quenneville = {'name':'John Quenneville', 'nationality': 'CAN', 'age':23, 'ht':73, 'wt':195, 'hand': 'L', 'exp': 3 , 'salary': 750000}
    wedin = {'name':'Anton Wedin','nationality': 'SWE', 'age':27, 'ht': 71, 'wt':195, 'hand': 'L', 'exp': 0.5 , 'salary': 925000}
    beaudin = {'name':'Nicolas Beaudin','nationality': 'CAN', 'age':20, 'ht':71, 'wt':172, 'hand': 'L', 'exp': 0.5 , 'salary': 894167}
    shaw = {'name':'Andrew Shaw','nationality': 'CAN', 'age':28, 'ht':71, 'wt':182, 'hand': 'R', 'exp': 9 , 'salary':3900000}
    
    
    empty_players = ['Brent Seabrook', 'Dylan Sikura', 'Calvin de Haan', 'Dennis Gilbert', 'Alex Nylander', 'John Quenneville', 'Anton Wedin', 'Nicolas Beaudin', 'Andrew Shaw']
    empty_player_dicts = [seabrook, sikura, dehaan, gilbert, nylander, quenneville, wedin, beaudin, shaw]
    
    for player in empty_players:
        for pdict in empty_player_dicts:
            full_df = full_df[full_df.name == player] = full_df.fillna(pdict)
            
    full_df.drop(full_df.tail(1).index, inplace = True)
    
    return full_df
    
    