def run_sequence(values):
    """Run a simple sequence and print each step."""
    for index, value in enumerate(values, start=1):
        print(f"Step {index}: {value}")

        #call python file in same folder with name extract_scn_to_scn.py
        if value == "extract scn to scn":
            import extract_scn_to_scn
            extract_scn_to_scn.merge_text_files_to_csv(r"D:\ITH\tempdownload\ca\202604\sc_scn_5dgs_bak", r"D:\ITH\tempdownload\ca\202604\extract_scanner_data.csv") 
        elif value == "extract ist to ist":
            import extract_ist_to_ist
            extract_ist_to_ist.main()
        elif value == "lookup hw sc ist":
            import lookup_hw_sc_ist
            lookup_hw_sc_ist.main()
        elif value == "lookup store sc":
            import lookup_store_sc
            lookup_store_sc.main()
        elif value == "count sc pos scanner model":
            import count_sc_pos_scanner_model
            count_sc_pos_scanner_model.main()
        elif value == "lookup store pos":
            import lookup_store_pos
            lookup_store_pos.main()



if __name__ == "__main__":
    sequence = ["start", "load data", "process", "finish"]
    inputfolder = r"D:\ITH\tempdownload\ca\202604"
    outputfolder = r"D:\ITH\tempdownload\ca\202604\output"
    run_sequence(sequence)
