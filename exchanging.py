from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests
import time

app = Flask(__name__)

# Kullanıcıya sunulacak döviz birimleri
CURRENCY_LIST = ['USD', 'EUR', 'TRY', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK']

def get_currency(in_currency, out_currency, amount):
    url = f'https://www.x-rates.com/calculator/?from={in_currency}&to={out_currency}&amount={amount}'
    try:
        content = requests.get(url).text
        soup = BeautifulSoup(content, 'html.parser')

        
        rate = soup.find("span", class_="ccOutputRslt").get_text()
        return rate
    except Exception as e:
        raise ValueError(f"Error fetching currency data: {e}")

@app.route('/api/exchange-rate', methods=['GET'])
def exchange_rate():
    in_currency = request.args.get('from', default='USD', type=str)
    out_currency = request.args.get('to', default='TRY', type=str)
    amount = request.args.get('amount', default=50, type=float)  

    
    time.sleep(1)  

    try:
        rate = get_currency(in_currency, out_currency, amount)
        return jsonify({
            'from': in_currency,
            'to': out_currency,
            'amount': amount,
            'rate': rate,
            'available_currencies': CURRENCY_LIST  
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)