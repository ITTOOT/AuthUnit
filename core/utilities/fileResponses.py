import csv
import json
from io import StringIO
from xml.etree.ElementTree import Element, SubElement, tostring


# XML
def generate_xml_response(data, root_name='root', element_name='element'):
    # Create the root element
    root = Element(root_name)

    # Iterate over the data and create XML elements
    for statistic in data:
        statistic_element = SubElement(root, element_name)
        for key, value in statistic.items():
            field_element = SubElement(statistic_element, key)
            field_element.text = str(value)

    # Convert the XML root element to a string
    xml_string = tostring(root, encoding='utf-8')

    return xml_string

# CSV
def generate_csv_response(data):
    # Create a string buffer to write CSV data
    csv_buffer = StringIO()

    # Create a CSV writer
    writer = csv.writer(csv_buffer)

    # Write the CSV headers
    headers = data[0].keys() if data else []
    writer.writerow(headers)

    # Write the CSV rows
    for statistic in data:
        writer.writerow(statistic.values())

    # Get the CSV content from the buffer
    csv_content = csv_buffer.getvalue()

    # Close the buffer
    csv_buffer.close()

    return csv_content

# TEXT
def generate_text_response(data):
    response = ''
    for statistic in data:
        # Format the statistic data as plain text
        text = f"Statistic: {statistic['statistic1']}, {statistic['statistic2']}\n"
        response += text
    return response

# JSON
def generate_json_response(data):
    # Convert the data to JSON format
    json_data = json.dumps(data)

    return json_data
