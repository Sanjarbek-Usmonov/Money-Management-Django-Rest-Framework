from rest_framework import routers
from .views import CategoryViewset, WalletTransactionView, UserRegisterView, CategoryOutcome
from django.urls import path

router = routers.SimpleRouter()

router.register(r'category', CategoryViewset)

urlpatterns = [
    path('transactions/', WalletTransactionView.as_view()),
    path('register', UserRegisterView.as_view(), name='register'),
    path('category_outcome', CategoryOutcome.as_view()),
              ] + router.urls