import streamlit as st
import numpy as np
import pandas as pd
import datetime as dt

df_comps = pd.read_excel("Data.xlsx", sheet_name='Spelschema')
# df_comps.set_index(df_comps.columns[0], inplace=True)
df_leaderboard = pd.read_excel("Data.xlsx", sheet_name='Leaderboard')
# df_leaderboard.set_index(df_leaderboard.columns[0], inplace=True)
# df_leaderboard.rename(index={0:'Namn'}, inplace=True)
df_boter = pd.read_excel("Data.xlsx", sheet_name="Böteskassa")
# df_vinst.set_index(df_vinst.columns[0], inplace=True)

today = dt.date.today()
finalen = dt.date(2024, 9, 7)
diff = finalen - today
diff_days = diff.days

st.title("Race to Hills 2024")

selection = st.radio("Välkommen till en liten samlingssida för Race to Hills 2024! Välj bland nedan menyer:", ('Bilder', 'Leaderboard', 'Spelschema', 'Böteskassa', 'Countdown'), horizontal=True)

if selection == 'Spelschema':
    st.subheader("Spelschema 2024")
    st.dataframe(df_comps, use_container_width=True, hide_index=True, column_config={' ':st.column_config.ImageColumn()})  

if selection == 'Bilder':
    st.image("bild1.jpg")
    st.image("bild2.jpeg")
    st.image("bild3.jpeg")
    st.image("bild4.jpeg")
    st.image("bild5.jpg")

if selection == 'Leaderboard':
    st.subheader("Leaderboard 2024")
    st.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Poäng']].sort_values('Poäng', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})
    st.write("P.S. Dubbelklicka för större bild")

    st.subheader("Antal vinster under året:")
    st.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal vinster']].sort_values('Antal vinster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

    st.subheader("Antal sistaplatser under året:")
    st.dataframe(df_leaderboard[['Spelarbild', 'Spelarnamn', 'Antal förluster']].sort_values('Antal förluster', ascending=False), hide_index=True, column_config={'Spelarbild':st.column_config.ImageColumn()})

if selection == 'Böteskassa':
    st.subheader("Böteskassa")
    bot = df_boter.iloc[0,1]
    st.write('Böteskassan ligger för närvarande på: {:}kr'.format(bot))

if selection == 'Countdown':
    st.write('Nu är det endast {:} dagar kvar till finalen. TAGGA!!'.format(diff_days))
    st.image("beer.jpg")

