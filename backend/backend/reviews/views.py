from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse

from accounts.utils import permission

import requests
import json
import math

from books.models import Book
from .models import Review, Phrase, ReviewComment, ReviewLike
from .serializers import ReviewSerializer, PhraseSerializer, ReviewCommentSerializer
from books.serializers import BookSerializer
from accounts.models import User, UserPrivacy
from accounts.serializers import UserSerializer

# Create your views here.
from accounts.avatars import avatars

class ReviewView(View):
    # create
    @permission
    def put(self, request):
        # print('review create start')
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        # print(data)
        book = get_object_or_404(Book, pk=book_pk)
        user = request.user
        user_serial = UserSerializer(user)
        # print(book)
        data['book'] = book_pk
        data['user'] = user.pk
        if Review.objects.filter(Q(user=user)&Q(book=book_pk)):
            # print("빈게아니야")
            data2 = {}
            data2['result'] = "책 마다 하나의 리뷰만 작성 가능"
            return JsonResponse(data2)

        # data['user'] = user_serial.data
        serializer = ReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data
        #     print(serializer.data)
        #     reviews = Review.objects.filter(book=book)
        #     reviews_serial = ReviewSerializer(reviews, many=True)
            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 reviews
    @permission
    def get(self, request):
        book_pk = int(request.GET.get("book_pk"))
        book = get_object_or_404(Book, pk=book_pk)
        reviews = Review.objects.filter(book=book)
        current_user = request.user
        data2 = {}
        data2['result'] = []
        data2['score'] = []
        if Review.objects.filter(Q(user=current_user)&Q(book=book_pk)):
            data2["status"] = "리뷰가 있어"
        else:
            data2["status"] = "리뷰가 없어"

        total_design_score = 0
        total_content_score = 0

        ### review like 넣기 , 현 좋아요 상태
        for i in range(len(reviews)):
            try:
                review = get_object_or_404(Review, pk=reviews[i].pk)
                author = get_object_or_404(User, pk=review.user.pk)
                author_profile = get_object_or_404(UserPrivacy, user=author)
                profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                total_design_score += review.design_score
                total_content_score += review.content_score

                review_serial = ReviewSerializer(review)
                user_serial = UserSerializer(author)
                
                ### review like 넣기 , 현 좋아요 상태
                review_likes = ReviewLike.objects.filter(review=review)
                count = len(review_likes)
                try:
                    review_like = get_object_or_404(ReviewLike, review=review, user = current_user)
                    review_like_state = True
                except:
                    review_like_state = False

                review_like = {}
                
                review_like["review_like_count"] = count
                review_like["review_like_state"] = review_like_state

                data2['result'].append({'review': review_serial.data, 
                                        'user': user_serial.data,
                                        'profile_url': profile_url,
                                        'review_like': review_like
                                        })
            except:
                data2['result'].append({'error': "등록된 리뷰 정보가 없습니다."})

        else:
            if len(reviews):
                data2["score"].append({
                    "design_score_average": math.ceil(total_design_score/len(reviews)),
                    "content_score_average": math.ceil(total_content_score/len(reviews)),
                })
            else:
                data2["score"].append({
                    "design_score_average": 0,
                    "content_score_average": 0,
                })

        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        review_pk = data['review_pk']
        review = get_object_or_404(Review, pk=review_pk)
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = ReviewSerializer(review, data=data)
        ### review like 넣기 , 현 좋아요 상태 - 보류
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        review_pk = request.GET.get("review_pk")
        review = get_object_or_404(Review, pk=review_pk)
        review.delete()
        data2 = {}
        data2["result"] = "success"
        return JsonResponse(data2)


class PhraseView(View):
    # create
    @permission
    def put(self, request):
        print('phrase create start')
        data = json.loads(request.body.decode('utf-8'))
        book_pk = data['book_pk']
        user = request.user
        data['book'] = book_pk
        data['user'] = user.pk
        serializer = PhraseSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data2 = {}
            data2['result'] = serializer.data

            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 phrases
    @permission
    def get(self, request):
        book_pk = int(request.GET.get("book_pk"))
        book = get_object_or_404(Book, pk=book_pk)
        try:
            phrases = Phrase.objects.filter(book=book)
            phrases_serial = PhraseSerializer(phrases, many=True)
            data2 = {}
            temp_data = phrases_serial.data
            for pick in temp_data:
                user = get_object_or_404(User, pk=pick["user"])
                pick["username"] = user.name
            data2['result'] = temp_data
        except:
            data2['result'] = "phrase 정보가 없습니다."

        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        phrase_pk = data['phrase_pk']
        phrase = get_object_or_404(Phrase, pk=phrase_pk)
        user = request.user
        data['book'] = phrase.book.pk
        data['user'] = user.pk
        phrase_serializer = PhraseSerializer(phrase, data=data)
        if phrase_serializer.is_valid(raise_exception=True):
            phrase_serializer.save()
            data2 = {}
            data2['result'] = phrase_serializer.data
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        phrase_pk = request.GET.get("phrase_pk")
        try:
            phrase = get_object_or_404(Phrase, pk=phrase_pk)
            phrase.delete()
            data2 = {}
            data2["result"] = "success"
        except:
            data2['result'] = "phrase 정보가 없습니다."

        return JsonResponse(data2)


class CommunityView(View):
    # 해당 book 의 reviews
    @permission
    def get(self, request):
        #     book_pk = int(request.GET.get("book_pk"))
        #     book = get_object_or_404(Book)
        #     reviews = Review.objects.filter(book=book)
        #     reviews_serial = ReviewSerializer(reviews, many=True)
        #     # print(reviews_serial.data)
        #     data2 = {}
        #     data2['result'] = reviews_serial.data
        #     return JsonResponse(data2)
        # def book_search(request):
        
        # user_pk, search_word, search_type
        try:
            user_pk = request.GET.get("user_pk")
            current_user = get_object_or_404(User, pk=user_pk)
        except:
            data2 = {
                "result" : "user_pk 가 없습니다."
            }
            return JsonResponse(data2)
        try:
            search_word = request.GET.get("search_word")
            search_type = request.GET.get("search_type")
        except:
            search_word = ""
            search_type = ""
        data2 = {}

        if search_word:
            # search_type
            # 제목(0), 유저(1), 책(2)
            if int(search_type) == 0:
                print("search_type 0")
                try:
                    reviews = Review.objects.filter(title__icontains=search_word)
                    if len(reviews):
                        reviews_serial = ReviewSerializer(reviews, many=True)
                        reviews_list = reviews_serial.data
                
                        for review in reviews_list:
                            book = get_object_or_404(Book, pk=review["book"])
                            book_serial = BookSerializer(book)

                            user = get_object_or_404(User, pk=review["user"])
                            user_serial = UserSerializer(user)

                            author_profile = get_object_or_404(UserPrivacy, user=user)
                            profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                            
                            ### review like 넣기 , 현 좋아요 상태
                            review_pk = review["id"]
                            review_likes = ReviewLike.objects.filter(pk=review_pk)
                            review_for_like = get_object_or_404(Review, pk=review_pk)
                            count = len(review_likes)
                            try:
                                review_like = get_object_or_404(ReviewLike, review=review_for_like, user = current_user)
                                review_like_state = True
                            except:
                                review_like_state = False

                            review["book_title"] = book_serial.data["title"]
                            review["book_img_url"] = book_serial.data["img_url"]
                            review["user_email"] = user_serial.data["email"]
                            review["user_name"] = user_serial.data["name"]
                            review['profile_url'] = profile_url
                            review["review_like_count"] = count
                            review["review_like_state"] = review_like_state

                            print(review)

                        data2['result'] = reviews_list
                        
                    else:
                        data2['result'] = "검색 결과가 없습니다."
                except:
                    print("except 진입")
                    data2['error'] = "검색 결과가 없습니다."

                    
            elif int(search_type) == 1:
                print("search_type 1")
                data2['result'] = []
                try:
                    users = User.objects.filter(name__icontains=search_word)
                    for user in users:
                        user_serial = UserSerializer(user)
                        
                        author_profile = get_object_or_404(UserPrivacy, user=user)
                        profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                        
                        reviews = Review.objects.filter(user=user)
                        if len(reviews):
                            reviews_serial = ReviewSerializer(reviews, many=True)
                            reviews_list = reviews_serial.data

                            for review in reviews_list:

                                book = get_object_or_404(Book, pk=review["book"])

                                book_serial = BookSerializer(book)
                            
                                ### review like 넣기 , 현 좋아요 상태
                                review_pk = review["id"]
                                review_for_like = get_object_or_404(Review, pk=review_pk)
                                review_likes = ReviewLike.objects.filter(review=review_for_like)
                                count = len(review_likes)
                                try:
                                    review_like = get_object_or_404(ReviewLike, review=review_for_like, user = current_user)
                                    review_like_state = True
                                except:
                                    review_like_state = False

                                review["review_like_count"] = count
                                review["review_like_state"] = review_like_state
                                review["book_title"] = book_serial.data["title"]
                                review["book_img_url"] = book_serial.data["img_url"]
                                review["user_email"] = user_serial.data["email"]
                                review["user_name"] = user_serial.data["name"]
                                review['profile_url'] = profile_url

                                data2['result'].append(review)

                except:
                    data2['error'] = "검색 결과가 없습니다."
            elif int(search_type) == 2:
                print("search_type 2")
                data2['result'] = []
                try:
                    books = Book.objects.filter(title__icontains=search_word)
                    for book in books:
                        book_serial = BookSerializer(book)
                        reviews = Review.objects.filter(book=book)
                        if len(reviews):
                            reviews_serial = ReviewSerializer(reviews, many=True)
                            reviews_list = reviews_serial.data

                            for review in reviews_list:

                                user = get_object_or_404(User, pk=review["user"])

                                user_serial = UserSerializer(user)

                                author_profile = get_object_or_404(UserPrivacy, user=user)
                                profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                                ### review like 넣기 , 현 좋아요 상태
                                review_pk = review["id"]
                                review_for_like = get_object_or_404(Review, pk=review_pk)
                                review_likes = ReviewLike.objects.filter(review=review_for_like)
                                count = len(review_likes)
                                try:
                                    review_like = get_object_or_404(ReviewLike, review=review_for_like, user = current_user)
                                    review_like_state = True
                                except:
                                    review_like_state = False

                                review["review_like_count"] = count
                                review["review_like_state"] = review_like_state
                                review["book_title"] = book_serial.data["title"]
                                review["book_img_url"] = book_serial.data["img_url"]
                                review["user_email"] = user_serial.data["email"]
                                review["user_name"] = user_serial.data["name"]
                                review['profile_url'] = profile_url
                                data2['result'].append(review)

                except:
                    data2['error'] = "검색 결과가 없습니다."
            elif int(search_type) == 3:
                print("search_type 3")
                try:
                    reviews = Review.objects.filter(content__icontains=search_word)
                    if len(reviews):
                        reviews_serial = ReviewSerializer(reviews, many=True)
                        reviews_list = reviews_serial.data
                
                        for review in reviews_list:
                            print("for 진입")
                            book = get_object_or_404(Book, pk=review["book"])
                            book_serial = BookSerializer(book)

                            user = get_object_or_404(User, pk=review["user"])
                            user_serial = UserSerializer(user)

                            author_profile = get_object_or_404(UserPrivacy, user=user)
                            profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                            
                            ### review like 넣기 , 현 좋아요 상태
                            review_pk = review["id"]
                            review_for_like = get_object_or_404(Review, pk=review_pk)
                            review_likes = ReviewLike.objects.filter(review=review_for_like)
                            count = len(review_likes)
                            try:
                                review_like = get_object_or_404(ReviewLike, review=review_for_like, user = current_user)
                                review_like_state = True
                            except:
                                review_like_state = False

                            review["book_title"] = book_serial.data["title"]
                            review["book_img_url"] = book_serial.data["img_url"]
                            review["user_email"] = user_serial.data["email"]
                            review["user_name"] = user_serial.data["name"]
                            review['profile_url'] = profile_url

                            review["review_like_count"] = count
                            review["review_like_state"] = review_like_state

                            print(review)

                        data2['result'] = reviews_list
                        
                    else:
                        data2['result'] = "검색 결과가 없습니다."
                except:
                    print("except 진입")
                    data2['error'] = "검색 결과가 없습니다."

            return JsonResponse(data2)
        else:
            print("search all")
            reviews = Review.objects.all()
            reviews_serial = ReviewSerializer(reviews, many=True)
            reviews_list = reviews_serial.data
            
            for review in reviews_list:
                book = get_object_or_404(Book, pk=review["book"])
                book_serial = BookSerializer(book)

                user = get_object_or_404(User, pk=review["user"])
                user_serial = UserSerializer(user)
                
                author_profile = get_object_or_404(UserPrivacy, user=user)
                profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"

                ### review like 넣기 , 현 좋아요 상태
                review_pk = review["id"]
                review_for_like = get_object_or_404(Review, pk=review_pk)
                review_likes = ReviewLike.objects.filter(review=review_for_like)
                count = len(review_likes)
                try:
                    review_like = get_object_or_404(ReviewLike, review=review_for_like, user = current_user)
                    review_like_state = True
                except:
                    review_like_state = False

                review["review_like_count"] = count
                review["review_like_state"] = review_like_state
                review["book_title"] = book_serial.data["title"]
                review["book_img_url"] = book_serial.data["img_url"]
                review["user_email"] = user_serial.data["email"]
                review["user_name"] = user_serial.data["name"]
                review['profile_url'] = profile_url

            data2['result'] = reviews_list
        return JsonResponse(data2)


class CommentView(View):
    # create
    @permission
    def put(self, request):
        print('comment create start')
        # content = [내용]
        # review = [review_pk]
        data = json.loads(request.body.decode('utf-8'))
        review_pk = data["review_pk"]
        user = request.user
        data['user'] = user.pk
        data['review'] = review_pk

        serializer = ReviewCommentSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            comments = ReviewComment.objects.filter(review=review_pk)
            comments_serial = ReviewCommentSerializer(comments, many=True)
            comments_list = comments_serial.data
            for comment in comments_list:
                user = get_object_or_404(User, pk=comment["user"])
                user_serial = UserSerializer(user)
                
                author_profile = get_object_or_404(UserPrivacy, user=user)
                profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                
                comment["user_email"] = user_serial.data["email"]
                comment["user_name"] = user_serial.data["name"]
                comment['profile_url'] = profile_url
                comment["edit"] = False

            data2 = {}
            data2['result'] = comments_list
            return JsonResponse(data2)

        return JsonResponse(data)

    # 해당 book 의 reviews
    @permission
    def get(self, request):
        # params: { review_pk : review_pk }
        review_pk = request.GET.get("review_pk")
        comments = ReviewComment.objects.filter(review=review_pk)
        comments_serial = ReviewCommentSerializer(comments, many=True)
        comments_list = comments_serial.data
        for comment in comments_list:
            user = get_object_or_404(User, pk=comment["user"])
            user_serial = UserSerializer(user)
            author_profile = get_object_or_404(UserPrivacy, user=user)
            profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
            
            comment["user_email"] = user_serial.data["email"]
            comment["user_name"] = user_serial.data["name"]
            comment['profile_url'] = profile_url
            comment["edit"] = False

        data2 = {}
        data2['result'] = comments_list
        return JsonResponse(data2)

    # update
    @permission
    def post(self, request):
        # comment_pk = [comment_pk]
        # content = [내용]
        # review = [review_pk]
        data = json.loads(request.body.decode('utf-8'))
        comment_pk = data["comment_pk"]
        review_pk = data["review_pk"]

        comment = get_object_or_404(ReviewComment, pk=comment_pk)
        user = request.user
        temp_data = {"content": data["content"], "review": review_pk, "user": user.pk}

        serializer = ReviewCommentSerializer(comment, data=temp_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            comments = ReviewComment.objects.filter(review=review_pk)
            comments_serial = ReviewCommentSerializer(comments, many=True)
            comments_list = comments_serial.data
            for comment in comments_list:
                user = get_object_or_404(User, pk=comment["user"])
                user_serial = UserSerializer(user)

                author_profile = get_object_or_404(UserPrivacy, user=user)
                profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                
                comment["user_email"] = user_serial.data["email"]
                comment["user_name"] = user_serial.data["name"]
                comment['profile_url'] = profile_url
                comment["edit"] = False

            data2 = {}
            data2['result'] = comments_list
            return JsonResponse(data2)

        data['result'] = "fail"

        return JsonResponse(data)

    @permission
    def delete(self, request):
        # comment_pk = [comment_pk]
        comment_pk = request.GET.get("comment_pk")
        review_pk = request.GET.get("review_pk")
        data2 = {}
        try:
            comment = get_object_or_404(ReviewComment, pk=comment_pk)
            review = get_object_or_404(Review, pk=review_pk)
            comment.delete()
            comments = ReviewComment.objects.filter(review=review)
            if len(comments):
                comments_serial = ReviewCommentSerializer(comments, many=True)
                comments_list = comments_serial.data
                for comment in comments_list:
                    user = get_object_or_404(User, pk=comment["user"])
                    user_serial = UserSerializer(user)
                    author_profile = get_object_or_404(UserPrivacy, user=user)
                    profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
                    
                    comment["user_email"] = user_serial.data["email"]
                    comment["user_name"] = user_serial.data["name"]
                    comment['profile_url'] = profile_url
                    comment["edit"] = False
                    
                data2['result'] = comments_list
            else:
                data2['result'] = "해당 review 의 comments 가 없습니다"
        except:
            data2["result"] = "오류가 생겼습니다"

        return JsonResponse(data2)

@csrf_exempt
def review_detail(request):
    review_pk = request.GET.get("review_pk")
    
    user_pk = request.GET.get("user_pk")
    user = get_object_or_404(get_user_model(), pk=user_pk)
    
    review = get_object_or_404(Review, pk=review_pk)
    review.update_counter
    review_serial = ReviewSerializer(review)

    review_user = get_object_or_404(get_user_model(), pk=review.user.pk)
    author_profile = get_object_or_404(UserPrivacy, user=review_user)
    profile_url = f"https://joeschmoe.io/api/v1/{avatars[author_profile.name]}"
    
    book = get_object_or_404(Book, pk=review.book.pk)
    
    ### review like 넣기 , 현 좋아요 상태
    review_likes = ReviewLike.objects.filter(review=review)
    count = len(review_likes)
    try:
        review_like = get_object_or_404(ReviewLike, review=review, user = user)
        review_like_state = True
    except:
        review_like_state = False

    data2 = {}
    data2['result'] = review_serial.data
    data2['result']["review_like_count"] = count
    data2['result']["review_like_state"] = review_like_state
    data2['result']['review_user_pk'] = review_user.pk
    data2['result']['review_user_name'] = review_user.name
    data2['result']['profile_url'] = profile_url

    data2['result']['book_title'] = book.title
    data2['result']['book_img_url'] = book.img_url

    print(data2)
    return JsonResponse(data2)


@csrf_exempt
def like_review(request):
    review_pk = int(request.GET.get("review_pk"))
    user_pk = int(request.GET.get("user_pk"))
    user = get_object_or_404(get_user_model(), pk=user_pk)
    review = get_object_or_404(Review, pk=review_pk)

    try:
        review_like = get_object_or_404(ReviewLike, review=review, user = user)
        print("삭제전",review_like)
        review_like.delete()
        review_likes = ReviewLike.objects.filter(review=review)
        print("삭제후",review_likes)
        count = len(review_likes)
        ## like 취소
        liked = False
    except:
        ## 새로운 review like 만들기
        review_like = ReviewLike(user=user, review=review)
        review_like.save()
        review_likes = ReviewLike.objects.filter(review=review)
        print("save후",review_like)
        count = len(review_likes)
        liked = True

    data2 = {
        "review_pk": review.pk,
        "review_like_state" : liked,
        "review_like_count" : count
    }

    return JsonResponse(data2)