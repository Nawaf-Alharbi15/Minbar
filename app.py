import streamlit as st
st.set_page_config(layout="wide", page_title="Religious Lessons", page_icon="📚")

import urllib.parse as urlparse
from models import LessonManager, User
from data_loader import load_initial_lessons

def get_youtube_id(url):
    url_data = urlparse.urlparse(url)
    if url_data.netloc in ('youtu.be', 'www.youtu.be'):
        return url_data.path[1:]
    query = urlparse.parse_qs(url_data.query)
    if 'v' in query:
        return query['v'][0]
    return None

# 1. Setup Data (The Data Lead's job)
# Creating sample lessons to satisfy the "browse lessons" requirement [cite: 7]
all_lessons = load_initial_lessons()
manager = LessonManager(all_lessons)

# Initialize user and favorites in session state
if 'user' not in st.session_state:
    st.session_state.user = User(username="Guest")
user = st.session_state.user

if 'language' not in st.session_state:
    st.session_state.language = "ar"

if "lesson_id" in st.query_params:
    st.session_state.selected_lesson_id = st.query_params["lesson_id"]

translations = {
    "ar": {
        "nav": "التنقل",
        "home": "🏠 الرئيسية",
        "fav": "🔖 المفضلة",
        "fav_help": "عرض الدروس المفضلة",
        "search_filter": "البحث والتصفية",
        "topic": "التصنيف",
        "topics": ["الكل", "الفقه", "العقيدة", "السيرة"],
        "scholar_name": "اسم الشيخ",
        "search_placeholder": "ابحث بالعنوان، الشيخ، أو التصنيف",
        "scholar_lbl": "الشيخ:",
        "topic_lbl": "التصنيف:",
        "level_lbl": "المستوى:",
        "add_fav": "أضف للمفضلة",
        "fav_success": "تمت الإضافة للمفضلة!",
        "in_fav": "في المفضلة",
        "back": "العودة للدروس",
        "switch_lang": "🌍 English",
        "switch_help": "Switch to English"
    },
    "en": {
        "nav": "Navigation",
        "home": "🏠 Home",
        "fav": "🔖 Favorites",
        "fav_help": "Show favorite lessons",
        "search_filter": "Search and Filter",
        "topic": "Topic",
        "topics": ["All", "Fiqah", "Aqeedah", "Seerah"],
        "scholar_name": "Scholar Name",
        "search_placeholder": "Search by Title, Scholar, or Topic",
        "scholar_lbl": "Scholar:",
        "topic_lbl": "Topic:",
        "level_lbl": "Level:",
        "add_fav": "Add to Favorites",
        "fav_success": "Added to favorites!",
        "in_fav": "In Favorites",
        "back": "Back to Lessons",
        "switch_lang": "🌍 العربية",
        "switch_help": "التبديل للعربية"
    }
}
lang = st.session_state.language
t = translations[lang]

if lang == "ar":
    st.markdown("""
        <style>
        .stApp {
            direction: rtl;
        }
        p, div, span, h1, h2, h3, h4, h5, h6, label, input, button {
            text-align: right;
        }
        </style>
    """, unsafe_allow_html=True)

# --- Sidebar Callbacks ---
def reset_filters():
    st.session_state.show_favorites = False
    st.session_state.topic_choice = translations[st.session_state.language]["topics"][0]
    st.session_state.scholar_search = ""
    st.session_state.search_bar = ""
    st.session_state.selected_lesson_id = None
    if "lesson_id" in st.query_params:
        del st.query_params["lesson_id"]

def clear_lesson():
    st.session_state.selected_lesson_id = None
    if "lesson_id" in st.query_params:
        del st.query_params["lesson_id"]

def toggle_language():
    old_lang = st.session_state.language
    new_lang = "en" if old_lang == "ar" else "ar"
    
    # Safely map topic choice index to prevent selectbox errors
    if 'topic_choice' in st.session_state and st.session_state.topic_choice in translations[old_lang]["topics"]:
        old_idx = translations[old_lang]["topics"].index(st.session_state.topic_choice)
        st.session_state.topic_choice = translations[new_lang]["topics"][old_idx]
        
    st.session_state.language = new_lang

with st.sidebar:
    st.markdown(f"## {t['nav']}")
    st.button(t['home'], key="home", help=t['home'], on_click=reset_filters)
    fav_clicked = st.button(t['fav'], key="fav", help=t['fav_help'])
    st.button(t['switch_lang'], key="lang_toggle", help=t['switch_help'], on_click=toggle_language)
    st.markdown("---")
    st.header(t['search_filter'])
    if 'topic_choice' not in st.session_state:
        st.session_state.topic_choice = t["topics"][0]
    if 'scholar_search' not in st.session_state:
        st.session_state.scholar_search = ""
    topic_choice = st.selectbox(t['topic'], t['topics'], key="topic_choice")
    scholar_search = st.text_input(t['scholar_name'], key="scholar_search")



# --- Main Area ---
st.markdown("""
    <style>
    .search-bar input {
        width: 100%;
        padding: 0.75em;
        font-size: 1.1em;
        border-radius: 10px;
        border: 1px solid #444;
        background: #222;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

search_query = st.text_input("", "", key="search_bar", placeholder=t['search_placeholder'], label_visibility="collapsed")


# --- Filtering Logic ---
if 'show_favorites' not in st.session_state:
    st.session_state.show_favorites = False


if fav_clicked:
    st.session_state.show_favorites = True

if st.session_state.show_favorites:
    filtered_lessons = user.favorites
else:
    if topic_choice == t["topics"][0]:
        filtered_lessons = all_lessons
    else:
        filtered_lessons = manager.filter_by_topic(topic_choice)
    if scholar_search:
        filtered_lessons = [lesson for lesson in filtered_lessons if scholar_search.lower() in lesson.get_attr('scholar', lang).lower()]
    if search_query:
        filtered_lessons = [lesson for lesson in filtered_lessons if search_query.lower() in lesson.get_attr('title', lang).lower() or search_query.lower() in lesson.get_attr('scholar', lang).lower() or search_query.lower() in lesson.get_attr('topic', lang).lower()]


# --- Display Results in Grid ---

# --- Lesson Card and Detail View ---
def lesson_card(lesson):
    video_id = get_youtube_id(lesson.youtube_url)
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else "https://via.placeholder.com/480x360.png?text=No+Thumbnail"
    
    with st.container():
        st.markdown(
            f"""
            <a href="/?lesson_id={lesson.lesson_id}" target="_self" style="text-decoration: none; color: inherit;">
                <div style='border:2px solid #444; border-radius:16px; margin-bottom:18px; background:#18191A; cursor: pointer; overflow:hidden; display: flex; flex-direction: column; min-height: 360px;'>
                    <img src="{thumbnail_url}" style="width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; border-bottom: 2px solid #444;">
                    <div style="padding: 18px; flex-grow: 1; display: flex; flex-direction: column;">
                        <h4 style='margin-bottom:0.5em; margin-top:0;'>{lesson.get_attr('title', lang)}</h4>
                        <div style="margin-top: auto; font-size: 0.95em; color: #ccc;">
                            <b>{t['scholar_lbl']}</b> {lesson.get_attr('scholar', lang)}<br>
                            <b>{t['topic_lbl']}</b> {lesson.get_attr('topic', lang)} | <b>{t['level_lbl']}</b> {lesson.get_attr('level', lang)}
                        </div>
                    </div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

def lesson_detail(lesson):
    st.markdown(f"# {lesson.get_attr('title', lang)}")
    st.write(f"**{t['scholar_lbl']}** {lesson.get_attr('scholar', lang)}")
    st.write(f"**{t['topic_lbl']}** {lesson.get_attr('topic', lang)}")
    st.video(lesson.youtube_url)
    if lesson not in user.favorites:
        if st.button(t['add_fav'], key=f"fav_detail_{lesson.lesson_id}"):
            user.add_favorite(lesson)
            st.success(t['fav_success'])
    else:
        st.info(t['in_fav'])
    st.button(t['back'], key="back_to_lessons", on_click=clear_lesson)

# --- Main Display Logic ---
if 'selected_lesson_id' not in st.session_state:
    st.session_state.selected_lesson_id = None

selected_lesson = None
if st.session_state.selected_lesson_id:
    for lesson in all_lessons:
        if lesson.lesson_id == st.session_state.selected_lesson_id:
            selected_lesson = lesson
            break

if selected_lesson:
    lesson_detail(selected_lesson)
else:
    cols = st.columns(3)
    for idx, lesson in enumerate(filtered_lessons):
        video_id = get_youtube_id(lesson.youtube_url)
        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg" if video_id else "https://via.placeholder.com/480x360.png?text=No+Thumbnail"
        
        with cols[idx % 3]:
            st.markdown(
                f"""
                <a href="/?lesson_id={lesson.lesson_id}" target="_self" style="text-decoration: none; color: inherit;">
                    <div style='border:2px solid #444; border-radius:16px; margin-bottom:18px; background:#18191A; cursor: pointer; overflow:hidden; display: flex; flex-direction: column; min-height: 360px;'>
                        <img src="{thumbnail_url}" style="width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; border-bottom: 2px solid #444;">
                        <div style="padding: 18px; flex-grow: 1; display: flex; flex-direction: column;">
                            <h4 style='margin-bottom:0.5em; margin-top:0;'>{lesson.get_attr('title', lang)}</h4>
                            <div style="margin-top: auto; font-size: 0.95em; color: #ccc;">
                                <b>{t['scholar_lbl']}</b> {lesson.get_attr('scholar', lang)}<br>
                                <b>{t['topic_lbl']}</b> {lesson.get_attr('topic', lang)} | <b>{t['level_lbl']}</b> {lesson.get_attr('level', lang)}
                            </div>
                        </div>
                    </div>
                </a>
                """,
                unsafe_allow_html=True
            )