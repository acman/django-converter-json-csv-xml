from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from .forms import UploadFileForm


class MainPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_homepage_available(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'main.html')

    def test_homepage_without_error_messages(self):
        self.assertEqual(self.response.context['message'], '')


class FormTest(TestCase):
    def setUp(self):
        self.file_json = open('file.json', 'w+')
        self.file_json.write('[{"id": 1, "name": "name1"}, \
            {"id": 2, "name": "name2"}]')
        self.file_json.close()

    def test_form(self):
        upload_file = open(self.file_json.name, 'rb')
        post_dict = {'out_extension': 'json'}
        file_dict = {'upload_file': SimpleUploadedFile(
            upload_file.name,
            upload_file.read()
        )}
        form = UploadFileForm(post_dict, file_dict)
        self.assertTrue(form.is_valid())
        response = self.client.post('/')
        self.assertEqual(response.status_code, 200)

    def test_bad_vote(self):
        response = self.client.post('/', {})
        self.assertFormError(response, 'form', 'upload_file', 'This field is required.')
