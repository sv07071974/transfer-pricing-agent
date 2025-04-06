# Transfer Pricing Knowledge Agent

A containerized application that provides a question-answering interface for UAE Transfer Pricing regulations, designed to be deployed on a Synology NAS.

## Features

- Interactive web interface for querying Transfer Pricing knowledge
- AI-powered responses based on UAE Transfer Pricing documentation
- Vector search for accurate information retrieval
- Containerized for easy deployment on Synology NAS
- Citations to source documents for transparency

## Prerequisites

- Synology NAS with Docker support
- OpenAI API key
- Internet connection for the NAS

## Setup Instructions

### 1. Prepare Your Synology NAS

1. Make sure Docker is installed on your Synology NAS
   - Open the Synology Package Center
   - Search for "Docker" and install it

2. Enable SSH access to your Synology NAS (temporarily)
   - Go to Control Panel > Terminal & SNMP
   - Check "Enable SSH service"

### 2. Download the Project

1. Connect to your Synology NAS via SSH:
   ```
   ssh admin@your-nas-ip
   ```

2. Create a directory for the project:
   ```
   mkdir -p /volume1/docker/transfer-pricing-agent
   cd /volume1/docker/transfer-pricing-agent
   ```

3. Clone the repository or upload the files to this directory

### 3. Add Your Transfer Pricing Document

1. Create the data directory:
   ```
   mkdir -p data/documents
   ```

2. Copy your Transfer Pricing guide to the documents folder:
   ```
   # Example using SCP from your local machine:
   scp "Transfer Pricing Guide - EN - 23 10 2023 (1).pdf" admin@your-nas-ip:/volume1/docker/transfer-pricing-agent/data/documents/
   ```

### 4. Configure Environment Variables

1. Edit the .env file:
   ```
   nano .env
   ```

2. Update the `OPENAI_API_KEY` with your actual OpenAI API key

### 5. Deploy the Application

1. Build and start the containers:
   ```
   docker-compose up -d
   ```

2. Check if the containers are running:
   ```
   docker-compose ps
   ```

### 6. Access the Application

1. Open a web browser and navigate to:
   ```
   http://your-nas-ip:3000
   ```

2. The application should load, and the knowledge base will initialize automatically

## Usage

1. Type your question about UAE Transfer Pricing in the search box
2. Click "Ask" or press Enter
3. The system will process your query and return the most relevant answer
4. Source references will be provided below the answer

## Maintenance

### Adding New Documents

1. Add new PDF documents to the `/volume1/docker/transfer-pricing-agent/data/documents/` directory
2. Click the "Refresh KB" button in the application to update the knowledge base

### Updating the Application

1. Navigate to the project directory:
   ```
   cd /volume1/docker/transfer-pricing-agent
   ```

2. Pull the latest changes (if using git)
   ```
   git pull
   ```

3. Rebuild and restart the containers:
   ```
   docker-compose down
   docker-compose up -d --build
   ```

### Troubleshooting

If the application is not working properly:

1. Check the logs:
   ```
   docker-compose logs
   ```

2. Ensure your OpenAI API key is valid and has sufficient credits

3. Restart the containers:
   ```
   docker-compose restart
   ```

## Security Considerations

- This application requires an OpenAI API key, which is stored in the .env file
- The application is designed to be used within your local network
- For additional security, consider:
  - Setting up a reverse proxy with HTTPS
  - Implementing authentication
  - Using a read-only API key with OpenAI

## Support

For questions or issues, please refer to the project documentation or contact your system administrator.
