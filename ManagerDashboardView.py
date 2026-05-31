from tkinter import *
from TkUtils import TkUtils as ut
from ErrorView import ErrorView
from SwapView import SwapView
from TeamDashboardView import TeamDashboardView

class ManagerDashboardView:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.withdraw_btn = None
        self.manage_btn = None

    #build and display the manager dashboard
    def control(self):
        # clear existing content and display the manager dash in same window
        ut.same_window("Manager Dashboard", self.root)

        ut.image(self.root, "image/banner.png").pack()

        #get the currently logged in manager
        manager = self.model.get_logged_in_manager()
        team = manager.get_team()

        ut.separator(self.root).pack(fill=X, pady=(0, 10))


        #display the team name, if no team then display generic message
        if team:
            team_label = str(team)
        else:
            team_label = "No Team"

        ut.label(self.root, team_label).pack()

        ut.separator(self.root).pack(fill=X, pady=(10, 0))

        #display team jersey icon, if no team display none.png
        if team:
            jersey_path = f"image/{team.team_name.lower()}.png"
        else:
            jersey_path = "image/none.png"

        ut.image(self.root, jersey_path, height=200, width=200).pack(pady=(10, 0))

        team_btn_frame = Frame(self.root)

        #create withdraw btn
        self.withdraw_btn = ut.button(team_btn_frame, "Withdraw", self.withdraw)
        self.withdraw_btn.pack(side=LEFT, expand=True, fill=X)

        #create manage btn
        self.manage_btn = ut.button(team_btn_frame, "Manage", self.manage)
        self.manage_btn.pack(side=LEFT, expand=True, fill=X)

        team_btn_frame.pack(fill=X, pady=(10, 0))

        bottom_btn_frame = Frame(self.root)

        ut.button(bottom_btn_frame, "Swap Team", self.swap_team).pack(side=LEFT, expand=True, fill=X)
        ut.button(bottom_btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)

        bottom_btn_frame.pack(expand=True, fill=BOTH)

        self.update_buttons()

    #only enable the withdraw and manage buttons if the manager a team
    def update_buttons(self):

        manager = self.model.get_logged_in_manager()
        has_team = manager.get_team() is not None

        if has_team:
            self.withdraw_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
            self.manage_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
        else:
            self.withdraw_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")
            self.manage_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")


    #withdraw manager from their current team
    def withdraw(self):

        try:
            manager = self.model.get_logged_in_manager()
            self.model.withdraw_manager_from_team(manager)

            # Refresh the view
            self.control()

        except Exception as e:
            ErrorView().show(str(e))

    #manage team
    def manage(self):

        manager = self.model.get_logged_in_manager()
        if manager.get_team() is not None:
            TeamDashboardView(self.root, self.model).control()

    #swap team
    def swap_team(self):
        SwapView(self.root, self.model, self).show()
        pass

    #closes the manager dashboard
    def close(self):

        self.root.destroy()