from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View

from decouple import config

import json
import numpy as np
from .models import Book
from .models import PopularBook
from accounts.models import User
from libraries.models import LibraryLocation
from django.contrib.auth import get_user_model
from .serializers import BookSerializer
from .serializers import PopularBookSerializer
from accounts.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from accounts.utils import permission
import requests
from collections import Counter

from analyze.tendency import UserTendency

def get_book_list(request):
    books = Book.objects.all()[:20000]
    res = BookSerializer(books, many=True)

    return JsonResponse(res.data, safe=False)

def get_pop_book_list(request):
    pop_books = PopularBook.objects.all()
    pop_book_serial = PopularBookSerializer(pop_books, many=True)

    return JsonResponse(pop_book_serial.data, safe=False)

def book_detail(request, book_pk):
    user_pk = request.GET.get("user_pk") 
    user = get_object_or_404(User, pk=user_pk)
    
    book = get_object_or_404(Book, pk=book_pk)
    book_serial = BookSerializer(book)
    
    data = {}
    data["like_count"] = book.like_users.count()
    data["unlike_count"] = book.unlike_users.count()

    # 유저 성향 확인
    ut = UserTendency(user)
    score = ut.get_books_user_tendency_score(book_pk)

    data["score"] = score if score >= 0.55 else False
    
    if user.like_books.filter(pk=book_pk).exists():
        data["like"] = True
        data["unlike"] = False
    elif user.unlike_books.filter(pk=book_pk).exists():
        data["like"] = False
        data["unlike"] = True
    else:
        data["like"] = False
        data["unlike"] = False
    for key, val in book_serial.data.items():
        data[key] = val

    try:
        pop_book = PopularBook.objects.filter(book=book)
        # print(pop_book)
        pop_book_serial = PopularBookSerializer(pop_book, many=True)
        # print(pop_book_serial.data)
        data["popular"] = {}
        data["popular"]['gender'] = {'남성':0, '여성':0}
        data["popular"]['age'] = [0,0,0,0,0,0,0]
        data["popular"]["date"] = {}
        data["popular"]["date"]["2017"] = {}
        data["popular"]["date"]["2018"] = {}
        data["popular"]["date"]["2019"] = {}
        data["popular"]["date"]["2020"] = {}
        data["popular"]["date"]["2017"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2018"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2019"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        data["popular"]["date"]["2020"] = [0,0,0,0,0,0,0,0,0,0,0,0]
        # print(pop_book_serial.data)
        for pick in pop_book_serial.data:
            # print(pick)
            if pick["gender"] == 0:
                data["popular"]['gender']['남성'] += pick['rent_count']
            else:
                data["popular"]['gender']['여성'] += pick['rent_count']
            if pick['age'] == "8~13세":
                data["popular"]["age"][0] += pick['rent_count']
            elif pick['age'] == "14~19세":
                data["popular"]["age"][1] += pick['rent_count']
            elif pick['age'] == "20대":
                data["popular"]["age"][2] += pick['rent_count']
            elif pick['age'] == "30대":
                data["popular"]["age"][3] += pick['rent_count']
            elif pick['age'] == "40대":
                data["popular"]["age"][4] += pick['rent_count']
            elif pick['age'] == "50대":
                data["popular"]["age"][5] += pick['rent_count']
            elif pick['age'] == "60세 이상":
                data["popular"]["age"][6] += pick['rent_count']

            year = pick['start_date'][:4]
            month = int(pick['start_date'][5:7])-1

            data["popular"]["date"][year][month] += pick['rent_count']
            
    except: 
        data['error'] = "도서 대여 정보가 없습니다."

    return JsonResponse(data)

class BookSearchView(View):
    @permission
    def get(self, request):
        user = request.user
        search_word = request.GET.get("search_word")
        search_type = request.GET.get("search_type")
        page = int(request.GET.get("page_num"))
        data2 = {}

        def page_conf(lst, leng, page_num):
            if leng % 9: # 나머지가 있다. 
                if leng // 9 == page_num: # 단, 10개 꽉 채워지진 않는다.
                    return lst[page_num*9:]
                elif leng // 9 > page_num: # 
                    return lst[page_num*9:(page_num+1)*9]
                elif leng // 9 < page_num: # 남은게 10개 초과다.
                    return []
            else: # 나머지 없다.
                if leng // 9 <= page_num: # 더 이상 보내줄 데이터가 없다.
                    return []
                else: # 
                    return lst[page_num*9:(page_num+1)*9]

        if search_word:
        # search_type
        # 제목(0), 작가(1), 출판사(2)
            if int(search_type) == 0:
                try:
                    books = Book.objects.filter(title__icontains=search_word)
                    books_serial = BookSerializer(books, many = True)

                    temp_len = len(books_serial.data)
                    temp_books = page_conf(books_serial.data, temp_len, page)
                    for book in temp_books:
                        if user.like_books.filter(pk=book["id"]).exists():
                            book["like"] = True
                            book["unlike"] = False
                        elif user.unlike_books.filter(pk=book["id"]).exists():
                            book["like"] = False
                            book["unlike"] = True
                        else:
                            book["like"] = False
                            book["unlike"] = False
                    data2['result'] = temp_books
                except:
                    data2['error'] = "도서 대여 정보가 없습니다."
            elif int(search_type) == 1:
                try:
                    books = Book.objects.filter(author__icontains=search_word)
                    books_serial = BookSerializer(books, many = True)

                    temp_len = len(books_serial.data)
                    temp_books = page_conf(books_serial.data, temp_len, page)
                    for book in temp_books:
                        if user.like_books.filter(pk=book["id"]).exists():
                            book["like"] = True
                            book["unlike"] = False
                        elif user.unlike_books.filter(pk=book["id"]).exists():
                            book["like"] = False
                            book["unlike"] = True
                        else:
                            book["like"] = False
                            book["unlike"] = False
                    data2['result'] = temp_books
                except:
                    data2['error'] = "도서 대여 정보가 없습니다."
            elif int(search_type) == 2:
                try:
                    books = Book.objects.filter(publisher__icontains=search_word)
                    books_serial = BookSerializer(books, many = True)
                    
                    temp_len = len(books_serial.data)
                    temp_books = page_conf(books_serial.data, temp_len, page)
                    for book in temp_books:
                        if user.like_books.filter(pk=book["id"]).exists():
                            book["like"] = True
                            book["unlike"] = False
                        elif user.unlike_books.filter(pk=book["id"]).exists():
                            book["like"] = False
                            book["unlike"] = True
                        else:
                            book["like"] = False
                            book["unlike"] = False
                    data2['result'] = temp_books
                except:
                    data2['error'] = "도서 대여 정보가 없습니다."
            return JsonResponse(data2)
        else:
            data2['result'] = "fail"
        return JsonResponse(data2)

def book_auto_search(request):
    try:
        search_word = request.GET.get("search_word")
    except:
        search_word = ""
    data2 = {}

    if search_word:
        try:
            books = Book.objects.filter(title__istartswith=search_word)
            books_serial = BookSerializer(books, many = True)

            data2['result'] = books_serial.data[:6]
        except:
            data2['result'] = []
            data2['error'] = "도서 정보가 없습니다."

        return JsonResponse(data2)

@csrf_exempt
def like_book(request):
    print("진입")
    book_pk = int(request.GET.get("book_pk"))
    user_pk = int(request.GET.get("user_pk"))
    user = get_object_or_404(get_user_model(), pk=user_pk)
    book = get_object_or_404(Book, pk=book_pk)

    if book.like_users.filter(pk=user.pk).exists():
        book.like_users.remove(user)
        liked = False
    else:
        book.like_users.add(user)
        liked = True
    
    book = get_object_or_404(Book, pk=book_pk)
    print(book.like_users)

    data2 = {
        "liked" : liked,
        "count" : book.like_users.count(),
    }

    return JsonResponse(data2)
    
@csrf_exempt
def library(request):
    def calc_distance(lat1, lon1, lat2, lon2):
        r = 6371
        lat2 = float(lat2)
        lon2 = float(lon2)
        phi1 = np.radians(lat1)
        phi2 = np.radians(float(lat2))
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)
        a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
        return r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    # 필요 params book_pk, user_pk
    authkey = config('NARU_AUTH_KEY')
    data2 = {}
    data2["result"] = {}

    book_pk = int(request.GET.get("book_pk"))
    user_pk = int(request.GET.get("user_pk"))

    book = get_object_or_404(Book, pk=book_pk)
    user = get_object_or_404(User, pk=user_pk)

    data2["result"]["user"] = {"latitude":user.latitude, "longitude":user.longitude}

    try:
        locs = LibraryLocation.objects.filter(location_users=user)
        for loc in locs:
            Url = f"http://data4library.kr/api/libSrchByBook?authKey={authkey}&isbn={book.isbn}&region={str(loc.loc_code)[:2]}&dtl_region={loc.loc_code}&format=json"
            data = requests.get(Url).json()
            num = int(data["response"]["numFound"])

            sort_index = []
            for lib in data["response"]["libs"]:
                lb = lib["lib"]

                sort_index.append(
                    calc_distance(user.longitude, user.latitude, lb["latitude"], lb["longitude"])
                )
            zipped_lists = zip(sort_index, data["response"]["libs"])
            sorted_zipped_lists = sorted(zipped_lists)
            sorted_libs = [d for _, d in sorted_zipped_lists]

            if num:
                data2["result"]["libs"] = sorted_libs
            else:
                data2["result"]["libs"] = "해당 책을 소장한 도서관이 없습니다"
    except:
        data2["result"]["error"] = "지역코드가 존재하지 않습니다."
   
    return JsonResponse(data2)

@csrf_exempt
def other_like_book(request):
    data2 = {}
    data2["result"] = []

    like_book_lists = []

    book_pk = request.GET.get("book_pk")
    user_pk = request.GET.get("user_pk")

    book = get_object_or_404(Book, pk=book_pk)
    current_user = get_object_or_404(User, pk=user_pk)
    
    users = book.like_users.all()

    for user in users:
        try: 
            like_books = user.like_books.all()
            if len(like_books):
                for like_book in like_books:
                    if like_book == book:
                        continue
                    if book.kdc_original == like_book.kdc_original:
                        like_book_lists.append(like_book.pk)
        except:
            continue
    
    if like_book_lists:
        counter = Counter(like_book_lists)
        most = counter.most_common()
        print(most)
        for pk,cnt in most:
            like_book = get_object_or_404(Book, pk=pk)
            like_book_serial = BookSerializer(like_book)
            data2["result"].append(like_book_serial.data)
    else:
        data2["result"].append("다른 사용자가 좋아요한 책이 존재하지 않습니다")

    return JsonResponse(data2)