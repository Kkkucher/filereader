import json
from io import BytesIO

from django.test import TestCase
from django.urls import reverse

from homepage.models import DataTable


def make_json_file(data):
    content = json.dumps(data).encode("utf-8")
    return BytesIO(content)


class UploadViewTests(TestCase):

    def test_get_returns_200(self):
        response = self.client.get(reverse("homepage:upload"))
        self.assertEqual(response.status_code, 200)

    def test_post_without_file_returns_error(self):
        response = self.client.post(reverse("homepage:upload"))
        self.assertContains(response, "No file selected")

    def test_post_valid_json_creates_records(self):
        data = [
            {"name": "Alice", "date": "2024-01-15_10:30"},
            {"name": "Bob", "date": "2024-06-20_08:00"},
        ]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertRedirects(response, reverse("homepage:tableview"))
        self.assertEqual(DataTable.objects.count(), 2)
        self.assertTrue(DataTable.objects.filter(name="Alice").exists())

    def test_post_missing_name_field_returns_error(self):
        data = [{"date": "2024-01-15_10:30"}]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertContains(response, "wrong json form")
        self.assertEqual(DataTable.objects.count(), 0)

    def test_post_missing_date_field_returns_error(self):
        data = [{"name": "Alice"}]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertContains(response, "wrong json form")
        self.assertEqual(DataTable.objects.count(), 0)

    def test_post_name_too_long_returns_error(self):
        data = [{"name": "A" * 50, "date": "2024-01-15_10:30"}]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertContains(response, "name field too long")
        self.assertEqual(DataTable.objects.count(), 0)

    def test_post_wrong_date_format_returns_error(self):
        data = [{"name": "Alice", "date": "15-01-2024"}]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertContains(response, "wromg date field")
        self.assertEqual(DataTable.objects.count(), 0)

    def test_post_partial_errors_saves_nothing(self):
        data = [
            {"name": "Alice", "date": "2024-01-15_10:30"},  # валидная
            {"name": "Bob", "date": "bad-date"},  # невалидная
        ]
        file = make_json_file(data)
        response = self.client.post(
            reverse("homepage:upload"),
            {"json_file": file},
        )
        self.assertContains(response, "wromg date field")
        self.assertEqual(DataTable.objects.count(), 0)


class TableViewTests(TestCase):

    def test_get_returns_200(self):
        response = self.client.get(reverse("homepage:tableview"))
        self.assertEqual(response.status_code, 200)

    def test_shows_existing_records(self):
        DataTable.objects.create(name="TestName", date="2024-01-15 10:30:00")
        response = self.client.get(reverse("homepage:tableview"))
        self.assertContains(response, "TestName")


class DataTableModelTests(TestCase):

    def test_create_and_retrieve(self):
        DataTable.objects.create(name="Slavik", date="2024-03-23 12:00:00")
        obj = DataTable.objects.get(name="Slavik")
        self.assertEqual(obj.name, "Slavik")

    def test_date_can_be_null(self):
        obj = DataTable.objects.create(name="NullDate", date=None)
        self.assertIsNone(obj.date)
