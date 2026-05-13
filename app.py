import streamlit as st
from Minbar.models import LessonManager, User
from Minbar.data_loader import load_initial_lessons

# 1. Setup Data (The Data Lead's job)
# Creating sample lessons to satisfy the "browse lessons" requirement [cite: 7]
all_lessons = load_initial_lessons()
manager = LessonManager(all_lessons)

# Initialize user and favorites in session state
if 'user' not in st.session_state:
    st.session_state.user = User(username="Guest")
user = st.session_state.user


# --- Sidebar ---


# --- Sidebar Callbacks ---
def reset_filters():
    st.session_state.show_favorites = False
    st.session_state.topic_choice = "الكل"
    st.session_state.scholar_search = ""
    st.session_state.search_bar = ""

with st.sidebar:
    st.markdown("## Navigation")
    st.button("🏠", key="home", help="Home", on_click=reset_filters)
    fav_clicked = st.button("🔖 المفضلة", key="المفضلة", help="عرض الدروس المفضلة")
    st.markdown("---")
    st.header("البحث والتصفية")
    if 'topic_choice' not in st.session_state:
        st.session_state.topic_choice = "الكل"
    if 'scholar_search' not in st.session_state:
        st.session_state.scholar_search = ""
    topic_choice = st.selectbox("التصنيف", ["الكل", "الفقه", "العقيدة", "السيرة"], key="topic_choice")
    scholar_search = st.text_input("اسم الشيخ", key="scholar_search")



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

search_query = st.text_input("", "", key="search_bar", placeholder="Search Bar", label_visibility="collapsed")


# --- Filtering Logic ---
if 'show_favorites' not in st.session_state:
    st.session_state.show_favorites = False


if fav_clicked:
    st.session_state.show_favorites = True

if st.session_state.show_favorites:
    filtered_lessons = user.favorites
else:
    if topic_choice == "الكل":
        filtered_lessons = all_lessons
    else:
        filtered_lessons = manager.filter_by_topic(topic_choice)
    if scholar_search:
        filtered_lessons = [lesson for lesson in filtered_lessons if lesson.scholar.lower() == scholar_search.lower()]
    if search_query:
        filtered_lessons = [lesson for lesson in filtered_lessons if search_query.lower() in lesson.title.lower()]


# --- Display Results in Grid ---

# --- Lesson Card and Detail View ---
def lesson_card(lesson):
    with st.container():
        st.markdown(
            f"""
            <div style='border:2px solid #444; border-radius:16px; padding:18px; margin-bottom:18px; background:#18191A;'>
                <h4 style='margin-bottom:0.5em'>{lesson.title}</h4>
                <b>Scholar:</b> {lesson.scholar}<br>
                <b>Topic:</b> {lesson.topic} | <b>Level:</b> {lesson.level}<br><br>
                <form action="" method="post">
                    <button name="view_{lesson.lesson_id}" type="submit" style='padding:8px 18px; border-radius:8px; background:#222; color:#fff; border:none;'>View Details</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.session_state.get(f"view_{lesson.lesson_id}"):
            st.session_state.selected_lesson_id = lesson.lesson_id

def lesson_detail(lesson):
    st.markdown(f"# {lesson.title}")
    st.write(f"**Scholar:** {lesson.scholar}")
    st.write(f"**Topic:** {lesson.topic}")
    st.video(lesson.youtube_url)
    if lesson not in user.favorites:
        if st.button("Add to Favorites", key=f"fav_detail_{lesson.lesson_id}"):
            user.add_favorite(lesson)
            st.success("Added to favorites!")
    else:
        st.info("In Favorites")
    if st.button("Back to Lessons", key="back_to_lessons"):
        st.session_state.selected_lesson_id = None

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
        with cols[idx % 3]:
            if st.button("View Details", key=f"view_{lesson.lesson_id}"):
                st.session_state.selected_lesson_id = lesson.lesson_id
            st.markdown(
                f"""
                <div style='border:2px solid #444; border-radius:16px; padding:18px; margin-bottom:18px; background:#18191A;'>
                    <h4 style='margin-bottom:0.5em'>{lesson.title}</h4>
                    <b>Scholar:</b> {lesson.scholar}<br>
                    <b>Topic:</b> {lesson.topic} | <b>Level:</b> {lesson.level}<br>
                </div>
                """,
                unsafe_allow_html=True
            )