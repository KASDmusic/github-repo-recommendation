import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configuration de la connexion à la base de données
def get_connection():
    return psycopg2.connect(
        dbname="mydatabase",
        user="myuser",
        password="mypassword",
        host="postgres",
        port=5432
    )

# Fonction pour récupérer les données
def get_notes_data():
    query = """
        SELECT *
        FROM notes
        ORDER BY date;
    """
    
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

data = get_notes_data()
data["date"] = pd.to_datetime(data["date"])

data_notes_by_date = data.groupby("date")["note"].mean().reset_index()

# Configuration de l'interface Streamlit
st.title("Suivi de l'évolution des notes moyennes")

# Récupération des données

if data.empty:
    st.write("Aucune donnée disponible.")
else:
    # Affichage d'indacteurs qui sont la moyenne sur le dernier mois et la moyenne sur les 3 derniers mois en filtrant en utilisant la date du jour
    st.write("### Indicateurs")
    last_month_avg = data_notes_by_date[data_notes_by_date["date"] >= pd.Timestamp.today() - pd.DateOffset(months=1)]["note"].mean()
    last_3_months_avg = data_notes_by_date[data_notes_by_date["date"] >= pd.Timestamp.today() - pd.DateOffset(months=3)]["note"].mean()

    # en utilisant st.metric pour afficher les indicateurs sur la même ligne
    left, right = st.columns(2, vertical_alignment="bottom")
    left.metric("Moyenne sur le dernier mois", round(last_month_avg, 2))
    right.metric("Moyenne sur les 3 derniers mois", round(last_3_months_avg, 2))


    # Affichage de l'évolution des notes moyennes en fonction du temps
    st.write("### Évolution des notes moyennes")
    fig = px.line(data_notes_by_date, x="date", y="note", markers=True, title="Évolution des notes moyennes au fil du temps")
    fig.update_layout(dragmode=False)  # Désactivation du zoom
    
    st.plotly_chart(fig)

st.write("© 2025 - Interface de suivi des notes")