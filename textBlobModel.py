from textblob import TextBlob


class TextBlobModel:
    msg_tickers = {}
    results = {}

    def __init__(self, msg_tickers):
        self.msg_tickers = msg_tickers

    def calc_tweet_avg(self):
        ticker_scores = {}
        for msg, tickers in self.msg_tickers.items():
            score = TextBlob(msg).sentiment[0]
            for ticker in tickers:
                if ticker not in ticker_scores.keys():
                    ticker_scores[ticker] = {'sum_score': score, 'count': 1}
                else:
                    ticker_scores[ticker] = {'sum_score': score + ticker_scores[ticker]['sum_score'],
                                             'count': ticker_scores[ticker]['count'] + 1}
        for ticker, info in ticker_scores.items():
            self.results[ticker] = info['sum_score'] / info['count']

    def print_result(self):
        print(self.results)
