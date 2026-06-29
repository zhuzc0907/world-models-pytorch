import numpy as np
import matplotlib.pyplot as plt
import os

# 加载数据
# file_path = './datasets/carracing/thread_0/rollout_0.npz'
# use relative path to this file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, '..','datasets', 'carracing', 'thread_0', 'rollout_0.npz')
data = np.load(file_path)
obs = data['observations']

print(f"Obs shape: {obs.shape}")
print(f"Frames: {len(obs)}")

# 获取图像尺寸
n_frames, height, width, channels = obs.shape
print(f"Image Size: {height}x{width}, #Channels: {channels}")

# 指示条通常在底部（最后 15-25% 的区域）
indicator_start = int(height * 0.78)  # 从 78% 高度开始
indicator_region = obs[:, indicator_start:, :, :]
print(f"Indicator region shape: {indicator_region.shape}")

# 找一个有效的帧（不是黑屏）
valid_frame_idx = min(30, n_frames - 1)  # 取第 30 帧，如果不足 30 帧就取最后一帧

# 显示该帧的完整图像
plt.figure(figsize=(8, 6))
plt.imshow(obs[valid_frame_idx])
plt.title(f"The {valid_frame_idx} Frame (Full Image)")
plt.axis('off')
plt.show()

# 单独显示指示条区域
if indicator_region.shape[1] > 0 and indicator_region.shape[2] > 0:
    plt.figure(figsize=(8, 2))
    plt.imshow(indicator_region[valid_frame_idx])
    plt.title(f"The {valid_frame_idx} Frame (Indicator Region)")
    plt.axis('off')
    plt.show()
else:
    print("Warning: Indicator region is empty! Please check the cropping parameters.")