import random
import pandas as pd
from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET'])
def random_city():
    num = random.randrange(0, 30408)
    df = pd.read_csv('uscities.csv', index_col=0)
    city = df.iat[num, 0]
    return city


if __name__ == "__main__":
    app.run(debug=True, port=5001)