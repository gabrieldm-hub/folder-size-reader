from datetime import datetime as dt
from tabulate import tabulate
from time import sleep
from lib import text
import pandas as pd
import os

class Menu:
    def __init__(self):
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
        except Exception as e:
            raise Exception(e)
    def start(self):
        try:
            folder = ''
            
            while folder.lower() != 'exit':
                print(f"Enter the root folder to read or type '{text.RED}exit{text.RESET}' to terminate the script")
                folder = input("Root folder: ")

                if folder.lower() != 'exit':
                    if os.path.exists(folder):
                        if os.path.isdir(folder):
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"{text.GREEN}SUCCESS{text.RESET}: Begining in '{folder}'. This may take a while...\n")
                            try:
                                start = dt.now()
                                get_folder_size_detailed = GetFolderSizeDetailed(folder=folder)
                                get_folder_size_detailed.start()
                                print(f"\nTime spent: {dt.now()-start}\n")
                            except Exception as e:
                                print(f"\n{text.RED}FAIL{text.RESET}: {e}\n")
                        else:
                            # os.system('cls' if os.name == 'nt' else 'clear')
                            print(f"\n{text.RED}FAIL{text.RESET}: The path '{folder}' refers to a {text.RED}{text.UNDERLINE}FILE{text.RESET}. A {text.GREEN}{text.UNDERLINE}FOLDER{text.RESET} is needed!{text.RESET}\n")
                        pass
                    else:
                        # os.system('cls' if os.name == 'nt' else 'clear')
                        print(f"\n{text.RED}FAIL{text.RESET}: Folder '{folder}' does not exist!{text.RESET}\n")
            else:
                print()
                bye = ["Bis bald","Até mais","See you soon"]
                for i in range(len(bye)):
                    print(f"{text.CYAN}{bye[i]}... =){text.RESET}{text.CLEAR}",end="\r",flush=True)
                    sleep(0.3)
                print()
                    

        except Exception as e:
            raise Exception(e)

class GetFolderSizeDetailed:
    def __init__(self,folder):
        try:
            self.root = folder
        except Exception as e:
            raise Exception(e)
    
    def start(self):
        try:
            df = pd.DataFrame(columns=["NAME","TYPE","SIZE_HUMAN","SIZE_ORIGINAL"])
            
            #FOLDER
            folders = [{"NAME": f,"TYPE": "FOLDER"} for f in os.listdir(self.root) if os.path.isdir(os.path.join(self.root,f))]
            folders_qtd = len(folders)
            print("{:<14} {:>6}".format("Total folders:",folders_qtd))

            #FILE
            files = [{"NAME": f,"TYPE": "FILE"} for f in os.listdir(self.root) if os.path.isfile(os.path.join(self.root,f))]
            files_qtd = len(files)
            print("{:<14} {:>6}".format("Total files:",files_qtd))
            
            if folders_qtd == 0 and files_qtd == 0:
                raise Exception(f"{text.YELLOW}There are no files and folders in '{self.root}'!{text.RESET}")
            
            # TREATING FOLDERS
            
            if folders_qtd > 0:
                print("\nreading folders")
                folders_read = 0
                start_ = dt.now()
                for folder in folders:
                    print("Loading [{:>6.2f}%]: {}{}".format((folders_read/folders_qtd)*100,folder["NAME"],text.CLEAR),end="\r",flush=True)
                    folder["SIZE_ORIGINAL"] = self._read_folder(folder=folder["NAME"])
                    folder["SIZE_HUMAN"] = self._humanize(size=folder["SIZE_ORIGINAL"])
                    folders_read+=1
                    print("Loading [{:>6.2f}%]: {}{}".format((folders_read/folders_qtd)*100,f"DONE [{dt.now()-start_}]" if folders_read == folders_qtd else folder["NAME"],text.CLEAR),end="\r",flush=True)
            else:
                folders = [{"NAME":"","TYPE":"","SIZE_HUMAN":None,"SIZE_ORIGINAL":None}]
                print(f"{text.YELLOW}There are no folders!{text.RESET}")
            
            df_folder = pd.DataFrame(folders)
            # END TREATING FOLDERS

            # TREATING FILES
            print()
            if files_qtd > 0:
                print("\nreading files")
                files_read = 0
                start_ = dt.now()
                for file_ in files:
                    print("Loading [{:>6.2f}%]: {}{}".format((files_read/files_qtd)*100,file_["NAME"],text.CLEAR),end="\r",flush=True)
                    file_["SIZE_ORIGINAL"] = self._read_file(file_=file_["NAME"])
                    file_["SIZE_HUMAN"] = self._humanize(size=file_["SIZE_ORIGINAL"])
                    files_read+=1
                    print("Loading [{:>6.2f}%]: {}{}".format((files_read/files_qtd)*100,f"DONE [{dt.now()-start_}]" if files_read == files_qtd else file_["NAME"],text.CLEAR),end="\r",flush=True)
                
            else:
                files = [{"NAME":"","TYPE":"","SIZE_HUMAN":None,"SIZE_ORIGINAL":None}]
                print(f"{text.YELLOW}There are no files!{text.RESET}")
            
            df_file = pd.DataFrame(files)
            # TREATING FILES

            df = pd.concat([df_folder,df_file],ignore_index=True)
            df.sort_values(by="SIZE_ORIGINAL",ascending=False,inplace=True)
            
            print("\n")
            with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                print(tabulate(df, showindex=False, headers=df.columns, colalign=("left","left","right","right")))
            
            print()

            total_size_ori = df["SIZE_ORIGINAL"].sum()
            total_size_ori_str = f"{text.YELLOW}{total_size_ori}{text.RESET}"

            total_size_hum = self._humanize(size=total_size_ori)
            total_size_hum_str = f"{text.YELLOW}{total_size_hum}{text.RESET}"

            total_size_ori_len = len(total_size_ori_str)
            total_size_hum_len = len(total_size_hum_str)

            format_max = total_size_ori_len if total_size_ori_len >= total_size_hum_len else total_size_hum_len
            # print(format_max)
            print("{:.<25}: {:>{}}".format("Total size [human]",total_size_hum_str,format_max))
            print("{:.<25}: {:>{}}".format("Total size [original]",total_size_ori_str,format_max))
            
        
        except Exception as e:
            raise Exception(e)
    
    def _read_folder(self,folder):
        try:
            
            # for fo in folders:
            size_original = 0
            for dirpath, dirnames, filenames in os.walk(os.path.join(self.root,folder)):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    # skip if it is symbolic link
                    if not os.path.islink(fp):
                        s = os.path.getsize(fp)
                    else:
                        s = 0
                    size_original += s

            return size_original
        except Exception as e:
            print(e)
            return 0
    
    def _read_file(self,file_):
        try:
            
            fp = os.path.join(self.root, file_)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                size_original = os.path.getsize(fp)
            else:
                size_original = 0

            return size_original
        except Exception as e:
            print(e)
            return 0
    
    def _humanize(self,size):
        try:
            if size/(1024*1024*1024) > 1:
                size_human = "{:.2f} GB".format(size/(1024*1024*1024))
            elif size/(1024*1024) > 1:
                size_human = "{:.2f} MB".format(size/(1024*1024))
            elif size/(1024) > 1:
                size_human = "{:.2f} KB".format(size/(1024))
            else:
                size_human = "{} KB".format(size)

            return size_human
        except Exception as e:
            raise Exception(e)