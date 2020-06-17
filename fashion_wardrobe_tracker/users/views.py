from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from ..data import BodyBuild, BodyShape
from ..helpers import generate_selection
from .forms import LoginForm, RegistrationForm, UserProfileForm, current_user
from .models import User, Profile


users = Blueprint('users', __name__)


@users.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form.user)
        flash("Logged in successfully.")
        current_app.logger.info('user logged in')
        if not current_user.profile:
            return redirect(url_for('users.create_profile', user_id=form.user.id))
        return redirect(request.args.get("next") or url_for("wardrobe.landing"))
    
    if form.errors:
        flash("Login Unsuccessful.")
        error_types = form.errors.keys()
        for each_err in error_types:
            errors = form.errors[each_err]
            for each in errors:
                flash("  " + each)
    return render_template('users/login.html', form=form)


@users.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User.create(**form.data)
        login_user(user)
        if not user.profile:
            return redirect(url_for('users.create_profile', user_id=user.id))
        else:
            return redirect(url_for('wardrobe.index'))

    if form.errors:
        flash("Login Unsuccessful.")
        error_types = form.errors.keys()
        for each_err in error_types:
            errors = form.errors[each_err]
            for each in errors:
                flash("  " + each)

    return render_template('users/register.html', form=form)



@users.route('/user/<int:user_id>', methods=('GET', 'POST'))
@login_required
def create_profile(user_id):
    user = User.query.filter(User.id==user_id).first()

    if not user.id == user_id:
        abort(401)

    if user.profile_exists():
        profile = Profile.query.filter(Profile.UserID==user.id).first()
        form = UserProfileForm(obj=profile)
        form.build.choices = generate_selection(BodyBuild, 'build')
        form.build.default = profile.build
        form.shape.choices = generate_selection(BodyShape, 'shape')
        form.shape.default = profile.shape

        if form.validate_on_submit():
            flash("Profile Update Successful")
            profile.update(**form.data)
            return redirect(url_for('wardrobe.wardrobe_user',
                                        user_id=profile.UserID))

    else:
        form = UserProfileForm()
        form.build.choices = builds_selection
        form.shape.choices = shapes_selection
        if form.validate_on_submit():
            flash("Profile Creation Successful.")
            profile = Profile.create(**form.data)
            profile.update(**{'UserID': user_id})
            user.profile=profile
            print(f"User Profile: {user.profile}")
            print(f"Profile User: {profile.user}")
            current_app.logger.info(f'New profile created for User: {user_id}')
            return redirect(url_for('wardrobe.wardrobe_user', user_id=profile.UserID))

    if form.errors:
        flash("Profile Creation Unsuccessful.")
        error_types = form.errors.keys()
        for err in error_types:
            e_type = form.errors[err]
            for x in e_type:
                flash(f"  {x}: {err}")

    return render_template('users/profile.html', form=form, user_id=user_id)
        
        


@users.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('wardrobe.index'))