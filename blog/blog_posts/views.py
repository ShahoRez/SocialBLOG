from os import abort
from flask import url_for, redirect, flash, render_template, request, Blueprint
from flask_login import current_user, login_required
from blog import db
from blog.models import BlogPost
from blog.blog_posts.forms import BlogPostForm


blog_posts = Blueprint("blog_posts", __name__)



#CREATE
@blog_posts.route('/create', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    
    if form.validate_on_submit():
        title = form.title.data
        text = form.text.data
        
        new_post = BlogPost(title=title, text=text, user_id= current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('core.index'))
    
    return render_template('create_post.html', form=form)
    
            
#View
@blog_posts.route('/posts', methods=['GET'])
def posts():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(
        BlogPost.date.desc()).paginate(page=page, per_page=5)
    
    print(page)
    return render_template('posts.html', blog_posts=blog_posts, page=page)

#View a Post
@blog_posts.route('/posts/<int:blog_post_id>', methods=['GET'])
def blog_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', post=post)
    
#UPDATE
@blog_posts.route('/posts/<int:blog_post_id>/update', methods=['GET', 'POST'])
def update_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    
    if post.author != current_user:
        abort(403)
        
    form = BlogPostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('blog_posts.blog_post', blog_post_id=post.id))
    
    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text
        
    return render_template(
        'create_post.html',
        post=post,
        title = 'Updating post',
        form=form
        )


#DELETE
@blog_posts.route('/<int:blog_post_id>', methods=['DELETE', 'POST'])
def delete_post(blog_post_id):
    post = BlogPost.query.get_or_404(blog_post_id)
    
    if post.author != current_user:
        abort(403)
        
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('blog_posts.posts'))