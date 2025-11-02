
# Automated Recognition of Autism-Related Behaviors Using Video-Based Pose Estimation

This repository hosts the implementation and experiments for our research paper:
**"Automated Recognition of Autism-Related Behaviors Using Video-Based Pose Estimation"**

Developed by:
- Hossam Fakher, Mayar Khedr, Marwa Emad, Mariam Yasser, Nosayba Rafat, Ahmed Soker  
Department of Artificial Intelligence, Faculty of Computers and Artificial Intelligence, Benha University, Egypt

---

## Abstract
This project proposes an automated pipeline for recognizing repetitive autism-related behaviors — such as arm flapping, spinning, and headbanging — using **RTMPose** for human pose estimation and **machine learning** for classification.  
Through preprocessing (cleaning, interpolation, PCA, augmentation) and model optimization, the system achieves **98.3% accuracy** using Gradient Boosting, outperforming traditional classifiers.

---

## Pipeline Overview
1. Data Cleaning and Frame Standardization  
2. Frame Interpolation (120-frame normalization)  
3. Data Augmentation (flip, rotation, zoom, brightness)  
4. Pose Estimation via RTMPose  
5. Feature Extraction and PCA  
6. Classification using ensemble and neural models  
7. Evaluation and visualization

---

## Technologies Used
- Python 3.x  
- RTMPose (OpenMMLab)  
- Scikit-learn  
- OpenCV, NumPy, Pandas  
- Matplotlib, Seaborn  

---

# Pose Estimation Framework

For pose estimation, this project utilizes RTMPose
 —
a state-of-the-art real-time multi-person human pose estimation framework developed by OpenMMLab as part of the MMPose library.

RTMPose was employed to extract human keypoints (such as head, eyes, hands, and legs) from each video frame.
These keypoints were later processed and used as input features for the machine learning models.

Key RTMPose characteristics leveraged in this research:

CSPNeXt backbone for efficient feature extraction

SimCC (Simple Coordinate Classification) for precise keypoint localization

Real-time multi-person support enabling scalable behavior analysis in unconstrained environments

The extracted keypoints were exported as CSV files and later processed in the notebook
model_training.ipynb for behavior classification.
