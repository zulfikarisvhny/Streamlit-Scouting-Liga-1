import streamlit as st
import pandas as pd
import mplsoccer 
from PIL import Image
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
from utils.st import (
    remote_css,
    local_css,
)

st.set_page_config(
        page_title="PERSIS Dashboard Statistics",
        layout="wide",
        initial_sidebar_state="expanded"
    )

remote_css("https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Poppins:wght@600&display=swap")
local_css("style.css")

header_url = "https://drive.google.com/uc?export=view&id=1ewVlK0aChC0wKiqs8lONEd129r70UQI7"

# Display image with fixed size
st.image(header_url, use_column_width=True)

import streamlit as st

# Define CSS style for box
box_style = '''
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;
    display: inline-block;
    margin: 3px;
    max-width: 25%;
'''

# all text markdown in streamlit app

HEADER_INFO = """""".strip()
SIDEBAR_INFO = """
<div class="contributors font-body text-bold">
<a class="contributor comma>Mehrdad Farahani</a>
<a class="contributor comma" href="https://persissolo.cm">PERSIS Dashboard</a>
</div>
"""
CHEF_INFO = """
<h2 class="font-title">Player Scouting and Pizza Chart <br>BRI Liga 1 2022-2023</h2>
<p class="strong font-body">
<span class="d-block extra-info">Unlock Insights with Player Performance Radar. Dynamic player performance radar delivers actionable insights on-demand, featuring top performers from BRI Liga 1 2022/2023. 
Simply apply the filters below to customize your view, 
and adjust them at any time from our intuitive dashboard. See player performance like never before, and take your game to the next level.</span>
</p>
""".strip()
STORY = """
<div class="story-box font-body">
<p>
Filter yang dapat digunakan untuk menentukan usia, menit bermain, dan asal pemain
</p>

</div>
""".strip()

# READ DATA
excel_file = 'Wyscout Liga 1.xlsx'
sheet_name = 'Search results (436)'

df = pd.read_excel(excel_file, 
                   sheet_name,
                   usecols = 'A:DL',
                   header=0,
                   )

all_value = df[['Player', 'Team', 'Position', 'Age', 'Contract expires','Matches played', 'Minutes played', 'Passport country', 'Fix Image', 'Foot', 'Height', 'Weight', 'Img Foot',
                'Goals', 'Shots per 90', 'Non-penalty goals per 90', 'xG per 90', 'xG', 'Shots', 
                'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90', 'Passes to penalty area per 90', 
                'Through passes per 90', 'Deep completions per 90', 'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90',
                'Successful dribbles, %', 'PAdj Sliding tackles', 'PAdj Interceptions', 'Defensive duels per 90', 'Defensive duels won, %', 
                'Passes to final third per 90', 'Progressive passes per 90', 'Passes per 90', 'Long passes per 90', 'Accurate long passes, %', 
                'Forward passes per 90', 'Crosses per 90', 'Accurate crosses, %', 'Shots blocked per 90', 'Aerial duels won, %']] 

# add new column with arithmetic operation from 2 column or more

# part goal threat add 2 column 
all_value['xG/ Shots'] = all_value['xG']/all_value['Shots']
all_value['Goals - xG'] = all_value['Goals'] - all_value['xG']

# part in possession add 2 column
all_value['Long pass proportion %'] = all_value['Long passes per 90']/all_value['Passes per 90']*100
all_value['Forward pass ratio %'] = all_value['Forward passes per 90']/all_value['Passes per 90']*100

# part out possession add 1 column and just add PAdj Interception and Sliding Tackles
all_value['PAdj Int + Tkl'] = all_value['PAdj Sliding tackles'] + all_value['PAdj Interceptions']

# delete and drop some column have done to get new column with the number from this column
all_value = all_value.drop(['xG', 
                  'Shots', 
                  'PAdj Interceptions', 
                  'PAdj Sliding tackles', 
                  'Goals', 
                  'Long passes per 90',
                  'Forward passes per 90'], 
                 axis=1)
all_value['Minutes played'] = all_value['Minutes played'].astype('float')
all_value['Age'] = all_value['Age'].astype('float')

# re-define data and index column with arrangment to be used in visualization
all_value = all_value[['Player', 'Team', 'Position', 'Age', 'Contract expires','Matches played', 'Minutes played', 'Passport country', 'Fix Image',  'Foot', 'Height', 'Weight', 'Img Foot',
             'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
             'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
             'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
             'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]

def dfpercentile(all_value):
    personal_data = all_value.iloc[:, :13]  # data personal player 
    number_data = all_value.iloc[:, 13:]    # number of statistics player
    
    number_data = number_data.fillna(0)
    number_data = number_data.apply(lambda x: x.rank(pct=True)).applymap(lambda x: x*100)
    number_data = number_data.round().astype(int)

    all_value = pd.concat([personal_data, number_data], axis = 1)

    #center_back = all_value[['Non-penalty goals per 90', 'xG per 90', 'Shots per 90', 'Assists per 90', 'Key passes per 90', 'Passes to final third per 90', 'Through passes per 90', 'Progressive passes per 90', 'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
    #fullback = all_value[['Non-penalty goals per 90', 'xG per 90', 'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to final third per 90', 'Passes to penalty area per 90', 'Progressive passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Progressive runs per 90', 'Crosses per 90', 'Accurate crosses, %', 'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
    #central_midfielder = all_value[['Non-penalty goals per 90', 'xG per 90', 'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 'Passes per 90', 'Accurate passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
    #attacking_midfielder = all_value[['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 'Passes per 90', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
    #wingers = all_value[['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
    #central_forward = [['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Aerial duels won, %']]
    return all_value
    #center_back, fullback, central_midfielder, attacking_midfielder, wingers, central_forward

def bikinpizza(all_value):  
    scout = all_value.loc[all_value['Player'] == player]

    if position == "Center Back":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 'Shots per 90', 
                    'Assists per 90', 'Key passes per 90', 'Passes to final third per 90', 'Through passes per 90', 'Progressive passes per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 3 + ["#adaf15"] * 5 + ["#a215af"] * 6 + ["#2115af"] * 5
        text_colors = ["#FAFAFA"] * 3 + ["#0E1117"] * 5 + ["#FAFAFA"] * 11
        #print(len(params), len(values))
    elif position == "Fullback":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to final third per 90', 'Passes to penalty area per 90', 'Progressive passes per 90',
                    'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Progressive runs per 90', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 2 + ["#adaf15"] * 6 + ["#a215af"] * 6 + ["#2115af"] * 5
        text_colors = ["#FAFAFA"] * 2 + ["#0E1117"] * 6 + ["#FAFAFA"] * 11
        
    elif position == "Central Midfielder":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 2 + ["#adaf15"] * 9 + ["#a215af"] * 6 + ["#2115af"] * 5
        text_colors = ["#FAFAFA"] * 2 + ["#0E1117"] * 9 + ["#FAFAFA"] * 11
        #print(len(params), len(values))
    elif position == "Attacking Midfielder":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Passes per 90', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 5 + ["#adaf15"] * 8 + ["#a215af"] * 4 + ["#2115af"] * 3
        text_colors = ["#FAFAFA"] * 5 + ["#0E1117"] * 8 + ["#FAFAFA"] * 7
        #print(len(params), len(values))
    elif position == "Wingers":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 5 + ["#adaf15"] * 6 + ["#a215af"] * 6 + ["#2115af"] * 3
        text_colors = ["#FAFAFA"] * 5 + ["#0E1117"] * 6 + ["#FAFAFA"] * 9
        #print(len(params), len(values))
    elif position == "Forward":
        values_scout = scout[['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %',
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Aerial duels won, %']]
        params = list(values_scout.columns)
        values_scout = values_scout.values
        values_scout = values_scout.tolist()
        values_scout = values_scout[0]

        # define the color palete and hexagon color
        slice_colors = ["#22af15"] * 5 + ["#adaf15"] * 6 + ["#a215af"] * 4 + ["#2115af"] * 4
        text_colors = ["#FAFAFA"] * 5 + ["#0E1117"] * 6 + ["#FAFAFA"] * 8
        #print(len(params), len(values))
    # create diagram dan pizza chart basic
    baker = PyPizza(
        params = params, 
        background_color="#0E1117", 
        straight_line_color="#0E1117",
        straight_line_lw=1, 
        last_circle_lw=0, 
        other_circle_lw=0, 
        inner_circle_size=2
        )

    fig, ax = baker.make_pizza(
        values_scout, compare_values = values_average,
        figsize = (8, 8),
        color_blank_space = "same", 
        slice_colors = slice_colors,
        value_colors = text_colors, 
        value_bck_colors = slice_colors,
        blank_alpha = 0.35,
        kwargs_slices = dict(
            edgecolor = "none", zorder = 0, linewidth = 1),
        kwargs_compare = dict(
            facecolor = "none", edgecolor="#0E1117", zorder = 8, linewidth = 1, ls = '--'),
        kwargs_params = dict(
            color = "#FAFAFA", fontsize = 5, va = "center"),
        kwargs_values = dict(
            color = "#0E1117", fontsize = 7, zorder = 2,
            bbox = dict(
                edgecolor = "#FAFAFA", boxstyle = "round,pad = 0.2", lw = 1)),
        kwargs_compare_values = dict(
            color = "#252627", fontsize = 12, zorder = 3, alpha = 0,
            bbox = dict(
                edgecolor = "#252627", facecolor = "#E1E2EF",
                boxstyle = "round,pad = 0.2", lw = 1, alpha = 0
                )
            )
        )
    fig.text(0.515, 0.975, f"{player} - {teamplay}", size=13,
            ha="center", color="#FAFAFA", weight='bold')
    fig.text(0.515, 0.953, f"Percentile Rank {position} vs {all_team} Player",
            size=9, ha="center", color="#FAFAFA")
    fig.text(0.268, 0.935, "Goal Threat                  Playmaking               In Possession                  Out of Possession",
                    size=7, color="#FAFAFA", va='center')
    fig.patches.extend([
        plt.Rectangle((0.247, 0.9275), 0.015, 0.015, fill=True, color="#22af15", transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.390, 0.9275), 0.015, 0.015, fill=True, color="#adaf15", transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.515, 0.9275), 0.015, 0.015, fill=True, color="#a215af", transform=fig.transFigure, figure=fig),
        plt.Rectangle((0.668, 0.9275), 0.015, 0.015, fill=True, color="#2115af", transform=fig.transFigure, figure=fig)])
    
    return fig
      
# view
col1, col2 = st.columns([5, 2])
with col1:
        st.markdown(HEADER_INFO, unsafe_allow_html=True)
        st.markdown(CHEF_INFO, unsafe_allow_html=True)
        team = st.selectbox('Select team', pd.unique(all_value['Team']))
        position = st.selectbox('Select Position', ['Center Back', 'Fullback', 'Central Midfielder', 'Attacking Midfielder', 'Wingers', 'Forward'])
        if position == 'Center Back':
                all_value = all_value[all_value['Position'].str.contains('CB')]
        elif position == 'Fullback':
                all_value = all_value[all_value['Position'].str.contains('RB')|
                                      all_value['Position'].str.contains('LB')|
                                      all_value['Position'].str.contains('RWB')|
                                      all_value['Position'].str.contains('LWB')]
        elif position == 'Central Midfielder':
                all_value = all_value[all_value['Position'].str.contains('CMF')]
        elif position == 'Attacking Midfielder':
                all_value = all_value[all_value['Position'].str.contains('AMF')]
        elif position == 'Forward':
                all_value = all_value[all_value['Position'].str.contains('CF')]
        else:
                all_value = all_value[all_value['Position'].str.contains('RW')|
                                      all_value['Position'].str.contains('LW')|
                                      all_value['Position'].str.contains('RWF')|
                                      all_value['Position'].str.contains('LWF')]
with col2:
        st.markdown(SIDEBAR_INFO, unsafe_allow_html=True)
        st.markdown(STORY, unsafe_allow_html=True)
        min_age = float(all_value['Age'].min())
        max_age = float(all_value['Age'].max())
        age_filter = st.slider(
                   'Select a age of player',
                   all_value['Age'].min(), all_value['Age'].max(), (min_age, max_age))
        all_value = all_value[all_value['Age'].between(age_filter[0], age_filter[1])]
        max_minutes = float(all_value['Minutes played'].max())
        minutes_filter = st.slider(
                   'Select a minutes played of player',
                   all_value['Minutes played'].min(), all_value['Minutes played'].max(), (1000.0, max_minutes))
        all_value = all_value[all_value['Minutes played'].between(minutes_filter[0], minutes_filter[1])]
        country = st.radio(
               "Local or foreigner player",
               ('Local', 'Foreigner', 'All Player'))
        if country == 'Local':
               all_value = all_value[all_value['Passport country'].str.contains('Indonesia')]
        elif country == 'Foreigner':
               all_value = all_value[~all_value['Passport country'].str.contains('Indonesia')]
        else:
               all_value = all_value


st.markdown(
       "<hr />",
       unsafe_allow_html=True
    )
all_teams = st.checkbox(f'Compare with {position} in all team')
if all_teams:
    all_team = "BRI Liga 1 2022/2023"
else:
    all_value = all_value[all_value['Team'] == team]
    all_team = team
SECTION_TWO = """
<h4 class="font-title">List Top {} Players in {}</h4>
<p class="strong font-body">
<span class="d-block extra-info">Our performance ratings algorithm identifies the top {} players in {} based on average ratings across key metrics.</span>
</p>""".format(position, all_team, position, all_team)
st.markdown(SECTION_TWO, unsafe_allow_html=True)
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric(label = 'Total Player', value = len(all_value))
m2.metric(label = 'Minimum Age', value = int(age_filter[0]))
m3.metric(label = 'Maximum Age', value = int(age_filter[1]))
m4.metric(label = 'Minutes Played Minimum', value = round(minutes_filter[0]))
m5.metric(label = 'Minutes Played Maximum', value = round(minutes_filter[1]))
m6.metric(label = 'Type Player', value = country)

all_value = all_value[['Player', 'Team', 'Position', 'Age', 'Contract expires','Matches played', 'Minutes played', 'Passport country', 'Fix Image',  'Foot', 'Height', 'Weight', 'Img Foot',
             'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
             'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
             'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
             'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
number = ['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
             'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
             'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
             'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']

averages = pd.DataFrame(all_value[number].mean()).T
averages['Player'] = 'Average'
averages['Team'] = 'Average'
averages['Position'] = 'Average'
averages['Age'] = 'Average'
averages['Contract expires'] = 'Average'
averages['Matches played'] = 'Average'
averages['Minutes played'] = 'Average'
averages['Passport country'] = 'Average'
averages['Fix Image'] = 'Average'
averages['Foot'] = 'Average'
averages['Height'] = 'Average'
averages['Weight'] = 'Average'
averages['Img Foot'] = 'Average'

# Append 'Average' row to the DataFrame
all_value = pd.concat([all_value, averages], ignore_index=True)

#all_value = pd.concat([all_value[['Player', 'Team', 'Position', 'Age', 'Contract expires', 'Matches played', 'Minutes played', 'Passport country', 'Fix Image', 'Foot', 'Height', 'Weight', 'Img Foot']], averages], ignore_index=True)
show_data = dfpercentile(all_value)
if position == 'Center Back':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 'Shots per 90', 
                    'Assists per 90', 'Key passes per 90', 'Passes to final third per 90', 'Through passes per 90', 'Progressive passes per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
      column_number = ['Non-penalty goals per 90', 'xG per 90', 'Shots per 90', 
                    'Assists per 90', 'Key passes per 90', 'Passes to final third per 90', 'Through passes per 90', 'Progressive passes per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)

elif position == 'Fullback':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to final third per 90', 'Passes to penalty area per 90', 'Progressive passes per 90',
                    'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Progressive runs per 90', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
      column_number = ['Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to final third per 90', 'Passes to penalty area per 90', 'Progressive passes per 90',
                    'Accurate passes, %', 'Long pass proportion %', 'Accurate long passes, %', 'Progressive runs per 90', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)

elif position == 'Central Midfielder':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']]
      column_number =['Non-penalty goals per 90', 'xG per 90', 
                    'Non-penalty goals per 90', 'xG per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Second assists per 90','Passes to final third per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Progressive passes per 90', 'Deep completions per 90', 
                    'Passes per 90', 'Accurate passes, %', 'Forward pass ratio %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Shots blocked per 90', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)

elif position == 'Attacking Midfielder':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
      column_number = ['Non-penalty goals per 90', 'xG per 90', 
                    'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)

elif position == 'Wingers':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']]
      column_number = ['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %', 'Crosses per 90', 'Accurate crosses, %', 
                    'PAdj Int + Tkl', 'Defensive duels won, %', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)

elif position == 'Forward':
      show_data = show_data[['Player', 'Team', 'Position', 'Age',
                    'Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %',
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Aerial duels won, %']]
      column_number = ['Non-penalty goals per 90', 'xG per 90', 'xG/ Shots', 'Goals - xG', 'Shots per 90', 
                    'Assists per 90', 'xA per 90', 'Key passes per 90', 'Passes to penalty area per 90', 'Through passes per 90', 'Deep completions per 90', 
                    'Accurate passes, %', 'Progressive runs per 90', 'Dribbles per 90', 'Successful dribbles, %',
                    'PAdj Int + Tkl', 'Defensive duels per 90', 'Defensive duels won, %', 'Aerial duels won, %']
      average_value = show_data.loc[show_data['Player'] == 'Average']
      average_value = average_value.drop(['Team', 'Position', 'Age'], axis=1)
      values_average = average_value.iloc[0, 1:].tolist()
      show_data = show_data.loc[show_data['Player'] != 'Average']
      show_data['Rating'] = show_data[column_number].mean(axis=1)
      show_data = show_data[['Player', 'Team', 'Position', 'Age', 'Rating']]
      st.dataframe(show_data, use_container_width=True)


col111, col112 = st.columns([1.9, 5])
with col111:
    player = st.selectbox('Select Player to See Details', pd.unique(all_value['Player']))
    img_url = str(all_value[all_value['Player'] == player]['Fix Image'].iloc[0])
st.markdown(
       "<hr />",
       unsafe_allow_html=True
    )
st.markdown(
    f"""
    <style>
        .square-img {{
        border-radius: 10px;
        object-fit: cover;
        width: 300px;
        height: 420px;
        overflow: hidden;
        border: 2px solid green;
    }}
</style>
""",
unsafe_allow_html=True
)

st.markdown(
    f"""
    <style>
        .withoutborder-img {{
        object-fit: cover;
        width: 80px;
        height: 60px;
        overflow: hidden;
        margin: 20px;
    }}
</style>
""",
unsafe_allow_html=True
)

postion = str(all_value[all_value['Player'] == player]['Position'].iloc[0])
teamplay = str(all_value[all_value['Player'] == player]['Team'].iloc[0])
height = str(all_value[all_value['Player'] == player]['Height'].iloc[0])
weight = str(all_value[all_value['Player'] == player]['Weight'].iloc[0])
foot_url = str(all_value[all_value['Player'] == player]['Img Foot'].iloc[0])
age = int(all_value[all_value['Player'] == player]['Age'].iloc[0])
nation = str(all_value[all_value['Player'] == player]['Passport country'].iloc[0])
menit = int(all_value[all_value['Player'] == player]['Minutes played'].iloc[0])

PLAYER_INFO = """
<h2 class="font-title">{} ({})</h2>
<h4 class="font-title">{}</h4>
<p class="strong font-body">
<span class="d-block extra-info">Pemain dari {} tahun 2022 2023 ini merupakan pemain yang berasal dari {} dan berposisi sebagai {}, {} berusia {} dan sudah mengemas {} menit bermain bersama {}.</span>
</p>""".format(player, age, teamplay, teamplay, nation, position, player, age, menit, teamplay)

BIODATA = """
<p class="strong font-body">
<span class="text-bold">Height: {} | Weight: {}</span>
</p>""".format(height, weight)

col21, col22 = st.columns([3, 6])
with col21:
       st.markdown(f'<img class="square-img" src="{img_url}">', unsafe_allow_html=True)
with col22:
       st.markdown(PLAYER_INFO, unsafe_allow_html=True)
       st.markdown(BIODATA, unsafe_allow_html=True)
       st.markdown(f'<div style="{box_style}">{postion}</div>', unsafe_allow_html=True)
       st.markdown(f'<img class="withoutborder-img" src="{foot_url}">', unsafe_allow_html=True)
       # Get input text from user
       #text = st.text_input('Enter text')
       #if text:
       #       st.markdown(f'<div style="{box_style}">{text}</div>', unsafe_allow_html=True)

st.markdown(
       "<hr />",
       unsafe_allow_html=True
    )

#a = dfpercentile(all_value)
#scout = dfpercentile(all_value)[dfpercentile(all_value)['Player'] == player]
#st.dataframe(scout)
st.pyplot(bikinpizza(dfpercentile(all_value)))




