# IS211_FinalProjectBookApp

I chose to do the book application, and decided to break down my app into:
displaying books, searching books, adding books, and deleting books.

I utilized FLASK as well as the SQL Alchemy flask extension for my database needs.

To display, I used an embedded loop to iterate through the Books table.

To search, I saved the ISBN input as a variable, and used it within the Google Books API call.

Search for book ISBN's here: https://books.google.com/

To add, I used an ISBN table to save the user's last input value from their search (the ISBN) and 
then inserted that into another API call to store into the Books table.

To delete, I tried to add a 'delete' button for each row, but I couldn't quite nail down functionality.
So instead, I added a user input form to select each row (single book entry) for deletion.

**EXTRA TIPS!!!**

-AFTER ISBN INPUT, REMEMBER TO HIT THE SEARCH BUTTON TO SEARCH Google Books API.

-WHEN ISBN IS FOUND, THE BOOK TITLE WILL APPEAR BELOW SEARCH FIELD.

-ONLY THEN YOU WILL BE ABLE TO ADD IT TO THE BOOK COLLECTION.

-THE TITLE WILL THEN DISAPPEAR WHEN BOOK IS ADDED SUCCESSFULLY.