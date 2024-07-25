from taipy.gui import Gui, notify
import taipy.gui.builder as tgb

def on_button_click(state):
    notify(state, "info", f"ABCD: {state.text}")
    notify(state, "error", f"ABCD: {state.text}")
    state.text = "Przycisk wcisniety"

text = "Tekst oryginalny"
with tgb.Page() as page:
    tgb.html("h1", "Aplikacja z przyciskiem")
    tgb.text("Mój tekst: {text}")
    tgb.input("{text}")
    tgb.button("Kliknij", on_action=on_button_click)

Gui(page).run(debug=True, port=1234)
