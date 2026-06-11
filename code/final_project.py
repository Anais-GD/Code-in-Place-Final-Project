
"""
Anaïs Galvañ final's project Stanford Code in Place

According to the International Plant Protection Convention (IPPC), a quarantine plant pest is defined as a species that is invasive and not present or widely distributed in an area that can potentially cause severe economic losses and, for this reason, is officially controlled (Schrader and Unger, 2003).

Following this definition, in this work, I will refer with 'pest' to any plant pathogen or arthropod to facilitate the reading.

Plant pests represent a growing threat to both global food production and ecosystem stability, with outbreaks resulting in losses of primary productivity and biodiversity that negatively impact both environmental conditions and socio-economic outcomes in affected regions (FAO, 2021; Singh et al. 2023, Galvañ-Domenech, 2025).

Climate change will exacerbate this situation by altering the evolutionary mechanisms of pathogens and favoring the emergence of new strains, thereby amplifying the risk of disease outbreaks in crops, forests, and other wild vegetation (FAO, 2021; Singh et al. 2023). As outlined above, the consequences of a pest or pathogen entering a new area can be devastating not only economically but also socially, as illustrated by cases such as citrus canker in Florida or Xylella fastidiosa in Spain and Italy (Galvañ-Domenech,2025). Early and accurate detection of these pests is therefore critical to alert the relevant authorities and implement control measures swiftly to ensure eradication.

In Europe, plant health is governed by a phytosanitary regulatory framework that, among other things, classifies pests into quarantine and non-quarantine categories. Quarantine pests are those not yet established in a given territory, or present only in limited areas, whereas non-quarantine pests are those already established. Within quarantine pests, a specific subset is designated as 'priority pests' due to their particularly severe social, environmental, and economic consequences (Galvañ-Domenech, 2025).

It is within this regulatory context that this project proposes a game based on European phytosanitary legislation, in which players must first identify a given crop and then attempt to identify its associated quarantine pests and pathogens.

#Bibliography

Domenech, A. G. (2025). Prevention strategies against citrus black spot and Huanglongbing in the Mediterranean Basin [Doctoral dissertation, Universitat Politècnica de València]. https://riunet.upv.es/entities/publication/dbf6e398-c698-4ac8-b3af-d5e68fe2ed0a.

Singh, B. K., Delgado-Baquerizo, M., Egidi, E., Guirado, E., Leach, J. E., Liu, H., & Trivedi, P. (2023). Climate change impacts on plant pathogens, food security and paths forward. Nature Reviews Microbiology, 21(10), 640-656. https://doi.org/10.1038/s41579-023-00900-7

Food and Agriculture Organization of the United Nations (FAO). (2021, June 2). Climate change will increase the risk of pest spread, which already destroys 40% of crop production. UN News. https://news.un.org/es/story/2021/06/1492762
"""

import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import urllib.parse
import io
import random

# Base URL for raw images on the GitHub project
BASE_URL = "https://raw.githubusercontent.com/Anais-GD/Code-in-Place-Final-Project/main/pics/"

# Pest database
# Format: key -> (scientific_name, common_name, crops, [image_filenames])
PESTS = {
    "bactrocera_dorsalis": (
        "Bactrocera dorsalis",
        "Oriental fruit fly",
        "mango tree, citrus tree, papaya",
        ["Bactrocera dorsalis.png"]
    ),
    "xylella_fastidiosa": (
        "Xylella fastidiosa",
        "xylella",
        "olive tree, almond tree, vine, citrus tree, etc. more than 300 hosts",
        ["xylella_fastidiosa_1.png"]
    ),
    "agrilus_planipennis": (
        "Agrilus planipennis",
        "emerald ash borer",
        "ash tree, white Fringetree",
        ["Agrilus planipennis.png",
         "Agrilus planipennis_2.png"]
    ),
    "agrilus_anxius": (
        "Agrilus anxius",
        "bronze birch borer",
        "birch tree",
        ["Agrilus anxius.png"]
    ),
    "anastrapha_ludens": (
        "Anastrepha ludens",
        "Mexican fruit fly",
        "citrus tree, mango tree, peach",
        ["Anastrepha ludens.png"]
    ),
    "anoplophora_glabripennis": (
        "Anoplophora glabripennis",
        ["Asian long-horned beetle", "asian beetle"],
        "maple tree, elm, willow, poplar",
        ["anoplophora_glabripennis.png"]
    ),
    "phyllosticta_citricarpa": (
        "Phyllosticta citricarpa",
        ["citrus black spot", 'CBS'],
        "citrus spp.",
        ["Phyllosticta citricarpa.png"]
    ),
}

# funcion para descargar y cargar las imágenes

def normalize(text):
    return text.strip().lower()

def load_image_from_url(filename):
    """Download image from GitHub and return a PIL Image."""
    url = BASE_URL + urllib.parse.quote(filename)
    with urllib.request.urlopen(url) as response:
        data = response.read()
    return Image.open(io.BytesIO(data))

# app principal

class PlantHealthQuiz:
    def __init__(self, root):
        self.root = root
        self.root.title("Plant Health Quiz")
        self.root.resizable(False, False)
        self.pest_list = list(PESTS.items())
        random.shuffle(self.pest_list)
        self.current = 0
        self.correct = 0
        self.total = len(self.pest_list)
        self.photo = None
        self._show_welcome()

    # pantalla de bienvenida, inicio
    def _show_welcome(self):
        BG = "#f5f5f0"
        self.root.configure(bg=BG)

        # Top bar
        top = tk.Frame(self.root, bg="#2d6a4f")
        top.pack(fill="x")
        tk.Label(top, text="PLANT HEALTH QUIZ", font=("Arial", 14, "bold"),
                 bg="#ef6f6c", fg="white", pady=8).pack()

        # Main welcome text
        tk.Label(self.root, text="Let's play the Plant Health Quiz!\n"
        "This game is designed to raise awareness about the European Union's priority pests and pathogens.\n"
        "It's still in beta, but it could become a great game in the future.\n "
        "Thanks for playing!",
                 font=("Arial", 11, "bold"), bg=BG, fg="#2d6a4f").pack(pady=(24, 8))

        intro = (
            "Every year, quarantine pests destroy crops, forests and ecosystems worldwide.\n"
            "Climate change is making things worse, new pests are spreading faster than ever.\n\n"
            "Under European phytosanitary law, some pests are classified as 'priority pests'\n"
            "because of their severe economic, social and environmental impact.\n\n"
            "Can you identify them?"
        )
        tk.Label(self.root, text=intro,
                 font=("Arial", 10), bg=BG, fg="#333",
                 justify="center", wraplength=460).pack(pady=(0, 20))

        # Rules box
        rules_frame = tk.Frame(self.root, bg="#e8f5e9", bd=1, relief="solid")
        rules_frame.pack(padx=40, pady=(0, 20), fill="x")
        tk.Label(rules_frame,
                 text=" HOW TO PLAY\n\n"
                      "• You will see a photo of a quarantine pest\n"
                      "• Type its scientific name or common name\n"
                      "• Press Submit or hit Enter\n"
                      f"• {self.total} pests in total, how many can you get right?",
                 font=("Arial", 10), bg="#e8f5e9", fg="#1b4332",
                 justify="left", padx=16, pady=12).pack()

        # Start button
        tk.Button(self.root, text=" Start quiz",
                  font=("Arial", 12, "bold"),
                  bg="#2d6a4f", fg="white", activebackground="#1b4332",
                  relief="flat", padx=24, pady=8,
                  command=self._start_quiz).pack(pady=(0, 30))

    def _start_quiz(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self._build_ui()
        self._load_question()

    #  Quiz UI 

    def _build_ui(self):
        BG = "#f5f5f0"
        self.root.configure(bg=BG)

        # Top bar
        top = tk.Frame(self.root, bg="#2d6a4f")
        top.pack(fill="x")
        tk.Label(top, text="PLANT HEALTH QUIZ! :D", font=("Arial", 16, "bold"),
                 bg="#2d6a4f", fg="white", pady=8).pack()

        # Counter
        self.counter_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.counter_var,
                 font=("Arial", 11), bg=BG, fg="#555").pack(pady=(8, 0))

        # Image
        self.img_label = tk.Label(self.root, bg=BG)
        self.img_label.pack(pady=8)

        # Answer
        tk.Label(self.root, text="Which pest is this?",
                 font=("Arial", 12), bg=BG).pack()
        tk.Label(self.root, text="(scientific name or common name)",
                 font=("Arial", 9), bg=BG, fg="#888").pack()

        self.answer_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.answer_var,
                              font=("Arial", 13), width=36, relief="solid", bd=1)
        self.entry.pack(pady=6)
        self.entry.bind("<Return>", lambda e: self._check_answer())
        self.entry.focus()

        # Submit button
        tk.Button(self.root, text="Submit answer",
                  font=("Arial", 11, "bold"),
                  bg="#2d6a4f", fg="white", activebackground="#1b4332",
                  relief="flat", padx=16, pady=6,
                  command=self._check_answer).pack(pady=4)

        # Feedback
        self.feedback_var = tk.StringVar()
        self.feedback_label = tk.Label(self.root, textvariable=self.feedback_var,
                                       font=("Arial", 11), bg=BG,
                                       wraplength=480, justify="center")
        self.feedback_label.pack(pady=4)

        # Next button (hidden until answer submitted)
        self.next_btn = tk.Button(self.root, text="Next ▶",
                                  font=("Arial", 11, "bold"),
                                  bg="#457b9d", fg="white", activebackground="#1d3557",
                                  relief="flat", padx=16, pady=6,
                                  command=self._next_question)

    def _load_question(self):
        if self.current >= self.total:
            self._show_final()
            return

        self.counter_var.set(f"Pest {self.current + 1} of {self.total}")
        self.feedback_var.set("")
        self.answer_var.set("")
        self.next_btn.pack_forget()
        self.entry.config(state="normal")
        self.entry.focus()

        _, (scientific_name, common_name, crops, images) = self.pest_list[self.current]
        filename = random.choice(images)

        self.img_label.config(image="", text="Loading image...", font=("Arial", 11), fg="#555")
        self.root.update()

        try:
            img = load_image_from_url(filename)
            img.thumbnail((500, 340))
            self.photo = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.photo, text="")
        except Exception:
            self.img_label.config(image="",
                                  text=f"[Could not load image: {filename}]",
                                  font=("Arial", 10), fg="red")

    def _check_answer(self):
        _, (scientific_name, common_name, crops, _) = self.pest_list[self.current]
        answer = self.answer_var.get()
        if not answer.strip():
            return

        # common_name can be a string or a list of accepted names
        if isinstance(common_name, list):
            common_names = common_name
        else:
            common_names = [common_name]

        is_correct = (
            normalize(answer) == normalize(scientific_name) or
            any(normalize(answer) == normalize(name) for name in common_names)
        )

        self.entry.config(state="disabled")

        # display_name: first common name for the feedback message
        display_name = common_names[0]

        if is_correct:
            self.correct += 1
            self.feedback_var.set(f"Correct! It is {scientific_name}")
            self.feedback_label.config(fg="#1b4332")
        else:
            self.feedback_var.set(
                f"No :( it is {scientific_name} ({display_name})\n"
                f"Priority pest affecting: {crops}"
            )
            self.feedback_label.config(fg="#9b2226")

        self.next_btn.pack(pady=(2, 10))

    def _next_question(self):
        self.current += 1
        self._load_question()

    #  Final screen 

    def _show_final(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        BG = "#f5f5f0"
        self.root.configure(bg=BG)

        tk.Label(self.root, text="PLANT HEALTH QUIZ", font=("Arial", 16, "bold"),
                 bg="#2d6a4f", fg="white", pady=8).pack(fill="x")
        tk.Label(self.root, text="Game over!", font=("Arial", 22, "bold"),
                 bg=BG, fg="#b6174b").pack(pady=(40, 10))
        tk.Label(self.root, text=f"You got {self.correct} of {self.total} correct",
                 font=("Arial", 16), bg=BG).pack(pady=6)

        if self.correct == self.total:
            msg, color = "Brilliant! You're an expert in plant health!", "#553555"
        elif self.correct >= self.total // 2:
            msg, color = "Well done! Keep studying quarantine pests.", "#553555"
        else:
            msg, color = "Try again! You'll get there!", "#553555"

        tk.Label(self.root, text=msg, font=("Arial", 13), bg=BG, fg=color).pack(pady=10)

        tk.Button(self.root, text="Play again",
                  font=("Arial", 11, "bold"),
                  bg="#2d6a4f", fg="white", relief="flat", padx=16, pady=6,
                  command=self._restart).pack(pady=20)

    def _restart(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.pest_list = list(PESTS.items())
        random.shuffle(self.pest_list)
        self.current = 0
        self.correct = 0
        self.photo = None
        self._show_welcome()


def main():
    root = tk.Tk()
    PlantHealthQuiz(root)
    root.mainloop()


if __name__ == "__main__":
    main()
