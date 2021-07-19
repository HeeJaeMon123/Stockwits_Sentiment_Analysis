from textBlobModel import TextBlobModel
from utils import get_msg_with_tickers

if __name__ == "__main__":
    # Text Blob Model
    msg_tickers = get_msg_with_tickers()
    text_blob_model = TextBlobModel(msg_tickers)
    text_blob_model.calc_tweet_avg()
    text_blob_model.print_result()

