import tkinter as tk
root = tk.Tk()
root.geometry("200x200")
main_menu = tk.Menu(root)
root.config(menu=main_menu)
main_menu.add("command", label="file", command=root.quit)
root.mainloop()