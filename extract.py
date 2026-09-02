import requests
import json

def extract_trials():
    url = "https://clinicaltrials.gov/api/v2/studies?query.cond=diabetes&pageSize=20"

    response = requests.get(url)
    data = response.json()
    studies = data["studies"]

    all_trials = []

    for trial in studies:
        nct_id = trial["protocolSection"]["identificationModule"]["nctId"]
        title = trial["protocolSection"]["identificationModule"]["briefTitle"]
        status = trial["protocolSection"]["statusModule"]["overallStatus"]

        conditions = trial["protocolSection"]["conditionsModule"]["conditions"]
        conditions_str = ", ".join(conditions)

        sponsor = trial["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"]["name"]

        phase = trial["protocolSection"]["designModule"].get("phases", ["NA"])
        phase_str = ", ".join(phase)

        enrollment_count = trial["protocolSection"]["designModule"].get("enrollmentInfo", {}).get("count", None)

        record = {
            "nct_id": nct_id,
            "title": title,
            "status": status,
            "conditions": conditions_str,
            "sponsor": sponsor,
            "phase": phase_str,
            "enrollment_count": enrollment_count
        }
        all_trials.append(record)

    with open("raw_trials.json", "w") as f:
        json.dump(all_trials, f, indent=2)

    return all_trials