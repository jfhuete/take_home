from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from actors.models import Actor
from movies.models import Movie


class CommonActorsAndPerformanceViewSetTestCase(TestCase):

    def setUp(self) -> None:

        self.actor_1_movie_1_2_dict = {
            "name": "Actor1",
            "age": 22,
            "gender": "male"
        }
        self.actor_2_movie_2_3_dict = {
            "name": "Actor2",
            "age": 33,
            "gender": "female"
        }
        self.actor_3_movie_1_3_dict = {
            "name": "Actor3",
            "age": 44,
            "gender": "male"
        }
        self.actor_4_movie_1_2_dict = {
            "name": "Actor4",
            "age": 55,
            "gender": "female"
        }

        self.movie_1_actor_1_3_4_dict = {
            "title": "Movie1",
            "category": "intrigue",
            "cast": ["Actor1", "Actor3", "Actor4"]
        }
        self.movie_2_actor_1_2_4_dict = {
            "title": "Movie2",
            "category": "terror",
            "cast": ["Actor1", "Actor2", "Actor4"]
        }
        self.movie_3_actor_2_3_dict = {
            "title": "Movie3",
            "category": "comedy",
            "cast": ["Actor2", "Actor3"]
        }

        self.actor_1_movie_1_2 = \
            Actor.objects.create(**self.actor_1_movie_1_2_dict)
        self.actor_2_movie_2_3 = \
            Actor.objects.create(**self.actor_2_movie_2_3_dict)
        self.actor_3_movie_1_3 = \
            Actor.objects.create(**self.actor_3_movie_1_3_dict)
        self.actor_4_movie_1_2 = \
            Actor.objects.create(**self.actor_4_movie_1_2_dict)

        self.movie_1_actor_1_3_4 = Movie.objects.create(
            title=self.movie_1_actor_1_3_4_dict["title"],
            category=self.movie_1_actor_1_3_4_dict["category"]
        )
        self.movie_1_actor_1_3_4.save()
        self.movie_1_actor_1_3_4.cast.add(*[
            self.actor_1_movie_1_2,
            self.actor_3_movie_1_3,
            self.actor_4_movie_1_2
        ])

        self.movie_2_actor_1_2_4 = Movie.objects.create(
            title=self.movie_2_actor_1_2_4_dict["title"],
            category=self.movie_2_actor_1_2_4_dict["category"]
        )
        self.movie_2_actor_1_2_4.save()
        self.movie_2_actor_1_2_4.cast.add(*[
            self.actor_1_movie_1_2,
            self.actor_2_movie_2_3,
            self.actor_4_movie_1_2
        ])

        self.movie_3_actor_2_3 = Movie.objects.create(
            title=self.movie_3_actor_2_3_dict["title"],
            category=self.movie_3_actor_2_3_dict["category"]
        )
        self.movie_3_actor_2_3.save()
        self.movie_3_actor_2_3.cast.add(*[
            self.actor_2_movie_2_3,
            self.actor_3_movie_1_3
        ])

        self.client = APIClient()

    # Performances

    def test_get_movies_in_actors_list_with_correct_data(self):
        """
        Test get movies in actors list with correct data

        GET /performances/?actors=Actor1,Actor4
        Expected status_code: 200 OK
        Expected body:
            [
                {
                    "title": "Movie1",
                    "category": "intrigue",
                    "cast": ["Actor1", "Actor3", "Actor4"]
                },
                {
                    "title": "Movie2",
                    "category": "terror",
                    "cast": ["Actor1", "Actor2", "Actor4"]
                }
            ]
        """

        expected_body = [
            self.movie_1_actor_1_3_4_dict,
            self.movie_2_actor_1_2_4_dict
        ]

        request = self.client.get('/performances/?actors=Actor1,Actor4')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertCountEqual(expected_body, request.data)

    def test_get_movies_starring_actors_who_do_not_exist(self):
        """
        Test get movies starring actors who do not exist

        GET /performances/?actors=Actor1,Actor20
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.get('/performances/?actors=Actor1,Actor20')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_get_performances_without_actors_query_params(self):
        """
        Test get performances without actors query params

        GET /performances/
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.get('/performances/')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    # Commond Actors

    def test_get_commond_actors_in_movies_list_with_correct_data(self):
        """
        Test get commond actors in movies list with correct data

        GET /common_actors/?movies=Movie1,Movie2
        Expected status_code: 200 OK
        Expected body:
            [
                {
                    "name": "Actor1",
                    "age": 22,
                    "gender": "male"
                },
                {
                    "name": "Actor4",
                    "age": 55,
                    "gender": "female"
                },
            ]
        """

        expected_body = [
            self.actor_1_movie_1_2_dict,
            self.actor_4_movie_1_2_dict
        ]

        request = self.client.get('/common_actors/?movies=Movie1,Movie2')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertCountEqual(expected_body, request.data)

    def test_get_commond_actors_in_movies_list_with_not_existent_movie(self):
        """
        Test get commond actors in movies list with not existent movie

        GET /common_actors/?movies=Movie1,Movie20
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.get('/common_actors/?movies=Movie1,Movie20')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_get_commond_actors_in_movies_without_movie_query_param(self):
        """
        Test get commond actors in movies without movie query param

        GET /common_actors/
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.get('/common_actors/')

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)
