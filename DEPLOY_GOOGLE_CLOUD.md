# Google Cloud Serverless Deployment — ELIF Engine

## 1. Prerequisites
- [Google Cloud SDK (gcloud)](https://cloud.google.com/sdk/docs/install) installed and authenticated (`gcloud auth login`).
- A GCP Project ID with **Cloud Functions API** and **Artifact Registry API** enabled.
- Billing enabled for the project (required for Cloud Functions gen2).

## 2. Prepare the Environment
Run these commands locally to set your project:
```powershell
gcloud config set project [YOUR_PROJECT_ID]
gcloud services enable cloudfunctions.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com
```

## 3. Deployment Script
The following command deploys the `handle_step_request` from `serverless_handler.py` as a Cloud Function.

### For the Engine (src/elif_v0_1)
```powershell
# Navigate to the source directory
cd "src"

# Deploy the function
gcloud functions deploy elif-engine-step \
  --gen2 \
  --runtime=python311 \
  --region=us-central1 \
  --source=. \
  --entry-point=elif_v0_1.serverless_handler.handle_step_request \
  --trigger-http \
  --allow-unauthenticated \
  --set-env-vars="ELIF_ANTHROPIC_API_KEY=[YOUR_KEY]"
```

## 4. Testing the Deployment
Once deployed, you will get a URL (e.g., `https://us-central1-[ID].cloudfunctions.net/elif-engine-step`).
You can test it with a JSON payload:
```powershell
curl -X POST [YOUR_FUNCTION_URL] \
  -H "Content-Type: application/json" \
  -d '{
    "step_id": "step_1",
    "case_id": "DEPLOY_TEST",
    "offline_mode": true,
    "input_frame": {"id": "1", "text": "Test Question"}
  }'
```

## 5. Automation Tips
- **Continuous Deployment**: Add the `gcloud functions deploy` command to a **GitHub Action** (_.github/workflows/deploy.yml_) triggered on `push` to the main branch.
- **Secrets Management**: Instead of `--set-env-vars`, use **Google Secret Manager** for the Anthropic API key to keep it secure.
