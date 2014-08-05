from django import forms

FORMATS = (
    ('json', 'json'),
    ('csv', 'csv'),
    ('xml', 'xml'),
)


class UploadFileForm(forms.Form):
    upload_file = forms.FileField()
    out_extension = forms.ChoiceField(choices=FORMATS)
