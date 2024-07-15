from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.service import get_an_article, get_article_list, do_like


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

    def test_get_article_list_should_prefetch_likes(self) -> None:
        # GIven
        user = User.objects.create(name="user1")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        Like.objects.create(user_id=user.id, article_id=articles[-1].id)

        # When
        result_articles = get_article_list(0, 10)

        # Then
        self.assertEqual(10, len(result_articles))
        self.assertEqual(1, result_articles[0].like_set.count())
        self.assertEqual(
            [a.id for a in reversed(articles[10:21])],
            [a.id for a in result_articles]
        )

    def test_get_article_list_should_prefetch_like(self) -> None:
        # GIven
        user = User.objects.create(name="user1")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        do_like(user_id=user.id, article_id=articles[-1].id)

        # When
        with self.assertNumQueries(2):
            result_articles = get_article_list(0, 10)
            result_counts = [a.like_set.count() for a in result_articles]

            # Then
            self.assertEqual(len(result_articles), 10)
            self.assertEqual(1, result_counts[0])
            self.assertEqual(
                [a.id for a in reversed(articles[10:21])],
                [a.id for a in result_articles]
            )
