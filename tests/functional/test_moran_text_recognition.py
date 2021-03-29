from tools.models.moran_text_recognition.recongition_interface import RecognitionInterface
import cv2


class TestMoranTextRecognition:
    def test_can_recognize_text(self):
        recognizer = RecognitionInterface()
        image = cv2.imread('./test/text_sample.png')
        text = recognizer.run_recognition(image)
        assert text == '181'
