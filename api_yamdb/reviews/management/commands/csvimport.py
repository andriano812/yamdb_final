# -*- coding: utf-8 -*-

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User


class Command(BaseCommand):
    help = 'Fill the database from static/data/*.csv files'

    def handle(self, *args, **options):
        data_path = os.path.join(os.path.dirname(settings.BASE_DIR),
                                 'api_yamdb',
                                 'static',
                                 'data'
                                 )
        category_path = os.path.join(data_path, 'category.csv')
        comments_path = os.path.join(data_path, 'comments.csv')
        genre_title_path = os.path.join(data_path, 'genre_title.csv')
        genre_path = os.path.join(data_path, 'genre.csv')
        review_path = os.path.join(data_path, 'review.csv')
        titles_path = os.path.join(data_path, 'titles.csv')
        users_path = os.path.join(data_path, 'users.csv')

        with open(category_path, encoding='utf-8') as category_file:
            reader = csv.DictReader(category_file)
            for row in reader:
                new_category = Category(id=row['id'],
                                        name=row['name'],
                                        slug=row['slug']
                                        )
                new_category.save()

        with open(genre_path, encoding='utf-8') as genre_file:
            reader = csv.DictReader(genre_file)
            for row in reader:
                new_genre = Genre(id=row['id'],
                                  name=row['name'],
                                  slug=row['slug']
                                  )
                new_genre.save()

        with open(titles_path, encoding='utf-8') as titles_file:
            reader = csv.DictReader(titles_file)
            for row in reader:
                new_title = Title(id=row['id'],
                                  name=row['name'],
                                  year=int(row['year']),
                                  category=Category.objects.get(
                                      id=row['category'])
                                  )
                new_title.save()

        with open(genre_title_path, encoding='utf-8') as gt_file:
            reader = csv.DictReader(gt_file)
            for row in reader:
                title = Title.objects.get(id=row['title_id'])
                genre_to_add = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre_to_add)
                title.save()

        with open(users_path, encoding='utf-8') as users_file:
            reader = csv.DictReader(users_file)
            for row in reader:
                new_user = User(id=row['id'],
                                username=row['username'],
                                email=row['email'],
                                role=row['role'],
                                bio=row['bio'],
                                first_name=row['first_name'],
                                last_name=row['last_name'],
                                )
                new_user.save()

        with open(review_path, encoding='utf-8') as review_file:
            reader = csv.DictReader(review_file)
            for row in reader:
                new_review = Review(
                    id=row['id'],
                    title=Title.objects.get(id=row['title_id']),
                    text=row['title_id'],
                    author=User.objects.get(id=row['author']),
                    score=int(row['score']),
                    pub_date=row['pub_date']
                )
                new_review.save()

        with open(comments_path, encoding='utf-8') as comments_file:
            reader = csv.DictReader(comments_file)
            for row in reader:
                new_comment = Comment(
                    id=row['id'],
                    review=Review.objects.get(id=row['review_id']),
                    text=row['text'],
                    author=User.objects.get(id=row['author']),
                    pub_date=row['pub_date']
                )
                new_comment.save()

        self.stdout.write(self.style.SUCCESS('Data were imported'))
