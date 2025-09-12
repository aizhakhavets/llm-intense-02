FROM python:3.13-slim

WORKDIR /app

# Copy project files
COPY . .

# Install uv and sync dependencies
RUN pip install uv && uv sync --frozen

# Create logs directory
RUN mkdir -p logs

# Run the bot
CMD ["uv", "run", "python", "main.py"]
