#!/usr/bin/env python
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from sys import exit
import numpy as np
import matplotlib.pyplot as plt
import re
import os

Builder.load_file('program.kv')


class MyLayout(Widget):

    def plot(self):
        """Function which plot given expresion"""
        replacements = {
            'sin': 'np.sin',
            'cos': 'np.cos',
            'tan': 'np.tan',
            'sqrt': 'np.sqrt',
            '^': '**',
            'ln': 'np.log',
            'log': 'np.log10',
            'abs': 'np.abs',
            'pi': 'np.pi',
            'e': 'np.e',
        }

        allowed_words = ['x', 'sin', 'cos', 'tan', 'sqrt', 'ln', 'log', 'abs', 'pi', 'e']

        fig, ax = plt.subplots(
            figsize=(self.width / 100 * self.ids.image.size_hint_x, self.height / 100 * self.ids.image.size_hint_y))
        ax.set_title(self.ids.title.text)
        ax.set_xlabel(self.ids.x_label.text)
        ax.set_ylabel(self.ids.y_label.text)
        ax.grid()

        try:
            a = self.ids.x_min.text
            b = self.ids.x_max.text

            if len(a) == 0:
                a = -5

            if len(b) == 0:
                b = 5

            a = float(a)
            b = float(b)

            ax.set_xlim(a, b)
            x = np.linspace(a, b, 1000)

        except ValueError:
            self.ids.information.text = " Start x and Stop x must be numbers!"
            self.ids.image.source = ''
            return None

        a = self.ids.y_min.text
        b = self.ids.y_max.text

        if len(a) != 0 or len(b) != 0:
            try:
                ax.set_ylim(float(a), float(b))
            except:
                pass

        def make_function(function_in_str):
            label = function_in_str

            def change_str_to_func(function_in_str):
                """Function change given expression in str to expresion which matplotlib know how to plot it"""

                for word in re.findall('[a-zA-Z_]+', function_in_str):
                    if word not in allowed_words:
                        self.ids.information.text = "You can't use word %s!" % str(word)
                        self.ids.image.source = ''
                        return None

                for old, new in replacements.items():
                    function_in_str = function_in_str.replace(old, new)
                function_in_str = function_in_str.replace('np.np.log10', 'np.log')

                def func(x):

                    try:
                        return eval(function_in_str)
                    except ZeroDivisionError:
                        self.ids.information.text = "You can't divide by 0!"
                        self.ids.image.source = ''
                        return None
                    except SyntaxError:
                        self.ids.information.text = "Please put * between multiplication"
                        self.ids.image.source = ''
                        return None

                return func

            func = change_str_to_func(function_in_str)
            print(func)

            try:
                ax.plot(x, func(x), label='y = ' + label)
            except:
                return None

            return True

        if len(self.ids.func.text.replace(";", "")) == 0:
            self.ids.information.text = "You can't plot nothing!"
            self.ids.image.source = ''
            return None

        for function_in_str in self.ids.func.text.split(";"):
            if len(function_in_str) != 0:
                a = make_function(function_in_str)
            if a is None:
                return None

        if self.ids.legend.active:
            ax.legend()
        fig.tight_layout()
        fig.savefig("Images\Wykres.png", dpi=500)
        self.ids.information.text = ''
        self.ids.image.reload()
        self.ids.image.source = 'Images\Wykres.png'

    def exit(self):
        """Function close application"""
        exit()

    def keypad(self, key):
        """Function which is used when you click button on application's keypad
        When you click value of key is added to your function, but C and CE have special functions"""
        pos = self.ids.func.cursor_index()
        if key == "C":
            self.ids.func.text = self.ids.func.text[:(pos - 1)] + self.ids.func.text[pos:]
            print(str(self.ids.func.cursor_col))
        elif key == "CE":
            self.ids.func.text = ''
        else:
            self.ids.func.text = self.ids.func.text[:pos] + str(key) + self.ids.func.text[pos:]


class PlotApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    os.chdir(os.path.split(os.path.realpath(__file__))[0])
    PlotApp().run()

