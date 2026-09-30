# Benodigde modules importeren.
import tkinter as tk
from tkinter       import Frame, ttk
import math

# Grootte van het plaatje vaststellen.
BREEDTE = 400
HOOGTE = 400

# Voorbeeldplaatjes voor de gebruiker (presets)
voorbeelden = {
    "Basisplaatje": (0, 0, 0.01, 100),
    "Zeepaardjes [1]": (-0.75, 0.1, 0.001, 200),
    "Zeepaardjes [2]": (-0.7436, 0.1318, 0.0002, 300),
    "Dubbele spiraal": (-0.7463, 0.1102, 0.00003, 300),
    "Olifantenvallei": (0.28, 0, 0.0005, 200),
}

def FindMandelgetal(x, y, maximum): # Geeft het mandelgetal van (x, y), of 0 als het oneindig is.
    a = 0
    b = 0
    for aantal in range(1, maximum + 1):
        nieuwe_a = a * a - b * b + x
        nieuwe_b = 2 * a * b + y
        a = nieuwe_a
        b = nieuwe_b
        if a * a + b * b > 4:      # afstand tot (0,0) is groter dan 2, sneller dan math.sqrt(x, y) gebruiken.
            return aantal
    return 0

def kleur(getal, kleurschema): # Geeft de kleur corresponderend met een kleurschema aan de hand van het mandelgetal.
    if getal == 0: # Oneindig -> zwart in elk kleurschema
        return "#000000"

    if kleurschema == "zwart-wit": # Kleurschema 1: zwart-wit
        if getal % 2 == 0:
            return "#000000"
        else:
            return "#ffffff"

    if kleurschema == "RGB": # Kleurschema 2: RGB 
        rood = int(127 * (1 + math.sin(getal * 0.11))) # Elke kleurcomponent volgt een eigen sinusgolf met verschillende snelheden en verschuivingen.
        groen = int(127 * (1 + math.sin(getal * 0.07 + 2))) # Formule resulteert in een getal tussen 0 en 254.
        blauw = int(127 * (1 + math.sin(getal * 0.05 + 4)))
        return "#%02x%02x%02x" % (rood, groen, blauw)

    stap = abs(getal % 60 - 30) / 30 # Kleurschema 3: Blauw-Geel
    rood = int(255 * stap)
    groen = int(200 * stap)
    blauw = int(255 * (1 - stap))
    return "#%02x%02x%02x" % (rood, groen, blauw)

def teken(): # functie voor het lezen van invoervelden -> tekent daarna rij voor rij het plaatje.
    x_midden = float(veld_x.get())
    y_midden = float(veld_y.get())
    schaal = float(veld_schaal.get())
    maximum = int(veld_max.get())
    kleurschema = kleurkeuze.get()

    for py in range(HOOGTE):
        rij = ""
        for px in range(BREEDTE):
            x = x_midden + (px - BREEDTE / 2) * schaal
            y = y_midden - (py - HOOGTE / 2) * schaal
            getal = FindMandelgetal(x, y, maximum)
            rij = rij + kleur(getal, kleurschema) + " "
        plaatje.put("{" + rij + "}", to=(0, py))
    scherm.update()


def vul_velden(x, y, schaal, maximum): # Zet waardes in de vier invoervelden. 
    for veld, waarde in [(veld_x, x), (veld_y, y), (veld_schaal, schaal), (veld_max, maximum)]:
        veld.delete(0, tk.END)
        veld.insert(0, str(waarde))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

def kies_voorbeeld(event): # Functie die wordt aangeroepen als de gebruiker een voorbeeldplaatje kiest.
    x, y, schaal, maximum = voorbeelden[voorbeeldkeuze.get()]
    vul_velden(x, y, schaal, maximum)
    teken()

def zoom(event, factor): # Zoomt in (factor 0.5) of uit (factor 2) op het aangeklikte punt.
    x_midden = float(veld_x.get())
    y_midden = float(veld_y.get())
    schaal = float(veld_schaal.get())
    nieuwe_x = x_midden + (event.x - BREEDTE / 2) * schaal
    nieuwe_y = y_midden - (event.y - HOOGTE / 2) * schaal
    vul_velden(nieuwe_x, nieuwe_y, schaal * factor, veld_max.get())
    teken()

def zoom_in(event): # Voor inzoomen d.m.v. linkermuisknop.
    zoom(event, 0.5)


def zoom_uit(event): # Voor uitzoomen d.m.v. rechtermuisknop.
    zoom(event, 2)


# Opbouw van het venster.
scherm = Frame()
scherm.master.title("Mandelbrot")
scherm.configure(background="lightblue")
scherm.pack()


# Opbouwing en indeling van labels & invoervelden.
tk.Label(scherm, text="midden x:").grid(row=0, column=0)
tk.Label(scherm, text="midden y:").grid(row=1, column=0)
tk.Label(scherm, text="schaal:").grid(row=2, column=0)
tk.Label(scherm, text="max aantal:").grid(row=3, column=0)
veld_x = tk.Entry(scherm)
veld_y = tk.Entry(scherm)
veld_schaal = tk.Entry(scherm)
veld_max = tk.Entry(scherm)
veld_x.grid(row=0, column=1)
veld_y.grid(row=1, column=1)
veld_schaal.grid(row=2, column=1)
veld_max.grid(row=3, column=1)
tk.Button(scherm, text="Go!", command=teken).grid(row=3, column=2)

# Keuzelijst met voorbeeldplaatjes.
tk.Label(scherm, text="voorbeeld:").grid(row=4, column=0)
voorbeeldkeuze = ttk.Combobox(scherm, values=list(voorbeelden), state="readonly")
voorbeeldkeuze.grid(row=4, column=1)
voorbeeldkeuze.bind("<<ComboboxSelected>>", kies_voorbeeld)

# Radiobuttons voor de kleuren.
kleurkeuze = tk.StringVar(value="RGB")
tk.Radiobutton(scherm, text="zwart-wit", variable=kleurkeuze, value="zwart-wit", command=teken).grid(row=5, column=0)
tk.Radiobutton(scherm, text="RGB", variable=kleurkeuze, value="RGB", command=teken).grid(row=5, column=1)
tk.Radiobutton(scherm, text="blauw-geel", variable=kleurkeuze, value="blauw-geel", command=teken).grid(row=5, column=2)

# Plaatje opzetten waarin Mandelbrot-figuur in wordt getekend. 
# Canvas zodat muisklikken opgevangen kunnen worden.
plaatje = tk.PhotoImage(width=BREEDTE, height=HOOGTE)
canvas = tk.Canvas(scherm, width=BREEDTE, height=HOOGTE)
canvas.grid(row=6, column=0, columnspan=3)
canvas.create_image(0, 0, image=plaatje, anchor="nw")
canvas.bind("<Button-1>", zoom_in)   # linkermuisknop
canvas.bind("<Button-3>", zoom_uit)  # rechtermuisknop
 
# Bij opstarten basisplaatje laten zien als default.
voorbeeldkeuze.set("Basisplaatje")
vul_velden(0, 0, 0.01, 100)
teken()

# Programma zal blijven runnen en wacht op input van de gebruiker. 
scherm.mainloop()

