from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Video
from .serilizers import CategorySerializer, VideoSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class ChunkedUploadView(APIView):
    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        chunk_number = request.data.get('chunk_number')
        total_chunks = request.data.get('total_chunks')
        video_id = request.data.get('video_id')

        # Generate a chunk file path
        file_name = f"uploads/{video_id}_chunk_{chunk_number}.part"

        # Save the current chunk
        default_storage.save(file_name, ContentFile(file_obj.read()))

        # If the last chunk is uploaded, merge and upload the complete file
        if int(chunk_number) == int(total_chunks):
            final_file_path = self._merge_chunks(video_id, total_chunks)

            # Upload the merged file to MinIO
            object_name = f"{video_id}.mp4"
            upload_to_minio(final_file_path, object_name)

        return Response({'status': 'Chunk received'},
                        status=status.HTTP_200_OK,
                        )

    @staticmethod
    def _merge_chunks(video_id, total_chunks):
        """Merge chunks into a single file."""
        final_file_path = f"uploads/{video_id}.mp4"
        with open(final_file_path, 'wb') as final_file:
            for i in range(1, int(total_chunks) + 1):
                chunk_path = f"uploads/{video_id}_chunk_{i}.part"
                with open(chunk_path, 'rb') as chunk_file:
                    final_file.write(chunk_file.read())
                default_storage.delete(chunk_path)

        return final_file_path
