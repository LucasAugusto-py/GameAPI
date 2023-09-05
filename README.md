# GameAPI
Welcome to the GamesAPI, a Django-based API powered by Django Rest Framework. This API provides valuable data and insights related to user activity and game reviews. Below, you will find information about the available endpoints and how to use them.
# Data
You can find all data in this link: https://drive.google.com/drive/folders/1dR63HEtW0yKA4KgZtpYS8T0iRQknX8Jw?usp=drive_link
## Endpoints
1. User Data
+ __Endpoint__: games/api/userdata/<str:user_id >
+ __Description__: Retrieve user-specific data, including the total money spent, recommendation percentage, and the number of items associated with a given user ID.
+ __Example Usage__: games/api/userdata/12345
2. Count Reviews
+ __Endpoint__: games/api/countreviews/<str:start_date >&<str:end_date >
+ __Description__: Count the number of users who have submitted reviews within a specified date range and calculate the percentage of recommendations among those reviews.
+ __Example Usage__: games/api/countreviews/2023-01-01&2023-12-31
3. Genre Rank
+ __Endpoint__: games/api/genre/<str:genre >
+ __Description__: Retrieve the position of a specific genre within a ranking based on hours played for games in that genre.
+ __Example Usage__: games/api/genre/Action
4. User for Genre
+ __Enpoint__: userforgenre/<str:genre >
+ __Description__: Retrieve the top 5 users with the most hours played in the given genre, along with their user URL and user_id.
+ __Example Usage__: games/api/userforgenre/Action
5. Developer
+ __Endpoint__: games/api/developer/<str:developer >
+ __Description__: Get the number of items and the percentage of free content per year for a given name developer.
+ __Example Usage__: games/api/developer/Activision
6. Sentiment Analysis
+ __Endpoint__: games/api/sentiment/<str:year >
+ __Description__: Based on the release year, return a list with the count of user review records categorized with sentiment analysis.
+ __Example Usage__: games/api/sentiment/2013
7. ML Recomendation:
+ __Endpoint__: games/api/recommend/<int:game_id >
+ __Description__: Returns a recommended list of 5 games based on the genres, specs and game tags entered
+ __Example Usage__: games/api/recommend/10

# Getting Started
To get started with the GamesAPI, follow these steps:

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/GamesAPI.git
```
Navigate to the project directory:

```bash
cd GamesAPI
```
Install the required dependencies:

```bash
pip install -r requirements.txt
```
Set up your Django project and configure the database.

Run the development server:

```bash
python manage.py runserver
```

### Contributing
If you'd like to contribute to this project, feel free to fork the repository, make your changes, and submit a pull request. We welcome contributions in the form of bug fixes, new features, or improvements.

## Issues
If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. We appreciate your feedback and help in making this API better.

#### Thank you for using the GamesAPI! We hope you find it valuable for your gaming-related data needs.





