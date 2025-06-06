from django.core.management.base import BaseCommand
from api.models import quiz, course_video

class Command(BaseCommand):
    help = 'Delete quiz records with invalid video foreign keys'

    def handle(self, *args, **kwargs):
        valid_video_ids = set(course_video.objects.values_list('id', flat=True))
        invalid_quizzes = quiz.objects.exclude(video_id__in=valid_video_ids)
        count = invalid_quizzes.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No invalid quiz records found.'))
        else:
            invalid_quizzes.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {count} invalid quiz records.'))
