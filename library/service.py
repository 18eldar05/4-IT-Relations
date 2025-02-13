import datetime
from datetime import datetime, timezone
import time
from django.core.mail import send_mail
from library.serializer import *


def send():
    users = User.objects.all()
    mails = []
    for user in users:
        debts = Issuance.objects.filter(reader=user.pk, is_returned=False)
        if debts.exists():
            data = ""
            for debt in debts:
                return_date = time.asctime(debt.date_of_return.timetuple())
                remaining = debt.date_of_return - datetime.now(timezone.utc)
                data = data + f"Name: {debt.book.name}, return date: {return_date}, time remaining: {remaining.days} days\n"
            send_mail(
                "Don't forget to return your books to the library",
                f"List of debts:\n{data}",
                "18eldar054@gmail.com",
                [user.email],
                fail_silently=False,
            )
            mails.append({"email": user.email, "data": data})
    return mails
