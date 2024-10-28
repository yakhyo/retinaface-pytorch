import os
import cv2
import argparse
import numpy as np

import torch

from layers import PriorBox
from config import get_config
from models import RetinaFace
from utils.box_utils import decode, decode_landmarks, nms


def parse_arguments():
    parser = argparse.ArgumentParser(description="Retinaface Webcam Inference")

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
        default=0.4,
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
        '-v', '--vis-threshold',
        type=float,
        default=0.6,
        help='Visualization threshold for displaying detections'
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
    for det in detections:
        if det[4] < vis_threshold:
            continue

        # Draw bounding box
        text = "{:.4f}".format(det[4])
        det = list(map(int, det))
        cv2.rectangle(original_image, (det[0], det[1]), (det[2], det[3]), (0, 0, 255), 2)
        cx, cy = det[0], det[1] + 12
        cv2.putText(original_image, text, (cx, cy), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

        # Draw landmarks
        cv2.circle(original_image, (det[5], det[6]), 1, (0, 0, 255), 4)
        cv2.circle(original_image, (det[7], det[8]), 1, (0, 255, 255), 4)
        cv2.circle(original_image, (det[9], det[10]), 1, (255, 0, 255), 4)
        cv2.circle(original_image, (det[11], det[12]), 1, (0, 255, 0), 4)
        cv2.circle(original_image, (det[13], det[14]), 1, (255, 0, 0), 4)


def main(params):
    cfg = get_config(params.network)
    if cfg is None:
        raise KeyError(f"Config file for {params.network} not found!")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    rgb_mean = (104, 117, 123)
    resize_factor = 1

    # model initialization
    model = RetinaFace(cfg=cfg)
    model.to(device)

    # loading state_dict
    state_dict = torch.load(params.weights, map_location="cpu", weights_only=True)
    model.load_state_dict(state_dict)
    print("Model loaded successfully!")

    # Open webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Prepare the frame for inference
        image = np.float32(frame)
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

        # draw detections on the frame
        draw_detections(frame, detections, params.vis_threshold)

        # Display the resulting frame
        cv2.imshow('Webcam Inference', frame)

        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
