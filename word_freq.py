import string
import os


def noOfWords(lst: list, st):
    count = 0;
    for word in lst:
        if st == word:
            count += 1
    return count

def make_report(lst: list, sett: set, words: list):
    print("---GENARAL STATISTICS---")
    print(f"Total Words:\t{len(lst)}")
    print(f"Unique Words:\t{len(sett)}")

    print("--- TOP 10 MOST FREQUENT WORDS ---")
    sorted_list = sorted(words, key=lambda x: x["Count"], reverse = True)
    for indx, item in enumerate(sorted_list):
        if indx < 10:
            print(f"{indx+1:>2}. {item["Word"]:<14}: {item["Count"]} times")
    return sorted_list

def save_report(lst: list, sett: set, sorted: list, f: str):
    filename = input("Enter the file name to store the record: ")
    total = "Total word: "+str(len(lst))
    unique = "Unique word: "+str(len(sett))
    try:
        with open(filename, "a") as file:
            file.write(f"Record of text and word frequency for {f}\n")
            file.write("---Genaral Statistics---\n")
            file.write(total)
            file.write(unique)
            file.write("---TOP 10 MOST FREQUENT WORDS ---")
            for indx, item in enumerate(sorted):
                if indx < 10:
                    file.write(f"{indx+1:>2}. {item["Word"]:<14}: {item["Count"]} times")


    except FileNotFoundError:
        print("\nFile not Found..!")
        print("Creating a new file name record.json")
        with open("record.json", "w")as jfile:
            jfile.write(f"Record of text and word frequency for {f}")
            jfile.write("---Genaral Statistics---")
            jfile.write(total)
            jfile.write(unique)
            jfile.write("---TOP 10 MOST FREQUENT WORDS ---")
            for indx, item in enumerate(sorted):
                if indx < 10:
                    jfile.write(f"{indx+1:>2}. {item["Word"]:<14}: {item["Count"]} times")


def main():
    print("==================================================")
    print("       TEXT AND WORD FREQUENCY ANALYSER           ")
    print("==================================================")

    filename = input("Enter the file path & name: ")
    if os.path.exists(filename):
        print(f"[✓] Successfully processed {filename}")
    else :
        print("File not Found...!")
        exit(0)

    with open(filename, "r") as file:
        data = file.read()

    lowcase = data.lower()

    table = str.maketrans('', '', string.punctuation)
    clean = lowcase.translate(table)

    words = clean.split()
    filtered_word = [word for word in words if word.isalpha()]

    sett = set()

    for word in filtered_word:
        sett.add(word)

    wordcountlist = []
    for word in sett:
        dict = {"Word": word, "Count": noOfWords(filtered_word, word)}
        wordcountlist.append(dict)

    sorted = make_report(filtered_word, sett, wordcountlist)
    ch = input("\n - Do you Want to save this report (y/N): ")
    if ch == None or ch == "N"or ch == "n":
        print("Report not saved..")
        print("Thank You..:)\n")
        exit(0)
    elif ch == "Y" or ch == "y":
        save_report(filtered_word, sett, sorted, filename)
    else:
        print("Invalid Choise ...!")
        print("Record not saved")
        exit(0)

    #print(wordcountlist)

if __name__ == "__main__":
    main()
