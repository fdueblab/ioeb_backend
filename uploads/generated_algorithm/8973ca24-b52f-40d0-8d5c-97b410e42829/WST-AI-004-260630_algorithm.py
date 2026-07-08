# WST-跨境支付AI监测-004-260630_algorithm.py
#
# 依赖清单（pip requirements）：
# yt-dlp>=2024.1.0
# opencv-python>=4.8.0
# mediapipe>=0.10.0
# numpy>=1.24.0
# requests>=2.28.0
# flask>=2.3.0
# flask-restx>=1.1.0
# Pillow>=9.0.0

import os
import cv2
import numpy as np
import requests
import subprocess
import tempfile
from PIL import Image
from typing import List, Dict, Optional, Tuple, Any
import logging

# 可选的Web层导入（用于Flask服务）
try:
    from flask import Flask, request, jsonify
    from flask_restx import Api, Resource, fields
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MediaPipe导入
try:
    import mediapipe as mp
    mp_pose = mp.solutions.pose
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe not available, pose detection will be disabled")


def download_video(video_url: str, output_dir: str = "temp_videos") -> str:
    """
    从YouTube或其他支持的平台下载视频。
    
    Args:
        video_url (str): 视频URL
        output_dir (str): 输出目录
        
    Returns:
        str: 下载的视频文件路径
    """
    if not video_url or not video_url.strip():
        raise ValueError("Video URL cannot be empty")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 创建临时文件名
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False, dir=output_dir) as tmp_file:
        temp_path = tmp_file.name
    
    try:
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", temp_path,
            "--max-filesize", "50M",  # 限制文件大小
            video_url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise RuntimeError(f"Video download failed: {result.stderr}")
        
        return temp_path
    except subprocess.TimeoutExpired:
        raise RuntimeError("Video download timeout")
    except Exception as e:
        if os.path.exists(temp_path):
            os.unlink(temp_path)
        raise RuntimeError(f"Video download error: {str(e)}")


def download_image(image_url: str) -> np.ndarray:
    """
    下载图片并转换为numpy数组。
    
    Args:
        image_url (str): 图片URL
        
    Returns:
        np.ndarray: 图片的numpy数组表示
    """
    if not image_url or not image_url.strip():
        raise ValueError("Image URL cannot be empty")
    
    try:
        response = requests.get(image_url, timeout=30)
        response.raise_for_status()
        
        # 使用PIL打开图片并转换为RGB
        image = Image.open(requests.get(image_url, stream=True).raw)
        image = image.convert('RGB')
        image_array = np.array(image)
        
        # 如果是RGBA，转换为RGB
        if image_array.shape[2] == 4:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
        
        return image_array
    except Exception as e:
        raise RuntimeError(f"Image download error: {str(e)}")


def extract_frames(video_path: str, max_frames: int = 30, sample_fps: int = 5) -> List[np.ndarray]:
    """
    从视频中提取帧。
    
    Args:
        video_path (str): 视频文件路径
        max_frames (int): 最大提取帧数
        sample_fps (int): 采样帧率
        
    Returns:
        List[np.ndarray]: 提取的帧列表
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video file")
    
    try:
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        if original_fps <= 0:
            original_fps = 30.0
        
        frame_interval = max(1, int(original_fps / sample_fps))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames_to_extract = min(max_frames, total_frames // frame_interval + 1)
        
        frames = []
        idx = 0
        frames_extracted = 0
        
        while cap.isOpened() and frames_extracted < frames_to_extract:
            ret, frame = cap.read()
            if not ret:
                break
            if idx % frame_interval == 0:
                frames.append(frame)
                frames_extracted += 1
            idx += 1
    finally:
        cap.release()
    
    return frames


def detect_pose_sequence(frames: List[np.ndarray]) -> List[Optional[np.ndarray]]:
    """
    对帧序列进行人体姿态检测。
    
    Args:
        frames (List[np.ndarray]): 输入帧列表
        
    Returns:
        List[Optional[np.ndarray]]: 每帧的姿态关键点数组，如果未检测到则为None
    """
    if not MEDIAPIPE_AVAILABLE:
        logger.warning("MediaPipe not available, returning empty pose data")
        return [None] * len(frames)
    
    pose = mp_pose.Pose(
        static_image_mode=False,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    
    keypoints_sequence = []
    try:
        for frame in frames:
            if frame is None or frame.size == 0:
                keypoints_sequence.append(None)
                continue
                
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
    finally:
        pose.close()
    
    return keypoints_sequence


def detect_pose_single_image(image: np.ndarray) -> Optional[np.ndarray]:
    """
    对单张图片进行人体姿态检测。
    
    Args:
        image (np.ndarray): 输入图片
        
    Returns:
        Optional[np.ndarray]: 姿态关键点数组，如果未检测到则为None
    """
    if not MEDIAPIPE_AVAILABLE:
        logger.warning("MediaPipe not available, returning empty pose data")
        return None
    
    pose = mp_pose.Pose(
        static_image_mode=True,
        model_complexity=1,
        min_detection_confidence=0.5,
    )
    
    try:
        rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb)
        if results.pose_landmarks:
            kps = np.array([
                [lm.x, lm.y, lm.z, lm.visibility]
                for lm in results.pose_landmarks.landmark
            ])
            return kps
        else:
            return None
    finally:
        pose.close()


def compute_suspicious_cash_handling_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算可疑现金处理行为得分。
    
    特征：双手在身体前方频繁移动，手腕位置异常，头部频繁左右查看。
    
    Args:
        keypoints_sequence (List[np.ndarray]): 姿态关键点序列
        fps (int): 帧率
        
    Returns:
        float: 可疑现金处理行为得分 (0.0-1.0)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
    
    scores = []
    
    for kps in keypoints_sequence:
        if kps is None or len(kps) < 17:
            scores.append(0.0)
            continue
        
        # 检查关键点可见性
        left_wrist = kps[15] if len(kps) > 15 else None
        right_wrist = kps[16] if len(kps) > 16 else None
        left_elbow = kps[13] if len(kps) > 13 else None
        right_elbow = kps[14] if len(kps) > 14 else None
        nose = kps[0] if len(kps) > 0 else None
        left_shoulder = kps[11] if len(kps) > 11 else None
        right_shoulder = kps[12] if len(kps) > 12 else None
        
        score = 0.0
        visible_count = 0
        
        # 检查手腕是否在身体前方（y坐标较小，表示靠近摄像头）
        if (left_wrist is not None and left_wrist[3] > 0.5 and 
            left_shoulder is not None and left_shoulder[3] > 0.5):
            if left_wrist[1] < left_shoulder[1] + 0.1:  # 手腕在肩膀下方不远
                score += 0.3
            visible_count += 1
            
        if (right_wrist is not None and right_wrist[3] > 0.5 and 
            right_shoulder is not None and right_shoulder[3] > 0.5):
            if right_wrist[1] < right_shoulder[1] + 0.1:
                score += 0.3
            visible_count += 1
        
        # 检查头部是否频繁左右移动（需要序列分析）
        # 简化：检查头部是否偏向一侧
        if nose is not None and nose[3] > 0.5 and left_shoulder is not None and right_shoulder is not None:
            shoulder_mid_x = (left_shoulder[0] + right_shoulder[0]) / 2
            if abs(nose[0] - shoulder_mid_x) > 0.1:  # 头部明显偏向一侧
                score += 0.2
            visible_count += 1
        
        if visible_count > 0:
            score = min(1.0, score / visible_count * 2.0)
        scores.append(score)
    
    # 返回平均得分
    return np.mean(scores) if scores else 0.0


def compute_atm_suspicious_behavior_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算ATM可疑操作行为得分。
    
    特征：身体前倾过度，频繁查看周围，手部动作异常。
    
    Args:
        keypoints_sequence (List[np.ndarray]): 姿态关键点序列
        fps (int): 帧率
        
    Returns:
        float: ATM可疑行为得分 (0.0-1.0)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
    
    scores = []
    
    for kps in keypoints_sequence:
        if kps is None or len(kps) < 25:
            scores.append(0.0)
            continue
        
        nose = kps[0] if len(kps) > 0 else None
        left_shoulder = kps[11] if len(kps) > 11 else None
        right_shoulder = kps[12] if len(kps) > 12 else None
        left_hip = kps[23] if len(kps) > 23 else None
        right_hip = kps[24] if len(kps) > 24 else None
        
        score = 0.0
        visible_count = 0
        
        # 检查身体前倾（头部相对于髋部的位置）
        if (nose is not None and nose[3] > 0.5 and 
            left_hip is not None and left_hip[3] > 0.5 and
            right_hip is not None and right_hip[3] > 0.5):
            hip_mid_y = (left_hip[1] + right_hip[1]) / 2
            if nose[1] < hip_mid_y - 0.2:  # 头部明显在髋部上方较远位置（前倾）
                score += 0.4
            visible_count += 1
        
        # 检查肩膀是否紧张（肩膀高度异常）
        if (left_shoulder is not None and left_shoulder[3] > 0.5 and
            right_shoulder is not None and right_shoulder[3] > 0.5):
            if left_shoulder[1] < 0.3 and right_shoulder[1] < 0.3:  # 肩膀位置较高
                score += 0.3
            visible_count += 1
        
        if visible_count > 0:
            score = min(1.0, score / visible_count * 2.0)
        scores.append(score)
    
    return np.mean(scores) if scores else 0.0


def compute_money_laundering_indicators_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算洗钱指标行为得分。
    
    特征：多人交互异常，物品传递行为，紧张的身体语言。
    
    Args:
        keypoints_sequence (List[np.ndarray]): 姿态关键点序列
        fps (int): 帧率
        
    Returns:
        float: 洗钱指标行为得分 (0.0-1.0)
    """
    # 由于MediaPipe Pose主要针对单人，这里简化处理
    # 主要检测紧张的身体语言
    
    if len(keypoints_sequence) < 5:
        return 0.0
    
    scores = []
    
    for kps in keypoints_sequence:
        if kps is None or len(kps) < 17:
            scores.append(0.0)
            continue
        
        left_wrist = kps[15] if len(kps) > 15 else None
        right_wrist = kps[16] if len(kps) > 16 else None
        left_elbow = kps[13] if len(kps) > 13 else None
        right_elbow = kps[14] if len(kps) > 14 else None
        nose = kps[0] if len(kps) > 0 else None
        
        score = 0.0
        visible_count = 0
        
        # 检查手部是否紧张（肘部弯曲角度）
        if (left_elbow is not None and left_elbow[3] > 0.5 and
            left_wrist is not None and left_wrist[3] > 0.5):
            # 简化：检查手腕是否靠近身体
            if abs(left_wrist[0] - 0.5) < 0.2 and left_wrist[1] > 0.4:
                score += 0.3
            visible_count += 1
            
        if (right_elbow is not None and right_elbow[3] > 0.5 and
            right_wrist is not None and right_wrist[3] > 0.5):
            if abs(right_wrist[0] - 0.5) < 0.2 and right_wrist[1] > 0.4:
                score += 0.3
            visible_count += 1
        
        # 检查头部是否低垂（紧张表现）
        if nose is not None and nose[3] > 0.5:
            if nose[1] > 0.3:  # 头部位置较低
                score += 0.2
            visible_count += 1
        
        if visible_count > 0:
            score = min(1.0, score / visible_count * 2.0)
        scores.append(score)
    
    return np.mean(scores) if scores else 0.0


def classify_suspicious_behavior(keypoints_data: List[Optional[np.ndarray]], is_video: bool = True) -> Dict[str, Any]:
    """
    基于姿态关键点数据分类可疑金融行为。
    
    Args:
        keypoints_data (List[Optional[np.ndarray]]): 姿态关键点数据
        is_video (bool): 是否为视频数据（影响分析策略）
        
    Returns:
        Dict[str, Any]: 分类结果，包含标签和置信度列表
    """
    if not keypoints_data:
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "suspicious_cash_handling": 0.0,
                "atm_suspicious_behavior": 0.0,
                "money_laundering_indicators": 0.0,
                "normal_behavior": 1.0
            }
        }
    
    # 过滤无效帧
    valid_keypoints = [kp for kp in keypoints_data if kp is not None and len(kp) >= 17]
    if len(valid_keypoints) < 3:
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "suspicious_cash_handling": 0.0,
                "atm_suspicious_behavior": 0.0,
                "money_laundering_indicators": 0.0,
                "normal_behavior": 1.0
            }
        }
    
    fps = 5 if is_video else 1
    
    # 计算各类行为得分
    cash_score = compute_suspicious_cash_handling_score(valid_keypoints, fps)
    atm_score = compute_atm_suspicious_behavior_score(valid_keypoints, fps)
    laundering_score = compute_money_laundering_indicators_score(valid_keypoints, fps)
    
    # 计算正常行为得分（反向）
    max_suspicious_score = max(cash_score, atm_score, laundering_score)
    normal_score = max(0.0, 1.0 - max_suspicious_score)
    
    confidence_list = {
        "suspicious_cash_handling": float(cash_score),
        "atm_suspicious_behavior": float(atm_score),
        "money_laundering_indicators": float(laundering_score),
        "normal_behavior": float(normal_score)
    }
    
    # 确定最高置信度的标签
    classification_label = max(confidence_list, key=confidence_list.get)
    
    return {
        "classification_label": classification_label,
        "confidence_list": confidence_list
    }


def main_process(video_url: str, image_url: str) -> Dict[str, Any]:
    """
    跨境支付AI监测主处理函数。
    
    该函数接收视频URL和图片URL，分析其中的可疑金融行为，
    返回分类标签和各类行为的置信度。
    
    Args:
        video_url (str): 视频URL，可以为空字符串
        image_url (str): 图片URL，可以为空字符串
        
    Returns:
        Dict[str, Any]: 包含classification_label和confidence_list的字典
    """
    # 输入验证
    if not video_url and not image_url:
        raise ValueError("Either video_url or image_url must be provided")
    
    keypoints_data = []
    is_video = False
    
    try:
        # 优先处理视频（如果提供了）
        if video_url and video_url.strip():
            video_path = None
            try:
                video_path = download_video(video_url)
                frames = extract_frames(video_path, max_frames=30)
                if frames:
                    keypoints_data = detect_pose_sequence(frames)
                    is_video = True
            finally:
                # 清理临时文件
                if video_path and os.path.exists(video_path):
                    os.unlink(video_path)
        
        # 如果没有视频或视频处理失败，处理图片
        elif image_url and image_url.strip():
            try:
                image = download_image(image_url)
                keypoints = detect_pose_single_image(image)
                if keypoints is not None:
                    keypoints_data = [keypoints]
                else:
                    keypoints_data = []
            except Exception as e:
                logger.warning(f"Image processing failed: {str(e)}")
                keypoints_data = []
        
        # 执行分类
        result = classify_suspicious_behavior(keypoints_data, is_video=is_video)
        return result
        
    except Exception as e:
        logger.error(f"Error in main_process: {str(e)}")
        # 返回默认正常行为结果
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "suspicious_cash_handling": 0.0,
                "atm_suspicious_behavior": 0.0,
                "money_laundering_indicators": 0.0,
                "normal_behavior": 1.0
            }
        }


# 可选的Web服务层（用于MCP服务封装）
if FLASK_AVAILABLE:
    app = Flask(__name__)
    api = Api(app, version='1.0', title='WST-跨境支付AI监测-004-260630 API',
              description='跨境支付AI监测服务')
    
    ns = api.namespace('detection', description='Suspicious behavior detection operations')
    
    detection_model = api.model('DetectionInput', {
        'video_url': fields.String(required=False, description='Video URL'),
        'image_url': fields.String(required=False, description='Image URL')
    })
    
    @ns.route('/analyze')
    class BehaviorDetection(Resource):
        @ns.doc('analyze_behavior')
        @ns.expect(detection_model)
        def post(self):
            """分析视频或图片中的可疑金融行为"""
            try:
                data = request.json
                video_url = data.get('video_url', '')
                image_url = data.get('image_url', '')
                
                result = main_process(video_url, image_url)
                return result, 200
            except Exception as e:
                return {'error': str(e)}, 400

if __name__ == '__main__':
    # 简单的测试
    if FLASK_AVAILABLE:
        app.run(debug=False, host='0.0.0.0', port=5000)
    else:
        print("Flask not available. Run with proper dependencies for web service.")