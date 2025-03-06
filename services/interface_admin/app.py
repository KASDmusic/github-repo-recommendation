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

# Configuration de l'interface Streamlit
st.title("Suivi de l'évolution des notes moyennes")

# Récupération des données

if data.empty:
    st.write("Aucune donnée disponible.")
else:
    # Affichage du graphique avec Plotly Express
    st.write("### Évolution des notes moyennes")
    fig = px.line(data, x="date", y="avg_note", markers=True, title="Évolution des notes moyennes au fil du temps")
    fig.update_layout(dragmode=False)  # Désactivation du zoom
    
    st.plotly_chart(fig)

st.write("© 2024 - Interface de suivi des notes")