from tkinter import ttk

class StartPage:
    def __init__(self, root, register_page, login_page):
        self.root = root
        self.register_page = register_page
        self.login_page = login_page

    def show(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        # Create a frame to hold the buttons
        frame = ttk.Frame(self.root)
        frame.pack(expand=True)

        button_register = ttk.Button(frame, text="Register", command=self.register_page.show)
        button_register.pack(side='left', padx=10)

        button_login = ttk.Button(frame, text="Login", command=self.login_page.show)
        button_login.pack(side='left', padx=10)