# Project Name

Brief description of what the project does.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

1. Clone the repository to your local machine:

    ```sh
    git clone https://your-repository-url.git
    ```

2. Navigate to the directory where you cloned the repository:

    ```sh
    cd path-to-your-project
    ```

3. Build and run the containers using Docker Compose:

    ```sh
    docker-compose up --build
    ```

    The `--build` flag is used to build the images before starting the containers.

4. Once the containers are running, you'll need to create the database tables. Run the migrations by executing the following command:

    ```sh
    docker-compose exec web python manage.py migrate
    ```

    The `docker-compose exec` command allows you to run commands inside the service's container. Here, `web` is assumed to be the service name defined in your `docker-compose.yml` that runs the Django project. Replace `web` with the actual service name if it's different.

5. Your project should now be running on [http://localhost:8050](http://localhost:8050) (or another port if you've configured it differently in your Docker settings).
## Creating a New Site

To add a new site to the system, follow these steps:

1. Go to the Create New Site page by clicking on the 'Create Site' button located on the 'Your Sites' page.

2. In the form provided, enter a unique name for the site in the 'Name' field. This should be an identifier that is easy for you to remember.

3. Enter the full URL of the site you wish to add in the 'URL' field, including the `http://` or `https://` prefix.

4. Click the 'Submit' button to create the site.

5. If you see any error messages, such as "A site with this name and URL already exists," correct the information accordingly and re-submit the form.

6. Once the site is successfully created, you will be redirected to a confirmation page or the list of your sites, where you can see the new entry.
