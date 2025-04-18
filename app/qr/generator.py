import qrcode
from io import BytesIO
from config.settings import QR_VERSION, QR_ERROR_CORRECTION, QR_BOX_SIZE, QR_BORDER


class QRCodeGenerator:
    @staticmethod
    async def generate_qr(data: str) -> BytesIO:
        """
        Generate a QR code from the given data.
        
        Args:
            data (str): The data to encode in the QR code
            
        Returns:
            BytesIO: A BytesIO object containing the generated QR code image
        """
        # Create QR code instance
        qr = qrcode.QRCode(
            version=QR_VERSION,
            error_correction=getattr(qrcode.constants, f'ERROR_CORRECT_{QR_ERROR_CORRECTION}'),
            box_size=QR_BOX_SIZE,
            border=QR_BORDER,
        )
        
        # Add data
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr