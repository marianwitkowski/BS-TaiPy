from taipy import Gui
import taipy.gui.builder as tgb

title="Aplikacja"
content = """
# Aplikacja testowa
Witaj <|{title}|>! Jestem **pogrubiony** i jestem *kursywa*!
"""

#Gui(page=content).run(debug=True, port=1234, dark_mode=False, use_reloader=True)

text = "Hello world"
with tgb.Page() as page:
    tgb.text("# Getting started with Taipy GUI", mode="md")
    tgb.text("Mój tekst: {text}")
    tgb.input("{text}")
#Gui(page).run(debug=True, port=1234, dark_mode=False, use_reloader=True)

### Tylko z wykorzystaniem znacznikow markdown
page = """
# Getting started with Taipy GUI

My text: <|{text}|>

<|{text}|input|>
"""
Gui(page).run(debug=True, port=1234, dark_mode=False, use_reloader=True)
