from django.test import TestCase

from tabom.models import Article
from tabom.service import get_an_article


class TestArticleService(TestCase):

    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title="test article")

        # WHen
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_error_when_article_does_not_exist(self) -> None:
        # Given
        article_id = 9988

        # When
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(article_id)
