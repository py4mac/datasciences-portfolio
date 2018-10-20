
# Movie Recommendation Engine Project

This project aims to build movie recommendation engine.

## Project structure


- [EDA](notebook_cleaning_and_exploration.ipynb) - Analyse and explore Dataset

Tags: KMeans, NearestNeighbors.

- [Api](api/) - Create a generic API to used the previously built model.

Tags: Flask

```bash
// Collect list of films
$wget -O - http://localhost:5000/film/

{
    "_results": "[{\"name\": \"Avatar\", \"id\": 0}, {\"name\": \"Pirates of the Caribbean: At World's End\", \"id\": 1}, {\"name\": \"Spectre\", \"id\": 2}, {\"name\": \"The Dark Knight Rises\", \"id\": 3}, ....]"
}
```

```bash
// Recommend movie by id 
$wget -O - http://localhost:5000/recommend/?id=228

{
  "_results": "[{\"name\": \"Star Wars: Episode II - Attack of the Clones\", \"id\": 229}, {\"name\": \"Star Wars: Episode I - The Phantom Menace\", \"id\": 232}, {\"name\": \"Star Wars: Episode VI - Return of the Jedi\", \"id\": 1476}, {\"name\": \"Man of Steel\", \"id\": 14}, {\"name\": \"Star Wars: Episode IV - A New Hope\", \"id\": 2864}]"
}
```
