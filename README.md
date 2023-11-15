# Project 1, Federated machine learning

## Background

Federated machine learning (FedML) is a promising approach that enables multiple participants to collaboratively train a shared machine
learning prediction model to high accuracy without requiring them to share their data. FedML works by allowing each user devices to download
current global model, improve it by learning from local data, and then submitting a summarized version of the changes often referred to as
updates. These updates are encrypted when sending to the server, and subsequently aggregated to improve the shared global model. However
the decentralized nature of federated machine learning makes it vulnerable to various security and privacy threats. Poison attacks are one such
threat and we will look at this threat in detail under this project.

## Poisoning Attack
Poison attacks are a serious security threat that can lead to unreliable results. 
Broadly categorized as either:
Data Poisoning Attacks based on fake data injection.
Model Poisoning Attacks based on fake update injection.

Goal: Goal: undermine model’s performance or induce miss classification.

## Project Aims
In order to design robust defensive mechanisms, it is imperative to first fully understand the impact of different types of attacks under federated
machine learning architecture. Hence, under this project the primary aims is to implement several state-of-the-art model poisoning attacks in
FedML and evaluate their performance. The attacks which will be explored under this project include:
Label flipping attack [3] that attacks the global model via manipulation of underlying training data (flipping the dataset labels).
Little is enough (LIE) attack [2] is carried out by making use of mean (μ) and standard deviation (σ) of the available benign updates.
Dynamic optimization (DYN-OPT) attack [4] that performs an attack by computing mean (μ) and perturbing it in an optimized direction.
Backdoor attack [1] that performs a targeted model poisoning attacks aiming to get miss-classification of specific (often tagged) samples.
Google’s data poisoning attack [5] which computes the attack vector by solving an optimization problem to maximize the loss over entire
benign dataset.

## Expected Outcomes:
An implementation of federated machine learning framework with some poison attacks will be provided as a starting point. Student are
expected to understand, and extend on the existing code base. To this end familiarity with courses like Data Engineering I and Data Engineering
II will prove beneficial especially the part that introduced FEDn: A Scalable Federated Machine Learning Framework since we will implement all
attacks under this framework. The expected outcomes of the project include:
Implementing various attacks in a distributed federated machine learning framework evaluating their performance. Successful
implementation of at least three attacks is expected to pass the project.
A quantitative comparison of the listed attacks under various practical settings including ration (%) of malicious clients, dataset distribution,
model size etc. A well maintained and open sourced implementation of the attacks that will be beneficial to the the research community.

Note: We expect students to have: a can-do attitude, willingness to learn new concepts, and independence to solve programming challenges.

## References
[1] Eugene Bagdasaryan, Andreas Veit, Yiqing Hua, Deborah Estrin, and Vitaly Shmatikov. How to backdoor federated learning. CoRR, abs/1807.00459, 2018.

[2] Moran Baruch, Gilad Baruch, and Yoav Goldberg. A little is enough: Circumventing defenses for distributed learning. CoRR, abs/1902.06156, 2019.

[3] Clement Fung, Chris J. M. Yoon, and Ivan Beschastnikh. The limitations of federated learning in sybil settings. In 23rd International Symposium on Research in Attacks,
Intrusions and Defenses (RAID 2020), pages 301–316, San Sebastian, October 2020. USENIX Association.

[4] Virat Shejwalkar and Amir Houmansadr. Manipulating the byzantine: Optimizing model poisoning attacks and defenses for federated learning. In NDSS, 2021.

[5] Virat Shejwalkar, Amir Houmansadr, Peter Kairouz, and Daniel Ramage. Back to the drawing board: A critical evaluation of poisoning attacks on federated learning.
CoRR, abs/2108.10241, 2021.

