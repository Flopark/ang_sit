# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:26:58 2026

@author: march
"""
import streamlit as st
import base64
import os
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Présentation TikTok", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MAGIQUE ---
st.markdown("""
<style>
/* Cacher le menu et le header de Streamlit */
[data-testid="stHeader"] {display: none;}
footer {visibility: hidden;}

/* Rendre les zones de clics SECRÈTES invisibles au public */
div.stButton > button {
    opacity: 0.01; /* Quasiment invisible */
    height: 100px; /* Grande zone de clic */
    width: 100%;
    border: none !important;
    box-shadow: none !important;
}
div.stButton > button:hover {
    opacity: 0.1; /* Léger reflet rouge au survol pour Florian */
    background-color: red !important; 
}

/* Style de la console de Florian */
.terminal-log {
    background-color: #1e1e1e;
    color: #00ff00;
    font-family: 'Courier New', Courier, monospace;
    padding: 15px;
    border-radius: 5px;
    margin-bottom: 10px;
    border-left: 5px solid red;
}
</style>
""", unsafe_allow_html=True)

# --- DONNÉES DES VIDÉOS (Les 11 scénarios) ---
VIDEOS = [
    {
        "file": "1.mp4", "user": "sigma_mindset", "desc": "Real ones know... 🐺🔥 #sigma",
        "skip_msg": "Zapping ultra-rapide.\nDéduction : Vie sociale épanouie.\n❌ Alerte : Inutile de lui vendre des formations de 'mâle alpha'.",
        "watch_msg": "Visionnage complet.\nDéduction : Se prend pour le perso principal. Reste en jogging dans sa chambre.\n🎯 Cible : Abonnements à des salles de sport."
    },
    {
        "file": "2.mp4", "user": "leo_dance_off", "desc": "Transition de fou ! 👔🕺 #dance",
        "skip_msg": "Zapping immédiat.\nDéduction : Amour-propre intact. Intolérance au malaise. L'algorithme est déçu.",
        "watch_msg": "Visionnage complet.\nDéduction : Tolérance au malaise anormale. Cerveau en veille.\n🎯 Cible : Formations 'Devenir influenceur en 24h'."
    },
    {
        "file": "4.mp4", "user": "geopolitics_hub", "desc": "Season finale looks crazy 😭🌍 #ww3",
        "skip_msg": "Zapping d'évitement.\nDéduction : Refuse de voir la réalité en face.\n🎯 Cible : Séjours 'All-Inclusive' à Punta Cana.",
        "watch_msg": "Visionnage fasciné.\nDéduction : Pic de cortisol. Romance l'apocalypse.\n🎯 Cible : Rations de survie goût bœuf bourguignon."
    },
    {
        "file": "5.mp4", "user": "vanity_queen", "desc": "Just feeling the vibe 💅🔥 #lipsync",
        "skip_msg": "Zapping immédiat.\nDéduction : Estime de soi normale. Insensible aux duckfaces.\n❌ Cible : Impossible de lui vendre du maquillage.",
        "watch_msg": "Visionnage complet.\nDéduction : L'utilisateur est très superficiel ou complexe sur son physique.\n🎯 Cible : Filtres payants et crèmes 'miracles'."
    },
    {
        "file": "3.mp4", "user": "dark_humor_ai", "desc": "Bro dropped the hardest cover 💀 #ai",
        "skip_msg": "Zapping de panique.\nDéduction : Boussole morale intacte.\n🎯 Action : Injecter 3 vidéos de chatons pour le rassurer.",
        "watch_msg": "Visionnage prolongé.\nDéduction : Humour noir détecté, sens moral défaillant.\n🎯 Cible : T-shirts ironiques et docs complotistes."
    },
    {
        "file": "6.mp4", "user": "block_master_fr", "desc": "POV : Tu trouves un village Minecraft IRL 🥕 #gaming",
        "skip_msg": "Zapping de gêne.\nDéduction : Plus de 12 ans d'âge mental. Allergique au malaise IRL.",
        "watch_msg": "Visionnage fasciné.\nDéduction : Syndrome de Peter Pan. Vit probablement encore chez ses parents.\n🎯 Cible : Boissons énergisantes et chaises gaming."
    },
    {
        "file": "7.mp4", "user": "world_alert_news", "desc": "Shocking footage from Bahrain 💥🏢 #news",
        "skip_msg": "Zapping de préservation.\nDéduction : Cherche du divertissement, refuse l'anxiété du monde réel.",
        "watch_msg": "Visionnage en boucle.\nDéduction : Pic de dopamine morbide. Aime le Doomscrolling.\n🎯 Cible : Médias anxiogènes et pubs pour antidépresseurs."
    },
    {
        "file": "8.mp4", "user": "tk_prime_officiel", "desc": "Quand t'en as gros sur la patate 🤬🚗 #coupdegueule",
        "skip_msg": "Zapping pacifiste.\nDéduction : Santé mentale équilibrée. Ne cherche pas le conflit virtuel.",
        "watch_msg": "Visionnage complet.\nDéduction : Rythme cardiaque synchronisé avec les cris. Adore le drama.\n🎯 Cible : Contenus de dashcams (accidents)."
    },
    {
        "file": "9.mp4", "user": "meme_craft_daily", "desc": "We all have that one friend 🥔💻 #pcgamer",
        "skip_msg": "Zapping.\nDéduction : N'a pas la référence. A probablement une vie sociale à l'extérieur.",
        "watch_msg": "Sourire détecté.\nDéduction : Gamer avec un PC éclaté au sol. Complexe d'infériorité matériel.\n🎯 Cible : Crédits conso pour acheter des cartes graphiques."
    },
    {
        "file": "10.mp4", "user": "hoops_hype", "desc": "Bro was too hyped 💀🏀 #basketball",
        "skip_msg": "Zapping.\nDéduction : Intolérance absolue au bruit et aux enfants qui crient.",
        "watch_msg": "Visionnage de la gêne.\nDéduction : Adore se moquer du ridicule des autres en public.\n🎯 Cible : Compilations de chutes humiliantes."
    },
    {
        "file": "11.mp4", "user": "techno_bunker_666", "desc": "Ce RRT'S dans 30 ans 🔊🕺 #hardstyle",
        "skip_msg": "Zapping de survie.\nDéduction : Tympans intacts. Préserve sa santé auditive.",
        "watch_msg": "Visionnage prolongé.\nDéduction : Cerveau grillé par les basses ou acouphènes sévères.\n🎯 Cible : Bouchons d'oreilles et billets de festival."
    }
]

# --- FONCTION DE FORMATAGE TIKTOK ---
def format_stat(num):
    """Formate les nombres façon TikTok (ex: 1.2M, 45.3k)"""
    if num >= 1000000:
        return f"{num/1000000:.1f}M".replace('.0M', 'M')
    elif num >= 1000:
        return f"{num/1000:.1f}k".replace('.0k', 'k')
    return str(num)

# --- GESTION DE L'ÉTAT POUR L'ALGORITHME ---
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.logs = []

def trigger_algo(action):
    # On vérifie qu'on ne dépasse pas le nombre de vidéos physiquement présentes
    videos_presentes = [v for v in VIDEOS if os.path.exists(v["file"])]
    if st.session_state.step < len(videos_presentes):
        video = videos_presentes[st.session_state.step]
        msg = video["skip_msg"] if action == "skip" else video["watch_msg"]
        st.session_state.logs.insert(0, f"**Vidéo {st.session_state.step + 1} (@{video['user']})**<br>{msg}")
        st.session_state.step += 1

# --- GÉNÉRATION DU SCROLL INFINI HTML/JS ---
def render_tiktok_feed():
    feed_html = """
    <div style="width: 360px; height: 650px; background: #000; border-radius: 20px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.8); overflow-y: scroll; scroll-snap-type: y mandatory; position: relative;" id="tiktok-feed">
    """
    
    # On ne garde que les vidéos qui existent vraiment dans le dossier
    videos_presentes = [v for v in VIDEOS if os.path.exists(v["file"])]
    
    if not videos_presentes:
        return "<div style='color:white; padding: 20px;'>Aucune vidéo trouvée. Placez vos fichiers .mp4 (ex: 1.mp4) dans le dossier.</div>"

    for vid in videos_presentes:
        with open(vid["file"], "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            
        # STATISTIQUES ALÉATOIRES
        likes = format_stat(random.randint(10000, 3500000))
        comments = format_stat(random.randint(100, 80000))
        saves = format_stat(random.randint(500, 150000))
        shares = format_stat(random.randint(50, 50000))
            
        feed_html += f"""
        <div style="height: 100%; width: 100%; scroll-snap-align: start; position: relative;">
            <video loop playsinline style="width: 100%; height: 100%; object-fit: cover;">
                <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            </video>
            
            <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 40%; background: linear-gradient(to top, rgba(0,0,0,0.8), transparent); pointer-events: none;"></div>
            
            <div style="position: absolute; right: 15px; bottom: 80px; display: flex; flex-direction: column; align-items: center; gap: 20px; z-index: 10;">
                <div style="width: 45px; height: 45px; background: #fff; border-radius: 50%; overflow: hidden; border: 2px solid white;">
                    <img src="https://api.dicebear.com/7.x/avataaars/svg?seed={vid['user']}" width="100%">
                </div>
                
                <div style="text-align: center; color: white; font-family: sans-serif; cursor: pointer;" onclick="toggleLike(this)">
                    <div class="heart-icon" style="font-size: 35px; transition: transform 0.2s ease, text-shadow 0.2s ease; text-shadow: 0px 0px 2px rgba(0,0,0,0.5);">🤍</div>
                    <div class="like-count" style="font-size: 12px; font-weight: bold; margin-top: -5px;">{likes}</div>
                </div>
                
                <div style="text-align: center; color: white; font-family: sans-serif;">
                    <div style="font-size: 30px; text-shadow: 0px 0px 2px rgba(0,0,0,0.5);">💬</div>
                    <div style="font-size: 12px; font-weight: bold;">{comments}</div>
                </div>
                <div style="text-align: center; color: white; font-family: sans-serif;">
                    <div style="font-size: 30px; text-shadow: 0px 0px 2px rgba(0,0,0,0.5);">🔖</div>
                    <div style="font-size: 12px; font-weight: bold;">{saves}</div>
                </div>
                <div style="text-align: center; color: white; font-family: sans-serif;">
                    <div style="font-size: 30px; text-shadow: 0px 0px 2px rgba(0,0,0,0.5);">↪️</div>
                    <div style="font-size: 12px; font-weight: bold;">{shares}</div>
                </div>
            </div>

            <div style="position: absolute; left: 15px; bottom: 20px; color: white; font-family: sans-serif; padding-right: 70px; z-index: 10;">
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 5px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">@{vid['user']}</div>
                <div style="font-size: 14px; margin-bottom: 10px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">{vid['desc']}</div>
                <div style="font-size: 12px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">🎵 Son original - {vid['user']}</div>
            </div>
        </div>
        """
        
    feed_html += """
    </div>
    <style>
        /* Cacher la barre de scroll disgracieuse */
        #tiktok-feed::-webkit-scrollbar { display: none; }
        #tiktok-feed { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
    <script>
        // Gestion de la lecture automatique au scroll
        const videos = document.querySelectorAll('video');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.play();
                } else {
                    entry.target.pause();
                }
            });
        }, { threshold: 0.6 });
        videos.forEach(v => observer.observe(v));

        // Fonction pour animer le bouton J'aime
        function toggleLike(element) {
            const heart = element.querySelector('.heart-icon');
            if (heart.innerText === '🤍') {
                heart.innerText = '❤️';
                heart.style.transform = 'scale(1.3)'; // Petit rebond
                setTimeout(() => {
                    heart.style.transform = 'scale(1)';
                }, 200);
            } else {
                heart.innerText = '🤍';
            }
        }
    </script>
    """
    return feed_html

# --- AFFICHAGE SUR SCÈNE ---
col_tiktok, col_algo = st.columns([1, 1.2])

videos_presentes = [v for v in VIDEOS if os.path.exists(v["file"])]

with col_tiktok:
    st.components.v1.html(render_tiktok_feed(), height=680)

with col_algo:
    st.markdown("## 🕵️‍♂️ L'Oeil de l'Algorithme")
    st.markdown("*En attente des actions de l'utilisateur (Scroll / Temps de visionnage)...*")
    st.markdown("---")
    
    # Boutons invisibles de Florian
    if st.session_state.step < len(videos_presentes):
        sec_col1, sec_col2 = st.columns(2)
        with sec_col1:
            st.button("Zapper", key=f"skip_{st.session_state.step}", on_click=trigger_algo, args=("skip",))
            st.caption("👈 Clic secret (Zapper - Vidéo " + str(st.session_state.step + 1) + ")")
        with sec_col2:
            st.button("Regarder", key=f"watch_{st.session_state.step}", on_click=trigger_algo, args=("watch",))
            st.caption("👈 Clic secret (Regarder - Vidéo " + str(st.session_state.step + 1) + ")")
    else:
        st.error("🚨 PLUS DE VIDÉOS. L'utilisateur est profilé à 100%. Prêt pour la vente des données.")
        if st.button("🔄 Recommencer l'expérience", type="primary"):
            st.session_state.step = 0
            st.session_state.logs = []
            st.rerun()

    # Affichage du journal d'analyse
    for log in st.session_state.logs:
        st.markdown(f"<div class='terminal-log'>{log}</div>", unsafe_allow_html=True)


