import os
import csv
import json
#import pdb
from tempfile import mkstemp
from types import StringTypes

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from xmlutils.xml2json import xml2json
from xmlutils.xml2csv import xml2csv

from .forms import UploadFileForm
from .utils import json2xml, csv2xml

FORMATS = ['json', 'csv', 'xml']


def home(request):
    # upload file
    uploaded_file = None
    message = ""
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            # get file
            uploaded_file = request.FILES['upload_file']

            # get output extension
            out_extension = request.POST['out_extension']

            # get input extension
            file_name, extension = os.path.splitext(uploaded_file.name)
            # cut point
            in_extension = extension[1:]

            # if good uploaded file
            if in_extension in FORMATS:

                # not the same extension
                if in_extension != out_extension:

                    # get place to save file
                    fd, temp_path = mkstemp()

                    # json
                    if in_extension == FORMATS[0]:
                        try:
                            file_json = json.load(uploaded_file)
                        except Exception, e:
                            raise e

                        # csv
                        if out_extension == FORMATS[1]:
                            write_header = True
                            item_keys = []

                            with open(temp_path, 'wb+') as csv_file:
                                writer = csv.writer(csv_file)

                                for item in file_json:
                                    item_values = []
                                    for key in item:
                                        if write_header:
                                            item_keys.append(key)

                                        value = item.get(key, '')
                                        if isinstance(value, StringTypes):
                                            item_values.append(value.encode('utf-8'))
                                        else:
                                            item_values.append(value)

                                    if write_header:
                                        writer.writerow(item_keys)
                                        write_header = False

                                    writer.writerow(item_values)
                        # xml
                        else:
                            with open(temp_path, 'wb+') as xml_file:
                                xml_file.write(json2xml(file_json))
                                xml_file.close()

                    # csv
                    elif in_extension == FORMATS[1]:
                        # json
                        if out_extension == FORMATS[0]:
                            csv_file = csv.DictReader(uploaded_file)
                            with open(temp_path, 'wb+') as json_file:
                                out = json.dumps([row for row in csv_file])
                                json_file.write(out)
                        # xml
                        else:
                            csv_file = csv.reader(uploaded_file)
                            with open(temp_path, 'wb+') as xml_file:
                                csv2xml(csv_file, xml_file)

                    # xml
                    else:
                        xml_file = uploaded_file
                        # json
                        if out_extension == FORMATS[0]:
                            converter = xml2json(xml_file, encoding="utf-8")
                            with open(temp_path, 'wb+') as json_file:
                                json_file.write(converter.get_json())
                                json_file.close()

                        # csv
                        else:
                            converter = xml2csv(xml_file, temp_path)
                            converter.convert(tag='item')

                    file = open(temp_path, 'r')
                    data = file.read()
                    file.close()
                    os.close(fd)
                    os.remove(temp_path)

                    # dowload file
                    response = HttpResponse(
                        data,
                        content_type='application/force-download')
                    response['Content-Disposition'] = 'attachment; \
                        filename=%s' % str(file_name + '.' + out_extension)

                    return response
                else:
                    message = """Input file has the same format as output,
                        choose another out extension"""
            else:
                message = """Input file has bad format,
                    upload files only with extension json, csv, xml"""
    else:
        form = UploadFileForm()

    return render(request, "main.html", {
        'form': form,
        'uploaded_file': uploaded_file,
        'message': message
    })
