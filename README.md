# SCHEDULED RELEASE DATE: September 15, 2022

This project was initially made as a fork of the Kicom anti-virus and distributed as closed source. The aim of this repo is to make a version from scratch with some key upgrades/feature additions and obviously to make it open source!

This is the first software deliverable of the AcuAngleSecurity company located at https://acuanglesecurity.com.

# Key Components
- Atomic Predicate integration
- Expanded node distribution model concerning sandboxed services
- High detection rate
- Low resource usage
- Real time protection
- Blockchain DAPP recursive detention


# Generic Architecture:
- GUI: No administrative rights, WEAK
- Guard DLL: web browser protection, MEDIUM
- Service: Admin rights. Serves as a gateway to kernel code and take decisions along with some database, STRONG
- Driver: Kernel filters, STRONG

## GUI
Doesn’t need any administrative right, it only takes user actions and transmits them to the service. It also displays product status. Nothing more, this is not its aim. If the GUI is killed, this is not a problem as the service should be able to restart it.

## Guard DLL
Are massively injected into all processes, and should be able to look for IAT hooks and/or malicious threads. They should be quite hard to unload or defeat. They are not critical but important.

## Service
Core of the product. Is unkillable, and is able to self-restart on kill. The service is responsible for communication between all modules of the product, it sends commands to drivers, takes commands from user, and queries the database for sample analysis. The "brain" of the module.

## Driver(s)
Tentacles that gather information on everything that happen on the system, and transmit them to the service for decision. They are also able to deny access to guarded places, based on service’s decision.

# Blockchain
- TODO: DAPP containerization: heavily decreases resource usage exponentially throughout the blockchain

# Visualization
This first model visualizes how services with single-layer child process are treated. In this case, **y** represents the child process of the service, **&** represents the containerized execution state of the child process, and **x** represents the user interaction with the child process.

Each user interaction with **x** sends an approval query to **&** and expects to receive a confirmation query from **&**, represented by the more frequent dashed lines.

This implementation can be scaled as much as desired, with no drastic impact on resource usage.

    - - - & --------- x - - -
    - - - \ - - - - - / - - -
    - - - - \ - - - / - - - -
    - - - - - \ - / - - - - -
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - y - - - - - - 

Thist second model visualizes how services with multi-layer child process are treated. In this case, **y** represents the initial child process of the service, **&** represents the containerized execution state of the initial child process, and **x** represents the user interaction with the initial child process. 

**a** and **b** are just the translations of **&** and **x**. **$** represents the containerized execution state of the second-layer child process. **o** represents the user interaction with the second-layer child process.

Each user interaction with **x** sends an approval query to **$** and expects to receive a confirmation query from **&**, represented by the more frequent dashed lines. The same happens between **$** and **o** in this model.

Again, this implementation can be scaled as much as desired, with no drastic impact on resource usage.

    $ - $ ------------- o - o
    \ - / - - - - - - - \ - /
    - | - - - - - - - - - | -
    - | - - - - - - - - - | -
    - a - - - - - - - - - b -
    - - \ - - - - - - - / - -
    - - - & --------- x - - -
    - - - \ - - - - - / - - -
    - - - - \ - - - / - - - -
    - - - - - \ - / - - - - -
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - | - - - - - - 
    - - - - - - y - - - - - - 
# 1st Fundamental Implemented: Security Standards
Security standards provide developers and application testers with guidance on what your company will accept and what it won’t. They are essential to maintaining consistency across your supply chain.

When security standards are documented and widely communicated, developers understand rules for the type of code they may use (e.g., COTS, open source, libraries) and the security requirements they must incorporate in their programs (e.g., specific crypto algorithms they must use or coding practices they must avoid).

# 2nd Fundamental Implemented: Security Policies
Security policies ensure that everyone involved shares a common definition of terms, understands roles and responsibilities, and has a set of operating procedures and governance rules to follow. Creating security policies paves the way for your team to follow the standards defined by your software security initiative.

Security policies typically cover:

Application testing. Define risk classifications. Determine which applications must be tested and which gates they must pass.
Remediation. Set expectations for fixing bugs and flaws.
Network security. Determine protocols and authorization levels.
Data security. Protect your valuable IP and sensitive customer data.
Physical security. Govern access control and secure your infrastructure.
Disaster recovery. Determine steps to take in the event of an attack, including reporting, recording, and resolution.

# 3rd Fundamental Implemented: Security metrics
To demonstrate the results of the software security initiative and  progress over time, a defined set of metrics (both strategic and operational) was established.
- Amount and cost of resources to ensure application security
- Number of critical applications that must undergo in-depth testing
- Number of tested applications
- Time to run test per application
- Time from design to launch to create a secure application
- Number of applications that meet or exceed compliance requirements
- Number of bugs in code that reach production
