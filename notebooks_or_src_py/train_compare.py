"""
train_compare.py — Huấn luyện và so sánh 5 mô hình hồi quy trên bộ House Prices.
Người phụ trách: Võ Phú Vinh.

Dùng lại preprocess.py (pipeline tiền xử lý + train/test split) và metrics.py
(MAE, RMSE, R²) để đảm bảo mọi mô hình được đánh giá công bằng trên CÙNG một
tập dữ liệu, CÙNG một cách xử lý, CÙNG một random seed.

Cách chạy:
    python notebooks_or_src_py/train_compare.py

Yêu cầu: đã có data/train.csv, đã cài đặt scikit-learn và xgboost
(pip install -r requirements.txt).

Kết quả:
    - results/model_results.csv   -> bảng so sánh MAE/RMSE/R²/CV/thời gian của 5 mô hình
    - models/best_model.pkl       -> mô hình có kết quả tốt nhất, đã lưu bằng joblib
"""

import os
import time
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None
    print("CẢNH BÁO: chưa cài xgboost. Chạy: pip install xgboost")

from preprocess import load_and_split, build_pipeline, RANDOM_SEED
from metrics import evaluate_all

RESULTS_DIR = "results"
MODELS_DIR = "models"
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)


def get_models() -> dict:
    """
    Danh sách 5 mô hình cần so sánh. Tham số ở đây là mức khởi điểm hợp lý —
    Vinh tinh chỉnh thêm (Grid/Randomized Search) ở bước sau khi đã chạy
    được bản so sánh cơ bản này.
    """
    models = {
        "Linear Regression": LinearRegression(),
        "Decision Tree": DecisionTreeRegressor(random_state=RANDOM_SEED, max_depth=8),
        "Random Forest": RandomForestRegressor(
            random_state=RANDOM_SEED, n_estimators=200, max_depth=None
        ),
        "Gradient Boosting": GradientBoostingRegressor(
            random_state=RANDOM_SEED, n_estimators=200, learning_rate=0.05
        ),
    }
    if XGBRegressor is not None:
        models["XGBoost"] = XGBRegressor(
            random_state=RANDOM_SEED, n_estimators=300, learning_rate=0.05,
            max_depth=4, verbosity=0
        )
    return models


def run_all_models(X_train, X_test, y_train, y_test, preprocessor, cv_folds: int = 5):
    results = []
    fitted_pipelines = {}

    for name, model in get_models().items():
        print(f"\n--- Đang huấn luyện: {name} ---")
        pipe = Pipeline(steps=[
            ("preprocess", preprocessor),
            ("model", model),
        ])

        start = time.time()
        pipe.fit(X_train, y_train)
        train_time = time.time() - start

        y_pred = pipe.predict(X_test)
        scores = evaluate_all(y_test, y_pred)

        # Cross-Validation trên tập train (đo độ ổn định, không dùng để chọn cuối cùng một mình)
        cv_scores = cross_val_score(
            pipe, X_train, y_train, cv=cv_folds, scoring="neg_mean_absolute_error"
        )
        cv_mae_mean = -cv_scores.mean()

        results.append({
            "Model": name,
            "MAE": round(scores["MAE"], 2),
            "RMSE": round(scores["RMSE"], 2),
            "R2": round(scores["R2"], 4),
            "CV_MAE_mean": round(cv_mae_mean, 2),
            "Train_time_s": round(train_time, 2),
        })
        fitted_pipelines[name] = pipe

        print(f"MAE={scores['MAE']:.2f} | RMSE={scores['RMSE']:.2f} | "
              f"R2={scores['R2']:.4f} | CV_MAE={cv_mae_mean:.2f} | "
              f"Thời gian={train_time:.2f}s")

    return pd.DataFrame(results), fitted_pipelines

def save_xgboost_feature_importance(fitted_pipelines: dict, top_n: int = 20):
    """
    Lưu Feature Importance của mô hình XGBoost:
    - results/xgboost_feature_importance.csv
    - results/xgboost_feature_importance.png
    """
    if "XGBoost" not in fitted_pipelines:
        print("\nKhông tìm thấy XGBoost, bỏ qua Feature Importance.")
        return

    xgb_pipe = fitted_pipelines["XGBoost"]

    # Lấy mô hình XGBoost sau khi pipeline đã fit
    xgb_model = xgb_pipe.named_steps["model"]

    # Lấy tên các feature sau khi xử lý missing và One-Hot Encoding
    preprocessor = xgb_pipe.named_steps["preprocess"]
    feature_names = preprocessor.get_feature_names_out()

    # Lấy độ quan trọng của từng feature
    importances = xgb_model.feature_importances_

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances,
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    ).reset_index(drop=True)

    # Lưu toàn bộ bảng Feature Importance
    csv_path = os.path.join(
        RESULTS_DIR,
        "xgboost_feature_importance.csv"
    )
    importance_df.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig"
    )

    # Chỉ vẽ top_n feature quan trọng nhất
    top_features = importance_df.head(top_n).sort_values(
        by="Importance",
        ascending=True
    )

    plt.figure(figsize=(10, 8))
    plt.barh(
        top_features["Feature"],
        top_features["Importance"]
    )
    plt.xlabel("Feature Importance")
    plt.ylabel("Feature")
    plt.title(f"Top {top_n} Feature Importance - XGBoost")
    plt.tight_layout()

    plot_path = os.path.join(
        RESULTS_DIR,
        "xgboost_feature_importance.png"
    )
    plt.savefig(plot_path, dpi=300, bbox_inches="tight")
    plt.close()

    print("\n=== FEATURE IMPORTANCE XGBOOST ===")
    print(importance_df.head(top_n).to_string(index=False))
    print(f"\nĐã lưu bảng: {csv_path}")
    print(f"Đã lưu biểu đồ: {plot_path}")
def select_and_save_best(results_df: pd.DataFrame, fitted_pipelines: dict):
    """Chọn mô hình có MAE thấp nhất trên tập test làm mô hình tốt nhất."""
    best_row = results_df.sort_values("MAE").iloc[0]
    best_name = best_row["Model"]
    best_pipe = fitted_pipelines[best_name]

    out_path = os.path.join(MODELS_DIR, "best_model.pkl")
    joblib.dump(best_pipe, out_path)

    print(f"\n=== Mô hình tốt nhất: {best_name} (MAE={best_row['MAE']}) ===")
    print(f"Đã lưu vào: {out_path}")
    return best_name


def main():
    X_train, X_test, y_train, y_test = load_and_split()
    preprocessor = build_pipeline(X_train)

    results_df, fitted_pipelines = run_all_models(
        X_train, X_test, y_train, y_test, preprocessor
    )

    save_xgboost_feature_importance(fitted_pipelines)
    results_df = results_df.sort_values("MAE").reset_index(drop=True)
    out_csv = os.path.join(RESULTS_DIR, "model_results.csv")
    results_df.to_csv(out_csv, index=False, encoding="utf-8-sig")

    print("\n=== BẢNG SO SÁNH 5 MÔ HÌNH (sắp xếp theo MAE tăng dần) ===")
    print(results_df.to_string(index=False))
    print(f"\nĐã lưu bảng kết quả vào: {out_csv}")

    select_and_save_best(results_df, fitted_pipelines)


if __name__ == "__main__":
    main()