import os
import cv2
import time
import argparse
import numpy as np

import torch

from layers import PriorBox
from config import get_config
from models import RetinaFace
from utils.box_utils import decode, decode_landmarks, nms


def parse_arguments():
    parser = argparse.ArgumentParser(description="Inference Arguments for RetinaFace")

    # Model and device options
    parser.add_argument(
        '-w', '--weights',
        type=str,
        default='./weights/Resnet34_Final.pth',
        help='Path to the trained model weights'
    )
    parser.add_argument(
        '--network',
        type=str,
        default='resnet34',
        choices=[
            'mobilenetv1', 'mobilenetv1_0.25', 'mobilenetv1_0.50',
            'mobilenetv2', 'resnet50', 'resnet34', 'resnet18'
        ],
        help='Backbone network architecture to use'
    )

    # Detection settings
    parser.add_argument(
        '--conf-threshold',
        type=float,
        default=0.02,
        help='Confidence threshold for filtering detections'
    )
    parser.add_argument(
        '--pre-nms-topk',
        type=int,
        default=5000,
        help='Maximum number of detections to consider before applying NMS'
    )
    parser.add_argument(
        '--nms-threshold',
        type=float,
        default=0.4,
        help='Non-Maximum Suppression (NMS) threshold'
    )
    parser.add_argument(
        '--post-nms-topk',
        type=int,
        default=750,
        help='Number of highest scoring detections to keep after NMS'
    )

    # Output options
    parser.add_argument(
        '-s', '--save-image',
        action='store_true',
        default=True,
        help='Save the detection results as images'
    )
    parser.add_argument(
        '-v', '--vis-threshold',
        type=float,
        default=0.6,
        help='Visualization threshold for displaying detections'
    )

    # Image input
    parser.add_argument(
        '--image-path',
        type=str,
        default='./assets/test.jpg',
        help='Path to the input image'
    )

    return parser.parse_args()


@torch.no_grad()
def inference(model, image):
    model.eval()
    loc, conf, landmarks = model(image)

    loc = loc.squeeze(0)
    conf = conf.squeeze(0)
    landmarks = landmarks.squeeze(0)

    return loc, conf, landmarks


def draw_detections(original_image, detections, vis_threshold):
    """
    Draws bounding boxes and landmarks on the image based on multiple detections.

    Args:
        original_image (ndarray): The image on which to draw detections.
        detections (ndarray): Array of detected bounding boxes and landmarks.
        vis_threshold (float): The confidence threshold for displaying detections.
    """

    # Colors for visualization
    LANDMARK_COLORS = [
        (0, 0, 255),    # Right eye (Red)
        (0, 255, 255),  # Left eye (Yellow)
        (255, 0, 255),  # Nose (Magenta)
        (0, 255, 0),    # Right mouth (Green)
        (255, 0, 0)     # Left mouth (Blue)
    ]
    BOX_COLOR = (0, 0, 255)
    TEXT_COLOR = (255, 255, 255)

    # Filter by confidence
    detections = detections[detections[:, 4] >= vis_threshold]

    # Slice arrays efficiently
    boxes = detections[:, 0:4].astype(np.int32)
    scores = detections[:, 4]
    landmarks = detections[:, 5:15].reshape(-1, 5, 2).astype(np.int32)

    for box, score, landmark in zip(boxes, scores, landmarks):
        # Draw bounding box
        cv2.rectangle(original_image, (box[0], box[1]), (box[2], box[3]), BOX_COLOR, 2)

        # Draw confidence score
        text = f"{score:.2f}"
        cx, cy = box[0], box[1] + 12
        cv2.putText(original_image, text, (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, TEXT_COLOR)

        # Draw landmarks
        for point, color in zip(landmark, LANDMARK_COLORS):
            cv2.circle(original_image, point, 1, color, 4)


def main(params):
    # load configuration and device setup
    cfg = get_config(params.network)
    if cfg is None:
        raise KeyError(f"Config file for {params.network} not found!")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rgb_mean = (104, 117, 123)
    resize_factor = 1

    # model initialization
    model = RetinaFace(cfg=cfg)
    model.to(device)
    model.eval()

    # loading state_dict
    state_dict = torch.load(params.weights, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    print("Model loaded successfully!")

    # read image
    original_image = cv2.imread(params.image_path, cv2.IMREAD_COLOR)
    image = np.float32(original_image)
    img_height, img_width, _ = image.shape

    # normalize image
    image -= rgb_mean
    image = image.transpose(2, 0, 1)  # HWC -> CHW
    image = torch.from_numpy(image).unsqueeze(0)  # 1CHW
    image = image.to(device)

    # forward pass
    loc, conf, landmarks = inference(model, image)

    # generate anchor boxes
    priorbox = PriorBox(cfg, image_size=(img_height, img_width))
    priors = priorbox.generate_anchors().to(device)

    # decode boxes and landmarks
    boxes = decode(loc, priors, cfg['variance'])
    landmarks = decode_landmarks(landmarks, priors, cfg['variance'])

    # scale adjustments
    bbox_scale = torch.tensor([img_width, img_height] * 2, device=device)
    boxes = (boxes * bbox_scale / resize_factor).cpu().numpy()

    landmark_scale = torch.tensor([img_width, img_height] * 5, device=device)
    landmarks = (landmarks * landmark_scale / resize_factor).cpu().numpy()

    scores = conf.cpu().numpy()[:, 1]

    # filter by confidence threshold
    inds = scores > params.conf_threshold
    boxes = boxes[inds]
    landmarks = landmarks[inds]
    scores = scores[inds]

    # sort by scores
    order = scores.argsort()[::-1][:params.pre_nms_topk]
    boxes, landmarks, scores = boxes[order], landmarks[order], scores[order]

    # apply NMS
    detections = np.hstack((boxes, scores[:, np.newaxis])).astype(np.float32, copy=False)
    keep = nms(detections, params.nms_threshold)

    detections = detections[keep]
    landmarks = landmarks[keep]

    # keep top-k detections and landmarks
    detections = detections[:params.post_nms_topk]
    landmarks = landmarks[:params.post_nms_topk]

    # concatenate detections and landmarks
    detections = np.concatenate((detections, landmarks), axis=1)

    # show image
    if params.save_image:
        draw_detections(original_image, detections, params.vis_threshold)
        # save image
        im_name = os.path.splitext(os.path.basename(params.image_path))[0]
        save_name = f"{im_name}_{params.network}_out.jpg"
        cv2.imwrite(save_name, original_image)
        print(f"Image saved at '{save_name}'")


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
