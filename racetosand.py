import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt
from PIL import Image


# Formattering av sidan
im = Image.open('r2s3.png')
st.set_page_config(page_title="Race to Hills 2024", page_icon = im)
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

df_comps = pd.read_excel("Data.xlsx", sheet_name='Spelschema')
df_leaderboard = pd.read_excel("Data.xlsx", sheet_name='Leaderboard')
df_plotdata = pd.read_excel("Data.xlsx", sheet_name='Leaderboard Utveckling')
df_boter = pd.read_excel("Data.xlsx", sheet_name="Böteskassa")

today = dt.date.today()
finalen = dt.date(2024, 9, 7)
diff = finalen - today
diff_days = diff.days

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.image('r2s3.png')

with col3:
    st.write(' ')

col1, col2, col3 = st.columns(3)
with col1:
    st.write(' ')

with col2:
    st.title('Race to Hills 2024')

with col3:
    st.write(' ') 
    

st.divider()

# selection = st.radio("Välkommen till en liten samlingssida för Race to Hills 2024! Välj bland nedan menyer:", ('Bilder', 'Leaderboard', 'Spelschema', 'Böteskassa', 'Countdown'), horizontal=True)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(['🏆 Leaderboard', '📅 Spelschema', '💸 Böteskassa', '📸 Bilder', '⏱️ Countdown', 'Uppdatera leaderboard'])

# Leaderboardtab
tab1.header("Leaderboard 2024")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

tab1.subheader("Utveckling Leaderboard 2024")
tab1.line_chart(df_plotdata, x='Deltävling', y='Poäng', color='Spelare')

tab1.divider()

tab1.header("Antal vinster under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal vinster']].sort_values('Antal vinster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

tab1.divider()

tab1.header("Antal sistaplatser under året:")
tab1.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal förluster']].sort_values('Antal förluster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

# Spelschematab
tab2.header("Spelschema 2024")
tab2.dataframe(df_comps, use_container_width=True, hide_index=True, column_config={' ':st.column_config.ImageColumn()}) 

# Böteskassatab
tab3.header("Böteskassa")
bot = df_boter.iloc[0,1]
tab3.write('Böteskassan ligger för närvarande på: {:}kr'.format(bot))

#Bildtab
tab4.image("bild1.jpg")
tab4.image("bild2.jpeg")
tab4.image("bild3.jpeg")
tab4.image("bild4.jpeg")
tab4.image("bild5.jpg")

#Countdowntab
tab5.header('Nedräkning till finalen')
tab5.write('Nu är det endast {:} dagar kvar till finalen. TAGGA!!'.format(diff_days))
tab5.image("beer.jpg")


#Uppdatera leaderboard
tab6.header("Här kan du uppdatera leaderboarden efter tävling")
num_players = tab6.selectbox('Hur många spelare var med i deltävlingen?', ('3', '4', '5', '6', '7', '8', '9', '10', '11', '12'),index=None, key='antal', placeholder=' ')
players = tab6.multiselect('Vilka spelare var med?', ('Axel', 'Crille', 'Jojo', 'Frasse', 'Rantzow', 'Alvin', 'Benne', 'Löken', 'Sebbe', 'Dempa', 'Vigge'), key='spelare', placeholder='')
major_flg = tab6.selectbox('Var tävlingen en major?', ('Ja', 'Nej'), index=None, key='major', placeholder=' ')
