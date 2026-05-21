import pefile
import hashlib
import argparse


"""

This script works to find the exportable functions hashes from any DLL, with educational purpose and learning 

It only works with Windows

AUTOR: Donuts Diaz

"""


# Function to calculate hashes
def calculate_hash_function(function_name, algorithm="md5"):

    bytes_name = function_name.encode('utf-8')
    
    if algorithm == "md5":
        return hashlib.md5(bytes_name).hexdigest()
    
    elif algorithm == "sha1":
        return hashlib.sha1(bytes_name).hexdigest()
    

    elif algorithm == "sha256":
        return hashlib.sha256(bytes_name).hexdigest()
    

    elif algorithm == "djb2": 
        hash_val = 5381
        for c in bytes_name:
            hash_val = ((hash_val << 5) + hash_val) + c
        return hex(hash_val & 0xFFFFFFFF)
    

    else:
        raise ValueError(f"Algorithm not supported: {algorithm}")


# import all functions and their hashes
def get_hashes_functions_from_dll(path_dll, algorithm="md5"):
    try:

        pe = pefile.PE(path_dll)
        hashes = []
        
        if not hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            print(f"{path_dll} it doesnt has exported functions")
            return []
        

        for export in pe.DIRECTORY_ENTRY_EXPORT.symbols:

            if export.name:  
                name = export.name.decode('utf-8')
                hash_val = calculate_hash_function(name, algorithm)
                ordinal = export.ordinal
                
                hashes.append({
                    'name': name,
                    'ordinal': ordinal,
                    'hash': hash_val,
                    'algorithm': algorithm,
                    'rva': export.address
                })
        
        return hashes
        
    except Exception as e:
        print(f"Error on processing {path_dll}: {e}")
        return []


# Specific functions to search
def find_functions(all_functions, functions_to_search):
    ret_list = []

    hash_by_name = {func['name']: func for func in all_functions}

    for name_to_search in functions_to_search:
            if name_to_search in hash_by_name:
                func = hash_by_name[name_to_search]
                ret_list.append(func)
                print(f"[+] {func['name']} | Hash: {func['hash']} (Ordinal: {func['ordinal']})  Algorithm: {func['algorithm']}  RVA:{func['rva']}")
            else:
                print(f"[-] '{name_to_search}' | No encontrada en la DLL")

    return ret_list


# Save the JSON file
def save_in_json(functions:any, file: str):
    import json
    with open(f"{file}.json", "w") as f:
        json.dump(functions, f, indent=2)
    print(f"\n[*] All hashes where saved in {file}.json ")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Program to get the hashes functions from DLL")

    # Arguments

    parser.add_argument("--path", type=str, required=True, help="Path for the respective DLL to get hashes")

    parser.add_argument("--functions", required=True, nargs="+", help="Functions list to get hashes \"all\"")

    parser.add_argument("--algorithm", type=str, help="Type of encrypt algorithm: \n\t[*] md5\n\t[*] sha1\n\t[*] sha256\n\t[*] djb2")

    parser.add_argument("--save", type=str, help="Name of the output JSON file\n")


    # Divide Arguments
    args = parser.parse_args()

    # Save variables
    path = args.path
    functions = args.functions

    # Algorithm
    algorithm = args.algorithm if args.algorithm else "md5"

    all_functions = get_hashes_functions_from_dll(path, algorithm)

    functions_to_export = []

    # Expotar todas las funciones
    if functions[0].casefold() == "all":
        print("[*] Imprimiendo todas las funciones")

        functions_to_export = all_functions

        print(" ================================================= ")

        for func in all_functions:
            print(f"[*] {func['name']} | Hash: {func['hash']} (Ordinal: {func['ordinal']}) Algorithm: {func['algorithm']}")

    # Cuando se da un .txt
    elif ".txt" in functions[0]:

        try:
            with open(functions[0], 'r', encoding='utf-8') as f:
                funciones_to_search = [
                    linea.strip()
                    for linea in f
                    if linea.strip() and not linea.startswith('#')
                ]

                functions_to_export = find_functions(all_functions, funciones_to_search)
            
        except FileNotFoundError:
            print(f"[-] The file {functions[0]} doesnt exist")
            exit(0)
            
        except Exception as e:
            print(f"[-] Error reading file: {e}")
            exit(0)
   

    # Funcion filtrada
    else:
        print(f"[*] Searching {len(functions)} function(s)...")
        print(" =================================================")

        functions_to_export = find_functions(all_functions, functions)
        
        print(" =================================================")
        print(f"[*] Found: {len(functions_to_export)} of {len(functions)} functions")

    # Guardar en JSON
    if args.save and len(functions_to_export) > 0:
        save_in_json(functions_to_export, args.save)


