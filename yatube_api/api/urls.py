from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (PostViewSet, CommentViewSet,
                    FollowViewSet, GroupViewSet)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'v1/posts/<int:post_id>/comments/',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='comments-list'
    ),
    path(
        'v1/posts/<int:post_id>/comments/<int:pk>/',
        CommentViewSet.as_view({'get': 'retrieve',
                                'patch': 'partial_update',
                                'delete': 'destroy'}),
        name='comment-detail'
    ),
    # Добавляем маршруты для JWT-аутентификации
    path('v1/jwt/create/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(),
         name='token_verify'),
]
