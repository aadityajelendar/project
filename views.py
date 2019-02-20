from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from models import Product,Stock,Cart
from signupapp.forms import SignUpForm
from signupapp.tokens import account_activation_token
from django.http import HttpResponse

def home(request):
    if request.method=="GET":
        return render(request,'home1.html')
    else:
        data=request.POST["drop1"]
        if data=="pn":
            pnm=request.POST["dt"]
            recs=Product.objects.filter(pname=pnm)
            return render(request,'display1.html',{'records':recs})
        else:
            pi=int(request.POST["dt"])
            recs=Product.objects.filter(pid=pi)
            return render(request,'display1.html',{'records':recs})
       


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')
def search(request):
    if request.method=="GET":
        return render(request,'search.html')
    else:
        data=request.POST["drop1"]
        if data=="pn":
            pnm=request.POST["dt"]
            recs=Product.objects.filter(pname=pnm)
            return render(request,'display.html',{'records':recs})
        else:
            pi=int(request.POST["dt"])
            recs=Product.objects.filter(pid=pi)
            return render(request,'display.html',{'records':recs}) 
@login_required
def cart(request):
    return render(request,'cart.html',display(request))
@login_required
def track(request):
    return render(request,'track.html')
@login_required
def cancel(request):
    return render(request,'cancel.html')

@login_required
def addcart(request):
    x=request.GET["pid"]
    qt=Stock.objects.filter(prodid=x)
    qtt=0
    for p in qt:
        #global qtt
        qtt=p
    qt=[q for q in range(1,qtt.tot_qty+1)]
    return render(request,'addcart.html',{"pid":x,"qtt":qt})
def insertcart(request):
    x=request.GET["pid"]
    qt=request.GET["qt"]
    user = User.objects.get(id=request.session.get("_auth_user_id"))
    un=str(user.username)
    pr=Product.objects.get(pid=x)
    a=int(str(x))
    b=int(str(qt))
    c=un
    d=float(pr.pcost)
    e=int(str(qt))*float(pr.pcost)
    ct=Cart(username=c,pid=a,units=b,unitprice=d,tuprice=e)
    ct.save()
    return render(request,'insertcart.html')
def viewcart(request):
    return render(request,'cart.html',display(request))
def deletecart(request):
    cs=Cart.objects.filter(id=int(request.GET["id"]))
    cs.delete()
    return render(request,'cart.html',display(request))
def modifycart(request):
    x=request.GET["pid"]
    qt=Stock.objects.filter(prodid=x)
    qtt=0
    for p in qt:
        global qtt
        qtt=p
    qt=[q for q in range(1,qtt.tot_qty+1)]
    oldqt=request.session[x]
    return render(request,'modifyqty.html',{"pid":x,"qtt":qt,"oq":oldqt})
def modifiedcart(request):
    request.session[request.GET["pid"]]=request.GET["nqt"]
    dic={}
    for k,v in request.session.items():
        if k[0]!='_':
            dic[k]=v
    return render(request,'cart.html',{"k":dic})
    
def display(request):
    user = User.objects.get(id=request.session.get("_auth_user_id"))
    un=str(user.username)
    ct=Cart.objects.filter(username=un)
    tp=0.0
    for p in ct:
        tp=tp+float(p.tuprice)
    dic={"k":ct,"tp":tp}
    return dic











