from taipy.gui import Gui

# Definicja układu strony w Markdown
md = """
# Układy
<|layout.start|columns=1 6|>
To jest lewy panel.
<|
Treść tutaj.
Muszę owinąć te elementy w część, ponieważ zajmują wiele linii.
|>
<|layout.end|>
"""

# Uruchomienie aplikacji z zadanym układem strony
Gui(page=md).run(dark_mode=False)
