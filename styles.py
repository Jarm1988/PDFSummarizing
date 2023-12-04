from tkinter import ttk


def configure_styles(root):
    style = ttk.Style()
    style.configure("TButton",
                    padding=(10, 5),  # Cambiar el relief a "flat"
                    background="green",
                    foreground="black",
                    font=('Helvetica', 10))

    style.map("TButton",
              background=[('!active', 'green'), ('active', 'darkgreen')]
              )
    style.configure("My.TButton",
                    padding=(5, 2))
    style.configure("TEntry",
                    padding=(10, 5),
                    font=('Helvetica', 10))
    style.configure("TLabel",
                    font=('Helvetica', 10)
                    )
    style.configure("TScrolledText",
                    font=('Helvetica', 10)
                    )
