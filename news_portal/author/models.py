from django.conf import settings
from django.db import models

# Модель Author
# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# cвязь «один к одному» с встроенной моделью пользователей User;
# рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.


class Author(models.Model):
    """Модель авторов статей."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=False, blank=False, default=0)

    def update_rating(self, user):
        """
        Обновляет рейтинг пользователя.
        Он состоит из следующего:
            суммарный рейтинг каждой статьи автора умножается на 3;
            суммарный рейтинг всех комментариев автора;
            суммарный рейтинг всех комментариев к статьям автора.
        """
        authors = Author.objects.filter(user=user)
        if not authors.exists():
            return

        author = authors.first()
        posts_rating = 0
        post_comments_rating = 0
        for post in author.posts.all():
            posts_rating += post.rating * 3
            post_comments_rating += sum(post.comments.all().values_list("rating", flat=True))

        comments_rating = sum(author.user.comments.all().values_list("rating", flat=True))
        self.rating = posts_rating + post_comments_rating + comments_rating
        self.save()
