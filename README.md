# gradescope-section-maker
Assigns students to grader sections given varying workloads.

### Instructions

Step 1: Add graders to a `graders.csv` file with the following columns:  

|      Grader Name     | Multiplier |
|:--------------------:|:----------:|
| Kani (Double Grader) | 2          |
| Lea (Normal Grader)  | 1          |
| Kipu (Half Grader)   | 0.5        |
| etc   |         |

Step 2: Download a student roster from SEAS Inclass and save it as `students.csv`.

Step 3: With all csv files and `makeSections.py` in the same folder, run the assignments script: `python makeSections.py`

Step 4: Upload `newRoster.csv` to Gradescope and save `workloadInfo.csv` for reference. Graders can find their associated section in `workloadInfo.csv`. Recommendation: upload `workloadInfo.csv` and `newRoster.csv` to a secure shared google drive where all TFs have access and name the files according to the current assignment: you may want to go back and check grader workload or grader assignments.