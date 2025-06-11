# %%
from imports import *

# %%
data_frames = []
data_frame_prev_data = []

read_rows = 0
read_job_order = ""
job_order_materials = ""

is_line_in = ""

# %%
def check_job_orders():
    global data_frames
    global data_frame_prev_data
    global read_rows
    global read_job_order

    global is_line_in

    read_rows = 0
    read_job_order = ""

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    main_dir = r'\\192.168.2.19\ai_team\AI Program\Outputs\JobOrder'
    os.chdir(main_dir)
    data_frames = pd.read_csv('JobOrderSerials.csv', encoding='latin1')

    read_job_order = data_frames["Job Order No"].tail(1).values[0]
    return read_job_order

# %%
def find_materials():
    global job_order_materials
    global read_job_order

    
    current_year = datetime.datetime.now().year

    
    folder_name_current_with_dollar = f"{current_year}$"
    folder_name_current_without_dollar = f"{current_year}"

    
    file_path_current_with_dollar = fr'\\192.168.2.19\production\{folder_name_current_with_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'

    
    if os.path.exists(file_path_current_with_dollar):
        try:
            job_order_materials = pd.read_excel(file_path_current_with_dollar)
            if "Material" in job_order_materials.columns:
                job_order_materials = job_order_materials["Material"]
            else:
                print(f"'Material' column not found in the file: {file_path_current_with_dollar}")
        except Exception as e:
            print(f"Error reading file in current year with dollar sign: {e}")
    else:
        
        file_path_current_without_dollar = fr'\\192.168.2.19\production\{folder_name_current_without_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
        if os.path.exists(file_path_current_without_dollar):
            try:
                job_order_materials = pd.read_excel(file_path_current_without_dollar)
                if "Material" in job_order_materials.columns:
                    job_order_materials = job_order_materials["Material"]
                else:
                    print(f"'Material' column not found in the file: {file_path_current_without_dollar}")
            except Exception as e:
                print(f"Error reading file in current year without dollar sign: {e}")
        else:
            
            previous_year = current_year - 1
            folder_name_prev_with_dollar = f"{previous_year}$"
            folder_name_prev_without_dollar = f"{previous_year}"

            
            file_path_prev_with_dollar = fr'\\192.168.2.19\{folder_name_prev_with_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
            if os.path.exists(file_path_prev_with_dollar):
                try:
                    job_order_materials = pd.read_excel(file_path_prev_with_dollar)
                    if "Material" in job_order_materials.columns:
                        job_order_materials = job_order_materials["Material"]
                    else:
                        print(f"'Material' column not found in the file: {file_path_prev_with_dollar}")
                except Exception as e:
                    print(f"Error reading file in previous year with dollar sign: {e}")
            else:
                
                file_path_prev_without_dollar = fr'\\192.168.2.19\{folder_name_prev_without_dollar}\1. Document for Production Admin\8. JOB ORDER MATERIAL LIST\{read_job_order}.xlsx'
                if os.path.exists(file_path_prev_without_dollar):
                    try:
                        job_order_materials = pd.read_excel(file_path_prev_without_dollar)
                        if "Material" in job_order_materials.columns:
                            job_order_materials = job_order_materials["Material"]
                        else:
                            print(f"'Material' column not found in the file: {file_path_prev_without_dollar}")
                    except Exception as e:
                        print(f"Error reading file in previous year without dollar sign: {e}")
                else:
                    print(f"File not found: {file_path_current_with_dollar}, {file_path_current_without_dollar}, {file_path_prev_with_dollar}, and {file_path_prev_without_dollar}")

# %%
# def write_done_in_job_order():
#     global data_frames
#     global data_frame_prev_data
#     global read_rows
#     global read_job_order
#     global is_line_in

#     data_frames["Checking"] = data_frames['Checking'].astype(object)
#     data_frames.loc[read_rows, "Checking"] = "Done"

#     file_dir = r'\\192.168.2.19\ai_team\AI Program\Outputs\JobOrder'
#     os.chdir(file_dir)
#     print(os.getcwd())


#     if is_line_in:
#         new_val = pd.concat([data_frames], axis=0, ignore_index=True)
#         wire_frame = new_val
#         wire_frame.to_csv('JobOrderSerials.csv', index=False)
    
#     else:
#         new_val = pd.concat([data_frame_prev_data, data_frames], axis=0, ignore_index=True)
#         wire_frame = new_val
#         wire_frame.to_csv('JobOrderSerials.csv', index=False)

# %%
# DTManager.GetDateToday()
check_job_orders()
read_job_order
find_materials()
job_order_materials



