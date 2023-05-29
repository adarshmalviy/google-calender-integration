# Django Google Calendar Integration

## Overview
This project is a Django application that integrates with Google Calendar using the Django Rest Framework and the OAuth2 mechanism. The aim of the project is to retrieve a list of events from a user's Google Calendar.

## API Endpoints

The following API endpoints have been implemented:

### `/rest/v1/calendar/init/` - `GoogleCalendarInitView`
This endpoint initiates step 1 of the OAuth process and prompts the user for their Google credentials.

### `/rest/v1/calendar/redirect/` - `GoogleCalendarRedirectView`
This endpoint performs the following tasks:
- Handles the redirect request sent by Google with a code for the token
- Implements the mechanism to get the `access_token` from the given code
- Once the `access_token` is obtained, it retrieves a list of events from the user's calendar

## Requirements
- Django
- No third-party libraries, except for Google's standard libraries

## Google API Credentials
To run this project, you need to obtain Google API credentials. Follow these steps to obtain the credentials:

1. Go to the Google Developers Console.
2. Create a new project or select an existing one.
3. Enable the Google Calendar API for the project.
4. Create an OAuth 2.0 client ID.
5. Download the client ID as a JSON file and save it in the project directory.
6. Rename the file to credential.json and add it to the project's Git ignore file to avoid accidental exposure of the sensitive information.
7. Update the settings.py file with the path to the credential.json file.

With these credentials in place, you can now run the project and interact with the Google Calendar API.

Run the Django development server using the following command:

```bash
python manage.py runserver
```
