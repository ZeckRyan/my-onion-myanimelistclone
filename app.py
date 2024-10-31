from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "db_anime"
mysql = MySQL(app)

@app.route('/home')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM animes ORDER BY created_at DESC") 
    animes = cur.fetchall()
    cur.close()
    return render_template('home.html', animes=animes)

@app.route('/add', methods=['GET', 'POST'])
def add_anime():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = request.form.get('rating', '0')
        try:
            ratingInt = int(rating)
        except ValueError:
            ratingInt = 1 
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO animes(title, genre, rating) VALUES(%s, %s, %s)",
            (title, genre, ratingInt))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    return render_template('add_anime.html')

@app.route('/delete/<int:anime_id>')
def delete_anime(anime_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM animes WHERE id = %s", (anime_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('home'))

@app.route("/edit/<int:anime_id>", methods=["GET", "POST"])
def edit_anime(anime_id):
    cur = mysql.connection.cursor()
    
    if request.method == "POST":
        new_title = request.form.get("title")
        new_genre = request.form.get("genre")
        new_rating = request.form.get("rating")

        new_rating_int = int(new_rating)
        cur.execute(
            "UPDATE animes SET title = %s, genre = %s, rating = %s WHERE id = %s",
            (new_title, new_genre, new_rating_int, anime_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('home'))
    else:
        cur.execute("SELECT * FROM animes WHERE id = %s", (anime_id,))
        anime = cur.fetchone()
        cur.close()
        
        if anime:
            return render_template("edit.html",
                                   title=anime[1],
                                   genre=anime[2],
                                   rating=anime[3])
        else:
            return "Anime not found", 404

@app.route('/comedy')
def genre_comedy():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM animes WHERE genre = %s", ("Comedy",))
    comedy_animes = cur.fetchall()
    cur.close()
    return render_template('genre_comedy.html', animes=comedy_animes)

@app.route('/horror')
def genre_horror():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM animes WHERE genre = %s", ("Horror",))
    horror_animes = cur.fetchall()
    cur.close()
    return render_template('genre_horror.html', animes=horror_animes)

@app.route('/isekai')
def genre_isekai():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM animes WHERE genre = %s", ("Isekai",))
    isekai_animes = cur.fetchall()
    cur.close()
    return render_template('genre_isekai.html', animes=isekai_animes)

@app.route('/romance')
def genre_romance():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM animes WHERE genre = %s", ("Romance",))
    romance_animes = cur.fetchall()
    cur.close()
    return render_template('genre_romance.html', animes=romance_animes)


if __name__ == '__main__':
    app.run(debug=True)
