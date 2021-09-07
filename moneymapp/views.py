from rest_framework import viewsets, permissions, views, response, status
from .models import Category, Wallet, Transactions
from .serializers import CategorySerializer, WalletTransactionSerializer, UserRegisterSerializer, CategoryOutcomeSerializer
from django.db.models import Sum
from rest_framework.pagination import LimitOffsetPagination

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class WalletTransactionView(views.APIView, LimitOffsetPagination):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        queryset = Transactions.objects.filter(wallet__user=self.request.user)
        qs_type = request.GET.get('type', None)
        if qs_type:
            queryset = queryset.filter(_type=qs_type)
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = WalletTransactionSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = WalletTransactionSerializer(
            data=request.data,
            context={'user': self.request.user, 'category_id': self.request.data.get('category_id', None)}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class UserRegisterView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class CategoryOutcome(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = (Transactions.objects.filter(wallet__user=self.request.user, _type=Transactions.OUT)
                    .values('category__name')
                    .annotate(total_sum=Sum('amount'))).order_by('-total_sum')
        serializer = CategoryOutcomeSerializer(queryset, many=True)
        return response.Response(serializer.data)