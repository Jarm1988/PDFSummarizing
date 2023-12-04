import tkinter as tk
from tkinter import ttk
import openai
from summaring_pdf import SummarizingPDF
from styles import configure_styles
from PIL import Image, ImageTk


class Register_key:
    def __init__(self, window):
        self.wind = window
        self.wind.title('PDFSummarizing')

        icon_path = "./icon.png"  # Reemplaza con la ruta de tu propio ícono
        self.icon_image = Image.open(icon_path)
        self.wind.iconphoto(True, ImageTk.PhotoImage(self.icon_image))

        # Establecer el tamaño de la ventana
        self.wind.geometry('600x170')  # Ancho x Alto
        self.wind.resizable(width=False, height=False)

        # Centrar el LabelFrame en la ventana
        self.wind.grid_rowconfigure(0, weight=1)
        self.wind.grid_columnconfigure(0, weight=1)
        self.wind.tk_setPalette(background="SystemButtonFace", foreground="SystemButtonText")

        # Crear un estilo temático de scidthemes
        configure_styles(window)

        # Crear un Frame Container
        frame = ttk.LabelFrame(self.wind, text='Please submit the OpenID Key', style="My.LabelFrame.TLabelframe")
        frame.grid(row=0, column=0, padx=20, pady=10, sticky=tk.N + tk.E + tk.W)

        # Clave de OpenAI
        ttk.Label(frame, text='OpenAI Key:').grid(row=2, column=0, pady=5, padx=5)
        self.openid_key = ttk.Entry(frame, style="My.TEntry", width=70)
        self.openid_key.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        # Botón para guardar la información
        my_button = ttk.Button(frame, text='Submit', command=self.submit)
        my_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

        # Mensajes de salida
        self.message = ttk.Label(frame, text='', foreground='red')
        self.message.grid(row=4, column=0, columnspan=3, pady=5, padx=5, sticky=tk.W + tk.E)

    def submit(self):
        openai_api_key = self.openid_key.get()
        openai.api_key = openai_api_key
        try:
            self.message.config(text='wait....', foreground='green')
            openai.Completion.create(model='curie')
        except Exception as e:
            self.message.config(text='error with the key, please try again', foreground='red')
            return
        self.message.config(text='ok', foreground='green')
        self.wind.destroy()
        root = tk.Tk()
        app = SummarizingPDF(root, openai_api_key)
        root.mainloop()
