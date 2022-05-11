from os import getenv
import datetime
from app.auth.forms import login_form


def utility_text_processors():
    message = "hello world"
    form = login_form()

    def deployment_environment():
        return getenv('FLASK_ENV', None)

    def current_year():
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        return year

    return dict(
        form=form,
        mymessage=message,
        deployment_environment=deployment_environment(),
        year=current_year(),
    )
