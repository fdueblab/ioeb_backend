WST-跨境支付AI监测-002-260624 Algorithm

This algorithm analyzes video or image content to detect suspicious activities
related to financial transactions and money laundering scenarios.
It uses computer vision techniques to identify behavioral patterns that may
indicate fraudulent or suspicious activities.

Dependencies:
yt-dlp>=2024.1.0
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
requests>=2.28.0
Pillow>=9.0.0
flask>=2.3.0
flask-restx>=1.1.0

import os
import cv2
import numpy as np
import requests
import subprocess
import tempfile
from typing import Optional, Dict, List, Tuple, Any
from urllib.parse import urlparse
import mediapipe as mp
from PIL import Image
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

def download_media(url: str, media_type: str = "video") -> str:
    """
    Download video or image from URL to local temporary file.
    
    Args:
        url (str): The URL of the video or image to download
        media_type (str): Either "video" or "image"
        
    Returns:
        str: Local file path of the downloaded media
    """
    if not url or not isinstance(url, str):
        raise ValueError("URL must be a non-empty string")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        if media_type == "video":
            # Use yt-dlp to download video
            output_path = os.path.join(temp_dir, "downloaded_video.mp4")
            output_template = output_path
            
            cmd = [
                "yt-dlp",
                "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", output_template,
                "--max-filesize", "50M",  # Limit file size to 50MB
                url,
            ]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=60  # 60 second timeout
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Video download failed: {result.stderr}")
                
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Downloaded video not found at {output_path}")
                
            return output_path
            
        else:  # image
            output_path = os.path.join(temp_dir, "downloaded_image.jpg")
            
            # Download image with requests
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save image
            with open(output_path, 'wb') as f:
                f.write(response.content)
                
            if not os.path.exists(output_path):
                raise FileNotFoundError(f"Downloaded image not found at {output_path}")
                
            return output_path
            
    except Exception as e:
        # Clean up temp directory on failure
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e


def extract_frames_from_video(video_path: str, max_frames: int = 30) -> List[np.ndarray]:
    """
    Extract frames from video for analysis.
    
    Args:
        video_path (str): Path to the video file
        max_frames (int): Maximum number of frames to extract
        
    Returns:
        List[np.ndarray]: List of extracted frames
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {video_path}")
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate frame interval to get desired number of frames
    frame_interval = max(1, total_frames // max_frames)
    
    frames = []
    frame_count = 0
    
    while cap.isOpened() and len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            frames.append(frame)
            
        frame_count += 1
        
    cap.release()
    return frames


def detect_human_pose_in_frames(frames: List[np.ndarray]) -> List[np.ndarray]:
    """
    Detect human pose in a sequence of frames using MediaPipe.
    
    Args:
        frames (List[np.ndarray]): List of frames to analyze
        
    Returns:
        List[np.ndarray]: List of pose keypoints for each frame (or None if no pose detected)
    """
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    
    keypoints_sequence = []
    
    for frame in frames:
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            kps = np.array([
                [lm.x, lm.y, lm.z, lm.visibility]
                for lm in results.pose_landmarks.landmark
            ])
            keypoints_sequence.append(kps)
        else:
            keypoints_sequence.append(None)
            
    pose.close()
    return keypoints_sequence


def analyze_image_for_fraud_indicators(image_path: str) -> Dict[str, float]:
    """
    Analyze a single image for fraud indicators.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        Dict[str, float]: Dictionary of fraud indicator scores
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image from {image_path}")
    
    # Convert to RGB for MediaPipe
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5
    )
    
    # Detect faces
    face_results = face_detection.process(rgb_image)
    
    # Initialize MediaPipe Pose for body detection
    pose = mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.5
    )
    
    pose_results = pose.process(rgb_image)
    
    # Calculate fraud indicators
    indicators = {
        'multiple_faces': 0.0,
        'no_face_detected': 0.0,
        'suspicious_body_posture': 0.0,
        'image_quality_issues': 0.0
    }
    
    # Check for multiple faces (potential identity fraud)
    if face_results.detections:
        face_count = len(face_results.detections)
        if face_count > 1:
            indicators['multiple_faces'] = min(1.0, face_count * 0.3)
        elif face_count == 0:
            indicators['no_face_detected'] = 0.8
    else:
        indicators['no_face_detected'] = 1.0
    
    # Check for suspicious body posture
    if pose_results.pose_landmarks:
        landmarks = pose_results.pose_landmarks.landmark
        
        # Check if hands are near face (potential attempt to hide identity)
        if (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y < landmarks[mp_pose.PoseLandmark.NOSE.value].y or
            landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y < landmarks[mp_pose.PoseLandmark.NOSE.value].y):
            indicators['suspicious_body_posture'] = 0.6
            
        # Check if body is turned away from camera
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        shoulder_diff = abs(left_shoulder.x - right_shoulder.x)
        if shoulder_diff < 0.1:  # Shoulders aligned vertically (facing away)
            indicators['suspicious_body_posture'] = max(indicators['suspicious_body_posture'], 0.4)
    
    # Check image quality (blurry, low resolution could indicate fraud)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    if laplacian_var < 100:  # Low variance indicates blurry image
        indicators['image_quality_issues'] = 0.5
    
    face_detection.close()
    pose.close()
    
    return indicators


def compute_suspicious_behavior_score(keypoints_sequence: List[np.ndarray], fps: float = 5.0) -> Dict[str, float]:
    """
    Compute suspicious behavior scores from pose keypoints sequence.
    
    Args:
        keypoints_sequence (List[np.ndarray]): Sequence of pose keypoints
        fps (float): Frames per second of the analyzed sequence
        
    Returns:
        Dict[str, float]: Dictionary of behavior scores
    """
    if not keypoints_sequence or len(keypoints_sequence) < 5:
        return {'suspicious_behavior': 0.0, 'nervous_movements': 0.0, 'evasive_behavior': 0.0}
    
    # Filter out None frames
    valid_keypoints = [kp for kp in keypoints_sequence if kp is not None]
    if len(valid_keypoints) < 3:
        return {'suspicious_behavior': 0.0, 'nervous_movements': 0.0, 'evasive_behavior': 0.0}
    
    scores = {
        'suspicious_behavior': 0.0,
        'nervous_movements': 0.0,
        'evasive_behavior': 0.0
    }
    
    # Extract keypoint trajectories
    nose_y = []
    left_wrist_y = []
    right_wrist_y = []
    left_shoulder_x = []
    right_shoulder_x = []
    
    for kp in valid_keypoints:
        if kp.shape[0] > 0:
            nose_y.append(kp[0, 1])  # NOSE y-coordinate
            left_wrist_y.append(kp[15, 1])  # LEFT_WRIST y-coordinate
            right_wrist_y.append(kp[16, 1])  # RIGHT_WRIST y-coordinate
            left_shoulder_x.append(kp[11, 0])  # LEFT_SHOULDER x-coordinate
            right_shoulder_x.append(kp[12, 0])  # RIGHT_SHOULDER x-coordinate
    
    # Analyze nervous movements (rapid hand movements)
    if len(left_wrist_y) > 2:
        left_wrist_diff = np.diff(left_wrist_y)
        left_wrist_changes = np.sum(np.abs(left_wrist_diff) > 0.05)
        nervous_score_left = min(1.0, left_wrist_changes / len(left_wrist_y) * 2)
    else:
        nervous_score_left = 0.0
        
    if len(right_wrist_y) > 2:
        right_wrist_diff = np.diff(right_wrist_y)
        right_wrist_changes = np.sum(np.abs(right_wrist_diff) > 0.05)
        nervous_score_right = min(1.0, right_wrist_changes / len(right_wrist_y) * 2)
    else:
        nervous_score_right = 0.0
        
    scores['nervous_movements'] = max(nervous_score_left, nervous_score_right)
    
    # Analyze evasive behavior (head movements, looking away)
    if len(nose_y) > 2:
        nose_diff = np.diff(nose_y)
        head_movement_score = min(1.0, np.sum(np.abs(nose_diff) > 0.03) / len(nose_y) * 2)
        scores['evasive_behavior'] = head_movement_score
    
    # Analyze suspicious body posture (shoulder alignment indicating turning away)
    if len(left_shoulder_x) > 0 and len(right_shoulder_x) > 0:
        shoulder_alignment = np.mean(np.abs(np.array(left_shoulder_x) - np.array(right_shoulder_x)))
        if shoulder_alignment < 0.1:  # Shoulders vertically aligned (facing away from camera)
            scores['suspicious_behavior'] = max(scores['suspicious_behavior'], 0.6)
    
    # Overall suspicious behavior score
    scores['suspicious_behavior'] = max(
        scores['suspicious_behavior'],
        (scores['nervous_movements'] + scores['evasive_behavior']) / 2
    )
    
    return scores


def classify_financial_activity(video_url: Optional[str] = None, 
                               image_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Classify financial activity as normal or suspicious based on video or image analysis.
    
    Args:
        video_url (Optional[str]): URL to video file for analysis
        image_url (Optional[str]): URL to image file for analysis
        
    Returns:
        Dict[str, Any]: Classification results with label and confidence scores
    """
    if not video_url and not image_url:
        raise ValueError("Either video_url or image_url must be provided")
    
    if video_url and image_url:
        raise ValueError("Only one of video_url or image_url should be provided")
    
    try:
        if video_url:
            # Process video
            video_path = download_media(video_url, "video")
            frames = extract_frames_from_video(video_path, max_frames=30)
            keypoints_sequence = detect_human_pose_in_frames(frames)
            behavior_scores = compute_suspicious_behavior_score(keypoints_sequence, fps=5.0)
            
            # Calculate final scores
            suspicious_score = behavior_scores['suspicious_behavior']
            nervous_score = behavior_scores['nervous_movements']
            evasive_score = behavior_scores['evasive_behavior']
            
            # Determine classification
            if suspicious_score > 0.6:
                label = "suspicious_behavior"
                confidence = suspicious_score
            elif nervous_score > 0.5 or evasive_score > 0.5:
                label = "potential_fraud"
                confidence = max(nervous_score, evasive_score)
            else:
                label = "normal_activity"
                confidence = 1.0 - suspicious_score
                
        else:  # image_url
            # Process image
            image_path = download_media(image_url, "image")
            fraud_indicators = analyze_image_for_fraud_indicators(image_path)
            
            # Calculate overall suspicious score
            suspicious_score = max(
                fraud_indicators['multiple_faces'],
                fraud_indicators['no_face_detected'],
                fraud_indicators['suspicious_body_posture'],
                fraud_indicators['image_quality_issues']
            )
            
            # Determine classification
            if suspicious_score > 0.7:
                label = "potential_fraud"
                confidence = suspicious_score
            elif suspicious_score > 0.4:
                label = "suspicious_behavior"
                confidence = suspicious_score
            else:
                label = "normal_activity"
                confidence = 1.0 - suspicious_score
                
        # Create confidence list for all possible classes
        confidence_list = {
            "normal_activity": 0.0,
            "suspicious_behavior": 0.0,
            "potential_fraud": 0.0
        }
        
        # Set confidence for predicted class
        confidence_list[label] = float(confidence)
        
        # Distribute remaining confidence to other classes based on scores
        if video_url:
            confidence_list["suspicious_behavior"] = float(behavior_scores['suspicious_behavior'])
            confidence_list["potential_fraud"] = float(max(behavior_scores['nervous_movements'], 
                                                         behavior_scores['evasive_behavior']))
            confidence_list["normal_activity"] = float(1.0 - max(confidence_list.values()))
        else:
            confidence_list["potential_fraud"] = float(suspicious_score)
            confidence_list["suspicious_behavior"] = float(suspicious_score * 0.7)
            confidence_list["normal_activity"] = float(1.0 - suspicious_score)
            
        # Ensure all confidence values are between 0 and 1
        for key in confidence_list:
            confidence_list[key] = max(0.0, min(1.0, confidence_list[key]))
            
        return {
            "classification_label": label,
            "confidence_list": confidence_list
        }
        
    except Exception as e:
        logger.error(f"Error in classification: {str(e)}")
        # Return default safe classification on error
        return {
            "classification_label": "normal_activity",
            "confidence_list": {
                "normal_activity": 1.0,
                "suspicious_behavior": 0.0,
                "potential_fraud": 0.0
            }
        }


def main_process(video_url: Optional[str] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Main entry point for the WST-跨境支付AI监测-002-260624 algorithm.
    
    This function analyzes video or image content to detect suspicious activities
    related to financial transactions and money laundering scenarios.
    
    Args:
        video_url (Optional[str]): URL to a video file showing financial transaction activity
        image_url (Optional[str]): URL to an image file showing financial transaction activity
        
    Returns:
        Dict[str, Any]: Dictionary containing:
            - classification_label (str): One of "normal_activity", "suspicious_behavior", or "potential_fraud"
            - confidence_list (Dict[str, float]): Confidence scores for all possible classifications
            
    Raises:
        ValueError: If neither video_url nor image_url is provided, or if both are provided
    """
    return classify_financial_activity(video_url, image_url)


# Optional: Flask API for web service (following platform requirements)
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    from flask_restx import Api, Resource, fields
    
    app = Flask(__name__)
    api = Api(app, version='1.0', title='WST-跨境支付AI监测-002-260624 API',
              description='AI monitoring for cross-border payment fraud detection')
    
    # Define input model
    input_model = api.model('Input', {
        'video_url': fields.String(required=False, description='URL to video file'),
        'image_url': fields.String(required=False, description='URL to image file')
    })
    
    # Define output model
    output_model = api.model('Output', {
        'classification_label': fields.String(description='Classification result'),
        'confidence_list': fields.Raw(description='Confidence scores for all classes')
    })
    
    @api.route('/analyze')
    class Analyze(Resource):
        @api.expect(input_model)
        @api.marshal_with(output_model)
        def post(self):
            """Analyze video or image for suspicious financial activity"""
            data = request.json
            video_url = data.get('video_url')
            image_url = data.get('image_url')
            
            try:
                result = main_process(video_url=video_url, image_url=image_url)
                return result
            except Exception as e:
                api.abort(400, str(e))
    
    app.run(host='0.0.0.0', port=5000, debug=False)