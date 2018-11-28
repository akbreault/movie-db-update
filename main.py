from flask import Flask, session, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://movie-db:movie-db@localhost:8889/movie-db'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Movie(db.Model):
    release_year = db.Column(db.Integer)
    title = db.Column(db.String(500))
    origin = db.Column(db.String(500))
    director = db.Column(db.String(500))
    cast = db.Column(db.String(1000))     
    genre = db.Column(db.String(500))  
    wiki = db.Column(db.String(500))
    plot = db.Column(db.String(2000))

    def __init__(self, release_year, title, origin, director, cast, genre, wiki, plot):
        self.release_year = release_year
        self.title = title
        self.origin = origin
        self.director = director
        self.cast = cast 
        self.genre = genre
        self.wiki = wiki
        self.plot = plot
    
    def __repr__(self):
        return '<Movie %r>' % self.title


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/movies")
def movie_listing():

    if len(request.args) == 0:
        movies = Movie.query.all()
        
        if len(movies) > 0:
            return render_template('movies.html', movies=movies)

        else: 
            return render_template('movies.html')
    
    elif request.args.get('title') != None:
        title = request.args.get('title','')
        movie = Movie.query.filter_by(title=title).first()
        title = movie.title
        release_year = movie.release_year
        origin = movie.origin
        director = movie.director
        cast = movie.cast 
        genre = movie.genre
        wiki = movie.wiki
        plot = movie.plot

        return render_template('movie-page.html', movie=movie, title=title, release_year=release_year, origin=origin, director=director, cast=cast, genre=genre, wiki=wiki, plot=plot)


@app.route('/add', methods=['GET','POST'])
def add_movie():
    
    blank_error = ''

    if request.method == 'POST':
        release_year = request.form['release_year'] 
        title = request.form['title']
        origin = request.form['origin']
        director = request.form['director']
        cast = request.form['cast']
        genre = request.form['genre']
        wiki = request.form['wiki']
        plot = request.form['plot']

        if len(title) == 0 or len(release_year) == 0 or len(origin) == 0 or len(cast) == 0 or len(wiki) == 0 or len(plot) == 0 or len(director) == 0 or len(genre) == 0:
            blank_error = 'Please fill in all fields'

        #TODO: add in wiki link validation    

        if not blank_error:
            new_movie = Movie(release_year, title, origin, director, cast, genre, wiki, plot)
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/movies')
        else:
            return render_template('add-movie.html', blank_error=blank_error)

    return render_template('add-movie.html')


@app.route('/edit', methods=['GET','POST'])
def edit_movie():

    title = request.args.get('title','')
    movie = Movie.query.filter_by(title=title).first()

    if request.method == 'POST':
        release_year = request.form['release_year']
        if len(release_year) > 0: 
            movie.release_year = release_year
            db.session.commit()

        title = request.form['title']
        if len(title) > 0: 
            movie.title = title
            db.session.commit()

        origin = request.form['origin']
        if len(origin) > 0: 
            movie.origin = origin
            db.session.commit()

        director = request.form['director']
        if len(title) > 0: 
            movie.title = title
            db.session.commit()

        cast = request.form['cast']
        if len(cast) > 0: 
            movie.cast = cast
            db.session.commit()

        genre = request.form['genre']
        if len(genre) > 0: 
            movie.genre = genre
            db.session.commit()

        wiki = request.form['wiki']
        if len(wiki) > 0: 
            movie.wiki = wiki
            db.session.commit()
        #TODO: add in wiki link validation 

        plot = request.form['plot']
        if len(plot) > 0: 
            movie.plot = plot
            db.session.commit()

        return redirect('/movies')
    
    return render_template('edit-movie.html', movie=movie) #TODO: add empty_error


@app.route('/delete', methods=['GET','POST'])
def delete_movie():
    
    title = request.args.get('title', '')
    movie = Movie.query.filter_by(title=title).first()

    if request.method == 'POST':
        db.session.delete(movie)
        db.session.commit() 
        return redirect('/movies')

    return render_template('delete-movie.html', movie=movie)



@app.route('/search', methods=['GET','POST'])
def search():

    # TODO: make search case-insensitive

    except_error = ''
    empty_error = ''

    if request.method == 'POST':

        title = request.form['title']
        if len(title) > 0:
            try:
                movie = Movie.query.filter_by(title=title).first()
                id = movie.id
                return redirect("/movies?id="+ str(id))
            except AttributeError:
                except_error = "Sorry, no movies match your query"

        release_year = request.form['release_year']
        if len(release_year) > 0:
            try:
                movie = Movie.query.filter_by(release_year=release_year).first()
                id = movie.id
                return redirect("/movies?id="+ str(id))
            except AttributeError:
                except_error = "Sorry, no movies match your query"

        origin = request.form['origin']
        if len(origin) > 0:
            try:
                movie = Movie.query.filter_by(origin=origin).first()
                id = movie.id
                return redirect("/movies?id="+ str(id))
            except AttributeError:
                except_error = "Sorry, no movies match your query"

        director = request.form['director']
        if len(director) > 0:
            try:
                movie = Movie.query.filter_by(director=director).first()
                id = movie.id
                return redirect("/movies?id="+ str(id))
            except AttributeError:
                except_error = "Sorry, no movies match your query"

        genre = request.form['genre']
        if len(genre) > 0:
            try:
                movie = Movie.query.filter_by(genre=genre).first()
                id = movie.id
                return redirect("/movies?id="+ str(id))
            except AttributeError:
                except_error = "Sorry, no movies match your query"

        if len(title) == 0 and len(release_year) == 0 and len(origin) == 0 and len(director) == 0 and len(genre) == 0:
            empty_error = "Please enter at least one search term"

    return render_template('search.html', except_error=except_error, empty_error=empty_error)


if __name__ == "__main__":
    app.run()

