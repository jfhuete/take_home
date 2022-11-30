from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from actors.models import Actor
from movies.models import Movie


class MovieViewSetTestCase(TestCase):
    """
    TestCase for Movie API endpoints
    """

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
        self.actor_3_movie_1_2_dict = {
            "name": "Actor3",
            "age": 55,
            "gender": "female"
        }

        self.movie_1_actor_1_3_dict = {
            "title": "Movie1",
            "category": "intrigue",
            "cast": ["Actor1", "Actor3"]
        }
        self.movie_2_actor_1_3_dict = {
            "title": "Movie2",
            "category": "terror",
            "cast": ["Actor1", "Actor2", "Actor3"]
        }
        self.movie_3_actor_2_dict = {
            "title": "Movie3",
            "category": "comedy",
            "cast": ["Actor2"]
        }

        self.actor_1_movie_1_2 = \
            Actor.objects.create(**self.actor_1_movie_1_2_dict)
        self.actor_2_movie_2_3 = \
            Actor.objects.create(**self.actor_2_movie_2_3_dict)
        self.actor_3_movie_1_2 = \
            Actor.objects.create(**self.actor_3_movie_1_2_dict)

        self.movie_1_actor_1_3 = Movie.objects.create(
            title=self.movie_1_actor_1_3_dict["title"],
            category=self.movie_1_actor_1_3_dict["category"]
        )
        self.movie_1_actor_1_3.save()
        self.movie_1_actor_1_3.cast.add(*[
            self.actor_1_movie_1_2,
            self.actor_3_movie_1_2
        ])

        self.movie_2_actor_1_3 = Movie.objects.create(
            title=self.movie_2_actor_1_3_dict["title"],
            category=self.movie_2_actor_1_3_dict["category"]
        )
        self.movie_2_actor_1_3.save()
        self.movie_2_actor_1_3.cast.add(*[
            self.actor_1_movie_1_2,
            self.actor_2_movie_2_3,
            self.actor_3_movie_1_2
        ])

        self.movie_3_actor_2 = Movie.objects.create(
            title=self.movie_3_actor_2_dict["title"],
            category=self.movie_3_actor_2_dict["category"]
        )
        self.movie_3_actor_2.save()
        self.movie_3_actor_2.cast.add(*[
            self.actor_2_movie_2_3,
        ])

        self.client = APIClient()

    # GET Endpoints

    def test_get_movies_return_a_list_with_all_movies(self):
        """
        Test get movies return a list with all movies

        GET /movies/
        Expected status_code: 200 OK
        Expected body:
            [
                {
                    "title": "Movie1",
                    "category": "intrigue",
                    "cast": ["Actor1", "Actor3"]
                },
                {
                    "title": "Movie2",
                    "category": "terror",
                    "cast": ["Actor1", "Actor2", "Actor3"]
                },
                {
                    "title": "Movie3",
                    "category": "comedy",
                    "cast": ["Actor2"]
                }
            ]
        """

        expected_body = [
            self.movie_1_actor_1_3_dict,
            self.movie_2_actor_1_3_dict,
            self.movie_3_actor_2_dict,
        ]

        request = self.client.get('/movies/')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertCountEqual(expected_body, request.data)

    def test_get_movie_by_title_return_dict_with_its_data(self):
        """
        Test get movie by title return dict with its data

        GET /movies/Movie1/
        Expected status_code: 200 OK
        Expected body:
            {
                "title": "Movie1",
                "category": "intrigue",
                "cast": ["Actor1", "Actor3"]
            }
        """

        expected_body = self.movie_1_actor_1_3_dict

        request = self.client.get('/movies/Movie1/')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertDictEqual(expected_body, request.data)

    def test_get_movie_no_saved_in_db_return_status_code_404(self):
        """
        Test get movie no saved in db return status code 404

        GET /movies/NewMovie/
        Expected status_code: 404 NOT FOUND
        """

        request = self.client.get('/movies/NewMovie/')

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)

    # POST Endpoints

    def test_post_new_movie_with_correct_data_return_status_code_200(self):
        """
        Test post new movie with correct data return status code 200

        POST /movies/
        Payload:
            {
                "title": "NewMovie",
                "gender": "children",
                "actors": ["Actor1", "Actor3"]
            }
        Expected status_code: 200 OK
        """

        request = self.client.post(
            '/movies/',
            {
                "title": "NewMovie",
                "category": "children",
                "cast": ["Actor1", "Actor3"]
            },
        )

        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_post_new_movie_with_no_existent_actor_return_status_code_400(self):
        """
        Test post new movie with no existent actor return status code 400

        POST /movies/
        Payload:
            {
                "title": "NewMovie",
                "gender": "children",
                "actors": ["Actor1", "ActorNotExistent"]
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.post(
            '/movies/',
            {
                "title": "NewMovie",
                "gender": "children",
                "actors": ["Actor1", "ActorNotExistent"]
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_post_new_movie_that_exists_in_db_return_status_code_400(self):
        """
        Test post new movie that exists in db return status code 400

        POST /movies/
        Payload:
            {
                "title": "Movie1",
                "category": "terror",
                "cast": ["Actor2"]
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.post(
            '/movies/',
            self.movie_1_actor_1_3_dict
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_post_malformed_payload_return_status_code_422(self):
        """
        Test post malformed payload return status code 422

        POST /movies/
        Payload: "foo"
        Expected status_code: 422 UNPROCESSABLE ENTITY
        """

        request = self.client.post(
            '/movies/',
            content_type='application/json',
            data="foo",
        )

        self.assertEqual(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            request.status_code
        )

    # PATCH Endpoints

    def test_patch_movie_update_category_with_correct_data_return_200_ok(self):
        """
        Test patch movie update category with correct data return 200 ok

        PATH /movies/Movie1/
        Payload:
            {
                "category": "comedy",
            }
        Expected status_code: 200 OK
        """

        request = self.client.patch(
            '/movies/Movie1/',
            {
                "category": "comedy",
            },
        )

        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_patch_movie_that_not_exists_return_status_code_404(self):
        """
        Test patch movie that not exists return status code 404

        PATH /movies/NotExists
        Payload:
            {
                "category": "foo",
            }
        Expected status_code: 404 NOT FOUND
        """

        request = self.client.patch(
            '/movies/NotExists/',
            {
                "category": "foo",
            }
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)

    def test_patch_movie_with_actor_that_not_exists_return_status_code_400(self):
        """
        Test patch movie with actor that not exists return status code 400

        PATH /movies/Movie1/
        Payload:
            {
                "cast": ["foo"],
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.patch(
            '/movies/Movie1/',
            {
                "cast": ["foo"],
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_patch_movie_with_malformed_data_return_status_code_422(self):
        """
        Test patch movie with malformed data return status code 422

        PATH /movies/Foo
        Payload: "foo"
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.patch(
            '/movies/Movie1/',
            content_type='application/json',
            data='foo',
        )

        self.assertEqual(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            request.status_code
        )

    # DELETE Endpoints

    def test_delete_movie_that_exists_in_db_return_status_code_204(self):
        """
        Test delete movie that exists in db return status code 204

        DELETE /movies/Movie1/

        Expected status_code: 204 NOT CONTENT
        """

        request = self.client.delete('/movies/Movie1/')

        self.assertEqual(status.HTTP_204_NO_CONTENT, request.status_code)

    def test_delete_movie_that_not_exists_return_status_code_404(self):
        """
        Test delete movie that not exists return status code 404

        DELETE /movies/NotExists

        Expected status_code: 404 NOT FOUND
        """

        request = self.client.patch('/movies/NotExists/')

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)
