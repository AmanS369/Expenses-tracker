


from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate
from tracker.models import expenses_block,balance
from django.contrib.auth import logout
# Create your views here.
def home(request):
 if request.method == 'GET':
   user=request.user
   
   if user.is_authenticated:
     print('y')
     bal=balance.objects.filter(user=user)
     ex_block=expenses_block.objects.filter(user=user).order_by('Date').reverse()
   
     data={}
     data['ex_block']=ex_block
     data['bal']=bal

     return render(request,'home.html',data)
   else:
    return render(request,'home.html')





def register(request):
    if request.method == 'POST':
        First_Name=request.POST['first_name']
        Last_Name=request.POST['last_name']
        username=request.POST['username']
        Email=request.POST['email']
        phone=request.POST['phone']
        Password=request.POST['password']
        Cpassword=request.POST['Cpassword']
        bank_name=request.POST['bank_name']
        income=request.POST['balance']
        
        if Password==Cpassword:
         if User.objects.filter(username=username).exists():
            error_message="Username already taken"
            return render(request, 'register.html',{'error':error_message})
         elif User.objects.filter(email=Email).exists():
              error_message="Email already taken"
              return render(request, 'register.html',{'error':error_message})
         else:
            user=User.objects.create_user(username=username,password=Cpassword,email=Email,first_name=First_Name,last_name=Last_Name)
            user.save();

            register_balance=balance(user=user,bank_name=bank_name,income=income)
            register_balance.save()
            return redirect(home)
        else:
         error_message = "PASSWORD DO NOT MATCH"
         return render(request, 'register.html',{'error':error_message})

    else:  
     return render(request, 'register.html')





def Login(request):
   if request.method == 'POST':
       Email=request.POST['email']
       Password=request.POST['password']
       
       user = auth.authenticate(username=Email, password=Password)
       print(Email)
       print(Password)
       if user is not None:
         auth.login(request,user)
         return redirect(home)
       else:
         error="Invalid Creditanidals"
         return render(request, 'login.html', {'error': error})
   else:
      return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect(home)


def Transcation(request):
    if request.method == 'POST':
       details=request.POST['detail']
       date=request.POST['date']
       type=request.POST['type']
       amount=request.POST['amount']
       category=request.POST['category']
       user=request.user
       balance_upt=balance.objects.get(user=user)
      
       
       
       
       if type == 'credit':
         balance_upt.income=balance_upt.income+int(amount)
         balance_upt.save()
       else:
         balance_upt.income=balance_upt.income-int(amount)
         balance_upt.save()
       Transcation = expenses_block(user=user,category=category,amount=amount,transaction_type=type,Date=date,Details=details,curr_balance=balance_upt.income)
       Transcation.save()


       return redirect(home)


    else:
     return render(request,'transcation.html')





#registeriton of income on other page
def register_income(request):
    if request.method == 'POST':
      user=request.user
      bank_name=request.POST['bank_name']
      income=request.POST['balance']

      register_balance=balance(user=user,bank_name=bank_name,income=income)
      register_balance.save()
      return redirect(home)
    else:
      return redirect(register_income)