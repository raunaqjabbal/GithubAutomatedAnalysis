# GithubAutomatedAnalysis
 
gcloud builds submit --tag gcr.io/peak-woodland-395617/analysis  --project=peak-woodland-395617


gcloud run deploy --image gcr.io/peak-woodland-395617/analysis --platform managed  --project=peak-woodland-395617 --allow-unauthenticated
