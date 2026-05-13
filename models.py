"""
models.py

Core data models for the Religious Lessons Platform MVP.
"""

from typing import List, Dict

class Lesson:
    """
    Represents a single religious lesson or lecture.
    """
    def __init__(self, lesson_id: str, title: str, topic: str, scholar: str, youtube_url: str, level: str):
        """
        Initialize a Lesson instance.
        Args:
            lesson_id (str): Unique identifier for the lesson.
            title (str): The title of the lesson.
            topic (str): The category (e.g., Fiqh, Aqeedah, Seerah).
            scholar (str): The name of the trusted source/speaker.
            youtube_url (str): The link to the embedded video.
            level (str): Learning level ('Beginner' or 'Intermediate').
        """
        self.lesson_id = lesson_id
        self.title = title
        self.topic = topic
        self.scholar = scholar
        self.youtube_url = youtube_url
        self.level = level

    def get_info(self) -> Dict[str, str]:
        """
        Returns a summary of all lesson attributes as a dictionary.
        """
        return {
            'lesson_id': self.lesson_id,
            'title': self.title,
            'topic': self.topic,
            'scholar': self.scholar,
            'youtube_url': self.youtube_url,
            'level': self.level
        }

    def render_video(self) -> None:
        """
        Logic to display the YouTube player in the UI (to be implemented in Streamlit app).
        """
        pass  # UI logic handled in Streamlit app


class User:
    """
    Manages the profile and preferences of the learner.
    """
    def __init__(self, username: str, preferred_level: str = 'Beginner'):
        """
        Initialize a User instance.
        Args:
            username (str): Display name of the user.
            preferred_level (str, optional): User's chosen level. Defaults to 'Beginner'.
        """
        self.username = username
        self.preferred_level = preferred_level
        self.favorites: List[Lesson] = []

    def set_level(self, new_level: str) -> None:
        """
        Updates the user's learning level.
        Args:
            new_level (str): The new learning level ('Beginner' or 'Intermediate').
        """
        self.preferred_level = new_level

    def add_favorite(self, lesson_obj: 'Lesson') -> None:
        """
        Adds a Lesson object to the user's favorites list if not already present.
        Args:
            lesson_obj (Lesson): The lesson to add to favorites.
        """
        if lesson_obj not in self.favorites:
            self.favorites.append(lesson_obj)


class LessonManager:
    """
    Acts as the logic layer to handle searching and filtering of lessons.
    """
    def __init__(self, all_lessons: List[Lesson]):
        """
        Initialize a LessonManager instance.
        Args:
            all_lessons (List[Lesson]): The master list containing all available lessons.
        """
        self.all_lessons = all_lessons

    def filter_by_topic(self, topic_name: str) -> List[Lesson]:
        """
        Returns lessons matching a specific topic.
        Args:
            topic_name (str): The topic to filter by.
        Returns:
            List[Lesson]: List of lessons matching the topic.
        """
        return [lesson for lesson in self.all_lessons if lesson.topic.lower() == topic_name.lower()]

    def filter_by_scholar(self, scholar_name: str) -> List[Lesson]:
        """
        Returns lessons matching a specific scholar.
        Args:
            scholar_name (str): The scholar's name to filter by.
        Returns:
            List[Lesson]: List of lessons matching the scholar.
        """
        return [lesson for lesson in self.all_lessons if lesson.scholar.lower() == scholar_name.lower()]

    def get_recommendations(self, user_obj: User) -> List[Lesson]:
        """
        Returns lessons matching the user's preferred learning level.
        Args:
            user_obj (User): The user for whom to get recommendations.
        Returns:
            List[Lesson]: List of recommended lessons.
        """
        return [lesson for lesson in self.all_lessons if lesson.level.lower() == user_obj.preferred_level.lower()]
