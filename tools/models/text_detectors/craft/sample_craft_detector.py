from craft_text_detector import Craft
import cv2

# set image path and export folder directory
image_path = r'D:\cloud_bus\cloud-bus-recognition\test\text_sample.png'
output_dir = r'D:\cloud_bus\cloud-bus-recognition\tools\models\craft_text_segmentation\result'

craft = Craft(output_dir=output_dir, crop_type="box", cuda=False, refiner=False, rectify=False)
image = cv2.imread('../../../test/text_sample.png')
prediction_result = craft.detect_text(image_path)

craft.unload_craftnet_model()
craft.unload_refinenet_model()
