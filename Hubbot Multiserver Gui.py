import Tkinter

class hubbot_gui(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

if __name__ == "__main__":
    app = hubbot_gui(None)
    app.title("Hubbot")
    app.mainloop()
