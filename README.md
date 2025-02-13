# Collections
A human sees the world and it's things as fragments of humans. Therefore it's items should be interrelated to humans themselves, as it simpifies data points for such items.

## V0
- metadata about a movie or show, like described in imdb.com, I feel, is analogous to human data. Therefore, will be the structure of the each item within the database.
- Utilize docker and the REST API from flask to interface which such dockers.
- Create a CRUD interface for such docker, utilizing a context manager
    - Maybe even having user based sessions to maintain a context manager???
- bundle everything together efficiently (docker-compose)
- Display information about the database, specified port.
- Config file to handle that sort of stuff... (default user, pass, and db names.)
