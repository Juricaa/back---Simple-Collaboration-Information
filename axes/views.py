from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from drf_yasg.utils import swagger_auto_schema

from axes.models import Axe
from .serializers import AxeSerializer


# ✅ Liste et création des axes
@swagger_auto_schema(method='post', request_body=AxeSerializer, responses={201: AxeSerializer})
@api_view(['GET', 'POST'])
def axe_list(request):
    if request.method == 'GET':
        axes = Axe.objects.all()

        titre = request.GET.get('titre', None)
        if titre is not None:
            axes = axes.filter(titre__icontains=titre)

        serializer = AxeSerializer(axes, many=True)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AxeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ Détail, mise à jour et suppression d’un axe
@swagger_auto_schema(method='put', request_body=AxeSerializer, operation_description="Met à jour un axe")
@swagger_auto_schema(method='delete', operation_description="Supprime un axe par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def axe_detail(request, pk):
    try:
        axe = Axe.objects.get(pk=pk)
    except Axe.DoesNotExist:
        return JsonResponse({'message': 'Axe non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AxeSerializer(axe)
        return JsonResponse(
            {
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK
        )

    elif request.method == 'PUT':
        serializer = AxeSerializer(axe, data=request.data, partial=True)
        # data = JSONParser().parse(request)
        # serializer = AxeSerializer(axe, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK
            )
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        axe.delete()
        return JsonResponse({'message': 'Axe supprimé avec succès !'}, status=status.HTTP_204_NO_CONTENT)
