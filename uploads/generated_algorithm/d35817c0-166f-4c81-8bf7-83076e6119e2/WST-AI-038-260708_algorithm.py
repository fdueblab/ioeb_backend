'''
跨境支付AI监测 - 视频异常行为识别算法

该算法用于金融风控和反洗钱场景中的可疑行为监测，
通过分析视频中的人体动作来识别潜在的异常行为模式。

Dependencies:
yt-dlp>=2024.1.0
opencv-python>=4.8.0
mediapipe>=0.10.0
numpy>=1.24.0
requests>=2.28.0
'''
import subprocess
import os
import cv2
import numpy as np
import mediapipe as mp
import requests
from typing import List, Dict, Optional, Tuple, Any
import tempfile
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose

def download_video(url: str, output_dir: str = "temp_videos") -> str:
    """
    从YouTube或其他支持的平台下载视频。
    
    Args:
        url: 视频URL
        output_dir: 输出目录
        
    Returns:
        下载的视频文件路径
    """
    os.makedirs(output_dir, exist_ok=True)
    temp_dir = tempfile.mkdtemp(dir=output_dir)
    output_template = os.path.join(temp_dir, "%(id)s.%(ext)s")
    
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
        "--merge-output-format", "mp4",
        "--no-warnings",
        "--quiet",
        "-o", output_template,
        url,
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
        # 获取下载的文件
        for file in os.listdir(temp_dir):
            if file.endswith('.mp4'):
                return os.path.join(temp_dir, file)
        raise ValueError("No video file found after download")
    except subprocess.TimeoutExpired:
        raise RuntimeError("Video download timeout")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Video download failed: {e.stderr}")

def download_image(url: str) -> str:
    """
    下载图片到临时文件。
    
    Args:
        url: 图片URL
        
    Returns:
        临时图片文件路径
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "temp_image.jpg")
        
        with open(temp_file, 'wb') as f:
            f.write(response.content)
            
        return temp_file
    except Exception as e:
        raise RuntimeError(f"Image download failed: {str(e)}")

def extract_frames(video_path: str, sample_fps: int = 5) -> List[np.ndarray]:
    """
    从视频中提取帧。
    
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
    if original_fps <= 0:
        original_fps = 30.0
    
    frame_interval = max(1, int(original_fps / sample_fps))
    frames = []
    idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if idx % frame_interval == 0:
            frames.append(frame)
        idx += 1
        # 限制最大帧数以避免内存问题
        if len(frames) >= 100:
            break
    
    cap.release()
    return frames

def detect_pose_sequence(frames: List[np.ndarray]) -> List[Optional[np.ndarray]]:
    """
    对帧序列进行人体姿态检测。
    
    Args:
        frames: 输入帧列表
        
    Returns:
        关键点序列列表，每个元素为33x4的数组[x, y, z, visibility]或None
    """
    if not frames:
        return []
    
    pose = mp_pose.Pose(
        static_image_mode=len(frames) == 1,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    )
    
    keypoints_sequence = []
    for frame in frames:
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
    
    pose.close()
    return keypoints_sequence

def compute_arm_flapping_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算手臂拍打行为的置信度分数。
    
    Args:
        keypoints_sequence: 有效关键点序列
        fps: 帧率
        
    Returns:
        置信度分数 [0, 1]
    """
    if len(keypoints_sequence) < 5:
        return 0.0
    
    # 提取左右手腕的y坐标
    left_wrist_y = []
    right_wrist_y = []
    
    for kps in keypoints_sequence:
        if kps[15][3] > 0.5:  # LEFT_WRIST visibility
            left_wrist_y.append(kps[15][1])
        if kps[16][3] > 0.5:  # RIGHT_WRIST visibility
            right_wrist_y.append(kps[16][1])
    
    scores = []
    for wrist_y in [left_wrist_y, right_wrist_y]:
        if len(wrist_y) < 5:
            continue
        
        # 计算一阶差分
        diff = np.diff(wrist_y)
        # 计算零交叉次数（方向变化）
        zero_crossings = np.where(np.diff(np.sign(diff)))[0]
        frequency = len(zero_crossings) / (len(wrist_y) / fps)
        
        # 计算运动幅度
        amplitude = np.std(wrist_y)
        
        # 综合评分
        if frequency > 1.0 and amplitude > 0.05:
            score = min(1.0, (frequency / 3.0) * (amplitude / 0.1))
            scores.append(score)
    
    return max(scores) if scores else 0.0

def compute_head_banging_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算头部摇晃行为的置信度分数。
    
    Args:
        keypoints_sequence: 有效关键点序列
        fps: 帧率
        
    Returns:
        置信度分数 [0, 1]
    """
    if len(keypoints_sequence) < 5:
        return 0.0
    
    nose_y = []
    shoulder_center_y = []
    
    for kps in keypoints_sequence:
        if kps[0][3] > 0.5:  # NOSE visibility
            nose_y.append(kps[0][1])
        if kps[11][3] > 0.5 and kps[12][3] > 0.5:  # Both shoulders visible
            shoulder_center_y.append((kps[11][1] + kps[12][1]) / 2)
    
    if len(nose_y) < 5 or len(shoulder_center_y) < 5:
        return 0.0
    
    # 计算头部相对于肩膀的运动
    relative_movement = []
    for i in range(min(len(nose_y), len(shoulder_center_y))):
        relative_movement.append(nose_y[i] - shoulder_center_y[i])
    
    if len(relative_movement) < 5:
        return 0.0
    
    # 计算频率和幅度
    diff = np.diff(relative_movement)
    zero_crossings = np.where(np.diff(np.sign(diff)))[0]
    frequency = len(zero_crossings) / (len(relative_movement) / fps)
    amplitude = np.std(relative_movement)
    
    if frequency > 0.8 and amplitude > 0.03:
        score = min(1.0, (frequency / 2.0) * (amplitude / 0.05))
        return score
    
    return 0.0

def compute_spinning_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """
    计算旋转行为的置信度分数。
    
    Args:
        keypoints_sequence: 有效关键点序列
        fps: 帧率
        
    Returns:
        置信度分数 [0, 1]
    """
    if len(keypoints_sequence) < 10:
        return 0.0
    
    angles = []
    for kps in keypoints_sequence:
        if kps[11][3] > 0.5 and kps[12][3] > 0.5:  # Both shoulders visible
            # 计算肩膀连线的角度
            dx = kps[12][0] - kps[11][0]  # RIGHT_SHOULDER - LEFT_SHOULDER
            dy = kps[12][1] - kps[11][1]
            angle = np.arctan2(dy, dx)
            angles.append(angle)
    
    if len(angles) < 10:
        return 0.0
    
    # 计算角度变化
    angle_diffs = np.diff(angles)
    # 处理角度环绕（-π到π）
    angle_diffs = np.arctan2(np.sin(angle_diffs), np.cos(angle_diffs))
    
    total_rotation = np.abs(np.sum(angle_diffs))
    rotation_speed = total_rotation / (len(angles) / fps)
    
    # 评分：总旋转角度和速度
    if total_rotation > 1.0 and rotation_speed > 0.5:
        score = min(1.0, (total_rotation / 3.0) * (rotation_speed / 2.0))
        return score
    
    return 0.0

def classify_action(keypoints_sequence: List[np.ndarray], fps: int = 5) -> Dict[str, Any]:
    """
    对关键点序列进行动作分类。
    
    Args:
        keypoints_sequence: 有效关键点序列
        fps: 帧率
        
    Returns:
        包含分类标签和置信度列表的字典
    """
    if len(keypoints_sequence) < 5:
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "arm_flapping": 0.0,
                "head_banging": 0.0,
                "spinning": 0.0,
                "normal_behavior": 1.0
            }
        }
    
    # 计算各类别分数
    arm_flapping_score = compute_arm_flapping_score(keypoints_sequence, fps)
    head_banging_score = compute_head_banging_score(keypoints_sequence, fps)
    spinning_score = compute_spinning_score(keypoints_sequence, fps)
    
    # 正常行为分数（基于最大异常分数的反向）
    max_anomaly_score = max(arm_flapping_score, head_banging_score, spinning_score)
    normal_score = max(0.0, 1.0 - max_anomaly_score)
    
    confidence_list = {
        "arm_flapping": float(arm_flapping_score),
        "head_banging": float(head_banging_score),
        "spinning": float(spinning_score),
        "normal_behavior": float(normal_score)
    }
    
    # 选择最高置信度的标签
    best_label = max(confidence_list, key=confidence_list.get)
    
    return {
        "classification_label": best_label,
        "confidence_list": confidence_list
    }

def process_image_file(image_path: str) -> Dict[str, Any]:
    """
    处理单张图片。
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        分类结果
    """
    try:
        frame = cv2.imread(image_path)
        if frame is None:
            raise ValueError("Failed to read image")
        
        frames = [frame]
        keypoints_sequence = detect_pose_sequence(frames)
        valid_kps = [kp for kp in keypoints_sequence if kp is not None]
        
        if not valid_kps:
            return {
                "classification_label": "normal_behavior",
                "confidence_list": {
                    "arm_flapping": 0.0,
                    "head_banging": 0.0,
                    "spinning": 0.0,
                    "normal_behavior": 1.0
                }
            }
        
        return classify_action(valid_kps, fps=1)
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "arm_flapping": 0.0,
                "head_banging": 0.0,
                "spinning": 0.0,
                "normal_behavior": 1.0
            }
        }

def process_video_file(video_path: str) -> Dict[str, Any]:
    """
    处理视频文件。
    
    Args:
        video_path: 视频文件路径
        
    Returns:
        分类结果
    """
    try:
        frames = extract_frames(video_path, sample_fps=5)
        if not frames:
            raise ValueError("No frames extracted from video")
        
        keypoints_sequence = detect_pose_sequence(frames)
        valid_kps = [kp for kp in keypoints_sequence if kp is not None]
        
        if not valid_kps:
            return {
                "classification_label": "normal_behavior",
                "confidence_list": {
                    "arm_flapping": 0.0,
                    "head_banging": 0.0,
                    "spinning": 0.0,
                    "normal_behavior": 1.0
                }
            }
        
        return classify_action(valid_kps, fps=5)
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "arm_flapping": 0.0,
                "head_banging": 0.0,
                "spinning": 0.0,
                "normal_behavior": 1.0
            }
        }

def main_process(video_url: Optional[str] = None, image_url: Optional[str] = None) -> Dict[str, Any]:
    """
    主处理函数，用于跨境支付AI监测中的异常行为识别。
    
    Args:
        video_url: 视频URL（YouTube或其他支持的平台）
        image_url: 图片URL
        
    Returns:
        包含classification_label和confidence_list的字典
    """
    if not video_url and not image_url:
        raise ValueError("Either video_url or image_url must be provided")
    
    if video_url and image_url:
        raise ValueError("Only one of video_url or image_url should be provided")
    
    temp_files = []
    try:
        if video_url:
            # 处理视频
            video_path = download_video(video_url)
            temp_files.append(os.path.dirname(video_path))
            result = process_video_file(video_path)
        else:
            # 处理图片
            image_path = download_image(image_url)
            temp_files.append(os.path.dirname(image_path))
            result = process_image_file(image_path)
        
        return result
        
    except Exception as e:
        logger.error(f"Main process error: {str(e)}")
        return {
            "classification_label": "normal_behavior",
            "confidence_list": {
                "arm_flapping": 0.0,
                "head_banging": 0.0,
                "spinning": 0.0,
                "normal_behavior": 1.0
            }
        }
    finally:
        # 清理临时文件
        for temp_dir in temp_files:
            try:
                import shutil
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(f"Failed to clean temp directory {temp_dir}: {str(e)}")

# Web API部分（可选）
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        # 命令行测试
        test_url = sys.argv[1]
        if test_url.endswith(('.jpg', '.jpeg', '.png')):
            result = main_process(image_url=test_url)
        else:
            result = main_process(video_url=test_url)
        print(result)
    else:
        print("Usage: python script.py <video_url_or_image_url>")