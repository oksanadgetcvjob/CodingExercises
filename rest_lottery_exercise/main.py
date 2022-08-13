from fastapi import FastAPI
import pandas as pd
from collections import Counter

df = pd.read_csv('input/powerball_winning_numbers copy.csv', parse_dates=[0])
df['set of winning numbers'] = df['Winning Numbers'].apply(lambda x: set(int(i) for i in x.split()))
df['sum of winning numbers'] = df['set of winning numbers'].apply(lambda x: sum(x))
df['year'] = pd.DatetimeIndex(df['Draw Date']).year
df['month'] = pd.DatetimeIndex(df['Draw Date']).month


app = FastAPI()


@app.get("/")
async def root():
    return df.to_json()


@app.get("/multiplier/{multiplier}")
async def root(multiplier: int):
    df_actual = df[df['Multiplier'] == multiplier]
    return df_actual.to_csv(index=False, columns=['Draw Date', 'Winning Numbers', 'Multiplier'])


def get_date_range(start, end):
    return df.loc[(df['Draw Date'] >= start) & (df['Draw Date'] <= end)]


def get_numbers_date(start, end):
    df_actual = get_date_range(start,end)
    return df_actual.to_csv(index=False, columns=['Draw Date', 'Winning Numbers'])


@app.get("/date/{start}")
async def root(start):
    return get_numbers_date(start, start)


@app.get("/date/{start}/{end}")
async def root(start, end):
    return get_numbers_date(start, end)



@app.get("/max_sum/{start}/{end}")
async def root(start, end):
    df_actual = get_date_range(start, end)
    return df_actual[df_actual['sum of winning numbers'] == max(df_actual['sum of winning numbers'])]['Draw Date']


@app.get("/win/{start}/{end}/{ticket_str}")
async def root(start, end, ticket_str):
    df_actual = get_date_range(start, end)
    ticket = set(int(i) for i in ticket_str.split())
    return [row['Draw Date'] for index, row in df_actual.iterrows() if len(ticket.intersection(row['set of winning numbers'])) > 3]


@app.get("/frequent_nums/{start}/{end}")
async def root(start, end):
    df_actual = get_date_range(start, end)
    all_numbers_counter = Counter()
    for el in df_actual['set of winning numbers']:
        all_numbers_counter.update(el)
    return list(i[0] for i in sorted(all_numbers_counter.items(), key=lambda x: x[1], reverse=True))[:6]


@app.get("/aaa/{mon}/{yea}")
async def root(mon: int, yea: int):
    df_sample = df.loc[(df['year'] == yea) & (df['month'] == mon)]
    return df_sample['Multiplier'].mean()
