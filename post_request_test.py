import unittest

import mock

from app import app


class PostRequestTest(unittest.TestCase):
    @mock.patch("psycopg2.connect")
    @mock.patch("app.get_presigned_url")
    def test_get_user_contact(self, mock_get_presigned_url, mock_connect):
        expected = [{"name": "Amdaul Bari Imad", "pic": "url"}]

        mock_con = mock_connect.return_value
        mock_cur = mock_con.cursor.return_value
        mock_cur.fetchone.return_value = expected
        mock_get_presigned_url.return_value = "url"

        app.testing = True
        with app.test_client() as client:
            result = client.post("/reverser", json={"num": "01843105424"})
            self.assertEqual({"num": "Amdaul Bari Imad", "pic_url": "url"}, result.json)
            self.assertTrue(mock_get_presigned_url.called)
            self.assertTrue(mock_connect.called)