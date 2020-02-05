import torch
from torch.autograd import Variable
import tools.models.moran.tools.utils as utils
import tools.models.moran.tools.dataset as dataset
from PIL import Image
from collections import OrderedDict
import cv2
from tools.models.moran.models.moran import MORAN as moran_recognizer


class RecognitionInterface:
    def __init__(self):
        self.model_name = "moran"
        self.model_path = "tools/models/moran/demo.pth"

    def run_recognition(self, cv2_image):
        alphabet = '0:1:2:3:4:5:6:7:8:9:a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r:s:t:u:v:w:x:y:z:$'

        cuda_flag = False
        if torch.cuda.is_available():
            cuda_flag = True
            MORAN = moran_recognizer(1, len(alphabet.split(':')), 256, 32, 100, BidirDecoder=True, CUDA=cuda_flag)
            MORAN = moran_recognizer.cuda()
        else:
            MORAN = moran_recognizer(1, len(alphabet.split(':')), 256, 32, 100, BidirDecoder=True, inputDataType='torch.FloatTensor', CUDA=cuda_flag)

        print('loading pretrained model from %s' % self.model_path)
        if cuda_flag:
            state_dict = torch.load(self.model_path)
        else:
            state_dict = torch.load(self.model_path, map_location='cpu')
        MORAN_state_dict_rename = OrderedDict()
        for k, v in state_dict.items():
            name = k.replace("module.", "") # remove `module.`
            MORAN_state_dict_rename[name] = v
        MORAN.load_state_dict(MORAN_state_dict_rename)

        for p in MORAN.parameters():
            p.requires_grad = False
        MORAN.eval()

        converter = utils.strLabelConverterForAttention(alphabet, ':')
        transformer = dataset.resizeNormalize((100, 32))
        image = Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY))
        image.convert('L')
        image = transformer(image)

        if cuda_flag:
            image = image.cuda()
        image = image.view(1, *image.size())
        image = Variable(image)
        text = torch.LongTensor(1 * 5)
        length = torch.IntTensor(1)
        text = Variable(text)
        length = Variable(length)

        max_iter = 20
        t, l = converter.encode('0'*max_iter)
        utils.loadData(text, t)
        utils.loadData(length, l)
        output = MORAN(image, length, text, text, test=True, debug=True)

        preds, preds_reverse = output[0]
        demo = output[1]

        _, preds = preds.max(1)
        _, preds_reverse = preds_reverse.max(1)

        sim_preds = converter.decode(preds.data, length.data)
        sim_preds = sim_preds.strip().split('$')[0]

        return sim_preds
