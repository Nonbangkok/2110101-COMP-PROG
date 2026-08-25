# 2110101 Computer Programming

Coursework for **2110101 Computer Programming**, Faculty of Engineering,
Chulalongkorn University — every problem with its statement, my solution, and
the complete set of test cases the course grader runs against it.

**→ [Browse it as a website](https://nonbangkok.github.io/2110101-COMP-PROG/)**

---

## What is in here

| | |
|---|---:|
| Problems | 150 |
| Topics | 16 |
| Test cases | 1934 |
| — example set | 539 |
| — full test set | 1395 |
| Data files | 63 |

Every problem folder holds the same four things:

```
<topic>/<problem>/
├── <problem>.pdf          problem statement
├── <problem>.py           solution
├── README.md              title and file list
├── data/                  input files, for problems that read from disk
└── testcases/
    ├── examplesets/       the cases shown in the problem statement
    │   ├── input/input01.txt …
    │   └── output/output01.txt …
    └── testsets/          the full set the grader scores you on
        ├── input/input01.txt …
        └── output/output01.txt …
```

## Topics

| Folder | Topic | Problems | Cases |
|---|---|---:|---:|
| [`00-Python-Intro`](00-Python-Intro/) | Python Intro | 2 | 4 |
| [`01-Data-Type-and-Expression`](01-Data-Type-and-Expression/) | Data Type and Expression | 8 | 65 |
| [`02-Basic-String-and-List`](02-Basic-String-and-List/) | Basic String and List | 11 | 137 |
| [`03-Selection`](03-Selection/) | Selection | 16 | 267 |
| [`04-Repetition`](04-Repetition/) | Repetition | 15 | 165 |
| [`05-List-Processing`](05-List-Processing/) | List Processing | 14 | 164 |
| [`06-Function`](06-Function/) | Function | 6 | 82 |
| [`07-String-Processing`](07-String-Processing/) | String Processing | 8 | 102 |
| [`08-Basic-Dict`](08-Basic-Dict/) | Basic Dict | 7 | 76 |
| [`09-Nested-Structure`](09-Nested-Structure/) | Nested Structure | 7 | 76 |
| [`10-Tuple-Set-Dict`](10-Tuple-Set-Dict/) | Tuple Set Dict | 11 | 116 |
| [`11-NumPy`](11-NumPy/) | NumPy | 7 | 67 |
| [`12-Class-and-Object`](12-Class-and-Object/) | Class and Object | 8 | 107 |
| [`P1-Grader-01-Practice`](P1-Grader-01-Practice/) | Grader 01 Practice | 11 | 204 |
| [`P2-Grader-02-Practice`](P2-Grader-02-Practice/) | Grader 02 Practice | 9 | 134 |
| [`P3-Grader-03-Practice`](P3-Grader-03-Practice/) | Grader 03 Practice | 10 | 168 |

`Work-Shop/` holds the extra in-class material (Pygame), which is not part of
the graded problem set.

## The website

`docs/` is a static site for reading all of this in a browser: the PDF embedded
inline, the solution with syntax highlighting, and each test case with its input
next to its expected output. Open `docs/index.html` directly, or serve the
repository root and visit `/docs/`.

See [`docs/README.md`](docs/README.md) for how to publish it on GitHub Pages and
how to regenerate the index after adding a problem.

## Running a solution

Solutions target **Python 3.12 or newer** — some use f-string syntax that older
versions reject.

```bash
cd 07-String-Processing/07_StrFile_33
python3 07_StrFile_33.py < testcases/examplesets/input/input01.txt
```

Problems that read from files expect those files in the working directory; copy
them out of `data/` first.

Some problems are graded by appending test code to your file rather than by
feeding it stdin — for those, the "input" of a case is Python source. You can
tell them apart at a glance: the input starts with `print(` or `exec(`.

## Where the test cases came from

The course ships a Thonny plugin whose **Test w/ Example** and **Test w/ TestSet**
buttons produce an HTML report containing the input and expected output of every
case. These files are extracted from those reports, then verified by running the
solutions against them and checking the pass/fail verdict matches the grader's,
case for case.

## License

Solutions are mine. Problem statements and test data belong to the course.
