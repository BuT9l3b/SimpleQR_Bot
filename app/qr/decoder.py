import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple


class QRCodeDecoder:
    @staticmethod
    async def decode_qr(image_data: BytesIO) -> Tuple[bool, Optional[str]]:
        """
        Decode a QR code from an image.
        
        Args:
            image_data (BytesIO): The image data containing the QR code
            
        Returns:
            Tuple[bool, Optional[str]]: A tuple containing:
                - bool: Success status
                - Optional[str]: Decoded data or error message
        """
        try:
            # Convert BytesIO to numpy array
            image = Image.open(image_data)
            image_np = np.array(image)
            
            # Convert to grayscale if needed
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            
            # Initialize QR code detector
            qr_detector = cv2.QRCodeDetector()
            
            # Detect and decode QR code
            retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(image_np)
            
            if not retval or not decoded_info:
                return False, "No QR code found in the image"
            
            # Return the first decoded QR code
            return True, decoded_info[0]
            
        except Exception as e:
            return False, f"Error decoding QR code: {str(e)}"