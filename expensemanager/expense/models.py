from django.db import models
from user.models import User
# Create your models here.

paymentmethod = (
    
    ('crediCard','crediCard'),
    ('cash','cash'),
    ('cheque','cheque'),
    ('UPI','UPI'),
    
)

statuss = (
    
    ('cleared','cleared'),
    ('uncleared','uncleared'),
    ('void','void'),
    
)

class Category(models.Model):
    categoryName = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'category'
    
    def __str__(self):
        return self.categoryName

class SubCategory(models.Model):
    subCategoryName = models.CharField(max_length=50)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    class Meta:
        db_table = 'subcategory'
        
    def __str__(self):
        return self.subCategoryName

goalStatus = (
    
    ('active','active'),
    ('paused','paused'),
    ('not-active','not-active'),
    
)    
class ExpenseGoal(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null= True)
    goalName = models.CharField(max_length=100) 
    maxAmount = models.PositiveIntegerField()
    startDate =models.DateField()
    endDate = models.DateField()
    status = models.CharField(max_length=100,choices=goalStatus)
    
    class Meta:
        db_table ="expGoal"
    
    def __str__(self):
        return self.goalName         
    
    
class Expense(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,null= True)
    amount = models.FloatField()
    expDateTime = models.DateTimeField()
    #payee = models.ForeignKey(Payee,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE)
    paymentMethod = models.CharField(max_length=50,choices=paymentmethod)
    status = models.CharField(max_length=255,choices=statuss)
    description = models.TextField()
    transactionType = models.CharField(max_length=255)
    goal = models.ForeignKey(ExpenseGoal,on_delete=models.CASCADE,null = True)
    
    class Meta:
        db_table = 'expense'
        
        
    def __str__(self):
        return self.description
    
    
class Books(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    bookImage = models.ImageField(upload_to="uploads/")
    
    
    
    class Meta:
        db_table = "books"
    
    def __str__(self):
        return self.name
  




