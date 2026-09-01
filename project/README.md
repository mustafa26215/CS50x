# Personal Expense Tracker

#### Video Demo: https://youtu.be/8cIqv7lIyBI

## Description

Personal Expense Tracker is a simple web application that helps users keep track of their daily expenses. I created this project as my final project for CS50x. The main purpose of the application is to give the user an easy way to record expenses and review their spending in one place.

The application allows the user to add a new expense by entering the amount, choosing a category, writing a description, and selecting the date. For example, the user can choose a category such as Food, Transportation, Shopping, or Bills, and then write a short description such as "Lunch", "Taxi", or "Groceries". This makes each expense easier to understand when reviewing the list later.

After the user submits the form, the expense is stored in a SQLite database. The saved expenses are then displayed in a table on the main page. The table allows the user to see the important information about each expense, including its description, category, amount, and date.

The application also provides a category filter. Instead of viewing all expenses at the same time, the user can select a specific category and view only the expenses that belong to it. The application also calculates the total amount spent, allowing the user to quickly see the overall amount of money recorded in the application.

Another feature is deleting expenses. If an expense was added by mistake or is no longer needed, the user can delete it. Before the expense is deleted, the application asks the user for confirmation. This helps prevent an expense from being removed accidentally.

I decided to keep the project relatively simple and focus on the main functions that are useful for an expense tracker. I wanted the application to be easy to understand and use instead of adding a large number of features that were not necessary for the main purpose of the project.

## Features

* Add a new expense
* Enter the expense amount
* Choose an expense category
* Write a description for the expense
* Select the expense date
* Store expenses in a SQLite database
* Display saved expenses in a table
* Filter expenses by category
* Calculate total spending
* Delete expenses
* Confirm before deleting an expense
* Responsive design for smaller screens

## Technologies Used

### Python

Python is used as the main programming language for the application. It handles the application logic, processes user input, and communicates with the SQLite database.

### Flask

Flask is used as the web framework for the project. It handles the application routes and requests, receives information submitted by the user, works with the database, and sends the required information to the HTML templates.

### SQLite

SQLite is used as the database for storing expenses. Each expense contains information such as its amount, category, description, and date. I chose SQLite because it is lightweight, easy to use, and suitable for a small personal web application.

### HTML

HTML is used to create the structure of the web pages. The project uses a shared layout and a main page containing the expense form, category filter, total spending, and expense table.

### CSS

CSS is used to control the visual appearance of the application. It handles the layout, spacing, buttons, forms, tables, and responsive behavior for smaller screens.

### JavaScript

JavaScript is used to add interactive behavior to the application. It is used to display a confirmation message before the user deletes an expense.

## Project Structure

```text
project/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── layout.html
│   └── index.html
└── static/
    ├── style.css
    └── script.js
```

### app.py

`app.py` is the main Python file of the project. It contains the Flask application and the backend logic. It creates the SQLite database table if it does not already exist, handles the main routes, receives information from the expense form, stores expenses in the database, retrieves expenses, filters them by category, calculates the total, and handles deleting expenses.

### requirements.txt

`requirements.txt` contains the Python packages required by the project. In this project, Flask is the main external dependency.

### templates/layout.html

`layout.html` contains the shared HTML structure used by the application. It includes the basic HTML document structure, page title, link to the CSS file, header, and JavaScript file. It also provides a template block that allows other HTML pages to add their own content.

### templates/index.html

`index.html` is the main page of the application. It extends `layout.html` and contains the form for adding expenses, the category filter, the total spending section, and the table that displays the saved expenses.

### static/style.css

`style.css` contains the styling for the application. It controls the appearance and layout of the page, including the form, buttons, sections, table, and responsive behavior.

### static/script.js

`script.js` contains the JavaScript used for client-side interaction. It displays a confirmation dialog when the user tries to delete an expense.

### README.md

`README.md` is the documentation file for the project. It explains the purpose of the application, its features, technologies, project structure, usage, and design choices.

## How to Use

When the application is opened, the user is presented with the main expense tracker page. To add an expense, the user fills out the form by entering the amount, choosing a category, writing a description, and selecting the date.

After submitting the form, the application processes the information and stores the expense in the SQLite database. The new expense then appears in the table along with the other saved expenses.

The user can review the list of expenses and use the category filter to display expenses from a specific category. The total spending is also calculated and displayed so the user can quickly see the overall amount recorded.

If the user wants to remove an expense, they can select the delete option. A confirmation step appears before the deletion is completed. This gives the user an opportunity to cancel the action if they selected the wrong expense.

## Design Choices

One of the main design choices was using SQLite instead of a larger database system. Since this project is a small personal expense tracker, SQLite provides the required database functionality without adding unnecessary complexity.

I also chose Flask because it provides a straightforward way to build a web application using Python. It allows the backend logic, database operations, and HTML templates to work together without requiring a complicated framework.

Another design choice was using a shared `layout.html` template. This keeps common HTML elements in one place instead of repeating the same structure in every page. The main page can extend the layout and focus only on the content specific to the expense tracker.

I also kept the main functionality on one page. The user can add expenses, view the expense list, filter the list, see the total, and delete expenses without having to navigate through many different pages. I chose this approach because it makes the application easier to use and keeps the interface focused on its main purpose.

The application uses direct SQLite queries instead of an ORM. This keeps the database operations simple and makes it easier to understand how the application stores and retrieves the expense data.

I also included server-side validation when adding an expense. The application checks that the required information is provided and that the amount can be converted to a number before saving it to the database.

## What I Learned

While working on this project, I practiced connecting different parts of a web application together. I worked with Python and Flask for the backend, SQLite for data storage, and HTML, CSS, and JavaScript for the frontend.

I also gained more experience working with forms, handling user input, storing information in a database, retrieving data, filtering results, and displaying information on a web page.

The project helped me understand how the concepts learned throughout CS50x can be combined to create a complete application instead of solving individual programming problems.

Building the project also helped me understand the importance of keeping the code organized and choosing a simple solution when a complicated one is not necessary.

## AI Assistance Disclosure

AI was used as a supporting tool during the development of this project for a few routine tasks, such as minor code suggestions and documentation wording.

I reviewed and tested the code and made sure I understood the final implementation.
