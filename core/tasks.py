import time
from celery import shared_task

# allows you to call this function asynchronously
@shared_task
def send_mass_emails(recipient):
    print(recipient)
    print("Started to sleep")
    time.sleep(5)
    print("Woke up from sleep")
    return


@shared_task
def send_scheduled_emails():
    # get all those email addresses
    pass