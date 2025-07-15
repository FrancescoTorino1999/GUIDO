# GUIDO — Gathering and Understanding Socio-Technical Aspects in Development Organizations

## Introduction

**GUIDO** Is a conversational agent designed to operate locally, accessible through an executable file, enabling the identification and management of *community smells* in software development communities on GitHub.

GUIDO is based on a previous tool for the detection of community smells, **CADOCS**, originally proposed by Voria et al. in a research paper published at ICSME 2022.

The *documents* folder contains various artifacts that facilitate understanding GUIDO, including instructional videos on its usage.

## How to Install the Tool

Follow the steps below to install and run **GUIDO** locally on your machine.

---

### 🛠️ 1. Prerequisites

Before installing, make sure you have the following installed on your system:

- [Docker](https://www.docker.com/)
- A **GitHub Personal Access Token (PAT)**

#### 🔐 Generate a GitHub PAT

To interact with GitHub, GUIDO requires a Personal Access Token (PAT):

1. **Log in** to your GitHub account.
2. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
3. Click **Generate new token** and configure:
   - **Expiration**: Choose a duration or select "No expiration".
   - **Permissions**: At minimum, enable:
     - `repo`
     - `write:discussion`
     - `project`
     - `user`
4. Click **Generate token** and **copy it immediately**. You won’t be able to see it again later.

> ⚠️ **Keep your PAT secure** – treat it like a password and never share it publicly.

---

### 🧪 2. Clone the Repository

```bash
git clone https://github.com/FrancescoTorino1999/GUIDO.git
```

---

### 💡 3. [Optional – Windows Users] Convert Shell Scripts to LF

If you're using **Windows**, make sure shell scripts (like `run.sh`) use **LF (Unix-style)** line endings.

> CRLF (Windows-style) endings can cause errors when running scripts in Docker.

#### ✅ To fix line endings:

- **Using VS Code**:
  - Open the `.sh` file.
  - Click on `CRLF` in the bottom-right corner and switch it to `LF`.

- **Or via terminal**:
  ```bash
  dos2unix run.sh
  ```

---

### 🐳 4. Build and Run with Docker

1. Navigate to the `docker` folder.
2. Open the `Dockerfile` and **add your GitHub PAT** where indicated.
3. Build and run the container:

```bash
docker-compose build
docker compose up
```

---

### 🌐 5. Access the Application

Once the container is running, open your browser and go to:

```
http://localhost:3000
```

You should now see the GUIDO interface running locally.

## Other Tools

The entire CADOCS tool is composed of three modules:
- **GUIDO** (this repository): The desktop application
- **CADOCS** [link](https://github.com/gianwario/CADOCS): it is the original tool.
- **csDetector** [link](https://github.com/PaoloCarmine1201/csDetector): the augmented and wrapped version of csDetector, used in our tool to detect community smells and other socio-technical metrics. The link is referred to our modified versions of the tool.

## Detectable Community Smells

The complete list of detectable community smells—through the use of csDetector—and the associated refactoring strategies.

| Community Smell | Description | Refactoring Strategies |
|---|---|---|
| Organizational Silo | Siloed areas of the community that do not communicate except through one or two of their respective members. | Restructure the community, create a communication plan, mentor, conduct a cohesion exercise, monitor, and introduce a social-rewarding mechanism. |
| Black Cloud | Information overload is due to a lack of structured communications or cooperation governance. | Create a communication plan, Restructure the community, and Introduce a Social sanctioning mechanism. | 
| Radio Silence | One interposes herself into every formal interaction across more sub-communities with little flexibility to introduce other channels. | Restructure the community, Create a communication plan, Mentoring, Cohesion exercising, Monitoring, and Introduce a Social sanctioning mechanism. | 
| Prima Donnas | A team of people is unwilling to respect external changes from other team members due to inefficiently structured collaboration. | NA | 
| Sharing Villainy | Cause of a lack of information exchange, team members share essential knowledge such as outdated, wrong, and unconfirmed information. | NA | 
| Organizational Skirmish | A misalignment between different expertise levels of individuals involved in the project leads to dropped productivity and affects the project's timeline and cost. | NA | 
| Solution Defiance | The development community presents different levels of cultural and experience background, leading to the division of the community into similar subgroups with completely conflicting opinions. | NA | 
| Truck Factor Smell | Risk of significant knowledge loss due to the turnover of developers resulting from the fact that project information and knowledge are concentrated in a minority of the developers. | NA | 
| Unhealthy Interaction | Long delays in stakeholder communications cause slow, light, and brief conversations and discussions. | NA | 
| Toxic Communication | Toxic interactions and conflicting opinions among developers could push them to leave the project. | NA |

