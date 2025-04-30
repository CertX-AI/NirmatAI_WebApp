"""Visual description module of Web App."""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.metrics import classification_report, confusion_matrix


def filter_unexpected_labels(
        true_labels: pd.Series,
        predicted_labels: pd.Series,
        required_labels: list[str]
    ) -> tuple[pd.Series, pd.Series, int, int]:
    """Filter out unexpected labels and count how many were removed."""
    unexpected_true_labels = ~true_labels.isin(required_labels)
    unexpected_pred_labels = ~predicted_labels.isin(required_labels)

    # Count unexpected labels
    num_unexpected_true = unexpected_true_labels.sum()
    num_unexpected_pred = unexpected_pred_labels.sum()

    # Filter out unexpected labels
    filtered_true_labels = true_labels[~unexpected_true_labels]
    filtered_pred_labels = predicted_labels[~unexpected_pred_labels]

    return filtered_true_labels, filtered_pred_labels, num_unexpected_true, num_unexpected_pred # noqa: E501

def plot_confusion_matrix(true_labels: pd.Series, predicted_labels: pd.Series) -> None:
    """Generate and display a confusion matrix."""
    required_labels = [
        "full-compliance",
        "minor non-conformity",
        "major non-conformity"
    ]

    # Filter unexpected labels
    filtered_true_labels, filtered_pred_labels, num_unexpected_true, num_unexpected_pred = filter_unexpected_labels(true_labels, predicted_labels, required_labels) # noqa: E501

    # Display counts of unexpected labels
    if num_unexpected_true > 0 or num_unexpected_pred > 0:
        st.warning(
            f"Filtered out {num_unexpected_true} unexpected true labels and {num_unexpected_pred} unexpected predicted labels." # noqa: E501
        )

    # Generate confusion matrix
    cm = confusion_matrix(
        filtered_true_labels,
        filtered_pred_labels,
        labels=required_labels
    )

    # Plot confusion matrix
    plt.figure(figsize=(6, 4))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=required_labels,
        yticklabels=required_labels
    )
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.title("Confusion Matrix")
    st.pyplot(plt)

def plot_compliance_distribution(df: pd.DataFrame) -> None:
    """Plot the distribution of true and predicted compliance labels."""
    if "Label" not in df.columns or "Compliance status" not in df.columns:
        st.error(
            "The required columns 'Label' and 'Compliance status' are missing."
        )
        return

    required_labels = [
        "full-compliance",
        "minor non-conformity",
        "major non-conformity"
    ]

    true_labels = df["Label"]
    predicted_labels = df["Compliance status"]

    # Filter unexpected labels
    filtered_true_labels, filtered_pred_labels, num_unexpected_true, num_unexpected_pred = filter_unexpected_labels(true_labels, predicted_labels, required_labels) # noqa: E501

    # Display counts of unexpected labels
    if num_unexpected_true > 0 or num_unexpected_pred > 0:
        st.warning(
            f"Filtered out {num_unexpected_true} unexpected true labels and {num_unexpected_pred} unexpected predicted labels." # noqa: E501
        )

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    # True label distribution
    true_label_counts = filtered_true_labels.value_counts()
    ax[0].bar(true_label_counts.index, true_label_counts.values, color="skyblue")
    ax[0].set_title("True Label Distribution")
    ax[0].set_xlabel("Compliance Status")
    ax[0].set_ylabel("Count")

    # Predicted label distribution
    pred_label_counts = filtered_pred_labels.value_counts()
    ax[1].bar(pred_label_counts.index, pred_label_counts.values, color="lightgreen")
    ax[1].set_title("Predicted Label Distribution")
    ax[1].set_xlabel("Compliance Status")
    ax[1].set_ylabel("Count")

    st.pyplot(fig)

def display_classification_report(
        true_labels: pd.Series,
        predicted_labels: pd.Series
    ) -> None:
    """Extract precision and display them by class."""
    required_labels = [
        "full-compliance",
        "minor non-conformity",
        "major non-conformity"
    ]

    # Filter unexpected labels
    filtered_true_labels, filtered_pred_labels, num_unexpected_true, num_unexpected_pred = filter_unexpected_labels(true_labels, predicted_labels, required_labels) # noqa: E501

    # Display counts of unexpected labels
    if num_unexpected_true > 0 or num_unexpected_pred > 0:
        st.warning(
            f"Filtered out {num_unexpected_true} unexpected true labels and {num_unexpected_pred} unexpected predicted labels." # noqa: E501
        )

    # Generate classification report
    report = classification_report(
        filtered_true_labels,
        filtered_pred_labels,
        target_names=required_labels,
        output_dict=True
    )

    # Extract precision by class
    precision_full_compliance = report["full-compliance"]["precision"]
    precision_minor_non_conformity = report["minor non-conformity"]["precision"]
    precision_major_non_conformity = report["major non-conformity"]["precision"]

    # Display precision metrics
    st.subheader("Precision by Class")
    precision_col1, precision_col2, precision_col3 = st.columns(3)

    with precision_col1:
        st.metric(
            label="Full Compliance Precision",
            value=f"{precision_full_compliance:.2f}"
        )
    with precision_col2:
        st.metric(
            label="Minor Non-conformity Precision",
            value=f"{precision_minor_non_conformity:.2f}"
        )
    with precision_col3:
        st.metric(
            label="Major Non-conformity Precision",
            value=f"{precision_major_non_conformity:.2f}"
        )

def plot_f1_score_chart(true_labels: pd.Series, predicted_labels: pd.Series) -> None:
    """Plot F1-score bar chart for each class."""
    required_labels = [
        "full-compliance",
        "minor non-conformity",
        "major non-conformity"
    ]

    # Filter unexpected labels
    filtered_true_labels, filtered_pred_labels, num_unexpected_true, num_unexpected_pred = filter_unexpected_labels(true_labels, predicted_labels, required_labels) # noqa: E501

    # Display counts of unexpected labels
    if num_unexpected_true > 0 or num_unexpected_pred > 0:
        st.warning(
            f"Filtered out {num_unexpected_true} unexpected true labels and {num_unexpected_pred} unexpected predicted labels." # noqa: E501
        )

    # Generate classification report
    report = classification_report(
        filtered_true_labels,
        filtered_pred_labels,
        target_names=required_labels,
        output_dict=True
    )

    # Extract F1-scores for each class
    f1_scores = {
        "Full Compliance": report["full-compliance"]["f1-score"],
        "Minor Non-conformity": report["minor non-conformity"]["f1-score"],
        "Major Non-conformity": report["major non-conformity"]["f1-score"]
    }

    # Plot F1-scores
    plt.figure(figsize=(8, 4))
    plt.bar(
        f1_scores.keys(),
        f1_scores.values(),
        color=["skyblue", "lightgreen", "salmon"]
    )
    plt.title("F1-scores by Compliance Class")
    plt.xlabel("Compliance Status")
    plt.ylabel("F1-score")

    # Display the plot
    st.pyplot(plt)
