from django.test import TestCase
from .utils import predict_sentiment
# Create your tests here.


class SentimentAnalysisTestCase(TestCase):
    def test_predict_sentiment(self):
        text = "I love this movie"
        sentiment = predict_sentiment(text)
        self.assertEqual(sentiment, "Positive")
