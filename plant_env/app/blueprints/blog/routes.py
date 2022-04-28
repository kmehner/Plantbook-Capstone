from numpy import add_newdoc
from . import blog
from flask import redirect, render_template, url_for, flash
from flask_login import login_required, current_user
from .forms import HealthForm, PhotoForm, PostForm, SearchForm, PlantForm, WaterForm
from .models import Plant, PlantBook, Post

@blog.route('/')
def index():
    title = 'Home'
    posts = Post.query.all()
    return render_template('index.html', title=title, posts=posts)

# Alter create post to take in plant_id and category (depending where it is called from)
@blog.route('/create-post/<plant_id>/<category>', methods=['GET', 'POST'])
@login_required
def create_post(plant_id, category):
    plant = Plant.query.get_or_404(plant_id)
    water_measurements = []

    # Calling the template
    if category == 'health_issues':
        title = form = HealthForm()
        title = 'Health Issue'
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            image = form.image.data
            new_post = Post(title=title, body=body, user_id=current_user.id, category=category, plant_id=plant_id)
            if image:
                new_post.upload_to_cloudinary(image)
            flash(f"{new_post.title} has been created", 'secondary')
            return redirect(url_for('blog.plantbook_more_info', plant_id = plant_id, category=category))

    elif category == 'watering_schedule':
        form = WaterForm()
        title = 'Watering Schedule'
        water_measurements = ['Fluid Ounce', 'Liter', 'Cup', 'Mililiter']
        if form.validate_on_submit():
            water_quantity = form.water_quantity.data
            water_measurement = form.water_measurement.data
            frequency_int = form.frequency_int.data
            frequency_measurement = form.frequency_measurement.data
            new_post = Post(water_quantity=water_quantity, water_measurement=water_measurement, frequency_int=frequency_int, frequency_measurement=frequency_measurement, user_id=current_user.id, category=category, plant_id=plant_id)

            flash(f"Watering schedule has been created", 'secondary')
            return redirect(url_for('blog.plantbook_more_info', plant_id = plant_id, category=category))
 
    elif category == 'photo_diary':
        form = PhotoForm()
        title = 'Photo Diary'
        if form.validate_on_submit():
            body = form.body.data
            new_post = Post(body=body, user_id=current_user.id, category=category, plant_id=plant_id)
            flash(f"A new photo entry has been created", 'secondary')
            return redirect(url_for('blog.plantbook_more_info', plant_id = plant_id, category=category))

    else: 
        form = PostForm()
        title = 'Post'
        if form.validate_on_submit():
            title = form.title.data
            body = form.body.data
            image = form.image.data
            new_post = Post(title=title, body=body, user_id=current_user.id, category=category, plant_id=plant_id)
            if image:
                new_post.upload_to_cloudinary(image)
            flash(f"{new_post.title} has been created", 'secondary')
            return redirect(url_for('blog.plantbook_more_info', plant_id = plant_id, category=category))

    return render_template('create_post.html', title=title, form=form, plant_id=plant_id, category=category, plant=plant, water_measurements=water_measurements)



# @blog.route('/my-posts')
# @login_required
# def my_posts():
#     title = 'My Posts'
#     posts = current_user.posts.all()
#     return render_template('my_posts.html', title=title, posts=posts)


# Get all posts that match search (need to update to new postform format, might not exist for a little)
@blog.route('/search-posts', methods=['GET', 'POST'])
def search_posts():
    title = 'Search'
    form = SearchForm()
    posts = [] 
    if form.validate_on_submit():
        term = form.search.data
        posts = Post.query.filter( (Post.title.ilike(f'%{term}%')) | (Post.body.ilike(f'%{term}%')) ).all()
    return render_template('search_posts.html', title=title, posts=posts, form=form)


# Get A Single Post by ID
@blog.route('/posts/<post_id>')
@login_required
def single_post(post_id):
    post = Post.query.get_or_404(post_id)
    title = post.title
    return render_template('post_detail.html', title=title, post=post)


# Edit a Single Post by ID
@blog.route('/edit-posts/<post_id>/<plant>', methods=["GET", "POST"])
@login_required
def edit_post(post_id, plant):
    post = Post.query.get_or_404(post_id)
    category = post.category

    if post.author != current_user:
        flash('You do not have edit access to this post.', 'danger')
        return redirect(url_for('blog.plantbook_more_info', plant_id=post.plant_id, category=category))
    
    title = f"Edit post"

    if category=='watering_schedule':
        form = WaterForm()
    elif category=='health_issues':
        form = HealthForm()
    elif category=='photo_diary':
        form = PhotoForm()
    else:
        form = PostForm()
    
    if form.validate_on_submit():
        post.update(**form.data)
        flash(f'The post has been updated', 'success')
        return redirect(url_for('blog.plantbook_more_info', plant_id=post.plant_id, category=category))


    return render_template('post_edit.html', title=title, post=post, form=form, category=category, plant=plant)


@blog.route('/delete-posts/<post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You do not have delete access to this post', 'danger')
    else:
        post.delete()
        flash(f'{post.title} has been deleted.', 'secondary')
    return redirect(url_for('blog.plantbook_more_info', plant_id=post.plant_id, category=post.category))


# ------------------- Plants ----------------------
@blog.route('/all-plants')
@login_required
def all_plants():
    title = 'All Plants'
    plants = Plant.query.all()
    return render_template('all_plants.html', title=title, plants=plants)

# ------------ Plant database functionality ------------

# Will be backend way to edit plant (no user_id attached to plant so whoever has access to this can edit/delete)
@blog.route('/my-plants', methods=['GET', 'POST'])
@login_required
def my_plants():
    title = 'My Plants'
    form = SearchForm()
    plants = Plant.query.all()

    if form.validate_on_submit():
        term = form.search.data
        plants = Plant.query.filter( (Plant.common_name.ilike(f'%{term}%')) | (Plant.scientific_name.ilike(f'%{term}%')) ).all()

    return render_template('my_plants.html', title=title, plants=plants, form=form)


@blog.route('/register-plant', methods=['GET', 'POST'])
@login_required
def register_plant():
    form = PlantForm()
    title = 'Register New Plant'
    if form.validate_on_submit():
        common_name = form.common_name.data
        scientific_name = form.scientific_name.data
        content = form.content.data
        image_url = form.image.data
        # Image Error: Cannot adapt filetype to image
        new_plant = Plant(common_name=common_name, scientific_name=scientific_name, content=content)
        # if image:
        #     new_plant.upload_to_cloudinary(image)
        flash(f"{new_plant.common_name} has been created", 'secondary')
        return redirect(url_for('blog.search_plants'))
    return render_template('register_plant.html', title=title, form=form)

@blog.route('/search-plants', methods=['GET', 'POST'])
def search_plants():
    title = 'Search'
    form = SearchForm()
    plants = Plant.query.all()

    # for plant in plants, if plant in user_plants display quantity
    # plantbook.count(plant)? * still figuring this out 
    user_plants = current_user.plants.all()

    if form.validate_on_submit():
        term = form.search.data
        plants = Plant.query.filter( (Plant.common_name.ilike(f'%{term}%')) | (Plant.scientific_name.ilike(f'%{term}%')) ).all()
    return render_template('all_plants.html', title=title, plants=plants, form=form, user_plants=user_plants)

@blog.route('/edit-plants/<plant_id>', methods=["GET", "POST"])
@login_required
def edit_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    title = f"Edit {plant.common_name}"
    form = PlantForm()
    if form.validate_on_submit():
        plant.update(**form.data)
        flash(f'{plant.common_name} has been updated', 'warning')
        return redirect(url_for('blog.my_plants'))

    return render_template('plant_edit.html', title=title, plant=plant, form=form)

@blog.route('/delete-plant/<plant_id>')
@login_required
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    plant.delete()
    flash(f'{plant.common_name} has been deleted.', 'secondary')
    return redirect(url_for('blog.my_plants'))

# --------------- Plantbook ----------- (move inside base?)

@blog.route('/my-plantbook', methods=['GET', 'POST'])
@login_required
def my_plantbook():
    form = SearchForm()
    user_plants = current_user.plants.all()
    plants = user_plants

    if form.validate_on_submit():
        plants = []
        term = form.search.data
        plant_search = Plant.query.filter( (Plant.common_name.ilike(f'%{term}%')) | (Plant.scientific_name.ilike(f'%{term}%')) ).all()
        for plant in plant_search:
            if plant in user_plants:
                plants.append(plant)

    return render_template('my_plantbook.html', user_plants=user_plants, plants=plants, form=form)


@blog.route('/add-to-my-plantbook/<plant_id>' , methods=['GET', 'POST'])
@login_required
def add_to_my_plantbook(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    plantbook = current_user.plants.all()

    if plant not in plantbook:
        plant_id = plant.id
        user_id = current_user.id
        new_plantBook = PlantBook(plant_id=plant_id, user_id=user_id)
        flash(f"{plant.common_name} has been added to your Plantbook!", "success")
    else:
        flash(f"{plant.common_name} already in your Plantbook!", "danger")
        return redirect(url_for('blog.search_plants'))
    # Change to whatever page the user was on
    return redirect(url_for('blog.search_plants'))

@blog.route('/delete-from-my-plantbook/<plant_id>')
@login_required
def delete_from_my_plantbook(plant_id):
    plant_to_delete = Plant.query.get_or_404(plant_id)
    current_user_id = current_user.id
    
    plant = PlantBook.query.filter( (PlantBook.plant_id == plant_id) and (PlantBook.user_id == current_user_id) ).first()
    if plant:
        plant.delete()
        flash(f'{plant_to_delete.common_name} has been removed from your Plantbook.', 'secondary')
    else:
        flash(f'There was an error removing {plant_to_delete.common_name} from your Plantbook', "danger")
    return redirect(url_for('blog.my_plantbook'))

# -------------- Inside plantbook --------


@blog.route('/plantbook-home/<plant_id>' , methods=['GET', 'POST'])
@login_required
def plantbook_home(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    
    return render_template("plantbook_base.html", plant=plant)

# Can add this to main dictionary as button ("Get info")
@blog.route('/plant-info/<plant_id>' , methods=['GET', 'POST'])
@login_required
def plant_info(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    return render_template("plant_info.html", plant=plant)



# Display page based on category 
@blog.route('/plantbook/<plant_id>/<category>', methods=['GET', 'POST'])
@login_required
def plantbook_more_info(plant_id, category):
 
    plant = Plant.query.get_or_404(plant_id)
    plant_id = plant_id
    # current_user
    current_user_id = current_user.id
    # category 
    category=category

    # Query for posts you want from the posts (we need this id)
    posts = Post.query.filter( Post.plant_id == plant_id, Post.user_id == current_user_id, Post.category == category).all()
    
    # Return render_template for basic display 
    return render_template(f'plantbook_more_info.html', plant=plant, posts=posts, category=category)









