# Railway Deployment Guide

This guide provides simple, step-by-step instructions for deploying the CrazyChef_Michlan bot to the cloud using Railway.

## Prerequisites

1.  **Railway Account**: You need a Railway account. You can create one at [railway.app](https://railway.app/).
2.  **GitHub Repository**: Your bot's code should be in a GitHub repository.

## Deployment Steps

1.  **Create a New Project on Railway**
    - Log in to your Railway dashboard.
    - Click on "New Project".
    - Select "Deploy from GitHub repo".
    - Choose the repository for your bot. Railway will automatically detect the `Dockerfile` and start building your project.

2.  **Configure Environment Variables**
    - In your project dashboard on Railway, go to the "Variables" tab.
    - Add the following required environment variables:
        - `ENV`: Set this to `production`.
        - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot token.
        - `OPENROUTER_API_KEY`: Your OpenRouter API key.
    - You can also add these optional variables to customize the bot's behavior (if you don't add them, default values will be used):
        - `OPENROUTER_MODEL`
        - `LLM_TEMPERATURE`
        - `LLM_MAX_TOKENS`
        - `MAX_CONTEXT_MESSAGES`

3.  **Deployment**
    - Once you add the environment variables, Railway will automatically trigger a new deployment.
    - You can monitor the deployment process in the "Deployments" tab.

4.  **Check the Logs**
    - To see the bot's logs and check if it's running correctly, click on your service in the project view and then go to the "Logs" tab.

That's it! Your CrazyChef_Michlan bot is now deployed on Railway.
