# WST-跨境支付AI监测-042-260708_algorithm.py
# 
# 依赖清单（pip requirements 风格）：
# yt-dlp>=2024.1.0
# opencv-python>=4.8.0
# mediapipe>=0.10.0
# numpy>=1.24.0
# requests>=2.28.0
# flask>=2.3.0
# flask-restx>=1.1.0

import os
import cv2
import numpy as np
import subprocess
import requests
import tempfile
import logging
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    MP_AVAILABLE = True
except ImportError:
    MP_AVAILABLE = False
    logger.warning("MediaPipe not available, some features will be disabled")

def download_video(url: str, output_dir: str = "temp_videos") -> str:
    """从YouTube或其他视频平台下载视频。
    
    Args:
        url: 视频URL
        output_dir: 输出目录
        
    Returns:
        下载的视频文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    output_template = os.path.join(output_dir, "%(id)s.%(ext)s")
    
    # 检查是否为YouTube URL
    if "youtube.com" in url or "youtu.be" in url:
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", output_template,
            "--quiet",
            url,
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
            video_id = url.split("v=")[-1].split("&")[0] if "v=" in url else url.split("/")[-1]
            return os.path.join(output_dir, f"{video_id}.mp4")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            logger.error(f"Failed to download video: {e}")
            raise ValueError(f"Failed to download video from {url}")
    else:
        # 尝试直接下载
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path) or "video.mp4"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return filepath
        except Exception as e:
            logger.error(f"Failed to download video directly: {e}")
            raise ValueError(f"Failed to download video from {url}")


def download_image(url: str, output_dir: str = "temp_images") -> str:
    """下载图像文件。
    
    Args:
        url: 图像URL
        output_dir: 输出目录
        
    Returns:
        下载的图像文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) or "image.jpg"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        return filepath
    except Exception as e:
        logger.error(f"Failed to download image: {e}")
        raise ValueError(f"Failed to download image from {url}")


def extract_frames(video_path: str, sample_fps: int = 5) -> List[np.ndarray]:
    """从视频中提取帧。
    
    Args:
        video_path: 视频文件路径
        sample_fps: 采样帧率（每秒帧数）
        
    Returns:
        帧列表
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {video_path}")
    
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps == 0:
        original_fps = 30  # 默认帧率
        
    frame_interval = max(1, int(original_fps / sample_fps))
    frames = []
    idx = 0
    frame_count = 0
    
    while cap.isOpened() and frame_count < 100:  # 限制最大帧数
        ret, frame = cap.read()
        if not ret:
            break
        if idx % frame_interval == 0:
            frames.append(frame)
            frame_count += 1
        idx += 1
        
    cap.release()
    return frames


def detect_pose_sequence(frames: List[np.ndarray]) -> List[Optional[np.ndarray]]:
    """对帧序列进行人体姿态估计。
    
    Args:
        frames: 输入帧列表
        
    Returns:
        关键点序列列表，每个元素是33x4的numpy数组[x, y, z, visibility]或None
    """
    if not MP_AVAILABLE:
        return [None] * len(frames)
        
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    
    keypoints_sequence = []
    for frame in frames:
        try:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb)
            if results.pose_landmarks:
                kps = np.array([
                    [lm.x, lm.y, lm.z, lm.visibility]
                    for lm in results.pose_landmarks.landmark
                ])
                keypoints_sequence.append(kps)
            else:
                keypoints_sequence.append(None)
        except Exception as e:
            logger.warning(f"Failed to process frame: {e}")
            keypoints_sequence.append(None)
            
    pose.close()
    return keypoints_sequence


def compute_suspicious_cash_handling_score(keypoints_sequence: List[np.ndarray], fps: int) -> float:
    """计算可疑现金处理行为得分。
    
    特征：频繁的手部动作、手部在身体前方的重复运动、手部快速移动
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        可疑现金处理得分 (0-1)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
        
    # 提取左右手腕和手肘的关键点
    left_wrist_scores = []
    right_wrist_scores = []
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        # MediaPipe关键点索引：15-左腕, 16-右腕, 13-左肘, 14-右肘
        left_wrist = kps[15] if len(kps) > 15 else None
        right_wrist = kps[16] if len(kps) > 16 else None
        left_elbow = kps[13] if len(kps) > 13 else None
        right_elbow = kps[14] if len(kps) > 14 else None
        
        # 检查可见性
        if (left_wrist is not None and left_wrist[3] > 0.5 and 
            left_elbow is not None and left_elbow[3] > 0.5):
            # 计算手腕相对于肘部的位置（身体前方）
            wrist_elbow_dist = np.sqrt((left_wrist[0] - left_elbow[0])**2 + 
                                     (left_wrist[1] - left_elbow[1])**2)
            if wrist_elbow_dist > 0.1:  # 最小距离阈值
                left_wrist_scores.append(wrist_elbow_dist)
                
        if (right_wrist is not None and right_wrist[3] > 0.5 and 
            right_elbow is not None and right_elbow[3] > 0.5):
            wrist_elbow_dist = np.sqrt((right_wrist[0] - right_elbow[0])**2 + 
                                     (right_wrist[1] - right_elbow[1])**2)
            if wrist_elbow_dist > 0.1:
                right_wrist_scores.append(wrist_elbow_dist)
    
    # 计算手部运动的活跃度
    total_hand_activity = 0.0
    if left_wrist_scores:
        total_hand_activity += np.mean(left_wrist_scores) * 0.5
    if right_wrist_scores:
        total_hand_activity += np.mean(right_wrist_scores) * 0.5
        
    # 归一化到0-1范围
    score = min(total_hand_activity * 5, 1.0)
    return score


def compute_nervous_behavior_score(keypoints_sequence: List[np.ndarray], fps: int) -> float:
    """计算紧张行为得分。
    
    特征：头部快速移动、频繁的肩膀耸动、身体姿态不稳定
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        紧张行为得分 (0-1)
    """
    if len(keypoints_sequence) < 10:
        return 0.0
        
    # 提取头部（鼻子）和肩膀关键点
    head_positions = []
    shoulder_positions = []
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        # 关键点索引：0-鼻子, 11-左肩, 12-右肩
        nose = kps[0] if len(kps) > 0 else None
        left_shoulder = kps[11] if len(kps) > 11 else None
        right_shoulder = kps[12] if len(kps) > 12 else None
        
        if (nose is not None and nose[3] > 0.5 and 
            left_shoulder is not None and left_shoulder[3] > 0.5 and
            right_shoulder is not None and right_shoulder[3] > 0.5):
            head_positions.append([nose[0], nose[1]])
            shoulder_center = [(left_shoulder[0] + right_shoulder[0]) / 2,
                             (left_shoulder[1] + right_shoulder[1]) / 2]
            shoulder_positions.append(shoulder_center)
    
    if len(head_positions) < 5:
        return 0.0
        
    # 计算头部相对于肩膀的运动幅度
    head_movement_scores = []
    for i in range(1, len(head_positions)):
        head_dist = np.sqrt((head_positions[i][0] - head_positions[i-1][0])**2 +
                          (head_positions[i][1] - head_positions[i-1][1])**2)
        head_movement_scores.append(head_dist)
    
    avg_head_movement = np.mean(head_movement_scores) if head_movement_scores else 0.0
    
    # 计算肩膀的稳定性（耸肩频率）
    shoulder_movement_scores = []
    for i in range(1, len(shoulder_positions)):
        shoulder_dist = abs(shoulder_positions[i][1] - shoulder_positions[i-1][1])
        shoulder_movement_scores.append(shoulder_dist)
    
    avg_shoulder_movement = np.mean(shoulder_movement_scores) if shoulder_movement_scores else 0.0
    
    # 综合得分
    total_score = (avg_head_movement * 10 + avg_shoulder_movement * 5) / 2
    return min(total_score, 1.0)


def compute_unusual_body_movement_score(keypoints_sequence: List[np.ndarray], fps: int) -> float:
    """计算异常身体动作得分。
    
    特征：不自然的身体姿势、过度的身体旋转、异常的肢体伸展
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        异常身体动作得分 (0-1)
    """
    if len(keypoints_sequence) < 8:
        return 0.0
        
    unusual_posture_scores = []
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        # 检查关键身体部位的可见性
        required_points = [0, 11, 12, 13, 14, 15, 16, 23, 24]  # 头、肩、肘、腕、髋
        visible_points = sum(1 for idx in required_points if idx < len(kps) and kps[idx][3] > 0.5)
        
        if visible_points < len(required_points) * 0.7:  # 至少70%关键点可见
            continue
            
        # 计算身体对称性和姿势
        try:
            # 肩膀水平度
            left_shoulder = kps[11]
            right_shoulder = kps[12]
            shoulder_slope = abs(left_shoulder[1] - right_shoulder[1])
            
            # 手臂伸展度
            left_elbow = kps[13]
            left_wrist = kps[15]
            right_elbow = kps[14]
            right_wrist = kps[16]
            
            left_arm_extension = np.sqrt((left_wrist[0] - left_shoulder[0])**2 +
                                       (left_wrist[1] - left_shoulder[1])**2)
            right_arm_extension = np.sqrt((right_wrist[0] - right_shoulder[0])**2 +
                                        (right_wrist[1] - right_shoulder[1])**2)
            
            # 身体直立度
            left_hip = kps[23]
            right_hip = kps[24]
            hip_shoulder_center_x = (left_shoulder[0] + right_shoulder[0] + left_hip[0] + right_hip[0]) / 4
            hip_shoulder_center_y = (left_shoulder[1] + right_shoulder[1] + left_hip[1] + right_hip[1]) / 4
            
            # 异常姿势得分（基于不自然的角度和位置）
            posture_score = (shoulder_slope * 2 + 
                           abs(left_arm_extension - right_arm_extension) * 3 +
                           abs(hip_shoulder_center_x - 0.5) * 2)
            
            unusual_posture_scores.append(posture_score)
            
        except (IndexError, ValueError):
            continue
    
    if not unusual_posture_scores:
        return 0.0
        
    avg_unusual_score = np.mean(unusual_posture_scores)
    return min(avg_unusual_score * 2, 1.0)


def classify_abnormal_behavior(keypoints_sequence: List[Optional[np.ndarray]], fps: int = 5) -> Dict[str, Any]:
    """对异常行为进行分类。
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        包含分类标签和置信度的字典
    """
    # 过滤无效帧
    valid_kps = [kp for kp in keypoints_sequence if kp is not None]
    if len(valid_kps) < 5:
        return {
            "classification_label": "normal",
            "confidence_list": [1.0, 0.0, 0.0, 0.0]
        }
    
    # 计算各类行为得分
    suspicious_cash_score = compute_suspicious_cash_handling_score(valid_kps, fps)
    nervous_score = compute_nervous_behavior_score(valid_kps, fps)
    unusual_movement_score = compute_unusual_body_movement_score(valid_kps, fps)
    
    # 归一化得分
    total_score = suspicious_cash_score + nervous_score + unusual_movement_score
    if total_score > 0:
        suspicious_cash_score_norm = suspicious_cash_score / total_score
        nervous_score_norm = nervous_score / total_score
        unusual_movement_score_norm = unusual_movement_score / total_score
        normal_score_norm = 0.0
    else:
        suspicious_cash_score_norm = 0.0
        nervous_score_norm = 0.0
        unusual_movement_score_norm = 0.0
        normal_score_norm = 1.0
    
    # 确定主要类别
    scores = {
        "suspicious_cash_handling": suspicious_cash_score_norm,
        "nervous_behavior": nervous_score_norm,
        "unusual_body_movement": unusual_movement_score_norm,
        "normal": normal_score_norm
    }
    
    best_label = max(scores, key=scores.get)
    
    # 构建置信度列表（按固定顺序）
    confidence_list = [
        scores["suspicious_cash_handling"],
        scores["nervous_behavior"],
        scores["unusual_body_movement"],
        scores["normal"]
    ]
    
    # 如果所有异常得分都很低，则归类为normal
    if (suspicious_cash_score < 0.3 and nervous_score < 0.3 and unusual_movement_score < 0.3):
        best_label = "normal"
        confidence_list = [0.0, 0.0, 0.0, 1.0]
    
    return {
        "classification_label": best_label,
        "confidence_list": confidence_list
    }


def process_image_for_abnormal_behavior(image_path: str) -> Dict[str, Any]:
    """处理单张图像进行异常行为检测。
    
    Args:
        image_path: 图像文件路径
        
    Returns:
        包含分类标签和置信度的字典
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Cannot read image: {image_path}")
            
        # 将单张图像作为一帧序列处理
        frames = [image]
        keypoints_sequence = detect_pose_sequence(frames)
        return classify_abnormal_behavior(keypoints_sequence, fps=1)
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return {
            "classification_label": "normal",
            "confidence_list": [0.0, 0.0, 0.0, 1.0]
        }


def main_process(video_url: Optional[str] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    """跨境支付AI监测异常行为分类主函数。
    
    基于视频或图像中的人体姿态分析，识别可能与金融犯罪相关的异常行为模式。
    适用于ATM监控、银行柜台监控、可疑交易场所监控等场景。
    
    Args:
        video_url: 视频URL（YouTube或其他视频平台）
        image_url: 图像URL
        
    Returns:
        包含以下字段的字典：
        - classification_label: 分类标签，可能值包括：
            - "suspicious_cash_handling": 可疑现金处理
            - "nervous_behavior": 紧张行为  
            - "unusual_body_movement": 异常身体动作
            - "normal": 正常行为
        - confidence_list: 四个类别的置信度列表，顺序对应上述标签
    """
    if not MP_AVAILABLE:
        return {
            "classification_label": "normal",
            "confidence_list": [0.0, 0.0, 0.0, 1.0]
        }
    
    try:
        if video_url:
            # 处理视频
            with tempfile.TemporaryDirectory() as temp_dir:
                video_path = download_video(video_url, temp_dir)
                frames = extract_frames(video_path, sample_fps=5)
                if not frames:
                    raise ValueError("No frames extracted from video")
                keypoints_sequence = detect_pose_sequence(frames)
                result = classify_abnormal_behavior(keypoints_sequence, fps=5)
                return result
                
        elif image_url:
            # 处理图像
            with tempfile.TemporaryDirectory() as temp_dir:
                image_path = download_image(image_url, temp_dir)
                result = process_image_for_abnormal_behavior(image_path)
                return result
                
        else:
            # 无有效输入
            return {
                "classification_label": "normal",
                "confidence_list": [0.0, 0.0, 0.0, 1.0]
            }
            
    except Exception as e:
        logger.error(f"Error in main_process: {e}")
        return {
            "classification_label": "normal",
            "confidence_list": [0.0, 0.0, 0.0, 1.0]
        }


# 可选：Flask Web API（符合平台规范）
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    from flask_restx import Api, Resource, fields
    
    app = Flask(__name__)
    api = Api(app, version='1.0', title='WST-跨境支付AI监测-042-260708 API',
              description='跨境支付AI监测异常行为分类服务')
    
    ns = api.namespace('classification', description='异常行为分类操作')
    
    classification_input = api.model('ClassificationInput', {
        'video_url': fields.String(required=False, description='视频URL'),
        'image_url': fields.String(required=False, description='图像URL')
    })
    
    classification_output = api.model('ClassificationOutput', {
        'classification_label': fields.String(description='分类标签'),
        'confidence_list': fields.List(fields.Float, description='置信度列表')
    })
    
    @ns.route('/')
    class Classification(Resource):
        @api.expect(classification_input)
        @api.marshal_with(classification_output)
        def post(self):
            """执行异常行为分类"""
            data = request.json
            video_url = data.get('video_url')
            image_url = data.get('image_url')
            return main_process(video_url=video_url, image_url=image_url)
    
    app.run(host='0.0.0.0', port=5000, debug=False)