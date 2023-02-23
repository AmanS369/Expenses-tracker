import json
from django.http import JsonResponse
from django.db.models import Sum
import datetime
from datetime import datetime, timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import auth,User
from django.contrib.auth import authenticate
from tracker.models import expenses_block,balance
from django.contrib.auth import logout
from tracker.serializers import ExpensesSerializer
from rest_framework import viewsets
# Create your views here.
def home(request):
 if request.method == 'GET':
   user=request.user
   
   if user.is_authenticated:
     today = datetime.now()
     current_month_start = datetime(today.year, today.month, 1)
     current_month_end = current_month_start + timedelta(days=31)
    #  months_ago = todays_date-datetime.timedelta(days=30*1)

     
     bal=balance.objects.filter(user=user)
    #  date__range=[current_month_start, current_month_end]
     expenses = expenses_block.objects.filter(user=user,Date__range=[current_month_start, current_month_end])
     ex_block=expenses.order_by('Date').reverse()
     debit_sum=0
     credit_sum=0
     for expenses in expenses:
          if expenses.transaction_type=='credit' :
            credit_sum=credit_sum+int(expenses.amount)
          else:
            debit_sum=debit_sum+int(expenses.amount)

     expenses = expenses_block.objects.filter(user=user)
     finalrep = {} 
     def get_category(expense):
      return expense.category

     category_list = list(set(map(get_category,expenses)))
     
   
     expenses_category=[]
     for category in category_list:
      category_name=category
      category_amt=expenses_block.objects.filter(user=user,category='Miscellous',transaction_type='debit')
     
     
     expenses_category = {}
     for categorys in category_list:
      category = categorys
      
      expenses =expenses_block.objects.filter(category=category,transaction_type='debit',Date__range=[current_month_start, current_month_end])
      total_spent = expenses.aggregate(Sum('amount'))['amount__sum']
      expenses_category[category] = total_spent
      print(f'Total spent on {category} expenses: {total_spent}')
    
     spend_category_x = list(expenses_category.keys())
     spend_amount_y = list(expenses_category.values())   
       
     datases = {'categories':spend_category_x ,'amounts': spend_amount_y}
     json_data = json.dumps(datases)
     context = {'json_data': json_data}
     data={}
     data['ex_block']=ex_block
     data['bal']=bal
     data['debit_sum']=debit_sum
     data['credit_sum']=credit_sum
     data['expenses_category']=expenses_category
     data['label']=spend_category_x
     data['datas']=spend_amount_y
     data['context']=context
     

     return render(request,'index.html',data)
   else:
    return render(request,'index.html')





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
       type=request.POST['transcation_type']
       amount=request.POST['amount']
       category=request.POST['category']
       user=request.user
       balance_upt=balance.objects.get(user=user)
       balance_upt.income=balance_upt.income-int(amount)
       balance_upt.save()
       Transcation = expenses_block(user=user,category=category,amount=amount,transaction_type=type,Date=date,Details=details,curr_balance=balance_upt.income)
       Transcation.save()


       return redirect(home)


    else:
     return render(request,'transcation.html')


def money_in(request):
  if request.method == 'GET':
    return render(request,'money_in.html')
  else:
       details=request.POST['detail']
       date=request.POST['date']
       type=request.POST['transcation_type']
       amount=request.POST['amount']
       
       user=request.user
       balance_upt=balance.objects.get(user=user)
       balance_upt.income=balance_upt.income+int(amount)
       balance_upt.save()
       Transcation = expenses_block(user=user,amount=amount,transaction_type=type,Date=date,Details=details,curr_balance=balance_upt.income)
       Transcation.save()

       return redirect(home)










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



# to delet transacatio
def delete_transcation(request):
  user=request.user
  delete_id=request.POST['delete_id']
  delete_block=expenses_block.objects.filter(user=user,id=delete_id)
  delete_block.delete()
  ex_block=expenses_block.objects.filter(user=user)
  data={}
  data['ex_block']=ex_block
  return render(request,'tables.html',data)



def Transcation_Table(request):
  if request.method == "GET":
    user=request.user
    ex_block=expenses_block.objects.filter(user=user)
    data={}
    data['ex_block']=ex_block
    return render(request,'tables.html',data)
  else:


    
    user=request.user
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
   
    ex_block=expenses_block.objects.filter(user=user,Date__range=[start_date,end_date])
    data={}
    data['ex_block']=ex_block
    return render(request,'tables.html',data)







    

class ExpensesViewSet(viewsets.ModelViewSet):
     
     queryset=expenses_block.objects.all()
     serializer_class=ExpensesSerializer
     filterset_fields=['user','transaction_type','category']




def expense_category_summary(request):
    today = datetime.now()
    current_month_start = datetime(today.year, today.month, 1)
    current_month_end = current_month_start + timedelta(days=31)
    expenses = expenses_block.objects.filter(user=request.user,transaction_type='debit',
                                      Date__range=[current_month_start, current_month_end])
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'charts.html')