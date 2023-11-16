# MalwareDetector

In this new era of on-demand virtual computing, security is of utmost importance. Recently, various security incidents have been reported by companies in the virtualization servers which raises a strong security concern towards designing the virtualization specific security frameworks. Traditional malware analysis techniques and detection methods are insufficient in detecting and analyzing the rapidly growing malware.

A windows malware analysis framework is proposed in Xen-based architecture to address the recent cyber-attacks on crucial virtualized ecosystems. The framework has been implemented successfully using recent windows malware dataset (executables) collected from online sources. 

A test bed set up has been created in the lab to perform malicious process injection and memory tracing using kernel debugging based introspection mechanism.The logs are pre-processed and analysed. We have primarily considered process control related syscall operations and dlls invocations during extracting features at the hypervisor which are further analysed using machine learning algorithms. The approach provides the promising results.

## Analysis setup

Memory introspection is used to track all process activity occurring at the kernel level while they are executing inside the compromised VM. An out-VM monitoring method is needed to monitor the system-level runtime state of the VM from the outside in order to combat sophisticated malware. Open source tools, which track the heap allocations and internal kernel operations, intercept Xen events, and map guest memory to host memory, have been used to keep the security system's stealthiness. When an event occurs, the currently running process undergoes scanning for loaded libraries. The process activity tracing commences its operation once the malware analysis tools are deployed on bare-metal machines, as elaborated in the following section. You can find instructions on how to set up these prerequisites by referring to the following [link](https://github.com/acsr-du/analysisEnvironmentV0.1.git).

## Preprocessing of generated logs

Significant features are extracted from the unstructured raw logs. The system call is regarded as a crucial attribute throughout the entire process execution tracing log. The combination of both syscall and DLL makes the proposed methodology distinctive.The structured, pre-processed dataset is subsequently subjected to further cleaning and standardization, preparing it for the learning and testing phases.

## Behaviour analysis
The proposed framework employs a Random Forest (RF) as a classifier for malware detection. The RF algorithm is a supervised ensemble learning technique. During the training phase, RF constructs multiple decision trees using bagging techniques, where each tree is built from a random sample. 

