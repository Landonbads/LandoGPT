# LandoGPT
https://www.landogpt.xyz/

## What is this project? 
A website that emulates chatgpt, but goes on a per-request basis instead of the monthly subscription for GPT-4. Communicates with the OpenAI API with version GPT-4 Turbo (gpt-4-1106-preview).

## Why I built the project
I wanted to gain experience with API interaction, user authentication, and database management. I think building out this project was a cool way to learn new technologies and how openai's API works.

## Technologies used
- Flask to facilitate the web development process (routes, templates, requests, etc.)
- Postgresql database provided by heroku (migrated from sqlite3) 
- Flask's sqlalchemy to communicate with the database (converting my python objects to SQL tables and converting python code to equivalent SQL queries)
- Bcrypt to hash passwords before storing in database
- Combination of html, css, javascript, and bootstrap for frontend
- Hosted via heroku

## Things to note
- Requests get more expensive as the conversation with the chat bot continues. This is because with every subsequent request the previous chat history is sent to keep context.
- Stripe payment is currently in test mode to demonstrate functionality (please don't drain my balance)
