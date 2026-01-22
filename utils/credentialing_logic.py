def evaluate_program_eligibility(program_row, modality_lookup):
    """
    Determines credentialing eligibility for a single FETP/FELTP program.
    Returns:
        status: Eligible | Conditionally Eligible | Not Eligible
        reasons: list of strings explaining the decision
        actions: list of recommended actions (if any)
    """

    reasons = []
    actions = []

    modality = program_row["modality"]
    accredited = program_row["accredited"]
    host = program_row["host_institution"]

    # -----------------------------
    # Rule 1 — Training Depth
    # -----------------------------
    if modality not in modality_lookup:
        return "Not Eligible", ["Unknown training modality"], ["Clarify modality"]

    modality_meta = modality_lookup[modality]
    duration = modality_meta["duration_months"]
    field_pct = modality_meta["field_based_percent"]

    if duration < 18:
        reasons.append("Training duration below professional threshold")
        actions.append("Upgrade to advanced-level training")

    # -----------------------------
    # Rule 2 — Field Intensity
    # -----------------------------
    if field_pct < 60:
        return "Not Eligible", ["Insufficient field-based training"], ["Increase field deployment"]
    elif field_pct < 70:
        reasons.append("Field exposure below optimal threshold")
        actions.append("Strengthen supervised field placements")

    # -----------------------------
    # Rule 3 — Accreditation
    # -----------------------------
    if accredited != "Yes":
        reasons.append("Program not accredited")
        actions.append("Pursue formal accreditation")

    # -----------------------------
    # Rule 4 — Host Institution
    # -----------------------------
    if not host or host.strip() == "":
        return "Not Eligible", ["No accountable host institution"], ["Establish institutional oversight"]

    # -----------------------------
    # Final Decision
    # -----------------------------
    if len(reasons) == 0:
        status = "Eligible"
    elif "Insufficient field-based training" in reasons:
        status = "Not Eligible"
    else:
        status = "Conditionally Eligible"

    return status, reasons, actions
