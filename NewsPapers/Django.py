#Создайте двух пользователей:

from django.contrib.auth.models import User

user1 = User.objects.create_user('user1')
user2 = User.objects.create_user('user2')

#Создайте два объекта модели Author, связанные с пользователями:

from news.models import Author

author1 = Author.objects.create(user=user1, rating=0)
author2 = Author.objects.create(user=user2, rating=0)

#Добавьте 4 категории в модель Category:

from news.models import Category

category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Развлечения', unique=True)

#Добавьте 2 статьи и 1 новость, распределите их по категориям:

from news.models import Post, PostCategory

post1 = Post.objects.create(author=author1, post_type='article', title='Статья 1', text='Это первая статья', rating=0)
post1.categories.add(category1, category2)

post2 = Post.objects.create(author=author2, post_type='news', title='Новость 1', text='Это первая новость', rating=0)
post2.categories.add(category1)

post3 = Post.objects.create(author=author1, post_type='article', title='Статья 2', text='Это вторая статья', rating=0)
post3.categories.add(category3)

#Создайте не менее 4 комментариев для различных объектов модели Post (каждый объект должен иметь хотя бы один комментарий):

from news.models import Comment

comment1 = Comment.objects.create(post=post1, user=user1, text='Это первый комментарий', rating=0)
comment2 = Comment.objects.create(post=post1, user=user2, text='Это второй комментарий', rating=0)
comment3 = Comment.objects.create(post=post2, user=user1, text='Это третий комментарий', rating=0)
comment4 = Comment.objects.create(post=post3, user=user2, text='Это четвертый комментарийt', rating=0)

#Применяя функции like() и dislike() к статьям/новостям и комментариям, регулируйте рейтинг этих объектов:

comment1.like()
comment2.dislike()
post1.like()
post2.dislike()

#Обновление оценок пользователей:

author1.update_rating()
author2.update_rating()

#Выводит имя пользователя и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта):

best_author = Author.objects.all().order_by('-rating').values('user__username', 'rating').first()
print(best_author)

#Вывод даты добавления, имени автора, рейтинга, заголовка и превью лучшей статьи на основе лайков/дизлайков к этой статье:

best_post = Post.objects.filter(post_type='article').order_by('-rating').values('pub_date', 'author__user__username', 'rating', 'title', 'preview').first()
print(best_post)

# Вывод всех комментариев (дата, пользователь, рейтинг, текст) к этой статье:

best_post_comments = Comment.objects.filter(post=best_post).values('pub_date', 'user__username', 'rating', 'text')
for comment in best_post_comments:
print(comment)