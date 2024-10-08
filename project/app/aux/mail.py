import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

FROM_EMAIL = "gsemen1918@gmail.com"
SENDGRID_CLIENT = SendGridAPIClient(os.environ.get('pafg pcwj ptjq ncyc'))


def send_mail(to_email, subject, html_content):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        response = SENDGRID_CLIENT.send(message)

        # log response
        print(response.status_code)
        print(response.body)
        print(response.headers)

        return response

    except Exception as e:
        print(e.message)
