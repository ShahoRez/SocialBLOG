# users/views.py

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from blog import db, login_manager
from blog.models import BlogPost, User
from blog.users.forms import (LoginForm, RegistrationForm,
                                        UpdateUserForm)
from blog.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# register
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(
            username=form.username.data).first()
        if existing_user:
            flash(
                "Username already exists. Please choose a different one.",
                "danger"
                )
            return redirect(url_for('users.register'))

        # Check if the email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash(
                "Email already exists. Please choose a different one.",
                "danger"
            )
            return redirect(url_for('users.register'))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created! You can now log in.", 'success')
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)



# login
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User fetched: {user.username if user else 'No user found'}")
        # Check if user exists
        if user is None:
            flash(
                "Email not found. Please check your email and try again.",
                "danger"
                )
            return redirect(url_for("users.login"))

        # Now it's safe to check the password
        if user.check_password(form.password.data):
            login_user(user)
            print(f"Logged in user: {current_user.username}")  # Should print user2
            flash("Login is successful", "success")

            next = request.args.get("next")

            if next is None or not next.startswith("/"):
                next = url_for("core.index")
            
            
            return redirect(next)

    return render_template("login.html", form=form)



# update
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()
    print(f"Current user before update: {current_user.username}")  # Debugging line

    if form.validate_on_submit():
        if form.profile_image.data:
            username = current_user.username
            print(username)
            pic = add_profile_pic(form.profile_image.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        # Reload the current user to ensure the session is up to date
        load_user(current_user.id)  # This ensures the current_user is refreshed
        print(f"Current user after update: {current_user.username}")  # Debugging line

        flash("Account updated!", 'success')
        return redirect(url_for("users.account"))

    form.username.data = current_user.username
    form.email.data = current_user.email

    profile_image = url_for("static", filename="profile_pic/" + current_user.profile_image)

    return render_template("account.html", form=form, profile_image=profile_image)


@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(user_id=user.id).order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template(
        "user_blog_posts.html", user=user, blog_posts=blog_posts
        )
