import pandas as pd


def load_data(dataset):
    print("Loading data...")
    movies = pd.read_csv("./data/" + dataset + "/movies.csv")
    people = pd.read_csv("./data/" + dataset + "/people.csv")
    stars = pd.read_csv("./data/" + dataset + "/stars.csv")
    print("Data loaded.")

    return movies, people, stars


def actor_id(people: pd.DataFrame, name):
    actors_ids = people.loc[people["name"] == name]["id"].to_list()
    if not actors_ids:
        print(
            "I don't recognise any actors with the name '" + name + "'. "
            "Make sure the spelling is correct or try again with another actor."
        )
        return None
    elif len(actors_ids) == 1:
        return actors_ids[0]
    elif len(actors_ids) > 1:
        print(
            "Please specify which actor with the name '" + name + "' you mean. "
            "Respond with the number of your chosen actor as seen in the following list."
        )

        def fill_in(actor_id):
            actor_id = str(actor_id)
            while len(actor_id) < 7:
                actor_id = "0" + actor_id
            return actor_id

        for i in range(len(actors_ids)):
            print(
                str(i + 1) + ": https://www.imdb.com/name/nm" + fill_in(actors_ids[i])
            )

        ind = int(input()) - 1

        return actors_ids[ind]


def movies_of_actor(stars: pd.DataFrame, actor_id):
    return stars.loc[stars["person_id"] == actor_id]["movie_id"].to_list()


def actors_in_movie(stars: pd.DataFrame, movie_id):
    return stars.loc[stars["movie_id"] == movie_id]["person_id"].to_list()


def actor_name(people: pd.DataFrame, actor_id):
    return people.loc[people["id"] == actor_id]["name"].to_list()[0]


def movie_title_and_year(movies: pd.DataFrame, movie_id):
    return (
        movies.loc[movies["id"] == movie_id]["title"].to_list()[0],
        movies.loc[movies["id"] == movie_id]["year"].to_list()[0],
    )
