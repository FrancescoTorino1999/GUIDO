# CADOCS II

## Introduction

**CADOCS II** Is a conversational agent designed to operate locally, accessible through an executable file, enabling the identification and management of *community smells* in software development communities on GitHub.

This repository hosts the modifications made to the original CADOCS repository, a tool used for Slack interactions.

## Other Tools

The entire CADOCS tool is composed of three modules:
- **CADOCS II** (this repository): The desktop application
- **CADOCS**: it is the Slack App used to interact with users.
- **CADOCS_NLU_Model** [link](https://github.com/alfcan/CADOCS_NLU_Model): it is the ML service used to interpret the users' intents.
- **csDetector** [link](https://github.com/PaoloCarmine1201/csDetector): the augmented and wrapped version of csDetector, used in our tool to detect community smells and other socio-technical metrics.
The links are referred to our modified versions of the tools.

## Detectable Community Smells

The complete list of detectable community smells—through the use of csDetector—and the associated refactoring strategies.

| Community Smell | Description | Refactoring Strategies |
|---|---|---|
| Organizational Silo | Siloed areas of the community that do not communicate, except through one or two of their respective members. | Restructure the community, Create communication plan, Mentoring, Cohesion exercising, Monitoring, and Introducing a social-rewarding mechanism. |
| Black Cloud | Information overload due to lack of structured communications or cooperation governance. | Create communication plan, Restructure the community, and Introduce a Social sanctioning mechanism. | 
| Radio Silence | One interposes herself into every formal interaction across more sub-communities with little flexibility to introduce other channels. | Restructure the community, Create communication plan, Mentoring, Cohesion exercising, Monitoring, and Introduce a Social sanctioning mechanism. | 
| Prima Donnas | A team of people is unwilling to respect external changes from other team members due to inefficiently structured collaboration. | NA | 
| Sharing Villainy | Cause of a lack of information exchange, team members share essential knowledge such as outdated, wrong and unconfirmed information. | NA | 
| Organizational Skirmish | A misalignment between different expertise levels of individuals involved in the project leads to dropped productivity and affects the project's timeline and cost. | NA | 
| Solution Defiance | The development community presents different levels of cultural and experience background, leading to the division of the community into similar subgroups with completely conflicting opinions. | NA | 
| Truck Factor Smell | Risk of significant knowledge loss due to the turnover of developers resulting from the fact that project information and knowledge are concentrated in a minority of the developers. | NA | 
| Unhealthy Interaction | Long delays in stakeholder communications cause slow, light and brief conversations and discussions. | NA | 
| Toxic Communication | Toxic interactions and conflicting opinions among developers could push them to leave the project. | NA |

## How to Install The Tool:

There are several ways to install the tool. We discuss them individually below.

### Docker Image pull ARM64
1. Run the following command:
   ```bash
   docker pull leopoldotodisco/guido-backend:1.0
2. Run the command: 
    ```bash 
    docker pull leopoldotodisco/guido-frontend:1.0
3. Configure and start backend container backend via Docker Desktop:
	- Open Docker Desktop.
	- Go in section “Images”.
	- find the image leopoldotodisco/guido-backend:1.0 and click on Play button.
	- In *additional options*, add PAT in Env Variables.
	- Set 5005 as port number.
4. Configure and start backend container backend via Docker Desktop:
	- In Docker Desktop, Go in section “Images”.
	- find the image leopoldotodisco/guido-frontens:1.0 and click on Play button.
	- Set 3000 as port number.
5. Start you brand new containers

### Local Docker Build
1. Clone our Repository
2. Go in folder "docker" and add your PAT in dockerfile
3. Run the following commands:
 ```bash
    docker-compose build
    docker compose up
