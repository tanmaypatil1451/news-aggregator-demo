from django.shortcuts import redirect, render
from django.template import context
import requests
from bs4 import BeautifulSoup
from django.forms import inlineformset_factory
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
#Times of india headlines scraping code
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[2:10] # removing footer links
toi_news = []
for th in toi_headings:
    toi_news.append(th.text)

#Times of india sports news scraping code
toi_sports_r = requests.get("https://timesofindia.indiatimes.com/briefs/sports")
toi_sports_soup = BeautifulSoup(toi_sports_r.content, 'html5lib')

toi_sports_headings = toi_soup.find_all("p")


toi_sports_headings = toi_sports_headings[10:] # removing footer links
toi_sports_news = []
for th in toi_sports_headings:
    toi_sports_news.append(th.text)
print(toi_sports_headings)

#Times of india tech news scraping code
toi_tech_r = requests.get("https://www.gadgetsnow.com/latest-news")
toi_tech_soup = BeautifulSoup(toi_tech_r.content, 'html5lib')
toi_tech_headings = toi_tech_soup.find_all("span", {"class":"w_tle"})
toi_tech_headings = toi_tech_headings[10:18] # removing footer links
toi_tech_news = []
for th in toi_tech_headings :
    toi_tech_news.append(th.text)
print(len(toi_tech_news))

#NDTV Headlines scraping code
ht_r = requests.get("https://www.ndtv.com/india")
ht_soup = BeautifulSoup(ht_r.content, 'html5lib')
ht_headings = ht_soup.findAll("h2", {"class": "newsHdng"})
ht_headings = ht_headings[:10]
ht_news = []
for hth in ht_headings:
    ht_news.append(hth.text)

#NDTV tech news scraping code
ndtv_tech_r = requests.get("https://gadgets360.com/news")
ndtv_tech_soup = BeautifulSoup(ndtv_tech_r.content, 'html5lib')
ndtv_tech_headings = ndtv_tech_soup.find_all("span", {"class":"news_listing"})
ndtv_tech_headings = ndtv_tech_headings[10:18] # removing footer links
ndtv_tech_news = []
for th in ndtv_tech_headings :
    ndtv_tech_news.append(th.text)






#Economicstimes headlines scraping code
th_r = requests.get("https://economictimes.indiatimes.com/news/india")
th_soup = BeautifulSoup(th_r.content, 'html5lib')

th_headings = th_soup.findAll("div", {"class": "eachStory"})
th_headings_item = th_soup.findAll('h3')
th_headings_item = th_headings_item[:11]
th_news = []
for th in th_headings_item:
    th_news.append(th.text)

#Economicstimes tech news scraping
etTech_r = requests.get("https://economictimes.indiatimes.com/tech/technology")
etTech_soup = BeautifulSoup(etTech_r.content, 'html5lib')

etTech_headings = etTech_soup.findAll("div", {"class": "desc"})
etTech_headings_item = etTech_soup.findAll('h4')
etTech_headings_item = etTech_headings_item[0:-5]
etTech_news = []
for th in etTech_headings_item:
    etTech_news.append(th.text)


etSports_r = requests.get("https://economictimes.indiatimes.com/news/sports")
etSports_soup = BeautifulSoup(etSports_r.content, 'html5lib')

etSports_headings = etSports_soup.findAll("div", {"class": "desc"})
etSports_headings_item = etSports_soup.findAll('p')
etSports_headings_item = etSports_headings_item[0:-5]
etSports_news = []
for th in etSports_headings_item:
    etSports_news.append(th.text)

toiFun_r = requests.get("https://timesofindia.indiatimes.com/etimes/etbriefs")
toiFun_soup = BeautifulSoup(toiFun_r.content, 'html5lib')

toiFun_headings = toiFun_soup.find_all('div',{"class":"synopsis"})

toiFun_headings = toiFun_headings[2:15] # removing footer links
toiFun_news = []
for th in toiFun_headings:
    toiFun_news.append(th.text)

toiFun1_r = requests.get("https://gadgets360.com/entertainment")
toiFun1_soup = BeautifulSoup(toiFun1_r.content, 'html5lib')

toiFun1_headings = toiFun1_soup.find_all('div',{"class":"caption"})

toiFun1_headings = toiFun1_headings[2:15] # removing footer links
toiFun1_news = []
for th in toiFun1_headings:
    toiFun1_news.append(th.text)








def signup(request):
    # form = UserCreationForm()
    if request.method == "POST":
        # username= request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.info(request,"Email Taken")
                return redirect('signup')

            elif User.objects.filter(username = username).exists():
                messages.info(request,"Email Taken")
                return redirect('signup')
            else:
                user =User.objects.create_user(username = username,password = password)
                user.email = email
                user.first_name = fname
                user.last_name = lname
                user.save();
                return redirect('signin')
        else:
            messages.info(request,"Password not matching")
            return redirect('signup')
        return redirect('/')
    return render(request,'news/signup.html')

def signin(request):
    context = {}
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['pass1']

        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credentials")
            return redirect('signin')
    else:
        return render(request, 'news/signin.html',context)

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")

def index(req):
    context={
        'toi_news':toi_news,
         'ht_news':ht_news,
         'th_news':th_news
    }
    return render(req, 'news/index.html',context)

@login_required(login_url='/signin')
def tech(request):
    context={
        'toi_tech_news':toi_tech_news,
        'ndtv_tech_news':ndtv_tech_news,
        'etTech_news':etTech_news
    }
    return render(request, 'news/tech.html',context)
@login_required(login_url='/signin')
def sports(request):
    context={
        'toi_sports_news':toi_sports_news,
        'etSports_news':etSports_news
    }
    return render(request,'news/sports.html',context)
@login_required(login_url='/signin')
def entertainment(request):
    context={
        'toiFun_news':toiFun_news,
        'toiFun1_news':toiFun1_news
    }
    return render(request,'news/entertainment.html',context)
