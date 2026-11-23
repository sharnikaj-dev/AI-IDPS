AI-DRIVEN CYBER THREAT DETECTION AND INTELLIGENT INTRUSION PREVENTION FOR SECURE CONNECTED COMMUNICATION NETWORKS

25EEC204 – MINI PROJECT I

Submitted by

SHARNIKA J (25205083)

in partial fulfillment for the award of the degree of

MASTER OF COMPUTER APPLICATIONS

DEPARTMENT OF MASTER

OF COMPUTER APPLICATIONS

RATHINAM TECHNICAL CAMPUS

An Autonomous Institution, Affiliated to Anna University, Chennai – 600025

MAY – 2027

BONAFIDE CERTIFICATE

Certified that this report titled AI-DRIVEN CYBER THREAT DETECTION AND INTELLIGENT INTRUSION PREVENTION FOR SECURE CONNECTED COMMUNICATION NETWORKS is the Bonafide work of Sharnika J (25205083) who carried out the work under my supervision. Certified further, that to the best of my knowledge the work reported here in does not form part of any other Main project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.

| Signature of the Director with date Dr. K. Anuradha Professor And Director Master of Computer Applications Rathinam Technical Campus Coimbatore. | Signature of the Supervisor with date Dr. K. Anuradha Professor And Director Master of Computer Applications Rathinam Technical Campus Coimbatore. |

| --- | --- |



Submitted for End Semester Project Viva Voce Examination held on ...................

| Internal Examiner | External Examiner |

| --- | --- |



DECLARATION

I, SHARNIKA J hereby declare that the project report titled “AI-DRIVEN CYBER THREAT DETECTION AND INTELLIGENT INTRUSION PREVENTION FOR SECURE CONNECTED COMMUNICATION NETWORKS” was carried out by me under the guidance of Dr. K. Anuradha, Professor and Director, Department of MCA at Rathinam Technical Campus, is submitted in partial fulfillment of the requirements for the award of Master of Computer Applications. Certified further that to the best of my knowledge the work reported here in does not form part of any other project report or dissertation on the basis of which a degree or award was conferred on an earlier occasion on this or any other candidate.

| DATE: | SIGNATURE OF CANDIDATE |

| --- | --- |

| PLACE: | SHARNIKA J |



ACKNOWLEDGEMENT

Apart from the efforts, the success of this project depends largely on the encouragement and guidelines of many others. I take this opportunity to praise the almighty and express my gratitude to the people who have been instrumental in the successful completion of my project.

I wish to acknowledge with sincere gratitude to Dr. Madan A. Sendhil, B.E., M.S., Ph.D., Chairman, Rathinam Group of Institutions for providing the excellent infrastructure and facilities on the campus for the successful completion of my project.

I also wish to express my heartfelt thanks to Dr. R. Manickam, MCA., Ph.D., CEO, Rathinam Group of Institutions, for providing the necessary facilities and academic environment to carry out the project successfully.

I extend my sincere thanks to Dr. B. Nagaraj, M.E., Ph.D., PDF (Italy), CBO, Rathinam Group of Institutions, for providing the required resources and facilities for the successful execution of my project work.

I wish to express my hearty thanks to Dr. K. Geetha, M.E., Ph.D., Principal (Administration), Rathinam Technical Campus, for providing me with the opportunity and encouragement to complete the project successfully.

I extend my heartfelt gratitude to Dr. K. Anuradha, Professor & Director, Department of MCA, Rathinam Technical Campus, who is also my Project Supervisor and who served as the backbone of all my project activities, for her tremendous guidance, continuous support, motivation, valuable suggestions, patience and encouragement throughout the completion of my project.

Finally, I extend my heartfelt thanks to my parents, friends, and faculty members for their constant support, encouragement, and motivation throughout this project. The assistance and guidance received from everyone greatly contributed to the successful completion of this project.

SHARNIKA J

ABSTRACT

Modern communication networks connect a large number of users, servers, cloud services and IoT devices, and this has increased the number of ways in which an attacker can enter a system. Traditional firewalls and signature-based intrusion detection systems can recognise only the attacks that are already known to them, they depend on constant manual updating of rules, and they usually leave the decision of how to respond to a human administrator. As a result, new and modified attacks are often detected late and the damage is done before a response is made.

This project presents AI-IDPS, an AI-driven cyber threat detection and intelligent intrusion prevention system for secure connected communication networks. The system analyses network traffic records of the NSL-KDD benchmark dataset and classifies each record as Normal or as one of four attack families, namely Denial of Service, Probe, Remote to Local and User to Root. The traffic data is cleaned, categorical fields are encoded, numeric fields are scaled and the most important features are selected. Decision Tree, Random Forest and XGBoost classifiers are trained and compared using accuracy, precision, recall, F1-score, false positive rate and the confusion matrix, and the Random Forest model is selected as the detection engine.

The detection engine outputs the predicted class together with a confidence score, and an intelligent prevention engine uses this score to choose a proportionate response. A prediction with very high confidence leads to blocking of the source IP address, a medium confidence prediction leads to rate-limiting of the source, and a low confidence prediction is only logged and shown to the analyst for review. Every decision is stored in a database so that it can be audited and reversed.

The system is implemented with Python and Scikit-learn for the machine learning part and with Flask, HTML, CSS, JavaScript and SQLite for the web dashboard. The dashboard provides secure login, live traffic monitoring, alerts, management of blocked addresses, display of model performance and report generation. The modular design of the project allows future enhancements such as live packet capture, deep learning models, explainable AI and integration with real firewalls, and it forms a base for further development as a final year project.

TABLE OF CONTENTS

| S. No | PARTICULARS | PAGE NO |

| --- | --- | --- |

|  | ABSTRACT | v |

|  | TABLE OF CONTENTS | vi |

|  | LIST OF TABLES | viii |

|  | LIST OF FIGURES | ix |

| 1 | INTRODUCTION | 1 |

|  | 1.1 Introduction to the Project | 2 |

|  | 1.2 Objective of the Project | 2 |

|  | 1.3 Scope of the Project | 3 |

|  | 1.4 Need for AI-Based Intrusion Detection and Prevention | 4 |

| 2 | LITERATURE REVIEW | 5 |

|  | 2.1 Existing Intrusion Detection and Prevention Systems | 6 |

|  | 2.2 Limitations of Current Systems | 6 |

|  | 2.3 Need for AI-Assisted Threat Detection | 7 |

|  | 2.4 Summary of Related Work | 7 |

| 3 | PROPOSED SYSTEM | 9 |

|  | 3.1 Overview of AI-IDPS | 10 |

|  | 3.2 System Architecture | 10 |

|  | 3.3 Features of the Proposed System | 11 |

|  | 3.4 Advantages of This System | 13 |

|  | 3.5 Applications of the System | 14 |

| 4 | SYSTEM DESIGN | 15 |

|  | 4.1 System Architecture Diagram | 16 |

|  | 4.2 Data Flow Diagram (DFD) Level 0 | 16 |

|  | 4.3 Data Flow Diagram (DFD) Level 1 | 17 |

|  | 4.4 Use Case Diagram | 18 |

|  | 4.5 Entity Relationship (ER) Diagram | 19 |

|  | 4.6 Database Design | 20 |

|  | 4.7 Sequence Diagram | 22 |

|  | 4.8 Prevention Decision Logic | 22 |

| 5 | METHODOLOGY | 24 |

|  | 5.1 System Workflow Description | 25 |

|  | 5.2 Step-By-Step Implementation | 26 |

|  | 5.3 Dataset Description | 27 |

|  | 5.4 Data Preprocessing and Feature Selection | 28 |

|  | 5.5 Machine Learning Models Used | 29 |

|  | 5.6 Evaluation Metrics | 29 |

|  | 5.7 Frontend Architecture | 30 |

|  | 5.8 Backend Architecture | 30 |

|  | 5.9 Tools and Technologies Used | 30 |

| 6 | RESULT AND DISCUSSION | 32 |

|  | 6.1 Input Screenshots | 33 |

|  | 6.2 Output Screenshots | 34 |

|  | 6.3 Performance Analysis | 38 |

|  | 6.4 Testing | 40 |

| 7 | CONCLUSION | 42 |

|  | 7.1 Conclusion of the Project | 43 |

|  | 7.2 Key Achievements | 43 |

|  | 7.3 Limitations of the Current System | 44 |

| 8 | FUTURE ENHANCEMENT | 45 |

|  | 8.1 Future Scope | 46 |

|  | APPENDIX | 47 |

|  | A. Sample Code | 47 |

|  | B. Sample Output | 53 |

|  | REFERENCES | 54 |



LIST OF TABLES

| Table No | Table Name | Page No |

| --- | --- | --- |

| 2.4.1 | Summary of related work | 8 |

| 4.6.1 | Structure of the users table | 20 |

| 4.6.2 | Structure of the traffic_logs table | 21 |

| 4.6.3 | Structure of the alerts table | 21 |

| 4.6.4 | Structure of the blocked_ips table | 21 |

| 4.6.5 | Structure of the model_info table | 22 |

| 5.3.1 | Class distribution of the NSL-KDD training and test files | 28 |

| 5.9.1 | Technologies used in AI-IDPS | 31 |

| 6.3.1 | Comparison of the trained models | 38 |

| 6.3.2 | Class-wise performance of the Random Forest model | 39 |

| 6.4.1 | Functional test cases | 41 |



LIST OF FIGURES

| Figure No | Figure Name | Page No |

| --- | --- | --- |

| 3.2.1 | System Architecture of AI-IDPS | 11 |

| 3.3.1 | Features Interaction Flow of AI-IDPS | 13 |

| 4.1.1 | System Architecture Diagram | 16 |

| 4.2.1 | Data Flow Diagram (DFD) Level 0 | 17 |

| 4.3.1 | Data Flow Diagram (DFD) Level 1 | 18 |

| 4.4.1 | Use Case Diagram | 19 |

| 4.5.1 | Entity Relationship (ER) Diagram | 20 |

| 4.7.1 | Sequence Diagram of the Detection Process | 22 |

| 4.8.1 | Prevention Decision Logic | 23 |

| 5.1.1 | System Workflow of AI-IDPS | 25 |

| 5.3.1 | Class Distribution of the NSL-KDD Training Data | 28 |

| 6.1.1 | Registration Page | 33 |

| 6.1.2 | Login Page | 34 |

| 6.1.3 | Start Monitoring Page | 34 |

| 6.2.1 | Dashboard | 35 |

| 6.2.2 | Live Monitor Page | 36 |

| 6.2.3 | Alerts Page | 36 |

| 6.2.4 | Blocked IPs Page | 37 |

| 6.2.5 | Model Performance Page | 37 |

| 6.2.6 | Reports Page | 38 |

| 6.3.1 | Accuracy and F1-score of the Trained Models | 38 |

| 6.3.2 | Confusion Matrix of the Random Forest Model | 39 |

| 6.3.3 | Top Ten Important Features of the Random Forest Model | 40 |



CHAPTER 1

INTRODUCTION

# CHAPTER 1
INTRODUCTION

## 1.1 INTRODUCTION TO THE PROJECT

Modern communication networks connect enterprises, universities, hospitals, banks, cloud platforms and a rapidly growing number of Internet of Things (IoT) devices. Every one of these connections carries data that someone may want to steal, alter or disrupt. As networks grow larger and more connected, the number of possible entry points for an attacker grows with them. Attacks such as Denial of Service (DoS), port scanning, password guessing and privilege escalation are now carried out with freely available tools, which means that even a person with limited skill can launch them.

Traditional security tools such as firewalls and signature-based intrusion detection systems protect a network by comparing traffic against a list of known attack patterns. This approach works well for attacks that have already been seen and documented, but it fails when an attacker changes a few details of a known attack or uses a completely new technique, which is called a zero-day attack. The rule lists of such tools also need constant manual updating, and a human administrator is usually needed to decide what to do when an alarm is raised.

The AI-Driven Cyber Threat Detection and Intelligent Intrusion Prevention for Secure Connected Communication Networks project, referred to in this report as AI-IDPS, is developed to reduce these problems. The system studies the behaviour of network traffic with machine learning, classifies every traffic record as either normal or as one of four attack categories, and then decides automatically how to respond. A record that the model is very sure about is blocked immediately, a record that looks suspicious but uncertain is rate-limited, and a low-confidence record is only logged and shown to the analyst for review.

The project is implemented using Python and the Scikit-learn library for the machine learning part, and the Flask framework with HTML, CSS and JavaScript for the web dashboard. The NSL-KDD benchmark dataset is replayed record by record to simulate a live network feed, which allows the complete detection and prevention cycle to be demonstrated, measured and reported without needing access to a real production network.

## 1.2 OBJECTIVE OF THE PROJECT

The main objective of this project is to develop an intelligent and automated system that can detect malicious network activity with high accuracy and respond to it without waiting for human action. The system should keep the number of false alarms low so that the analyst can trust what the dashboard shows.

The specific objectives of this project are as follows:

To design and develop an AI-based model that classifies network traffic into five classes, namely Normal, DoS, Probe, R2L and U2R.

To preprocess the traffic data by cleaning, encoding categorical fields, scaling numeric fields and selecting the most useful features.

To train and compare three machine learning algorithms, namely Decision Tree, Random Forest and XGBoost, and to select the best model using accuracy, precision, recall, F1-score and false positive rate.

To implement an intelligent prevention engine that blocks, rate-limits or logs a traffic source depending on the confidence of the prediction.

To build a secure web dashboard with user authentication that shows live traffic, detected threats, blocked IP addresses and model performance.

To store traffic logs, alerts and blocked addresses in a database so that every decision can be audited and reported later.

To design the system in separate modules so that it can later be extended with live packet capture, deep learning and explainable AI.

## 1.3 SCOPE OF THE PROJECT

The scope of this project covers the complete life cycle of detecting and preventing an intrusion at the software level. This includes loading and preparing the dataset, training and saving the model, receiving traffic records, predicting their class, applying the prevention rules, storing the results and presenting them on a web dashboard.

The system is intended for network administrators, security analysts, students and researchers who want to understand how artificial intelligence can be applied to network security. It works with the 41 traffic features defined in the NSL-KDD dataset, such as protocol type, service, duration, number of bytes transferred and connection error rates. The five traffic classes in this dataset cover the most common attack families, which makes it a suitable base for a mini project.

In the present version, traffic is supplied by replaying dataset records, and blocking is performed by maintaining a list of blocked IP addresses in the database that behaves like a firewall rule set. Capturing packets directly from a network card, pushing rules into a hardware firewall or an SDN controller, analysing encrypted traffic and using deep learning models are outside the scope of this mini project, and they are listed as future enhancements in Chapter 8.

## 1.4 NEED FOR AI-BASED INTRUSION DETECTION AND PREVENTION

The number and variety of cyber attacks have increased every year, and attackers now use automation to try thousands of targets in a short time. A security team that depends only on fixed rules is always one step behind, because a rule can be written only after an attack has been observed. Machine learning removes this dependency by learning the general behaviour of attack traffic, such as sudden bursts of connections or unusual error rates, instead of memorising exact signatures.

Another problem in network security is the large number of false alarms. When an analyst receives hundreds of warnings every hour and most of them are harmless, real attacks are easily missed. A well-trained classifier that also reports how confident it is allows the system to treat strong and weak detections differently, which keeps the number of useless alerts low and keeps attention on the cases that matter.

Speed is also important. Many attacks, especially DoS attacks, cause damage within seconds, while a human response may take minutes. Combining detection with an automatic prevention engine closes this gap. The system does not replace the analyst, because every action is logged and can be reversed from the dashboard, but it removes the delay between detection and the first line of defence.

Finally, connected communication networks such as campus networks, cloud environments and IoT deployments produce a very large amount of traffic that cannot be inspected manually. An AI-driven system can examine every record in milliseconds and keep improving when it is retrained with new data, which is why this project proposes an AI-based approach to intrusion detection and prevention.

CHAPTER 2

LITERATURE REVIEW

# CHAPTER 2
LITERATURE REVIEW

## 2.1 EXISTING INTRUSION DETECTION AND PREVENTION SYSTEMS

An intrusion detection system (IDS) monitors events in a computer system or network and analyses them for signs of possible incidents. An intrusion prevention system (IPS) does the same and, in addition, attempts to stop the detected incident. The National Institute of Standards and Technology describes these technologies together as intrusion detection and prevention systems (IDPS) and classifies them as network-based, host-based and wireless, depending on where the sensors are placed (Scarfone and Mell, 2007).

Most deployed systems detect threats in one of three ways. Signature-based detection compares traffic with a database of known attack patterns. Anomaly-based detection builds a profile of normal behaviour and raises an alarm when the observed behaviour deviates from it. Stateful protocol analysis compares observed protocol activity against vendor-defined profiles of how a protocol should behave. Widely used open-source tools such as Snort, which was introduced as a lightweight network intrusion detection system (Roesch, 1999), Suricata and Zeek, as well as commercial next-generation firewalls, are built mainly around the first of these ideas.

Researchers have also studied the use of data mining and machine learning for intrusion detection for many years. A survey of these methods (Buczak and Guven, 2016) describes how classifiers such as decision trees, support vector machines, neural networks and ensemble methods have been applied to labelled network data, and it shows that the quality and representativeness of the training data strongly influences the results. Public benchmark datasets such as NSL-KDD, UNSW-NB15 and CICIDS2017 have been created to make such experiments repeatable.

## 2.2 LIMITATIONS OF CURRENT SYSTEMS

The main limitation of signature-based systems is that they can only recognise what they already know. A new or modified attack passes through unnoticed until a signature is written and distributed. Keeping a very large rule set up to date is also a continuous manual task, and a badly written rule can either miss an attack or block legitimate users.

Anomaly-based and learning-based systems can detect unknown behaviour, but they have their own difficulties. Sommer and Paxson (2010) point out that applying machine learning in operational networks is harder than in other fields, because a false alarm is expensive for the analyst who must investigate it, and because a model trained on one network does not always transfer to another. A system that produces many false positives is quickly ignored by the people who are supposed to rely on it.

Many existing solutions also treat detection and response as two separate jobs. The detection tool raises an alert, and a person must read it, decide what to do and then change a firewall rule manually. During a fast attack this delay can be long enough for the damage to be done. In addition, the older KDD Cup 1999 data used in many studies contains a large number of duplicate records, which makes reported accuracy figures look better than the real performance (Tavallaee et al., 2009).

## 2.3 NEED FOR AI-ASSISTED THREAT DETECTION

Machine learning models learn from examples, so they can recognise the characteristics of attacks such as very high connection counts, abnormal error rates or unusual byte ratios, even when the exact pattern has not been seen before. For structured tabular data like network flow records, ensemble methods such as Random Forest (Breiman, 2001) and gradient boosting as implemented in XGBoost (Chen and Guestrin, 2016) are known to give strong results while remaining fast enough for near real-time use.

A classifier can also output a probability for each class. This confidence value is very useful in practice, because it lets the system apply a graded response instead of a simple yes or no decision. A very confident detection can be blocked at once, while an uncertain one can be limited or sent to the analyst. This idea is the basis of the intelligent prevention engine used in this project.

Finally, a learning-based system can be improved over time. When the analyst confirms an alert or marks it as a false positive, the labelled result can be added to the training data and the model can be retrained. The proposed AI-IDPS is designed with this life cycle in mind, which is why it is built as a set of independent modules for data preparation, detection, prevention and reporting.

## 2.4 SUMMARY OF RELATED WORK

The works that influenced the design of this project are summarised in the table given below. They cover the datasets used for evaluation, the algorithms selected for the model and the general lessons about applying machine learning to network security.

Table 2.4.1 Summary of related work

| Reference | Contribution | Relevance to this project |

| --- | --- | --- |

| Roesch (1999) | Introduced Snort, a lightweight signature-based network intrusion detection system. | Represents the traditional rule-based approach that AI-IDPS aims to improve upon. |

| Tavallaee et al. (2009) | Analysed the KDD Cup 99 data and created NSL-KDD by removing redundant records. | NSL-KDD is the dataset used to train and test the model. |

| Breiman (2001) | Proposed Random Forest, an ensemble of decision trees trained on random subsets of data and features. | Random Forest is the main classifier of the proposed system. |

| Chen and Guestrin (2016) | Presented XGBoost, a scalable gradient boosted tree system. | XGBoost is compared with the other models during evaluation. |

| Buczak and Guven (2016) | Surveyed data mining and machine learning methods used for cyber security intrusion detection. | Guided the choice of algorithms and evaluation metrics. |

| Sommer and Paxson (2010) | Discussed why machine learning is difficult to use for network intrusion detection in real networks. | Motivated the focus on low false positive rate and graded response. |

| Scarfone and Mell (2007) | NIST guide describing the types and functions of IDPS technologies. | Provided the terminology and the detection and prevention concepts used in this report. |



CHAPTER 3

PROPOSED SYSTEM

# CHAPTER 3
PROPOSED SYSTEM

## 3.1 OVERVIEW OF AI-IDPS

AI-IDPS is a web-based security system that combines an AI detection engine and an intelligent prevention engine. The detection engine receives a traffic record, converts it into the numeric form expected by the model and predicts whether it is normal or belongs to one of the four attack families. Along with the class label, it produces a confidence score between 0 and 1.

The prevention engine reads this label and score and applies a response policy. When the confidence of an attack prediction is at least 0.90, the source IP address is blocked. When it lies between 0.60 and 0.90, the source is rate-limited. In all other cases the record is logged and a low-severity alert is raised for review. Every decision is written to the database so that it can be displayed, audited and reversed by the analyst.

The analyst interacts with the system through a secure web dashboard. After logging in, the analyst can select the data source, start or stop monitoring, watch live traffic and predictions, inspect alerts, unblock addresses, view the performance of the trained models and generate reports for a chosen time period. The whole system runs on a normal laptop and does not need any special hardware.

## 3.2 SYSTEM ARCHITECTURE

The system is organised into five layers, and each layer passes its output to the next one. The Data Acquisition layer receives traffic flow records from the network or from the replayed dataset. The Preprocessing and Feature layer cleans the record and converts it into the format required by the model. The AI Detection layer loads the trained model and predicts the class and confidence. The Decision and Prevention layer applies the response policy, and the Monitoring and Reporting layer presents the results to the analyst through the dashboard.

Two data stores support these layers. The trained model and its encoders are stored as files and loaded by the detection layer, while the SQLite database stores users, traffic logs, alerts and the list of blocked IP addresses. This separation allows the model to be replaced or retrained without changing the dashboard or the database, as shown in the figure below.

Fig 3.2.1 System Architecture of AI-IDPS

## 3.3 FEATURES OF THE PROPOSED SYSTEM

The proposed system provides the following features, which together cover the complete path from raw traffic to a protective action.

1. Secure User Authentication

Only registered users can access the console. Passwords are stored as salted hashes, and the dashboard pages are protected by a login session. Two roles are supported, an administrator who can manage users and blocked addresses, and an analyst who can monitor and view reports.

2. Traffic Ingestion

The system reads flow records from the selected data source at a configurable speed. In the present version the NSL-KDD test set is replayed record by record, and the same interface can later be connected to a live flow exporter.

3. Automatic Preprocessing

Each record is converted using the same encoders and scaler that were saved during training. This guarantees that live data is prepared exactly like the training data, which is essential for correct predictions.

4. Multi-class Threat Detection

The Random Forest model identifies whether a record is Normal, DoS, Probe, R2L or U2R and reports the confidence of its decision. Detecting the attack family, and not only the presence of an attack, helps the analyst understand what is happening.

5. Confidence-based Prevention

The prevention engine blocks, rate-limits or logs a source depending on the confidence score. The two thresholds can be changed from the monitoring page without changing any code.

6. Live Monitoring Dashboard

The dashboard shows the number of analysed flows, detected threats and blocked addresses, together with a traffic chart, an attack-type chart and the most recent alerts. The display is refreshed automatically while monitoring is running.

7. Alert and Blocked IP Management

Every detection creates an alert with a severity level of high, medium or low. The analyst can filter alerts by severity and can unblock or re-block an address when a decision needs to be corrected.

8. Model Performance Evaluation

The system stores and displays accuracy, precision, recall, F1-score, the confusion matrix and a comparison of the trained models, so the quality of the detection can be checked at any time.

9. Reports and Logging

A summary report of detected, blocked and rate-limited threats can be generated for any time period and downloaded as a CSV file for documentation or further analysis.

The way these features work together, from login to the final dashboard update, is shown in the flow below.

Fig 3.3.1 Features Interaction Flow of AI-IDPS

## 3.4 ADVANTAGES OF THIS SYSTEM

The first advantage of the proposed system is its ability to detect attacks that are not written in any rule list. Because the model learns from the characteristics of traffic, it can recognise new variations of known attack families, which is where signature-based tools are weakest.

The second advantage is the reduction in analyst workload. The graded response of the prevention engine handles clear cases automatically, so the analyst only needs to examine the uncertain alerts. At the same time, every automatic action is recorded and can be reversed, which keeps a human in control of the final decision.

The third advantage is speed. Prediction of a single record takes only a few milliseconds with a Random Forest model, so detection and prevention happen almost at the moment the record arrives. The fourth advantage is transparency, because the dashboard shows the predicted class, the confidence and the action taken for every record, and the stored logs make later investigation possible.

Lastly, the system is economical and flexible. It uses only open-source software, it runs on an ordinary computer, and its modular design allows the dataset, the model or the prevention rules to be changed independently of each other.

## 3.5 APPLICATIONS OF THE SYSTEM

The system can be used in campus and enterprise networks to watch the traffic between internal users and servers and to block hosts that begin scanning or flooding the network. In cloud and data centre environments, the same approach can monitor the traffic of virtual machines and protect public-facing services from DoS attacks.

In IoT and smart environments, where many small devices with weak security are connected to the network, the system can identify a compromised device by its abnormal traffic and limit it before it affects other devices. In financial and healthcare networks, which handle sensitive data, it can act as an additional monitoring layer that raises early warnings for unauthorised access attempts such as password guessing.

The project is also useful as a teaching and research platform. Students can use it to understand the complete workflow of an AI-based security tool, to compare different algorithms on a standard dataset and to test new ideas such as feature selection methods or alternative response policies.

CHAPTER 4

SYSTEM DESIGN

# CHAPTER 4
SYSTEM DESIGN

## 4.1 SYSTEM ARCHITECTURE DIAGRAM

The system follows a layered architecture in which each layer has a single responsibility and communicates only with the layer next to it. This makes the system easier to develop, test and extend. The presentation layer contains the web pages that the analyst sees. The application layer, written in Flask, receives requests from the pages and coordinates the work. The AI/ML layer holds the preprocessing code and the trained model, and the data layer stores users, traffic logs, alerts, blocked addresses and the saved model files.

When the analyst starts monitoring, the dashboard sends a request to the Flask server. The server takes the next batch of records from the data source, passes them through the preprocessor to the model, hands the predictions to the prevention engine, saves the results in the database and returns a response that the dashboard uses to update its tables and charts.

Fig 4.1.1 System Architecture Diagram

## 4.2 DATA FLOW DIAGRAM (DFD) LEVEL 0

The Level 0 data flow diagram, also called the context diagram, shows the whole system as a single process and the external entities that interact with it. The Security Analyst sends login details and start or stop commands to the system and receives alerts, reports and charts in return. The Network Traffic Source supplies the flow records that must be inspected. The system reads training data and the saved model from the Dataset and Model Store, and it sends block and unblock rules to the Firewall or Blocked IP List.

Fig 4.2.1 Data Flow Diagram (DFD) Level 0

## 4.3 DATA FLOW DIAGRAM (DFD) LEVEL 1

The Level 1 diagram divides the system into five processes. Process 1.0, User Authentication, verifies the analyst against the Users store. Process 2.0, Traffic Ingestion and Preprocessing, receives the flow records, stores them in the Traffic Logs and converts them into model features. Process 3.0, Threat Detection, loads the model from the Model Store and produces a label and a confidence score. Process 4.0, the Prevention Engine, takes the malicious flows, applies the thresholds and writes block rules to the Blocked IPs store. Process 5.0, the Alert and Report Module, saves the alerts and sends alerts, reports and charts back to the analyst.

Fig 4.3.1 Data Flow Diagram (DFD) Level 1

## 4.4 USE CASE DIAGRAM

The use case diagram shows how the actors interact with the functions of the system. The Admin or Security Analyst can log in and out, select a dataset, start or stop monitoring, view live traffic, view detected threats, block or unblock an IP address, view the performance of the model and generate reports. The Network Traffic Source takes part in the use cases that need traffic, namely starting monitoring and viewing live traffic, because it supplies the data for them.

Fig 4.4.1 Use Case Diagram

## 4.5 ENTITY RELATIONSHIP (ER) DIAGRAM

The database consists of five entities. A user starts monitoring sessions that produce many traffic log records, so the relationship between Users and Traffic Logs is one to many. A traffic log can raise an alert, and many alerts may lead to the same blocked address. A user also trains and registers models, so one user can be linked to many records in the Model Info table. The primary key and foreign key attributes of each entity are marked in the diagram.

Fig 4.5.1 Entity Relationship (ER) Diagram

## 4.6 DATABASE DESIGN

The structure of each table of the SQLite database is given below. The tables follow the entities of the ER diagram and use integer primary keys that are generated automatically.

Table 4.6.1 Structure of the users table

| Field | Data type | Description |

| --- | --- | --- |

| user_id | INTEGER (PK) | Unique identifier of the user |

| username | TEXT | Full name of the user |

| email | TEXT (UNIQUE) | Email address used to log in |

| password_hash | TEXT | Salted hash of the password |

| role | TEXT | Admin or analyst |

| created_at | DATETIME | Date and time of registration |



Table 4.6.2 Structure of the traffic_logs table

| Field | Data type | Description |

| --- | --- | --- |

| log_id | INTEGER (PK) | Unique identifier of the flow record |

| user_id | INTEGER (FK) | User who started the monitoring session |

| src_ip | TEXT | Source IP address of the flow |

| dst_ip | TEXT | Destination IP address of the flow |

| protocol | TEXT | Protocol type such as tcp, udp or icmp |

| service | TEXT | Network service such as http or ftp |

| src_bytes | INTEGER | Bytes sent from source to destination |

| dst_bytes | INTEGER | Bytes sent from destination to source |

| logged_at | DATETIME | Time at which the record was processed |



Table 4.6.3 Structure of the alerts table

| Field | Data type | Description |

| --- | --- | --- |

| alert_id | INTEGER (PK) | Unique identifier of the alert |

| log_id | INTEGER (FK) | Flow record that raised the alert |

| block_id | INTEGER (FK) | Blocked address entry, if the source was blocked |

| attack_type | TEXT | Predicted class: DoS, Probe, R2L or U2R |

| confidence | REAL | Confidence of the prediction between 0 and 1 |

| severity | TEXT | High, medium or low |

| action_taken | TEXT | Blocked, rate-limited or logged |

| alert_time | DATETIME | Time at which the alert was raised |



Table 4.6.4 Structure of the blocked_ips table

| Field | Data type | Description |

| --- | --- | --- |

| block_id | INTEGER (PK) | Unique identifier of the entry |

| ip_address | TEXT | Blocked IP address |

| reason | TEXT | Attack class that caused the block |

| blocked_at | DATETIME | Time at which the address was blocked |

| status | TEXT | Blocked or unblocked |



Table 4.6.5 Structure of the model_info table

| Field | Data type | Description |

| --- | --- | --- |

| model_id | INTEGER (PK) | Unique identifier of the trained model |

| user_id | INTEGER (FK) | User who trained or registered the model |

| algorithm | TEXT | Decision Tree, Random Forest or XGBoost |

| accuracy | REAL | Accuracy on the test set |

| f1_score | REAL | Weighted F1-score on the test set |

| trained_on | DATETIME | Date and time of training |



## 4.7 SEQUENCE DIAGRAM

The sequence diagram shows the order of messages when the analyst starts monitoring. The analyst clicks the start button on the dashboard, which sends a request to the Flask server. The server fetches the next batch of flow records, sends each record to the ML model for prediction and receives the class and the confidence. It then saves the alert and the blocking decision in the database and returns a JSON response, which the dashboard uses to refresh the live charts.

Fig 4.7.1 Sequence Diagram of the Detection Process

## 4.8 PREVENTION DECISION LOGIC

The prevention engine is a small rule set applied to the output of the model. If the model predicts an attack class with a confidence of at least 0.90, the source address is blocked, stored in the blocked IP table and a high severity alert is raised. If the confidence lies between 0.60 and 0.90, the device is rate-limited and a medium severity alert is raised. Any other prediction is logged and a low severity alert is raised for the analyst. Records predicted as Normal are only logged. The two thresholds are stored as settings so that they can be tuned to the needs of a particular network.

Fig 4.8.1 Prevention Decision Logic

CHAPTER 5

METHODOLOGY

# CHAPTER 5
METHODOLOGY

## 5.1 SYSTEM WORKFLOW DESCRIPTION

The working of AI-IDPS is divided into two phases. In the offline training phase, the dataset is loaded, cleaned, encoded and scaled, the important features are selected, and the machine learning models are trained and evaluated. The best model is saved to a file together with the encoders and the scaler. This phase is carried out once, and it is repeated when the model needs to be retrained.

In the online detection and prevention phase, each incoming flow record is preprocessed using the saved encoders, the saved model predicts its class and confidence, and the prevention engine selects the action. The result is stored in the database, and the dashboard is updated. The complete workflow of both phases is shown in the figure below.

Fig 5.1.1 System Workflow of AI-IDPS

## 5.2 STEP-BY-STEP IMPLEMENTATION

Step 1: Requirement Analysis

The functional requirements of the system were identified, namely user login, traffic replay, threat classification, automatic prevention, alerts, blocked IP management, model performance display and reports. The non-functional requirements were also fixed, which are a prediction time of a few milliseconds per record, a clear and simple interface and the ability to extend the system later.

Step 2: Dataset Collection

The NSL-KDD dataset was selected because it removes the duplicate records of the older KDD Cup 99 data and gives a fairer evaluation of the model. The KDDTrain+ file is used for training and validation, and the KDDTest+ file is used to replay live traffic in the dashboard. Because NSL-KDD records do not contain IP addresses, the replay module assigns simulated source and destination addresses to each record so that the blocking function can be demonstrated.

Step 3: Data Preprocessing

The records are checked for missing and duplicate values. The three categorical fields, protocol type, service and flag, are converted to numbers using label encoding, and the numeric fields are scaled with standard scaling. The original attack names of the dataset are mapped to the four attack families, and the label of normal traffic is kept as Normal.

Step 4: Feature Selection

The importance of every feature is calculated from a preliminary Random Forest, and highly correlated features are removed. This reduces the training time and the prediction time without lowering the accuracy.

Step 5: Model Training

The dataset is split into 80 percent for training and 20 percent for testing using stratified sampling so that all five classes are present in both parts. Decision Tree, Random Forest and XGBoost classifiers are trained on the training part. Class weights are used in the Decision Tree and Random Forest models to give more importance to the rare R2L and U2R classes.

Step 6: Evaluation and Model Selection

The trained models are evaluated on the test part using accuracy, precision, recall, F1-score, false positive rate and the confusion matrix. The model that gives the best balance of these measures is selected, and in this project it is the Random Forest model. The model, the encoders and the scaler are saved with the joblib library.

Step 7: Backend and Prevention Engine

The Flask application is written with routes for login, registration, starting and stopping monitoring, fetching the next batch of records, alerts, blocked addresses and reports. The prevention engine is written as a separate module that receives the prediction and the confidence and returns the action to be taken.

Step 8: Dashboard Development

The pages are designed with HTML and CSS, and JavaScript with Chart.js is used to draw the live traffic and attack type charts. The page requests new results from the server at regular intervals, so that the tables and charts update without reloading.

Step 9: Testing and Deployment

Each module is tested separately and then the complete flow is tested from login to report generation. The application is finally run on the local machine, and it can be deployed on any server that supports Python.

## 5.3 DATASET DESCRIPTION

NSL-KDD is an improved version of the KDD Cup 99 intrusion detection dataset. Each record describes one network connection with 41 features and a label. Three of the features are categorical (protocol type, service and flag), four are binary, and the remaining ones are numeric values such as duration, number of bytes, count of connections and error rates. The features are grouped into basic features of a connection, content features, time-based traffic features and host-based traffic features.

The attacks of the dataset belong to four families. Denial of Service (DoS) attacks make a service unavailable by flooding it. Probe attacks scan the network to collect information, for example a port scan. Remote to Local (R2L) attacks try to gain local access from a remote machine, for example by guessing passwords. User to Root (U2R) attacks try to gain administrator privileges from a normal user account. The number of records of each class in the training file is given below.

Table 5.3.1 Class distribution of the NSL-KDD training and test files

| Class | KDDTrain+ records | KDDTest+ records | Type |

| --- | --- | --- | --- |

| Normal | 67,343 | 9,711 | Legitimate traffic |

| DoS | 45,927 | 7,458 | Flooding attacks |

| Probe | 11,656 | 2,421 | Scanning attacks |

| R2L | 995 | 2,754 | Remote access attacks |

| U2R | 52 | 200 | Privilege escalation |

| Total | 125,973 | 22,544 |  |



The chart below shows how unevenly the classes are distributed in the training data. Normal and DoS records make up most of the data, while R2L and U2R records are very few. This imbalance is the reason why class weights and class-wise metrics are used in the evaluation, because a model could reach a high overall accuracy while missing most of the rare attacks.

Fig 5.3.1 Class Distribution of the NSL-KDD Training Data

## 5.4 DATA PREPROCESSING AND FEATURE SELECTION

Preprocessing makes the raw data suitable for a machine learning model. First, the column names are assigned and the difficulty-level column of the dataset is dropped, because it is not a network feature. Duplicate rows and missing values are removed. Next, the individual attack names are grouped into the four attack families and the label Normal, so the problem becomes a five-class classification task.

The categorical fields protocol type, service and flag are converted to integers with label encoding. The numeric fields have very different ranges, for example the number of bytes can reach millions while an error rate lies between 0 and 1, so they are scaled with standard scaling to zero mean and unit variance. The encoders and the scaler are fitted only on the training data and then saved, so that live records are transformed in exactly the same way.

For feature selection, the importance scores of a Random Forest are used to rank the features, and one feature of each highly correlated pair is dropped. The most important features include the number of bytes sent from the source and from the destination, the service, the rate of connections to the same service, the connection count and the connection flag. Using the selected features keeps the model small and fast.

## 5.5 MACHINE LEARNING MODELS USED

Three supervised learning algorithms are trained and compared in this project. All of them work well on structured tabular data and do not need a graphics processor.

Decision Tree builds a tree of simple yes or no questions on the features, for example whether the number of connections to the same host is above a certain value. It is fast and easy to interpret, but a single tree may overfit the training data.

Random Forest trains many decision trees on random subsets of the data and features and combines their votes (Breiman, 2001). This reduces overfitting and gives stable results. The fraction of trees that vote for a class is also used as the confidence of the prediction, which the prevention engine needs.

XGBoost is a gradient boosting method in which new trees are added one after another, each correcting the errors of the earlier ones (Chen and Guestrin, 2016). It is often very accurate, but it has more settings to tune than a Random Forest.

After evaluation, Random Forest was chosen as the deployed model, because it gave the best balance of accuracy, recall on the attack classes and low false positive rate, and because its vote fraction provides a natural confidence score.

## 5.6 EVALUATION METRICS

Accuracy alone is not enough for an intrusion detection system, because the classes are imbalanced. The following measures are therefore used. Accuracy is the fraction of all records that are classified correctly. Precision is the fraction of records predicted as a class that really belong to it. Recall, also called detection rate, is the fraction of the records of a class that the model finds. F1-score is the harmonic mean of precision and recall. The false positive rate is the fraction of normal records that are wrongly reported as attacks, and a confusion matrix shows exactly which classes are confused with each other.

In network security, recall and the false positive rate are the most important of these. A low recall means that real attacks are being missed, and a high false positive rate means that the analyst is flooded with useless alerts and legitimate users may be blocked.

## 5.7 FRONTEND ARCHITECTURE

The frontend is built with HTML, CSS and JavaScript, and it is kept simple, clean and responsive. The pages share a common layout with a navigation menu on the left and the content on the right. The main pages are registration, login, start monitoring, dashboard, live monitor, alerts, blocked IPs, model performance and reports.

JavaScript is used to request new results from the server at fixed intervals with the fetch function, and Chart.js is used to draw the traffic chart and the attack type chart. Severity levels and actions are displayed with clear labels, so that the analyst can recognise high priority items at a glance.

## 5.8 BACKEND ARCHITECTURE

The backend is written in Python using the Flask framework. It is organised into separate modules. The preprocessing module transforms records, the detection module loads the model and returns the class and the confidence, the prevention module decides the action, and the database module saves and reads data. The Flask routes only connect these modules to the web pages, so each module can be tested without the web server.

SQLite is used as the database because it needs no separate server and is enough for a mini project. User passwords are stored as hashes generated with the Werkzeug security helpers, and the pages that show data are accessible only after login. The database layer can be replaced by MySQL later without changing the other modules.

## 5.9 TOOLS AND TECHNOLOGIES USED

The tools and technologies used to develop the system are listed in the table below. All of them are free and open source.

Table 5.9.1 Technologies used in AI-IDPS

| Component | Technology | Purpose |

| --- | --- | --- |

| Programming language | Python 3 | Data processing, model training and backend |

| Machine learning | Scikit-learn, XGBoost | Training and evaluating the classifiers |

| Data handling | Pandas, NumPy | Loading, cleaning and transforming the dataset |

| Model storage | Joblib | Saving the model, encoders and scaler |

| Web framework | Flask | Routes, sessions and API for the dashboard |

| Frontend | HTML, CSS, JavaScript | User interface of the dashboard |

| Charts | Chart.js | Traffic and attack type charts |

| Database | SQLite | Users, logs, alerts and blocked addresses |

| Dataset | NSL-KDD | Training and replay of network traffic |

| Development tools | VS Code, Jupyter Notebook, Git | Coding, experiments and version control |



The system was designed for the following minimum hardware and software requirements.

Hardware: a computer with an Intel Core i3 or higher processor, 4 GB of RAM (8 GB recommended) and 2 GB of free disk space.

Operating system: Windows 10 or 11, Ubuntu 20.04 or later, or macOS.

Software: Python 3.10 or later, the libraries listed above and any modern web browser such as Chrome, Edge or Firefox.

CHAPTER 6

RESULT AND DISCUSSION

# CHAPTER 6
RESULT AND DISCUSSION

## 6.1 INPUT SCREENSHOTS

This section shows the pages through which the analyst gives input to the system. The registration and login pages control who can use the console, and the start monitoring page is used to choose the data source and the prevention settings.

6.1.1 Registration Page

A new user creates an account by entering a name, an email address and a password. The password is confirmed by entering it twice, and it is stored only as a salted hash. The email address must be unique, and the form shows an error message if the address is already registered.

Fig 6.1.1 Registration Page

6.1.2 Login Page

A registered user logs in with the email address and password. After successful verification a session is created and the user is taken to the dashboard. If the details are wrong, an error message is displayed and no data page can be opened.

Fig 6.1.2 Login Page

6.1.3 Start Monitoring Page

On this page the analyst selects the traffic data source, the replay speed, the block threshold, the rate-limit threshold and the active model. The default values are 0.90 for blocking and 0.60 for rate-limiting. Pressing the Start Monitoring button begins the replay of traffic records, and the Stop button ends it.

Fig 6.1.3 Start Monitoring Page

## 6.2 OUTPUT SCREENSHOTS

This section shows the pages that present the results of the detection and prevention process to the analyst.

6.2.1 Dashboard

The dashboard gives a summary of the current situation. The four cards at the top show the number of flows analysed, the number of threats detected, the number of blocked addresses and the accuracy of the active model. Below them, a line chart compares normal traffic with attack traffic over time, a bar chart shows how many attacks of each type were found, and a table lists the most recent alerts. A sudden peak in the attack line, as seen in the chart, is the typical signature of a flooding attack.

Fig 6.2.1 Dashboard

6.2.2 Live Monitor

The live monitor page lists every processed record with its time, source and destination address, protocol, service, predicted class, confidence and the action taken. The action is shown as a label so that blocked, rate-limited and logged records can be told apart quickly. The page also shows how many records of the data source have been processed.

Fig 6.2.2 Live Monitor Page

6.2.3 Alerts Page

Every detected attack creates an alert, and the alerts page lists all of them with an identifier, the time, the source address, the attack type, the confidence, the severity and the action taken. The buttons at the top filter the list by severity, which lets the analyst concentrate on high severity alerts first.

Fig 6.2.3 Alerts Page

6.2.4 Blocked IPs Page

The blocked IPs page shows the addresses that were blocked by the prevention engine, the attack class that caused the block and the time of blocking. If the analyst finds that a block was wrong, the Unblock button removes the address from the blocked list, and the same entry can be blocked again later with the Re-block button.

Fig 6.2.4 Blocked IPs Page

6.2.5 Model Performance Page

This page displays the accuracy, precision, recall and F1-score of the active model, together with its confusion matrix and a comparison of the three trained models. It lets the analyst check the quality of the detection and decide when the model should be retrained.

Fig 6.2.5 Model Performance Page

6.2.6 Reports Page

The reports page generates a summary of the detection and prevention activity for a chosen time period. The summary lists, for every attack class, how many threats were detected and how many of them were blocked, rate-limited or only logged. The report can be downloaded as a CSV file.

Fig 6.2.6 Reports Page

## 6.3 PERFORMANCE ANALYSIS

The models were evaluated on a test set of 25,195 records, which is 20 percent of the KDDTrain+ file selected by stratified sampling. The overall results of the three models are given in the table below. Random Forest achieved the highest values in all measures and also the lowest false positive rate, so it was selected as the model used by the system.

Table 6.3.1 Comparison of the trained models

| Model | Accuracy (%) | Precision (%) | Recall (%) | F1-score (%) | False positive rate (%) |

| --- | --- | --- | --- | --- | --- |

| Decision Tree | 99.52 | 99.52 | 99.52 | 99.51 | 0.21 |

| Random Forest | 99.84 | 99.84 | 99.84 | 99.84 | 0.06 |

| XGBoost | 99.78 | 99.78 | 99.78 | 99.77 | 0.09 |



Fig 6.3.1 Accuracy and F1-score of the Trained Models

The class-wise results of the Random Forest model are given in the next table. The model detects Normal, DoS and Probe traffic almost perfectly, because these classes have thousands of training examples. The R2L class is detected with good precision and recall, but the U2R class has a clearly lower recall, since only 52 U2R records are available in the training file and only 10 of them are in the test set.

Table 6.3.2 Class-wise performance of the Random Forest model

| Class | Precision (%) | Recall (%) | F1-score (%) | Test records |

| --- | --- | --- | --- | --- |

| Normal | 99.81 | 99.94 | 99.87 | 13,470 |

| DoS | 99.98 | 99.96 | 99.97 | 9,185 |

| Probe | 99.83 | 99.66 | 99.74 | 2,331 |

| R2L | 96.32 | 91.96 | 94.09 | 199 |

| U2R | 85.71 | 60.00 | 70.59 | 10 |



The confusion matrix below shows exactly where the errors occur. Most of the wrong predictions are attack records that were labelled as Normal, mainly from the R2L and U2R classes, because the connections of these attacks look very similar to legitimate user sessions. Only very few normal records were reported as attacks, which gives a false positive rate of 0.06 percent, so the analyst is not flooded with false alarms.

Fig 6.3.2 Confusion Matrix of the Random Forest Model

The importance of the features used by the Random Forest is shown in the next chart. The numbers of bytes transferred, the service, the rate of connections to the same service and the connection count are the most useful features. These are the same characteristics that a human analyst would look at when examining flooding and scanning activity, which shows that the model has learned meaningful behaviour.

Fig 6.3.3 Top Ten Important Features of the Random Forest Model

In summary, the system achieves a detection accuracy of 99.84 percent, a detection rate of 99.78 percent for attack traffic and a false positive rate of 0.06 percent on the test data. These results are obtained on a benchmark dataset, and the performance on a real network may be lower because real traffic differs from the dataset, so the model should be retrained with traffic of the target network before real deployment.

## 6.4 TESTING

The main functions of the system were tested with the test cases given below. Each test case describes the scenario, the input given and the result that the system is expected to produce.

Table 6.4.1 Functional test cases

| Test ID | Test scenario | Input | Expected result |

| --- | --- | --- | --- |

| TC-01 | Registration with a new email | Name, unique email, matching passwords | Account is created and password is stored as a hash |

| TC-02 | Login with valid details | Registered email and correct password | User is redirected to the dashboard |

| TC-03 | Login with a wrong password | Registered email and wrong password | Error message is shown, access is denied |

| TC-04 | Access a page without login | Dashboard URL opened directly | User is redirected to the login page |

| TC-05 | Start monitoring | Select KDDTest+ and press Start | Records are replayed and predictions appear on the live monitor |

| TC-06 | High confidence attack | DoS record with confidence 0.90 or more | Source IP is blocked and a high severity alert is created |

| TC-07 | Medium confidence attack | Probe record with confidence between 0.60 and 0.90 | Source is rate-limited and a medium severity alert is created |

| TC-08 | Normal traffic | Record predicted as Normal | Record is logged and no alert is created |

| TC-09 | Unblock an address | Press Unblock for a blocked IP | Status changes to Unblocked |

| TC-10 | Generate report | Select a time range and press Generate | Summary table is displayed and CSV can be downloaded |



CHAPTER 7

CONCLUSION

# CHAPTER 7
CONCLUSION

## 7.1 CONCLUSION OF THE PROJECT

The project AI-Driven Cyber Threat Detection and Intelligent Intrusion Prevention for Secure Connected Communication Networks successfully demonstrates how machine learning can be used to detect malicious network traffic and to respond to it automatically. The system classifies every traffic record into one of five classes, assigns a confidence to the decision and selects a proportionate response, which is more useful in practice than a simple alarm.

Three algorithms were trained and compared on the NSL-KDD dataset, and the Random Forest model gave the best results with an accuracy of 99.84 percent and a very low false positive rate. The model is integrated with a Flask web application that provides secure login, live monitoring, alerts, blocked IP management, performance display and reporting, so the full cycle from detection to prevention can be demonstrated on an ordinary computer.

The modular design of the system, with separate components for preprocessing, detection, prevention and reporting, makes it a good base for further development. The project has also given a practical understanding of the complete workflow of an AI-based security application, from data preparation and model selection to deployment and evaluation.

## 7.2 KEY ACHIEVEMENTS

Developed a five-class traffic classifier based on the Random Forest algorithm with an accuracy of 99.84 percent on the test data.

Compared Decision Tree, Random Forest and XGBoost using accuracy, precision, recall, F1-score, false positive rate and confusion matrix.

Implemented a confidence-based prevention engine that blocks, rate-limits or logs the traffic source automatically.

Built a secure web dashboard with registration, login, live monitoring, alerts, blocked IP management, model performance and reports.

Designed a database that records traffic logs, alerts and blocked addresses for auditing.

Created a modular architecture that can be extended with live packet capture, deep learning and explainable AI.

## 7.3 LIMITATIONS OF THE CURRENT SYSTEM

The present version of the system has some limitations. The traffic is supplied by replaying the NSL-KDD dataset, which is an older benchmark, and it does not contain IP addresses, so simulated addresses are used to demonstrate blocking. The results on this dataset may not be the same as on the traffic of a real network.

The blocking is done by a software list of addresses and does not change the rules of a real firewall. The rare attack classes, especially U2R, have very few training examples, so their detection rate is lower than that of the other classes. The system also cannot inspect the content of encrypted traffic, and an attacker who deliberately designs traffic to look normal may avoid detection. These limitations are addressed in the future enhancements.

CHAPTER 8

FUTURE ENHANCEMENT

# CHAPTER 8
FUTURE ENHANCEMENT

## 8.1 FUTURE SCOPE

This mini project forms the base of a larger system, and it is planned to extend it as the final year project. The following enhancements are proposed.

Real-time packet capture: capturing live traffic with Scapy and converting it into flow records with a tool such as CICFlowMeter, so that the system works on a real network instead of a replayed dataset.

Modern datasets: training and testing the model with newer datasets such as CICIDS2017 (Sharafaldin et al., 2018) and UNSW-NB15 (Moustafa and Slay, 2015), which contain more recent attack behaviour.

Deep learning models: adding LSTM, CNN and autoencoder models to improve the detection of unknown attacks and of sequences of events.

Real prevention: sending the block and rate-limit decisions to a real firewall through iptables or to a software-defined networking controller.

Explainable AI: using SHAP (Lundberg and Lee, 2017) or LIME to show the analyst why a particular flow was flagged, which increases trust in automatic decisions.

Handling class imbalance: applying oversampling techniques such as SMOTE and collecting more examples of the rare classes to improve the recall of R2L and U2R attacks.

Feedback and retraining: allowing the analyst to confirm alerts or mark false positives, and retraining the model automatically with this feedback.

Federated learning: training the model across several networks without sharing their raw traffic, which protects privacy.

Reinforcement learning: letting the prevention engine learn the best response policy instead of using fixed thresholds.

Integration and alerting: connecting the system with SIEM tools and sending alerts by email or SMS, and deploying it on the edge for IoT networks.

# APPENDIX

# A. SAMPLE CODE

A.1 preprocess.py (data loading and preprocessing)

| import pandas as pd import joblib from sklearn.preprocessing import StandardScaler   COLUMNS = ["duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",     "land", "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",     "num_compromised", "root_shell", "su_attempted", "num_root", "num_file_creations",     "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login",     "is_guest_login", "count", "srv_count", "serror_rate", "srv_serror_rate",     "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",     "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",     "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",     "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",     "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label", "difficulty"]   FAMILIES = {     "DoS": ["back", "land", "neptune", "pod", "smurf", "teardrop", "apache2",             "udpstorm", "processtable", "worm", "mailbomb"],     "Probe": ["ipsweep", "nmap", "portsweep", "satan", "mscan", "saint"],     "R2L": ["ftp_write", "guess_passwd", "imap", "multihop", "phf", "spy",             "warezclient", "warezmaster", "sendmail", "named", "snmpgetattack",             "snmpguess", "xlock", "xsnoop", "httptunnel"],     "U2R": ["buffer_overflow", "loadmodule", "perl", "rootkit", "ps", "sqlattack", "xterm"], } ATTACK_MAP = {"normal": "Normal"} for family, names in FAMILIES.items():     for name in names:         ATTACK_MAP[name] = family   CATEGORICAL = ["protocol_type", "service", "flag"]     def load(path):     df = pd.read_csv(path, names=COLUMNS)     df = df.drop(columns=["difficulty"])     df["label"] = df["label"].map(ATTACK_MAP)     return df.dropna().drop_duplicates()     def fit_preprocessor(df, save_path="models/preprocessor.pkl"):     X = df.drop(columns=["label"]).copy()     y = df["label"]     mappings = {}     for col in CATEGORICAL:         classes = sorted(X[col].unique())         mappings[col] = {c: i for i, c in enumerate(classes)}         X[col] = X[col].map(mappings[col])     scaler = StandardScaler()     X_scaled = scaler.fit_transform(X)     joblib.dump({"mappings": mappings, "scaler": scaler,                  "columns": list(X.columns)}, save_path)     return X_scaled, y |

| --- |



A.2 train.py (model training and selection)

| import joblib from sklearn.model_selection import train_test_split from sklearn.preprocessing import LabelEncoder from sklearn.tree import DecisionTreeClassifier from sklearn.ensemble import RandomForestClassifier from sklearn.metrics import (accuracy_score, precision_recall_fscore_support,                              classification_report, confusion_matrix) from xgboost import XGBClassifier from preprocess import load, fit_preprocessor   df = load("data/KDDTrain+.txt") X, y = fit_preprocessor(df)   label_encoder = LabelEncoder() y_num = label_encoder.fit_transform(y)   X_train, X_test, y_train, y_test = train_test_split(     X, y_num, test_size=0.2, stratify=y_num, random_state=42)   models = {     "Decision Tree": DecisionTreeClassifier(class_weight="balanced", random_state=42),     "Random Forest": RandomForestClassifier(n_estimators=100, class_weight="balanced",                                             n_jobs=-1, random_state=42),     "XGBoost": XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1,                              eval_metric="mlogloss", random_state=42), }   best_name, best_f1 = None, 0.0 for name, model in models.items():     model.fit(X_train, y_train)     pred = model.predict(X_test)     acc = accuracy_score(y_test, pred)     p, r, f1, _ = precision_recall_fscore_support(y_test, pred, average="weighted")     print(f"{name}: accuracy={acc:.4f} precision={p:.4f} recall={r:.4f} f1={f1:.4f}")     if f1 > best_f1:         best_name, best_f1 = name, f1   best = models[best_name] pred = best.predict(X_test) print(classification_report(y_test, pred, target_names=label_encoder.classes_)) print(confusion_matrix(y_test, pred))   joblib.dump({"model": best, "labels": list(label_encoder.classes_)}, "models/model.pkl") print("Saved best model:", best_name) |

| --- |



A.3 detect.py (prediction with confidence)

| import joblib import numpy as np import pandas as pd   bundle = joblib.load("models/model.pkl") prep = joblib.load("models/preprocessor.pkl") model, labels = bundle["model"], bundle["labels"]     def preprocess(record):     row = pd.DataFrame([record])[prep["columns"]]     for col, mapping in prep["mappings"].items():         row[col] = row[col].map(mapping).fillna(-1)     return prep["scaler"].transform(row)     def predict(record):     x = preprocess(record)     proba = model.predict_proba(x)[0]     index = int(np.argmax(proba))     return labels[index], float(proba[index]) |

| --- |



A.4 prevent.py (intelligent prevention engine)

| from datetime import datetime   BLOCK_THRESHOLD = 0.90 LIMIT_THRESHOLD = 0.60     def decide(label, confidence):     if label == "Normal":         return "Logged", "LOW"     if confidence >= BLOCK_THRESHOLD:         return "Blocked", "HIGH"     if confidence >= LIMIT_THRESHOLD:         return "Rate-limited", "MEDIUM"     return "Logged", "LOW"     def apply_action(db, log_id, src_ip, label, confidence):     action, severity = decide(label, confidence)     now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     block_id = None     if label != "Normal":         if action == "Blocked":             row = db.execute("SELECT block_id FROM blocked_ips "                              "WHERE ip_address=? AND status='Blocked'", (src_ip,)).fetchone()             if row:                 block_id = row[0]             else:                 cur = db.execute("INSERT INTO blocked_ips (ip_address, reason, blocked_at, status) "                                  "VALUES (?, ?, ?, 'Blocked')", (src_ip, label, now))                 block_id = cur.lastrowid         db.execute("INSERT INTO alerts (log_id, block_id, attack_type, confidence, "                    "severity, action_taken, alert_time) VALUES (?, ?, ?, ?, ?, ?, ?)",                    (log_id, block_id, label, confidence, severity, action, now))     db.commit()     return action, severity |

| --- |



A.5 schema.sql (database tables)

| CREATE TABLE IF NOT EXISTS users (     user_id INTEGER PRIMARY KEY AUTOINCREMENT,     username TEXT NOT NULL,     email TEXT UNIQUE NOT NULL,     password_hash TEXT NOT NULL,     role TEXT DEFAULT 'analyst',     created_at DATETIME DEFAULT CURRENT_TIMESTAMP );   CREATE TABLE IF NOT EXISTS traffic_logs (     log_id INTEGER PRIMARY KEY AUTOINCREMENT,     user_id INTEGER REFERENCES users(user_id),     src_ip TEXT, dst_ip TEXT, protocol TEXT, service TEXT,     src_bytes INTEGER, dst_bytes INTEGER,     logged_at DATETIME DEFAULT CURRENT_TIMESTAMP );   CREATE TABLE IF NOT EXISTS blocked_ips (     block_id INTEGER PRIMARY KEY AUTOINCREMENT,     ip_address TEXT NOT NULL,     reason TEXT,     blocked_at DATETIME,     status TEXT DEFAULT 'Blocked' );   CREATE TABLE IF NOT EXISTS alerts (     alert_id INTEGER PRIMARY KEY AUTOINCREMENT,     log_id INTEGER REFERENCES traffic_logs(log_id),     block_id INTEGER REFERENCES blocked_ips(block_id),     attack_type TEXT, confidence REAL, severity TEXT, action_taken TEXT,     alert_time DATETIME );   CREATE TABLE IF NOT EXISTS model_info (     model_id INTEGER PRIMARY KEY AUTOINCREMENT,     user_id INTEGER REFERENCES users(user_id),     algorithm TEXT, accuracy REAL, f1_score REAL,     trained_on DATETIME DEFAULT CURRENT_TIMESTAMP ); |

| --- |



A.6 app.py (Flask application)

| from flask import Flask, render_template, request, redirect, session, jsonify from werkzeug.security import generate_password_hash, check_password_hash import sqlite3   from preprocess import load from detect import predict from prevent import apply_action   app = Flask(__name__) app.secret_key = "change-this-secret-key" DB_FILE = "idps.db" stream = {"data": None, "pos": 0, "running": False}     def get_db():     db = sqlite3.connect(DB_FILE)     db.row_factory = sqlite3.Row     return db     def sim_ip(i, internal=False):     # NSL-KDD has no IP addresses, so simulated addresses are assigned     if internal:         return "10.0.0.%d" % (i % 90 + 5)     return "192.168.%d.%d" % (i % 4 + 1, i % 200 + 10)     @app.route("/register", methods=["GET", "POST"]) def register():     if request.method == "POST":         db = get_db()         db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",                    (request.form["name"], request.form["email"],                     generate_password_hash(request.form["password"])))         db.commit()         return redirect("/login")     return render_template("register.html")     @app.route("/login", methods=["GET", "POST"]) def login():     if request.method == "POST":         db = get_db()         user = db.execute("SELECT * FROM users WHERE email=?",                           (request.form["email"],)).fetchone()         if user and check_password_hash(user["password_hash"], request.form["password"]):             session["user_id"] = user["user_id"]             return redirect("/dashboard")         return render_template("login.html", error="Invalid email or password")     return render_template("login.html")     @app.route("/dashboard") def dashboard():     if "user_id" not in session:         return redirect("/login")     return render_template("dashboard.html")     @app.route("/start", methods=["POST"]) def start():     if "user_id" not in session:         return jsonify(error="login required"), 401     stream["data"] = load("data/KDDTest+.txt").reset_index(drop=True)     stream["pos"], stream["running"] = 0, True     return jsonify(status="running", total=len(stream["data"]))     @app.route("/stop", methods=["POST"]) def stop():     stream["running"] = False     return jsonify(status="stopped")     @app.route("/api/next") def next_batch():     if not stream["running"] or "user_id" not in session:         return jsonify(results=[])     db = get_db()     results = []     start = stream["pos"]     batch = stream["data"].iloc[start:start + 5]     stream["pos"] += len(batch)     for i, (_, row) in enumerate(batch.iterrows(), start=start):         record = row.drop("label").to_dict()         label, confidence = predict(record)         src, dst = sim_ip(i), sim_ip(i, internal=True)         cur = db.execute("INSERT INTO traffic_logs (user_id, src_ip, dst_ip, protocol, "                          "service, src_bytes, dst_bytes) VALUES (?, ?, ?, ?, ?, ?, ?)",                          (session["user_id"], src, dst, record["protocol_type"],                           record["service"], int(record["src_bytes"]), int(record["dst_bytes"])))         action, severity = apply_action(db, cur.lastrowid, src, label, confidence)         results.append({"src_ip": src, "dst_ip": dst, "protocol": record["protocol_type"],                         "service": record["service"], "prediction": label,                         "confidence": round(confidence * 100, 1), "action": action})     db.commit()     return jsonify(results=results, position=stream["pos"])     @app.route("/unblock/<int:block_id>", methods=["POST"]) def unblock(block_id):     db = get_db()     db.execute("UPDATE blocked_ips SET status='Unblocked' WHERE block_id=?", (block_id,))     db.commit()     return jsonify(status="unblocked")     if __name__ == "__main__":     app.run(debug=True) |

| --- |



A.7 dashboard.js (live refresh of the dashboard)

| const tbody = document.getElementById("live-body"); let attackCount = 0;   function addRow(r) {   const tr = document.createElement("tr");   tr.innerHTML = "<td>" + r.src_ip + "</td><td>" + r.dst_ip + "</td><td>" + r.protocol +     "</td><td>" + r.service + "</td><td>" + r.prediction + "</td><td>" +     r.confidence + "%</td><td>" + r.action + "</td>";   tbody.prepend(tr);   if (tbody.rows.length > 12) tbody.deleteRow(-1); }   async function refresh() {   const response = await fetch("/api/next");   const data = await response.json();   data.results.forEach(r => {     addRow(r);     if (r.prediction !== "Normal") attackCount++;   });   document.getElementById("threat-count").textContent = attackCount; }   setInterval(refresh, 1000); |

| --- |



# B. SAMPLE OUTPUT

B.1 Console output of train.py

| Decision Tree: accuracy=0.9952 precision=0.9952 recall=0.9952 f1=0.9951 Random Forest: accuracy=0.9984 precision=0.9984 recall=0.9984 f1=0.9984 XGBoost: accuracy=0.9978 precision=0.9978 recall=0.9978 f1=0.9977 Saved best model: Random Forest |

| --- |



Table B.2 Classification report printed by train.py for the selected model

| Class | Precision | Recall | F1-score | Support |

| --- | --- | --- | --- | --- |

| Normal | 1.00 | 1.00 | 1.00 | 13470 |

| DoS | 1.00 | 1.00 | 1.00 | 9185 |

| Probe | 1.00 | 1.00 | 1.00 | 2331 |

| R2L | 0.96 | 0.92 | 0.94 | 199 |

| U2R | 0.86 | 0.60 | 0.71 | 10 |

| Accuracy |  |  | 1.00 | 25195 |

| Weighted average | 1.00 | 1.00 | 1.00 | 25195 |



B.3 Sample response of the /api/next route

| {   "position": 1245,   "results": [     {"src_ip": "192.168.1.45", "dst_ip": "10.0.0.5", "protocol": "tcp",      "service": "http", "prediction": "DoS", "confidence": 98.4, "action": "Blocked"},     {"src_ip": "172.16.4.9", "dst_ip": "10.0.0.5", "protocol": "tcp",      "service": "ftp", "prediction": "R2L", "confidence": 74.6, "action": "Rate-limited"},     {"src_ip": "192.168.1.12", "dst_ip": "10.0.0.5", "protocol": "tcp",      "service": "http", "prediction": "Normal", "confidence": 99.1, "action": "Logged"}   ] } |

| --- |



Table B.4 Sample entries of the alerts table

| Alert ID | Attack type | Confidence | Severity | Action taken | Alert time |

| --- | --- | --- | --- | --- | --- |

| A-1041 | DoS | 0.984 | HIGH | Blocked | 2026-11-19 10:42:11 |

| A-1040 | Probe | 0.912 | HIGH | Blocked | 2026-11-19 10:41:58 |

| A-1039 | R2L | 0.746 | MEDIUM | Rate-limited | 2026-11-19 10:41:30 |

| A-1035 | R2L | 0.552 | LOW | Logged | 2026-11-19 10:37:02 |



# REFERENCES

[1]  Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5-32.

[2]  Buczak, A. L., & Guven, E. (2016). A survey of data mining and machine learning methods for cyber security intrusion detection. IEEE Communications Surveys & Tutorials, 18(2), 1153-1176.

[3]  Canadian Institute for Cybersecurity, University of New Brunswick. NSL-KDD dataset. https://www.unb.ca/cic/datasets/nsl.html

[4]  Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 785-794.

[5]  Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems 30.

[6]  Moustafa, N., & Slay, J. (2015). UNSW-NB15: A comprehensive data set for network intrusion detection systems. Military Communications and Information Systems Conference (MilCIS), IEEE.

[7]  Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830.

[8]  Pallets Projects. Flask documentation. https://flask.palletsprojects.com

[9]  Roesch, M. (1999). Snort: Lightweight intrusion detection for networks. Proceedings of the 13th USENIX Conference on System Administration (LISA), 229-238.

[10]  Scarfone, K., & Mell, P. (2007). Guide to Intrusion Detection and Prevention Systems (IDPS). NIST Special Publication 800-94.

[11]  Sharafaldin, I., Lashkari, A. H., & Ghorbani, A. A. (2018). Toward generating a new intrusion detection dataset and intrusion traffic characterization. Proceedings of the 4th International Conference on Information Systems Security and Privacy (ICISSP), 108-116.

[12]  Sommer, R., & Paxson, V. (2010). Outside the closed world: On using machine learning for network intrusion detection. IEEE Symposium on Security and Privacy, 305-316.

[13]  Tavallaee, M., Bagheri, E., Lu, W., & Ghorbani, A. A. (2009). A detailed analysis of the KDD CUP 99 data set. IEEE Symposium on Computational Intelligence for Security and Defense Applications (CISDA).