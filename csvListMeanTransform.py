import sys
import csv
import pandas as pd

class outputfile:
    def __init__(self, filename, es, x, y, ef, esv, edv, split):
        self.filename = filename
        self.es = es
        self.x = x
        self.y = y
        self.ef = ef
        self.edv = edv
        self.esv = esv
        self.split = split

    def to_dict(self):
        return {
            "FileName": self.filename,
            "ES": self.es,
            "x": self.x,
            "y": self.y,
            "EF": self.ef,
            "EDV": self.edv,
            "ESV": self.esv,
            "Split": self.split
        }

class inputfile:
    def __init__(self, filename, ef, esv, edv, split):
        self.filename = filename
        self.ef = ef
        self.esv = esv
        self.edv = edv
        self.split = split



if __name__ == '__main__':
    # Check if at least one argument (besides the script name) was provided
    filelist = ""
    volumeTracings = ""
    outFile=""

    if len(sys.argv) > 3:
        filelist = sys.argv[1]
        volumeTracings = sys.argv[2]
        outFile = sys.argv[3]
    else:
        print("Error: No file provided.")
        print("Usage: python print_arg.py <file.csv>")
        sys.exit(1) # Exit with a non-zero status to indicate an error

    inputFiles = dict()
    outputFiles = []

    try:
        with open(filelist, "r", newline="") as csvfile:

            csvreader = csv.DictReader(csvfile)
            c = 0

            #parse input file
            for row_dict in csvreader:
                inputFiles[row_dict["FileName"]] = inputfile(row_dict["FileName"], float(row_dict["EF"]), float(row_dict["ESV"]), float(row_dict["EDV"]), row_dict["Split"])
                c=c+1
                if(c == 10030):
                    break

    except Exception as e:
        print(f"An error occurred while parsing the inputfiles: {e}")

    #write output csv
    csv_headers=["FileName", "ES", "x", "y", "EF", "EDV", "ESV", "Split"]

    try:
        with open(outFile, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, csv_headers)

            writer.writeheader()

            tracings = pd.read_csv(volumeTracings)

            count = 0
            for input in inputFiles.values():
                print(count)
                count += 1
                filterByName = tracings["FileName"] == input.filename
                curr = tracings[filterByName]
                if (curr.shape[0] < 2):
                    break
                frames = curr["Frame"].unique()
                frames.sort()

                filterByFrame1 = curr["Frame"] == frames[0]
                filterByFrame2 = curr["Frame"] == frames[1]

                curr1 = curr[filterByFrame1]
                x1 = (sum(curr1["X1"]) + sum(curr1["X2"])) / (len(curr1) + len(curr1))
                y1 = (sum(curr1["Y1"]) + sum(curr1["Y2"])) / (len(curr1) + len(curr1))
                outputfile1 = outputfile(f"{input.filename}_{frames[0]}", False, x1, y1, input.ef, input.esv, input.edv,input.split)
                outputFiles.append(outputfile1)

                writer.writerow(outputfile1.to_dict())

                curr2 = curr[filterByFrame2]
                x2 = (sum(curr2["X1"]) + sum(curr2["X2"])) / (len(curr2) + len(curr2))
                y2 = (sum(curr2["Y1"]) + sum(curr2["Y2"])) / (len(curr2) + len(curr2))
                outputfile2 = outputfile(f"{input.filename}_{frames[1]}", True, x2, y2, input.ef, input.esv, input.edv, input.split)
                outputFiles.append(outputfile2)

                writer.writerow(outputfile2.to_dict())


            # rowsToWrite = [file.to_dict() for file in outputFiles]
            # writer.writerows(rowsToWrite)

    except Exception as e:
        print(f"An error occurred while writing: {e}")

