from tkinter import *
from PIL import Image, ImageTk
from function_drawer import *


class Window(Tk):
    def __init__(self, *args, **kwargs) -> None:
        super(Window, self).__init__(*args, **kwargs)
        self.load_gui()

    def load_gui(self, *args, **kwargs) -> None:
        self.geometry(f"{config.img_width}x{config.img_height+50}")

        self.label1 = Label(self, text="F(x) = ")
        self.functions = Entry(self)
        self.button1 = Button(self, text="OK", command=self.draw_functions)
        self.image_label = Label(self, image=ImageTk.PhotoImage(Image.open(config.imgs_path)))
        self.label1.pack()
        self.functions.pack()
        self.button1.pack()
        self.image_label.pack()

    def draw_functions(self, *args, **kwargs) -> None:
        pass

    @staticmethod
    def load_img(path, *args, **kwargs) -> ImageTk.PhotoImage:
        return ImageTk.PhotoImage(Image.open(path))


if __name__ == '__main__':
    root = Tk()

    label = Label(root, image=Window.load_img("imgs/new.jpg"))
    label.pack()

    root.mainloop()
