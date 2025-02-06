# Readme

Curious Camel (preliminary name) is an Intelligent Tutoring System for programming. In this file, you will find information on how to start using, contributing or hosting Curious Camel. This software is developed and maintained by the Knowledge Representation and Machine Learning (KML) group of Bielefeld University (https://www.uni-bielefeld.de/fakultaeten/technische-fakultaet/arbeitsgruppen/kml/).

## License

This software is distributed under the xxxx license. It shall not be redistributed commercially. The source code shall not be used in proprietary systems unless permission is granted by the KML group. 

## Feature List

- [x] Online code-editor
- [x] Display tasks and feedback with markdown
- [x] User management and data-collection settings
- [x] Save code execution using Jugde0
- [x] Program evaluation/submission based on unit-tests
- [x] Run programs with custom parameters
- [x] Users can send feedback requests to an ollama LLM-server
- [x] Print, function and multiple-choice tasks
- [x] Multiple courses per user
- [x] E-Mail based login
- [x] Monaco code editor
- [x] Upload courses
- [x] Conceptual Feedback on Steps
- [x] Course settings
- [x] Task selection based on user competency
- [ ] Tasks with image-files
- [ ] Fill the gap-tasks



## How to use?

At this point, the feature set of Curious Camel is limited. To maintain courses within the system, it is currently necessary to administrate the server directly. Therefore, this manual features two user groups: students and administrators. 

### Learners

#### Registration

At registration, learners have to enter an email-adress for account verification. The email-adress is only stored until the user has succesfully verified (afterwords it will be hashed and encrypted for cases of a password reset).  On registration, learners must select, whether they want their intermediate steps to be stored in the database and whether they allow the usage of their system data for research purposes. 

![register](doc/pictures/register.png "Register"){width=300}


#### Login

Users can log in to the selected course with their username and password. 

![login](doc/pictures/login.png "Login"){width=300}

#### Reset Password

To reset their password users have to enter their mail, their username and the password reset token they received via email on registration.

![forget password](doc/pictures/forgot_password.png "Forgot password"){width=300}

#### Tutoring View

The tutoring view is the main view within a particular course. It allows for solving and navigating tasks. The task description is displayed in the upper left corner, different feedback and result types are displayed in the lower left corner. On the right side, the code editor allows for entering solutions to tasks. The action panel on the bottom allows for three actions: "Run", "Feedback" and "Submission". 

![tutoring view](doc/pictures/tutoring_view.png "Tutoring View"){width=500}


The "Run" button allows for the execution of the learner program with custom parameters. The "Submit" functionality will run unit tests on the current solution and display the results to the learner in the feedback panel. The "Feedback" button will send a Feedback request to the backend. Depending on the course settings, feedback on the current learner program will then be generated.

#### Profile View

The user profile can be reached over the navigation bar. It displays basic information about the user profile. Also, the user profile allows for reviewing and re-setting the data-collection preferences that were originally set during registration.


![profile](doc/pictures/profile.png "Profile View"){width=300}

### Admins

#### Installation

Specify .env file with different secrets for the backend.

#### Loading a course to the system

#### Setting up the LLM Server

## Contributing

We welcome external contributors to this project. If you want to contribute, we are happy to assist with questions regarding the integration of your contribution with our system. In any case, contributions should align with the general system architecture of the system.


## Contributors

### Active Contributors

Alina Deriyeva (primary)
Arno Gaußelmann
Benjamin Paaßen
Jesper Dannath (primary)

### Additional Contributors

Aliena Strathmann
Björn Buschkämper
Tobias Hillmer
