import taipy.gui.builder as tgb
from taipy import Gui
import datetime

# Przykładowe dane
text = "Oryginalny tekst"
toogle_val = "Element 1"
date = datetime.datetime(2024, 7, 14, 17, 5, 12)
value = 123

# Zakres wartości dla osi X
x_range = range(-10, 11, 4)
# Dane do tabeli
table_data = {
    "x": x_range,
    "y1": [x*x for x in x_range],
    "y2": [100-x*x for x in x_range]
}

with tgb.Page() as page:
    tgb.text("# Aplikacja Taipy", mode="md")
    tgb.text("Mój tekst: {text}")
    tgb.number("{value}")
    tgb.slider(value=50, min=1, max=100, labels={1:"Niski",100:"Wysoki"})
    tgb.toggle("{toogle_val", lov="Element 1;Element 2;Element 3")
    tgb.date("{date}")
    tgb.table("{table_data}")

# Uruchomienie aplikacji z debugowaniem i automatycznym przeładowywaniem
Gui(page).run(debug=True, port=1234, use_reloader=True, watermark="BlueSoft", dark_mode=False)