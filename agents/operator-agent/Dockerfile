FROM python:3.11-slim

WORKDIR /app
COPY . .

# Create logs directory
RUN mkdir -p logs

# Run the agent script
CMD ["python", "agent.py"]
