## Deploying a Large Language Model (LLM) on Jetson Orin Nano with Ollama

### Overview

This guide provides a streamlined approach to deploying and running a Large Language Model (LLM) on the Jetson Orin Nano using Ollama, a powerful framework for running LLMs locally. You will learn how to set up the environment, deploy a pre-built Docker container, and interact with the model inside the container.

For detailed documentation, refer to: [Jetson AI Lab Ollama Tutorial](https://www.jetson-ai-lab.com/tutorial_ollama.html).

---

### Deployment Steps Using a Pre-Built Container

1. Pull the Docker image:
   ```bash
   docker pull dustynv/ollama:r35.4.1
   ```

2. Run the container:
   ```bash
   docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama dustynv/ollama:r35.4.1
   ```

3. Execute the model inside the running container:
   ```bash
   docker exec -it ollama ollama run sam4096/qwen2tools:1.5b
   ```

---

### Steps for Building and Deployment from scratch

> Use this when working on jetpack 5. dustynv/ollama:r36.2.0 only works on jetpack 6

#### 1. Clone the Container Repository

The first step is to clone the repository containing the Jetson-compatible containers. This repository provides pre-built containers optimized for Nvidia Jetson devices, including the Orin Nano.

Run the following command to clone the repository:

```bash
git clone https://github.com/dusty-nv/jetson-containers
```

This command will download the `jetson-containers` repository to your local machine, allowing you to access and use the container configurations specific to Jetson devices.

#### 2. Install the Containers

After cloning the repository, you'll need to run the installation script provided within the repository. This script installs all the necessary components and prepares your system to run the containers.

Run the installation script with:

```bash
bash jetson-containers/install.sh
```

This script sets up the environment, installs dependencies, and configures the system to work with the containers designed for Jetson devices.

#### 3. Run the Ollama Container

Once the installation is complete, you can run the Ollama container. The container is designed to leverage the Jetson Orin Nano's capabilities, providing an optimized environment for running LLMs.

Use the following command to start the container:

```bash
jetson-containers run --name ollama $(autotag ollama)
```

- `jetson-containers run`: This command launches the container using the configurations provided by the `jetson-containers` repository.
- `--name ollama`: This option names the container "ollama" for easy identification.
- `$(autotag ollama)`: Automatically tags and pulls the latest Ollama container image compatible with the Jetson Orin Nano.

### Manually Download and Run a LLM in the Ollama Container

To manually download and run a specific LLM model, such as Llama 3.1, inside the Ollama container, use the following command:

```bash
docker exec -it ollama ollama run sam4096/qwen2tools:1.5b
```

- `docker exec -it ollama`: Executes commands inside the running Ollama container.
- `ollama run sam4096/qwen2tools:1.5b`: Runs the specified model (`sam4096/qwen2tools:1.5b`) within the container.

---

### Access the Container Shell

For more control or troubleshooting, you might want to access the container's shell directly. This allows you to interact with the container's file system and manually manage models or configurations.

Enter the container's shell using:

```bash
docker exec -it ollama sh
```

This command opens an interactive shell session within the Ollama container.

---

### Interact with Ollama in the Container Shell

Once inside the container's shell, you can interact with Ollama using its command-line interface (CLI). Below is an overview of the basic usage and available commands.

#### Basic Usage:

```bash
ollama [command] [flags]
```

#### Available Commands:

- **serve**: Start Ollama's service.
- **create**: Create a model from a Modelfile.
- **show**: Display information about a model.
- **run**: Execute a model.
- **pull**: Download a model from a registry.
- **push**: Upload a model to a registry.
- **list**: List all available models.
- **ps**: List currently running models.
- **cp**: Copy a model.
- **rm**: Remove a model.
- **help**: Get help for any command.

#### Example Commands:

1. **Run a Model**:
   ```bash
   ollama run sam4096/qwen2tools:1.5b
   ```

2. **List Available Models**:
   ```bash
   ollama list
   ```

3. **Pull a Model from a Registry**:
   ```bash
   ollama pull sam4096/qwen2tools:1.5b
   ```