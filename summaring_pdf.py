from langchain.chains.summarize import load_summarize_chain
from langchain.document_loaders import PyPDFLoader
from langchain import OpenAI
from langchain.indexes import VectorstoreIndexCreator
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext
from styles import configure_styles


class About:
    def __init__(self, parent):
        self.index = None
        self.window = parent
        self.window.title("About")
        self.window.resizable(width=False, height=False)

        label = ttk.Label(self.window, text=(
            "Welcome to PDFSummarizing!\n"
            "Version 1.0\n\n"
            "Powered by Lic Jorge A. Rodriguez\n"
            "© 2023 All rights reserved."
        ), wraplength=300, justify="center")
        label.pack(padx=20, pady=20)

        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)


class SummarizingPDF:
    def __init__(self, window, openai_api_key):
        self.index = None
        self.wind = window
        self.wind.title('PDFSummarizing')
        self.llm = OpenAI(openai_api_key=openai_api_key, temperature=0.2)
        os.environ['OPENAI_API_KEY'] = openai_api_key

        # Establecer el tamaño de la ventana
        self.wind.geometry('900x600')  # Ancho x Alto
        self.wind.resizable(width=False, height=False)

        # Centrar el LabelFrame en la ventana
        self.wind.grid_rowconfigure(0, weight=1)
        self.wind.grid_columnconfigure(0, weight=1)

        # Crear un estilo temático de scidthemes
        self.style = configure_styles(window)

        self.menubar = tk.Menu(self.wind)
        self.wind.config(menu=self.menubar)

        # Crea un menú desplegable llamado "File"
        self.file_menu1 = tk.Menu(self.menubar, tearoff=0)
        self.file_menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Home", menu=self.file_menu1)
        self.menubar.add_cascade(label="File", menu=self.file_menu2)
        self.file_menu1.add_command(label="Go Init", command=self.go_init)
        self.file_menu1.add_command(label="Exit", command=self.exit)
        self.file_menu2.add_command(label="Save Summary", command=self.save_summary)
        self.file_menu2.add_command(label="Save Querys", command=self.save_querys)
        self.file_menu2.add_command(label="Clear Querys", command=self.clear_querys)
        self.menubar.add_command(label="About", command=self.about)

        # Crear un Frame Container
        frame = ttk.LabelFrame(self.wind, text='Select PDFs to process')
        frame.grid(row=0, column=0, padx=20, pady=10, sticky=tk.N + tk.E + tk.W + tk.S)
        frame.columnconfigure(1, weight=1)

        # Botón para abrir el diálogo de selección de carpeta
        self.boton_seleccionar_carpeta = ttk.Button(frame, text="Select PDF", command=self.select_file)
        self.boton_seleccionar_carpeta.grid(row=0, column=0, padx=20, pady=10, sticky=tk.N + tk.W + tk.S)

        self.message = ttk.Label(frame, text='', foreground='red')
        self.message.grid(row=0, column=1, padx=20, pady=(0, 20), sticky=tk.N + tk.E + tk.S)

        self.file = ttk.Label(frame, text='No PDF selected', foreground='red')
        self.file.grid(row=1, column=0, padx=20, pady=10, sticky=tk.N + tk.W + tk.S)

        frame2 = ttk.LabelFrame(self.wind, text='Summary')
        frame2.grid(row=2, column=0, padx=20, pady=10, sticky=tk.N + tk.E + tk.W + tk.S)

        # Campo de texto grande para mostrar la ruta de la carpeta seleccionada
        self.summary_text = scrolledtext.ScrolledText(frame2, height=7, width=100, wrap=tk.WORD,
                                                      state=tk.DISABLED)
        self.summary_text.grid(pady=10, padx=10)

        frame3 = ttk.LabelFrame(self.wind, text='Queries')
        frame3.grid(row=4, column=0, padx=20, pady=10, sticky=tk.N + tk.E + tk.W + tk.S)

        # Campo de texto grande para mostrar la ruta de la carpeta seleccionada
        self.text_querys = scrolledtext.ScrolledText(frame3, height=12, width=100, wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.text_querys.grid(row=1, column=0, columnspan=3, pady=10, padx=10)

        self.query = ttk.Entry(frame3, width=110)
        self.query.grid(row=2, column=0, columnspan=2, pady=5, padx=10,
                        sticky=tk.E + tk.W)
        ttk.Button(frame3, text='Send', style="My.TButton", command=self.send_query).grid(row=2, column=2, sticky=tk.W)

    def select_file(self):
        self.message.config(text='wait...', foreground='green')
        try:
            file_options = {
                'title': 'Seleccionar PDF',
                'filetypes': [('Archivos PDF', '*.pdf')],
            }
            pdf_file = filedialog.askopenfilename(**file_options)
            if pdf_file:
                name_pdf_file = os.path.basename(pdf_file)
                summarie = self.summarize_pdf(pdf_file)
                self.summary_text.config(state=tk.NORMAL)
                self.summary_text.delete(1.0, tk.END)
                self.summary_text.insert(tk.END, f'{summarie}')
                self.summary_text.config(state=tk.DISABLED)
                self.file.config(text=name_pdf_file, foreground='black')
                self.message.config(text='', foreground='black')
            else:
                self.message.config(text='', foreground='red')
        except Exception as e:
            self.message.config(text='Error with the key, please try again', foreground='red')

    def send_query(self):
        self.message.config(text='wait...', foreground='green')
        query = self.query.get()
        if query != '':
            try:
                response = self.response_query(query)
                self.text_querys.config(state=tk.NORMAL)
                self.text_querys.tag_configure("blue", foreground='blue')
                self.text_querys.tag_configure("red", foreground='green')
                self.text_querys.insert(tk.END, f'{query}:\n', ('blue'))
                self.text_querys.insert(tk.END, f'{response}\n\n', ('red'))
                self.text_querys.config(state=tk.DISABLED)
                self.text_querys.see(tk.END)
                self.message.config(text='', foreground='green')
            except Exception as e:
                self.message.config(text='Error with the key, please try again', foreground='red')

    def summarize_pdf(self, pdf_file):
        loader = PyPDFLoader(pdf_file)
        self.index = VectorstoreIndexCreator().from_loaders([loader])
        docs = loader.load_and_split()
        chain = load_summarize_chain(self.llm, chain_type="map_reduce")
        summary = chain.run(docs)
        return summary

    def response_query(self, query):
        return self.index.query(query)

    def go_init(self):
        from register_key import Register_key
        self.wind.destroy()
        root = tk.Tk()
        app = Register_key(root)
        root.mainloop()

    def exit(self):
        self.wind.destroy()

    def clear_querys(self):
        self.text_querys.config(state=tk.NORMAL)
        self.text_querys.delete(1.0, tk.END)
        self.text_querys.config(state=tk.DISABLED)

    def save_querys(self):
        query_text = self.text_querys.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            # Abrir el archivo en modo escritura
            with open(file_path, "w") as file:
                file.write(query_text)

    def clear_summary(self):
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state=tk.DISABLED)

    def save_summary(self):
        query_text = self.summary_text.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            # Abrir el archivo en modo escritura
            with open(file_path, "w") as file:
                file.write(query_text)

    def about(self):
        root = tk.Tk()
        app = About(root)
        root.mainloop()
