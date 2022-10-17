        for face in faces:
            landmarks = predictor(imgGray,face)

            landmarks = face_utils.shape_to_np(landmarks)
            leftEye = landmarks[42:48]
            rightEye = landmarks[36:42]

            leftEye = eye_aspect_ratio(leftEye)
            rightEye = eye_aspect_ratio(rightEye)

            eye = (leftEye + rightEye) / 2.0

            if eye<0.3:
                count+=1
            else:
                if count>=3:
                    total+=1

                count=0