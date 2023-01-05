def jwt_response_payload_handler(token, user=None, request=None):
    user_ip = request.META.get('REMOTE_ADDR')
    return {
        'user': user.username,
        'token': token,
        'user_ip': user_ip,
    }
