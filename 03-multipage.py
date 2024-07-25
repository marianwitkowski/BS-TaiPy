from taipy import Gui

# Treść dla poszczególnych stron
root_md = "# Aplikacja wielostronicowa"
page1_md = "## To jest strona 1"
page2_md = "## To jest strona 2"

# Słownik mapujący ścieżki URL do treści stron
pages = {
    "/": root_md,      # Strona główna
    "page1": page1_md, # Strona 1
    "page2": page2_md  # Strona 2
}

# Uruchomienie aplikacji z określonymi stronami
Gui(pages=pages).run()