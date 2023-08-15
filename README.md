# GithubAutomatedAnalysis


https://analysis-vxjlff6bga-el.a.run.app/


How it works...

All GitHub repositories that aren't forks are cloned.

Summary for all repositories are generated using cloc.

These summaries are processed, aggregated and sent to GPT 3.5

Only summaries sent to GPT, making it very cost efficient.

Answer is extracted and response is shown.

Deployed on Google Cloud Run and made with SteamLit.



# gcloud builds submit --tag gcr.io/peak-woodland-395617/analysis  --project=peak-woodland-395617
# gcloud run deploy --image gcr.io/peak-woodland-395617/analysis --platform managed  --project=peak-woodland-395617 --allow-unauthenticated
