from main import LessonScreen
from util import dotdict


class LessonCollection:

    def __init__(self, screens=[], manager=None):
        self._lessons = list(screens)
        self._manager = manager

    def add(self, screen):
        if self._lessons.count(screen) == 0:
            self._lessons.append(screen)

    def get_by_id(self, i):
        result = None
        #level = self._manager.get_current_level()
        for lesson in self.get_all_by_level():
            #print(lesson.get_id())

            if lesson.get_id() == i:
                result = lesson
                #print(result.get_id())

        return result

    def get_all(self):
        return self._lessons

    def get_all_by_level(self):
        level = self._manager.get_current_level()
        print(level)
        result = [lesson for lesson in self._lessons if lesson.get_level() == level]
        return result

    def get_lesson_id(self):
        # print(self._lessons)
        lessons = self.get_all_by_level()

        if len(lessons) < 1:
            return 0

        ids = [lesson.get_id() for lesson in lessons]
        return max(ids)

    def set(self, lessons):
        self._lessons.clear()
        self._lessons.extend(lessons)


class Lesson:
    def __init__(self, id, level="N5"):
        self._words = []
        self._id = id or 1
        self._level = level

    def add_word(self, w):
        self._words.append(w)

    def get(self, i):
        return self._words[i]

    def get_level(self):
        return self._level

    def get_words(self):
        return self._words

    def get_id(self):
        return self._id


class LessonManager:

    def __init__(self):
        self._lessons = LessonCollection([], self)
        self._manager = None
        self._viewer = None
        self._current_level = None

    def get_current_level(self):
        return self._current_level

    def set_current_level(self, level):
        self._current_level = level

    def set_screen_manager(self, manager):
        self._manager = manager
        self._viewer = LessonViewer(self._manager)

    def finish_lesson(self, *args):
        for lesson in self.get_lessons():
            self._viewer.clear_view(lesson)

    def get_last_id(self):
        print(self._lessons.get_lesson_id()+1)
        return self._lessons.get_lesson_id()+1

    def view(self, lesson):
        self._viewer.view_lesson(lesson)

    def add_lesson(self, lesson):
        self._lessons.add(lesson)

    def get_lesson(self, id):

        return self._lessons.get_by_id(id)

    def get_lessons(self):
        # print(self._lessons)

        return self._lessons.get_all_by_level()

    def set_lessons(self, lessons):
        self._lessons = lessons

    def generate_lesson(self, origin, words=[], level=None, lesson_id=False):
        # print(self._lessons.get_all())
        if not lesson_id:
            lesson = Lesson(self.get_last_id(), level)
        elif self.get_lesson(lesson_id):
            lesson = self.get_lesson(lesson_id)

            #  print(self.get_lessons())
            return lesson
        else:
            lesson = Lesson(lesson_id, level)

        library_screen = origin
        word_screens = [LessonScreen(l_id=word.get_id(),
                                     word=word.get_word(),
                                     meaning=word.get_meaning(),
                                     examples=word.get_examples(),
                                     reading=word.get_reading(),
                                     name="lesson" + str(words.index(word)) + str(origin.name) + str(
                                         self.get_last_id())) for word in words]
        for word_screen in word_screens:
            next = word_screens.index(word_screen) + 1
            prev = word_screens.index(word_screen) - 1
            if len(word_screens) == 1:
                word_screen.next_btn(library_screen)

            elif word_screens.index(word_screen) == 0:
                # add next , prev btns where 1 arg - next btn
                # 2 arg - prev btns
                word_screen.next_btn(word_screens[next])

            elif word_screens.index(word_screen) == (len(word_screens) - 1):
                word_screen.prev_btn(word_screens[prev])
                word_screen.next_btn(library_screen)
            else:
                word_screen.prev_btn(word_screens[prev])
                word_screen.next_btn(word_screens[next])
            lesson.add_word(word_screen)

        self.add_lesson(lesson)

        return lesson


class LessonViewer:
    def __init__(self, manager):
        self._manager = manager

    def view_lesson(self, lesson):
        #print(lesson.get_words())
        for word in lesson.get_words():
            self._manager.add_widget(word)

    def clear_view(self, lesson):
        self._manager.clear_widgets(lesson.get_words())


# sorry lessons ---- words

lessonManager = LessonManager()
