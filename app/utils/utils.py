from app.utils.constants import TargetLabels


def score_to_label(
    score: float, threshold: float
) -> TargetLabels:
    return (
        TargetLabels.TARGET_1
        if score >= threshold
        else TargetLabels.TARGET_0
    )
