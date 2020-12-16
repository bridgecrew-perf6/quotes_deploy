from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Users, Quotes
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            print(pw_hash)
            new_user = Users.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
                password_confirm=pw_hash
            )
            request.session['userid'] = new_user.id
            return redirect('/quotes')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = Users.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        if not Users.objects.authenticate(request.POST['email'], request.POST['password']):
            messages.error(request, 'Invalid Email or Password')
            return redirect('/')
        else:
            user = Users.objects.filter(email=request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                    request.session['userid'] = logged_user.id
                    print("User logged in")
                    return redirect('/quotes')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def quotes(request):
    if 'userid' not in request.session:
        return redirect('/')
    user = Users.objects.get(id=request.session['userid'])
    context = {
        'user': user,
        'all_quotes': Quotes.objects.exclude(users_who_like=request.session['userid']),
        'fave_quotes': Quotes.objects.filter(users_who_like=request.session['userid'])
    }
    return render(request, 'quotes.html', context)

def add_quote(request):
    if request.method == 'POST':
        errors = Quotes.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        else:
            Quotes.objects.create(
                quoted_by=request.POST['quoted_by'],
                message=request.POST['message'],
                uploaded_by=Users.objects.get(id=request.POST['uploaded_by']),
            )
        return redirect('/quotes')
    else:
        return redirect('/quotes')

def add_favorite(request, quote_id):
    user = Users.objects.get(id=request.session['userid'])
    fave_quote = Quotes.objects.get(id=quote_id)
    user.liked_quotes.add(fave_quote)
    return redirect('/quotes')

def remove_favorite(request, quote_id):
    user = Users.objects.get(id=request.session['userid'])
    bye_quote = Quotes.objects.get(id=quote_id)
    user.liked_quotes.remove(bye_quote)
    return redirect('/quotes')

def edit_quote(request, quote_id):
    context = {
        'quote_to_edit': Quotes.objects.get(id=quote_id),
    }
    return render(request, "edit_quote.html", context)

def update_quote(request, quote_id):
    quote_update = Quotes.objects.get(id=quote_id)
    if request.method == 'POST':
        errors = Quotes.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/quotes/{quote_id}/edit_quote')
        else:
            quote_update.quoted_by = request.POST['quoted_by']
            quote_update.message = request.POST['message']
            quote_update.save()
        return redirect('/quotes')
    else:
        return redirect(f'/quotes/{quote_id}/edit_quote')

def delete_quote(request, quote_id):
    kill_quote = Quotes.objects.get(id=quote_id)
    kill_quote.delete()
    return redirect('/quotes')

def user_profile(request, profile_id):
    context = {
        'profile': Users.objects.get(id=profile_id),
        'quantity': Quotes.objects.filter(uploaded_by__id=profile_id).count()
    }
    return render(request, "user_profile.html", context)