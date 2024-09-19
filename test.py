import pandas as pd

# 创建示例数据
data = {
    "timestamp": [
        "2023-09-18 12:00:30",
        "2023-09-18 12:01:45",
        "2023-09-18 12:03:50",
        "2023-09-18 12:06:10",
        "2023-09-18 12:07:30",
        "2023-09-18 12:10:45",
    ],
    "value": [10, 15, 7, 12, 20, 25],
}

# 将数据转换为 DataFrame
df = pd.DataFrame(data)

# 将时间戳转换为 datetime 格式
df["timestamp"] = pd.to_datetime(df["timestamp"])

# 将时间戳设为索引
df.set_index("timestamp", inplace=True)

# 按照5分钟间隔进行重采样，并对'value'列进行聚合（例如取平均值）
resampled_df = df.resample("5T").mean()

# 显示结果
print(resampled_df)
