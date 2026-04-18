from pathlib import Path

import qrcode
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Generate QR code for the website URL"

    def add_arguments(self, parser):
        parser.add_argument(
            "--url",
            default="https://kryschendo.com",
            help="URL to encode in the QR code",
        )

    def handle(self, *args, **options):
        url = options["url"]

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="#2D5A5A", back_color="#FAFAF7")

        output_path = (
            Path(__file__).resolve().parent.parent.parent
            / "static"
            / "main"
            / "images"
            / "qr_code.png"
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        img.save(output_path)

        self.stdout.write(
            self.style.SUCCESS(f"QR code for {url} saved to {output_path}")
        )
