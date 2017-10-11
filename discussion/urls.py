from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^recent/$', views.recent, name='recent'),
    url(r'^answered/$', views.answered, name='answered'),
    url(r'^unanswered/$', views.unanswered, name='unanswered'),
    url(r'^upvoteQues/$', views.VoteUpQues, name='upvoteQues'),
    url(r'^quesVotes/$', views.quesVotes, name='quesVotes'),
    url(r'^upvoteAns/$', views.VoteUpAns, name='upvoteAns'),
    url(r'^downvoteQues/$', views.VoteDownQues, name='downvoteQues'),
    url(r'^downvoteAns/$', views.VoteDownAns, name='downvoteAns'),
    url(r'^starQues/$', views.addStar, name='addStar'),
    url(r'^checkAns/(?P<ans>\d+)/(?P<ques>\d+)/$', views.checkAns, name='checkAns'),
    url(r'^question/details/(?P<ques>\d+)/$', views.details, name='details'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^comment/(?P<ques>\d+)/$', views.comment, name='comment'),
    url(r'^answer/(?P<ques>\d+)/$', views.answer, name='answer'),
    url(r'^answer/accept/$', views.accept, name='accept'),
    url(r'^answer/vote/$', views.vote, name='vote'),
    url(r'^my_account/(?P<user_id>\d+)/$', views.myAccount, name="my_account"),
    url(r'^my_account/(?P<user_id>\d+)/set_image/$', views.set_image, name="set_image"),
    url(r'^my_account/(?P<user_id>\d+)/update/$', views.update, name="update"),
    url(r'^my_account/(?P<user_id>\d+)/change_pass/$', views.change_pass, name="change_pass"),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
]