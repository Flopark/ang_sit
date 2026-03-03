# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:26:58 2026

@author: march
"""

import streamlit as st
import time

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Projet TikTok - Léo & Florian", layout="wide")

# --- DONNÉES DE DÉMONSTRATION (À remplacer par tes vidéos) ---
# Format des URL Github : utilise le lien "Raw" du fichier mp4 (ex: https://raw.githubusercontent.com/...)
# --- DONNÉES DE L'ALGORITHME (Le "Trash Talk" de Florian) ---
VIDEOS = [
    {
        "url": "1.mp4", 
        "theme": "L'edit 'Sigma Male' ténébreux",
        "skip_msg": "Zapping en {time}s. Déduction : L'utilisateur a une vie sociale épanouie et ne se prend pas pour un loup solitaire incompris. ❌ Alerte : Inutile de lui vendre des formations de 'mâle alpha'.",
        "watch_msg": "Visionnage de {time}s. Déduction : Se prend pour le personnage principal de sa vie, mais passe ses samedis soirs en jogging dans sa chambre. 🎯 Cible : Abonnements hors de prix à des salles de sport où il n'ira jamais."
    },
    {
        "url": "2.mp4", 
        "theme": "La danse de chambre avec transition claquée",
        "skip_msg": "Zapping en {time}s. Déduction : L'utilisateur a encore un peu d'amour-propre et une intolérance au malaise. L'algorithme est déçu.",
        "watch_msg": "Visionnage de {time}s. Analyse oculaire : Tolérance au malaise anormalement élevée. Le cerveau est en mode veille totale. 🎯 Cible : Publicités pour des micros-cravates et des formations 'Devenir influenceur en 24h'."
    },
    {
        "url": "3.mp4", 
        "theme": "Le Deepfake IA absurde et malaisant (Humour noir)",
        "skip_msg": "Zapping de panique en {time}s. Déduction : Boussole morale intacte. L'utilisateur a été effrayé par cette abomination numérique. 🎯 Action : Injecter 3 vidéos de chatons mignons pour le rassurer.",
        "watch_msg": "Visionnage prolongé de {time}s. L'algorithme est formel : Humour noir détecté, sens moral potentiellement défaillant. L'utilisateur adore l'absurde. 🎯 Cible : T-shirts ironiques, mèmes obscurs et documentaires complotistes."
    },
    {
        "url": "4.mp4", 
        "theme": "Le Doomscrolling Géopolitique (WW3 Anime Opening)",
        "skip_msg": "Zapping d'évitement en {time}s. Déduction : Refuse de voir la réalité en face ou déteste les animes. 🎯 Cible : Filtre à bulles activé. On va lui vendre des séjours 'All-Inclusive' à Punta Cana pour le garder dans le déni.",
        "watch_msg": "Visionnage fasciné de {time}s. Pic de cortisol (stress) détecté. L'utilisateur romance l'apocalypse et souffre d'éco-anxiété. 🎯 Cible : Rations de survie goût bœuf bourguignon et purificateurs d'eau vendus 3 fois leur prix."
    }
]
# --- GESTION DE L'ÉTAT (Session State) ---
if 'index' not in st.session_state:
    st.session_state.index = 0
    st.session_state.start_time = time.time()
    st.session_state.logs = []
    st.session_state.game_over = False

def next_video(action):
    # Calcul du temps passé (simulé pour la démo si on clique vite)
    time_spent = round(time.time() - st.session_state.start_time, 1)
    
    # On force un peu le temps pour l'humour (si on clique "Regarder" ça met un temps long, "Zapper" un temps court)
    if action == "skip":
        display_time = max(0.5, time_spent) # Zapping rapide
        msg = VIDEOS[st.session_state.index]["skip_msg"].format(time=display_time)
    else:
        display_time = max(15.0, time_spent + 10) # Faux temps long
        msg = VIDEOS[st.session_state.index]["watch_msg"].format(time=display_time)

    # Ajouter au journal de l'algorithme
    st.session_state.logs.append(f"⏱️ **Vidéo {st.session_state.index + 1} ({VIDEOS[st.session_state.index]['theme']}) :** {msg}")
    
    # Passer à la vidéo suivante ou terminer
    if st.session_state.index < len(VIDEOS) - 1:
        st.session_state.index += 1
        st.session_state.start_time = time.time() # Reset chrono
    else:
        st.session_state.game_over = True

# --- INTERFACE UTILISATEUR ---
st.title("📱 Expérience TikTok : L'envers du décor")

if not st.session_state.game_over:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Ce que voit l'utilisateur (Léo) 🤩")
        st.markdown(f"**Vidéo {st.session_state.index + 1} / {len(VIDEOS)}**")
        
        # Affichage de la vidéo
        st.video(VIDEOS[st.session_state.index]["url"])
        
        # Boutons de simulation
        c1, c2 = st.columns(2)
        with c1:
            st.button("⏭️ Zapper vite (Moins de 2s)", on_click=next_video, args=("skip",), use_container_width=True)
        with c2:
            st.button("👀 Regarder en entier", type="primary", on_click=next_video, args=("watch",), use_container_width=True)

    with col2:
        st.subheader("Ce que voit l'Algorithme (Florian) 🕵️‍♂️")
        st.markdown("---")
        if not st.session_state.logs:
            st.info("En attente des premières données... L'algorithme observe.")
        else:
            for log in reversed(st.session_state.logs):
                st.warning(log)
else:
    # --- LE TICKET DE CAISSE FINAL ---
    st.balloons()
    st.error("🚨 FIN DE LA COLLECTE DE DONNÉES 🚨")
    st.subheader("🧾 Votre Ticket de Caisse Numérique :")
    
    for log in st.session_state.logs:
        st.write(log)
    
    st.markdown("---")
    st.markdown("""
    **Bilan Psychologique Synthétique :**
    * 🧠 **Niveau de manipulation possible :** 98%
    * 💸 **Valeur marchande de vos données :** 0,42 centimes. (Oui, vous valez moins d'un euro).
    * 🎯 **Recommandation algorithmique :** Enfermer l'utilisateur dans une boucle de vidéos de chats pour le rendre docile.
    """)
    
    if st.button("Recommencer l'expérience"):
        st.session_state.index = 0
        st.session_state.logs = []
        st.session_state.game_over = False
        st.session_state.start_time = time.time()
        st.rerun()

# Cacher le menu Streamlit par défaut pour faire plus "pro"
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_streamlit_style, unsafe_allow_html=True)
