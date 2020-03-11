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