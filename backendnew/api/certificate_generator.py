import cv2
import os
from django.core.files.base import ContentFile
from django.conf import settings

def generate_certificate_image(student_name, course_name):
    template_path = os.path.join(settings.MEDIA_ROOT, "images/certificate-template.jpg")
    template = cv2.imread(template_path)

    if template is None:
        raise Exception(f"Certificate template not found at {template_path}")

    font = cv2.FONT_HERSHEY_TRIPLEX
    font_scale = 2  # smaller for testing
    thickness = 3

    name_size = cv2.getTextSize(student_name, font, font_scale, thickness)[0]
    course_size = cv2.getTextSize(course_name, font, font_scale, thickness)[0]

    name_x = int((template.shape[1] - name_size[0]) / 2)
    name_y = int(template.shape[0] * 0.55)

    course_x = int((template.shape[1] - course_size[0]) / 2)
    course_y = int(template.shape[0] * 0.80)

    cv2.putText(template, student_name, (name_x, name_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
    cv2.putText(template, course_name, (course_x, course_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)

    cv2.imwrite("test_output.jpg", template)  # Debugging output

    is_success, buffer = cv2.imencode('.jpg', template)
    if not is_success:
        raise Exception("Failed to encode certificate image")

    return ContentFile(buffer.tobytes(), name=f"{student_name}_certificate.jpg")
