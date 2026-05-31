from tkinter import *
from TkUtils import TkUtils as ut

class ErrorView:
    def __init__(self):
        pass

    #display an error window message in a new popup window
    def show(self, message):

        #create error window
        error_window = ut.top_level("Error")


        #display error image and formatting
        ut.image(error_window, "image/error.png").pack()
        ut.separator(error_window).pack(fill=X, pady=(0, 10))


        # parse error message from a separate exception type
        if ":" in message:
            #split on first colon to get exception type
            parts = message.split(":", 1)
            exception_type = parts[0].strip()
            error_message = parts[1].strip()
        else:
            #if there is no colon, assume UnauthorisedAccessException
            exception_type = "UnauthorisedAccessException"
            error_message = message

        #display the exception type in error label
        ut.error_label(error_window, exception_type).pack()
        ut.separator(error_window).pack(fill=X, pady=(10, 10))

        #display error message under the exception type
        Label(error_window, text=error_message, font="Arial 10", foreground="#ff8f8f", background="#d9d9d9").pack()


        ut.separator(error_window).pack(fill=X, pady=(10, 10))
        # button to close window
        ut.button(error_window, "Close", error_window.destroy).pack(expand=True, fill=X)

        pass
