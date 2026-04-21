import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="SSENSE Fashion Analysis", layout="wide")

# Titre
st.title("🖤 SSENSE Fashion Analysis")
st.markdown("Analyse des dynamiques de prix et de positionnement de la mode avant-garde — novembre 2023")

# Chargement des données
df = pd.read_csv("data/ssense_dataset.csv")

# Sidebar
st.sidebar.title("Filtres")
brands = st.sidebar.multiselect("Sélectionner des marques", 
                                 options=df['brand'].unique(),
                                 default=['Rick Owens', 'Gucci', 'Nike', 'Bottega Veneta', 'Marni'])
df_filtered = df[df['brand'].isin(brands)]

# Métriques
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de produits", f"{len(df_filtered):,}")
col2.metric("Prix moyen", f"${df_filtered['price_usd'].mean():.0f}")
col3.metric("Prix max", f"${df_filtered['price_usd'].max():,}")

st.divider()

# Graphique 1 — Top marques
st.subheader("Nombre de produits par marque")
fig1, ax1 = plt.subplots(figsize=(10,4))
top_brands = df_filtered['brand'].value_counts()
sns.barplot(x=top_brands.values, y=top_brands.index, palette='magma', ax=ax1)
ax1.set_xlabel("Nombre de produits")
st.pyplot(fig1)

st.divider()

# Graphique 2 — Prix moyen par marque
st.subheader("Prix moyen par marque")
fig2, ax2 = plt.subplots(figsize=(10,4))
prix_moyen = df_filtered.groupby('brand')['price_usd'].mean().sort_values(ascending=False)
sns.barplot(x=prix_moyen.values, y=prix_moyen.index, palette='magma', ax=ax2)
ax2.set_xlabel("Prix moyen (USD)")
st.pyplot(fig2)

st.divider()

# Graphique 3 — Distribution des prix
st.subheader("Distribution des prix")
bins = [0, 100, 300, 600, 1000, 10000]
labels = ['< $100', '$100-300', '$300-600', '$600-1000', '> $1000']
df_filtered['tranche_prix'] = pd.cut(df_filtered['price_usd'], bins=bins, labels=labels)
fig3, ax3 = plt.subplots(figsize=(10,4))
df_filtered['tranche_prix'].value_counts().sort_index().plot(kind='bar', color='black', ax=ax3)
ax3.set_xlabel("Tranche de prix")
ax3.set_ylabel("Nombre de produits")
plt.xticks(rotation=45)
st.pyplot(fig3)

st.divider()

# Conclusion
st.subheader("Conclusion")
st.markdown("""
Ce dataset de novembre 2023 donne un aperçu intéressant 
de la composition du catalogue SSENSE à un moment précis.

Rick Owens s'impose comme la marque au prix moyen le plus 
élevé avec $1843, ce qui reflète le positionnement historique 
de la maison. Bottega Veneta et Gucci suivent, confirmant 
la place centrale du luxe traditionnel sur la plateforme.

Ce qui retient l'attention, c'est la présence de Nike 
en deuxième position en volume. Cela illustre une tendance 
de fond dans le marché du luxe multi-marques : l'intégration 
du streetwear premium comme segment à part entière, 
porté par une clientèle plus jeune et des collaborations 
de plus en plus fréquentes entre les univers.
""")