import streamlit as st
import pandas as pd
import altair as alt

# Configuration de la page
st.set_page_config(
    page_title="نتائج الدراسة العملية الوطنية للشارة الخشبية - تيبازة 2024",
    page_icon="images/logop.png",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_excel('data/resultats.xlsx')
    df = df.iloc[2:].reset_index(drop=True)
    df.columns = ['id', 'ordre', 'nom_prenom', 'groupe', 'commune', 'wilaya', 'point_finale', 'observation']
    df = df[['id', 'ordre', 'nom_prenom', 'groupe', 'commune', 'wilaya', 'point_finale', 'observation']]
    return df

data = load_data()

# Fonction de recherche
def rechercher_id(df, id_recherche):
    resultat = df[df['id'] == id_recherche]
    colonnes_arabe = {
        'id': 'id رقم',
        'ordre': 'الترتيب',
        'nom_prenom': 'الاسم واللقب',
        'groupe': 'المجموعة',
        'commune': 'البلدية',
        'wilaya': 'الولاية',
        'point_finale': 'النقطة النهائية',
        'observation': 'الملاحظة'
    }
    resultat = resultat.rename(columns=colonnes_arabe)
    resultat = resultat.reindex(columns=resultat.columns[::-1])
    return resultat

# CSS
st.markdown(""" 
<style>
    body {
        direction: rtl;
        font-family: 'Arial', sans-serif;
        background-image: url('images/logo.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    [data-testid="block-container"] {
        padding: 2rem 2rem 0rem 2rem;
        margin-bottom: -7rem;
    }
    [data-testid="stVerticalBlock"] {
        padding: 0rem;
    }
    [data-testid="stMetric"] {
        background-color: #393939;
        text-align: center;
        padding: 15px 0;
    }
    [data-testid="stMetricLabel"] {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    [data-testid="stMetricDeltaIcon-Up"] {
        position: relative;
        left: 38%;
        transform: translateX(-50%);
    }
    [data-testid="stMetricDeltaIcon-Down"] {
        position: relative;
        left: 38%;
        transform: translateX(-50%);
    }
    .highlight {
        color: #10344b;
        font-weight: bold;
    }
    @media (max-width: 768px) {
        .title-text {
            font-size: 20px;
        }
        .highlight {
            font-size: 18px;
        }
        [data-testid="stMetricLabel"] {
            flex-direction: column;
        }
        
        .block-container {
            padding: 1rem;
        }
        .stImage {
            width: 100%;
        }
    }
    .stDataFrame {
        margin: 0 auto;
        width: 80%; /* Ajuster la largeur du tableau pour qu'il soit plus lisible */
    }
    .stExpander {
        margin: 0 auto;
        max-width: 800px;
    }
    .highlight {
        color: #10344b;
        font-weight: bold;
    }
    .stExpander > label {
        display: none;
    }
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        width: 100%;
    }
    .title-text {
        font-family: 'Arial', sans-serif;
        text-align: center;
        font-size: 24px;
    }
    .stTextInput input {
        background-color: white !important;  /* Fond blanc */
        color: black !important;  /* Texte noir */
        font-size: 16px;
        padding: 10px;
    }
    .stButton > button {
        width: 100%;  /* Bouton largeur 100% */
        text-align: center;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Titre avec icône
st.markdown(
    """
    <div style="text-align: center;">
        <h3 class='title-text' style="margin-top: 20px;">
            📊 نتائج الدراسة العملية الوطنية للشارة الخشبية<br> تيبازة 2024<br>
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Déplacer la ligne rouge vers le haut avec une marge négative
st.markdown("<hr style='border: 1px solid red; margin-top: -10px;'>", unsafe_allow_html=True)

# Main Panel
st.markdown('### :mag_right: لوحة البحث', unsafe_allow_html=True)

# Entrée ID
st.markdown(
    '''
    <div style="text-align: center;">
        <span class="highlight">أدخل🔑 id رقم:</span>
    </div>
    ''',
    unsafe_allow_html=True
)
id_input = st.text_input("", key="search_input")  # Champ de texte vide (le titre est déjà affiché)

# Utiliser st.columns pour centrer le bouton
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Bouton pour rechercher
    if st.button('بحث', key="search_button", help="إضغط هنا للبحث"):
        recherche_effectuee = True  # Définir la variable de recherche
    else:
        recherche_effectuee = False  # Réinitialiser la variable si le bouton n'est pas cliqué

# Affichage des résultats
 
if recherche_effectuee:
    if id_input.isdigit():  # Vérifier si l'entrée est un nombre
        id_recherche = int(id_input)
        resultat = rechercher_id(data, id_recherche)
        
        # Remplacer les valeurs manquantes (None ou NaN) par '...plus'
        resultat = resultat.fillna('...plus')
        
        if not resultat.empty:
            # Centrer le tableau
            st.markdown('<div class="centered-container">', unsafe_allow_html=True)
            st.dataframe(resultat, use_container_width=True)  # Utiliser st.dataframe pour un meilleur contrôle
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning(f"لم يتم العثور على نتائج لـ {id_input} id رقم المدخل.")
    else:
        st.error("يرجى إدخال معرف صالح (رقمي).")


# À propos de l'application
st.markdown('<div class="centered-container">', unsafe_allow_html=True)

# Titre personnalisé avec icône
st.markdown(
    '''
    <div style="text-align: center;">
        <span class="highlight">ℹ️ حول التطبيق</span>
    </div>
    ''',
    unsafe_allow_html=True
)

# Expander sans titre natif (masqué via CSS)
with st.expander("", expanded=True):  # Titre vide
    st.markdown(''' 
    <div style="text-align: center;">
        هذا تطبيق لعرض النتائج تم تطويره بواسطة <span class="highlight">هيئة تأطير الدّراسة العمليّة الوطنية للشارة الخشبية - تيبازة 2024</span>.
    </div>
    ''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Affichage de l'image centrée
st.markdown('<div class="centered-container">', unsafe_allow_html=True)
st.image('images/logo.png', use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
