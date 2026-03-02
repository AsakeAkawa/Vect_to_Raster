import os
import numpy as np
import rasterio
from rasterio.transform import from_origin
import pyreadr
import pandas as pd
from scipy.io import loadmat

def validate_and_calculate(total_elements):
    """
    Validation Mechanism / 校验与适配机制
    Checks if the total count fits a global 2:1 geographic grid.
    """
    # rows = sqrt(total / 2)
    rows = int(np.sqrt(total_elements / 2))
    cols = rows * 2
    actual_product = rows * cols

    # Integrity Check (Divisibility) 
    # 整除校验
    if actual_product != total_elements:
        print("\n" + "!"*50)
        print("Data Mismatch / 数据量不匹配!")
        print(f"Total elements received / 收到数据总数: {total_elements}")
        print(f"Expected for 2:1 Grid / 理论全球网格需要: {actual_product}")
        print("-" * 50)
        
        # Root Cause Analysis (Common Issues)
        # 常见原因分析
        if total_elements < 9000000 and total_elements > 2000000:
            print("Possible Reason: Masked Data (Land Only).")
            print("数据可能剔除了海洋像素，仅保留了陆地部分，无法直接还原。")
        elif total_elements % 2 != 0:
            print("Possible Reason: Regional Clipping.")
            print("数据可能是局部区域切片，而非全球范围。")
        
        print("!"*50 + "\n")
        return None, None, None

    # Resolution Plausibility Check
    # 分辨率合理性校验
    res = 180.0 / rows
    return rows, cols, res

def load_vector(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".rdata":
        result = pyreadr.read_r(file_path)
        df = result[list(result.keys())[0]]
        return df.iloc[:, 0].values
    elif ext in [".csv", ".txt"]:
        return pd.read_csv(file_path, header=None).iloc[:, 0].values
    elif ext == ".mat":
        data = loadmat(file_path)
        var_names = [k for k in data.keys() if not k.startswith('__')]
        return data[var_names[0]].flatten()
    elif ext == ".npy":
        return np.load(file_path).flatten()
    else:
        raise ValueError(f"Unsupported format: {ext}")

def run_universal_recovery():
    # ==================== Configuration / 路径配置 ====================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    INPUT_FOLDER = os.path.join(BASE_DIR, "data")
    OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")
    
    FILE_NAME = "test_data_csv.csv"  # Please replace the file name here / 请进行文件名替换
    OUT_TIFF_NAME = "Global_Recovered_Result.tif"
    # =================================================================

    input_path = os.path.join(INPUT_FOLDER, FILE_NAME)
    if not os.path.exists(OUTPUT_FOLDER): os.makedirs(OUTPUT_FOLDER)
    
    if not os.path.exists(input_path):
        print(f"Missing file / 找不到文件: {input_path}")
        return

    try:
        # 1. 加载数据 / Load Data
        vector = load_vector(input_path)
        
        # 2. 执行校验与维度计算 / Validate and Calculate
        rows, cols, res = validate_and_calculate(len(vector))
        
        if rows is None:
            return # 校验失败，停止运行 / Validation Failed

        print(f"Validation Passed / 校验通过")
        print(f"Grid: {rows}x{cols} | Resolution: {res:.6f}°")

        # 3. 重塑与保存 / Reshape and save
        grid = vector.reshape((rows, cols))
        transform = from_origin(-180, 90, res, res)
        
        with rasterio.open(
            os.path.join(OUTPUT_FOLDER, OUT_TIFF_NAME), 'w', 
            driver='GTiff', height=rows, width=cols, count=1,
            dtype='float32', crs='EPSG:4326', transform=transform, nodata=-9999
        ) as dst:
            dst.write(np.nan_to_num(grid, nan=-9999).astype('float32'), 1)

        print(f"Result saved to / 结果已保存至: {OUTPUT_FOLDER}")

    except Exception as e:
        print(f"Critical Error / 严重错误: {e}")

if __name__ == "__main__":
    run_universal_recovery()