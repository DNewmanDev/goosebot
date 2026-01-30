from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_content
def main():
    print("Result for current directory:")
    print(get_files_info("calculator", "."))
    print()
    
    print("Result for 'pkg' directory:")
    print(get_files_info("calculator", "pkg"))
    print()
    
    print("Result for '/bin' directory:")
    print(get_files_info("calculator", "/bin"))
    print()
    
    print("Result for '../' directory:")
    print(get_files_info("calculator", "../"))


if __name__ == "__main__":
    main()