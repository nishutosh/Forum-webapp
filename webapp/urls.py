from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from webapp.views import userpage,answersub,seeques,submitsignup,authuser,\
authlogout,postques,deleteprofile,editques,userhomenav,indexnav,searchengine,\
deleteques,pyforumall,homepage,editans,deleteans,userinfo,\
picupload,aboutyoutext,changeemail,changepassword,userquestions,useranswers,picupload
urlpatterns=[
  url(r'^admin/', include(admin.site.urls)),
  url(r'^$',homepage,name="homepage"),
  url(r'^index/(?P<choice>\w+)$',indexnav,name="indexnav"),
  url(r'^search$',searchengine,name="search"),
  url(r'^signup/(?P<ques>\w+)$',submitsignup,name="signup"),
  url(r'^login/(?P<alink>\w+)$',authuser,name="login"),
  url(r'^logout$',authlogout,name="logout"),  
  url(r'^userhome/(?P<choice>\w+)$',userhomenav,name="usernav"),
  url(r'^askquestion$',postques,name="askquestion"),
  url(r'^question/48(?P<useeques>\d+)563/(?P<slugtext>[\w-]+)$',seeques,name="seeques"),
  url(r'^answered/(?P<uanswersub>\d+)$',answersub,name="postanswer"),
  url(r'^profiles/(?P<userprofile>\w+)$',userpage,name="userpage"),
  url(r'^profile/delete$',deleteprofile,name="deleteprofile"),
  url(r'^profile/userquestions$',userquestions,name="userquestions"),
  url(r'^profile/useranswers$',useranswers,name="useranswers"),
  url(r'^profile/editques/(?P<eques>\d+)$',editques,name="editques"),
  url(r'^profile/deleteques/(?P<eques>\d+)$',deleteques,name="deleteques"),
  url(r'^profile/editans/(?P<eans>\d+)$',editans,name="editans"),
  url(r'^profile/deleteans/(?P<eans>\d+)$',deleteans,name="deleteans"),
  url(r'^profile/user/(?P<userid>\d+)/(?P<username>\w+)$',userinfo,name="user"),
  url(r'^profile/user/uploadpic$',picupload,name="picupload"),
  url(r'^profile/user/aboutyou$',aboutyoutext,name="aboutyoutext") ,
  url(r'^profile/user/changeemailid$',changeemail,name="changeemail"),
  url(r'^profile/user/changepassword$',changepassword,name="changepassword"),
  url(r'^profile/user/changeprofilepic$',picupload,name="picupload"),
  url(r'^allaboutus/(?P<goto>\w+)$',pyforumall,name="all"),
 ] 

