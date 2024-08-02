import tkinter as tk
import os
from PIL import Image, ImageTk


class InteractivePowerPoint:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive PowerPoint")

        # Lista dei nomi dei file delle slide
        self.slides = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
        self.current_slide_index = 0

        # Carica l'immagine iniziale
        self.load_image(self.slides[self.current_slide_index])

        # Crea un canvas per visualizzare l'immagine
        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack()

        # Aggiunge l'immagine al canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Imposta le dimensioni della finestra
        root.geometry(f"{self.image.width}x{self.image.height}")


        # Crea i pulsanti con le relative funzioni di callback
        self.button_skip = tk.Button(root, text="Skip Tutorial", bg="#4285f4", fg="white", command=self.skip_tutorial, font=("Helvetica", 40, "bold"),height=2)
        self.button_start = tk.Button(root, text="Start Tutorial", bg="#4285f4", fg="white", command=self.start_tutorial, font=("Helvetica", 40, "bold"),height=2)
        self.button_next = tk.Button(root, text="Next Gesture", bg="#4285f4", fg="white", command=self.next_gesture, font=("Helvetica", 40, "bold"),height=2)
        self.button_previous = tk.Button(root, text="Previous Gesture", bg="#4285f4", fg="white", command=self.previous_gesture, font=("Helvetica", 40, "bold"),height=2)
        self.button_select = tk.Button(root, text="Select File", bg="#4285f4", fg="white", command=self.select_file, font=("Helvetica", 42, "bold"),height=2)

        # Aggiorna la visualizzazione dei pulsanti
        self.update_buttons()

    def select_file(self):

        #dopo che hai selezionato il file chiudi la finestra
        self.root.quit()
        return

    def load_image(self, image_name):
        # Ottiene il percorso assoluto dell'immagine e la carica
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, image_name)
        self.image = Image.open(image_path)
        self.photo = ImageTk.PhotoImage(self.image)

    def update_image(self):
        # Carica la nuova immagine e aggiorna il canvas
        self.load_image(self.slides[self.current_slide_index])
        self.canvas.itemconfig(self.image_on_canvas, image=self.photo)
        self.canvas.image = self.photo

    def update_buttons(self):
        # Rimuove i pulsanti attuali dal canvas
        self.canvas.delete("button")
        if self.current_slide_index == 0:
            # Visualizza i pulsanti Inizia Tutorial e Salta Tutorial
            self.canvas.create_window(self.image.width - 50, self.image.height - 50, anchor=tk.SE, window=self.button_start, tags="button")
            self.canvas.create_window(50, self.image.height - 50, anchor=tk.SW, window=self.button_skip, tags="button")
        else:
            if self.current_slide_index > 1 and self.current_slide_index < 5:
                self.canvas.create_window(1000, self.image.height - 50, anchor=tk.SW, window=self.button_previous, tags="button")
            if self.current_slide_index < len(self.slides) - 1:
                self.canvas.create_window(self.image.width - 50, self.image.height - 50, anchor=tk.SE, window=self.button_next, tags="button")
            if self.current_slide_index < len(self.slides) - 1:
                self.canvas.create_window(50, self.image.height - 50, anchor=tk.SW, window=self.button_skip, tags="button")

            if self.current_slide_index==5:
                self.canvas.create_window(825, self.image.height - 350, anchor=tk.SW, window=self.button_select, tags="button")

    def skip_tutorial(self):
        print("Skip Tutorial clicked")
        # Salta all'ultima slide
        self.current_slide_index = len(self.slides) - 1
        self.update_image()
        self.update_buttons()

    def start_tutorial(self):
        print("Start Tutorial clicked")
        # Inizia il tutorial dalla seconda slide
        self.current_slide_index = 1
        self.update_image()
        self.update_buttons()

    def next_gesture(self):
        if self.current_slide_index < len(self.slides) - 1:
            # Vai alla slide successiva
            self.current_slide_index += 1
            self.update_image()
            self.update_buttons()

    def previous_gesture(self):
        if self.current_slide_index > 0:
            # Vai alla slide precedente
            self.current_slide_index -= 1
            self.update_image()
            self.update_buttons()

root = tk.Tk()
app = InteractivePowerPoint(root)
root.mainloop()
root.destroy()