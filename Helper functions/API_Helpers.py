def handle_response_code(response):
    status = response.status_code
    # Check the status code
    if status < 200:
        print('informational')
        # If the status code is 200, treat the information.
    elif status >= 200 and status < 300:
        print('Connection is established')
        # okBehavior(response) # runs the function to get list of archives
    elif status >= 300 and status < 400:
        print('redirection')
    elif status >= 400 and status < 500:
        print('client error')
    else:
        print('server error')