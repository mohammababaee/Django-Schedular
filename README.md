# In name of Allah

## Introduction
We want a simple app to schedule & validate tasks for users. It should be possible to use django admin as interface for this application.

There are two kind of users:
- normal users
- admin users

**note** that each user must have below fields:
- email
- username
- password
- first name
- last name
- permissions (admin & normal)

You should extend AbstractUser for implementing user model.

normal users can only see, filter & add to their own tasks. These tasks will have a title, description, owner, time to send and precondition tasks field. the task should be scheduled to send an email to its owner at the specified time (use celery for this purpose) **Note** that every task has a set of precondition tasks (which are tasks as well) meaning for a task to be done, first, the set of tasks defined for it should have been done by the time it needs to be sent, otherwise the task will not be considered done. Also definition of done for a task is if it was sent at the specified time.

admin users have the permission to manage users, add to them and delete them. Also they can manage all tasks of users, add task for them and edit their tasks. When created or edited, scheduled tasks should be added or edited.

### Note
Write an API for validating a set of tasks (validation means if the set of tasks is possible to be done or not). If there is a precondition task which is not in the specified set of tasks, you do not need to consider it.

### Example

#### example 1
- Task
  - id: 1
  - title: task 1
  - description: desc 1
  - owner: nilva.man
  - time to send: 2020-05-10 10:30
  - pre-tasks: 
- Task
  - id: 2
  - title: task 2
  - description: desc 2
  - owner: nilva.man
  - time to send: 2020-05-06 10:30
  - pre-tasks: 
    - 1
    - 3
- Task
  - id: 3
  - title: task 3
  - description: desc 3
  - owner: nilva.man
  - time to send: 2020-02-10 9:30
  - pre-tasks: 

result: **No**, task 1 happens after task 2, but is a precondition of task 2, which makes it impossible to happen

#### example 2
- Task
  - id: 1
  - title: task 1
  - description: desc 1
  - owner: nilva.man
  - time to send: 2020-05-10 10:30
  - pre-tasks: 
- Task
  - id: 2
  - title: task 2
  - description: desc 2
  - owner: nilva.man
  - time to send: 2020-06-10 12:30
  - pre-tasks: 
    - 1
    - 3
- Task
  - id: 3
  - title: task 3
  - description: desc 3
  - owner: nilva.man
  - time to send: 2020-06-01 12:30
  - pre-tasks: 
    - 1

result: **Yes**, First task 1 will happen, then task 3, then task 2


## Expectations

So What does matter to us?
- a clean structure of codebase & components
- clean code practices
- well written unit tests
- finally, ability to learn

## Tasks

1. Fork this repository
2. Break and specify your tasks in project management tool (append the image of your tasks to readme file of your project)
3. Learn & Develop
4. Push your code to your repository
5. Explain the roadmap of your development in readme of repository (also append the image of your specified tasks on part 2 to file)
6. Send us a pull request, we will review and get back to you
7. Enjoy

**Finally** don't be afraid to ask anything from us.


# Project roadmap

## Introduction
To initiate the project, the first step was defining the models. We primarily focused on two main objects: **User** and **Task**. This entailed creating dedicated apps for each and seamlessly integrating them into the project settings.

## User Model
In developing the User model, I extended Django's built-in `AbstractUser` and introduced a `permission` field. Although we could have utilized Django's `is_staff`, I opted for an `is_admin` boolean field. Additionally, to accommodate potential future permissions, I chose a choice field. Furthermore, I enforced the requirement of an email field for user registration.

## Task Model
The Task model followed the guidelines outlined in the project's README. However, I introduced some enhancements:
- **notification_status:** Indicates whether the user has been notified.
- **notification_datetime:** Records the date and time of the notification, facilitating easier job handling.

These additional fields were incorporated to streamline operations and enhance functionality.

## Admin Interface Implementation
After defining the models, the subsequent step involved implementing the admin interface as per the README specifications.

## Email Notification Mechanism
The next significant task involved setting up a mechanism to send emails to users using Celery and Django signals. This allowed for asynchronous handling of email notifications, enhancing the responsiveness and efficiency of the system.

## Task Validation API
Subsequently, I developed an API to validate sets of tasks submitted by users, providing responses in the form of 'yes' or 'no'.

## Test Suite
At the project's conclusion, a comprehensive suite of tests was developed to ensure the reliability and robustness of the API, User model, and Task model.

### API Tests
A series of tests were designed to rigorously assess the functionality and behavior of the API. These tests covered various scenarios and edge cases to validate the correctness and responsiveness of the API endpoints.

### User Model Tests
Extensive testing was conducted on the User model to verify its integrity and functionality.

### Task Model Tests
Similar to the User model, thorough testing was performed on the Task model to validate its reliability and effectiveness. 

At the end, this project wasn't intended for production level. For production readiness, the following steps should be taken:
- Remove SECRET_KEY from settings file.
- Change the database from SQLite to another database.
- Avoid using WSGI.
- Set DEBUG to False

# API Response Photos
### First Example :
![Example 1](/images/Capture.PNG)
### Second Example: 
![Example 2](/images/my_info.PNG)
# Project Workflow
![Workflow](/images/project_flow.PNG)