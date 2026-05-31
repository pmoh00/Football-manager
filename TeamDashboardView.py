from tkinter import *
from TkUtils import TkUtils as ut
from ErrorView import ErrorView
from model.enums.Position import Position
from model.exception.InvalidSigningException import InvalidSigningException
from model.exception.FillException import FillException


class TeamDashboardView:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.tree = None
        self.sign_entry = None
        self.sign_btn = None
        self.unsign_btn = None
        self.jersey_labels = []

    # press enter to sign
    def handle_enter(self, event):
        if str(self.sign_btn['state']) != 'disabled':
            self.sign_player()

    # build and display team managemnt dashboard
    def control(self):
        manager = self.model.get_logged_in_manager()
        team = manager.get_team()

        # clear jersey labels list for refresh
        self.jersey_labels = []

        ut.same_window("Team Dashboard", self.root)

        ut.image(self.root, "image/banner.png", height=200, width=360).pack()

        ut.separator(self.root).pack(fill=X, pady=(0, 10))
        ut.label(self.root, str(team)).pack()
        ut.separator(self.root).pack(fill=X, pady=(10, 10))

        sign_frame = Frame(self.root)
        ut.label(sign_frame, "Sign a new player:").pack(side=LEFT, padx=(0, 10))

        self.sign_entry = Entry(sign_frame, width=20)
        self.sign_entry.pack(side=LEFT, padx=(0, 10))
        self.sign_entry.bind("<KeyRelease>", lambda e: self.update_sign_button())
        self.sign_entry.bind("<Return>", self.handle_enter)

        self.sign_btn = ut.button(sign_frame, "Sign", self.sign_player)
        self.sign_btn.pack(side=LEFT)
        self.sign_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

        sign_frame.pack(pady=(0, 10))

        content_frame = Frame(self.root)


        left_frame = Frame(content_frame, highlightbackground="#e8e8e8", highlightthickness=1, bd=0)

        # gradient table header
        header_frame = Frame(left_frame)


        gradient_top = Frame(header_frame, bg="#fafafa", height=3)
        gradient_top.pack(fill=X)

        gradient_mid1 = Frame(header_frame, bg="#f2f2f2", height=2)
        gradient_mid1.pack(fill=X)

        header_content = Frame(header_frame, bg="#e8e8e8")
        Label(header_content, text="Name", font="Arial 10 bold", bg="#e8e8e8",
              width=15, anchor=CENTER, fg="#ff8080").pack(side=LEFT)
        Label(header_content, text="Position", font="Arial 10 bold", bg="#e8e8e8",
              width=10, anchor=CENTER, fg="#ff8080").pack(side=LEFT)
        header_content.pack(fill=X)

        gradient_mid2 = Frame(header_frame, bg="#d8d8d8", height=2)
        gradient_mid2.pack(fill=X)

        gradient_bottom = Frame(header_frame, bg="#c8c8c8", height=3)
        gradient_bottom.pack(fill=X)

        header_frame.pack(fill=X)

        # table
        tree_frame = Frame(left_frame, highlightthickness=0, borderwidth=0)
        self.tree = ut.treeview(tree_frame, ["Name", "Position"], width=250)
        self.tree.config(height=15, show="")
        self.tree.pack()
        tree_frame.pack()

        self.populate_players(team)

        self.tree.bind("<<TreeviewSelect>>", lambda e: self.update_unsign_button())

        left_frame.pack(side=LEFT, padx=(10, 5))

        # active team on the right
        right_frame = Frame(content_frame, bg="white")

        active_header_frame = Frame(right_frame, bg="#2b2b2b")
        Label(active_header_frame, text="Active Team", font="Arial 12 bold",
              foreground="#ff8080", bg="#2b2b2b").pack(fill=X, pady=5)
        active_header_frame.pack(fill=X)

        jersey_frame = Frame(right_frame, bg="white")

        self.create_jersey_position(jersey_frame, 0, team).grid(row=0, column=1, padx=3, pady=3)
        self.create_jersey_position(jersey_frame, 1, team).grid(row=1, column=0, padx=3, pady=3)
        self.create_jersey_position(jersey_frame, 2, team).grid(row=1, column=1, padx=3, pady=3)
        self.create_jersey_position(jersey_frame, 3, team).grid(row=1, column=2, padx=3, pady=3)
        self.create_jersey_position(jersey_frame, 4, team).grid(row=2, column=1, padx=3, pady=3)

        jersey_frame.pack(pady=5)

        right_frame.pack(side=LEFT, padx=(5, 10), fill=Y)

        content_frame.pack()

        # bottom buttons
        btn_frame = Frame(self.root)

        self.unsign_btn = ut.button(btn_frame, "Unsign", self.unsign_player)
        self.unsign_btn.pack(side=LEFT, expand=True, fill=X)
        self.unsign_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

        ut.button(btn_frame, "Close", self.close).pack(side=LEFT, expand=True, fill=X)

        btn_frame.pack(expand=True, fill=BOTH, pady=(10, 0))

    # jersey images for positions on the active team
    def create_jersey_position(self, parent, position_index, team):

        frame = Frame(parent, bg="#f0f0f0")

        player = team.current_team[position_index]

        if player:
            jersey_path = f"image/{team.team_name.lower()}.png"
            tooltip_text = f"{player.get_full_name()} ({player.get_position()})"
        else:
            jersey_path = "image/none.png"
            tooltip_text = "Empty Position"

        jersey_label = ut.image(frame, jersey_path, height=60, width=60)
        jersey_label.pack()

        ut.attach_tooltip(jersey_label, tooltip_text)

        jersey_label.position_index = position_index

        jersey_label.bind("<Button-1>", lambda e: self.assign_to_position(position_index))

        self.jersey_labels.append(jersey_label)

        return frame

    # popoulate the table
    def populate_players(self, team):

        for item in self.tree.get_children():
            self.tree.delete(item)

        all_players = team.get_all_players().get_players()

        for i, player in enumerate(all_players):
            self.tree.insert("", END, values=(player.get_full_name(), str(player.get_position())))
            # Add alternating row colors
            if i % 2 == 0:
                self.tree.item(self.tree.get_children()[i], tags=('evenrow',))
            else:
                self.tree.item(self.tree.get_children()[i], tags=('oddrow',))

        #always have 15 rows in table
        remaining_rows = 15 - len(all_players)
        for i in range(remaining_rows):
            current_index = len(all_players) + i
            self.tree.insert("", END, values=("", ""))
            if current_index % 2 == 0:
                self.tree.item(self.tree.get_children()[current_index], tags=('evenrow',))
            else:
                self.tree.item(self.tree.get_children()[current_index], tags=('oddrow',))

        # white/grey pattern on table rows
        self.tree.tag_configure('evenrow', background='#f0f0f0')
        self.tree.tag_configure('oddrow', background='white')

    # only enable sign button is there is text in the signing entry
    def update_sign_button(self):

        if self.sign_entry.get().strip():
            self.sign_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
        else:
            self.sign_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

    #only enable the unsign button if a player is selected
    def update_unsign_button(self):

        selection = self.tree.selection()
        if selection:
            self.unsign_btn.config(state=NORMAL, background="#ff8f8f", foreground="white")
        else:
            self.unsign_btn.config(state=DISABLED, background="#ecbaba", disabledforeground="white")

    # sign player to the team
    def sign_player(self):

        try:
            player_name = self.sign_entry.get().strip()
            manager = self.model.get_logged_in_manager()
            team = manager.get_team()

            # find player
            player = self.model.get_players().player(player_name)

            if player is None:
                raise InvalidSigningException("Player does not exist within the league")

            #check if it already signed to current team
            if player.get_team() == team:
                raise InvalidSigningException(f"{player.get_full_name()} is already signed to your team")

            #check if player is signed to the another team
            if player.get_team() is not None:
                raise InvalidSigningException(
                    f"Cannot sign {player.get_full_name()}, player is already signed to {player.get_team()}")

            #sign player
            player.set_team(team)
            team.get_all_players().add(player)

            #refresh
            self.sign_entry.delete(0, END)
            self.control()

        except InvalidSigningException as e:
            ErrorView().show(f"InvalidSigningException: {str(e)}")
        except Exception as e:
            ErrorView().show(str(e))

    #unsign a player from the team
    def unsign_player(self):

        try:
            selection = self.tree.selection()
            if not selection:
                return

            manager = self.model.get_logged_in_manager()
            team = manager.get_team()

            selected_values = self.tree.item(selection[0])["values"]
            player_name = selected_values[0]

            #find player
            player = team.get_all_players().player(player_name)

            if player:
                # check if player is active
                if player in team.current_team:
                    raise InvalidSigningException(
                        f"Cannot remove {player.get_full_name()}, player is in the active team")

                # remove from team
                player.set_team(None)
                team.get_all_players().remove(player)

                self.control()

        except InvalidSigningException as e:
            ErrorView().show(f"InvalidSigningException: {str(e)}")
        except Exception as e:
            ErrorView().show(str(e))

    #assigns selected player to active position
    def assign_to_position(self, position_index):

        try:
            selection = self.tree.selection()
            manager = self.model.get_logged_in_manager()
            team = manager.get_team()

            #clear position
            if not selection:
                team.current_team[position_index] = None
                self.control()
                return

            #get selected player
            selected_values = self.tree.item(selection[0])["values"]
            player_name = selected_values[0]
            player = team.get_all_players().player(player_name)

            if player:
                #check if plyaer is active in a different position
                if player in team.current_team:
                    current_position = team.current_team.index(player)
                    if current_position != position_index:
                        raise FillException(f"{player.get_full_name()} is already in the active playing team")

                #assign, replace if position is filled
                team.current_team[position_index] = player


                self.control()

        except FillException as e:
            ErrorView().show(f"FillException: {str(e)}")
        except Exception as e:
            ErrorView().show(str(e))

    def close(self):
        self.root.destroy()