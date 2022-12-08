Global Architecture:
GUI: No administrative rights, WEAK
Guard DLL: web browser protection, MEDIUM
Service: Admin rights. Serves as a gateway to kernel code and take decisions along with some database, STRONG
Driver: Kernel filters, STRONG

The GUI doesn’t need any administrative right, it only takes user actions and transmits them to the service. It also displays product status. Nothing more, this is not its aim. If the GUI is killed, this is not a problem as the service should be able to restart it.

The guard DLLs (if any), are massively injected into all processes, and should be able to look for IAT hooks and/or malicious threads. They should be quite hard to unload or defeat. They are not critical but important.

The service is the core of the product. It should be unkillable, or at least should be able to self-restart on kill. The service is responsible for communication between all modules of the product, it sends commands to drivers, takes commands from user, and queries the database for sample analysis. This is the brain.

The kernel drivers are also critical. They are the tentacles that gather information on everything that happen on the system, and transmit them to the service for decision. They are also able to deny access to guarded places, based on service’s decision.

IMPORTANT TO MAKE SURE IN CODE THAT YOU FOCUS ON NETWORKING OF THE SERVICE

The analysis engine is one of the most important part, it’s responsible for analysing file/memory samples coming from the drivers. If must be fast (even with a huge database), and should be able to handle most of the file types (Self-extracted executables, Archives – RAR, ZIP, Packed files – UPX, … ) and thus should have many modules to do this:

Unpacker : That module must be able to detect and unpack most of the known packers (UPX, Armadillo, ASPack, …)
Signature engine: The database of an antivirus contains millions of signatures, and the engine should be able to fast search for them into a sample. Thus, a very powerful algorithm should be part of it. Some examples : AhoCorasick, RabinKarp, string matching algorithms.
Sandbox : That module is not necessary, but would be a plus to be able to run samples into a limited memory, with no effect on the system. That could help to unpack samples packed with unknown packers, and help the heuristic engine (see after) to detect API calls that could be considered as suspicious or malicious. Some good sandbox here.
Heuristic engine : As said above, the heuristic engine does not search for signatures, but rather look for suspicious behaviour (ie. sample that opens a connexion on the website hxxp://malware_besite.com). That can be done by static analysis, or through a sandbox.



1ST fundamental: Security standards
Security standards provide developers and application testers with guidance on what your company will accept and what it won’t. They are essential to maintaining consistency across your supply chain.

When security standards are documented and widely communicated, developers understand rules for the type of code they may use (e.g., COTS, open source, libraries) and the security requirements they must incorporate in their programs (e.g., specific crypto algorithms they must use or coding practices they must avoid).



2ND fundamental: Security policies
Security policies ensure that everyone involved shares a common definition of terms, understands roles and responsibilities, and has a set of operating procedures and governance rules to follow. Creating security policies paves the way for your team to follow the standards defined by your software security initiative.

Security policies typically cover:

Application testing. Define risk classifications. Determine which applications must be tested and which gates they must pass.
Remediation. Set expectations for fixing bugs and flaws.
Network security. Determine protocols and authorization levels.
Data security. Protect your valuable IP and sensitive customer data.
Physical security. Govern access control and secure your infrastructure.
Disaster recovery. Determine steps to take in the event of an attack, including reporting, recording, and resolution.



3RD fundamental: Security metrics
To demonstrate the results of your software security initiative and track your progress over time, you must establish a defined set of metrics.

Some examples of strategic and operational metrics:

Amount and cost of resources to ensure application security
Number of critical applications that must undergo in-depth testing
Number of tested applications
Time to run test per application
Time from design to launch to create a secure application
Number of applications that meet or exceed compliance requirements
Number of bugs in code that reach production



Receive process name, the file object, the PID, and so. As the process is pending, the driver can tell its service to analyse the process's memory for anything malicious. If it finds something, the driver will simply set CreationStatus to FALSE and return.

Make a NDIS and TDI for low level IP filtering driver.

Make userland protection to protect against process spies and Trojan Bankers more importantly. 
This will both kill malicious processes, and will able to guard critical processes like bank info, etc.

Use AppInitDII registry key to register the protector DLL. It will load the DLL into every process started on the system.


As far as the registry goes, I would have to add rules for failures in the system manager and set every failure rule to restart the service. Because of this, I would be able to debug the process for malware, since when the service is not stopped by service manager, ther service restarts.
-An alternative method for this could be to set callbacks on the process handles.


The final step in the antivirus would be the GUI portion. It needs to be visibly beautiful in every shape to attract clients and companies alike. Also must be easily maneuverable to maximize efficiency of anti virus. 

Critera:
    Detection Rate
    Resource Usage
    Real Time Protection
