"""Early-warning model: predicts risk of failing and explains WHY for every student."""
import numpy as np, pandas as pd, joblib, os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

FEATURES = ["attendance", "study_hours", "previous_marks", "assignments_done", "sleep_hours", "internet_usage_hours"]
NICE = {"attendance": "Low attendance", "study_hours": "Low study hours", "previous_marks": "Weak previous marks",
        "assignments_done": "Assignments pending", "sleep_hours": "Poor sleep", "internet_usage_hours": "High non-study internet use"}
ACTION = {"attendance": "Call parents / counsel on attendance condonation rules",
          "study_hours": "Assign study buddy and fixed study-hour schedule",
          "previous_marks": "Enrol in remedial / bridge classes",
          "assignments_done": "Set weekly assignment follow-up with staff advisor",
          "sleep_hours": "Wellness counselling session",
          "internet_usage_hours": "Time-management counselling"}

def make_data(n=1500, seed=7):
    r = np.random.default_rng(seed)
    d = pd.DataFrame({"attendance": r.integers(40, 101, n), "study_hours": np.round(r.uniform(0, 8, n), 1),
        "previous_marks": r.integers(30, 100, n), "assignments_done": r.integers(0, 11, n),
        "sleep_hours": np.round(r.uniform(4, 9, n), 1), "internet_usage_hours": np.round(r.uniform(0, 8, n), 1)})
    s = (0.30*d.attendance + 4*d.study_hours + 0.35*d.previous_marks + 2*d.assignments_done
         + d.sleep_hours - 1.5*d.internet_usage_hours + r.normal(0, 6, n))
    d["result"] = (s > np.percentile(s, 38)).astype(int)
    return d

def train(df=None, path="model/risk_model.pkl"):
    df = make_data() if df is None else df
    X, y = df[FEATURES], df["result"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    cands = {"Logistic Regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
             "Random Forest": RandomForestClassifier(300, random_state=42),
             "Gradient Boosting": GradientBoostingClassifier(random_state=42)}
    rows, best, best_auc = [], None, -1
    for n, m in cands.items():
        m.fit(Xtr, ytr); p = m.predict_proba(Xte)[:, 1]
        auc = roc_auc_score(yte, p)
        rows.append({"Model": n, "Accuracy": round(accuracy_score(yte, p > .5), 3),
                     "F1": round(f1_score(yte, p > .5), 3), "ROC-AUC": round(auc, 3)})
        if auc > best_auc: best, best_auc, best_name = m, auc, n
    explainer = cands["Logistic Regression"]            # linear model -> transparent reasons
    bundle = {"model": best, "name": best_name, "explainer": explainer,
              "table": pd.DataFrame(rows), "means_pass": df[df.result == 1][FEATURES].mean(),
              "importance": getattr(best, "feature_importances_", None)}
    os.makedirs("model", exist_ok=True); joblib.dump(bundle, path)
    return bundle

def load():
    return joblib.load("model/risk_model.pkl") if os.path.exists("model/risk_model.pkl") else train()

def analyse(df, bundle):
    """Return df with fail-risk %, level, top reasons and suggested action per student."""
    X = df[FEATURES]
    risk = 1 - bundle["model"].predict_proba(X)[:, 1]
    pipe = bundle["explainer"]; scaler, lr = pipe.steps[0][1], pipe.steps[1][1]
    contrib = scaler.transform(X) * lr.coef_[0]          # negative => pushes toward FAIL
    reasons, actions = [], []
    for row in contrib:
        idx = [i for i in np.argsort(row) if row[i] < -0.15][:2]
        reasons.append(", ".join(NICE[FEATURES[i]] for i in idx) or "No major concern")
        actions.append(ACTION[FEATURES[idx[0]]] if idx else "Keep encouraging")
    out = df.copy()
    out["fail_risk_%"] = (risk * 100).round(1)
    out["risk_level"] = pd.cut(out["fail_risk_%"], [-1, 35, 65, 101], labels=["Low", "Medium", "High"])
    out["main_reasons"], out["suggested_action"] = reasons, actions
    return out.sort_values("fail_risk_%", ascending=False)
