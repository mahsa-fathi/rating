from rest_framework import generics, permissions, pagination, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from collections import OrderedDict

from social.models import Post, UserRating
from social.serializers import PostSerializer,  UserRatingSerializer


class PostListPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('number_of_pages', self.page.paginator.num_pages),
            ('results', data)
        ]))


class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')
    serializer_class = PostSerializer
    pagination_class = PostListPagination


class UserRatingAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            post_id = int(request.data.get('post'))
            user_rating_value = int(request.data.get('rate'))
            request.data['user'] = request.user.id

            rating, created = UserRating.objects.get_or_create(
                user=request.user, post_id=post_id,
                defaults={'rate': user_rating_value}
            )

            if not created:
                # Update the existing rating
                rating.rate = user_rating_value
                rating.save(update_fields=['rate', 'updated_at'])
            else:
                rating.save()

            return Response({'success': True}, status=status.HTTP_200_OK)
        except TypeError as e:
            return Response(
                data={'success': False, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response(
                data={'success': False, 'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                data={'success': False, 'message': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
