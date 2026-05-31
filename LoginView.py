from tkinter import *
from TkUtils import TkUtils as ut
from model.application.League import league
from model.exception.UnauthorisedAccessException import UnauthorisedAccessException
from ErrorView import ErrorView
from ManagerDashboardView import ManagerDashboardView


class LoginView:

    def __init__(self, root, model):
        self.root = root  #root (tk.TK) stores reference to the main window
        self.model = model #stores reference to league
        self.entry = None   #text entry field for ID, initialized later
        self.login_btn = None   #login button, initialized later

    #enter to login
    def handle_enter(self, event):
        #check if button is enabled
        if str(self.login_btn['state']) != 'disabled':
            self.login() #if it is, trigger the login

    #build and display the login window
    def control(self):
        ut.image(self.root, "image/banner.png").pack()
        ut.separator(self.root).pack(fill=X, pady=(0, 10))
        ut.label(self.root, "Login").pack()
        ut.separator(self.root).pack(fill=X, pady=(0, 10))

        #manager id label and input
        content_frame = Frame(self.root)
        ut.label(content_frame, "Manager ID: ").pack(side=LEFT)
        self.entry = Entry(content_frame)
        self.entry.pack(side=LEFT)
        self.entry.bind("<KeyRelease>", lambda e: self.update_login_button())   #update button state as the user types
        self.entry.bind("<Return>", self.handle_enter)  #functionality to login with enter
        content_frame.pack()

        #create login button
        btn_frame = Frame(self.root)
        self.login_btn = ut.button(btn_frame, "Login", self.login)
        self.login_btn.pack(side=LEFT, expand=True, fill=X)
        self.login_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")


        #create close button
        ut.button(btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)
        btn_frame.pack(expand=True, fill=BOTH, pady=(10, 0))

    def update_login_button(self):
        if self.entry.get().strip():
            self.login_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
        else:
            self.login_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

    def close(self):
        self.root.destroy()

    # validate the login details
    def login(self):

        try:
            manager_id_str = self.entry.get().strip()

            if not manager_id_str:
                ErrorView().show("UnauthorisedAccessException: Incorrect format for manager id")
                return

            manager_id = int(manager_id_str)
            manager = self.model.validate_manager(manager_id)

            self.model.set_logged_in_manager(manager)

            ManagerDashboardView(self.root, self.model).control()


        except ValueError:
            ErrorView().show("UnauthorisedAccessException: Incorrect format for manager id")
        except UnauthorisedAccessException as e:
            ErrorView().show("UnauthorisedAccessException: Invalid login credentials")
        except Exception as e:
            ErrorView().show(str(e))


if __name__ == "__main__":
    root = ut.root()
    LoginView(root, league).control()
    root.mainloop()