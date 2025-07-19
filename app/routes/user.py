from flask import Blueprint, render_template, request, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..functions import save_picture
from ..extensions import db
from ..forms import RegistrationForm, LoginForm
from ..models.user import User


user = Blueprint('user', __name__)


@user.route('/user/list', methods=['GET'])
@login_required
def user_list():
    return render_template('/user/all.html', users=User.query.all())


@user.route('/user/create', methods=['GET', 'POST'])
@login_required
def create():
    username = request.form.get('user_name')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')
    email = request.form.get('email')
    subscription = request.form.get('subscription')

    if request.method == 'POST':
        try:
            hash_pwd = generate_password_hash(password)
            user = User(username=username,
                        firstname=firstname,
                        lastname=lastname,
                        password=hash_pwd,
                        email=email,
                        plan=subscription)
            db.session.add(user)
            db.session.commit()
            return redirect('/user/list')
        except Exception as e:
            print('Adding User Failed', str(e))
            db.session.rollback()

    return render_template('user/create.html')


@user.route('/user/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    user = User.query.get(id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.firstname = request.form.get('firstname')
        user.lastname = request.form.get('lastname')
        user.email = request.form.get('email')

        try:
            db.session.commit()
            return redirect('/user/list')
        except Exception as e:
            print('Updating User Failed', str(e))
            db.session.rollback()
    else:
        return render_template('user/update.html', user=user)


@user.route('/user/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = User.query.get(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/user/list')
    except Exception as e:
        print('Deleting User Failed', str(e))
        db.session.rollback()


# @user.route('/user/login', methods=['GET', 'POST'])
# def login_page():
#     login = request.form.get('login')
#     password = request.form.get('password')
#     if login and password:
#         user = User.query.filter_by(username=login).first()
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             next_page = request.args.get('next')
#             # flash(f"You have been logged in as {user.username}", "success")
#             return redirect(next_page) if next_page else redirect(url_for('main.index'))
#         else:
#             flash(f"Login or password incorrect", "danger")
#     # else:
#     #     flash("Please check your login and password")
#
#     return render_template('user/login.html')
#     #return render_template('main/index.html')

@user.route('/user/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username and password:
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('user/login.html', form=form)


# @user.route('/user/register', methods=['GET', 'POST'])
# def register():
#     login = request.form.get('login')
#     password = request.form.get('password')
#     password2 = request.form.get('password2')
#     email = request.form.get('email')
#
#     if request.method == 'POST':
#         if not (login or password or password2):
#             flash(f"Please, fill all fields.", "danger")
#         elif password != password2:
#             flash(f"Passwords do not match", "danger")
#         else:
#             hash_pwd = generate_password_hash(password)
#             new_user = User(username=login, password=hash_pwd, email=email)
#             try:
#                 db.session.add(new_user)
#                 db.session.commit()
#                 flash(f"You have successfully registered.", "success")
#                 return redirect(url_for('user.login_page'))
#             except Exception as e:
#                 print(str(e))
#                 flash(f"Error occurred", "danger")
#     return render_template('user/register.html')


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pwd = generate_password_hash(form.password.data)
        avatar_filename = save_picture(form.avatar.data)
        new_user = User(username=form.username.data,
                        password=hash_pwd,
                        email=form.email.data,
                        avatar=avatar_filename)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f"You have successfully registered.", "success")
            return redirect(url_for('user.login_page'))
        except Exception as e:
            print(str(e))
            flash(f"Registration Failed", "danger")
    # else:
    #     #print('Registration Failed')

    return render_template('user/register.html', form=form)


@user.route('/user/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login_page'))


@user.after_request
def redirect_to_login(response):
    if response.status_code == 401:
        return redirect(url_for('user.login_page') + '?next=' + request.url)

    return response
