
import argparse


number_of_letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def PlusOne(text:str):
    print("En un futuro lo agregare")
    pass

def PlusRandom(text:str):
    print("En un futuro lo arreglare")
    pass

def NumberPosition(text:str):
    
    output = []
    list_nums = list(number_of_letter)

    for letter in text:
        output.append(list_nums.index(letter))

    print(f"[*]La lista es la siguiente: {output}")
    print(f"[*]Longitud: {len(output)}")

    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Script to encrypt text")

    # Arguments

    parser.add_argument("--txt", type=str, required=True, help="Text to Encrypt")

    parser.add_argument("--type", required=True, type=str, help="Type of encription")

    # Parse the arguments
    args = parser.parse_args()

    if(args.type == "PlusOne"):
        PlusOne(args.txt)

    elif(args.type == "RandomPlus"):
        PlusRandom(args.txt)
    
    elif(args.type == "NumberPosition"):
        NumberPosition(args.txt)

