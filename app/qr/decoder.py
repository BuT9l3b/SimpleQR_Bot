import cv2
import numpy as np
from PIL import Image
from typing import Optional, Tuple, BinaryIO
import logging


logger = logging.getLogger(__name__)


class QRCodeDecoder:
    @staticmethod
    async def decode_qr(image_data: BinaryIO) -> Tuple[bool, Optional[str]]:
        """
        Decode a QR code from an image.
        
        Args:
            image_data (BinaryIO): The image data containing the QR code
            
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
            
            qr_detector = cv2.QRCodeDetector()  # Initialize QR code detector
            
            data, bbox, _ = qr_detector.detectAndDecode(image_np)  # Detect and decode QR code
            
            if not data: return False, "No QR code found in the image"
            return True, data  # Return the decoded QR code
            
        except Exception as e:
            logger.error(f"Error decoding QR code: {e}")
            return False, f"Error decoding QR code: {str(e)}"