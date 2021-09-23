from django.urls import path
from .views import authentication, main, chatroom, transactions

urlpatterns = [
    path('', main.index, name="base"),
    path('login/', authentication.login, name="login"),
    path('chatroom/', chatroom.chatroom, name="chatroom"),
    path('transfermoney/', main.transfermoney, name="transfermoney"),
    path('login/account_no', main.account_no, name="account_no"),
    path('login/video', main.video, name="video"),
    path('profile/', main.profile, name="profile"),
    path('loan/', main.loan, name="loan"),
    path('profile/transactions/', transactions.get_transactions, name="profile-transactions"),

    ## Endpts
    path('getuser/', main.get_user, name="getuser"),
]
