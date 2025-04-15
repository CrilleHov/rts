import streamlit as st
from streamlit import connections
import pandas as pd
import numpy as np
import datetime as dt
from st_social_media_links import SocialMediaIcons
import psycopg2
from psycopg2 import Error


st.set_page_config(page_title="Race to Hills 2025")
hide_default_format = """
       <style>
       #MainMenu {visibility: hidden; }
       footer {visibility: hidden;}
       </style>
       """
st.markdown(hide_default_format, unsafe_allow_html=True)

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["supabase"]["host"],
        database=st.secrets["supabase"]["database"],
        user=st.secrets["supabase"]["user"],
        password=st.secrets["supabase"]["password"],
        port=st.secrets["supabase"]["port"]
    )

conn = get_connection()
cursor = conn.cursor()


try:
    cursor.execute("SELECT * FROM spelare;")
    df_golfid = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
except Exception as e:
    st.error(f"Fel vid datahämtning från 'spelare': {e}")
    conn.rollback()
    st.stop()
       
# Hämta data med querys
try:


    st.write("Getting table2")
    cursor.execute("SELECT * FROM competitions;")
    df_spelschema = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    st.write("Getting table3")
    cursor.execute("""
        SELECT spelare AS Spelare, 
            SUM(poäng) AS poäng,
            SUM(CASE WHEN poäng != 0 THEN 1 ELSE 0 END) AS antal_comps,
            SUM(CASE WHEN placering = 1 THEN 1 ELSE 0 END) AS antal_vinster,
            SUM(CASE WHEN placering = antal_spelare THEN 1 ELSE 0 END) AS antal_losses
        FROM leaderboard
        GROUP BY spelare;
    """)
    df_leaderboard = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    cursor.execute("SELECT * FROM leaderboard;")
    df_leaderboard_chart = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    cursor.execute("""
        SELECT spelare,
            ROUND(SUM(bötesbelopp)) AS total_böter
        FROM fees
        GROUP BY spelare;
    """)
    df_böter = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

    cursor.execute("SELECT * FROM tot_böter WHERE datum = (SELECT MAX(datum) FROM tot_böter);")
    df_tot_böter = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])

except Exception as e:
    st.error(f"Något gick fel med datahämtningen: {e}")
    conn.rollback()
    st.stop()



df_leaderboard_chart = (
    df_leaderboard_chart
    .assign(tävling=lambda x: pd.to_datetime(x['tävling']))
    .sort_values(['spelare', 'tävling'])
    .assign(totala_poäng=lambda x: x.groupby('spelare')['poäng'].cumsum())
)

df_leaderboard = df_leaderboard.rename(columns={'spelare': 'Spelare',
                                                'poäng':'Totala poäng', 
                                                'antal_comps':'Antal spelade tävlingar',
                                                'antal_vinster':'Antal vinster',
                                                'antal_losses':'Antal sistaplatser'})

df_böter['total_böter'] = df_böter['total_böter'].round(0).astype(int)

# Funktion för att hämta rätt poäng efter placering, hur många spelare som var med, och om tävlingen var en major
def get_points(placering=1, antal_spelare=3, major_flag='Nej'):
    if placering == 0:
        return 0
    else:
        antal_spelare = int(antal_spelare)
        if major_flag == 'Ja':
            points = df_point_major.loc[placering, antal_spelare]
        else:
            points = df_point_nonmajor.loc[placering, antal_spelare]
        return points
    

# Poängsystem
df_point_nonmajor = pd.DataFrame({
            3: [4,2,1,0,0,0,0,0,0,0,0,0],
            4: [5,3,2,1,0,0,0,0,0,0,0,0],
            5: [6,4,3,2,1,0,0,0,0,0,0,0],
            6: [7,5,4,3,2,1,0,0,0,0,0,0],
            7: [8,6,5,4,3,2,1,0,0,0,0,0],
            8: [9,7,6,5,4,3,2,1,0,0,0,0],
            9: [10,8,7,6,5,4,3,2,1,0,0,0],
            10:[11,9,8,7,6,5,4,3,2,1,0,0],
            11:[12,10,9,8,7,6,5,4,3,2,1,0],
            12:[13,11,10,9,8,7,6,5,4,3,2,1]
            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])

df_point_major = pd.DataFrame({
            3: [5,2.5,1,0,0,0,0,0,0,0,0,0],
            4: [6,3.5,2,1,0,0,0,0,0,0,0,0],
            5: [7,4.5,3,2,1,0,0,0,0,0,0,0],
            6: [8,5.5,4,3,2,1,0,0,0,0,0,0],
            7: [9,6.5,5,4,3,2,1,0,0,0,0,0],
            8: [10,7.5,6,5,4,3,2,1,0,0,0,0],
            9: [11,8.5,7,6,5,4,3,2,1,0,0,0],
            10:[12,9.5,8,7,6,5,4,3,2,1,0,0],
            11:[13,10.5,9,8,7,6,5,4,3,2,1,0],
            12:[14,11.5,10,9,8,7,6,5,4,3,2,1]
            }, index=[1,2,3,4,5,6,7,8,9,10,11,12])


player_names = ["Benne", "Löken", "Vigge", "Frasse", "Rantzow",
                    "Alvin", "Jojo", "Axel", "Sebbe", "Crille"]



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
    st.title('Race to Hills 2025')

with col3:
    st.write(' ') 
    

st.write("")
st.write("Välkomna till en ny rafflande upplaga av Race to Hills 2025. "
            "Vi kommer under året att spela sex stycken deltävlingar innan finalen går av stapeln i Göteborg den 15 - 17 augusti.")
st.write("")
st.write("Väl mött!")

social_media_links = [
    "https://www.instagram.com/racetosand/",
]
social_media_icons = SocialMediaIcons(social_media_links)
social_media_icons.render()

st.divider()

# Skapa tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(['🏆 Leaderboard', 
                                                          '📅 Spelschema', 
                                                          '💸 Böteskassa', 
                                                          '📸 Bilder', 
                                                          '⏱️ Countdown',
                                                          '🏅 Tidigare vinnare', 
                                                          'Uppdatera leaderboard', 
                                                          'Golf-id'])



# Leaderboardtab
with tab1:
    tab1.dataframe(df_leaderboard.sort_values('Totala poäng', ascending=False), use_container_width=True, 
                   hide_index=True)

    tab1.line_chart(df_leaderboard_chart, x='tävling', y='totala_poäng', color='spelare', 
                    width=800, height=500, x_label = 'Datum', y_label='Totala poäng')

    with st.form(key='update', border=False):
        update = st.form_submit_button(label='Uppdatera sidan')
        if update:
            st.cache_data.clear()
            st.rerun()



# Spelschematab
df_spelschema = df_spelschema.rename(columns={'datum': 'Datum',
                                              'bana':'Bana',
                                              'hosts':'Hosts',
                                              'major':'Major',
                                              'plats':'Plats',
                                              'år':'År'
                                              })
with tab2:
    year = tab2.radio("Vilket år vill du se spelschema för?",
                        ['2024', '2025'], 1)
    tab2.header("Spelschema {:}".format(year))
    tab2.dataframe(df_spelschema[df_spelschema["År"] == year], use_container_width=True, 
                   hide_index=True)


# Böteskassa
with tab3:
    tab3.header("Böteskassa 2025")

    tab3.subheader("Total böteskassa:")
    tab3.write(f"Total böteskassa är för närvarande på {df_tot_böter.iloc[0,1]} kr (uppdaterat: {df_tot_böter.iloc[0,0]})")

    tab3.divider()
    tab3.subheader("Nedan ser ni bötesbeloppen för 2025 års säsong:")
    tab3.write("")
    tab3.write("Streck/0 poäng: 10kr")
    tab3.write("Kissar på golfbanan: 50kr")
    tab3.write("Kastar utrustning: 50kr/gång")
    tab3.write("Kastar boll: 15kr/boll")
    tab3.write("Tappar bort järnheadcovers: 50kr/styck")
    tab3.write("Inte på golfbanan 30 min innan FÖRSTA starttid: 50kr")
    tab3.write("Har ej straffutrustning: 1000kr")
    tab3.write("Inte har minst ett Race to Sand-plagg på sig: 100kr")
    tab3.write("Bira-boll: 20kr")
    tab3.write("HIO/Albatross ska de andra spelarna böta: 100kr")
    tab3.write("Ej tillgänglig att scoreföra på Gamebook: 100kr")
    tab3.write("Host har inte med priset till deltävling: 500kr")

    tab3.divider()

    tab3.subheader("Nedan ser ni total inbetald bötesbelopp under säsongen, per spelare:")

    for row in df_böter.itertuples():
        st.write(f"{row.spelare}:  {row.total_böter} kr")
    
    tab3.write("")
    tab3.bar_chart(df_böter, x='spelare', y='total_böter', x_label='Spelare', y_label='Total böter, kr', color='spelare')

    tab3.divider()

    tab3.subheader("Efter varje deltävling, fyll i hur mycket böter spelaren fick i formuläret nedan:")
    
    # Formulär för att fylla i spelarnas böter efter varje deltävling
    with st.form(key='fee_form'):
        fees = {}
        for player in player_names:
            fee = st.number_input(f"Böter för {player}", min_value=0, step=1, key=player)
            fees[player] = fee
        
        submit_button = st.form_submit_button(label='Uppdatera spelarböter')

        if submit_button:
            try:
                for player, fee in fees.items():
                    cursor.execute(
                        "INSERT INTO böter (spelare, bötesbelopp) VALUES (%s, %s);",
                        (player, fee)
                    )
                conn.commit()
                st.success("Bötesbeloppen är uppdaterade.")
                st.cache_data.clear()
                st.rerun()
            except Error as e:
                conn.rollback()
                st.error(f"Något gick fel vid uppdatering av böter: {e}")


# Bildtab
with tab4:
    tab4.image("bild6.jpg")
    tab4.image("bild1.jpg")
    tab4.image("bild2.jpeg")
    tab4.image("bild3.jpeg")
    tab4.image("bild4.jpeg")
    tab4.image("bild5.jpg")


# Countdowntab
diff = dt.date(2025, 8, 14) - dt.date.today()
diff_days = diff.days
with tab5:
    tab5.header('Nedräkning till finalen')
    tab5.write('Nu är det endast {:} dagar kvar till finalen. TAGGA!!'.format(diff_days))
    tab5.image("hills.jpeg")
    tab5.image("beer2.jpeg")


# Historiska vinnare
with tab6:
    tab6.header('Tidigare vinnare')
    tab6.write('2019: Alvin')
    tab6.write('2020: Crille')
    tab6.write('2021: Frasse')
    tab6.write('2022: Löken')
    tab6.write('2023: Alvin')
    tab6.write('2024: Frasse')
    tab6.write('2025: TBD (Axel känns het i år)')


# Uppdatera leaderboarden
with tab7:
    tab7.header('Uppdatera leaderborden:')
    tab7.write('Fyll i vilken tävling och placering för respektive spelare. Om någon inte spelade, fyll i "0"')


    comps = df_spelschema[df_spelschema['År'] == '2025']['Datum']
    comp = tab7.selectbox('Vilken deltävling?', comps,
                          index=None, key='tävling', placeholder=' ')
    
    num_players = tab7.selectbox('Hur många spelare var med i deltävlingen?', 
                                 ('','3', '4', '5', '6', '7', '8', '9', '10', '11', '12'),
                                 index=None, key='antal', placeholder=' ')
    
    majorflag = tab7.selectbox('Var tävlingen en major?', ('Ja', 'Nej'), index=None, key='major', placeholder='')




    with st.form(key='leaderboard_form'):
        placering = {}
        for player in player_names:
            placering_spelare = st.number_input(f"Vilken placering fick {player}", min_value=0, step=1, key=player+' ')
            placering[player] = placering_spelare
        
        submit_button = st.form_submit_button(label='Uppdatera leaderboard')




        if submit_button:
            placering2 = {}
            for player in player_names:
                placering_spelare = int(placering[player])
                placering2[player] = {
                    'point': get_points(placering_spelare, num_players, majorflag),
                    'placering': placering_spelare
                }

            try:
                for player, data in placering2.items():
                    cursor.execute("""
                        INSERT INTO leaderboard (tävling, spelare, poäng, placering, antal_spelare)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (comp, player, data['point'], data['placering'], num_players))
                conn.commit()

                st.success("Leaderboarden är uppdaterad.")
                spelade = sum(1 for p in placering.values() if p > 0)
                if spelade != int(num_players):
                    st.warning(f"Du angav att {num_players} spelade men du har fyllt i {spelade} placeringar... Kontakta IT för att rätta i databasen!")
                else:
                    st.cache_data.clear()
                    st.rerun()
            except Error as e:
                conn.rollback()
                st.error(f"Något gick fel vid uppdatering av böter: {e}")



# Golf-id
with tab8:
    tab8.title("Golf-id för respektive spelare")
    for row in df_golfid.itertuples():
        st.write(f"{row.spelarnamn}  {row.golfid}")
