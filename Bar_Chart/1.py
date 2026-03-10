import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os

# --- 1. 字体设置 (建议预先安装 Times New Roman，或使用系统默认 Serif) ---
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
plt.rcParams['axes.unicode_minus'] = False 

# --- 2. 数据准备 ---
labels = ['a', 'b', 'c']
base_models_scores = [275, 247, 134]
aligned_models_scores = [62, 64, 58]
diffs = [-213, -183, -76] 

x = np.arange(len(labels)) 
width = 0.25 

# --- 3. 创建画布 ---
fig, ax = plt.subplots(figsize=(10, 6))

# 设置柱状图，zorder 设为 2 (较低层)
rects1 = ax.bar(x - width/2, base_models_scores, width, label='Base Models', 
                color='#3D77B4', edgecolor='black', linewidth=1.5, zorder=2)
rects2 = ax.bar(x + width/2, aligned_models_scores, width, label='Ours', 
                color='#EC7676', edgecolor='black', linewidth=1.5, hatch='//', zorder=2)

# --- 4. 设置网格置顶与外边框封闭 ---

# 4.1 网格设置：设置较高的 zorder 使其显示在柱子上方
ax.yaxis.grid(True, linestyle='--', alpha=1, zorder=5, color="#ACACAC")
ax.set_axisbelow(False) # 确保坐标轴/网格不被放在最底层

# 4.2 外边框封闭：开启所有四个方向的边框线
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(1.5)
    spine.set_edgecolor('black')

# 4.3 坐标轴细节调整
ax.set_ylabel('Number of Detected', fontsize=22)
ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=22)
ax.set_ylim(0, 300) 
ax.legend(loc='upper right', fontsize=22, frameon=True, edgecolor='black') 
ax.tick_params(axis='both', labelsize=22, width=1.5)

# 柱顶数值 (zorder 设为 6，保证在网格线之上)
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height + 5,
            f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=22, zorder=6)

# --- 5. 绘制标注箭头 (zorder 设为 7-8，防止被网格切割) ---
for i in range(len(labels)):
    x_pos = x[i] + width/2 
    top_y = base_models_scores[i]      
    target_y = aligned_models_scores[i] 
    
    # 顶部和底部的红短横线
    line_w = 0.06
    ax.plot([x_pos - line_w, x_pos + line_w], [top_y, top_y], color='#C00100', lw=2, zorder=7)
    
    # 垂直贯穿箭头
    ax.annotate('', 
                xy=(x_pos, target_y + 20), 
                xytext=(x_pos, top_y),            
                arrowprops=dict(arrowstyle='<->', color='#C00100', lw=2, mutation_scale=20),
                zorder=7)
    
    # 差值文字 (带白色背景 bbox 覆盖箭头中段，营造“截断”感)
    text_y = (top_y + target_y + 20) / 2
    ax.text(x_pos, text_y, f'{diffs[i]}', 
            color='#C00100', ha='center', va='center', 
            fontstyle='italic', fontweight='bold', fontsize=22,
            bbox=dict(facecolor='white', edgecolor='none', pad=1),
            zorder=8)

plt.tight_layout()
plt.savefig("1.png", dpi=300)
plt.show()