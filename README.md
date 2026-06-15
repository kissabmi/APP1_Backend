# Project Backend 04 — Python_Bootcamp

**Summary:**  
In this project, you will learn how to add databases to web applications in Python using Flask and work with authorization.

💡 [Click here](https://new.oprosso.net/p/4cb31ec3f47a4596bc758ea1861fb624) to share your feedback on this project. It’s anonymous and helps our team improve the learning experience. We recommend completing the survey immediately after finishing the project.

## Contents

  - [Chapter I](#chapter-i)
    - [Instructions](#instructions)
  - [Chapter II](#chapter-ii)
    - [General Information](#general-information)
      - [Authorization](#authorization)
      - [Identification, Authentication, Authorization](#identification-authentication-authorization)
      - [Authorization Using Login and Password](#authorization-using-login-and-password)
    - [Topics to Study](#topics-to-study)
  - [Chapter III](#chapter-iii)
    - [Task 1. Adding a Database](#task-1-adding-a-database)
    - [Task 2. Adding Authorization](#task-2-adding-authorization)
    - [Task 3. Adding Game Logic for Two Players](#task-3-adding-game-logic-for-two-players)

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

### General Information

#### Authorization

Authorization tools control access of legitimate users to system resources, granting each user only the rights assigned by the administrator.

#### Identification, Authentication, Authorization

- **Identification** is the process by which a subject’s unique identifier is established, unambiguously defining them within an information system.
- **Authentication** is the procedure of verifying authenticity — for example, validating a user by comparing the entered password with the stored password in the system.
- **Authorization** is the granting of rights to a specific individual or group to perform a defined set of actions.

#### Authorization Using Login and Password

This method is based on the user providing a login and password for successful identification and authentication within the system. The login-password pair is set by the user during registration. Upon successful authorization, the server grants the user rights to perform permitted requests.  
The client sends a request to the server and receives an "Unauthorized" message along with information on how to authorize. After successful authorization, each subsequent client request automatically includes an Authorization header ([authorization header formation](https://datatracker.ietf.org/doc/html/rfc7617)), which carries client credentials for server authentication.

![auth_eng](misc/images/Auth_ENG.png)

[Other methods of authorization](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication#authentication_schemes) also exist.

### Topics to Study

- Web application,
- Authorization using login and password pair (basic auth),
- PostgreSQL,
- Flask,
- SQLAlchemy.

## Chapter III

## Project: Tic-Tac-Toe
Use the backend project from last week’s T03.

### Task 1. Adding a Database

- Define the connection to a PostgreSQL database using SQLAlchemy.
- Remove the storage class.
- Add appropriate annotations to class parameters that need to be persisted in the database.

### Task 2. Adding Authorization

- Add users with UUID, login, and password.
- Implement user support across all layers.
- Create a SignUpRequest model containing login and password.
- Create an authorization service that uses UserService:
  - a registration method that accepts a SignUpRequest and returns a success status;
  - an authorization method that accepts login and password encoded in Base64 (login:password) in the header and returns the user’s UUID.
- Create an authorization controller with the following endpoints:
  - user registration;
  - user authorization (login).
- Create a UserAuthenticator structure that protects against requests from unauthorized users:
  - validate login and password;
  - if validation succeeds, process the request;
  - if validation fails, respond with status code 401 and do not process the request.
- Apply UserAuthenticator to your endpoints:
  - allow unauthenticated access to registration and authorization endpoints;
  - require authorization for all other endpoints.

### Task 3. Adding Game Logic for Two Players

- Add states for the current game:
  - Waiting for players;
  - Player’s turn with UUID;
  - Draw;
  - Victory for player with UUID.
- Add information about the marks (symbols) that users will use during the game.
- Improve the game-ending logic using the defined states.
- Add an endpoint for creating a new game with either a user or the computer.
- Add an endpoint to retrieve available current games.
- Add an endpoint for a user to join a game.
- Improve the endpoint for updating the current game, considering whether the opponent is a user or the computer.
- Add an endpoint to retrieve the current game.
- Add an endpoint to retrieve user information by UUID.