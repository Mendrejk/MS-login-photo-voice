from enum import Enum

import face_recognition


class FaceComparisonResult(Enum):
    MATCH = 0
    NO_MATCH = 1
    NO_FACE = 2


def compare(registered_photo_data, captured_photo_data, tolerance=0.6) -> FaceComparisonResult:
    # Get the face encodings for each image
    registered_face_encodings = face_recognition.face_encodings(registered_photo_data)
    captured_face_encodings = face_recognition.face_encodings(captured_photo_data)

    # If no faces are found in either image, return False
    if len(registered_face_encodings) == 0 or len(captured_face_encodings) == 0:
        return FaceComparisonResult.NO_FACE

    # Compare the faces
    matches = face_recognition.compare_faces([registered_face_encodings[0]], captured_face_encodings[0], tolerance)

    return FaceComparisonResult.MATCH if matches[0] else FaceComparisonResult.NO_MATCH
