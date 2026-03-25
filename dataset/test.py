from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
import pandas as pd

# =========================
# STEP 1: Load dataset
# =========================
df = pd.read_csv("keystroke.csv")

print("Original Shape:", df.shape)
print("\nNumber of users:", df['subject'].nunique())

# =========================
# STEP 2: Clean data
# =========================
df = df.dropna()
print("Shape after cleaning:", df.shape)

# =========================
# STEP 3: Convert to Authentication
# =========================
target_user = 's002'   # you can change this

# Genuine = 1, Impostor = 0
y = df['subject'].apply(lambda x: 1 if x == target_user else 0)

# Features
X = df.drop(['subject', 'sessionIndex', 'rep'], axis=1)

print("\nFeature shape:", X.shape)
print("Label shape:", y.shape)

# =========================
# STEP 4: Scale features
# =========================
scaler = StandardScaler()
X = scaler.fit_transform(X)

# =========================
# STEP 5: Train-test split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# STEP 6: Train model
# =========================
model = SVC(probability=True)
model.fit(X_train, y_train)

# =========================
# STEP 7: Predictions
# =========================
y_pred = model.predict(X_test)

# =========================
# STEP 8: Evaluation
# =========================
cm = confusion_matrix(y_test, y_pred)
tn, fp, fn, tp = cm.ravel()

# FAR = False Acceptance Rate
far = fp / (fp + tn)

# FRR = False Rejection Rate
frr = fn / (fn + tp)

# EER (approx)
eer = (far + frr) / 2

print("\nConfusion Matrix:")
print(cm)

print("\nFAR:", far)
print("FRR:", frr)
print("Approx EER:", eer)
