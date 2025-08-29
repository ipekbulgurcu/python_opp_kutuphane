"""Barcode scanner module using OpenCV and pyzbar."""

import cv2
from pyzbar.pyzbar import decode
from typing import Optional, Tuple

class BarcodeScanner:
    def __init__(self):
        self.cap = None
        
    def start_camera(self) -> bool:
        """Start camera capture"""
        self.cap = cv2.VideoCapture(0)
        return self.cap.isOpened()
        
    def scan_barcode(self) -> Optional[Tuple[str, str]]:
        """Scan barcode/ISBN from camera
        Returns: Tuple of (barcode_data, barcode_type) if detected, None otherwise
        """
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError("Camera not started")
            
        ret, frame = self.cap.read()
        if not ret:
            return None
            
        # Decode barcodes in frame
        barcodes = decode(frame)
        
        for barcode in barcodes:
            # Draw rectangle around barcode
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x-10, y-10), 
                         (x+w+10, y+h+10), (0, 255, 0), 2)
                         
            # Get barcode data
            data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Show frame with rectangle
            cv2.imshow('Barcode Scanner', frame)
            return data, barcode_type
            
        # Show frame even if no barcode detected
        cv2.imshow('Barcode Scanner', frame)
        return None
        
    def stop_camera(self):
        """Stop camera capture and close windows"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
