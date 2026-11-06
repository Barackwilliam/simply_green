from django.urls import path

from . import views

app_name = "site"

urlpatterns = [
    path("", views.home, name="home"),

    path("about/", views.about, name="about"),
    path("about/team/", views.team, name="team"),

    path("focus-areas/", views.focus_areas, name="focus_areas"),
    path("focus-areas/<slug:slug>/", views.focus_area_detail, name="focus_area_detail"),

    path("programmes/", views.programmes, name="programmes"),
    path("programmes/<slug:slug>/", views.programme_detail, name="programme_detail"),

    path("resources/", views.resources, name="resources"),
    path("resources/<slug:slug>/download/", views.publication_download, name="publication_download"),

    path("news/", views.news, name="news"),
    path("news/<slug:slug>/", views.post_detail, name="post_detail"),

    path("events/", views.events, name="events"),
    path("events/<slug:slug>/", views.event_detail, name="event_detail"),

    path("gallery/", views.gallery, name="gallery"),
    path("gallery/videos/", views.videos, name="videos"),
    path("gallery/<slug:slug>/", views.album_detail, name="album_detail"),

    path("get-involved/", views.get_involved, name="get_involved"),
    path("get-involved/volunteer/", views.volunteer, name="volunteer"),
    path("get-involved/partner/", views.partner, name="partner"),
    path("donate/", views.donate, name="donate"),

    path("contact/", views.contact, name="contact"),
    path("newsletter/", views.newsletter, name="newsletter"),
    path("privacy/", views.privacy, name="privacy"),
]
