from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from actors.models import Actor


class ActorViewSetTestCase(TestCase):
    """
    TestCase for Actors API endpoints
    """

    def setUp(self) -> None:

        self.actor_male_created_dict = {
            "name": "Foo",
            "age": 22,
            "gender": "male"
        }
        self.actor_female_created_dict = {
            "name": "Bar",
            "age": 33,
            "gender": "female"
        }
        self.new_actor_male_dict = {
            "name": "New Foo",
            "age": 44,
            "gender": "male"
        }
        self.new_actor_female_dict = {
            "name": "New Bar",
            "age": 55,
            "gender": "female"
        }
        self.new_actor_bad_gender_dict = {
            "name": "New Bar",
            "age": 66,
            "gender": "baz"
        }
        self.new_actor_bag_age_dict = {
            "name": "New Bar",
            "age": "baz",
            "gender": "male"
        }

        self.actor_foo = Actor.objects.create(**self.actor_male_created_dict)
        self.actor_bar = Actor.objects.create(**self.actor_female_created_dict)

        self.client = APIClient()

    # GET Endpoints

    def test_get_actors_return_a_list_with_all_actors(self):
        """
        Test get actors return a list with all actors

        GET /actors/
        Expected status_code: 200 OK
        Expected body:
            [
                {
                    "name": "Foo",
                    "age": 22,
                    "gender": "male"
                },
                {
                    "name": "Bar",
                    "age": 33,
                    "gender": "female"
                },
            ]
        """

        expected_body = [
            self.actor_male_created_dict,
            self.actor_female_created_dict
        ]

        request = self.client.get('/actors/')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertCountEqual(expected_body, request.data)

    def test_get_actor_by_name_return_dict_with_his_data(self):
        """
        Test get actor by name return dict with his data

        GET /actors/Foo/
        Expected status_code: 200 OK
        Expected body:
            {
                "name": "Foo",
                "age": 22,
                "gender": "male"
            }
        """

        expected_body = self.actor_male_created_dict

        request = self.client.get('/actors/Foo/')

        self.assertEqual(status.HTTP_200_OK, request.status_code)
        self.assertDictEqual(expected_body, request.data)

    def test_get_actor_no_saved_in_db_return_status_code_404(self):
        """
        Test get actor no saved in db return status code 404

        GET /actors/New%20Foo/
        Expected status_code: 404 NOT FOUND
        """

        request = self.client.get('/actors/New%20Foo/')

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)

    # POST Endpoints

    def test_post_new_actor_with_correct_data_return_status_code_200(self):
        """
        Test post new actor with correct data return status code 200

        POST /actors/
        Payload:
            {
                "name": "New Foo",
                "age": 44,
                "gender": "male"
            }
        Expected status_code: 200 OK
        """

        request = self.client.post(
            '/actors/',
            self.new_actor_male_dict,
        )

        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_post_new_actor_with_bad_gender_return_status_code_400(self):
        """
        Test post new actor with bad gender return status code 400

        POST /actors/
        Payload:
            {
                "name": "New Bar",
                "age": 66,
                "gender": "baz"
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.post(
            '/actors/',
            self.new_actor_bad_gender_dict,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_post_new_actor_who_exists_in_db__return_status_code_400(self):
        """
        Test post new actor who exists in db return status code 400

        POST /actors/
        Payload:
            {
                "name": "Foo",
                "age": 22,
                "gender": "male"
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.post(
            '/actors/',
            self.actor_male_created_dict,
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_post_malformed_payload_return_status_code_422(self):
        """
        Test post malformed payload return status code 422

        POST /actors/
        Payload: "foo"
        Expected status_code: 422 UNPROCESSABLE ENTITY
        """

        request = self.client.post(
            '/actors/',
            content_type='application/json',
            data="foo",
        )

        self.assertEqual(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            request.status_code
        )

    # PATCH Endpoints

    def test_patch_actor_update_age_with_correct_data_return_200_ok(self):
        """
        Test patch actor update age with correct data return 200 ok

        PATH /actors/Foo/
        Payload:
            {
                "age": 33,
            }
        Expected status_code: 200 OK
        """

        request = self.client.patch(
            '/actors/Foo/',
            {
                "age": 33
            },
        )

        self.assertEqual(status.HTTP_200_OK, request.status_code)

    def test_patch_actor_that_not_exists_return_status_code_404(self):
        """
        Test patch actor that not exists return status code 404

        PATH /actors/NotExists
        Payload:
            {
                "age": 33,
            }
        Expected status_code: 404 NOT FOUND
        """

        request = self.client.patch(
            '/actors/NotExists/',
            {
                "age": 33
            },
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)

    def test_patch_actor_with_incorrect_data_return_status_code_400(self):
        """
        Test patch actor with incorrect data return status code 400

        PATH /actors/Foo
        Payload:
            {
                "gender": "foo",
            }
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.patch(
            '/actors/Foo/',
            {
                "gender": "foo"
            },
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, request.status_code)

    def test_patch_actor_with_malformed_data_return_status_code_422(self):
        """
        Test patch actor with malformed data return status code 422

        PATH /actors/Foo
        Payload: "foo"
        Expected status_code: 400 BAD REQUEST
        """

        request = self.client.patch(
            '/actors/Foo/',
            content_type='application/json',
            data='foo',
        )

        self.assertEqual(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            request.status_code
        )

    # DELETE Endpoints

    def test_delete_actor_that_exists_in_db_return_status_code_204(self):
        """
        Test delete actor that exists in db return status code 204

        DELETE /actors/Foo/

        Expected status_code: 204 NOT CONTENT
        """

        request = self.client.delete('/actors/Foo/')

        self.assertEqual(status.HTTP_204_NO_CONTENT, request.status_code)

    def test_delete_actor_that_not_exists_return_status_code_404(self):
        """
        Test delete actor that not exists return status code 404

        DELETE /actors/NotExists

        Expected status_code: 404 NOT FOUND
        """

        request = self.client.patch('/actors/NotExists/')

        self.assertEqual(status.HTTP_404_NOT_FOUND, request.status_code)
