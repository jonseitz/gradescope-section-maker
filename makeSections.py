import csv as csvOperator
import sys
from random import shuffle
from copy import copy

##### CSV Helpers #####

# CSV file writer
def writeCSV(filename, header, data):
  # Add extension if necessary
  if not filename.endswith('.csv'):
    filename += '.csv'
  with open(filename, 'w') as csvfile:
    writer = csvOperator.writer(csvfile, delimiter=',', quotechar='|', quoting=csvOperator.QUOTE_MINIMAL)
    # Write header
    writer.writerow(header)
    # Data
    for row in data:
      writer.writerow(row)

# CSV file reader
def readCSV(filename):
  with open(filename) as file:
    csvfile = csvOperator.reader(file, delimiter=',')
    
    csv = {}
    csv['data'] = []
    csv['headers'] = None
    for row in csvfile:
      if (csv['headers'] == None):
        csv['headers'] = row
      else:
        csv['data'].append(row)
    return csv

##### MAIN PROGRAM #####

print "\n\nSection Maker for CS121 (v1.0)"
print "- Your graders.csv should be: [Grader Name, Multiplier]"
print "- Your students.csv should be a normal roster from Canvas"
print "\nNote: a \"multiplier\" defines a grader's workload. Examples:"
print "- Multiplier is 2, grader will grade twice as many students"
print "- Multiplier is 0.5, grader will grade halfa as many students\n\n"
try:
  raw_input("If ready, press return. Otherwise, ctrl+c.")
except:
  print "\n\nGoodbye!"
  sys.exit(0)

# Read in files
students = None
graders = None
try:
  students = readCSV('students.csv')
except:
  print "\nCouldn't read students.csv. Goodbye!"
  sys.exit(0)
try:
  graders = readCSV('graders.csv')
except:
  print "\nCouldn't read graders.csv. Goodbye!"
  sys.exit(0)

## Process csv data

# Get students section column
NO_SECTION = '0'
studentsSectionCol = None
for i in range(len(students['headers'])):
  header = students['headers'][i]
  if header.lower() == 'section':
    studentsSectionCol = i
    break
if studentsSectionCol is None:
  # Need to add a new column
  studentsSectionCol = len(students['headers'])
  students['headers'].append('section')
  # Add empty sections to all students
  for i in range(len(students['data'])):
    students['data'][i].append(NO_SECTION)

# Get section information
multipliers = []
sectionToName = {}
totalMultiplierMass = 0.0
for i in range(len(graders['data'])):
  row = graders['data'][i]
  section = i + 1

  name = row[0]
  multiplier = float(row[1])
  multipliers.append(multiplier)
  totalMultiplierMass += multiplier
  sectionToName[section] = name

## Generate workloads based on multipliers
workloads = {} # section => numStudents
numStudents = len(students['data'])
numAssigned = 0
nextSection = 1
# Assign students based on multipliers
for multiplier in multipliers:
  minStudentsToGrade = int(multiplier * float(numStudents)/totalMultiplierMass)
  workloads[nextSection] = minStudentsToGrade
  numAssigned += minStudentsToGrade
  nextSection += 1
sections = range(1,len(multipliers)+1)

# Assign rest of students
unShuffledSections = copy(sections)
shuffle(sections)
nextSectionVictim = 0
while numAssigned < numStudents:
  section = sections[nextSectionVictim]

  workloads[section] += 1
  numAssigned += 1

  nextSectionVictim = (nextSectionVictim + 1) % len(sections)

## Assign students to sections
rowIndices = range(numStudents)
shuffle(rowIndices)
nextRow = 0
for section in sections:
  for i in range(workloads[section]):
    students['data'][rowIndices[nextRow]][studentsSectionCol] = section
    nextRow += 1

## Output new roster
writeCSV('newRoster.csv', students['headers'], students['data'])

## Output workload
workloadHeaders = ['Grader Name', 'Section', 'Num Students Assigned']
workloadData = []
for section in unShuffledSections:
  graderName = sectionToName[section]
  numAssigned = workloads[section]
  workloadData.append([graderName, section, numAssigned])
writeCSV('workloadInfo.csv', workloadHeaders, workloadData)

print "\nDone! I wrote two csv files:"
print "- newRoster.csv (includes updated section numbers)"
print "- workloadInfo.csv (includes graders, their associated sections, and the # students they're grading"