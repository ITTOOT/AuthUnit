from django.dispatch import receiver
from core.jwt.jwtMiddleware import breach_alert
from django.core.mail import send_mail


@receiver(breach_alert)
def handle_breach_alert(sender, user, ip_address, **kwargs):
    # Prepare the email content
    subject = 'Breach Alert: Unauthorized Login Attempt'
    message = f'An unauthorized login attempt was detected for user {user.username} from IP address {ip_address}. Please take appropriate action.'

    # Send the email notification
    send_mail(subject, message, 'admin@example.com', ['admin@example.com'])

    # Trigger an alert or take any other appropriate action
    # You can use logging, external service integration, or any other mechanism to trigger the alert

    # You can also update the user's status or perform additional actions based on the breach
    # For example, you might want to flag the user's account for further investigation or enforce additional security measures
