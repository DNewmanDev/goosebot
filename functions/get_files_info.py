import os
def get_files_info(working_directory, directory="."):
        try: 
            working_dir_abs=os.path.abspath(working_directory) #grab absolute path of working dir

            target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
            
            valid_target_dir= os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
            if valid_target_dir == False:
               return(f'Error: Cannot list "{directory}", unauthorized access')
            if os.path.isdir(target_dir) == False:
              return(f'Error: "{directory}" is not a directory')
            response=[]
            for item in os.listdir(target_dir):
                path = os.path.join(target_dir, item)
               
                response.append(f" - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")

            return "\n".join(response)
        except Exception as e:
            return f"ERROR: {str(e)}"
