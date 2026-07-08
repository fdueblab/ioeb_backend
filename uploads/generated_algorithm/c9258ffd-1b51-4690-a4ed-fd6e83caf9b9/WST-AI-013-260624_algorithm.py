import os
import subprocess
import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Optional, Tuple, Any
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mp_pose = mp.solutions.pose

def download_video(video_url: str, output_dir: str = "temp_videos") -> str:
    """从URL下载视频文件。
    
    Args:
        video_url: 视频URL地址
        output_dir: 视频保存目录
        
    Returns:
        下载的视频文件路径
        
    Raises:
        subprocess.CalledProcessError: 视频下载失败
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        video_id = video_url.split("v=")[-1].split("&")[0] if "v=" in video_url else "video"
        output_path = os.path.join(output_dir, f"{video_id}.mp4")
        
        # 检查文件是否已存在
        if os.path.exists(output_path):
            return output_path
            
        cmd = [
            "yt-dlp",
            "-f", "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", output_path,
            video_url,
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output_path
    except Exception as e:
        logger.error(f"视频下载失败: {e}")
        raise

def extract_frames(video_path: str, sample_fps: int = 5) -> List[np.ndarray]:
    """从视频中提取帧。
    
    Args:
        video_path: 视频文件路径
        sample_fps: 采样帧率（每秒帧数）
        
    Returns:
        提取的帧列表
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")
        
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    if original_fps == 0:
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
    """检测视频帧序列中的人体姿态关键点。
    
    Args:
        frames: 视频帧列表
        
    Returns:
        关键点序列列表，每个元素为33x4的数组[x, y, z, visibility]或None
    """
    pose = mp_pose.Pose(
        static_image_mode=False,
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

def compute_suspicious_behavior_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """计算可疑行为分数。
    
    可疑行为特征：
    1. 频繁的头部转动（查看周围环境）
    2. 手部遮挡面部区域
    3. 身体姿态不稳定或异常
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        可疑行为分数 (0.0-1.0)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
        
    # 计算头部转动频率（基于鼻子关键点的水平移动）
    nose_x_coords = []
    for kps in keypoints_sequence:
        if kps is not None and kps[0][3] > 0.5:  # NOSE visibility
            nose_x_coords.append(kps[0][0])
    
    if len(nose_x_coords) < 3:
        return 0.0
        
    # 计算水平方向的变化频率
    x_diffs = np.diff(nose_x_coords)
    direction_changes = np.sum(np.abs(np.diff(np.sign(x_diffs))) > 0)
    head_turning_freq = direction_changes / (len(nose_x_coords) / fps)
    
    # 手部遮挡面部检测
    face_cover_score = 0.0
    face_cover_count = 0
    total_valid_frames = 0
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        total_valid_frames += 1
        # 检查手腕是否在面部区域内
        # 面部区域：x方向相近，y方向手腕高于肩膀
        if (kps[15][3] > 0.5 and kps[16][3] > 0.5 and  # 手腕可见
            kps[11][3] > 0.5 and kps[12][3] > 0.5):   # 肩膀可见
            
            # 计算面部中心（鼻子）
            face_x = kps[0][0]
            face_y = kps[0][1]
            
            # 手腕位置
            left_wrist_x, left_wrist_y = kps[15][0], kps[15][1]
            right_wrist_x, right_wrist_y = kps[16][0], kps[16][1]
            
            # 检查手腕是否接近面部
            left_face_dist = np.sqrt((left_wrist_x - face_x)**2 + (left_wrist_y - face_y)**2)
            right_face_dist = np.sqrt((right_wrist_x - face_x)**2 + (right_wrist_y - face_y)**2)
            
            # 如果手腕距离面部很近且位置较高（遮挡）
            if (left_face_dist < 0.2 or right_face_dist < 0.2) and (left_wrist_y < face_y or right_wrist_y < face_y):
                face_cover_count += 1
    
    if total_valid_frames > 0:
        face_cover_score = face_cover_count / total_valid_frames
    
    # 综合评分
    head_turning_score = min(head_turning_freq / 2.0, 1.0)  # 正常对话头部转动约1-2次/秒
    suspicious_score = 0.6 * head_turning_score + 0.4 * face_cover_score
    
    return min(suspicious_score, 1.0)

def compute_normal_transaction_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """计算正常交易行为分数。
    
    正常交易特征：
    1. 身体姿态稳定
    2. 手部动作集中在操作区域（如ATM面板）
    3. 头部朝向设备屏幕
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        正常交易分数 (0.0-1.0)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
        
    # 身体稳定性（基于髋部关键点的移动）
    hip_x_coords = []
    hip_y_coords = []
    
    for kps in keypoints_sequence:
        if kps is not None and kps[23][3] > 0.5 and kps[24][3] > 0.5:
            hip_center_x = (kps[23][0] + kps[24][0]) / 2
            hip_center_y = (kps[23][1] + kps[24][1]) / 2
            hip_x_coords.append(hip_center_x)
            hip_y_coords.append(hip_center_y)
    
    if len(hip_x_coords) < 3:
        return 0.0
        
    # 计算身体移动幅度
    hip_x_std = np.std(hip_x_coords)
    hip_y_std = np.std(hip_y_coords)
    body_stability = max(0, 1 - (hip_x_std + hip_y_std) * 10)
    
    # 头部朝向（鼻子应该朝向屏幕，即y坐标相对稳定）
    nose_y_coords = []
    for kps in keypoints_sequence:
        if kps is not None and kps[0][3] > 0.5:
            nose_y_coords.append(kps[0][1])
    
    if len(nose_y_coords) > 0:
        nose_y_stability = max(0, 1 - np.std(nose_y_coords) * 20)
    else:
        nose_y_stability = 0.0
    
    # 手部动作合理性
    hand_movement_score = 0.0
    valid_hand_frames = 0
    
    for i, kps in enumerate(keypoints_sequence):
        if kps is None:
            continue
            
        valid_hand_frames += 1
        # 检查手部是否在合理的操作区域内（y坐标应该在肩膀和髋部之间）
        if kps[15][3] > 0.5 and kps[11][3] > 0.5 and kps[23][3] > 0.5:
            shoulder_y = kps[11][1]
            hip_y = kps[23][1]
            wrist_y = kps[15][1]
            
            # 手腕应该在肩膀下方、髋部上方的合理范围内
            if shoulder_y < wrist_y < hip_y:
                hand_movement_score += 1
    
    if valid_hand_frames > 0:
        hand_movement_score = hand_movement_score / valid_hand_frames
    else:
        hand_movement_score = 0.0
    
    # 综合评分
    normal_score = 0.4 * body_stability + 0.3 * nose_y_stability + 0.3 * hand_movement_score
    return min(normal_score, 1.0)

def compute_potential_fraud_score(keypoints_sequence: List[np.ndarray], fps: int = 5) -> float:
    """计算潜在欺诈行为分数。
    
    潜在欺诈特征：
    1. 异常快速的手部动作
    2. 频繁的视线转移
    3. 身体紧张或不自然姿态
    
    Args:
        keypoints_sequence: 关键点序列
        fps: 帧率
        
    Returns:
        潜在欺诈分数 (0.0-1.0)
    """
    if len(keypoints_sequence) < 5:
        return 0.0
        
    # 手部动作速度（计算手腕位置变化率）
    left_wrist_speeds = []
    right_wrist_speeds = []
    
    prev_left_wrist = None
    prev_right_wrist = None
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        if kps[15][3] > 0.5:  # 左手腕可见
            current_left = (kps[15][0], kps[15][1])
            if prev_left_wrist is not None:
                speed = np.sqrt((current_left[0] - prev_left_wrist[0])**2 + 
                              (current_left[1] - prev_left_wrist[1])**2) * fps
                left_wrist_speeds.append(speed)
            prev_left_wrist = current_left
            
        if kps[16][3] > 0.5:  # 右手腕可见
            current_right = (kps[16][0], kps[16][1])
            if prev_right_wrist is not None:
                speed = np.sqrt((current_right[0] - prev_right_wrist[0])**2 + 
                              (current_right[1] - prev_right_wrist[1])**2) * fps
                right_wrist_speeds.append(speed)
            prev_right_wrist = current_right
    
    # 计算平均手部速度
    avg_speed = 0.0
    if left_wrist_speeds or right_wrist_speeds:
        all_speeds = left_wrist_speeds + right_wrist_speeds
        avg_speed = np.mean(all_speeds) if all_speeds else 0.0
    
    # 高速动作分数（正常操作速度通常<0.5，异常快速>1.0）
    speed_score = min(max((avg_speed - 0.5) / 0.5, 0.0), 1.0)
    
    # 身体紧张度（基于肩膀和髋部的相对位置）
    tension_score = 0.0
    tension_count = 0
    total_frames = 0
    
    for kps in keypoints_sequence:
        if kps is None:
            continue
            
        total_frames += 1
        if (kps[11][3] > 0.5 and kps[12][3] > 0.5 and 
            kps[23][3] > 0.5 and kps[24][3] > 0.5):
            
            # 计算肩膀宽度和髋部宽度的比例
            shoulder_width = abs(kps[11][0] - kps[12][0])
            hip_width = abs(kps[23][0] - kps[24][0])
            
            if hip_width > 0:
                ratio = shoulder_width / hip_width
                # 正常比例约为0.8-1.2，异常紧张时比例会偏离
                if ratio < 0.6 or ratio > 1.4:
                    tension_count += 1
    
    if total_frames > 0:
        tension_score = tension_count / total_frames
    
    # 综合评分
    fraud_score = 0.7 * speed_score + 0.3 * tension_score
    return min(fraud_score, 1.0)

def classify_action(keypoints_sequence: List[Optional[np.ndarray]], fps: int = 5) -> Dict[str, Any]:
    """对视频中的行为进行分类。
    
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
            "classification_label": "unknown",
            "confidence_list": [0.0, 0.0, 0.0]
        }
    
    # 计算各类别分数
    suspicious_score = compute_suspicious_behavior_score(valid_kps, fps)
    normal_score = compute_normal_transaction_score(valid_kps, fps)
    fraud_score = compute_potential_fraud_score(valid_kps, fps)
    
    # 归一化分数
    total_score = suspicious_score + normal_score + fraud_score
    if total_score > 0:
        suspicious_score /= total_score
        normal_score /= total_score
        fraud_score /= total_score
    
    scores = [suspicious_score, normal_score, fraud_score]
    labels = ["suspicious_behavior", "normal_transaction", "potential_fraud"]
    
    best_idx = int(np.argmax(scores))
    best_label = labels[best_idx]
    best_confidence = float(scores[best_idx])
    
    return {
        "classification_label": best_label,
        "confidence_list": [float(score) for score in scores]
    }

def main_process(video_url: str) -> Dict[str, Any]:
    """主处理函数：从视频URL识别异常行为并分类。
    
    Args:
        video_url: 视频URL地址
        
    Returns:
        包含classification_label和confidence_list的字典
        
    Example:
        >>> result = main_process("https://youtube.com/watch?v=example")
        >>> print(result["classification_label"])
        "suspicious_behavior"
        >>> print(result["confidence_list"])
        [0.75, 0.15, 0.10]
    """
    try:
        # 1. 下载视频
        video_path = download_video(video_url)
        
        # 2. 提取帧
        frames = extract_frames(video_path, sample_fps=5)
        if not frames:
            return {
                "classification_label": "unknown",
                "confidence_list": [0.0, 0.0, 0.0]
            }
        
        # 3. 姿态估计
        keypoints_sequence = detect_pose_sequence(frames)
        
        # 4. 分类
        result = classify_action(keypoints_sequence, fps=5)
        
        # 清理临时文件
        try:
            os.remove(video_path)
        except:
            pass
            
        return result
        
    except Exception as e:
        logger.error(f"处理视频时发生错误: {e}")
        return {
            "classification_label": "unknown",
            "confidence_list": [0.0, 0.0, 0.0]
        }

# Web API部分（可选）
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    from flask_restx import Api, Resource, fields
    
    app = Flask(__name__)
    api = Api(app, version='1.0', title='跨境支付AI监测API',
              description='视频异常行为识别服务')
    
    ns = api.namespace('detection', description='异常行为检测操作')
    
    detection_input = api.model('DetectionInput', {
        'video_url': fields.String(required=True, description='视频URL')
    })
    
    detection_output = api.model('DetectionOutput', {
        'classification_label': fields.String(description='分类标签'),
        'confidence_list': fields.List(fields.Float, description='置信度列表')
    })
    
    @ns.route('/analyze')
    class VideoAnalysis(Resource):
        @ns.doc('analyze_video')
        @ns.expect(detection_input)
        @ns.marshal_with(detection_output)
        def post(self):
            """分析视频中的异常行为"""
            video_url = request.json.get('video_url')
            if not video_url:
                return {'error': 'video_url is required'}, 400
            return main_process(video_url)
    
    app.run(host='0.0.0.0', port=5000, debug=False)