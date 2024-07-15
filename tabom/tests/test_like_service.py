from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.service import do_like, undo_like


class TestLikeService(TestCase):

    def test_a_user_can_like_an_article(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test article")

        # When
        like = do_like(user.id, article.id)

        # Then
        self.assertIsNotNone(like)
        self.assertEqual(user.id, like.user_id)
        self.assertEqual(article.id, like.article_id)

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_article")

        # Expect
        like1 = do_like(user.id, article.id)
        with self.assertRaises(IntegrityError):
            like2 = do_like(user.id, article.id)

    def test_like_with_non_existing_user(self) -> None:
        # Given
        article = Article.objects.create(title="test_article")

        # When
        with self.assertRaises(IntegrityError):
            like = do_like(98989898989898, article.id)

    def test_like_count_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_article")

        # When
        do_like(user.id, article.id)

        # Then
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())

    def test_a_user_can_undo_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_article")
        like = do_like(user.id, article.id)

        # When
        undo_like(user.id, article.id)

        # Then: 어떻게 할까...!
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=like.id)
