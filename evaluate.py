import pandas as pd

print("Evaluating Model Performance...")

# Load original data with labels
true_data = pd.read_csv(r"C:\Users\DELL\OneDrive\Desktop\llm\data\processed\new_resume.csv")

# Load predictions from training
pred_data = pd.read_csv("C:\Users\DELL\OneDrive\Desktop\llm\prompts")

# Convert score to Fit / No Fit
def score_to_label(score):
    try:
        return "Fit" if int(score) >= 60 else "No Fit"
    except:
        return "No Fit"

pred_data["predicted_label"] = pred_data["score"].apply(score_to_label)

# Accuracy
accuracy = (
    pred_data["predicted_label"] == true_data["label"]
).mean()

print(f"Accuracy: {accuracy*100:.2f}%")
