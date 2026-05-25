import terminal
import experiment_interface
import tkinter as tk

#USAR PELO TERMINAL
#t = terminal.terminal()
#t.show()

#USAR COM INTERFACE GRÁFICA
root = tk.Tk()
visual = experiment_interface.ExperimentInterface(root)
root.mainloop()