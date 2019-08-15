# Data Camp Course Scrapper

## Libraries used
- os
- Requests
- BeautifulSoup (**lxml** parser)
- fake_useragent
- selenium

## Working bits of the program
This Program takes **Data Camp** `User ID` and `Password` to login to the Datacamp account 

Once logged in, The program takes a **_Course URL_** Like 'https://www.datacamp.com/courses/cleaning-data-with-apache-spark-in-python' and `Id` of the course and additional few options and starts to download the neccessary videos and screenshots of the given `Data Camp Course` 
