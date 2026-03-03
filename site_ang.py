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
VIDEOS = [
    {
        "url": "https://www.w3schools.com/html/mov_bbb.mp4", # Vidéo de test (lapin)
        "theme": "Vidéo d'animaux mignons",
        "skip_msg": "Zapping en {time}s. Déduction : N'aime pas la nature. Empathie faible. 🎯 Cible pour : Publicités pour des SUV très polluants.",
        "watch_msg": "Visionnage de {time}s. Déduction : Ennui profond, besoin de réconfort émotionnel. 🎯 Cible pour : Glaces en livraison et applications de rencontre."
    },
    {
        "url": "https://www.w3schools.com/html/mov_bbb.mp4", # Remplace par ta vidéo 2 (ex: Sport)
        "theme": "Influenceur Fitness (Musculation extrême)",
        "skip_msg": "Zapping en {time}s. Déduction : Flemme totale. 🎯 Cible pour : UberEats, promos sur les pizzas 4 fromages.",
        "watch_msg": "Visionnage de {time}s. Déduction : Complexe d'infériorité physique détecté. 🎯 Cible pour : Poudre protéinée hors de prix et pilules miracles."
    },
    {
        "url": "https://www.w3schools.com/html/mov_bbb.mp4", # Remplace par ta vidéo 3 (ex: Argent facile)
        "theme": "Gourou de la finance 'Deviens riche en 2 jours'",
        "skip_msg": "Zapping en {time}s. Déduction : Esprit critique encore fonctionnel. On va devoir contourner ses défenses.",
        "watch_msg": "Visionnage de {time}s. Déduction : Naïveté au maximum. Profil très rentable. 🎯 Cible pour : Arnaques aux cryptomonnaies et NFT de singes."
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