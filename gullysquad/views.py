from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from matches.models import Match
from squads.models import Squad
from django.utils import timezone
from datetime import date

User = get_user_model()

def home(request):
    upcoming_matches = Match.objects.filter(status='upcoming', date__gte=date.today()).order_by('date', 'time')[:6]
    return render(request, "home.html", {"upcoming_matches": upcoming_matches})

def matches_list(request):
    matches = Match.objects.all().order_by('-date', '-time')
    return render(request, "matches/list.html", {"matches": matches})

def squads_list(request):
    squads = Squad.objects.all().order_by('-id')
    return render(request, "squads/list.html", {"squads": squads})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back, {}!".format(user.first_name or user.username))
            next_url = request.GET.get('next') or '/'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        profile_picture = request.FILES.get("profile_picture")

        if password != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.phone_number = phone_number
            user.role = role
            if profile_picture:
                user.profile_picture = profile_picture
            user.save()
            login(request, user)
            messages.success(request, "Account created successfully! Welcome, {}.".format(user.first_name or user.username))
            return redirect("/")
    return render(request, "register.html")

@login_required
def match_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        location = request.POST.get("location")
        date = request.POST.get("date")
        time = request.POST.get("time")
        max_players = request.POST.get("max_players")
        description = request.POST.get("description")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        if not (title and location and date and time and max_players):
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                match = Match.objects.create(
                    title=title,
                    location=location,
                    date=date,
                    time=time,
                    max_players=max_players,
                    description=description,
                    created_by=request.user,
                    status='upcoming',
                    current_players=1,
                    latitude=float(latitude) if latitude else None,
                    longitude=float(longitude) if longitude else None
                )
                messages.success(request, "Match created successfully!")
                return redirect("/matches/")
            except Exception as e:
                messages.error(request, f"Error creating match: {e}")
    return render(request, "matches/create.html")

@login_required
def squad_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        role = request.POST.get("role", "captain")
        is_private = request.POST.get("is_private") == "on"
        max_members = request.POST.get("max_members", 11)
        
        if not (name and description):
            messages.error(request, "Please fill in all required fields.")
        else:
            try:
                squad = Squad.objects.create(
                    name=name,
                    description=description,
                    created_by=request.user,
                    is_private=is_private,
                    max_members=max_members
                )
                # Add creator as member with selected role
                from squads.models import SquadMember
                SquadMember.objects.create(
                    squad=squad,
                    user=request.user,
                    role=role
                )
                messages.success(request, "Squad created successfully!")
                return redirect("/squads/")
            except Exception as e:
                messages.error(request, f"Error creating squad: {e}")
    return render(request, "squads/create.html")

def logout_view(request):
    auth_logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("/")

@login_required
def profile_view(request):
    return render(request, "profile.html") 