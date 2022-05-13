import tkinter
import tkinter.messagebox
import customtkinter
import database

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

connection = database.connect()
database.create_tables(connection)
c = connection.cursor()


class App(customtkinter.CTk):
    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.submit = None
        self.title("Coffee App")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        # self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20, weight=1)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Coffee Beans Database",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Add New Bean",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="See All Beans",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.see_all)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Search",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.button_4 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Best Method",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_event)
        self.button_4.grid(row=5, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(7, weight=0)
        self.frame_info.columnconfigure(0, weight=1)

    def button_event(self):

        def submit_new_bean():
            connection.execute("INSERT INTO beans VALUES (:name, :method, :rating)",
                               {
                                   'name': entry_name.get(),
                                   'method': entry_method.get(),
                                   'rating': entry_rating.get(),
                               })

            connection.commit()

        label_bean = customtkinter.CTkLabel(master=self.frame_info,
                                            text="Enter Bean Information:",
                                            height=25,
                                            justify=tkinter.LEFT)
        label_bean.grid(column=0, row=0, sticky="nw", padx=15, pady=5)
        entry_name = customtkinter.CTkEntry(master=self.frame_info,
                                            placeholder_text="Coffee Bean Name",
                                            width=200,
                                            height=25,
                                            border_width=2,
                                            corner_radius=10)
        entry_name.grid(column=0, row=1, sticky="nw", padx=15, pady=5)

        entry_method = customtkinter.CTkEntry(master=self.frame_info,
                                              placeholder_text="Method Used",
                                              width=200,
                                              height=25,
                                              border_width=2,
                                              corner_radius=10)
        entry_method.grid(column=0, row=2, sticky="nw", padx=15, pady=5)

        entry_rating = customtkinter.CTkEntry(master=self.frame_info,
                                              placeholder_text="Rating Score (0-100)",
                                              width=200,
                                              height=25,
                                              border_width=2,
                                              corner_radius=10)
        entry_rating.grid(column=0, row=3, sticky="nw", padx=15, pady=5)

        self.submit = customtkinter.CTkButton(master=self.frame_info,
                                              text="submit",
                                              command=submit_new_bean
                                              )
        self.submit.grid(row=8, column=2, columnspan=1, pady=0, padx=5, sticky="we")

    def see_all(self):
        c.execute("SELECT *, oid FROM beans")
        records = c.fetchall()
        print(records)

        connection.commit()

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
