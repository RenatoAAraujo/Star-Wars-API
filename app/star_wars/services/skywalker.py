from app.star_wars.services.integration import SWIntegration


def skywalker_films():
    """Return all Skywalkers film apperences"""
    star_wars = SWIntegration()

    skywalkers = star_wars.get_people("Skywalker")

    for i, _skywalker in enumerate(skywalkers):
        skywalkers[i]["films_data"] = star_wars.get_character_films(skywalkers[i]["films"])
        
        participated_films_string = skywalkers[i]["name"] + " participated in "
        for j, _film_data in enumerate(skywalkers[i]["films_data"]):
            if j != range(len(skywalkers[i]["films_data"]))[-1]:
                participated_films_string += _film_data["title"] + ", "
            else:
                participated_films_string += _film_data["title"] + "."

        skywalkers[i]["participated_films"] = participated_films_string

    return {"description": "".join([x["participated_films"] + " " for x in skywalkers])}
