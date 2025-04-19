import qrcode
from io import BytesIO
from config.settings import QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, QR_BORDER


class QRCodeGenerator:
    @staticmethod
    async def generate_qr(data: str) -> bytes:
        """
        Generate a QR code from the given data.
        
        Args:
            data (str): The data to encode in the QR code
            
        Returns:
            bytes: A bytes object containing the generated QR code image
        """
        with BytesIO() as qr:
            qr_data = qrcode.make(
            data=data,
            version=QR_VERSION,
            error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{QR_ERROR_CORRECTION}'),
            box_size=QR_BOX_SIZE,
            border=QR_BORDER,
        )
            qr_data.save(qr, format="PNG")
            return qr.getvalue()