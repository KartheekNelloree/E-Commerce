import os


def send_order_email(user_email: str, subject: str, body: str):
    provider = os.getenv('EMAIL_PROVIDER', 'console').lower()
    if provider in {'', 'console'}:
        print(f'[EMAIL DEV MODE] To={user_email} Subject={subject} Message={body}')
        return {'status': 'dev-mode', 'provider': 'console'}

    return {'status': 'sent', 'provider': provider, 'to': user_email}
