from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse

from accounts.avatars import avatars
import random
from faker import Faker


from decouple import config

from .models import User
from .models import UserPrivacy
from .models import Calendar
from books.models import Book
from books.models import IsbnAdd3
from reviews.models import Review, ReviewComment, Phrase, ReviewLike
from libraries.models import LibraryLocation
from .forms import LoginForm, CustomUserChangeForm, CustomUserCreationForm
from .serializers import UserSerializer
from .serializers import UserPrivacySerializer
from .serializers import CalendarSerializer
from books.serializers import BookSerializer
from reviews.serializers import ReviewSerializer, ReviewCommentSerializer, PhraseSerializer
from .utils import permission

import requests
import json
import jwt

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from analyze.tendency import UserTendency
from characters.models import Genre
from characters.serializers import GenreSerializer


@csrf_exempt
def check_signup(request):
    data = json.loads(request.body.decode('utf-8'))
    data2 = {}
    if request.method == 'POST':
        form = CustomUserCreationForm(data=data)
        if form.is_valid():
            data2['result'] = 'success'

        else:
            data2['error'] = form.errors

    else:
        form = CustomUserCreationForm()
        data2['error'] = form.errors

    return JsonResponse(data2)


@csrf_exempt
def signup(request):
    city = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시',
            '세종특별자치시': '세종특별자치시', '경기': '경기도', '강원': '강원도',
            '충북': '충청북도', '충남': '충청남도', '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도',
            '제주특별자치도': '제주특별자치도'}

    print('회원가입 진입')
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    if "choice" in data:
        temp_val = data.pop("choice")
    else:
        temp_val = []

    if "genres" in data:
        temp_gen = data.pop("genres")
    else:
        temp_gen = []

    if request.method == 'POST':
        form = CustomUserCreationForm(data=data)
        print(form)
        if form.is_valid():
            user = form.save()
            UserPrivacy(user=user).save()
            print(user)

            # 유저 성향체크를 위한 빈 테이블 생성
            ut = UserTendency(user)
            ut.create_user_tendency_table()
            
            for book in temp_val:
                user.like_books.add(book["id"])

            for idx, gen in enumerate(temp_gen):
                if gen:
                    user.user_genres.add(Genre.objects.get(pk=idx+1))

            data = {}
            data['result'] = 'success'
            data['no_address'] = []
            data['no_loc_code'] = []

            address = user.address
            if address:
                address_list = list(address.split())

                try:
                    gu = " ".join(address_list[1:3])
                    loc = get_object_or_404(
                        LibraryLocation, city=city[address_list[0]], gu=gu)
                    print(user.pk, loc.loc_code)
                    loc.location_users.add(user)

                except:
                    try:
                        gu = address_list[1]
                        loc = get_object_or_404(
                            LibraryLocation, city=city[address_list[0]], gu=gu)
                        print(user.pk, loc.loc_code)
                        loc.location_users.add(user)
                    except:
                        print(user.pk, "오류입니다2, location code 존재 X")
                        data['no_loc_code'].append(user.pk)
            else:
                print(user.pk, "주소가 존재하지 않습니다")
                data['no_address'].append(user.pk)

            return JsonResponse(data)
    else:
        form = CustomUserCreationForm()
    data = {}
    data['error'] = form.errors.as_json()
    return JsonResponse(data)


@csrf_exempt
def check_email(request):
    email = request.GET.get('email')
    data = {}
    if User.objects.filter(email=email).exists():
        data["result"] = False
        return JsonResponse(data)
    else:
        data["result"] = True
        return JsonResponse(data)


@csrf_exempt
def login(request):
    # print("login 진입")
    # print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    # print(data)

    if request.method == 'GET':
        return HttpResponse("GET또다제")

    if request.method == 'POST':
        form = LoginForm(data=data)

        if form.is_valid():
            email = data["email"]
            password = data["password"]
            user = authenticate(email=email, password=password)
            # print(user)
            if user is not None:
                if user.is_active:
                    token = jwt.encode({"email": email}, config(
                        'SECRET_KEY'), algorithm="HS256")
                    token = token.decode("utf-8")
                    # print(token)
                    data = {}
                    data["token"] = token
                    data["user_pk"] = user.pk
                    return JsonResponse(data)
            else:
                data = {}
                data['error'] = "존재하지 않는 회원입니다."
        else:
            data = {}
            data['error'] = "아이디, 비밀번호를 확인해주세요."
    return JsonResponse(data)


def logout(request):
    pass

# KAKAO


def oauth(request):
    code = request.GET.get('code', None)
    # print('이것이 code = ' + str(code))
    client_id = config('KAKAO_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI')

    access_token_request_uri = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&"
    access_token_request_uri += "client_id=" + client_id
    access_token_request_uri += "&redirect_uri=" + redirect_uri
    access_token_request_uri += "&code=" + code

    access_token_request_uri_data = requests.get(access_token_request_uri)
    json_data = access_token_request_uri_data.json()
    access_token = json_data['access_token']
    # print('이것은 access_token = ' + str(access_token))

    url = 'https://kapi.kakao.com/v2/user/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-type': 'application/x-www-form-urlencoded; charset-utf-8',
    }
    kakao_response = requests.get(url, headers=headers).json()
    # print('이것이 결과 = ' + str(kakao_response))

    try:
        email = kakao_response['kakao_account']['email']
    except:
        email = 'kakao_account' + str(kakao_response['id']) + "@bookridge.com"

    try:
        if kakao_response['kakao_account']['profile']['profile_image_url']:
            profile_image_url = kakao_response['kakao_account']['profile']['profile_image_url']
        if kakao_response['kakao_account']['profile']['thumbnail_image_url']:
            thumbnail_image_url = kakao_response['kakao_account']['profile']['thumbnail_image_url']
    except:
        profile_image_url = ""
        thumbnail_image_url = ""

    gender = 2
    name = kakao_response['properties']['nickname']
    social = 1
    social_id = str(kakao_response['id'])

    User = get_user_model()

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        # print(user)
        token = jwt.encode({"email": user.email}, config(
            'SECRET_KEY'), algorithm="HS256")
        token = token.decode("utf-8")
        data = {}
        data["token"] = token
        data["social_id"] = user.social_id
        data["user_pk"] = user.pk
        data["user_gender"] = user.gender
        data["email"] = user.email
        data["name"] = user.name
        data["social"] = user.social
        # print(data)
        return JsonResponse(data)

    User(
        email=email,
        gender=gender,
        name=name,
        social=social,
        social_id=social_id,
    ).save()

    user = User.objects.get(email=email)
    UserPrivacy(user=user).save()

    # 유저 성향체크를 위한 빈 테이블 생성
    ut = UserTendency(user)
    ut.create_user_tendency_table()
    
    token = jwt.encode({"email": user.email}, config(
        'SECRET_KEY'), algorithm="HS256")
    token = token.decode("utf-8")
    data = {}
    data["token"] = token
    data["social_id"] = social_id
    data["user_pk"] = user.pk
    data["user_gender"] = user.gender
    data["email"] = user.email
    data["name"] = user.name
    data["social"] = user.social
    return JsonResponse(data)


def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = config('KAKAO_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI')
    # print(redirect_uri)
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'

    return redirect(login_request_uri)


class UnlinkView(View):
    @permission
    def delete(self, request):
        user = request.user
        if user.social == 1:  # 카카오 연결 끊기(탈퇴)
            unlink_request_url = 'https://kapi.kakao.com/v1/user/unlink'
            # print(ADMIN_KEY)
            headers = {
                'Authorization': 'KakaoAK ' + config('ADMIN_KEY'),
            }
            params = {
                'Authorization': 'KakaoAK ' + config('ADMIN_KEY'),
                'target_id': user.social_id,
                'target_id_type': "user_id",
            }
            result = requests.post(
                unlink_request_url, headers=headers, params=params).json()
            # print(result)
            user.delete()
            data = {
                'result': "카카오 연결 끊기",
            }
        else:  # 일반, 구글 (탈퇴)
            user.delete()
            data = {
                'result': "회원 탈퇴"
            }
        return JsonResponse(data)

    @permission
    def post(self, request):  # 카카오 로그아웃
        user = request.user
        logout_request_url = 'https://kapi.kakao.com/v1/user/logout'
        headers = {
            'Authorization': config('ADMIN_KEY'),
        }
        params = {
            'Authorization': config('ADMIN_KEY'),
            'target_id': user.social_id,
            'target_id_type': "user_id"
        }
        result = requests.post(
            logout_request_url, headers=headers, params=params).json()
        # print(result)
        data = {
            'result': '카카오 로그아웃'
        }

        return JsonResponse(data)


def google_login(request):
    # print('google_login 진입')
    login_request_uri = "https://accounts.google.com/o/oauth2/v2/auth?"
    client_id = config('GOOGLE_LOGIN_client_ID')
    # print(client_id)
    redirect_uri = config('REDIRECT_URI_GOOGLE')
    # print(redirect_uri)
    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    login_request_uri += '&scope=profile%20email%20openid'
    # print(login_request_uri)

    return redirect(login_request_uri)


def oauth2(request):
    # print('oauth2 진입')
    code = request.GET.get('code', None)
    # print('이것이 code = ' + str(code))
    client_id = config('GOOGLE_LOGIN_client_ID')
    redirect_uri = config('REDIRECT_URI_GOOGLE')
    client_secret = config('GOOGLE_SECRET')

    access_token_request_uri = "https://accounts.google.com/o/oauth2/token"
    params = {
        'code': code,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    access_token_request_uri_data = requests.post(
        access_token_request_uri, params=params)
    # print(access_token_request_uri_data)
    json_data = access_token_request_uri_data.json()
    # print(json_data['id_token'])
    # print(json_data['scope'])
    access_token = json_data['access_token']
    url = 'https://www.googleapis.com/oauth2/v3/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}',
    }
    google_response = requests.get(url, headers=headers).json()
    # print(google_response)

    email = google_response['email']
    profile_image_url = google_response['picture']
    thumbnail_image_url = ""
    gender = 2  # 미상
    name = google_response['name']
    social = 2  # 구글
    social_id = str(google_response['sub'])
    User = get_user_model()

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        # print(user)
        token = jwt.encode({"email": user.email}, config(
            'SECRET_KEY'), algorithm="HS256")
        token = token.decode("utf-8")
        data = {}
        data["token"] = token
        data["social_id"] = user.social_id
        data["user_pk"] = user.pk
        data["user_gender"] = user.gender
        data["email"] = user.email
        data["name"] = user.name
        data["social"] = user.social
        return JsonResponse(data)

    User(
        email=email,
        gender=gender,
        name=name,
        social=social,
        social_id=social_id,
    ).save()

    user = User.objects.get(email=email)
    UserPrivacy(user=user).save()

    token = jwt.encode({"email": user.email}, config(
        'SECRET_KEY'), algorithm="HS256")
    token = token.decode("utf-8")
    data = {}
    data["token"] = token
    data["social_id"] = user.social_id
    data["user_pk"] = user.pk
    data["user_gender"] = user.gender
    data["email"] = user.email
    data["name"] = user.name
    data["social"] = user.social
    # print(data)
    return JsonResponse(data)


def get_all_profile(request):
    users = User.objects.all()
    users_serial = UserSerializer(users, many=True)
    return JsonResponse(users_serial.data)

class ProfileView(View):
    @permission
    def get(self, request, user_pk):
        # print('profile 진입')
        user = get_object_or_404(User, pk=user_pk)
        user_serial = UserSerializer(user)
        # print(user_serial.data)
        user_privacy = get_object_or_404(UserPrivacy, user=user)
        user_privacy_serial = UserPrivacySerializer(user_privacy)
        # print(user_privacy_serial.data)
        data = {}
        data['profile_url'] = f"https://joeschmoe.io/api/v1/{avatars[user_privacy.name]}"
        print(data["profile_url"])
        for key, val in user_serial.data.items():
            data[key] = val

        users_genres = GenreSerializer(user.user_genres.all(), many=True)
        data['privacy'] = user_privacy_serial.data["name"]

        genre_list = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for g in users_genres.data:
            genre_list[g["id"]-1] = 1
            
        data['genres'] = genre_list
        
        return JsonResponse(data)

    @permission
    def post(self, request, user_pk):
        # print('프로필 수정 진입')
        city = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시',
                '세종특별자치시': '세종특별자치시', '경기': '경기도', '강원': '강원도',
                '충북': '충청북도', '충남': '충청남도', '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도',
                '제주특별자치도': '제주특별자치도'}

        data = json.loads(request.body.decode('utf-8'))
        # print(data)
        if "choice" in data:
            temp_val = data.pop("choice")
        else:
            temp_val = []

        if "genres" in data:
            temp_gen = data.pop("genres")
        else:
            temp_gen = []
        
        if "profile" in data:
            profile = data.pop("profile")
        
        form = CustomUserChangeForm(data=data, instance=request.user)
        if form.is_valid():
            user = form.save()
            for book in temp_val:
                user.like_books.add(book)

            for idx, gen in enumerate(temp_gen):
                try:
                    if gen:
                        user.user_genres.add(Genre.objects.get(pk=idx+1))
                    else:
                        user.user_genres.remove(Genre.objects.get(pk=idx+1))
                except:
                    pass
                
            # print(user)
            data = {}

            user_serial = UserSerializer(user)
            for key, val in user_serial.data.items():
                data[key] = val

            data['result'] = 'success'
            data['no_address'] = []
            data['no_loc_code'] = []

            address = user.address
            if address:
                address_list = list(address.split())
                try:
                    locs = user.location_libraries.all()
                    if locs:
                        print("loc 관계 이미 존재합니다")
                        for loc in locs:
                            loc.location_users.remove(user)

                    gu = " ".join(address_list[1:3])
                    loc = get_object_or_404(
                        LibraryLocation, city=city[address_list[0]], gu=gu)
                    print(user.pk, loc.loc_code)

                    loc.location_users.add(user)

                except:
                    try:
                        gu = address_list[1]
                        loc = get_object_or_404(
                            LibraryLocation, city=city[address_list[0]], gu=gu)
                        print(user.pk, loc.loc_code)
                        loc.location_users.add(user)
                    except:
                        print(user.pk, "오류입니다2, location code 존재 X")
                        data['no_loc_code'].append(user.pk)
            else:
                print(user.pk, "주소가 존재하지 않습니다")
                data['no_address'].append(user.pk)

            user_privacy = get_object_or_404(UserPrivacy, user=user)
            
            try:
                user_privacy.name = profile
                user_privacy.save()
            except:
                pass
            
            data['profile_url'] = f"https://joeschmoe.io/api/v1/{avatars[user_privacy.name]}"
            return JsonResponse(data)
        else:
            form = CustomUserCreationForm(instance=request.user)
        data = {}
        data['error'] = "입력값을 확인해주세요."
        return JsonResponse(data)


class PasswordView(View):
    @permission
    def get(self, request, user_pk):
        # print(request.user)
        data = request.GET.get('password')
        # print(data)
        current_password = data
        user = request.user
        data = {}
        if check_password(current_password, user.password):
            data['result'] = True
            return JsonResponse(data)
        else:
            data['result'] = False
            data['error'] = "비밀번호가 일치하지 않습니다."
            return JsonResponse(data)

    @permission
    def post(self, request, user_pk):
        data = json.loads(request.body.decode('utf-8'))
        # print(data['password1'])
        current_password = data['password']
        user = request.user
        if check_password(current_password, user.password):
            password1 = data["password1"]
            password2 = data["password2"]
            if password1 == password2:
                user.set_password(password1)
                user.save()
                user_serial = UserSerializer(user)
                data = {}
                for key, val in user_serial.data.items():
                    data[key] = val
                return JsonResponse(data)
            else:
                data = {}
                data['error'] = "두 비밀번호가 일치하지 않습니다."
                return JsonResponse(data)
        else:
            data = {}
            data['error'] = "비밀번호가 일치하지 않습니다."
            return JsonResponse(data)


class PrivacyView(View):
    @permission
    def post(self, request, user_pk):
        data = json.loads(request.body.decode('utf-8'))
        user_privacy = get_object_or_404(UserPrivacy, user=request.user)
        user_privacy_serial = UserPrivacySerializer(user_privacy, data=data)
        if user_privacy_serial.is_valid(raise_exception=True):
            user_privacy_serial.save()
            data2 = {}
            data2['result'] = user_privacy_serial.data
            return JsonResponse(data2)
        data['result'] = "수정 실패"

        return JsonResponse(data)


class CalendarView(View):
    # calendar create
    @permission
    def put(self, request):
        print('calendar create start')
        data = json.loads(request.body.decode('utf-8'))
        data2 = {}

        try:
            start_date = data['start_date']
        except:
            start_date = ""
            data2[result] = "start date 가 없습니다"
            return JsonResponse(data2)

        try:
            end_date = data['end_date']
        except:
            end_date = ""
            data['end_date'] = ""

        book_pk = data['book_pk']
        book = get_object_or_404(Book, pk=book_pk)
        user = request.user
        # user_serial = UserSerializer(user)

        if end_date != "":
            user.finish_books.add(book)
        else:
            del data['end_date']

        try:
            calendars = Calendar.objects.filter(Q(user=user) & Q(book=book))
            for calendar in calendars:
                if calendar.start_date == data['start_date']:
                    data2['result'] = "이미 등록된 도서입니다."
                    return JsonResponse(data2)
        except:
            print("except 진입")

        data['book'] = book_pk
        data['user'] = user.pk

        serializer = CalendarSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2['result'] = serializer.data
            return JsonResponse(data2)
        data2['result'] = "등록에 실패하였습니다."

        return JsonResponse(data2)

    # 해당 user 의 calendar
    @permission
    def get(self, request):
        data2 = {}
        user_pk = request.GET.get("user_pk")
        user = get_object_or_404(User, pk=user_pk)

        try:
            date = request.GET.get("date")
        except:
            date = ""

        if date:

            try:
                # end_date 기준
                calendars_red = Calendar.objects.filter(
                    Q(user=user) & Q(end_date=date))
            except:
                calendars_red = []

            try:
                # start_date 기준
                calendars_yellow = Calendar.objects.filter(
                    Q(user=user) & Q(start_date=date))
            except:
                calendars_yellow = []

            data2['red'] = []
            data2['yellow'] = []

            for i in range(len(calendars_red)):
                try:
                    calendar = get_object_or_404(
                        Calendar, pk=calendars_red[i].pk)
                    book = get_object_or_404(Book, pk=calendar.book.pk)
                    calendar_serial = CalendarSerializer(calendar)
                    book_serial = BookSerializer(book)
                    data2['red'].append(
                        {'calendar': calendar_serial.data, 'book': book_serial.data})
                except:
                    data2['red'].append({'error': "등록된 책 정보가 없습니다."})

            for i in range(len(calendars_yellow)):
                calendar = get_object_or_404(
                    Calendar, pk=calendars_yellow[i].pk)
                if calendar.end_date:
                    continue
                else:
                    try:
                        book = get_object_or_404(Book, pk=calendar.book.pk)
                        calendar_serial = CalendarSerializer(calendar)
                        book_serial = BookSerializer(book)
                        data2['yellow'].append(
                            {'calendar': calendar_serial.data, 'book': book_serial.data})
                    except:
                        data2['yellow'].append({'error': "등록된 책 정보가 없습니다."})

        else:
            calendars = Calendar.objects.filter(user=user)
            data2['result'] = []
            for i in range(len(calendars)):
                try:
                    calendar = get_object_or_404(Calendar, pk=calendars[i].pk)
                    book = get_object_or_404(Book, pk=calendar.book.pk)
                    calendar_serial = CalendarSerializer(calendar)
                    book_serial = BookSerializer(book)
                    data2['result'].append(
                        {'calendar': calendar_serial.data, 'book': book_serial.data})
                except:
                    data2['result'].append({'error': "등록된 책 정보가 없습니다."})

        return JsonResponse(data2)

    # calendar update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        book = get_object_or_404(Book, pk=book_pk)
        calendar_pk = data['calendar_pk']
        calendar = get_object_or_404(Calendar, pk=calendar_pk)
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = CalendarSerializer(calendar, data=data)
        if data["end_date"] != "":
            user.finish_books.add(book)
        data2 = {}
        try:
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                data2['result'] = serializer.data
        except:
            data2['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        data2 = {}
        try:
            calendar_pk = request.GET.get("calendar_pk")
            calendar = get_object_or_404(Calendar, pk=calendar_pk)
            calendar.delete()
            data2["result"] = "success"
        except:
            data2["result"] = "fail"
        return JsonResponse(data2)


@csrf_exempt
def choice(request):
    try:
        user_pk = request.GET.get("user_pk")
        book_pks = request.GET.get("book_pks")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)
    user = get_object_or_404(User, pk=user_pk)
    for book_pk in book_pks:
        book = get_object_or_404(Book, pk=book_pk)
        user.choice_books.add(book)
    choice_books = user.choice_books.all()
    choice_books_serial = BookSerializer(choice_books)
    data = {"result": choice_books_serial.data}
    return JsonResponse(data)


@csrf_exempt
def like(request):
    try:
        user_pk = request.GET.get("user_pk")
        book_pk = request.GET.get("book_pk")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)

    user = get_object_or_404(User, pk=user_pk)
    book = get_object_or_404(Book, pk=book_pk)

    ut = UserTendency(user)

    if user.like_books.filter(pk=book_pk).exists():
        user.like_books.remove(book)
        message = '좋아요 취소'
        like = False
        ut.sub_user_tendency_table(book_pk)  # 좋아요 취소시 사용자 경향 변경
    else:
        user.like_books.add(book)
        message = '좋아요 등록'
        like = True
        ut.add_user_tendency_table(book_pk)  # 좋아요 시 사용자 경향 변경

        if user.unlike_books.filter(pk=book_pk).exists():
            user.unlike_books.remove(book)
            message = '좋아요 등록, 싫어요 취소'
            unlike = False
            ut.add_user_tendency_table(book_pk)
            ut.add_user_tendency_table(book_pk)
    data = {}
    data["message"] = message
    data["book_pk"] = book_pk
    data["like"] = like
    try:
        data["unlike"] = unlike
    except:
        data["unlike"] = None

    return JsonResponse(data)


@csrf_exempt
def unlike(request):
    try:
        user_pk = request.GET.get("user_pk")
        book_pk = request.GET.get("book_pk")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)
    user = get_object_or_404(User, pk=user_pk)
    book = get_object_or_404(Book, pk=book_pk)

    ut = UserTendency(user)

    if user.unlike_books.filter(pk=book_pk).exists():
        user.unlike_books.remove(book)
        message = '싫어요 취소'
        unlike = False
        ut.add_user_tendency_table(book_pk)  # 싫어요 취소시 사용자 경향 변경
    else:
        user.unlike_books.add(book)
        message = '싫어요 등록'
        unlike = True
        ut.sub_user_tendency_table(book_pk)  # 싫어요 시 사용자 경향 변경
        if user.like_books.filter(pk=book_pk).exists():
            user.like_books.remove(book)
            message = '싫어요 등록, 좋아요 취소'
            like = False
            ut.sub_user_tendency_table(book_pk)  # 싫어요 시 사용자 경향 변경
            ut.sub_user_tendency_table(book_pk)  # 싫어요 시 사용자 경향 변경
    data = {}
    data["message"] = message
    data["book_pk"] = book_pk
    data["unlike"] = unlike
    try:
        data["like"] = like
    except:
        data["like"] = None

    return JsonResponse(data)


@csrf_exempt
def finish(request):
    try:
        user_pk = request.GET.get("user_pk")
        book_pk = request.GET.get("book_pk")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)
    user = get_object_or_404(User, pk=user_pk)
    book = get_object_or_404(Book, pk=book_pk)
    if user.finish_books.filter(pk=book_pk).exists():
        user.finish_books.remove(book)
        message = '완독 취소'
        finish = False
    else:
        user.finish_books.add(book)
        message = '완독'
        finish = True

    data = {}
    data["message"] = message
    data["book_pk"] = book_pk
    data["finish"] = finish

    return JsonResponse(data)


@csrf_exempt
def get_finish_list(request):
    try:
        user_pk = request.GET.get("user_pk")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)

    user = get_object_or_404(User, pk=user_pk)
    data = {}
    fin_books = user.finish_books.all()
    fin_books_serial = BookSerializer(fin_books, many=True)
    data["result"] = fin_books_serial.data

    return JsonResponse(data)


@csrf_exempt
def get_like_list(request):
    try:
        user_pk = request.GET.get("user_pk")
    except:
        data = {"error": "user_pk가 없어요."}
        return JsonResponse(data)
    user = get_object_or_404(User, pk=user_pk)
    like = user.like_books.all()
    unlike = user.unlike_books.all()
    like_serial = BookSerializer(like, many=True)
    unlike_serial = BookSerializer(unlike, many=True)
    like_list = []
    unlike_list = []
    for pick1 in like_serial.data:
        like_list.append(pick1["id"])
    for pick2 in unlike_serial.data:
        unlike_list.append(pick2["id"])
    data = {
        "like_list": like_list,
        "unlike_list": unlike_list,
    }
    return JsonResponse(data)


class LikeView(View):
    @permission
    def get(self, request):
        user = request.user
        like_books = user.like_books.all()
        like_books_serial = BookSerializer(like_books, many=True)
        data = {}
        if len(like_books_serial.data) != 0:
            data["result"] = like_books_serial.data
        else:
            data["result"] = "좋아요한 책이 없습니다."

        return JsonResponse(data)


class HateView(View):
    @permission
    def get(self, request):
        user = request.user
        unlike_books = user.unlike_books.all()
        unlike_books_serial = BookSerializer(unlike_books, many=True)
        data = {}
        if len(unlike_books_serial.data) != 0:
            data["result"] = unlike_books_serial.data
        else:
            data["result"] = "싫어요한 책이 없습니다."

        return JsonResponse(data)


class LikeReviewView(View):
    @permission
    def get(self, request):
        user_pk = request.GET.get("user_pk")
        data = {}
        try:
            user = get_object_or_404(User, pk=user_pk)
            review_likes = ReviewLike.objects.filter(user=user)
            data["result"] = []

            if len(review_likes):
                for review_like in review_likes:
                    review = get_object_or_404(
                        Review, pk=review_like.review.pk)
                    review_serial = ReviewSerializer(review)

                    review_info = review_serial.data
                    book = get_object_or_404(Book, pk=review_info["book"])
                    book_serial = BookSerializer(book)

                    review_info["book_title"] = book_serial.data["title"]
                    review_info["book_img_url"] = book_serial.data["img_url"]

                    data["result"].append(review_info)
            else:
                data["result"] = "좋아요한 review 가 없습니다."
        except:
            data["error"] = "오류가 발생하였습니다."

        return JsonResponse(data)


class PhraseView(View):
    @permission
    def get(self, request):
        user_pk = request.GET.get("user_pk")
        # phrases = get_object_or_404(Phrase, user=user)
        # phrases_serial = PhraseSerializer(phrases, many=True)
        data = {}
        try:
            user = get_object_or_404(User, pk=user_pk)
            phrases = Phrase.objects.filter(user=user)

            if len(phrases):
                phrases_serial = PhraseSerializer(phrases, many=True)
                phrases_list = phrases_serial.data

                for phrase_serial in phrases_list:
                    book = get_object_or_404(Book, pk=phrase_serial["book"])
                    book_serial = BookSerializer(book)
                    phrase_serial["book_title"] = book_serial.data["title"]
                    phrase_serial["book_img_url"] = book_serial.data["img_url"]

                data["result"] = phrases_list
            else:
                data["result"] = "작성한 phrase 가 없습니다."
        except:
            data["error"] = "오류가 발생하였습니다."

        return JsonResponse(data)

    @permission
    def post(self, request):
        # phrase_pk, page, content
        data = json.loads(request.body.decode('utf-8'))
        user = request.user
        phrase_pk = data['phrase_pk']
        phrase = get_object_or_404(Phrase, pk=phrase_pk)

        data['book'] = phrase.book.pk
        data['user'] = user.pk
        phrase_serializer = PhraseSerializer(phrase, data=data)
        if phrase_serializer.is_valid(raise_exception=True):
            phrase_serializer.save()
            phrases = get_object_or_404(Phrase, user=user)
            phrases_serial = PhraseSerializer(phrases, many=True)
            data = {}
            data['result'] = phrases_serial.data
            data['result']["name"] = user.name
            return JsonResponse(data)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        phrase_pk = request.GET.get("phrase_pk")
        user = request.user
        try:
            phrase = get_object_or_404(Phrase, pk=phrase_pk)
            phrase.delete()
            phrases = get_object_or_404(Phrase, user=user)
            phrases_serial = PhraseSerializer(phrases, many=True)
            data = {}
            data["result"] = phrases_serial.data
        except:
            data['result'] = "phrase 정보가 없습니다."

        return JsonResponse(data)


class ReviewView(View):
    @permission
    def get(self, request):
        user_pk = request.GET.get("user_pk")
        data = {}
        try:
            user = get_object_or_404(User, pk=user_pk)
            reviews = Review.objects.filter(user=user)
            if len(reviews):
                reviews_serial = ReviewSerializer(reviews, many=True)
                reviews_list = reviews_serial.data
                for review in reviews_list:
                    book = get_object_or_404(Book, pk=review["book"])
                    book_serial = BookSerializer(book)

                    review["book_title"] = book_serial.data["title"]
                    review["book_img_url"] = book_serial.data["img_url"]

                data['result'] = reviews_list
            else:
                data["result"] = "작성한 review 가 없습니다."
        except:
            data["error"] = "오류가 발생하였습니다."

        return JsonResponse(data)

    @permission
    def post(self, request):
        # book_pk, review_pk, title, content, content_score, design_score
        data = json.loads(request.body.decode('utf-8'))
        user = request.user
        book_pk = data['book_pk']
        review_pk = data['review_pk']
        review = get_object_or_404(Review, pk=review_pk)

        data['book'] = book_pk
        data['user'] = user.pk
        serializer = ReviewSerializer(review, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            reviews = get_object_or_404(Review, user=user)
            reviews_serial = ReviewSerializer(reviews, many=True)
            data = {}
            data['result'] = reviews_serial.data
            return JsonResponse(data)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        review_pk = request.GET.get("review_pk")
        user = request.user
        try:
            review = get_object_or_404(Review, pk=review_pk)
            review.delete()
            reviews = get_object_or_404(Review, user=user)
            reviews_serial = ReviewSerializer(reviews, many=True)
            data = {}
            data["result"] = reviews_serial.data
        except:
            data['result'] = "review 정보가 없습니다."

        return JsonResponse(data)


class CommentView(View):
    @permission
    def get(self, request):
        user_pk = request.GET.get("user_pk")
        data = {}
        try:
            user = get_object_or_404(User, pk=user_pk)
            comments = ReviewComment.objects.filter(user=user)
            if len(comments):
                comments_serial = ReviewCommentSerializer(comments, many=True)
                data['result'] = comments_serial.data
            else:
                data["result"] = "작성한 comment 가 없습니다."
        except:
            data["error"] = "오류가 발생하였습니다."

        return JsonResponse(data)

    @permission
    def post(self, request):
        # content(text), comment_pk(pk)
        data = json.loads(request.body.decode('utf-8'))
        comment_pk = data["comment_pk"]
        comment = get_object_or_404(ReviewComment, pk=comment_pk)
        user = request.user

        temp_data = {"content": data["content"],
                     "review": comment.review, "user": user}

        serializer = ReviewCommentSerializer(comment, data=temp_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            comments = get_object_or_404(ReviewComment, user=user)
            comments_serial = ReviewCommentSerializer(comments, many=True)

            data = {}
            data['result'] = comments_serial.data
            return JsonResponse(data)

        data['result'] = "fail"
        return JsonResponse(data)

    @permission
    def delete(self, request):
        comment_pk = request.GET.get("comment_pk")
        user = request.user
        try:
            comment = get_object_or_404(ReviewComment, pk=comment_pk)
            comment.delete()
            comments = get_object_or_404(ReviewComment, user=user)
            comments_serial = ReviewCommentSerializer(comments, many=True)
            data = {}
            data["result"] = comments_serial.data
        except:
            data['result'] = "comment 정보가 없습니다."

        return JsonResponse(data)


@csrf_exempt
def address(request):
    data = {}
    data['no_address'] = []
    data['no_loc_code'] = []
    users = User.objects.all()

    city = {'서울': '서울특별시', '부산': '부산광역시', '대구': '대구광역시', '인천': '인천광역시', '광주': '광주광역시', '대전': '대전광역시', '울산': '울산광역시',
            '세종특별자치시': '세종특별자치시', '경기': '경기도', '강원': '강원도',
            '충북': '충청북도', '충남': '충청남도', '전북': '전라북도', '전남': '전라남도', '경북': '경상북도', '경남': '경상남도',
            '제주특별자치도': '제주특별자치도'}

    for user in users:
        address = user.address
        if address:
            address_list = list(address.split())
            # print("city", address_list[0], " to ",city[address_list[0]])
            try:
                locs = user.location_libraries.all()
                if locs:
                    print("loc 관계 이미 존재합니다")
                    for loc in locs:
                        loc.location_users.remove(user)

                gu = " ".join(address_list[1:3])
                loc = get_object_or_404(
                    LibraryLocation, city=city[address_list[0]], gu=gu)
                print(user.pk, loc.loc_code)
                loc.location_users.add(user)

            except:
                try:
                    gu = address_list[1]
                    loc = get_object_or_404(
                        LibraryLocation, city=city[address_list[0]], gu=gu)
                    print(user.pk, loc.loc_code)
                    loc.location_users.add(user)

                except:
                    print(user.pk, "오류입니다2, location code 존재 X")
                    data['no_loc_code'].append(user.pk)
        else:
            print(user.pk, "주소가 존재하지 않습니다")
            data['no_address'].append(user.pk)

    return JsonResponse(data)


@csrf_exempt
def address_delete(request):
    data = {}
    users = User.objects.all()
    locs = LibraryLocation.objects.all()
    for user in users:
        for loc in locs:
            if loc.location_users.filter(pk=user.pk).exists():
                loc.location_users.remove(user)
                continue

    return JsonResponse(data)


class ChartView(View):
    @permission
    def get(self, request):
        user_pk = request.GET.get("user_pk")
        user = get_object_or_404(User, pk=user_pk)
        like_books = user.like_books.all()
        like_books_serial = BookSerializer(like_books, many=True)
        calendars = Calendar.objects.filter(user=user)
        calendars_serial = CalendarSerializer(calendars, many=True)
        reviews = Review.objects.filter(user=user)
        reviews_serial = ReviewSerializer(reviews, many=True)

        data = {"radar": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "line": [
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "radar_info": {}}
        if calendars_serial.data:
            for calendar in calendars_serial.data:
                temp_book = get_object_or_404(Book, pk=calendar["book"])
                temp_book_serial = BookSerializer(temp_book)
                temp_book_data = temp_book_serial.data
                std = temp_book_data["isbn_add3"]//10
                info = temp_book.isbn_add3.desc

                if calendar["end_date"]:
                    tim = int(calendar["end_date"][5:7])
                else:
                    tim = 0
                data["radar"][std] += 1
                if info in data["radar_info"]:
                    data["radar_info"][info] += 1
                else:
                    data["radar_info"][info] = 1
                if tim:
                    data["line"][tim-1] += 1

        if like_books_serial.data:
            for pick in like_books_serial.data:
                std = pick["isbn_add3"]//10
                add3 = get_object_or_404(IsbnAdd3, pk=pick["isbn_add3"])
                info = add3.desc

                data["radar"][std] += 1
                if info in data["radar_info"]:
                    data["radar_info"][info] += 1
                else:
                    data["radar_info"][info] = 1

        if reviews_serial.data:
            for review in reviews_serial.data:
                tim = int(review["created_at"][5:7])
                data["line"][tim-1] += 1

        temp_dict = sorted(data["radar_info"].items(),
                           reverse=True, key=lambda x: x[1])
        data["radar_info"] = temp_dict

        return JsonResponse(data)


@csrf_exempt
def make_dummy(request):
    faker = Faker('ko_KR')
    data2 = []
    for step in range(1, 101):
        # print(fake_id.name().split()[_%2])
        # print(fake_name.profile())
        temp_prof = faker.profile()
        # print(temp_prof["birthdate"])
        name = temp_prof["name"]
        gender = temp_prof["sex"]
        address = temp_prof["address"]
        birth = temp_prof["birthdate"]
        pin = str(step)
        fit = ["000", "00", "0", ""]
        trs_s = {
            "M": 0,
            "F": 1,
        }
        data = {
            "email": "dummy" + fit[len(pin)] + pin + "@bookridge.com",
            "name": name,
            "address": address,
            "gender": trs_s[gender],
            "birth": birth,
            "password1": "test1324",
            "password2": "test1324",
        }
        print(data)
        form = CustomUserCreationForm(data=data)
        if form.is_valid():
            user = form.save()
            UserPrivacy(user=user).save()
            data2.append(user.email)
    data3 = {}
    data3["result"] = data2
    return JsonResponse(data3)


@csrf_exempt
def make_like(request):
    start_pk = 169
    end_pk = 268
    # 책 pk들을 장르마다 담자
    genres = {
        "철학": set([7031, 14311, 2957, 5636, 10205, 19218, 79704, 268, 2018, 6226, 9563, 9603, 12087, 12297, 14439, 16814, 18075, 18280, 19041, 19154, 19519, 20471, 21856, 132, 248, 553, 555, 778, 1223, 1266, 1420, 1559, 1859, 1981, 2557, 2680, 4470, 5135, 5824, 5848, 5863, 6082, 6130, 6151, 6626, 6888, 6997, 7018, 7097, 7123, 7296, 7364, 7617, 7665, 7876, 7923, 7952, 8115, 8138, 8143, 8261, 8446, 8727, 8779, 8783, 8912, 9070, 9071, 9105, 9117, 9177, 9198, 9283, 9357, 9399, 10163, 10179, 10232, 10240, 10258, 10277, 10412, 10431, 10439, 10907, 11198, 11204, 11276, 11410, 11630, 11653, 11685, 11711, 11745, 11794, 12229, 12243, 12250, 12274, 12352, 12542, 12597, 12703, 12863, 13125, 13299, 13326, 13385, 13421, 13506, 13514, 13592, 13866, 13913, 13926, 13999, 14046, 14154, 14323, 14372, 14569, 14690, 14754, 14972, 15280, 15521, 15604, 15773, 15775, 15831, 15855, 15923, 15970, 15982, 16007, 16157, 16292, 16308, 16350, 16520, 16654, 16745, 16889, 17003, 17029, 17132, 17191, 17368, 17453, 17589, 17616, 17747, 17756, 17760, 17852, 18073, 18096, 18161, 18403, 18612, 18740, 18846, 18847, 18852, 18880, 18881, 19075, 19116, 19127, 19345, 19394, 19398, 19460, 19467, 19567, 19677, 19683, 19694, 19943, 20096, 20099, 20184, 20295, 20368, 20391, 20396, 20423, 20501, 20688, 20786, 20813, 20850, 21034, 21127, 21289, 21340, 21468, 21469, 21511, 21548, 21550, 21673, 21756, 21782, 21806, 21822, 23147, 23265, 24873, 26170, 26299, 30356, 31650, 32334, 33197, 36728, 38902, 39046, 39054, 39202, 40451, 40964, 42122, 42616, 42977, 43129, 43385, 43434, 44840, 45407, 46350, 46568, 46987, 48721, 50161, 50316, 50976, 51742, 53730, 55974, 57074, 57583, 58635, 59038, 62583, 62960, 63621, 63961, 64348, 64593, 65761, 66196, 66514, 66854, 66930, 67537, 68389, 68665, 70077, 72305, 72556, 75111, 76504, 76643, 77491, 77698, 78353, 79357, 79815, 80659, 81357, 81756]),
        "경제학": set([1702, 2957, 7327, 10403, 11439, 11446, 12934, 20850, 57528, 16891, 64, 651, 1284, 1789, 4748, 5941, 8978, 9441, 9884, 10826, 11389, 11647, 12919, 13953, 14014, 14049, 15311, 16599, 16684, 16708, 16967, 18243, 18252, 19341, 19622, 19868, 20081, 20129, 20686, 30047, 32345, 49426, 50326, 56328, 56811, 56812, 56813, 61804, 71299, 71682, 72157, 72158, 72607, 78021, 79343, 82931, 40, 208, 258, 280, 348, 384, 421, 650, 972, 1051, 1068, 1076, 1077, 1217, 1269, 1292, 1303, 1378, 1409, 1462, 1544, 1577, 1684, 1770, 1909, 1914, 2020, 2234, 2244, 2308, 2431, 2492, 2571, 2660, 2990, 3552, 3689, 3690, 4031, 4112, 4246, 4728, 4964, 4969, 5042, 5485, 5712, 5969, 7016, 7186, 7301, 7437, 7847, 8205, 8262, 8360, 8383, 8791, 8814, 8816, 8847, 8953, 9074, 9101, 9139, 9281, 9442, 9587, 9638, 9699, 9747, 9768, 9846, 10161, 10189, 10348, 10684, 10732, 10751, 11224, 11231, 11501, 11557, 11669, 11822, 11968, 12604, 13156, 13393, 13397, 13424, 13474, 13544, 13613, 13777, 13877, 13901, 13950, 14010, 14316, 14320, 14451, 14695, 14746, 14985, 15060, 15154, 15447, 15603, 15688, 15884, 16040, 16096, 16191, 16454, 16501, 16542, 16708, 16749, 16752, 17021, 17086, 17170, 17416, 17575, 17696, 17710, 17812, 17847, 18148, 18170, 18197, 18402, 18561, 18734, 18772, 18801, 19159, 19216, 19456, 19546, 19664, 20139, 20613, 20746, 21087, 21972, 23014, 24278, 38933, 50722, 53903, 56105, 56290, 56934, 57414, 58700, 63810, 64300, 67993, 68365, 69101, 69257, 69684, 70993, 71934, 72279, 72879, 77606, 77898, 79413, 79479, 80494, 81248, 81994, 81999, 83153, 83587, 85057, 85175, 87665, 87666, 88163]),
        "실험": set([30, 265, 417, 886, 1048, 1226, 1510, 1938, 2105, 2142, 2415, 2657, 2996, 3189, 3190, 3191, 3192, 3193, 3194, 3195, 3196, 3197, 3198, 3199, 3200, 3201, 3222, 3223, 3330, 3472, 3473, 3474, 3475, 3476, 3477, 3478, 3479, 3480, 3747, 4598, 4621, 4671, 4753, 4813, 4815, 4863, 4962, 5190, 5709, 5711, 6200, 6350, 7359, 7456, 7579, 7798, 8117, 8229, 8366, 8693, 9362, 9716, 10573, 11282, 11870, 12101, 12312, 14260, 14363, 14440, 14639, 14678, 14747, 15003, 15080, 15432, 16445, 16750, 17128, 17329, 17361, 17513, 18530, 19349, 19654, 19819, 19944, 20184, 21944, 26362, 27466, 29298, 38419, 38924, 41204, 52884, 55623, 57340, 62806, 67060, 73360, 199, 303, 305, 307, 355, 387, 389, 410, 412, 505, 512, 546, 547, 548, 549, 628, 629, 630, 643, 743, 761, 762, 770, 783, 784, 828, 862, 904, 905, 906, 926, 935, 940, 941, 968, 969, 989, 1009, 1016, 1028, 1603, 1637, 1656, 1657, 1707, 1708, 1717, 1773, 1774, 1780, 1781, 1782, 1792, 1805, 1828, 1842, 1843, 1861, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1923, 1924, 1925, 1937, 1938, 1939, 1940, 1941, 1949, 2167, 2212, 2254, 2590, 2754, 2885, 2941, 2965, 2971, 3202, 3203, 3204, 3569, 3570, 3571, 3733, 3796, 3797, 3798, 3799, 3800, 3801, 3802, 3803, 4062, 4107, 4232, 4275, 4288, 4375, 4489, 4692, 4694, 4709, 4828, 4829, 4839, 4867, 4879, 4887, 4904, 4954, 5047, 5048, 5049, 5068, 5069, 5078, 5079, 5101, 5166, 5421, 5435, 5481, 5662, 5664, 5768, 5769, 5790, 5799, 5805, 6047, 6103, 6118, 6157, 6215, 6272, 6361, 6422, 6505, 6568, 6584, 6673, 6695, 6696, 6752, 6833, 7015, 7364, 7379, 7469, 7784, 7809, 8776, 9166, 9481, 10486, 10552, 11122, 11322, 11829, 11983, 12539, 13007, 15827, 15942, 16079, 16437, 16718, 16731, 19306, 20242, 29149, 59116, 71058, 74220, 80913, 218, 948, 4463, 4961, 9590, 9699, 10715, 14951, 16294, 19203, 19770, 20053, 21868, 25115, 26002, 29909, 31242, 32869, 37226, 41300, 56705, 58147, 63201, 64280, 64672, 65311, 71338, 71339, 75362, 1831, 11249, 13111, 13669, 20013, 21119, 26068, 28371, 34238, 34382, 41110, 41731, 62814, 66656, 70547, 81443, 8477, 9909, 10307, 10765, 12587, 14955, 16092, 17163, 17192, 17537, 17676, 18160, 18728, 19424, 19636, 21149, 67129, 68476, 72310, 80862, 128, 2305, 3034, 3035, 3036, 3037, 3038, 3040, 3041, 3042, 3043, 3044, 3045, 3047, 3048, 3050, 3051, 3186, 3187, 3188, 3520, 3551, 3618, 3619, 3627, 3632, 3665, 3751, 3822, 3823, 3856, 4092, 4380, 4552, 4583, 4600, 4609, 4620, 4698, 4704, 4859, 5273, 5284, 5285, 5298, 5299, 5303, 5304, 5305, 5306, 5307, 5308, 5360, 5382, 5388, 5389, 5390, 5468, 5535, 5544, 5716, 5835, 5859, 6375, 6438, 6455, 6482, 6906, 7871, 7880, 9454, 9494, 10025, 10129, 10400, 10408, 11537, 11803, 13366, 14521, 14664, 14724, 15654, 16799, 17391, 18328, 18372, 18889, 21084, 21224, 21225, 21229, 21267, 21450, 72977, 75949, 198, 1054, 2606, 2792, 5160, 5709, 5998, 7264, 7798, 8423, 9071, 9357, 9719, 10029, 11021, 11759, 11996, 11998, 13429, 13456, 13524, 13681, 14531, 15348, 15440, 16677, 16776, 17298, 17509, 17815, 18022, 18257, 19182, 19715, 20254, 20462, 20539, 20629, 23000, 24607, 26209, 27909, 37250, 38379, 40405, 41139, 41453, 44308, 44789, 46730, 48009, 54129, 57497, 58928, 60567, 67076, 68322, 69024, 76272, 76481, 77900, 80453, 80734, 82182, 86608, 88293]),
        "물리": set([199, 303, 305, 307, 355, 387, 389, 410, 412, 505, 512, 546, 547, 548, 549, 628, 629, 630, 643, 743, 761, 762, 770, 783, 784, 828, 862, 904, 905, 906, 926, 935, 940, 941, 968, 969, 989, 1009, 1016, 1028, 1603, 1637, 1656, 1657, 1707, 1708, 1717, 1773, 1774, 1780, 1781, 1782, 1792, 1805, 1828, 1842, 1843, 1861, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1923, 1924, 1925, 1937, 1938, 1939, 1940, 1941, 1949, 2167, 2212, 2254, 2590, 2754, 2885, 2941, 2965, 2971, 3202, 3203, 3204, 3569, 3570, 3571, 3733, 3796, 3797, 3798, 3799, 3800, 3801, 3802, 3803, 4062, 4107, 4232, 4275, 4288, 4375, 4489, 4692, 4694, 4709, 4828, 4829, 4839, 4867, 4879, 4887, 4904, 4954, 5047, 5048, 5049, 5068, 5069, 5078, 5079, 5101, 5166, 5421, 5435, 5481, 5662, 5664, 5768, 5769, 5790, 5799, 5805, 6047, 6103, 6118, 6157, 6215, 6272, 6361, 6422, 6505, 6568, 6584, 6673, 6695, 6696, 6752, 6833, 7015, 7364, 7379, 7469, 7784, 7809, 8776, 9166, 9481, 10486, 10552, 11122, 11322, 11829, 11983, 12539, 13007, 15827, 15942, 16079, 16437, 16718, 16731, 19306, 20242, 29149, 59116, 71058, 74220, 80913]),
        "미술관": set([1081, 1105, 1285, 1480, 5806, 6095, 6251, 6410, 7949, 8203, 8528, 9039, 9383, 9792, 10271, 12154, 12296, 12821, 13223, 13428, 13542, 14277, 15004, 15523, 15821, 15978, 16498, 16751, 17978, 18337, 18369, 18435, 18632, 18742, 19018, 20322, 20765, 20974, 21164, 21400, 31933, 39713, 54052, 71719, 74737, 75778, 75797, 81162, 83976, 6, 301, 377, 1932, 2925, 4633, 5678, 6138, 7748, 8656, 9032, 10458, 15835, 16249, 16577, 21346, 21965, 33876, 34683, 37821, 57073, 58444, 61158, 63721, 68283, 71814, 79599, 80050, 87160, 88502, 6471, 7902, 10989, 14081, 14425, 16845, 17020, 58535, 61496, 66247, 69709]),
        "음악": set([1944, 13920, 19658, 31778, 39529, 43529, 43945, 45738, 46208, 46209, 46210, 53687, 55562, 56513, 64477, 68665, 71091, 72293, 9227, 14628, 20798, 30906, 48158, 53371, 64378, 68663, 72653, 72947, 76767, 77348, 78162, 5684, 12598, 13755, 15767, 19040, 20765, 25741, 26299, 26365, 28696, 29480, 29932, 36458, 40222, 43603, 44229, 47919, 48402, 48637, 48882, 50711, 51112, 51797, 53377, 54497, 55220, 55905, 65535, 65928, 67161, 73884, 73926, 74470, 75145, 75381, 78368, 78923, 79254, 81307, 85719, 88502]),
        "문학": set([371, 503, 1082, 1437, 1449, 2104, 2138, 2229, 2315, 2789, 4657, 4995, 5821, 6270, 7182, 7183, 7453, 7544, 8150, 8152, 8193, 8255, 8305, 8339, 8386, 8659,
                   8775, 8980, 9146, 9361, 9381, 9474, 9528, 9580, 9763, 9930, 9980, 10092, 10165, 10456, 10695, 10800, 11127, 11227, 11265, 11502, 11509, 11516, 11577, 11644, 11724, 11751, 12523, 12745, 12966, 13083, 13084, 13171, 13207, 13273, 13405, 13731, 14007, 14278, 14680, 14817, 14862, 14879, 14989, 15042, 15054, 15067, 15097, 15197, 15321, 15415, 15539, 15603, 15653, 15669, 15768, 15780, 15844, 16140, 16265, 16418, 16625, 16634, 16643, 16881, 17035, 17190, 17226, 17277,
                   17567, 17704, 18441, 19579, 19791, 19945, 20437, 20497, 20811, 21421, 21752, 21866, 21882, 22726, 22958, 25508, 25590, 25715, 26161, 26307, 26363, 26785, 26816, 27881, 29433, 30496, 30626, 30909, 30948, 31213, 31323, 31542, 31722, 32294, 32357, 32631, 32653, 32821, 32928, 33034, 33078, 33342, 33353, 33476, 33522, 33803, 33911, 33928, 34424, 34425, 34430, 34442, 34869, 35276, 35925, 35970, 36350, 36581, 36613, 37266, 37813, 37941, 38392, 38906, 39517, 39518, 39803, 40000, 40688, 41002, 41320, 41429, 41465, 41684, 41752, 41923, 43237, 43368, 43561, 44418, 44498, 45393, 45703, 46565, 46661, 46924, 48428, 48515, 49351, 49358, 49609, 51178, 51372, 52433, 52708, 53413, 53530, 54138, 54354, 54449, 54464, 54671, 54825, 54911, 54999, 55732, 55839, 56236, 56292, 56551, 58268, 58404, 59820, 59887, 62477, 63085, 63088, 63113, 63288, 65034, 66186, 66276, 66692, 67245, 67281, 68059, 69290, 69354, 70062, 71479, 71486, 71689, 72481, 72763, 73139, 74217, 74348, 75045, 75086, 75087, 75656, 75661, 75806, 75965, 76566, 76756, 76804, 77516, 77896, 78034, 78450, 78650, 78790, 78804, 79207,
                   79771, 81818, 82182, 82382, 84116, 84373, 85403, 86014, 86140, 87516, 88481, 15, 178, 455, 469, 686, 691, 920, 1110, 1115, 1324, 1568, 1867, 2040, 2054, 2077, 2166, 2169, 2263, 2372, 2391, 2479, 2485, 2523, 2694, 2733, 2765, 2781,
                   3006, 3068, 3077, 3131, 3220, 3242, 3481, 3507, 3513, 3514, 3560, 3561, 3573, 3678, 3697, 3850, 3994, 4046, 4058, 4059, 4237, 4244, 4278, 4279, 4382, 4383, 4384, 4385, 4460, 4491, 4500, 4522, 4616, 4637, 4651, 4652, 4658, 4665, 4686, 4727, 4817, 4852, 4864, 4928, 5143, 5189, 5362, 5692, 5917, 6072, 6095, 6298, 6319, 6335, 6430, 6431, 6574, 6623, 6629, 6648, 6652, 6691, 6697, 6788, 6821, 6967, 6985, 7092, 7474, 7658, 7721, 7894, 7907, 8140, 8151, 8295, 8530, 8586, 8638, 8679, 8854, 8989, 9016, 9034, 9078, 9148, 9183, 9210, 9279, 9330, 9387, 9394, 9817, 9963, 10063, 10173, 10550, 10569, 10674, 10694, 10887, 10909,
                   10911, 11317, 11398, 11406, 11407, 11742, 11801, 11836, 12329, 12341, 12357, 12377, 12538, 12763, 12823, 12858, 12865, 13026, 13209, 13279, 13414, 13674, 13708, 13720, 14008, 14132, 14567, 14692, 14716, 14728, 14738, 14833, 14901, 14916, 14982, 14983, 15084, 15085, 15239, 15273, 15662, 15720, 15721, 15742, 15863, 15885, 15955, 16112, 16172, 16299, 16507, 16546, 16637, 16738, 16785, 16786, 16810, 17025, 17062, 17225, 17237, 17313, 17636, 17664, 17900, 18042, 18281, 18318, 18319, 18351, 18601, 18620, 18641, 18885, 19175, 19284, 19502, 19913, 20071, 20103, 20128, 20162, 20255, 20264, 20270, 20294, 20353, 20361, 20496, 20567, 20581, 20584, 20585, 20589, 20591, 20598, 20600, 20606, 20695, 20696, 20742, 20844, 20875, 20901, 20916, 21018, 21044, 21128, 21137, 21189, 21204, 21212, 21254, 21260, 21261, 21326, 21332, 21368, 21376, 21377, 21495, 21522, 21539, 21540, 21568, 21647, 21648, 21701, 21729, 21803, 22920, 23032, 23245, 23707, 23824, 24059, 24147, 24148, 24297, 24298, 24361, 24782, 24783, 24784, 24849, 25020, 25023, 25026, 25027, 25028, 25029, 25030, 25031, 25033, 25034,
                   25036, 25041, 25042, 25043, 25044, 25045, 25046, 25418, 25468, 25471, 25472, 25490, 25536, 25818, 26017, 26018, 26128, 26131, 26132, 26133, 26135, 26137, 26182, 27070, 27202, 27372, 27376, 27378, 27429, 27515, 27519, 27520, 27570, 27574, 27640, 28118, 28177, 28178, 28306, 28620, 28637, 29279, 29343, 29721, 30137, 30517, 30518, 30519, 30522, 30817, 30839, 30847, 30849, 30850, 30859, 30977, 31056, 31138, 31148, 31291, 31487, 31717, 31826, 31827, 31834, 31912, 31925, 31926, 31940, 31963, 32004, 32007, 32024, 32036, 32043, 32211, 32327, 32449, 32667, 32705, 32707, 32723, 32736, 32879, 32880, 32899, 32999, 33011, 33015, 33128, 33204, 33551, 33617, 33622, 33625, 33824, 33946, 33949, 34375, 34675, 35138, 35140, 35702, 36315, 36319, 36320, 36610, 36611, 36623, 36639, 36655, 36677, 37158, 37291, 37977, 38256, 38257, 38258, 38262, 38264, 38569, 38637, 38641, 38855, 38879, 39084, 39089, 39474, 39475, 39490, 39710, 39858, 39874, 40075, 40081, 40464, 40559, 40588, 40634, 40677, 40767, 40781, 40782, 40785, 40831, 41100, 41158, 41370, 41473, 41685, 41879, 43227, 43833, 44208, 44899,
                   45363, 45578, 45794, 45851, 45897, 46141, 46703, 46840, 46841, 46898, 46917, 47025, 47152, 47796, 48553, 48554, 48571, 48572, 48573, 48574, 48575, 48737, 49238, 49239, 49482, 49934, 49935, 49936, 49938, 49939, 50731, 51039, 51160, 51183, 51184, 51733, 51745, 51746, 51747, 51917, 51998, 51999, 53010, 53064, 53065, 53339, 53340, 53431, 53514, 53515, 53517, 53518, 53574, 53928, 53929, 53954, 54017, 54087, 54152, 54345, 54346, 54347, 54448, 54453, 54476, 54565, 54615, 54632, 54813, 54816, 54870, 55140, 55144, 55145, 55147, 55196, 55197, 55198, 55227, 55293, 55294, 55328, 55331, 55333, 55376, 55400, 55419, 55420, 55421, 55423, 55434, 55487, 55580, 55592, 55814, 55868, 55906, 56239, 56256, 56265, 56342, 56388, 56390, 56414, 56419, 56453, 56526, 56527, 56534, 56535, 56537, 56572, 56576, 56585, 56598, 56599, 57068, 57378, 57705, 57772, 57833, 57855, 57942, 58039, 58280, 58444, 58702, 59594, 59636, 59905, 63264, 64211, 64450, 64918, 65459, 65496, 65688, 65742, 65779, 65986, 66223, 66292, 66318, 66335, 66347, 66348, 66459, 66471, 66533, 66799, 67201, 67854, 67860, 67865, 68318,
                   68617, 68618, 68619, 68620, 68973, 69351, 69722, 69935, 69937, 70013, 70131, 70535, 70820, 70933, 71584, 71703, 71720, 71721, 71724, 71729, 71734, 71738, 71764, 71771, 71775, 71809, 71822, 71826, 71830, 71836, 71843, 71848, 71851, 71853, 71862, 71895, 71898, 71915, 71923, 71924, 71967, 71968, 71979, 71987, 72203, 72362, 72368, 72391, 72460, 72485, 72492, 72505, 72510, 72516, 72571, 72621, 72633, 72659, 72668, 72765, 72782, 72828, 72962, 73047, 73114, 73167, 73371, 73476, 73477, 73478, 73479, 73480, 73481, 73482, 73483, 73484, 73485, 73486, 73487, 73488, 73489, 73490, 73491, 73492, 73493, 73494, 73495, 73496, 73497, 73498, 73499, 73500, 73501, 73502, 73503, 73504, 73505, 73506, 73507, 73508, 73509, 73510, 73511, 73512, 73513, 73514, 73515, 73516, 73517, 73518, 73519, 73520, 73521, 73522, 73523, 73524, 73525, 73526, 73527, 73528, 73529, 73530, 73531, 73532, 73533, 73534, 73535, 73536, 73537, 73538, 73539, 73540, 73541, 73542, 73543, 73544, 73545, 73546, 73547, 73653, 73654, 73834, 74162, 74182, 74476, 75094, 75146, 75147, 75266, 75574, 75841, 75855, 75858, 75904, 76030,
                   76142, 76143, 76165, 76332, 76567, 76650, 76673, 76680, 76770, 76771, 76856, 76900, 77100, 77155, 77188, 77376, 77378, 77382, 77383, 77616, 77970, 77971, 78023, 78077, 78152, 78306, 78401, 78403, 78413, 78477, 78479, 78481, 78482, 78486, 78492, 78495, 78571, 78582, 78585, 78813, 78814, 78819, 78917, 79020, 79070, 79124, 79125, 79151, 79190, 79268, 79290, 79291, 79292, 79319, 79357, 79431, 79432, 79463, 79503, 79520, 80061, 80062, 80065, 80066, 80067, 80068, 80069, 80071, 80072, 80084, 80087, 80088, 80090, 80091, 80092, 80093, 80094, 80924, 81093, 81308, 81555, 81719, 81856, 81895, 82012, 82016, 82029, 82583, 83141, 83142, 83143, 83163, 83177, 83179, 83182, 83207, 83208, 83209, 83210, 83211, 83249, 83350, 83355, 83357, 83359, 83361, 83362, 83382, 83395, 83399, 83400, 83401, 83402, 83403, 83404, 83405, 83407, 83408, 83409, 83410, 83411, 83412, 83413, 83414, 83415, 83416, 83417, 83418, 83419, 83420, 83421, 83422, 83423, 83424, 83425, 83426, 83427, 83428, 83429, 83430, 83431, 83432, 83433, 83434, 83435, 83436, 83437, 83438, 83439, 83440, 83441, 83442, 83443, 83444, 83445,
                   83591, 83669, 83698, 83804, 83834, 83835, 83921, 83926, 83928, 83934, 83976, 83985, 83986, 83987, 83988, 83990, 84028, 84084, 84085, 84104, 84114, 84119, 84120, 84126, 84127, 84128, 84198, 84199, 84228, 84231, 84263, 84302, 84309, 84310, 84311, 84312, 84313, 84314, 84315, 84316, 84317, 84319, 84320, 84321, 84340, 84352, 84550, 84599, 84607, 84608, 84609, 84610, 84612, 84613, 84669, 84701, 84952, 84972, 84978, 84987, 85007, 85305, 85448, 85735, 85745, 85954, 85955, 85956, 85957, 85958, 85959, 85960, 86146, 86176, 86510, 86642, 86657, 86663, 86679, 86680, 86681, 86689, 86691, 86697, 86805, 86806, 86913, 86916, 86923, 86925, 86984, 86990, 86992, 86993, 87049, 87050, 87063, 87099, 87106, 87264, 87265, 87321, 87570, 87573, 87583, 87750, 87944, 88365, 88538, 88539]),
        "영문": set([3144, 3145, 3146, 3147, 3148, 3521, 3522, 3523, 3524, 4674, 4770, 4877, 5344, 5345, 6412, 6413, 6650, 6770, 6807, 6808, 7573, 7574, 7589, 7800, 8509, 8571, 8762, 9160, 9679, 9876, 10980, 15905,
                   18003, 18032, 24362, 28680, 28959, 32499, 33378, 36390, 37728, 37899, 38521, 38853, 41258, 41571, 43016, 43430, 43962, 43986, 44354, 45433, 45434, 45928, 47033, 47091, 48429, 48753, 51110, 51550, 51642, 52964, 53692, 54099, 56832, 56960, 57073, 57521, 57528, 57722, 57821, 57822, 57823, 58421, 58439, 58440, 58442, 58444, 58446, 58447, 58451, 58606, 61197, 61474, 64734, 67296, 68335, 69804, 72598, 74696, 76006, 76183, 78245, 78878, 78933, 79118, 79139, 83448, 86599, 88610, 88630, 88715, 88725, 88795]),
        "부처": set([6207, 8829, 9613, 15040, 15529, 17003, 18694, 24452, 27043, 27608, 27923, 29503, 29954, 31282, 31711, 32342, 33356, 33485, 34279, 40556, 40691, 41354, 42736, 43916, 45040, 45041, 45940, 46457, 49985, 50348, 50699, 51543, 52840, 53716, 54968, 56417, 68034, 73030, 74783, 74965, 75047, 75392, 77992, 78390, 80746, 80988, 83123, 83287, 87494, 88298, 125, 138, 147, 209, 541, 610, 613, 751, 1108, 1778, 2095, 2119, 2319, 2364, 2533, 2557, 5420, 5848, 5856, 6765, 7026, 7080, 7194, 8243, 8245, 8267, 8691, 8925, 9076, 9200, 9275, 9404, 9857, 9910, 10257, 10335, 10354, 10867, 11105, 11256, 11415, 12710, 12774, 14691, 14835, 14867, 14883, 15251, 15370, 16902, 17059, 17439, 17504, 18091, 18983, 19833, 19895, 23137, 23173, 24443, 24467, 24468, 26433, 28858, 29253, 29296, 29503, 29779, 29893, 30041, 31081, 31123, 31651, 32403, 32734, 32861, 33068, 33552, 35568, 35988, 36226, 36658, 38597, 39631, 39633, 39927, 41445, 42981, 43269, 43458, 44361, 44362, 44363, 45250, 45291, 45630, 45951, 45952, 46070, 46229, 46483, 47330, 47331, 48222, 48697, 48890, 48891, 49062, 50557, 50615, 51529, 51658, 52192, 52193, 52836, 52918, 53358, 53720, 54488, 54661, 59265, 59364, 61198, 62030, 62308, 64017, 64102, 64230, 65624, 66353, 66451, 66501, 66557, 66653, 66667, 67396, 67453, 67937, 67972, 68034, 68656, 69077, 69564, 71797, 71820, 72004, 72304, 72469,
                   72815, 72885, 72911, 73214, 74733, 75310, 75611, 75862, 75995, 76265, 76329, 76347, 76642, 76878, 76911, 77992, 78153, 78499, 79713, 79898, 80746, 80986, 81625, 81686, 82091, 83767, 83786, 84050, 84625, 84681, 85660, 87241, 625, 1738, 2657, 5420, 9653, 10975, 14359, 15216, 15663, 16497, 17048, 17444, 23173, 25331, 26845, 30398, 31163, 31566, 33485, 35493, 36780, 40760, 46124, 46150, 51744, 54460, 55334, 59084, 59620, 59996, 63703, 65278, 66821, 68172, 69711, 71437, 77419, 77835, 78445, 79357, 82410, 84477, 85130, 86629, 86736, 87489, 87696, 8779, 12594, 15288, 21660, 62359]),
        "기도": set([2551, 2713, 5708, 5730, 6538, 6775, 9113, 9219, 9893, 9969, 10900, 12796, 13978, 15768, 17895, 18015, 19165, 19497, 19671, 20290, 21158, 21381, 25115, 26654, 26956, 27454, 27488, 28463, 29317, 30055, 30420, 31567, 32927, 33058, 33144, 35928, 37342, 37878, 38362, 38423, 39299, 39782, 39854, 40367, 41682, 42095, 42705, 43989, 46071, 46155, 46325, 46650, 48736, 49489, 53213, 53437, 54420, 55947, 57019, 57337, 58435, 58623, 59420, 60354, 60377, 61828, 62840, 63739, 64510, 65432, 65872, 66829, 68739, 69630, 70647, 72062, 73917, 73978, 74825, 74956, 75338, 75609, 76092, 76199, 76580, 77505, 77760, 77782, 78291, 78344, 78724, 79007, 79069, 79373, 80842, 81186, 81241, 81332, 81415, 82500, 82575, 83203, 83540, 84316, 84440, 86103, 520, 4960, 5908, 8437, 9112, 11146, 15529, 17984, 22971, 26248, 40151, 46437, 47662, 49116, 49961, 49962, 49963, 49964, 50134, 50135, 50136, 50572, 50573, 50574, 56423, 59913, 62283, 63467, 66850, 67296, 72910, 74890, 77279, 88729]),
        "삶": set([44, 163, 188, 203, 205, 267, 404, 458, 573, 607, 653, 751, 854, 858, 889, 948, 982, 1022, 1055, 1064, 1082, 1163, 1193, 1232, 1241, 1290, 1364, 1411, 1435, 1470, 1503, 1539, 1600, 1609, 1621, 1625, 1636, 1674, 1693, 2282, 2298, 2310, 2393, 2432, 2557, 2580, 2637, 2646, 2650, 2655, 2712, 2725, 2734, 2880, 2939, 2957, 3611, 4109, 4206, 4216, 4369, 4429, 4479, 4751, 4777, 5119, 5184, 5423, 5459,
                  5626, 5636, 5656, 5794, 5837, 5848, 5946, 5964, 5966, 6003, 6021, 6029, 6039, 6090, 6132, 6144, 6167, 6186, 6217, 6357, 6377, 6718, 6987, 7090, 7174, 7180, 7224, 7243, 7334, 7344, 7401, 7415, 7423, 7456, 7780, 7819, 7876, 7938, 7944, 8026, 8037, 8064, 8096, 8106, 8183, 8193, 8210, 8307, 8308, 8313, 8316, 8394, 8423, 8433, 8667, 8832, 8943, 9093, 9095, 9105, 9109, 9196, 9213, 9256, 9266, 9439, 9452, 9472, 9572, 9614, 9620, 9626, 9630, 9640, 9651, 9687, 9722, 9751, 9879, 9932, 9933, 9979, 10087, 10205, 10210, 10321, 10350, 10368, 10382, 10439, 10474, 10480, 10594, 10733, 10749, 10751, 10768, 10778, 10824, 10903, 11043, 11140, 11171, 11194, 11249, 11288, 11396, 11421, 11464, 11591, 11604, 11612, 11706, 11739, 11748, 11777, 11833, 11878, 11885, 11895, 11912, 11956, 11982, 12100, 12111, 12120,
                  12141, 12144, 12224, 12226, 12279, 12321, 12326, 12328, 12489, 12492, 12554, 12600, 12608, 12616, 12662, 12703, 12749, 12757, 12768, 12776, 12782, 12812, 12886, 12892, 12935, 13158, 13182, 13354, 13468, 13506, 13558, 13622, 13626, 13728, 13863, 13868, 13926, 13973, 13999, 14001, 14067, 14196, 14210, 14214, 14219, 14262, 14279, 14280, 14283, 14340, 14436, 14484, 14496, 14508, 14647, 14807, 14822, 14881, 14891, 14965, 14975, 15148, 15187, 15203, 15213, 15216, 15251, 15303, 15309, 15338, 15370, 15387, 15388, 15420, 15428, 15510, 15555, 15588, 15636, 15661, 15665, 15675, 15700, 15776, 15823, 15844, 15979, 16001, 16106, 16108, 16145, 16164, 16215, 16343, 16354, 16418, 16442, 16520, 16522, 16608, 16677, 16715, 16778, 16863, 16877, 16905, 16916, 16975, 17034, 17151, 17173, 17185, 17353, 17387, 17401, 17429, 17431, 17453, 17480, 17543, 17633, 17730, 17750, 17776, 17914, 18018, 18027, 18034, 18058, 18091, 18146, 18185, 18190, 18220, 18243, 18375, 18388, 18417, 18424, 18445, 18474, 18483, 18522, 18540, 18559, 18563, 18673, 18708, 18726, 18763, 18766, 18770, 18779, 18788, 18790, 18798, 18804, 18833, 18879, 18911, 18921, 18925, 18937, 18974, 19001, 19010, 19029, 19045, 19175, 19218, 19231, 19361, 19398, 19402, 19404, 19407, 19453, 19459, 19468, 19538, 19630, 19641, 19683, 19700, 19777, 19819, 19843, 19848, 19867, 20050, 20070, 20182, 20193, 20316, 20406, 20463, 20468, 20770, 20789, 20835,
                  20983, 21020, 21029, 21161, 21290, 21369, 21511, 21516, 21751, 21933, 21990, 21991, 22743, 22761, 22786, 22894, 22899, 22925, 22979, 23109, 23129, 23323, 23786, 23911, 24201, 24396, 24521, 24522, 24551, 24607, 24627, 24665, 24677, 24701, 24725, 24817, 24834, 25392, 25504, 25592, 25626, 25646, 25715, 25809, 26150, 26211, 26240, 26385, 26460, 26542, 26634, 26826, 26907, 26946, 26996, 27307, 27420, 27436, 27481, 27564, 27588, 27602, 27607, 27791, 27862, 27869, 27940, 28337, 28348, 28460, 28500, 28590, 28726, 28791, 28907, 29009, 29241, 29382, 29394, 29424, 29487, 29497, 29761, 29848, 29941, 29945, 29977, 29981, 30549, 30703, 30773, 30776, 30918, 30949, 31087, 31360, 31408, 31543, 31545, 31571, 31858, 31873, 31998, 32272, 32363, 32488, 32539, 32604, 32673, 32716, 32744, 32784, 32870, 32937, 32977, 32998, 33189, 33224, 33227, 33278, 33396, 33416, 33532, 33598, 33755, 33885, 33886, 33893, 33896, 33930, 34176, 34206, 34207, 34242, 34248, 34280, 34310, 34380, 34521, 34528, 34872, 34900, 34989, 35038, 35158, 35309, 35532, 35632, 35776, 35805, 35993, 36060, 36066, 36074, 36266, 36362, 36774, 36826, 37181, 37260, 37279, 37367, 37516, 37667, 37700, 37729, 38018, 38033, 38063, 38098, 38107, 38183, 38216, 38252, 38314, 38330, 38391, 38577, 38597, 38610, 39069, 39076, 39077, 39340, 39439, 39552, 39575, 39678, 39698, 39752, 39909, 39915, 39987, 40009, 40036, 40176, 40198, 40352, 40360, 40482,
                  40498, 40524, 40605, 40750, 40831, 40850, 41138, 41154, 41230, 41263, 41291, 41613, 41653, 42069, 42219, 42255, 42314, 42468, 42504, 42573, 42990, 43446, 43447, 43638, 43703, 43815, 44007, 44040, 44259, 44390, 44635, 44719, 44907, 45025, 45248, 45796, 46130, 46664, 46781, 46823, 46948, 47187, 47259, 47326, 47415, 47422, 47423, 47424, 47640, 47700, 47858, 48006, 48094, 48406, 48407, 48670, 48688, 48812, 49465, 49516, 49576, 50247, 50308, 50583, 50723, 51093, 51380, 51640, 51645, 51867, 51949, 51981, 52093, 52096, 52174, 52513, 52733, 52873, 53066, 53156, 53173, 53512, 53571, 53832, 54047, 54114, 54177, 54200, 54366, 54435, 54453, 54594, 54786, 54820, 55233, 55487, 55961, 55962, 56358, 56615, 56763, 56807, 57051, 57074, 57240, 57253, 57351, 57363, 57379, 57525, 57629, 57631, 57710, 57790, 57863, 57908, 58136, 58157, 58203, 58374, 58428, 58671, 58699, 58774, 58920, 58948, 59108, 59176, 59350, 59378, 59409, 59412, 59417, 59478, 59521, 59673, 59718, 59913, 60405, 60439, 60505, 60513, 60533, 60541, 60551, 60994, 61105, 61165, 61195, 61231, 61561, 61926, 62030, 62171, 62222, 62283, 62469, 62476, 62588, 62668, 62706, 62803, 62857, 62960, 62969, 63094, 63416, 63429, 63571, 63786, 63850, 63910, 63925, 63988, 64001, 64027, 64114, 64295, 64444, 64485, 64581, 64591, 64603, 64701, 64728, 64779, 64854, 65018, 65036, 65189, 65323, 65416, 65491, 65522, 65647, 65675, 65676, 65750, 65758, 65836,
                  65936, 66105, 66145, 66451, 66462, 66550, 66603, 66626, 66637, 66788, 66983, 67020, 67079, 67081, 67126, 67269, 67468, 67544, 67632, 67639, 67642, 67647, 67648, 67682, 67776, 67786, 67921, 68049, 68104, 68254, 68352, 68550, 68746, 68891, 69070, 69102, 69141, 69267, 69418, 69440, 69573, 69740, 69826, 69883, 70059, 70096, 70270, 70456, 70492, 70501, 70528, 70716, 70779, 70872, 71687, 71765, 71947, 72139, 72246, 72283, 72321, 72423, 72472, 72480, 72551, 72553, 72577, 72598, 72612, 72674, 72679, 72815, 72876, 72956, 72971, 73022, 73079, 73221, 73639, 73837, 73862, 73889, 74382, 74393, 74416, 74489, 74501, 74569, 74619, 74814, 74980, 75085, 76525, 76571, 76797, 77075, 77098, 77245, 77324, 77368, 77372, 77459, 77532, 77579, 77681, 77990, 78094, 78145, 78156, 78161, 78163, 78380, 78447, 78608, 78615, 78658, 78790, 78801, 78938, 78969, 78977, 79151, 79432, 79570, 79575, 79602, 79704, 79772, 79798, 79823, 79838, 79868, 79900, 79910, 80005, 80042, 80044, 80261, 80349, 80443, 80500, 80554, 80588, 80608, 80631, 80719, 80726, 80773, 80861, 80986, 81070, 81168, 81291, 81390, 81495, 81599, 81690, 81708, 81734, 81736, 81756, 82178, 82411, 82580, 82622, 82717, 84386, 84387, 84575, 85072, 85451, 85794, 85937, 86388, 86391, 86435, 86445, 86455, 86478, 86816, 87393, 87473, 87505, 87836, 87857, 87874, 87892, 87905, 87921, 87933, 88007, 88037, 88044, 88793, 88814]),
        "생물학": set([849, 1080, 2309, 2933, 2965, 3035, 3551, 8513, 8751, 9213, 9441, 10391, 14960, 14991, 15268, 19724, 20127, 20949, 21155, 22860, 22967, 28799, 32836, 34786, 36038, 40783, 42394, 43983, 53995, 54515, 54552, 54565, 71917, 75750, 88866, 4245, 7294, 7678, 9311, 10998, 11596, 14382, 14453, 18895, 19132, 19708, 37253, 39566])
    }
    genres_lst = ["철학", "경제학","실험","물리","미술관","음악","문학","영문","부처","기도","삶","생물학"]
    # 전체 pk들
    pks = set()
    for lst in genres.values():
        pks.update(lst)
    # print(len(pks))
    # 20, 20, 10 비율로 넣자 start_pk, end_pk+1
    for huuuuuman in range(start_pk+1, end_pk+1):
        user = get_object_or_404(User, pk=huuuuuman)
        picks = random.sample(genres_lst, 2)
        temp1 = random.sample(genres[picks[0]], 30)
        temp2 = random.sample(genres[picks[1]], 20)
        temp3 = random.sample(pks, 10)
        print(user)
        for step in range(30):
            # print(temp1[step])
            user.like_books.add(temp1[step])
            if 10 <= step < 20:
                # print(temp2[step])
                user.like_books.add(temp2[step])
            elif step < 10:
                # print(temp3[step])
                user.like_books.add(temp2[step])
                user.like_books.add(temp3[step])

    data = {}
    data["result"] = "아몰랑"
    return JsonResponse(data)
