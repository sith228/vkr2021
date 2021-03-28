from craft_text_detector import Craft

# set image path and export folder directory
image_path = r'D:\cloud_bus\cloud-bus-recognition\test\mobilenet_data_v1\2019-10-06 13-12-21.jpg'
output_dir = r'D:\cloud_bus\cloud-bus-recognition\tools\models\craft_text_segmentation\result'

craft = Craft(output_dir=output_dir, crop_type="box", cuda=False, refiner=False, rectify=False)
prediction_result = craft.detect_text(image_path)

craft.unload_craftnet_model()
craft.unload_refinenet_model()
