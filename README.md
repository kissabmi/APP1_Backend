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

1. Throughout the course, you will experience feelings of uncertainty and a sharp lack of information — this is normal. Remember, the repository and Google are always with you, as are your peers and Rocket.Chat. Communicate. Search. Use common sense. Don’t be afraid to make mistakes.
2. Be careful with your sources of information. Verify, think critically, analyze, and compare.
3. Read the tasks carefully. Read them several times.
4. It’s also best to read the examples carefully, as they may contain details not explicitly stated in the tasks.
5. You may encounter contradictions when something new in the task or example conflicts with what you already know. If that happens, try to figure it out. If you cannot, write down your question as an open issue and clarify it during your work. Don’t leave open questions unresolved.
6. If a task seems unclear or impossible, it only seems so. Try breaking it down; likely, individual parts will become clearer.
7. You will encounter various tasks along the way. Those marked with an asterisk (\*) are for the more meticulous. They are more challenging and optional, but completing them will give you additional experience and knowledge.
8. Don’t try to cheat the system or others. In the first place, you will cheat yourself.
9. Have a question? Ask your neighbor on the right. If that doesn’t help, ask the neighbor on the left.
10. When receiving help, always understand why, how, and for what purpose. Otherwise, the help won’t make sense.
11. Always push only to the develop branch! The master branch will be ignored. Work within the src directory.
12. Your directory should not contain any files other than those specified in the tasks.

## Chapter II
### General Informatiom
#### Token, Session Token, Refresh Token

A token is a unique sequence of characters that replaces the user’s login and password to prevent confidential information leaks. Tokens have a specific lifetime, after which they expire and stop working.

A **session token** grants the user rights to perform allowed actions during a session. It is reusable and has a short lifespan.

A **refresh token** extends the validity period of the session token. It is single-use and has a long lifespan.

#### Topics to Study

- Web application
- JWT authorization
- Flask
- SQLAlchemy

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