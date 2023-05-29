import os
import json

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

CLIENT_SECRETS_FILE = "credential.json"
SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/userinfo.email',
          'https://www.googleapis.com/auth/userinfo.profile',
          'openid']
REDIRECT_URI = 'http://127.0.0.1:8000/rest/v1/calendar/redirect'
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


@api_view(['GET'])
def GoogleCalendarInitView(request):
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    request.session['state'] = state
    return Response({'authorization_url': authorization_url})


@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session.get('state')
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state
    )
    flow.redirect_uri = REDIRECT_URI

    authorization_response = request.get_full_path()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)

    if 'credentials' not in request.session:
        return redirect('v1/calendar/init')

    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials']
    )

    service = googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    calendar_list = service.calendarList().list().execute()
    calendar_id = calendar_list['items'][0]['id']
    events = service.events().list(calendarId=calendar_id).execute()

    events_list = []
    if not events['items']:
        return Response({"message": "No events found in the calendar"})
    else:
        for event in events['items']:
            event_data = {}
            event_data['summary'] = event['summary']
            event_data['start_time'] = event.get('start', {}).get('dateTime', '')
            event_data['end_time'] = event.get('end', {}).get('dateTime', '')
            events_list.append(event_data)
        return Response({"events": events_list})




