from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/crypto', methods=['GET'])
def get_crypto():
    coin_name = request.args.get('coin')
    # CoinMarketCap API
    cmc_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    cmc_headers = {'X-CMC_PRO_API_KEY': 'da342396-84fe-4ea1-80e5-b8f25452f85b'}
    cmc_params = {'start': '1', 'limit': '100', 'convert': 'USD'}
    cmc_resp = requests.get(cmc_url, headers=cmc_headers, params=cmc_params)
    cmc_data = cmc_resp.json()
    coin = next((c for c in cmc_data['data'] if c['name'].lower() == coin_name.lower()), None)
    if not coin:
        return jsonify({'error': 'Coin not found'}), 404

    # NewsAPI
    news_url = 'https://newsapi.org/v2/everything'
    news_params = {
        'q': coin_name,
        'apiKey': '0aaf2be9e81442e8a49f41dfc2b271fc',
        'pageSize': 3,
        'sortBy': 'publishedAt',
        'language': 'en'
    }
    news_resp = requests.get(news_url, params=news_params)
    news_data = news_resp.json()

    return jsonify({
        'name': coin['name'],
        'symbol': coin['symbol'],
        'price': coin['quote']['USD']['price'],
        'news': news_data.get('articles', [])
    })

if __name__ == '__main__':
    app.run(debug=True)