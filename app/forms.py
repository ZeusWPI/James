from datetime import datetime, timedelta
from flask.ext.login import current_user
from flask_wtf import Form
from wtforms import SelectField, DateTimeField, validators, SubmitField, HiddenField
from models import User, Location
from utils import euro

__author__ = 'feliciaan'


class OrderForm(Form):
    courrier_id = SelectField('Courrier', coerce=int)
    location_id = SelectField('Location', coerce=int, validators=[validators.required()])
    starttime = DateTimeField('Starttime', default=datetime.now)
    stoptime = DateTimeField('Stoptime')
    submit_button = SubmitField('Submit')

    def populate(self):
        if current_user.is_admin():
            self.courrier_id.choices = [(0, None)] + \
                                       [(u.id, u.username) for u in User.query.order_by('username')]
        else:
            self.courrier_id.choices = [(0, None), (current_user.id, current_user.username)]
        self.location_id.choices = [(l.id, l.name)
                                    for l in Location.query.order_by('name')]
        if self.stoptime.data is None:
            self.stoptime.data = datetime.now() + timedelta(hours=1)


class OrderItemForm(Form):
    food_id = SelectField('Item', coerce=int)
    submit_button = SubmitField('Submit')

    def populate(self, location):
        self.food_id.choices = [(i.id, (i.name + ": " + euro(i.price))) for i in location.food]