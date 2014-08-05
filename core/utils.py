def json2xml(json_obj, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    if json_obj_type is list:
        for sub_elem in json_obj:
            result_list.append(json2xml(sub_elem, line_padding))

        return "\n".join(result_list)

    if json_obj_type is dict:
        for tag_name in json_obj:
            sub_obj = json_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "\n".join(result_list)

    return "%s%s" % (line_padding, json_obj)


def csv2xml(csv_file, xml_file):
    xml_file.write('<?xml version="1.0"?>' + "\n")
    # there must be only one top-level tag
    xml_file.write('<csv_data>' + "\n")

    row_num = 0
    for row in csv_file:
        if row_num == 0:
            tags = row
            # replace spaces w/ underscores in tag names
            for i in range(len(tags)):
                tags[i] = tags[i].replace(' ', '_')
        else:
            xml_file.write('<row>' + "\n")
            for i in range(len(tags)):
                xml_file.write('    ' + '<' + tags[i] + '>' \
                                + row[i] + '</' + tags[i] + '>' + "\n")
            xml_file.write('</row>' + "\n")

        row_num += 1

    xml_file.write('</csv_data>' + "\n")
    xml_file.close()
