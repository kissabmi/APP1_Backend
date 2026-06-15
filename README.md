# Project Backend 05 — Python_Bootcamp

**Summary:**  
In this project, you will learn how to work with JWT authorization and extend the capabilities of web applications in Python using Flask.

💡 [Click here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) to share your feedback on this project. It’s anonymous and helps our team improve the learning experience. We recommend completing the survey immediately after finishing the project.

## Contents

  - [Chapter I](#chapter-i)
    - [Instructions](#instructions)
  - [Chapter II](#chapter-ii)
    - [General Informatiom](#general-informatiom)
      - [Token, Session Token, Refresh Token](#token-session-token-refresh-token)
      - [Topics to Study](#topics-to-study)
  - [Chapter III](#chapter-iii)
  - [Project: Tic-Tac-Toe](#project-tic-tac-toe)
    - [Task 1. Switching from Basic Authorization to JWT](#task-1-switching-from-basic-authorization-to-jwt)
    - [Task 2. Adding Game History Support](#task-2-adding-game-history-support)
    - [Task 3. Adding Leaderboard Support](#task-3-adding-leaderboard-support)

## Chapter I
### Instructions

How to learn at “School 21”:

- Here, you’ll find a unique learning experience with a lot of freedom. You’re given a task and left to find your own way to solve it, using whatever resources work best for you — whether that’s the Internet or AI tools like GigaChat. Just be mindful of information quality: verify, think critically, analyze, and compare.
- Peer-to-peer (P2P) learning is the exchange of knowledge and experience with peers, where everyone acts as both mentor and student. This approach allows you to gain a deeper understanding of the material by learning from one another.
- Feel free to ask for help: around you are peers who are also navigating this path for the first time. Share your own experience and ideas with others.  Join Rocket.Chat to stay updated with the latest community announcements. 
- Your learning is meaningless if you just copy someone else’s solutions. When receiving help from others, always make sure you fully understand the “why”, “how”, and “purpose” behind the solution. Don’t be afraid to make mistakes. 
- Does the task seem impossible? Take a break, get some fresh air and clear your mind — this has helped many people. Maybe after that, the solution will come to you naturally.
- The learning process is just as important as the result. It’s not just about completing the task — it’s about understanding HOW to solve it. 

How to work with the project:

- Before starting, clone the project from GitLab into a repository with the same name.
- All files should be created inside the _src/_ folder of the cloned repository.
- After cloning the project, create a _develop_ branch and do all your development there. Then, push the _develop_ branch to GitLab.
- Your directory should not contain any files other than those specified in the assignments.

## Chapter II
### General Informatiom
#### Token, Session Token, Refresh Token

A token is a unique sequence of characters that replaces the user’s login and password to prevent confidential information leaks. Tokens have a specific lifetime, after which they expire and stop working.

A **session token** grants the user rights to perform allowed actions during a session. It is reusable and has a short lifespan.

A **refresh token** extends the validity period of the session token. It is single-use and has a long lifespan.

#### Topics to Study

- Web application,
- JWT authorization,
- Flask,
- SQLAlchemy.

## Chapter III

## Project: Tic-Tac-Toe
Use the backend project from last week (T04).

### Task 1. Switching from Basic Authorization to JWT

- Create a JwtRequest model containing login and password.
- Create a JwtResponse model containing type, accessToken, and refreshToken.
- Create a RefreshJwtRequest model containing refreshToken.
- Implement a JwtProvider class with the following methods:
  - Use flask_jwt_extended from Flask to generate tokens.
  - A method to generate an accessToken from a User, saving the UUID in the token.
  - A method to generate a refreshToken from a User, saving the UUID in the token.
  - A method to validate accessToken.
  - A method to validate refreshToken.
  - A method to extract UUID from the token.
- Update the authorization service, which uses UserService and JwtProvider, to implement:
  - Modify the authorization method to accept a JwtRequest and return a JwtResponse.
  - Add a method to refresh the accessToken that accepts a refreshToken and returns a JwtResponse.
  - Add a method to refresh the refreshToken that accepts a refreshToken and returns a JwtResponse.
- Update the authorization controller by adding or modifying endpoints:
  - For user authorization;
  - For accessToken refresh;
  - For refreshToken refresh.
- Change the logic for determining an authorized user:
  - Retrieve the token from the Authorization header containing "Bearer {accessToken}".
  - Validate the token using JwtProvider.
  - Set authorization with the JWT extension’s sign method for the request.
- Remove basic authorization from Authentication.
- Add bearer authorization to Authentication.
- Use JwtProvider for token validation.
- If validation fails, respond with a 401 status code and do not process the request.
- Allow unauthenticated access to the accessToken refresh endpoint.
- Add an endpoint to retrieve user information by accessToken.

### Task 2. Adding Game History Support

- Add a creation date to the game model.
- Define a database query to retrieve all completed games by user UUID.
- A game is considered completed if it is in one of the following states:
  - Victory for a player with UUID;
  - Draw.
- Add a method to the game service for retrieving all completed games by user UUID.
- Add an endpoint to get all completed games by accessToken, accessible only to authorized users.

### Task 3. Adding Leaderboard Support

- Create a model for information about won games, including user UUID and win ratio.
- Define a database query that:
  - Calculates the ratio of won games to losses and draws for each user;
  - Sorts by win ratio in descending order;
  - Selects the top N records, each containing the user UUID and win ratio.
- Add a method to the game service to retrieve the top N players.
- Add an endpoint to get the top N players, which accepts N (number of top players) and returns a list of top players (UUID and login) with their win ratios.
- The endpoint to retrieve top players should be accessible only to authorized users.