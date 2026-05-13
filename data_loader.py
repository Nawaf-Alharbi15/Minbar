from models import Lesson

def load_initial_lessons():
    return [
        Lesson(
            lesson_id="1", 
            title_ar="الفقه الميسر - الحلقة الأولى - العريفي", 
            title_en="Easy Fiqh - Episode 1 - Al-Arifi",
            topic_ar="الفقه", 
            topic_en="Fiqah",
            scholar_ar="العريفي", 
            scholar_en="Al-Arifi",
            youtube_url="https://www.youtube.com/watch?v=028eA_0mc3o", 
            level_ar="مبتدئ",
            level_en="Beginner"
        ),
        Lesson(
            lesson_id="2", 
            title_ar="أصول الإعتقاد الصحيح", 
            title_en="Principles of Correct Belief",
            topic_ar="العقيدة", 
            topic_en="Aqeedah",
            scholar_ar="وليد السعيدان", 
            scholar_en="Waleed Al-Saeedan",
            youtube_url="https://www.youtube.com/watch?v=eZyOapQP7XU&list=PLlX1sKIV4qu-B7OzL4dMbXP9M8_OH2psf", 
            level_ar="متوسط",
            level_en="Intermediate"
        ),
        Lesson(
            lesson_id="3", 
            title_ar="السيرة النبوية الحلقة 1 الشيخ نبيل العوضي", 
            title_en="Prophetic Biography Episode 1 - Nabil Al-Awadi",
            topic_ar="السيرة", 
            topic_en="Seerah",
            scholar_ar="نبيل العوضي", 
            scholar_en="Nabil Al-Awadi",
            youtube_url="https://youtu.be/f5QeWsfYyQo?si=IlUZ83sUVebIczwc", 
            level_ar="مبتدئ",
            level_en="Beginner"
        ),
        Lesson(
            lesson_id="4", 
            title_ar="دروس في العقيدة (1-26) شرح الشيخ عبد العزيز بن باز", 
            title_en="Lessons in Aqeedah (1-26) Explanation by Sheikh Ibn Baz",
            topic_ar="العقيدة", 
            topic_en="Aqeedah",
            scholar_ar="الشيخ عبد العزيز بن باز", 
            scholar_en="Sheikh Abdul Aziz bin Baz",
            youtube_url="https://youtu.be/3KkLKSa5CkE?si=MWohNB9SBerVVkVi", 
            level_ar="متوسط",
            level_en="Intermediate"
        ),
    ]