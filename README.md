# The Persian Universal Dependency Treebank (PerUDT) (v1.0)

# Summary
The Persian Universal Dependency Treebank (PerUDT) is the result of automatic coversion of Persian Dependency Treebank (PerDT) with extensive manual corrections. Please refer to the follwoing work, if you use this data:
*  Mohammad Sadegh Rasooli, Pegah Safari, Amirsaeid Moloodi, and Alireza Nourian. "The Persian Dependency Treebank Made Universal". 2020 (to appear).


# Introduction
[The Persian Universal Dependency Treebank (PerUDT)](https://universaldependencies.org/treebanks/fa_perdt/index.html) is based on <a href="https://www.aclweb.org/anthology/N13-1031v1.pdf"> Persian Dependency Treebank (PerDT) </a>(Rasooli et al.,2013). The original Treebank consists of 29K sentences sampled from contemporary Persian text in different genres including: news, academic papers, magazine articles and fictions. 

This treebank was annotated based on a language-specific schema and its automatic conversion involved three main steps: revising tokenization, POS mapping and dependency mapping. 

In tokenization step, in order to separate multiword inflections of simple verbs grouped as one token in PerDT, we followed the guidelines in (Rasooli et al., 2013, Table 3) to automatically find the main verbs. Also we automatically separated pronominal clitics. 

In POS conversion step, we used the state of the art <a href="https://arxiv.org/abs/2003.08875"> BERT-based Persian NER tagger</a> (Taher et al.,2020) with manual corrections to extend recall. Through seven different entities detected by tagger, we used Person and Location to mark PROPN tags. 

PerDT contains 43 syntactic relations with no straightforward mapping for most of them, conjunctions arranged from the beginning of the sentence to the end and more importantly, prepositions regarded as the head of prepositional phrases and auxiliary verbs as the head of sentences. So we rearranged the order of conjunctions from end to the beginning through a script and tailored rules to convert each kind of relation to its UD version properly. Through the whole process and at the end of each step, we investigated the results and applied manual corrections if it was needed.  


# Acknowledgements
Thanks to Morteza Rezaei-Sharifabadi for helping with the copyright of this data.


# Statistics of PerUDT
| Split | #Sent. | #Tok. | #word | #Type Lemma | #Verbs |
|-------|--------|-------|-------|-------------|--------|
| Train |  26196 |  459K | 34.9K |    20.7K    |  5275  |
| Dev   |  1456  |  26K  |  7.0K |     5.2K    |  1427  |
| Test  |  1455  |  24K  |  6.7K |     5.1K    |  1671  |
| All   |  29107 |  509K | 36.7K |    21.6K    |  5413  |

* Dep. relations: 36 of which 3 are language-specific.

* POS tags: 17

# Data Split
We followed the same split used in PerDT: 89% of data is dedicated to train while 5% of it is used for each dev and test sections. 

# Feedback and Bug Reports
For feedback and bug reports, please contact rasooli@seas.upenn.edu and pegh.safari@gmail.com.


# References

*  Mohammad Sadegh Rasooli, Manouchehr Kouhestani, and Amirsaeid Moloodi. "Development of a Persian syntactic dependency treebank." Proceedings of the 2013 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies. 2013.

*  Ehsan Taher, Seyed Abbas Hoseini, and Mehrnoush Shamsfard. "Beheshti-NER: Persian named entity recognition Using BERT." arXiv preprint arXiv:2003.08875 (2020).

*  Mohammad Sadegh Rasooli, Pegah Safari, Amirsaeid Moloodi, and Alireza Nourian. "The Persian Dependency Treebank Made Universal". 2020 (to appear).

# Change Log

* 2021-05-15 v2.8
  * Undocumented relation compound:lv changed to compound:lvc to pass validation.
* 2020-11-15 v2.7
  * Initial release in Universal Dependencies.


# Metadata
<pre>
=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.7
License: CC BY-SA 4.0
Includes text: yes
Genre: news fiction nonfiction academic web blog
Lemmas: converted with corrections
UPOS: converted from manual
XPOS: manual native
Features: converted with corrections
Relations: converted with corrections
Contributors: Rasooli, Mohammad Sadegh; Safari, Pegah; Moloodi, Amirsaeid; Nourian, Alireza
Contributing: here source
Contact: rasooli@seas.upenn.edu, pegh.safari@gmail.com
===============================================================================
</pre>
