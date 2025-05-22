import qrcode
from io import BytesIO
from django.conf import settings
from django.urls import reverse


def generate_qr_code(certificate):
    """
    Generate a QR code for a certificate.
    The QR code will contain a URL to validate the certificate.
    """
    # Generate the validation URL
    validation_url = settings.BASE_URL + reverse('certificate-validate')
    qr_data = f"{validation_url}?code={certificate.unique_code}"

    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Create an image from the QR Code
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Convert to BytesIO
    buffer = BytesIO()
    qr_image.save(buffer, format='PNG')
    buffer.seek(0)

    return buffer
