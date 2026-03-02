# Vect_to_Raster 无参考全球数据转TIFF图像

**Transform coordinate-free 1D vectors into geo-referenced TIFF files.**  
**本工具用于将无参考信息的数据转换为 TIFF 文件，还原没有参考坐标系和分辨率的全球空间数据。**

---

## Disclaimer / 声明

- **Data Accuracy**: This tool operates based on the mathematical assumption of "Equirectangular Projection." Due to the diversity of original data sources, results may contain offsets or distortions. Users must verify geographic accuracy before analysis.  
  **数据准确性**：本工具基于“等经纬度投影”的数学假设进行空间还原。由于原始数据源的多样性，转换结果可能存在偏移或变形。用户在使用前务必自行校核准确性。
- **Compliance**: Users must adhere to the original provider's License (e.g., SPAM, GAEZ). The author assumes no responsibility for unauthorized data use.  
  **版权与合规**：用户在使用本工具处理特定的数据集（如 SPAM, GAEZ 等）时，需自行遵守原数据持有方的使用协议。本工具作者不对用户非法获取或违规使用数据的行为承担任何责任。
- **No Warranty**: This software is provided "as is" without any warranty. The author is not liable for any direct or indirect losses (data loss, research bias, etc.).  
  **无担保责任**：本程序按“现状”提供。作者不对因使用本程序导致的任何直接或间接损失（包括但不限于数据丢失、研究偏差、经济损失）负责。
- **Legal Use**: It is prohibited to use this tool for any activities that violate local laws and regulations.  
  **合规使用**：禁止利用本工具进行任何违反所在地区法律法规的行为。
- **Sample Data**: The test data consists of 2020 global maize crop distribution, sourced from IFPRI open data.  
  **测试数据**：测试数据为 2020 年全球玉米作物种植数据，来源于 IFPRI 的开源数据。

---

## Features / 功能特性

- **Multi-format Support**: Compatible with `.RData`, `.mat`, `.csv`, `.txt`, and `.npy`.  
  **多格式支持**: 支持 `.RData`, `.mat`, `.csv`, `.txt`, 及 `.npy` 等多种科研数据格式。
- **Smart Detection**: Automatically calculates dimensions and matches global resolutions (5', 10', or 30'').  
  **智能维度检测**: 根据数据总量自动计算行列数并匹配全球 5', 10', 或 30'' 分辨率。
- **Validation**: Built-in mismatch alerts that can identify:  
  **校验机制**: 内置数据适配检查，能够识别：
  - **Regional Clipping** (局部区域切片)
  - **Masked/Land-only Data** (仅包含陆地像素/掩膜数据)

---

## Data Requirements / 适用数据要求

To ensure successful recovery, input data must meet three criteria:  
为了确保数据能够成功还原，输入数据必须满足以下三个前提条件：
1. **Global Coverage**: Must cover longitude 360° and latitude 180°.  
   **全球范围**: 数据需覆盖全球（经度 360°, 纬度 180°）。
2. **Equirectangular Projection**: CRS must be WGS84 or equivalent.  
   **等经纬度投影**: 坐标系需为 WGS84 及其等效投影。
3. **Full Grid Storage**: Must include ocean pixels (no background clipping).  
   **全样点存储**: 数据必须包含海洋像素，不得剔除背景值。

---

## Usage Guide / 使用说明

### 1. Requirements / 环境要求
Install the necessary Python libraries:  
请安装必要的Python库：
```bash
pip install numpy pandas rasterio pyreadr scipy
```

### 2. Project Structure / 项目结构

```text
Vect_to_Raster/
├── data/       <-- Put your original data here (将原始数据放入此处)
├── output/     <-- Results will be saved here (转换结果将保存在此处)
├── test_data/     <-- Test data is here (提供的测试文件)
├── Blind_Raster_Recovery.py     <-- Core script (核心脚本)
└── README.md   <-- Documentation (项目说明)
``` 

### 3. Execution / 运行指南
- Place your data into the /data folder.  
  将数据放入 /data 文件夹
- Update the corresponding FILE_NAME in the script.  
  在脚本中修改对应的文件名
- Run the program.  
  运行程序

