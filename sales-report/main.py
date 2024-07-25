import pandas as pd
from taipy.gui import Gui, notify

df = pd.read_excel(
    io="data/supermarkt_sales.xlsx",
    engine="openpyxl",
    sheet_name="Sales",
    skiprows=3,
    usecols="B:R",
    nrows=1000,
)
df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour


city = cities = list(df["City"].unique())
customer_type = types = list(df["Customer_type"].unique())
gender = genders = list(df["Gender"].unique())

layout = {"margin": {"l": 220}}

page = """
<|toggle|theme|>

<|25 75|layout|gap=30px|
<|sidebar|
## Proszę **filtruj**{: .color-primary} tutaj:

<|{city}|selector|lov={cities}|multiple|label=Wybierz miasto|dropdown|on_change=on_filter|class_name=fullwidth|>

<|{customer_type}|selector|lov={types}|multiple|label=Wybierz typ klienta|dropdown|on_change=on_filter|class_name=fullwidth|>

<|{gender}|selector|lov={genders}|multiple|label=Wybierz płeć|dropdown|on_change=on_filter|class_name=fullwidth|>
|>

<main_page|
# 📊 **Panel sprzedaży**{: .color-primary}

<|1 1 1|layout|
<total_sales|
## **Całkowita**{: .color-primary} sprzedaż:
US $ <|{int(df_selection["Total"].sum())}|>
|total_sales>

<average_rating|
## Średnia **ocena**{: .color-primary}:
<|{round(df_selection["Rating"].mean(), 1)}|> <|{"⭐" * int(round(round(df_selection["Rating"].mean(), 1), 0))}|>
|average_rating>

<average_sale|
## Średnia **sprzedaż**{: .color-primary}:
US $ <|{round(df_selection["Total"].mean(), 2)}|>
|average_sale>
|>

<br/>

<|Tabela sprzedaży|expandable|expanded|
<|{df_selection}|table|page_size=5|>
|>

<|card p2|
<|{sales_by_hour}|chart|x=Hour|y=Total|type=bar|title=Sprzedaż według godzin|>

<|{sales_by_product_line}|chart|x=Total|y=Product line|type=bar|orientation=h|title=Sprzedaż według produktu|layout={layout}|>
|>

|main_page>
|>

"""


def filter(city, customer_type, gender):
    df_selection = df[
        df["City"].isin(city)
        & df["Customer_type"].isin(customer_type)
        & df["Gender"].isin(gender)
        ]

    # SALES BY PRODUCT LINE [BAR CHART]
    sales_by_product_line = (
        df_selection[["Product line", "Total"]]
        .groupby(by=["Product line"])
        .sum()[["Total"]]
        .sort_values(by="Total")
    )
    sales_by_product_line["Product line"] = sales_by_product_line.index

    # SALES BY HOUR [BAR CHART]
    sales_by_hour = (
        df_selection[["Hour", "Total"]].groupby(by=["Hour"]).sum()[["Total"]]
    )
    sales_by_hour["Hour"] = sales_by_hour.index
    return df_selection, sales_by_product_line, sales_by_hour


def on_filter(state):
    if len(state.city) == 0 or len(state.customer_type) == 0 or len(state.gender) == 0:
        notify(state, "Error", "Brak wyników. Sprawdź filtry.")
        return

    state.df_selection, state.sales_by_product_line, state.sales_by_hour = filter(
        state.city, state.customer_type, state.gender
    )


if __name__ == "__main__":
    df_selection, sales_by_product_line, sales_by_hour = filter(
        city, customer_type, gender
    )
    Gui(page).run(margin="0em", title="Panel sprzedaży", use_reloader=True, port=4321, dark_mode=False)
