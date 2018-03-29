from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as authlogin,logout as aulogout
from django.contrib.auth.decorators import login_required
from webapp.models import questions,answer,userextend
from django.http import Http404
from django.core.urlresolvers import reverse
from datetime import datetime
from webapp.forms import searchbox,Signup,Login,Ask,Answer,emailform,editanswer,editpasswordform,deleteaccount,aboutyou
from django.contrib.postgres.search import SearchVector
from django.utils.text import slugify
from math import ceil
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib import messages
import os
def homepage(request):
        aulogout(request)
        searchform=searchbox()    
        queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[0:10]
        hotlist=questions.objects.defer("body","ucode").order_by("-views")[0:10]
        return render(request,"index.html",{"list":queslist,"hotlist":hotlist,"search":searchform})   
def indexnav(request,choice):
     aulogout(request)
     searchform=searchbox()  
     hotlist=questions.objects.defer("body","ucode").order_by("-reply")[0:10]
     if choice=="new":
          page=request.GET.get("page")
          limit=questions.objects.count()          
          totalpages=int(ceil(limit/10.0))
          last=limit%10         
          try: 
               page=int(page)
               if page<=limit and page >= 0:
                  currentpage=(page/10)+1               
                  queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[page:page+10] 
                  npage=page+10;
                  ppage=page-10;
               else:
                  currentpage=totalpages
                  queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[limit-last:limit]                
                  npage=10; 
                  ppage=limit-last-10;                       
          except:
              currentpage=1
              queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[0:10]             
              npage=10;  
              ppage=-10;   
          return render(request,"indexqueslist.html",{"contacts":queslist,"search":searchform,"choice":"new","page":npage,"totalpages":
            totalpages,"current":currentpage,"previouspage":ppage,"hotlist":hotlist})
     elif choice=="top":
          page=request.GET.get("page")
          limit=questions.objects.count()          
          totalpages=int(ceil(limit/10.0))
          last=limit%10         
          try: 
               page=int(page)
               if page<=limit and page >= 0:
                  currentpage=(page/10)+1               
                  queslist=questions.objects.defer("body","ucode").order_by("-views")[page:page+10] 
                  npage=page+10;
                  ppage=page-10;
               else:
                  currentpage=totalpages
                  queslist=questions.objects.defer("body","ucode").order_by("-views")[limit-last:limit]                
                  npage=10; 
                  ppage=limit-last-10;                       
          except:
              currentpage=1
              queslist=questions.objects.defer("body","ucode").order_by("-views")[0:10]             
              npage=10;  
              ppage=-10;   
          return render(request,"indexqueslist.html",{"contacts":queslist,"search":searchform,"choice":"top","page":npage,"totalpages":
            totalpages,"current":currentpage,"previouspage":ppage,"hotlist":hotlist})        
     else:
         raise Http404      
def searchengine(request):
      hotlist=questions.objects.defer("body","ucode").order_by("-reply")[0:10]
      searchform=searchbox(request.GET)
      if searchform.is_valid():
          limit=questions.objects.annotate(search=SearchVector("body","header","ucode")).filter(search=searchform.cleaned_data["searchinfo"]).count()
          page=request.GET.get("page")
          totalpages=int(ceil(limit/10.0))
          last=limit%10         
          try: 
              page=int(page)
              if page<=limit and page >= 0:
                  currentpage=(page/10)+1               
                  searchlist=questions.objects.annotate(search=SearchVector("body","header","ucode")).filter(search=searchform.cleaned_data["searchinfo"])[page:page+10]
                  npage=page+10;
                  ppage=page-10;
              else:
                  currentpage=totalpages
                  searchlist=questions.objects.annotate(search=SearchVector("body","header","ucode")).filter(search=searchform.cleaned_data["searchinfo"])[limit-last:limit]                
                  npage=10; 
                  ppage=limit-last-10;           
          except: 
                currentpage=1
                searchlist=questions.objects.annotate(search=SearchVector("body","header","ucode")).filter(search=searchform.cleaned_data["searchinfo"])[0:10]             
                npage=10;  
                ppage=-10;    
          return render(request,"search.html",{"search":searchform,"list":hotlist,"contacts":searchlist,"username":request.user,"srch":searchform.cleaned_data["searchinfo"],"page":npage,"totalpages":
                totalpages,"current":currentpage,"previouspage":ppage})
      else:
        raise Http404    
def submitsignup(request,ques):
  aulogout(request)
  link=request.build_absolute_uri()         
  if request.method=="POST":
      form=Signup(request.POST)
      if form.is_valid(): 
          User.objects.create_user(username=form.cleaned_data["username"],email=form.cleaned_data["email"].lower(),password=form.cleaned_data["password"],first_name=form.cleaned_data["first_name"].title(),last_name=form.cleaned_data["last_name"].title())
          user=get_object_or_404(User,username=form.cleaned_data["username"])
          userextend.objects.create(euser=user)
          messages.success(request,"Profile Created please log in")
          return redirect(reverse("login" ,kwargs={"alink":ques}))      
      else:
          return render(request,"signup.html",{"ques":ques,"form":form,"link":link})
  else:
      form=Signup()
      return render(request,"signup.html",{"ques":ques,"form":form,"link":link})
def authuser(request,alink):
    aulogout(request)  
    if request.method=="POST":
       form=Login(request.POST)
       if form.is_valid():
         user=authenticate(username=form.cleaned_data["user_name"],password=form.cleaned_data["login_password"])
         if (user is not None) and user.is_active:
           authlogin(request,user)
           if alink=="new":
               return redirect(reverse("usernav",kwargs={"choice":"first"}))
           else:
             ques=int(alink)
             q=get_object_or_404(questions,pk=ques)
             answerform=Answer()
             return render(request,"answerform.html",{"question":q,"username":request.user,"form":answerform})
         else:
             form=Login()
             return render(request,"login.html",{"form":form,"alink":alink,"message":"invalid username or password"})
       else:
           return render(request,"login.html",{"form":form,"alink":alink})
    else:
       form=Login()
       return render(request,"login.html",{"form":form,"alink":alink})
@login_required()
def authlogout(request):
  aulogout(request)
  return redirect(reverse("indexnav",kwargs={"choice":"new"}))    
@login_required()
def postques(request): 
    searchform=searchbox()
    if request.method=="POST":
        form=Ask(request.POST)
        if form.is_valid():
                   sluged=slugify(form.cleaned_data["user_question"])
                   currentq=questions(header=form.cleaned_data["user_question"].capitalize(),ucode=form.cleaned_data["question_code"],body=form.cleaned_data["question_body"],user=request.user,dateqtime=datetime.now(),slug=sluged)
                   currentq.save()
                   return redirect(reverse("seeques",kwargs={"useeques":currentq.id,"slugtext":sluged}))
        else:
            return render(request,"useraskques.html",{"search":searchform,"username":request.user,"form":form})
    else:
        form=Ask()
        return render(request,"useraskques.html",{"search":searchform,"username":request.user,"form":form})
@login_required()
def userhomenav(request,choice):
     searchform=searchbox()
     if choice=="new":
       hotlist=questions.objects.defer("body","ucode").order_by("-reply")[0:10]
       queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")   
       page=request.GET.get("page")
       limit=questions.objects.count()          
       totalpages=int(ceil(limit/10.0))
       last=limit%10         
       try: 
             page=int(page)
             if page<=limit and page >= 0:
                currentpage=(page/10)+1               
                queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[page:page+10] 
                npage=page+10;
                ppage=page-10;
             else:
                currentpage=totalpages
                queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[limit-last:limit]                
                npage=10; 
                ppage=limit-last-10;                       
       except:
            currentpage=1
            queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[0:10]             
            npage=10;  
            ppage=-10;        
       return render(request,"userqueslist.html",{"contacts":queslist,"search":searchform,"username":request.user,"choice":"new","page":npage,"totalpages":
          totalpages,"current":currentpage,"previouspage":ppage,"hotlist":hotlist})       
     elif choice =="top":
       hotlist=questions.objects.defer("body","ucode").order_by("-reply")[0:10]
       queslist=questions.objects.defer("body","ucode").order_by("-views")
       page=request.GET.get("page")      
       limit=questions.objects.count()          
       totalpages=int(ceil(limit/10.0))
       last=limit%10         
       try: 
               page=int(page)
               if page<=limit and page >= 0:
                  currentpage=(page/10)+1               
                  queslist=questions.objects.defer("body","ucode").order_by("-views")[page:page+10] 
                  npage=page+10;
                  ppage=page-10;
               else:
                  currentpage=totalpages
                  queslist=questions.objects.defer("body","ucode").order_by("-views")[limit-last:limit]                
                  npage=10; 
                  ppage=limit-last-10;                       
       except:
              currentpage=1
              queslist=questions.objects.defer("body","ucode").order_by("-views")[0:10]             
              npage=10;  
              ppage=-10;   
       return render(request,"userqueslist.html",{"contacts":queslist,"search":searchform,"choice":"top","username":request.user,"page":npage,"totalpages":
            totalpages,"current":currentpage,"previouspage":ppage,"hotlist":hotlist})
     elif choice=="first":   
        queslist=questions.objects.defer("body","ucode").order_by("-dateqtime")[0:10]
        hotlist=questions.objects.defer("body","ucode").order_by("-views")[0:10]
        return render(request,"userhome.html",{"contacts":queslist,"search":searchform,"hotlist":hotlist,"first":1,"username":request.user})  
     else:
         raise Http404
def seeques(request,useeques,slugtext):
  searchform=searchbox()  
  if request.user.is_authenticated():
    ques=get_object_or_404(questions,pk=useeques)
    ques.views=ques.views+1;
    ques.save()
    ans=ques.answer_set.all()
    link=request.build_absolute_uri()
    return render(request,"userques.html",{"search":searchform,"headers":ques,"list":ans,"username":request.user,"link":link}) 
  else:
    ques=get_object_or_404(questions,pk=useeques)
    ques.views=ques.views+1;
    ques.save()
    ans=ques.answer_set.all()
    link=request.build_absolute_uri()
    return  render(request,"ques.html",{"search":searchform,"headers":ques,"list":ans,"link":link})

@login_required()
def  answersub(request,uanswersub):
    searchform=searchbox()
    ques=get_object_or_404(questions,pk=uanswersub)
    if request.method=="POST":
      form=Answer(request.POST)  
      if form.is_valid():  
        answer.objects.create(question=ques,userans=request.user,answer=form.cleaned_data["answer"],acode=form.cleaned_data["answer_code"],datentime=datetime.now() )  
        ques.reply=ques.reply+1
        ques.save()
        return redirect(reverse("seeques",kwargs={"useeques":ques.id,"slugtext":ques.slug}))
      else:
        return  render(request,"answerform.html",{"search":searchform,"question":ques,"username":request.user,"form":form})  
    else :
        form=Answer()
        return  render(request,"answerform.html",{"search":searchform,"question":ques,"username":request.user,"form":form})  

def pyforumall(request,goto):
    return render(request,"all.html",{"goto":goto})

@login_required()
def userpage(request,userprofile):
  person=get_object_or_404(User,username=request.user.username)
  add=get_object_or_404(userextend,euser=person)
  tques=person.questions_set.all().count()
  tans=person.answer_set.all().count()
  return render(request,"userprofile.html",{"name":add,"username":person,"count_ques":tques,"count_ans":tans})
@login_required()
def aboutyoutext(request):
  person=get_object_or_404(User,username=request.user.username)
  addperson=get_object_or_404(userextend,euser=person)
  if request.POST:
    form=aboutyou(request.POST)
    if form.is_valid():
        addperson.description=form.cleaned_data["more"]
        addperson.save()
        return redirect(reverse("userpage",kwargs={"userprofile":request.user.username}))
    else:
       return render(request,"addnewinfo.html",{"more":form,"username":request.user}) 
  else:
    form=aboutyou(initial={"more":addperson.description})
    return render(request,"addnewinfo.html",{"more":form,"username":request.user})  
@login_required()
def userquestions(request):
  person=get_object_or_404(User,username=request.user.username)
  uques=person.questions_set.all().defer("body","ucode").order_by("-dateqtime")
  return render(request,"userquestionsall.html",{"question":uques,"username":request.user})
@login_required()
def editques(request,eques):
  ques=get_object_or_404(questions,pk=eques)
  if (ques.user.id==request.user.id):
     if request.POST:
        form=Ask(request.POST)
        if form.is_valid():
            ques.header=form.cleaned_data["user_question"]
            ques.body=form.cleaned_data["question_body"]
            ques.ucode=form.cleaned_data["question_code"]
            ques.dateqtime=datetime.now()
            ques.updated=True
            ques.save()
            messages.success(request,"Your Question is Updated")
            return redirect(reverse("userquestions"))
        else:
          return render(request,"editquesform.html",{"form":form,"questions":ques,"username":request.user})
     else:
        form=Ask(initial={"user_question":ques.header,"question_body":ques.body,"question_code":ques.ucode})
        return render(request,"editquesform.html",{"form":form,"questions":ques,"username":request.user})
  else:
    raise Http404
@login_required()
def deleteques(request,eques):
  ques=get_object_or_404(questions,pk=eques)
  if (ques.user.id==request.user.id):
     ques.delete() 
     messages.success(request,"Question Deleted")
     return redirect(reverse("userquestions"))
  else:
    raise Http404
@login_required()
def useranswers(request):
  person=get_object_or_404(User,username=request.user.username)
  uans=person.answer_set.all().defer("answer","acode").order_by("-datentime")
  return render(request,"useranswersall.html",{"answer":uans,"username":request.user})
@login_required()
def deleteans(request,eans):
  ans=get_object_or_404(answer,pk=eans)
  if (ans.userans.id==request.user.id):
     ans.question.reply-=1
     ans.question.save()
     ans.delete()
     messages.success(request,"answer deleted") 
     return redirect(reverse("useranswers"))
  else:
    raise Http404 
@login_required()
def editans(request,eans):
  ans=get_object_or_404(answer,pk=eans)
  if (ans.userans.id==request.user.id):
     if request.POST:
        form=editanswer(request.POST)
        if form.is_valid():
            ans.answer=form.cleaned_data["abody"]
            ans.acode=form.cleaned_data["acode"]
            ans.datentime=datetime.now()
            ans.save()
            messages.success(request,"answer edited")
            return redirect(reverse("useranswers"))
        else:
          return render(request,"editanswerform.html",{"form":form,"ans":ans,"username":request.user})
     else:
        form=editanswer(initial={"abody":ans.answer,"acode":ans.acode})
        return render(request,"editanswerform.html",{"form":form,"answer":ans,"username":request.user})
  else:
    raise Http404
@login_required()
def deleteprofile(request):
    person=get_object_or_404(User,username=request.user.username) 
    if request.method=="POST":
       form=deleteaccount(request.POST)
       if form.is_valid():
           if request.user.check_password(form.cleaned_data["user_password"]):
                  person.delete()
                  return redirect(reverse("indexnav",kwargs={"choice":"new"}))                            
           else:
               return render(request,"deleteform.html",{"error":"incorrect old password","person":person,"form":form})
       else:
         return render(request,"deleteform.html",{"username":person,"form":form})
    else:
      form=deleteaccount()
      return render(request,"deleteform.html",{"form":form,"username":person})
def userinfo(request,userid,username):
   user=get_object_or_404(User,pk=userid)
   person=get_object_or_404(userextend,euser=user)
   tques=user.questions_set.all()
   tans=user.answer_set.all()      
   return render(request,"userinfo.html",{"person":person,"user_ques":tques,"user_ans":tans,"username":request.user})
@login_required()
def changeemail(request):
  person=get_object_or_404(User,username=request.user.username)  
  if request.method=="POST":
      form=emailform(request.POST)
      if form.is_valid():
            request.user.email=form.cleaned_data["user_mail"].lower()
            request.user.save()
            messages.success(request,"Email id changed")
            return redirect(reverse("userpage",kwargs={"userprofile":request.user.username}))                             
      else:
        return render(request,"emailchange.html",{"eform":form,"username":request.user})      
  else:
    form=emailform(initial={"user_mail":person.email})
    return render(request,"emailchange.html",{"eform":form,"username":request.user})
@login_required()
def changepassword(request):
  if request.method=="POST":
      form=editpasswordform(request.POST) 
      if form.is_valid():      
           if request.user.check_password(form.cleaned_data["edit_cpassword"]):
                  request.user.set_password(form.cleaned_data["edit_npassword"])
                  request.user.save()                         
                  messages.success(request,"password changed please log in")
                  return redirect(reverse("login",kwargs={"alink":"new"}))                             
           else:
               return render(request,"changepassword.html",{"form":form,"username":request.user,"error":"invalid old password"})               
      else:
         return render(request,"changepassword.html",{"form":form,"username":request.user})             
  else:
    form=editpasswordform() 
    return render(request,"changepassword.html",{"form":form,"username":request.user}) 
@login_required()
def picupload(request):
  return render(request,"substitutepicupload.html",{})
