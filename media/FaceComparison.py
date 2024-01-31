import face_recognition


def compare(registered_photo_data, captured_photo_data, tolerance=0.6):
    # Load the images
    registered_image = face_recognition.load_image_file(registered_photo_data)
    captured_image = face_recognition.load_image_file(captured_photo_data)

    # Get the face encodings for each image
    registered_face_encodings = face_recognition.face_encodings(registered_image)
    captured_face_encodings = face_recognition.face_encodings(captured_image)

    # If no faces are found in either image, return False
    if len(registered_face_encodings) == 0 or len(captured_face_encodings) == 0:
        return False

    # Compare the faces
    matches = face_recognition.compare_faces([registered_face_encodings[0]], captured_face_encodings[0], tolerance)

    return matches[0]
