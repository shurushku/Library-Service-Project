# Library-Service-Project
There is a library, where you can borrow books and pay for your borrowings using cash, depending on the days you read the book.
The problem is, that the system of tracking books, borrowings, users & payments in the library is outdated - everything is done manually and all tracking is performed on paper. There is no possibility to check the inventory of specific books in the library. Also, you are obliged to pay with cash (no credit card support). Library administration never knows, who returned the book in time, and who did not.

In this project, you will be fixing all these problems. And to do so, you’ll implement an online management system for book borrowings. The system will optimize the work of library administrators and will make the service much more user-friendly.

### Functional:
* Web-based
* Manage books inventory
* Manage books borrowing
* Manage customers
* Display notifications
* Handle payments
### Non-functional:
* 5 concurrent users
* Up to 1000 books
* 50k borrowings/year
* ~30MB/year

## Installation
Python3 must be installed
```shell
git clone https://github.com/shurushku/library-service-project.git
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Create file ```.env``` by example ```.env.sample``` in the root of the project

## Components
### Books Service
Managing books amount (CRUD for Books)
```
POST:         books/           - add new 
GET:          books/           - get a list of books
GET:          books/<id>/      - get book's detail info 
PUT/PATCH:    books/<id>/      - update book (also manage inventory)
DELETE:       books/<id>/      - delete book
```
### Users Service
Managing authentication & user registration
```
POST:         users/                  - register a new user 
POST:         users/token/            - get JWT tokens 
POST:         users/token/refresh/    - refresh JWT token 
GET:          users/me/               - get my profile info 
PUT/PATCH:    users/me/               - update profile info 
```
For registration is_staff user
```shell
python manage.py createsuperuser
```
### Borrowings Service
Managing users' borrowings of books
```
POST:   borrowings/                             - add new borrowing (when borrow book - inventory should be made -= 1) 
GET:    borrowings/?user_id=...&is_active=...   - get borrowings by user id and whether is borrowing still active or not.
GET:    borrowings/<id>/                        - get specific borrowing 
POST: 	borrowings/<id>/return/                 - set actual return date (inventory should be made += 1)
```
### Notifications Service (Telegram):
Notifications about new borrowing created, borrowings overdue & successful payment
Asynchronous (Django Q package or Django Celery will be used)
Other services interact with it to send notifications to library administrators.
Usage of Telegram API, Telegram Chats & Bots.
### Payments Service (Stripe):
Perform payments for book borrowings through the platform.
Interact with Stripe API using the `stripe` package.
```
GET:    success/    - check successful stripe payment
GET:    cancel/     - return payment paused message 
```
View Service (Delegated to the Front-end Team):
Front-end interface for communication with Library API.
Will not be implemented here.
