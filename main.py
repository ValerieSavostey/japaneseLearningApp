#!/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
__version__ = "1.0.3"

from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, WipeTransition, CardTransition


class JPLabel(Label):
    pass


# custom screen wrapper

class JPAppScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)

    def next_screen(self, name):
        if not self.manager.has_screen(name):
            print("No Screen was found")
        self.manager.transition.direction = "left"

        self.manager.current = name

    def back_screen(self, name=None):
        # print(self.manager.screen_names)
        if name is None:
            name = self.manager.previous()
        self.manager.transition.direction = "right"

        self.manager.current = name


class LevelManager(JPAppScreen):

    def generate(self):
        words = WordsMn.get_rand_words()

        lesson = lesson_manager.generate_lesson(self, words, lesson_manager.get_current_level())
        lesson_manager.view(lesson)
        self.manager.lesson_events.bind(on_finished=self.manager.lesson_finishes)
        self.gen_library()
        self.next_screen(lesson.get(0).name)

    def gen_library(self):
        if self.manager.has_screen("Library"):
            self.manager.remove_widget(self.manager.get_screen("Library"))
        library = Library()
        # print)
        lessons = lesson_manager.get_lessons()
        lessons.sort(key=lambda e: e.get_id())
        print(lessons)
        for lesson in lessons:
            l_id = lesson.get_id()
            btn = Button(size_hint=(None, None),
                         size=("140dp", "80dp"),
                         background_color=(.9, .9, .9, .9),
                         text=str(l_id),
                         font_size="20dp",
                         color=(1, 1, 1, 1))
            btn.bind(on_press=lambda instance: library.go_to_lesson(int(instance.text)))
            library.ids.lesson_library.add_widget(btn)
        self.manager.add_widget(library)

    def library(self):
        self.gen_library()
        self.next_screen("Library")


# static screens

class MainMenu(JPAppScreen):

    def choose_level(self, btn):
        if not WordsMn.get_words(btn.text):
            Popup(title="Sorry",
                  size_hint=(None, None),
                  size=("500dp", "500dp"),
                  content=Label(font_size="20sp", text="No words available for this level!:(")).open()
        else:
            # self.manager.get_screen("Generate").gen_library()
            # lesson_manager.set_current_level(WordsMn.get_current_level())
            self.next_screen("Generate")


class Options(JPAppScreen):

    def save_changes(self, q):
        WordsMn.set_quantity(q.value)


class Library(JPAppScreen):

    def __init__(self, **kwargs):
        super(Library, self).__init__(**kwargs)

        # for i in range(lesson_manager.get_last_id()):

    def go_to_lesson(self, l_id):
        words = lesson_manager.get_lesson(l_id).get_words()
        lesson = lesson_manager.generate_lesson(self, words, lesson_manager.get_current_level(), l_id)
        # print(l_id)
        lesson_manager.view(lesson)
        self.manager.lesson_events.bind(on_finished=lesson_manager.finish_lesson)
        self.next_screen(lesson.get(0).name)


# Lesson


class LessonScreen(JPAppScreen):

    def __init__(self, l_id, word, meaning, examples, reading=None, **kwargs):
        super(LessonScreen, self).__init__(**kwargs)
        self._id = l_id
        self._word = word
        self._meaning = meaning
        self._reading = reading
        self._examples = examples

        width = Window.size[0]
        if self._word:
            # self.ids.word_reading.add_widget(JPLabel(font_size=width/15, text=self._word))
            self.ids.word.text = self._word
        else:
            self.ids.word_reading.remove_widget(self.ids.word)
        if self._reading:
            # self.ids.word_reading.add_widget(JPLabel(font_size=width/15, text=self._reading))
            self.ids.reading.text = self._reading
        else:
            self.ids.word_reading.remove_widget(self.ids.reading)
        if self._meaning:
            self.ids.meaning.text = self._meaning
        for example in self._examples:
            self.ids.examples.add_widget(Example(example))

    def next_btn(self, screen):
        # print(screen)
        cb = lambda x: self.next(screen.name)
        if not isinstance(screen, LessonScreen):
            if isinstance(screen, LevelManager):
                screen.gen_library()
            cb = lambda y: self.finishes("Library")
        self.ids.next_prev_btns.add_widget(Button(text="Next word",
                                                  background_color=(0, .8, 1, .9),
                                                  size_hint=(0.5, 1),
                                                  color=(1, 1, 1, 1),
                                                  pos_hint={"right": 1},
                                                  on_press=cb))

    def prev_btn(self, screen):
        self.ids.next_prev_btns.add_widget(Button(text="Previous word",
                                                  background_color=(0, .8, 1, .9),
                                                  size_hint=(0.5, 1),
                                                  color=(1, 1, 1, 1),
                                                  pos_hint={"left": 0},
                                                  on_press=lambda x: self.back(screen.name)))

    def next(self, lesson):

        self.next_screen(lesson)

    def back(self, lesson):

        self.back_screen(lesson)

    def finishes(self, screen):
        self.next(screen)
        self.manager.lesson_events.execute()


class Example(BoxLayout):
    def __init__(self, example_p, **kwargs):
        super(Example, self).__init__(**kwargs)
        # example is (id,'kanji example','furigana example','translation',word_id)
        self.ids.kanji.text = example_p[1]
        self.ids.furigana.text = example_p[2]
        self.ids.romaji.text = example_p[3]


# Main classes

class JPWordsClass(ScreenManager):
    _current_level = ""

    def __init__(self, **kwargs):
        super(JPWordsClass, self).__init__(**kwargs)
        self._lesson = lesson_manager.get_last_id()
        self.lesson_events = LessonEvents()
        self.lesson_events.bind(on_finished=self.lesson_finishes)

    def lesson_finishes(self, lesson):
        print("::::")
        print(lesson_manager.get_last_id() - 1)
        WordsMn.save_lessons(lesson_manager.get_last_id() - 1)
        lesson_manager.finish_lesson(lesson)

    def get_lesson_id(self):
        return self._lesson


class LessonEvents(EventDispatcher):

    def __init__(self, **kwargs):
        self.register_event_type("on_finished")
        super(LessonEvents, self).__init__(**kwargs)

    def on_finished(self, *args):
        print(args)

    def execute(self):
        self.dispatch("on_finished")


class JPWords(App):
    def build(self):
        sm = JPWordsClass(transition=CardTransition())
        lesson_manager.set_screen_manager(sm)
        return sm


if __name__ == '__main__':
    from lessons import lessonManager as lesson_manager
    from wordsManager import wordsMn as WordsMn

    LabelBase.register("Japanese", "./fonts/NotoSansJP-Medium.otf")
    JPWords().run()
