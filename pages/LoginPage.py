from tkinter import ttk

class LoginPage:
    def __init__(self, root, show_start_page):
        self.root = root
        self.show_start_page = show_start_page

    def login(self):
        pass
    #     username = self.entry_username.get()
    #     c.execute("SELECT * FROM users WHERE username=?", (username,))
    #     user = c.fetchone()
    #     if user:
    #         # Here you should add the code to compare the voice_sample and photo with the ones stored in the database
    #         pass

    def show(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

        username_entry = ttk.Entry(self.root)
        username_entry.pack()

        login_button = ttk.Button(self.root, text="Login", command=self.login)
        login_button.pack()

        back_button = ttk.Button(self.root, text="Back", command=self.show_start_page)
        back_button.pack()