"""Public website views.

Everything is server-rendered.

These views are deliberately not wrapped in `cache_page`. The newsletter form
sits in the footer of every page, so every page carries a CSRF token — and a
cached page serves the first visitor's token to everyone, which Django then
rejects with a 403. Correctness wins: the queries here are small and indexed,
and on a free instance the cold start dominates anything caching would save.

If caching is wanted later, cache the fragments that have no token rather
than whole responses.
"""

from django.conf import settings as django_settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.about.models import CoreValue, Objective, PartnerReason, TeamMember
from apps.core.models import HeroSlide, ImpactStat, Partner
from apps.engage.models import DonationMethod, NewsletterSubscriber
from apps.gallery.models import Album, Video
from apps.news.models import Category, Event, Post
from apps.programmes.models import FocusArea, Programme
from apps.resources.models import Publication

from .forms import (
    ContactForm,
    DonationPledgeForm,
    EventRegistrationForm,
    NewsletterForm,
    PartnerForm,
    VolunteerForm,
)

def _notify(subject: str, body: str) -> None:
    """Email the office about a submission. Never blocks the visitor."""
    recipients = getattr(django_settings, "NOTIFICATION_RECIPIENTS", [])
    if not recipients:
        return
    try:
        send_mail(
            subject=f"[Simply Green] {subject}",
            message=body,
            from_email=django_settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True,
        )
    except Exception:
        pass


# ---------------------------------------------------------------- home

def home(request):
    focus_areas = list(FocusArea.objects.published())
    return render(request, "pages/home.html", {
        "slides": HeroSlide.objects.published(),
        "stats": ImpactStat.objects.published()[:4],
        "focus_areas": focus_areas,
        "pillars": focus_areas[:3],
        "programmes": Programme.objects.published().filter(status="ongoing")[:3],
        "reasons": PartnerReason.objects.published()[:3],
        "posts": Post.objects.published()[:3],
        "partners": Partner.objects.published().exclude(logo=""),
        "values": CoreValue.objects.published()[:6],
    })


# --------------------------------------------------------------- about

def about(request):
    return render(request, "pages/about.html", {
        "values": CoreValue.objects.published(),
        "objectives": Objective.objects.published(),
        "reasons": PartnerReason.objects.published(),
    })


def team(request):
    groups = []
    for key, label in TeamMember.Group.choices:
        people = TeamMember.objects.published().filter(group=key)
        if people:
            groups.append({"label": label, "people": people})
    return render(request, "pages/team.html", {"groups": groups})


# ------------------------------------------------------- focus & work

def focus_areas(request):
    return render(request, "pages/focus_areas.html", {
        "areas": FocusArea.objects.published(),
    })


def focus_area_detail(request, slug):
    area = get_object_or_404(FocusArea.objects.published(), slug=slug)
    return render(request, "pages/focus_area_detail.html", {
        "area": area,
        "programmes": area.programmes.filter(is_published=True),
    })


def programmes(request):
    qs = Programme.objects.published().prefetch_related("focus_areas")
    status = request.GET.get("status", "")
    area = request.GET.get("area", "")
    if status:
        qs = qs.filter(status=status)
    if area:
        qs = qs.filter(focus_areas__slug=area)
    return render(request, "pages/programmes.html", {
        "programmes": qs.distinct(),
        "statuses": Programme.Status.choices,
        "areas": FocusArea.objects.published(),
        "status": status,
        "area": area,
    })


def programme_detail(request, slug):
    programme = get_object_or_404(
        Programme.objects.published().prefetch_related(
            "focus_areas", "outcomes", "images", "partners"
        ),
        slug=slug,
    )
    return render(request, "pages/programme_detail.html", {"programme": programme})


# ----------------------------------------------------------- resources

def resources(request):
    qs = Publication.objects.published()
    kind = request.GET.get("kind", "")
    if kind:
        qs = qs.filter(kind=kind)
    return render(request, "pages/resources.html", {
        "publications": qs,
        "kinds": Publication.Kind.choices,
        "kind": kind,
    })


def publication_download(request, slug):
    """Count the download, then hand the visitor the file."""
    publication = get_object_or_404(Publication.objects.published(), slug=slug)
    Publication.objects.filter(pk=publication.pk).update(
        download_count=F("download_count") + 1
    )
    return redirect(publication.download_url or "site:resources")


# ---------------------------------------------------------------- news

def news(request):
    qs = Post.objects.published().select_related("category")
    kind = request.GET.get("kind", "")
    category = request.GET.get("category", "")
    if kind:
        qs = qs.filter(kind=kind)
    if category:
        qs = qs.filter(category__slug=category)
    return render(request, "pages/news.html", {
        "posts": qs,
        "kinds": Post.Kind.choices,
        "categories": Category.objects.published(),
        "kind": kind,
        "category": category,
    })


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.published().select_related("category", "author"), slug=slug
    )
    Post.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
    related = Post.objects.published().filter(kind=post.kind).exclude(pk=post.pk)[:3]
    return render(request, "pages/post_detail.html", {"post": post, "related": related})


# -------------------------------------------------------------- events

def events(request):
    now = timezone.now()
    base = Event.objects.published()
    return render(request, "pages/events.html", {
        "upcoming": base.filter(start_datetime__gte=now).order_by("start_datetime"),
        "past": base.filter(start_datetime__lt=now),
    })


def event_detail(request, slug):
    event = get_object_or_404(Event.objects.published(), slug=slug)
    form = EventRegistrationForm()

    if request.method == "POST":
        if not event.registration_open:
            messages.error(request, "Registration for this event is closed.")
            return redirect("site:event_detail", slug=slug)

        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.save()
            _notify("New event registration", str(registration))
            messages.success(
                request,
                "You are registered. We will be in touch with the final arrangements.",
            )
            return redirect("site:event_detail", slug=slug)

    return render(request, "pages/event_detail.html", {"event": event, "form": form})


# ------------------------------------------------------------- gallery

def gallery(request):
    return render(request, "pages/gallery.html", {"albums": Album.objects.published()})


def album_detail(request, slug):
    album = get_object_or_404(
        Album.objects.published().prefetch_related("photos"), slug=slug
    )
    return render(request, "pages/album_detail.html", {"album": album})


def videos(request):
    return render(request, "pages/videos.html", {"videos": Video.objects.published()})


# -------------------------------------------------------- get involved

def get_involved(request):
    return render(request, "pages/get_involved.html")


def volunteer(request):
    form = VolunteerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        application = form.save()
        _notify("New volunteer application", str(application))
        messages.success(
            request,
            "Thank you for offering your time. We will review your application "
            "and contact you about what is coming up.",
        )
        return redirect("site:volunteer")
    return render(request, "pages/volunteer.html", {
        "form": form,
        "areas": FocusArea.objects.published(),
    })


def partner(request):
    form = PartnerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        enquiry = form.save()
        _notify("New partner enquiry", str(enquiry))
        messages.success(
            request,
            "Thank you. Our team will review your proposal and come back to you.",
        )
        return redirect("site:partner")
    return render(request, "pages/partner.html", {
        "form": form,
        "reasons": PartnerReason.objects.published(),
    })


def donate(request):
    form = DonationPledgeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        pledge = form.save()
        _notify("New donation pledge", str(pledge))
        messages.success(
            request,
            "Thank you. We have recorded your pledge and will confirm it once "
            "your transfer arrives.",
        )
        return redirect("site:donate")

    methods = DonationMethod.objects.published()
    return render(request, "pages/donate.html", {
        "form": form,
        "banks": [m for m in methods if m.channel == "bank"],
        "mobile": [m for m in methods if m.channel != "bank"],
        "has_methods": bool(methods),
    })


# ------------------------------------------------------------- contact

def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)
        message.source_ip = request.META.get("REMOTE_ADDR")
        message.save()
        _notify("New contact message", str(message))
        messages.success(
            request, "Message sent. We read every message and will reply soon."
        )
        return redirect("site:contact")
    return render(request, "pages/contact.html", {"form": form})


@require_POST
def newsletter(request):
    form = NewsletterForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"].lower().strip()
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={
                "full_name": form.cleaned_data.get("full_name", ""),
                "source": "footer",
            },
        )
        if not created and not subscriber.is_active:
            subscriber.is_active = True
            subscriber.unsubscribed_at = None
            subscriber.save(update_fields=["is_active", "unsubscribed_at"])
        messages.success(request, "Thank you — you are on the list.")
    else:
        messages.error(request, "Please enter a valid email address.")
    return redirect(request.META.get("HTTP_REFERER", "site:home"))


def privacy(request):
    return render(request, "pages/privacy.html")


def handler404(request, exception):  # noqa: ARG001
    return render(request, "pages/404.html", status=404)
