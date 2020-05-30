from flask import Blueprint, render_template
from flask_login import login_required, current_user

from freedebtapp import db
from freedebtapp.models import UserPersonalDetails, User

profiles = Blueprint('profiles', __name__)


@profiles.route('/profile')
@login_required
def profile():
    # user_details = User.query.filter_by(email = current_user.email)
    user_full = db.session.query(UserPersonalDetails).filter(UserPersonalDetails.email == current_user.email).all()
    user_table_full = db.session.query(User).filter(User.email == current_user.email).all()
    # user_personal = UserPersonalDetails.query.first()
    print("inside profile")

    user_name = user_table_full[0].name
    user_email = user_table_full[0].email

    user_occu = user_full[0].occupation

    if user_occu == 1:
        user_occ_name = "Student"
    else:
        user_occ_name = "Working Professional"

    user_personal = user_full[0]

    # user_occ_name = "Student"
    user_martial_status = user_personal.martial_status
    user_education = user_personal.education
    user_region = user_personal.region

    return render_template('homepages/profile.html',
                           name=user_name,
                           email=user_email,
                           occupation=user_occ_name,
                           martial=user_martial_status,
                           education=user_education,
                           region=user_region)
