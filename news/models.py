# (venv) ~/django-projects/Mac $ python manage.py makemigrations
# (venv) ~/django-projects/Mac $ python manage.py migrate
# (venv) ~/django-projects/Mac $ python manage.py shell


from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Новости
class News(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True, # названия новостей не должны повторяться
    )
    description = models.TextField()
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)],
    )
    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='news', # все новости в категории будут доступны через поле news
    )
    # # поле категории будет ссылаться на модель author
    # author = models.ForeignKey(
    #     to='Author',
    #     on_delete=models.CASCADE,
    #     related_name='news',  # все новости в категории будут доступны через поле news
    # )


    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'


# # Категория, к которой будет привязываться товар
# class Category(models.Model):
#     # названия категорий тоже не должны повторяться
#     name = models.CharField(max_length=100, unique=True)
#
#     def __str__(self):
#         return self.name.title()


# Модель, содержащая объекты всех авторов.
# Имеет следующие поля:
# cвязь «один к одному» с встроенной моделью пользователей User;
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    #рейтинг пользователя. Ниже будет дано описание того, как этот рейтинг можно посчитать.
    def update_rating(self):
        post_rating = sum(self.posts.all().values_list('rating', flat=True))
        comment_rating = sum(self.user.comments.all().values_list('rating', flat=True))
        self.rating = post_rating * 3 + comment_rating
        self.save()

    def __str__(self):
        return self.user.username


# Категории новостей/статей — темы, которые они отражают (спорт, политика, образование и т. д.).
# Имеет единственное поле: название категории. Поле должно быть уникальным
# (в определении поля необходимо написать параметр unique = True).
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Эта модель должна содержать в себе статьи и новости, которые создают пользователи.
# Каждый объект может иметь одну или несколько категорий.
# Соответственно, модель должна включать следующие поля:
# связь «один ко многим» с моделью Author;
# поле с выбором — «статья» или «новость»;
# автоматически добавляемая дата и время создания;
# связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory);
# заголовок статьи/новости;
# текст статьи/новости;
# рейтинг статьи/новости.
class Post(models.Model):
    POST_TYPES = (
        ('article', 'Article'),
        ('news', 'News')
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=7, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = self.likes.all().count() - self.dislikes.all().count()
        self.save()
        self.author.update_rating()

    def preview(self):
        if len(self.text) > 127:
            return self.text[:124] + '...'
        else:
            return self.text

    def __str__(self):
        return self.title

# Промежуточная модель для связи «многие ко многим»:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» с моделью Category.
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


# Под каждой новостью/статьёй можно оставлять комментарии, поэтому необходимо организовать их способ хранения тоже.
# Модель будет иметь следующие поля:
# связь «один ко многим» с моделью Post;
# связь «один ко многим» со встроенной моделью User (комментарии может оставить любой пользователь, необязательно автор);
# текст комментария;
# дата и время создания комментария;
# рейтинг комментария.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = self.likes.all().count() - self.dislikes.all().count()
        self.save()
        self.post.update_rating()
        self.user.author.update_rating()

    def like(self):
        self.rating += 1
        self.save()
        self.update_rating()

    def dislike(self):
        self.rating -= 1
        self.save()
        self.update_rating()

    def __str__(self):
        return self.text

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislikes')
