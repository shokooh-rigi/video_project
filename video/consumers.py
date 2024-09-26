import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings


class UploadProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Accept WebSocket connection."""
        await self.accept()

    async def receive(self, text_data):
        """Handle receiving upload progress."""
        data = json.loads(text_data)
        video_id = data['video_id']
        chunk_number = data['chunk_number']
        total_chunks = data['total_chunks']

        # Calculate upload progress
        progress = (int(chunk_number) / int(total_chunks)) * 100

        # Send progress update to client
        await self.send(text_data=json.dumps({
            'video_id': video_id,
            'progress': progress
        }))

        # When upload is complete, send the final link to the client
        if int(chunk_number) == int(total_chunks):
            file_url = f"http://{settings.MINIO_ENDPOINT}/{settings.MINIO_BUCKET_NAME}/{video_id}.mp4"
            await self.send(text_data=json.dumps({
                'video_id': video_id,
                'progress': 100,
                'file_url': file_url
            }))
