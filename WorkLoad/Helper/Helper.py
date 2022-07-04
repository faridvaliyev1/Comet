class Helper:
    def get_workloads():
        file=open("Data/workload.txt","r")
        workloads=[]
        workload=[]
        for line in file.readlines():
            if "#" in line:
                continue
            elif "{" in line:
                workload=[]
            elif "}" in line:
                workloads.append(workload)
                workload=[]
            elif ":" in line:
                for word in line.split():
                    if ":" in word:
                        workload.append(word.replace(":","_"))


        return workloads