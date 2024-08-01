import argparse
import os
import pandas as pd
import boto3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--model-dir", type=str, default=os.getenv("SM_MODEL_DIR"))
    parser.add_argument("--data-dir", type=str, default="./")
    parser.add_argument("--output-model-dir", type=str)
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        # 打印参数以供调试
        print(f"Arguments: {args}")

        # 加载数据
        data_path = os.path.join(args.data_dir, "demo_data.csv")
        print(f"Loading data from {data_path}")
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at {data_path}")

        df = pd.read_csv(data_path)
        print("Data loaded successfully")

        # 分割数据集
        X = df[["X1", "X2"]]
        y = df["y"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=0
        )
        print("Data split into training and testing sets")

        # 训练简单的线性回归模型
        model = LinearRegression()
        model.fit(X_train, y_train)
        print("Model trained successfully")

        # 预测和评估
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Mean Squared Error: {mse}")

        # 保存模型
        model_path = os.path.join(args.model_dir, "model.pkl")
        print(f"Saving model to {model_path}")
        pd.to_pickle(model, model_path)
        print("Model saved successfully")

        # 上传模型和结果到S3
        s3 = boto3.client("s3", region_name="cn-northwest-1")
        bucket = args.output_model_dir.split("/")[2]
        s3_model_path = "/".join(args.output_model_dir.split("/")[3:]) + "/model.pkl"
        print(f"Uploading model to S3 at s3://{bucket}/{s3_model_path}")
        s3.upload_file(model_path, bucket, s3_model_path)
        print(f"Model uploaded to S3 at s3://{bucket}/{s3_model_path}")

    except Exception as e:
        print(f"Error during training: {e}")
        raise


if __name__ == "__main__":
    main()
