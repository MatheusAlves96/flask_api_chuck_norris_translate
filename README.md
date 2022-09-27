# Voxus_api
Selection process voxus documentation

to get a random joke

    GET /api/jokes/random
    Returns a random joke.
    
    {
        "sucess": true,
        "joke_en": "Mick Jagger: \"oh you can't always get what you waaaannt.\" Chuck Norris \"Yes I can.\""
    } 

to get all categories

    GET /api/jokes/categories
    Returns all categories.
    
    {
        "sucess": true,
        "categories": [
            "animal",
            "career",
            "celebrity",
            "dev",
            "explicit",
            "fashion",
            "food",
            "history",
            "money",
    ................

to get a random joke from a category

    GET /api/jokes/category/{category}
    Returns a random joke from a category.
    
    {
        "sucess": true,
        "joke_en": "Chuck Norris doesn't play god. Playing is for children."
    }

to get a list of joke with text filter 

    GET /api/jokes/filter?limit={limit}&search={search}
    Returns a list of joke with text filter, limited by limit param.
    
    {
        "sucess": true,
        "joke_en": "Chuck Norris doesn't play god. Playing is for children."
    }

all endpoints with joke return have the pt_br parameter, which returns the translated joke
example:

to get a random joke with translate

    GET /api/jokes/random?pt_br=1
    Returns a random joke with translate.
    
    {
        "sucess": true,
        "joke_en": "Chuck Norris is forbidden from competing in paintball games... for very fucking obvious reasons.",
        "joke_pt_br": "Chuck Norris está proibido de competir em jogos de paintball... por razões óbvias."
    }

## Setup
``` 
git clone git@github.com:MatheusAlves96/Voxus_api.git
cd Voxus_api
pip install -r requirements.txt
python app.py
```