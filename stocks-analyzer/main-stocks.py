from taipy.gui import Gui, notify
from datetime import date
import yfinance as yf
from prophet import Prophet
import pandas as pd
import taipy.gui.builder as tgb
from plotly import graph_objects as go

# Parametry do pobierania danych giełdowych
start_date = "2020-01-01"
end_date = date.today().strftime("%Y-%m-%d")
selected_stock = 'AAPL'
n_years = 1

# Funkcja pobierająca dane giełdowe
def get_stock_data(ticker, start, end):
    ticker_data = yf.download(ticker, start, end)  # Pobieranie danych giełdowych od start do end
    ticker_data.reset_index(inplace=True)  # Umieszczenie daty w pierwszej kolumnie
    ticker_data['Date'] = pd.to_datetime(ticker_data['Date']).dt.tz_localize(None)
    return ticker_data


# Funkcja pobierająca dane w wybranym zakresie
def get_data_from_range(state):
    start_date = state.start_date if type(state.start_date) == str else state.start_date.strftime("%Y-%m-%d")
    end_date = state.end_date if type(state.end_date) == str else state.end_date.strftime("%Y-%m-%d")

    state.data = get_stock_data(state.selected_stock, start_date, end_date)
    if len(state.data) == 0:
        notify(state, "error", f"Nie można pobrać danych {state.selected_stock} od {start_date} do {end_date}")
        return
    notify(state, 's', 'Dane historyczne zostały zaktualizowane!')
    notify(state, 'w', 'Usuwanie poprzednich prognoz...')
    state.forecast = pd.DataFrame(columns=['Date', 'Lower', 'Upper'])


# Funkcja tworząca wykres świecowy
def create_candlestick_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Date'],
                                 open=data['Open'],
                                 high=data['High'],
                                 low=data['Low'],
                                 close=data['Close'],
                                 name='Candlestick'))
    fig.update_layout(margin=dict(l=30, r=30, b=30, t=30), xaxis_rangeslider_visible=False)
    return fig


# Funkcja generująca dane prognoz
def generate_forecast_data(data, n_years):
    # PROGNOZOWANIE
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})  # Format akceptowany przez Prophet

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=n_years * 365)
    fc = m.predict(future)[['ds', 'yhat_lower', 'yhat_upper']].rename(
        columns={"ds": "Date", "yhat_lower": "Lower", "yhat_upper": "Upper"})
    print("Proces zakończony!")
    return fc


# Funkcja wyświetlająca prognozę
def forecast_display(state):
    notify(state, 'i', 'Prognozowanie...')
    state.forecast = generate_forecast_data(state.data, state.n_years)
    notify(state, 's', 'Prognoza zakończona! Dane prognozy zostały zaktualizowane!')

# Funkcja wyświetlająca pesymistyczną prognozę
def pessimistic_forecast_display(forecast, data):
    if len(forecast) == 0 or len(data) == 0:
        return -1
    return int((forecast.loc[len(forecast) - 1, 'Lower'] - forecast.loc[len(data), 'Lower']) / forecast.loc[
        len(data), 'Lower'] * 100)

# Funkcja wyświetlająca optymistyczną prognozę
def optimistic_forecast_display(forecast, data):
    if len(forecast) == 0 or len(data) == 0:
        return -1
    return int((forecast.loc[len(forecast) - 1, 'Upper'] - forecast.loc[len(data), 'Upper']) / forecast.loc[
        len(data), 'Upper'] * 100)

#### Pobieranie danych, tworzenie początkowej prognozy i budowanie interfejsu webowego za pomocą Taipy GUI
data = get_stock_data(selected_stock, start_date, end_date)
forecast = generate_forecast_data(data, n_years)

show_dialog = False

partial_md = "<|{forecast}|table|>"
dialog_md = "<|{show_dialog}|dialog|partial={partial}|title=Dane Prognozy|on_action={lambda state: state.assign('show_dialog', False)}|>"

with tgb.Page() as page:
    tgb.toggle(theme=True)

    tgb.dialog("{show_dialog}",
               partial="{partial}",
               title="Dane Prognozy",
               on_action="{lambda state: state.assign('show_dialog', False)}")

    with tgb.part("container"):
        tgb.text("# Dashboard Analizy Cen Akcji", mode="md")
        with tgb.layout("1 2 1", gap="40px", class_name="card"):
            with tgb.part():
                tgb.text("#### Wybrany Okres", mode="md")
                tgb.text("Od:")
                tgb.date("{start_date}", on_change=get_data_from_range)
                tgb.html("br")
                tgb.text("Do:")
                tgb.date("{end_date}", on_change=get_data_from_range)
            with tgb.part():
                tgb.text("#### Wybrany Ticker", mode="md")
                tgb.input(value="{selected_stock}", label="Akcja", on_action=get_data_from_range)
                tgb.html("br")

                tgb.text("lub wybierz popularny ticker")
                lov = ["MSFT", "GOOG", "AAPL", "AMZN", "META", "COIN", "AMC", "PYPL"]
                tgb.toggle(value="{selected_stock}", lov=lov, on_change=get_data_from_range)
            with tgb.part():
                tgb.text("#### Lata Prognozy", mode="md")
                tgb.text("Wybierz liczbę lat prognozy: {n_years}")
                tgb.html("br")
                tgb.slider("{n_years}", min=1, max=5)

                tgb.button("Prognozuj", on_action=forecast_display, class_name="{'plain' if len(forecast)==0 else ''}")

        tgb.html("br")

        tgb.chart(figure="{create_candlestick_chart(data)}")

        with tgb.expandable(title="Dane Historyczne", value="Dane Historyczne", expanded=False):
            with tgb.layout("1 1"):
                with tgb.part():
                    tgb.text("### Historyczne Ceny Zamknięcia", mode="md")
                    tgb.chart("{data}", mode="line", x="Date", y__1="Open", y__2="Close")

                with tgb.part():
                    tgb.text("### Historyczny Wolumen Dziennego Handlu", mode="md")
                    tgb.chart("{data}", mode="line", x="Date", y="Volume")

            tgb.text("### Całe Historyczne Dane {selected_stock}", mode="md")
            tgb.table("{data}")

        tgb.text("### Dane Prognozy", mode="md")

        with tgb.layout("1 1", class_name="text-center"):
            tgb.text("Pesymistyczna Prognoza {pessimistic_forecast_display(forecast, data)}%", class_name="h4 card", )
            tgb.text("Optymistyczna Prognoza {optimistic_forecast_display(forecast, data)}%", class_name="h4 card")

        tgb.chart("{forecast}", mode="line", x="Date", y__1="Lower", y__2="Upper")

        tgb.html("br")

        with tgb.part("text-center"):
            tgb.button("Więcej informacji", on_action="{lambda s: s.assign('show_dialog', True)}")

# Uruchomienie Taipy GUI
gui = Gui(page)
partial = gui.add_partial(partial_md)
gui.run(dark_mode=False, title="Wizualizacja Akcji", port=3002)