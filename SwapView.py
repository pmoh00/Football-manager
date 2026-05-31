from tkinter import *
from TkUtils import TkUtils as ut
from ErrorView import ErrorView


class SwapView:
    def __init__(self, root, model, observable_view):
        self.root = root
        self.model = model
        self.observable_view = observable_view
        self.tree = None
        self.swap_window = None
        self.swap_btn = None

    # display the swap window with avaliable teams
    def show(self):

        #create swap in separate window
        self.swap_window = ut.top_level("Swap")

        ut.image(self.swap_window, "image/banner.png").pack()

        ut.separator(self.swap_window).pack(fill=X, pady=(0, 10))

        ut.label(self.swap_window, "Swap Team").pack()

        ut.separator(self.swap_window).pack(fill=X, pady=(10, 10))

        listbox_frame = Frame(self.swap_window)

        scrollbar = Scrollbar(listbox_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        #create a listbox to display the avaliable teams
        self.listbox = Listbox(listbox_frame, yscrollcommand=scrollbar.set,
                               font="Arial 11", height=15, width=40,
                               selectmode=SINGLE, relief=FLAT,
                               highlightthickness=1, highlightbackground="#d9d9d9",
                               justify=CENTER, bg="white", selectbackground="#b0e0ff")
        self.listbox.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        listbox_frame.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))


        #bind selection to enable/disable the swap btn
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.update_swap_button())


        #fill listbox with managable teams
        self.populate_teams()

        btn_frame = Frame(self.swap_window)

        self.swap_btn = ut.button(btn_frame, "Swap", self.swap)
        self.swap_btn.pack(side=LEFT, expand=True, fill=X)
        self.swap_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

        ut.button(btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)

        btn_frame.pack(expand=True, fill=BOTH)

    # team list population
    def populate_teams(self):

        self.listbox.delete(0, END)

        #get teams that dont have a manager
        manageable_teams = self.model.get_manageable_teams().get_teams()

        #add each team to listbox
        for i, team in enumerate(manageable_teams):
            self.listbox.insert(END, str(team))
            if i % 2 == 0:
                self.listbox.itemconfig(i, background="#f0f0f0", selectbackground="#b0e0ff")
            else:
                self.listbox.itemconfig(i, background="white", selectbackground="#b0e0ff")

    def update_swap_button(self):
        selection = self.listbox.curselection()
        if selection:
            self.swap_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
        else:
            self.swap_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")

    # assign the selected team to the logged in manager
    def swap(self):
        try:
            #list view selction
            selection = self.listbox.curselection()

            if not selection:
                return

            selected_team_name = self.listbox.get(selection[0])

            manageable_teams = self.model.get_manageable_teams().get_teams()
            selected_team = None

            for team in manageable_teams:
                if str(team) == selected_team_name:
                    selected_team = team
                    break

            if selected_team:
                manager = self.model.get_logged_in_manager()
                self.model.set_manager_for_team(manager, selected_team)


                self.populate_teams()
                self.observable_view.control()

        except Exception as e:
            ErrorView().show(str(e))

    # close
    def close(self):

        self.swap_window.destroy()