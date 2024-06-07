import cv2
import numpy as np
import pytesseract
import re

def align_image_by_contour(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    box = cv2.boxPoints(rect)
    box = np.intp(box)

    width = int(rect[1][0])
    height = int(rect[1][1])

    if width < height:
        width, height = height, width

    pts_dst = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype="float32")
    h, status = cv2.findHomography(box, pts_dst)
    aligned_image = cv2.warpPerspective(image, h, (width, height))

    return aligned_image

def align_image_by_content(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    scale_percent = 200  # увеличим изображение на 200%
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    dim = (width, height)
    gray = cv2.resize(gray, dim, interpolation=cv2.INTER_AREA)
    
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 3)

    try:
        osd = pytesseract.image_to_osd(gray)
        angle = float(re.search('(?<=Rotate: )\d+', osd).group(0))

        if angle != 0:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated
    except pytesseract.TesseractError as e:
        print(f"Tesseract error: {e}")
        return image

def align_image_by_hough_transform(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is not None:
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            angles.append(angle)

        median_angle = np.median(angles)
        angle = -median_angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        return rotated
    else:
        raise ValueError("Не удалось найти линии для выравнивания изображения.")

def main():
    image_path = 'C:/mp2024-3211_python/image.jpg'  # Путь к вашему изображению
    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Не удалось загрузить изображение по пути: {image_path}")

    try:
        aligned_contour = align_image_by_contour(image)
        print('Изображение выровнено по внешнему контуру')
    except ValueError as e:
        print(e)
        aligned_contour = image

    try:
        aligned_content = align_image_by_content(aligned_contour)
        print('Изображение выровнено по содержимому')
    except ValueError as e:
        print(e)
        aligned_content = aligned_contour

    try:
        aligned_hough_transform = align_image_by_hough_transform(aligned_content)
        print('Изображение выровнено с помощью Hough Transform')
    except ValueError as e:
        print(e)
        aligned_hough_transform = aligned_content

    combined_image = aligned_hough_transform

    output_path = 'C:/mp2024-3211_python/combined_aligned_image.jpg'
    cv2.imwrite(output_path, combined_image)
    print(f'Итоговое изображение сохранено как {output_path}')

if __name__ == '__main__':
    main()
