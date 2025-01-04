from rest_framework.renderers import JSONRenderer


class EnvelopeJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        request = renderer_context.get("request")
        response = renderer_context.get("response")

        status_code = response.status_code
        message = get_response_message(request, response)
        if status_code >= 200 and status_code < 300:
            data = success_response(data, message)

        elif status_code >= 400:
            data = error_response(data, message)

        return super().render(data, accepted_media_type, renderer_context)


def success_response(data, message):
    return {"status": True, "message": message, "data": data}


def error_response(data, message=None):
    details = compress_data_to_list(data)
    if len(details) == 1:
        message = details[0]
    return {"status": False, "errors": details, "message": message}


def get_response_message(request, response):
    message = None
    if response.status_code == 201:
        message = "Successfully created"
    elif response.status_code == 200:
        message = "Successfully retrieved"
        if request.method in ["PUT", "PATCH"]:
            message = "Successfully updated"
    elif response.status_code == 400:
        message = "Validation errors"
    elif response.status_code == 401:
        message = "Authentication credentials were not provided"
    elif response.status_code == 403:
        message = "You do not have permission to perform this action"
    elif response.status_code == 404:
        message = "Resource not found"
    elif response.status_code == 500:
        message = "Internal server error"

    return message


def compress_data_to_list(data, key=None):
    compressed = list()
    if isinstance(data, list):
        for value in data:
            compressed.extend(compress_data_to_list(value, key))
    elif isinstance(data, dict):
        for key, value in data.items():
            compressed.extend(compress_data_to_list(value, key))
    else:
        if data == "This field is required.":
            compressed.append(f"{key} is required.")

        elif data == "This field may not be blank.":
            compressed.append(f"{key} may not be blank.")

        elif data == "This field may not be null.":
            compressed.append(f"{key} may not be null.")

        elif data == "A valid integer is required.":
            compressed.append(f"A valid integer is required for {key}")

        elif isinstance(data, str) and data.endswith("is not a valid choice."):
            compressed.append(f"{data.strip('.')} for {key}.")

        elif isinstance(data, str) and data.startswith("Expected a list of items"):
            compressed.append(f"{data.strip('.')} for {key}.")

        elif isinstance(data, str) and data.startswith("Ensure this field "):
            compressed.append(data.replace("this field", f"{key}"))

        elif isinstance(data, str) and data.startswith("Ensure this value "):
            compressed.append(data.replace("this value", f"{key}"))

        elif isinstance(data, str) and data == "No file was submitted.":
            compressed.append(data.replace(".", f" for {key}."))

        elif (
            data
            == "The submitted data was not a file. Check the encoding type on the form."
        ):
            if isinstance(key, int):
                compressed.append(
                    (
                        f"Invalid file type for file {key} index of array object."
                        " Please upload a valid file."
                    )
                )
            else:
                compressed.append(
                    f"Invalid file type for {key}. Please upload a valid file."
                )
        else:
            compressed.append(data)
    return compressed
