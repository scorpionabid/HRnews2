from django.core.management.base import BaseCommand
from news.fetch_api_data import fetch_and_store_news  # İmportu düzgün tənzimləyin

class Command(BaseCommand):
    help = 'Beynəlxalq HR və Texnologiya xəbərlərini News API-dən çəkir və saxlayır.'

    def handle(self, *args, **options):
        """
        HR və Texnologiya kateqoriyalarına uyğun xəbərləri News API vasitəsilə çəkmək və bazaya saxlamaq.
        """
        try:
            # HR sahəsi üzrə xəbərləri çək və saxla
            fetch_and_store_news('human resources', 'dunya', 'Dünya')
            self.stdout.write(self.style.SUCCESS('HR sahəsi üzrə xəbərlər uğurla yeniləndi.'))

            # Texnologiya sahəsi üzrə xəbərləri çək və saxla
            fetch_and_store_news('technology', 'texnologiya', 'Texnologiya')
            self.stdout.write(self.style.SUCCESS('Texnologiya sahəsi üzrə xəbərlər uğurla yeniləndi.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Xəbərlər çəkilərkən xəta baş verdi: {e}"))
