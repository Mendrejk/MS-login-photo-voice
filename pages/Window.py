import os

from ttkthemes.themed_tk import ThemedTk

from pages.LoginPage import LoginPage
from pages.RegisterPage import RegisterPage
from pages.StartPage import StartPage


class Window:
    def __init__(self):
        self.root = ThemedTk(theme="equilux")
        self.root.geometry("1600x1200")
        self.root.configure(background='#3d3d3d')

        self.register_page = RegisterPage(self.root, lambda: self.show_page(self.start_page))
        self.login_page = LoginPage(self.root, lambda: self.show_page(self.start_page))
        self.start_page = StartPage(self.root, self.register_page, self.login_page)

    def show_page(self, page):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        page.show()

    def on_closing(self):
        self.root.destroy()


    def start(self):
        self.show_page(self.start_page)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
