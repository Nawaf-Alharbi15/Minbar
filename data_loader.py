from Minbar.models import Lesson

def load_initial_lessons():
    return [
        Lesson("1", "الفقه الميسر - الحلقة الأولى - العريفي", "الفقه", "العريفي", "https://www.youtube.com/watch?v=028eA_0mc3o", "Beginner"),
        Lesson("2", "أصول الإعتقاد الصحيح", "العقيدة", "وليد السعيدان", "https://www.youtube.com/watch?v=eZyOapQP7XU&list=PLlX1sKIV4qu-B7OzL4dMbXP9M8_OH2psf", "Intermediate"),
        Lesson("3", "السيرة النبوية الحلقة 1 الشيخ نبيل العوضي", "السيرة", "نبيل العوضي", "https://youtu.be/f5QeWsfYyQo?si=IlUZ83sUVebIczwc", "Beginner"),
        Lesson("4", "دروس في العقيدة (1-26) شرح الشيخ عبد العزيز بن باز", "العقيدة", "الشيخ عبد العزيز بن باز", "https://youtu.be/3KkLKSa5CkE?si=MWohNB9SBerVVkVi", "Intermediate"),
    ]