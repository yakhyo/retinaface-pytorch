# 📸 RetinaFace: Single-stage Dense Face Localisation in the Wild

[![Downloads](https://img.shields.io/github/downloads/yakhyo/retinaface-pytorch/total)](https://github.com/yakhyo/retinaface-pytorch/releases)
[![GitHub Repo stars](https://img.shields.io/github/stars/yakhyo/retinaface-pytorch)](https://github.com/yakhyo/retinaface-pytorch/stargazers)
[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/yakhyo/retinaface-pytorch)
[![GitHub License](https://img.shields.io/github/license/yakhyo/retinaface-pytorch)](https://github.com/yakhyo/retinaface-pytorch/blob/main/LICENSE)

> [!TIP]  
> The models and functionality in this repository are **integrated into [UniFace](https://github.com/yakhyo/uniface)** — an all-in-one face analysis toolkit.  
> [![PyPI Version](https://img.shields.io/pypi/v/uniface.svg)](https://pypi.org/project/uniface/) [![GitHub Stars](https://img.shields.io/github/stars/yakhyo/uniface)](https://github.com/yakhyo/uniface/stargazers) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)


<video controls autoplay loop src="https://github.com/user-attachments/assets/ad279fea-33fb-43f1-884f-282e6d54c809" muted="false" width="100%"></video>

This is a face detection model for high-precision facial localization based on [RetinaFace: Single-stage Dense Face Localisation in the Wild](https://arxiv.org/abs/1905.00641). This model accurately detects facial landmarks and bounding boxes for faces in images. This repository provides custom training & inference code, and several new backbone models have been integrated for improved performance and flexibility.

> [!NOTE]  
> We've updated the codebase with new trained models and a refactored structure, enhancing functionality and maintainability. These improvements include support for MobileNetV1 (including v1_025 and v1_050), MobileNetV2, and various ResNet versions (18, 34, 50), offering a cleaner and more reproducible experience.

<div align="center">
<img src="assets/mv2_test.jpg">
</div>

In this implementation, we use several lightweight and powerful backbone architectures to provide flexibility between performance and accuracy.

## ✨ Features

| Date       | Feature Description                                                                                                                                                                           |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2024-11-27 | 🔄 **New trained model weights**: Filtering out smaller faces (<16 pixels) to decrease false positives.                                                                                       |
| 2024-11-05 | 🎥 **Webcam Inference**: Real-time inference capability using a webcam for direct application testing and live demos.                                                                         |
| 2024-11-05 | 🔄 **ONNX Export & Inference**: Enables model export to ONNX format for versatile deployment and cross-platform inference.                                                                    |
| 2024-11-05 | ✅ **Cleaner & Reproducible Code**: Refactored for simplicity and consistency, making it easier to use and maintain.                                                                          |
| 2024-11-05 | 📱 **MobileNetV1_0.25 & MobileNetV1_0.50**: Lightweight versions for faster inference with reduced computational cost.                                                                        |
| 2024-11-05 | 📲 **MobileNetV1**: [Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/abs/1704.04861) - Optimized for mobile and low-power applications.             |
| 2024-11-05 | 📈 **MobileNetV2**: [Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381) - Improved efficiency for mobile use-cases with advanced architecture.                      |
| 2024-11-05 | 🔍 **ResNet Models (18, 34, 50)**: [Deep Residual Networks](https://arxiv.org/abs/1512.03385) - Enhanced accuracy with deeper residual connections, supporting a range of model complexities. |


## 📈 Results on WiderFace Evaluation Set

### Multi-scale image resizing

| RetinaFace Backbones          | Easy       | Medium     | Hard       |
| ----------------------------- | ---------- | ---------- | ---------- |
| MobileNetV1 (width mult=0.25) | 88.48%     | 87.02%     | 80.61%     |
| MobileNetV1 (width mult=0.50) | 89.42%     | 87.97%     | 82.40%     |
| MobileNetV1                   | 90.59%     | 89.14%     | 84.13%     |
| MobileNetV2                   | 91.70%     | 91.03%     | 86.60%     |
| ResNet18                      | 92.50%     | 91.02%     | 86.63%     |
| ResNet34                      | **94.16%** | **93.12%** | **88.90%** |
| ResNet50                      |            |            |            |

### Original image size

| RetinaFace Backbones          | Easy       | Medium     | Hard       |
| ----------------------------- | ---------- | ---------- | ---------- |
| MobileNetV1 (width mult=0.25) | 90.70%     | 88.12%     | 73.82%     |
| MobileNetV1 (width mult=0.50) | 91.56%     | 89.46%     | 76.56%     |
| MobileNetV1                   | 92.19%     | 90.41%     | 79.56%     |
| MobileNetV2                   | 94.04%     | 92.26%     | 83.59%     |
| ResNet18                      | 94.28%     | 92.69%     | 82.95%     |
| ResNet34                      | **95.07%** | **93.48%** | **84.40%** |
| ResNet50                      |            |            |            |

## 📈 Results on WiderFace Evaluation Set (filtered out faces smaller than `16 pixels`)

- Check the line 61 in `transform.py`
- Makes less FP and good at `easy` & `medium` samples, but does not perform well on `hard` samples.

### Multi-scale image resizing

| RetinaFace Backbones          | Easy       | Medium     | Hard       |
| ----------------------------- | ---------- | ---------- | ---------- |
| MobileNetV1 (width mult=0.25) | 89.02%     | 87.34%     | 80.04%     |
| MobileNetV1 (width mult=0.50) | 89.54%     | 87.93%     | 82.24%     |
| MobileNetV1                   | 91.29%     | 89.87%     | 84.36%     |
| MobileNetV2                   | 92.78%     | 92.34%     | 87.51%     |
| ResNet18                      | 92.26%     | 91.63%     | 86.88%     |
| ResNet34                      | **94.19%** | **93.29%** | **88.94%** |
| ResNet50                      |            |            |            |

### Original image size

| RetinaFace Backbones          | Easy       | Medium     | Hard   |
| ----------------------------- | ---------- | ---------- | ------ |
| MobileNetV1 (width mult=0.25) | 91.68%     | 89.69%     | 61.49% |
| MobileNetV1 (width mult=0.50) | 92.22%     | 90.49%     | 62.93% |
| MobileNetV1                   | 93.65%     | 92.00%     | 64.72% |
| MobileNetV2                   | 95.23%     | 94.13%     | 67.75% |
| ResNet18                      | 95.21%     | 93.90%     | 67.00% |
| ResNet34                      | **95.81%** | **94.60%** | 67.66% |
| ResNet50                      |            |            |        |


## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yakhyo/retinaface-pytorch.git
   cd retinaface-pytorch
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔄 Backbones

This RetinaFace implementation supports the following feature extractor backbones:

- 🟢 **MobileNetV1**: Lightweight and fast, suitable for mobile and embedded devices.
- 🟠 **MobileNetV1_0.25 & 0.50**: Variants of MobileNetV1 with reduced width multipliers for faster inference.
- 🔵 **MobileNetV2**: Improved version of MobileNetV1 with better accuracy.
- 🟣 **ResNet18/34/50**: A range of ResNet models providing a balance between complexity and performance.

## 📂 Dataset

### 📥 Download the WIDERFACE Dataset

1. **Download the Dataset**:

   - Download the [WIDERFACE](http://shuoyang1213.me/WIDERFACE/WiderFace_Results.html) dataset.
   - Download annotations (face bounding boxes & five facial landmarks) from [Baidu Cloud](https://pan.baidu.com/s/1Laby0EctfuJGgGMgRRgykA) (password: `fstq`) or [Dropbox](https://www.dropbox.com/s/7j70r3eeepe4r2g/retinaface_gt_v1.1.zip?dl=0).

2. **Organize the Dataset Directory**:

   Structure your dataset directory as follows:

   ```
   data/
   └── widerface/
      ├── train/
      │   ├── images/
      │   └── label.txt
      └── val/
         ├── images/
         └── wider_val.txt
   ```

> [!NOTE]  
> `wider_val.txt` only includes val file names but not label information.

There is also an organized dataset (as shown above): Link from [Google Drive](https://drive.google.com/open?id=11UGV3nbVv1x9IC--_tK3Uxf7hA6rlbsS) or [Baidu Cloud](https://pan.baidu.com/s/1jIp9t30oYivrAvrgUgIoLQ) _(password: ruck)_. Thanks to [biubug6](https://github.com/biubug6) for the organized dataset.

## 🏋️‍♂️ Training

To train the RetinaFace model with a specific backbone, use the following command:

```bash
python train.py --network mobilenetv1  # Replace 'mobilenetv1' with your choice of backbone
```

Download [mobilenetv1_0.25.pretrained](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/mobilenetv1_025.pretrained) (pre-trained weights on ImageNet, weights ported from @biubug6) to reproduce the results.

### 🎛️ Available Backbone Options:

- `mobilenetv1_0.25`
- `mobilenetv1_0.50`
- `mobilenetv1`
- `mobilenetv2`
- `resnet18`
- `resnet34`
- `resnet50`

### ⬇️ Get Pretrained Models

#### MobileNet-based models:

| Model Name      | PyTorch Weights                                                                                                          | ONNX Weights Filename                                                                                                      |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| MobileNetV1_025 | [retinaface_mv1_0.25.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1_0.25.pth) | [retinaface_mv1_0.25.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1_0.25.onnx) |
| MobileNetV1_050 | [retinaface_mv1_0.50.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1_0.50.pth) | [retinaface_mv1_0.50.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1_0.50.onnx) |
| MobileNetV1     | [retinaface_mv1.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1.pth)           | [retinaface_mv1.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv1.onnx)           |
| MobileNetV2     | [retinaface_mv2.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv2.pth)           | [retinaface_mv2.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_mv2.onnx)           |

#### ResNet-based models:

| Model Name | PyTorch Weights                                                                                                | ONNX Weights Filename                                                                                            |
| ---------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| ResNet18   | [retinaface_r18.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_r18.pth) | [retinaface_r18.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_r18.onnx) |
| ResNet34   | [retinaface_r34.pth](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_r34.pth) | [retinaface_r34.onnx](https://github.com/yakhyo/retinaface-pytorch/releases/download/v0.0.1/retinaface_r34.onnx) |
| ResNet50   | [not available](#)                                                                                             | [not available](#)                                                                                               |

## 📊 Inference

Image Inference:

```bash
python detect.py -n mobilenetv1 -w retinaface_mv1.pth
```

Video Inference
```bash
python webcam_inference.py -n mobilenetv2 -w retinaface_mv2.pth --source [path/to/video&webcam] --save-video
```

<div align="center">
<p>Using MobileNet v2 as a backbone, 632 faces found on large selfi image, see the `assets` folder.</p>
<img src="assets/mv2_large_selfi_632people.jpg">
</div>

### Export to ONNX

Run following command to export `.pth` (pytorch model) to `ONNX`:

Static shapes:
```
python -m scripts.onnx_export -w pytorch/model/path -n network/arch/name
```

Dynamix shapes:
```
python -m scripts.onnx_export -w pytorch/model/path -n network/arch/name --dynamic
```

## 🧪 Evaluating RetinaFace on WiderFace Dataset

### 1. Get and Install WiderFace Evaluation Tool

1. Clone the WiderFace evaluation repository inside the `retinaface-pytorch` folder:
   ```bash
   git clone https://github.com/yakhyo/widerface_evaluation
   ```
2. Navigate to the `widerface_evaluation` folder and build the required extension:
   ```bash
   cd widerface_evaluation
   python3 setup.py build_ext --inplace
   ```
3. Return to the `retinaface-pytorch` folder after installation is complete:
   ```bash
   cd ..
   ```

### 2. Generate Predictions

Run the following command to evaluate your RetinaFace model with WiderFace, specifying the model architecture (`mobilenetv1` in this example) and the path to the trained weights. Predictions will be stored in `widerface_txt` inside the `widerface_evaluation` folder.

```bash
python evaluate_widerface.py --network mobilenetv1 --weights weights/mobilenetv1.pth
```

### 3. Run the Final Evaluation

After generating predictions, navigate to the widerface_evaluation folder and run the following command to compare predictions with the ground truth annotations:

```bash
cd widerface_evaluation
python evaluation.py -p widerface_txt -g ground_truth
```

> [!NOTE]  
> Ensure `ground_truth` is the path to the WiderFace ground truth directory.

This will begin the evaluation process of your model on the WiderFace dataset.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔗 References

- https://github.com/biubug6/Pytorch_Retinaface
- https://github.com/yakhyo/faceboxes-pytorch
