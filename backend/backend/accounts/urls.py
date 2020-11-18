from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('oauth/', views.oauth, name='oauth'),
    path('kakao_login/', views.kakao_login, name='kakao_login'),
    path('oauth2/', views.oauth2, name='oauth2'),
    path('google_login/', views.google_login, name='google_login'),
    path('get_all_profile/', views.get_all_profile, name="get_all_profile"),
    path('check_email/', views.check_email, name="check_email"),
    path('unlink/', csrf_exempt(views.UnlinkView.as_view()), name='unlink'),
    path('profile/<int:user_pk>/', csrf_exempt(views.ProfileView.as_view()), name='profile'),
    path('profile/like/', csrf_exempt(views.LikeView.as_view()), name='profile_like'),
    path('profile/hate/', csrf_exempt(views.HateView.as_view()), name='profile_hate'),
    path('profile/like_review/', csrf_exempt(views.LikeReviewView.as_view()), name='profile_like_review'),
    path('profile/phrase/', csrf_exempt(views.PhraseView.as_view()), name='profile_phrase'),
    path('profile/review/', csrf_exempt(views.ReviewView.as_view()), name='profile_review'),
    path('profile/comment/', csrf_exempt(views.CommentView.as_view()), name='profile_comment'),
    path('profile/chart/', csrf_exempt(views.ChartView.as_view()), name='profile_chart'),
    path('privacy/<int:user_pk>/', csrf_exempt(views.PrivacyView.as_view()), name="privacy"),
    path('password/<int:user_pk>/', csrf_exempt(views.PasswordView.as_view()), name='password'),
    path('calendar/', csrf_exempt(views.CalendarView.as_view()), name='calendar'),
    path('choice/', views.choice, name='choice'),
    path('get_like_list/', views.get_like_list, name='get_like_list'),
    path('like/', views.like, name='like'),
    path('unlike/', views.unlike, name='unlike'),
    path('finish/', views.finish, name='finish'),
    path('get_finish_list/', views.get_finish_list, name='get_finish_list'),
    path('check_signup/', views.check_signup, name="check_signup"),
    path('address/', views.address, name="address"),
    path('address_delete/', views.address_delete, name="address_delete"),
    path('make_dummy/', views.make_dummy, name="make_dummy"),
    path('make_like/', views.make_like, name="make_like"),
]