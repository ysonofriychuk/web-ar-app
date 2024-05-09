import numpy as np
import cv2


def find_and_warp(frame, source, cached_ref_pts=None):
    if frame is None or source is None:
        return None, None

    (imgH, imgW) = frame.shape[:2]
    (srcH, srcW) = source.shape[:2]

    # Convert frame to grayscale and apply Gaussian blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest rectangular contour
    max_perimetr = -1
    rect_contour = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        if len(approx) == 4 and perimeter > max_perimetr:  # Check if the contour is a rectangle
            rect_contour = approx

    if rect_contour is None:
        if cached_ref_pts is not None:
            rect_contour = cached_ref_pts
        else:
            return None, None  # Rectangle not found

    # Assume the contour points are in the order: TL, TR, BR, BL
    refPts = rect_contour.reshape(4, 2)
    srcMat = np.array([[0, 0], [srcW, 0], [srcW, srcH], [0, srcH]])
    (H, _) = cv2.findHomography(srcMat, refPts)

    warped = cv2.warpPerspective(source, H, (imgW, imgH))

    # Create a mask and perform masking operations
    mask = np.zeros((imgH, imgW), dtype="uint8")
    cv2.fillConvexPoly(mask, refPts.astype("int32"), 255)
    rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.dilate(mask, rect, iterations=2)
    maskScaled = mask.astype(float) / 255.0
    maskScaled = np.dstack([maskScaled] * 3)
    warpedMultiplied = cv2.multiply(warped.astype("float"), maskScaled)
    imageMultiplied = cv2.multiply(frame.astype("float"), 1.0 - maskScaled)
    output = cv2.add(warpedMultiplied, imageMultiplied)
    output = output.astype("uint8")

    return output, rect_contour
