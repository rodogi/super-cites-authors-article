import requests
import multiprocessing as mp
import pandas as pd


def gender(name):
    params['name'] = name
    res = requests.get(url, params=params)

    return [res.json()[k] for k in header]


if __name__ == '__main__':
    with open('/home/rdora/femec/data/unique_names.txt') as f:
        names = f.read().splitlines()
    url = "https://genderapi.io/api/"
    key = "5ebaf057756fae39f5000db2"
    params = {'key': key}
    header = ['name', 'q', 'gender', 'total_names', 'probability', 'country']

    with mp.Pool(40) as pool:
        data = pool.map(gender, names)
    df = pd.DataFrame(data, columns=header)
    df.to_csv('/home/rdora/femec/data/gender.csv', index=False)
