# MalwareDetector

In the dynamic realm of virtual computing, security is paramount. Recent incidents in virtualization servers emphasize the need for advanced security frameworks. Conventional malware analysis falls short, prompting the proposal of a Xen-based Windows malware framework for resilient defense.

This framework, implemented successfully with a recent dataset, incorporates a lab test bed for executing malicious processes and kernel-level memory tracing. Meticulous pre-processing and analysis of logs, emphasizing hypervisor-level syscall operations and DLL invocations, provide a robust foundation for subsequent machine learning algorithms, yielding promising results.

### Analysis setup

Memory introspection tracks process activities at the kernel level within the compromised VM. An out-VM monitoring method enables system-level runtime state monitoring externally. Open-source tools intercept Xen events, map guest memory to host memory, maintaining security system stealthiness. Event-driven scanning focuses on loaded libraries within the running process. Deployment on bare-metal machines initiates process activity tracing.

Setup instructions here. [link](https://github.com/acsr-du/analysisEnvironmentV0.1.git).

### Preprocessing of generated logs

A critical phase involves extracting significant features from unstructured raw logs. System calls emerge as pivotal attributes throughout the entire process execution tracing log. The distinctiveness of the proposed methodology lies in combining both syscall and DLL information. The resultant structured and pre-processed dataset undergoes further cleaning and standardization, preparing it for subsequent learning and testing phases.

Pythom programs to generate the required csv are uploaded here - [link](https://github.com/acsr-du/malwareDetectorV0.1/tree/8a454289226f5e82cc3c801070553be37d4633d0/logsPreprocessingCodes)

### Behaviour analysis

The chosen framework adopts a Random Forest (RF) as a classifier for malware detection. RF, a supervised ensemble learning technique, constructs multiple decision trees during the training phase. Bagging techniques are employed, with each tree built from a random sample. This approach enhances the model's robustness and effectiveness in discerning malicious patterns within the analyzed dataset.

Classifier program - [link](https://github.com/acsr-du/malwareDetectorV0.1/blob/302cf466945f74104353106e485a3d3bbb2e52f0/src/ml/classifiers.py)

*Note - Current framework has been implemented considered using the dataset genrated in our lab [four malware, one benign]. In presently, we have considered four malware families due to time and resource constraints. However, the proposed framework can be scalable.*

Sample of Logs and csv - [link](https://github.com/acsr-du/malwareDetectorV0.1/tree/ae99451f5783783a254526c33578105bde77a11a/sample)

### Installation

- Clone the repository to your local machine
  
```
sudo apt-get install git git-lfs python3-pip
sudo su
cd /var/
git clone https://github.com/acsr-du/malwareDetectorV0.1.git
exit
cd /var/malwareDetectorV0.1/
pip install -r requirements.txt
```

- Take full permission to make folder completely accessible

```
sudo chown -R (pc-name) /var/malwareDetectorV0.1
```

- Check Streamlit Is Working.
  
```
streamlit hello 
```
A streamlit web interface should load up which is hosted locally. To close the interface, use Ctrl+C in the terminal.

## Usage guide

- Change terminal working directory to malwareDetectorV0.1

```
cd /var/malwareDetectorV0.1/
```

- Initialize the web-app

```
streamlit run src/Home.py
```
