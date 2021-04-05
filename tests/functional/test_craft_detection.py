from craft_text_detector import Craft, get_prediction
import cv2


class TestCraftDetector:
    def test_craft_detector_on_cpu(self):
        craft = Craft(crop_type="box", cuda=False, refiner=False, rectify=False)
        image = cv2.imread('./test_data/text_sample.png')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # following two cases are not explained in the original repo
        if image.shape[0] == 2:
            image = image[0]
        if image.shape[2] == 4:
            image = image[:, :, :3]

        prediction_result = get_prediction(
            image=image,
            craft_net=craft.craft_net,
            text_threshold=craft.text_threshold,
            link_threshold=craft.link_threshold,
            low_text=craft.low_text,
            cuda=craft.cuda,
            long_size=craft.long_size,
        )
        assert prediction_result

