def handler(event, context):
    print(event)

    response = {"version": "0-0-1"}
    response.update(event)

    return response
